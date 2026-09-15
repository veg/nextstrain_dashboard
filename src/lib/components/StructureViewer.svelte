<script lang="ts">
  import { surveillance, resolveAssetUrl } from '$lib/stores/surveillanceStore.svelte';
  import { getVelocityColor, getVelocityRgb } from '$lib/utils/colorScales';
  import { onMount } from 'svelte';
  import * as THREE from 'three';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

  let container: HTMLDivElement;
  let canvas2d: HTMLCanvasElement;
  let renderer: THREE.WebGLRenderer | null = null;
  let scene: THREE.Scene | null = null;
  let camera: THREE.PerspectiveCamera | null = null;
  let controls: OrbitControls | null = null;
  let residueMeshes: THREE.InstancedMesh | null = null;
  let focalBeaconMesh: THREE.Mesh | null = null;
  let atomPositions: { codon: number; pos: [number, number, number]; centeredPos: [number, number, number] }[] = [];
  let raycaster = new THREE.Raycaster();
  let mouse = new THREE.Vector2();

  let isRotating = $state(false);
  let hasWebGL = $state(true);
  let viewMode = $state<'3d' | '2d'>('3d');
  let colorMode = $state<'velocity' | 'domain' | 'sector'>('domain');

  let hoveredResidue = $state<{
    codon: number;
    domain: { name: string; color: string } | null;
    vel: number;
    sector: { id: number; name: string; coherence: number } | null;
    screenX: number;
    screenY: number;
  } | null>(null);

  const DOMAINS_SARS = [
    { name: 'Signal', start: 1, end: 13, color: '#64748b' },
    { name: 'NTD', start: 14, end: 305, color: '#0ea5e9' },
    { name: 'RBD', start: 319, end: 541, color: '#f59e0b' },
    { name: 'RBM', start: 437, end: 508, color: '#ef4444' },
    { name: 'S1/S2 Furin', start: 681, end: 686, color: '#ec4899' },
    { name: 'S2 Core', start: 687, end: 1273, color: '#10b981' },
  ];

  const DOMAINS_H5N1 = [
    { name: 'Signal', start: 1, end: 16, color: '#64748b' },
    { name: 'HA1 (Head)', start: 17, end: 340, color: '#0ea5e9' },
    { name: 'RBS (Receptor Site)', start: 130, end: 230, color: '#ef4444' },
    { name: 'HA2 (Stem)', start: 341, end: 568, color: '#10b981' },
  ];

  const SECTOR_COLORS = [
    '#06b6d4', // Cyan
    '#a855f7', // Purple
    '#10b981', // Emerald
    '#f59e0b', // Amber
    '#f43f5e', // Rose
    '#3b82f6', // Blue
    '#ec4899', // Pink
    '#8b5cf6', // Violet
    '#14b8a6', // Teal
  ];

  function getActiveDomains() {
    return surveillance.currentPathogen === 'avian-flu-h5n1' ? DOMAINS_H5N1 : DOMAINS_SARS;
  }

  function getCodonDomain(codon: number): { name: string; color: string } | null {
    const domains = getActiveDomains();
    for (let i = domains.length - 1; i >= 0; i--) {
      if (codon >= domains[i].start && codon <= domains[i].end) {
        return domains[i];
      }
    }
    return null;
  }

  function getCodonSector(codon: number): { id: number; name: string; coherence: number } | null {
    const sectors = surveillance.epistasisGraph?.sectors;
    if (!sectors) return null;
    for (const s of sectors) {
      if (s.members.includes(codon)) {
        return { id: s.sector_id, name: s.name || `Sector #${s.sector_id}`, coherence: s.coherence };
      }
    }
    return null;
  }

  // Parse CA (Carbon Alpha) backbone atoms from PDB
  async function loadPdbCoordinates(pdbId: string) {
    try {
      const url = resolveAssetUrl(`structures/${pdbId}.pdb`);
      const res = await fetch(url);
      if (!res.ok) return;
      const text = await res.text();
      const lines = text.split('\n');

      const rawCoords: { codon: number; pos: [number, number, number] }[] = [];
      let avgX = 0, avgY = 0, avgZ = 0;

      for (const line of lines) {
        if (line.startsWith('ATOM') || line.startsWith('HETATM')) {
          const atomName = line.substring(12, 16).trim();
          if (atomName === 'CA') {
            const resSeq = parseInt(line.substring(22, 26).trim());
            const x = parseFloat(line.substring(30, 38).trim());
            const y = parseFloat(line.substring(38, 46).trim());
            const z = parseFloat(line.substring(46, 54).trim());
            rawCoords.push({ codon: resSeq, pos: [x, y, z] });
            avgX += x;
            avgY += y;
            avgZ += z;
          }
        }
      }

      if (rawCoords.length) {
        avgX /= rawCoords.length;
        avgY /= rawCoords.length;
        avgZ /= rawCoords.length;

        atomPositions = rawCoords.map((c) => ({
          codon: c.codon,
          pos: c.pos,
          centeredPos: [c.pos[0] - avgX, c.pos[1] - avgY, c.pos[2] - avgZ],
        }));
      }

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
    if (focalBeaconMesh) {
      scene.remove(focalBeaconMesh);
      focalBeaconMesh.geometry.dispose();
      focalBeaconMesh = null;
    }

    const count = atomPositions.length;
    const geom = new THREE.SphereGeometry(1.3, 14, 14);
    const mat = new THREE.MeshStandardMaterial({
      roughness: 0.35,
      metalness: 0.25,
    });
    residueMeshes = new THREE.InstancedMesh(geom, mat, count);

    const dummy = new THREE.Object3D();
    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      const a = atomPositions[i];
      dummy.position.set(a.centeredPos[0], a.centeredPos[1], a.centeredPos[2]);
      dummy.updateMatrix();
      residueMeshes.setMatrixAt(i, dummy.matrix);

      color.setRGB(0.25, 0.35, 0.45);
      residueMeshes.setColorAt(i, color);
    }

    residueMeshes.instanceMatrix.needsUpdate = true;
    if (residueMeshes.instanceColor) residueMeshes.instanceColor.needsUpdate = true;
    scene.add(residueMeshes);

    // Add Beacon Mesh for focal codon highlighting
    const beaconGeom = new THREE.SphereGeometry(2.4, 16, 16);
    const beaconMat = new THREE.MeshBasicMaterial({
      color: 0x38bdf8,
      wireframe: true,
      transparent: true,
      opacity: 0.85,
    });
    focalBeaconMesh = new THREE.Mesh(beaconGeom, beaconMat);
    focalBeaconMesh.visible = false;
    scene.add(focalBeaconMesh);

    updateResidueColors();
    updateFocalBeacon();
  }

  function updateFocalBeacon() {
    if (!focalBeaconMesh || !atomPositions.length) return;
    const focal = surveillance.focalCodon;
    if (!focal) {
      focalBeaconMesh.visible = false;
      return;
    }

    const atom = atomPositions.find((a) => a.codon === focal);
    if (atom) {
      focalBeaconMesh.position.set(atom.centeredPos[0], atom.centeredPos[1], atom.centeredPos[2]);
      focalBeaconMesh.visible = true;
    } else {
      focalBeaconMesh.visible = false;
    }
  }

  function focusOnCodon(codon: number) {
    if (!camera || !controls || !atomPositions.length) return;
    const atom = atomPositions.find((a) => a.codon === codon);
    if (atom) {
      controls.target.set(atom.centeredPos[0], atom.centeredPos[1], atom.centeredPos[2]);
      controls.update();
    }
  }

  function resetCamera() {
    if (!camera || !controls) return;
    camera.position.set(0, 0, 140);
    controls.target.set(0, 0, 0);
    controls.update();
  }

  function updateResidueColors() {
    if (!residueMeshes || !residueMeshes.instanceColor || !atomPositions.length) return;

    const velMap = surveillance.activeResidueVelocities;
    const focal = surveillance.focalCodon;
    const color = new THREE.Color();
    const sectors = surveillance.epistasisGraph?.sectors || [];

    for (let i = 0; i < atomPositions.length; i++) {
      const a = atomPositions[i];
      const isFocal = focal === a.codon;

      if (isFocal) {
        color.setRGB(0.2, 0.95, 1.0);
      } else if (colorMode === 'velocity') {
        const v = velMap.get(a.codon) || 0;
        if (v > 0.001) {
          const [r, g, b] = getVelocityRgb(v, 0.035);
          color.setRGB(r / 255, g / 255, b / 255);
        } else {
          color.setRGB(0.16, 0.22, 0.30);
        }
      } else if (colorMode === 'domain') {
        const dom = getCodonDomain(a.codon);
        if (dom) {
          color.setStyle(dom.color);
        } else {
          color.setRGB(0.22, 0.28, 0.35);
        }
      } else if (colorMode === 'sector') {
        const sector = getCodonSector(a.codon);
        if (sector) {
          const cIdx = (sector.id - 1) % SECTOR_COLORS.length;
          color.setStyle(SECTOR_COLORS[cIdx >= 0 ? cIdx : 0]);
        } else {
          color.setRGB(0.14, 0.18, 0.24);
        }
      }

      residueMeshes.setColorAt(i, color);
    }

    residueMeshes.instanceColor.needsUpdate = true;
  }

  function handlePointerMove(e: MouseEvent) {
    if (!renderer || !camera || !residueMeshes || !atomPositions.length) {
      hoveredResidue = null;
      return;
    }
    const rect = renderer.domElement.getBoundingClientRect();
    const clientX = e.clientX - rect.left;
    const clientY = e.clientY - rect.top;

    mouse.x = (clientX / rect.width) * 2 - 1;
    mouse.y = -(clientY / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(residueMeshes);

    if (intersects.length > 0 && intersects[0].instanceId !== undefined) {
      const instanceId = intersects[0].instanceId;
      const atom = atomPositions[instanceId];
      if (atom) {
        const codon = atom.codon;
        const domain = getCodonDomain(codon);
        const vel = surveillance.activeResidueVelocities.get(codon) || 0;
        const sector = getCodonSector(codon);

        hoveredResidue = {
          codon,
          domain,
          vel,
          sector,
          screenX: clientX,
          screenY: clientY,
        };
        return;
      }
    }
    hoveredResidue = null;
  }

  function handlePointerClick(e: MouseEvent) {
    if (!renderer || !camera || !residueMeshes || !atomPositions.length) return;
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(residueMeshes);

    if (intersects.length > 0 && intersects[0].instanceId !== undefined) {
      const atom = atomPositions[intersects[0].instanceId];
      if (atom) {
        surveillance.setFocalCodon(atom.codon);
      }
    }
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
    const domains = getActiveDomains();

    // 1. Protein Ribbon Track
    const centerY = h / 2;
    const trackH = 14;

    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.roundRect(padding.left, centerY - trackH / 2, drawW, trackH, 6);
    ctx.fill();

    // 2. Domains
    for (const d of domains) {
      const x1 = padding.left + (d.start / totalCodons) * drawW;
      const x2 = padding.left + (d.end / totalCodons) * drawW;
      const dW = Math.max(3, x2 - x1);

      ctx.fillStyle = `${d.color}cc`;
      ctx.fillRect(x1, centerY - trackH / 2, dW, trackH);

      ctx.fillStyle = d.color;
      ctx.font = '9px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText(d.name, (x1 + x2) / 2, centerY - trackH / 2 - 8);
    }

    // 3. Selection Velocity Spikes
    const velMap = surveillance.activeResidueVelocities;
    const focal = surveillance.focalCodon;

    if (velMap.size > 0) {
      for (const [codon, vel] of velMap.entries()) {
        if (vel <= 0.0005) continue;
        const x = padding.left + (codon / totalCodons) * drawW;
        const isFocal = focal === codon;
        const peakH = Math.min(45, (vel / 0.035) * 40);
        const color = getVelocityColor(vel, 0.035);

        ctx.strokeStyle = color;
        ctx.lineWidth = isFocal ? 2.5 : 1.5;
        ctx.beginPath();
        ctx.moveTo(x, centerY + trackH / 2);
        ctx.lineTo(x, centerY + trackH / 2 + peakH);
        ctx.stroke();

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

    ctx.fillStyle = '#94a3b8';
    ctx.font = '10px JetBrains Mono, monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`${isH5N1 ? 'Hemagglutinin HA' : 'Spike Glycoprotein S'} (1–${totalCodons} aa)`, padding.left, h - 14);
  }

  function initThree(): (() => void) | undefined {
    if (!container) return;

    try {
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

      // OrbitControls with damping
      controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.06;
      controls.rotateSpeed = 0.8;
      controls.zoomSpeed = 1.0;
      controls.panSpeed = 0.8;

      controls.addEventListener('start', () => {
        isRotating = false;
      });

      // Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
      scene.add(ambientLight);

      const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
      dirLight.position.set(60, 80, 100);
      scene.add(dirLight);

      const dirLight2 = new THREE.DirectionalLight(0x38bdf8, 0.4);
      dirLight2.position.set(-60, -80, -50);
      scene.add(dirLight2);

      let frameId: number;
      function animate() {
        frameId = requestAnimationFrame(animate);
        if (controls) controls.update();

        if (residueMeshes && isRotating) {
          residueMeshes.rotation.y += 0.003;
          if (focalBeaconMesh) focalBeaconMesh.rotation.y += 0.003;
        }

        if (focalBeaconMesh && focalBeaconMesh.visible) {
          const s = 1.0 + 0.15 * Math.sin(Date.now() * 0.006);
          focalBeaconMesh.scale.set(s, s, s);
        }

        if (renderer && scene && camera && viewMode === '3d') {
          renderer.render(scene, camera);
        }
      }
      animate();

      return () => {
        cancelAnimationFrame(frameId);
        controls?.dispose();
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
    const _m = colorMode;
    const _p = surveillance.epistasisGraph;
    if (hasWebGL && viewMode === '3d') {
      updateResidueColors();
      updateFocalBeacon();
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

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative select-none">
  <!-- Header Bar -->
  <div class="h-10 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/70 shrink-0 z-10">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT C: 3D STRUCTURAL DYNAMICS</span>
      <span class="text-[10px] font-mono text-slate-500">{hasWebGL && viewMode === '3d' ? 'Mol* Orbit Controls' : '2D Schematic'}</span>
    </div>

    <!-- Controls Toolbar -->
    <div class="flex items-center space-x-2 text-[10px] font-mono">
      <!-- Color Mode Toggles -->
      <div class="flex items-center space-x-1 bg-dark-950 rounded-lg p-0.5 border border-slate-800">
        <button
          type="button"
          onclick={() => (colorMode = 'domain')}
          class="px-2 py-0.5 rounded transition-colors {colorMode === 'domain' ? 'bg-sky-500 text-dark-950 font-bold' : 'text-slate-400 hover:text-slate-200'}"
          title="Color by Structural Domains (NTD, RBD, RBM, HA1, RBS, HA2)"
        >
          Domains
        </button>
        <button
          type="button"
          onclick={() => (colorMode = 'velocity')}
          class="px-2 py-0.5 rounded transition-colors {colorMode === 'velocity' ? 'bg-rose-500 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
          title="Color by Selection Velocity v_s(t) at Scrubber Date"
        >
          Selection v_s(t)
        </button>
        <button
          type="button"
          onclick={() => (colorMode = 'sector')}
          class="px-2 py-0.5 rounded transition-colors {colorMode === 'sector' ? 'bg-purple-500 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
          title="Color by CESI Epistatic Co-selection Sectors"
        >
          CESI Sectors
        </button>
      </div>

      <!-- Rotation Toggle -->
      <button
        type="button"
        onclick={() => (isRotating = !isRotating)}
        class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
        title="Toggle automatic rotation"
      >
        {isRotating ? 'Pause' : 'Spin'}
      </button>

      <!-- Reset Camera Button -->
      <button
        type="button"
        onclick={resetCamera}
        class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
        title="Reset camera zoom and rotation"
      >
        Reset
      </button>

      {#if surveillance.focalCodon}
        <button
          type="button"
          onclick={() => focusOnCodon(surveillance.focalCodon!)}
          class="px-2 py-1 rounded bg-sky-950 text-sky-300 border border-sky-600/50 hover:bg-sky-900 transition-colors"
          title="Center 3D camera on focal codon"
        >
          Focus #{surveillance.focalCodon}
        </button>
      {/if}

      <!-- 2D/3D Mode -->
      {#if hasWebGL}
        <button
          type="button"
          onclick={() => (viewMode = viewMode === '3d' ? '2d' : '3d')}
          class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 transition-colors"
        >
          {viewMode === '3d' ? '2D Map' : '3D View'}
        </button>
      {/if}
    </div>
  </div>

  <!-- Structure Container -->
  <div
    class="flex-1 w-full h-full relative overflow-hidden"
    bind:this={container}
    onmousemove={handlePointerMove}
    onclick={handlePointerClick}
    role="region"
    aria-label="3D molecular structure view"
  >
    <!-- 2D Canvas Fallback / Mode -->
    <canvas
      bind:this={canvas2d}
      class="absolute inset-0 w-full h-full block {hasWebGL && viewMode === '3d' ? 'pointer-events-none opacity-0' : 'opacity-100'}"
    ></canvas>

    <!-- Floating Interactive 3D Tooltip -->
    {#if hoveredResidue}
      {@const posX = Math.min(hoveredResidue.screenX + 16, (container?.clientWidth || 700) - 260)}
      {@const posY = Math.max(12, Math.min(hoveredResidue.screenY - 20, (container?.clientHeight || 400) - 160))}
      <div
        class="absolute pointer-events-none z-30 flex flex-col p-3 rounded-xl bg-dark-950/95 border border-slate-700/90 shadow-2xl backdrop-blur text-xs font-mono max-w-[250px] animate-in fade-in duration-100"
        style="left: {posX}px; top: {posY}px;"
      >
        <!-- Residue Title -->
        <div class="flex items-center justify-between pb-1.5 border-b border-slate-800">
          <div class="flex items-center space-x-1.5 font-bold text-sky-300 text-sm">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            <span>Residue #{hoveredResidue.codon}</span>
          </div>
          {#if hoveredResidue.domain}
            <span
              class="text-[10px] px-1.5 py-0.5 rounded border font-semibold"
              style="background-color: {hoveredResidue.domain.color}22; color: {hoveredResidue.domain.color}; border-color: {hoveredResidue.domain.color}55;"
            >
              {hoveredResidue.domain.name}
            </span>
          {/if}
        </div>

        <!-- Metric Details -->
        <div class="py-2 space-y-1.5 text-[11px]">
          <div class="flex items-center justify-between">
            <span class="text-slate-400">Selection Velocity:</span>
            <div class="flex items-center space-x-1 font-bold">
              <span class="w-2 h-2 rounded-full" style="background-color: {getVelocityColor(hoveredResidue.vel, 0.035)};"></span>
              <span style="color: {hoveredResidue.vel > 0.005 ? '#f43f5e' : '#94a3b8'};">
                {hoveredResidue.vel.toFixed(4)}
              </span>
              <span class="text-[9px] text-slate-500 font-normal">subs/yr</span>
            </div>
          </div>

          {#if hoveredResidue.sector}
            <div class="mt-1 pt-1.5 border-t border-slate-800/80">
              <div class="text-[10px] text-purple-400 font-semibold flex items-center space-x-1">
                <span>🧬 {hoveredResidue.sector.name}</span>
              </div>
              <div class="text-[9px] text-slate-400 mt-0.5">
                Coherence: {hoveredResidue.sector.coherence.toFixed(2)} &bull; Strong Pairwise Epistasis
              </div>
            </div>
          {/if}
        </div>

        <!-- Hint -->
        <div class="pt-1.5 border-t border-slate-800 text-[9px] text-sky-400/80 flex items-center justify-between">
          <span>Click residue to lock codon</span>
          <span>↗</span>
        </div>
      </div>
    {/if}

    <!-- Domain Architecture Legend Strip -->
    <div class="absolute bottom-2 left-3 pointer-events-auto flex items-center space-x-1 text-[10px] font-mono bg-dark-950/85 px-2.5 py-1.5 rounded-lg border border-slate-800/80 backdrop-blur z-10 flex-wrap gap-y-1">
      <span class="text-slate-500 mr-1">Domains:</span>
      {#each getActiveDomains() as dom}
        <button
          type="button"
          onclick={() => {
            colorMode = 'domain';
            surveillance.setFocalCodon(Math.round((dom.start + dom.end) / 2));
            focusOnCodon(Math.round((dom.start + dom.end) / 2));
          }}
          class="px-1.5 py-0.5 rounded flex items-center space-x-1 bg-dark-900 border border-slate-800 hover:border-slate-600 transition-colors"
          title="Click to highlight {dom.name} ({dom.start}–{dom.end})"
        >
          <span class="w-1.5 h-1.5 rounded-full" style="background-color: {dom.color};"></span>
          <span style="color: {dom.color};">{dom.name}</span>
        </button>
      {/each}
    </div>

    <!-- Mouse Interaction Hint -->
    <div class="absolute top-2 right-3 pointer-events-none text-[9px] font-mono text-slate-500 bg-dark-950/80 px-2 py-0.5 rounded border border-slate-800/60 backdrop-blur z-10">
      Drag to rotate &bull; Scroll to zoom &bull; Right-click to pan &bull; Click residue to focus
    </div>
  </div>
</div>
