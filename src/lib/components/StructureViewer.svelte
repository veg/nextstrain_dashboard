<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { getVelocityColor, getVelocityRgb } from '$lib/utils/colorScales';
  import { onMount } from 'svelte';
  import * as THREE from 'three';

  let container: HTMLDivElement;
  let renderer: THREE.WebGLRenderer | null = null;
  let scene: THREE.Scene;
  let camera: THREE.PerspectiveCamera;
  let residueMeshes: THREE.InstancedMesh | null = null;
  let atomPositions: { codon: number; pos: [number, number, number] }[] = [];
  let isRotating = $state(true);

  // Parse CA (Carbon Alpha) backbone atoms from PDB for 3D ribbon / sphere representation
  async function loadPdbCoordinates(pdbId: string) {
    try {
      const res = await fetch(`/structures/${pdbId}.pdb`);
      if (!res.ok) return;
      const text = await res.text();
      const lines = text.split('\n');

      const coords: { codon: number; pos: [number, number, number] }[] = [];
      for (const line of lines) {
        if (line.startsWith('ATOM') || line.startsWith('HETATM')) {
          const atomName = line.substring(12, 16).trim();
          if (atomName === 'CA') {
            const resSeq = parseInt(line.substring(22, 26).trim());
            const x = parseFloat(line.substring(30, 38).trim());
            const y = parseFloat(line.substring(38, 46).trim());
            const z = parseFloat(line.substring(46, 54).trim());
            coords.push({ codon: resSeq, pos: [x, y, z] });
          }
        }
      }
      atomPositions = coords;
      build3DProtein();
    } catch (e) {
      console.warn('Could not load PDB:', e);
    }
  }

  function build3DProtein() {
    if (!scene || !atomPositions.length) return;

    if (residueMeshes) {
      scene.remove(residueMeshes);
      residueMeshes.geometry.dispose();
      residueMeshes = null;
    }

    // Center coordinates
    let avgX = 0, avgY = 0, avgZ = 0;
    for (const a of atomPositions) {
      avgX += a.pos[0];
      avgY += a.pos[1];
      avgZ += a.pos[2];
    }
    avgX /= atomPositions.length;
    avgY /= atomPositions.length;
    avgZ /= atomPositions.length;

    const count = atomPositions.length;
    const geom = new THREE.SphereGeometry(1.2, 12, 12);
    const mat = new THREE.MeshStandardMaterial({ roughness: 0.3, metalness: 0.2 });
    residueMeshes = new THREE.InstancedMesh(geom, mat, count);

    const dummy = new THREE.Object3D();
    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      const a = atomPositions[i];
      dummy.position.set(a.pos[0] - avgX, a.pos[1] - avgY, a.pos[2] - avgZ);
      dummy.updateMatrix();
      residueMeshes.setMatrixAt(i, dummy.matrix);

      // Default coloring
      color.setRGB(0.2, 0.3, 0.4);
      residueMeshes.setColorAt(i, color);
    }

    residueMeshes.instanceMatrix.needsUpdate = true;
    if (residueMeshes.instanceColor) residueMeshes.instanceColor.needsUpdate = true;
    scene.add(residueMeshes);

    updateResidueColors();
  }

  function updateResidueColors() {
    if (!residueMeshes || !residueMeshes.instanceColor || !atomPositions.length) return;

    const velMap = surveillance.activeResidueVelocities;
    const focal = surveillance.focalCodon;
    const color = new THREE.Color();

    for (let i = 0; i < atomPositions.length; i++) {
      const a = atomPositions[i];
      const v = velMap.get(a.codon) || 0;
      const isFocal = focal === a.codon;

      if (isFocal) {
        // Blazing cyan for focal codon
        color.setRGB(0.2, 0.9, 1.0);
      } else if (v > 0.001) {
        // High velocity flame
        const [r, g, b] = getVelocityRgb(v, 0.035);
        color.setRGB(r / 255, g / 255, b / 255);
      } else {
        // Muted slate backbone
        color.setRGB(0.18, 0.24, 0.33);
      }
      residueMeshes.setColorAt(i, color);
    }

    residueMeshes.instanceColor.needsUpdate = true;
  }

  function initThree() {
    if (!container) return;
    const width = container.clientWidth;
    const height = container.clientHeight;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(45, width / height, 1, 1000);
    camera.position.set(0, 0, 140);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio || 1);
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(50, 50, 100);
    scene.add(dirLight);

    let frameId: number;
    function animate() {
      frameId = requestAnimationFrame(animate);
      if (residueMeshes && isRotating) {
        residueMeshes.rotation.y += 0.003;
      }
      if (renderer && scene && camera) {
        renderer.render(scene, camera);
      }
    }
    animate();

    return () => {
      cancelAnimationFrame(frameId);
      renderer?.dispose();
    };
  }

  $effect(() => {
    // Re-color when velocities or focal codon updates
    const _v = surveillance.activeResidueVelocities;
    const _f = surveillance.focalCodon;
    updateResidueColors();
  });

  $effect(() => {
    // Load PDB when pathogen changes
    const pid = surveillance.currentPathogen;
    const pdb = pid === 'avian-flu-h5n1' ? '4HMG' : '7KRR';
    loadPdbCoordinates(pdb);
  });

  onMount(() => {
    const cleanup = initThree();
    loadPdbCoordinates('7KRR');
    const observer = new ResizeObserver(() => {
      if (renderer && camera && container) {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      }
    });
    observer.observe(container);

    return () => {
      cleanup?.();
      observer.disconnect();
    };
  });
</script>

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative">
  <!-- Header Bar -->
  <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/60 select-none z-10">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT C: 3D STRUCTURAL DYNAMICS</span>
      <span class="text-[10px] font-mono text-slate-500">Mol* / WebGL</span>
    </div>

    <!-- Controls -->
    <div class="flex items-center space-x-2 text-[10px] font-mono">
      <button
        onclick={() => (isRotating = !isRotating)}
        class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
      >
        {isRotating ? 'Pause Spin' : 'Resume Spin'}
      </button>
      <span class="text-slate-500">PDB: {surveillance.currentPathogen === 'avian-flu-h5n1' ? '4HMG (HA)' : '7KRR (Spike)'}</span>
    </div>
  </div>

  <!-- 3D Canvas -->
  <div class="flex-1 w-full h-full relative" bind:this={container}>
    <!-- Glow Overlay Badge -->
    <div class="absolute bottom-2 left-3 pointer-events-none text-[10px] font-mono text-slate-400 bg-dark-950/80 px-2 py-1 rounded border border-slate-800/60 backdrop-blur z-10">
      Residue Overpaint = Instantaneous Selection Intensity at Cursor Date
    </div>
  </div>
</div>
