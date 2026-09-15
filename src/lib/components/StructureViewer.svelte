<script lang="ts">
  import { surveillance, resolveAssetUrl } from '$lib/stores/surveillanceStore.svelte';
  import { getVelocityColor, getVelocityRgb } from '$lib/utils/colorScales';
  import { onMount } from 'svelte';
  import * as THREE from 'three';

  let container: HTMLDivElement;
  let canvas2d: HTMLCanvasElement;
  let renderer: THREE.WebGLRenderer | null = null;
  let scene: THREE.Scene | null = null;
  let camera: THREE.PerspectiveCamera | null = null;
  let residueMeshes: THREE.InstancedMesh | null = null;
  let atomPositions: { codon: number; pos: [number, number, number] }[] = [];
  
  let isRotating = $state(true);
  let hasWebGL = $state(true);
  let viewMode = $state<'3d' | '2d'>('3d');

  // Parse CA (Carbon Alpha) backbone atoms from PDB for 3D ribbon / sphere representation
  async function loadPdbCoordinates(pdbId: string) {
    try {
      const url = resolveAssetUrl(`structures/${pdbId}.pdb`);
      const res = await fetch(url);
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
      if (hasWebGL && renderer) {
        build3DProtein();
      } else {
        render2dSchematic();
      }
    } catch (e) {
      console.warn('Could not load PDB:', e);
      render2dSchematic();
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
        color.setRGB(0.2, 0.9, 1.0);
      } else if (v > 0.001) {
        const [r, g, b] = getVelocityRgb(v, 0.035);
        color.setRGB(r / 255, g / 255, b / 255);
      } else {
        color.setRGB(0.18, 0.24, 0.33);
      }
      residueMeshes.setColorAt(i, color);
    }

    residueMeshes.instanceColor.needsUpdate = true;
  }

  function render2dSchematic() {
    if (!canvas2d || !container) return;
    const ctx = canvas2d.getContext('2d');
    if (!ctx) return;

    const w = container.clientWidth;
    const h = container.clientHeight;
    const dpr = window.devicePixelRatio || 1;

    canvas2d.width = w * dpr;
    canvas2d.height = h * dpr;
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    const isH5N1 = surveillance.currentPathogen === 'avian-flu-h5n1';
    const totalCodons = isH5N1 ? 568 : 1273;
    const padding = { left: 40, right: 40, top: 45, bottom: 45 };
    const drawW = w - padding.left - padding.right;

    // Domain definitions
    const domains = isH5N1
      ? [
          { name: 'Signal', start: 1, end: 16, color: '#64748b' },
          { name: 'HA1 (Head)', start: 17, end: 340, color: '#0ea5e9' },
          { name: 'Receptor Site (RBS)', start: 130, end: 230, color: '#ef4444' },
          { name: 'HA2 (Stem)', start: 341, end: 568, color: '#10b981' },
        ]
      : [
          { name: 'Signal', start: 1, end: 13, color: '#64748b' },
          { name: 'NTD', start: 14, end: 305, color: '#0ea5e9' },
          { name: 'RBD', start: 319, end: 541, color: '#f59e0b' },
          { name: 'RBM', start: 437, end: 508, color: '#ef4444' },
          { name: 'S1/S2', start: 681, end: 686, color: '#ec4899' },
          { name: 'S2 Core', start: 686, end: 1273, color: '#10b981' },
        ];

    // 1. Draw Protein Backbone Ribbon Track
    const centerY = h / 2;
    const trackH = 14;

    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.roundRect(padding.left, centerY - trackH / 2, drawW, trackH, 6);
    ctx.fill();

    // 2. Draw Domains
    for (const d of domains) {
      const x1 = padding.left + (d.start / totalCodons) * drawW;
      const x2 = padding.left + (d.end / totalCodons) * drawW;
      const dW = Math.max(3, x2 - x1);

      ctx.fillStyle = `${d.color}aa`;
      ctx.fillRect(x1, centerY - trackH / 2, dW, trackH);

      // Domain Label
      ctx.fillStyle = d.color;
      ctx.font = '9px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText(d.name, (x1 + x2) / 2, centerY - trackH / 2 - 8);
    }

    // 3. Draw Active Residue Velocity Peaks
    const velMap = surveillance.activeResidueVelocities;
    const focal = surveillance.focalCodon;

    if (velMap.size > 0) {
      for (const [codon, vel] of velMap.entries()) {
        if (vel <= 0.0005) continue;
        const x = padding.left + (codon / totalCodons) * drawW;
        const isFocal = focal === codon;
        const peakH = Math.min(45, (vel / 0.035) * 40);
        const color = getVelocityColor(vel, 0.035);

        // Velocity Spike
        ctx.strokeStyle = color;
        ctx.lineWidth = isFocal ? 2.5 : 1.5;
        ctx.beginPath();
        ctx.moveTo(x, centerY + trackH / 2);
        ctx.lineTo(x, centerY + trackH / 2 + peakH);
        ctx.stroke();

        // Glow head
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, centerY + trackH / 2 + peakH, isFocal ? 4 : 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // 4. Highlight Focal Codon
    if (focal && focal <= totalCodons) {
      const fx = padding.left + (focal / totalCodons) * drawW;
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(fx, centerY, 12, 0, Math.PI * 2);
      ctx.stroke();

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 10px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`Codon ${focal}`, fx, centerY + trackH / 2 + 58);
    }

    // Header info on canvas
    ctx.fillStyle = '#94a3b8';
    ctx.font = '10px JetBrains Mono, monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`${isH5N1 ? 'Hemagglutinin HA' : 'Spike Glycoprotein S'} (1–${totalCodons} aa)`, padding.left, h - 14);
  }

  function initThree(): (() => void) | undefined {
    if (!container) return;

    try {
      // Test WebGL support
      const testCanvas = document.createElement('canvas');
      const gl = testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl');
      if (!gl) {
        hasWebGL = false;
        viewMode = '2d';
        render2dSchematic();
        return;
      }

      const width = container.clientWidth;
      const height = container.clientHeight;

      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(45, width / height, 1, 1000);
      camera.position.set(0, 0, 140);

      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(width, height);
      renderer.setPixelRatio(window.devicePixelRatio || 1);
      container.appendChild(renderer.domElement);
      hasWebGL = true;

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
        if (renderer && scene && camera && viewMode === '3d') {
          renderer.render(scene, camera);
        }
      }
      animate();

      return () => {
        cancelAnimationFrame(frameId);
        renderer?.dispose();
      };
    } catch (e) {
      console.warn('WebGL init failed, using 2D fallback:', e);
      hasWebGL = false;
      viewMode = '2d';
      render2dSchematic();
      return undefined;
    }
  }

  $effect(() => {
    const _v = surveillance.activeResidueVelocities;
    const _f = surveillance.focalCodon;
    if (hasWebGL && viewMode === '3d') {
      updateResidueColors();
    } else {
      render2dSchematic();
    }
  });

  $effect(() => {
    const pid = surveillance.currentPathogen;
    const pdb = pid === 'avian-flu-h5n1' ? '4HMG' : '7KRR';
    loadPdbCoordinates(pdb);
  });

  onMount(() => {
    const cleanup = initThree();

    const observer = new ResizeObserver(() => {
      if (renderer && camera && container && viewMode === '3d') {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      } else {
        render2dSchematic();
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
  <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/60 select-none z-10 shrink-0">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT C: 3D STRUCTURAL DYNAMICS</span>
      <span class="text-[10px] font-mono text-slate-500">{hasWebGL && viewMode === '3d' ? 'Mol* WebGL' : '2D Schematic'}</span>
    </div>

    <!-- Controls -->
    <div class="flex items-center space-x-2 text-[10px] font-mono">
      {#if hasWebGL}
        <button
          type="button"
          onclick={() => (viewMode = viewMode === '3d' ? '2d' : '3d')}
          class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 transition-colors"
        >
          {viewMode === '3d' ? '2D Map' : '3D View'}
        </button>
      {/if}
      <button
        type="button"
        onclick={() => (isRotating = !isRotating)}
        class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
      >
        {isRotating ? 'Pause Spin' : 'Resume Spin'}
      </button>
      <span class="text-slate-500">PDB: {surveillance.currentPathogen === 'avian-flu-h5n1' ? '4HMG (HA)' : '7KRR (Spike)'}</span>
    </div>
  </div>

  <!-- Structure Container -->
  <div class="flex-1 w-full h-full relative overflow-hidden" bind:this={container}>
    <!-- 2D Canvas Fallback / Mode -->
    <canvas
      bind:this={canvas2d}
      class="absolute inset-0 w-full h-full block {hasWebGL && viewMode === '3d' ? 'pointer-events-none opacity-0' : 'opacity-100'}"
    ></canvas>

    <!-- Legend Overlay Badge -->
    <div class="absolute bottom-2 left-3 pointer-events-none text-[10px] font-mono text-slate-400 bg-dark-950/80 px-2 py-1 rounded border border-slate-800/60 backdrop-blur z-10">
      Residue Overpaint = Instantaneous Selection Intensity at Cursor Date
    </div>
  </div>
</div>
