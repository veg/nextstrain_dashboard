<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { onMount } from 'svelte';
  import * as THREE from 'three';

  let container: HTMLDivElement;
  let canvas2d: HTMLCanvasElement;
  let renderer: THREE.WebGLRenderer | null = null;
  let scene: THREE.Scene | null = null;
  let camera: THREE.PerspectiveCamera | null = null;
  let graphGroup: THREE.Group | null = null;
  let nodeObjects: { id: number; mesh: THREE.Mesh; pos: THREE.Vector3 }[] = [];

  let hasWebGL = $state(true);
  let viewMode = $state<'3d' | '2d'>('3d');
  let hoveredNode = $state<number | null>(null);

  function buildGraph() {
    if (!scene) return;

    if (graphGroup) {
      scene.remove(graphGroup);
      graphGroup.clear();
    }
    graphGroup = new THREE.Group();
    nodeObjects = [];

    const epi = surveillance.epistasisGraph;
    if (!epi || !epi.nodes.length) return;

    const { nodes, edges } = epi;
    const nodeCount = nodes.length;
    const radius = 35;

    // Place nodes on sphere surface with force dispersion
    const nodeMap = new Map<number, THREE.Vector3>();
    const nodeGeom = new THREE.SphereGeometry(1.2, 16, 16);

    nodes.forEach((n, idx) => {
      const phi = Math.acos(-1 + (2 * idx) / Math.max(1, nodeCount));
      const theta = Math.sqrt(nodeCount * Math.PI) * phi;
      const x = radius * Math.cos(theta) * Math.sin(phi);
      const y = radius * Math.sin(theta) * Math.sin(phi);
      const z = radius * Math.cos(phi);
      const pos = new THREE.Vector3(x, y, z);
      nodeMap.set(n.id, pos);

      const isFocal = surveillance.focalCodon === n.id;
      const mat = new THREE.MeshStandardMaterial({
        color: isFocal ? 0x38bdf8 : 0xa855f7,
        roughness: 0.3,
        metalness: 0.4,
      });

      const mesh = new THREE.Mesh(nodeGeom, mat);
      mesh.position.copy(pos);
      graphGroup!.add(mesh);
      nodeObjects.push({ id: n.id, mesh, pos });
    });

    // Draw CESI Edges
    const lineMat = new THREE.LineBasicMaterial({
      color: 0x6366f1,
      transparent: true,
      opacity: 0.35,
    });
    const highlightMat = new THREE.LineBasicMaterial({
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.95,
      linewidth: 2,
    });

    edges.slice(0, 150).forEach((e) => {
      const pA = nodeMap.get(e.source);
      const pB = nodeMap.get(e.target);
      if (!pA || !pB) return;

      const isTouchingFocal = surveillance.focalCodon === e.source || surveillance.focalCodon === e.target;
      const geom = new THREE.BufferGeometry().setFromPoints([pA, pB]);
      const line = new THREE.Line(geom, isTouchingFocal ? highlightMat : lineMat);
      graphGroup!.add(line);
    });

    scene.add(graphGroup);
  }

  function render2dNetwork() {
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

    const epi = surveillance.epistasisGraph;
    if (!epi || !epi.nodes.length) {
      ctx.fillStyle = '#64748b';
      ctx.font = '11px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText('No Epistatic Co-selection Edges (CESI ≥ 1.5)', w / 2, h / 2);
      return;
    }

    const { nodes, edges } = epi;
    const centerX = w / 2;
    const centerY = h / 2;
    const radius = Math.min(w, h) * 0.38;

    // Calculate node 2D positions in concentric or circular orbit
    const posMap = new Map<number, [number, number]>();
    const nodeCount = nodes.length;

    nodes.forEach((n, idx) => {
      const angle = (idx / nodeCount) * Math.PI * 2 - Math.PI / 2;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      posMap.set(n.id, [x, y]);
    });

    // 1. Draw Edges
    const focal = surveillance.focalCodon;
    for (const e of edges.slice(0, 100)) {
      const p1 = posMap.get(e.source);
      const p2 = posMap.get(e.target);
      if (!p1 || !p2) continue;

      const isTouchingFocal = focal === e.source || focal === e.target;
      ctx.beginPath();
      ctx.moveTo(p1[0], p1[1]);
      ctx.lineTo(p2[0], p2[1]);
      ctx.strokeStyle = isTouchingFocal ? '#38bdf8' : 'rgba(168, 85, 247, 0.25)';
      ctx.lineWidth = isTouchingFocal ? 2.0 : 1.0;
      ctx.stroke();
    }

    // 2. Draw Nodes
    for (const n of nodes) {
      const pos = posMap.get(n.id);
      if (!pos) continue;

      const isFocal = focal === n.id;
      const isHovered = hoveredNode === n.id;
      const r = isFocal ? 7 : (isHovered ? 6 : 4.5);

      // Outer glow for focal
      if (isFocal) {
        ctx.fillStyle = 'rgba(56, 189, 248, 0.3)';
        ctx.beginPath();
        ctx.arc(pos[0], pos[1], r + 5, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.fillStyle = isFocal ? '#38bdf8' : '#a855f7';
      ctx.beginPath();
      ctx.arc(pos[0], pos[1], r, 0, Math.PI * 2);
      ctx.fill();

      // Label
      if (isFocal || isHovered || nodes.length <= 25) {
        ctx.fillStyle = isFocal ? '#38bdf8' : '#e2e8f0';
        ctx.font = `${isFocal ? 'bold ' : ''}9px JetBrains Mono, monospace`;
        ctx.textAlign = pos[0] >= centerX ? 'left' : 'right';
        const offset = pos[0] >= centerX ? 8 : -8;
        ctx.fillText(String(n.id), pos[0] + offset, pos[1] + 3);
      }
    }
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
        render2dNetwork();
        return;
      }

      const width = container.clientWidth;
      const height = container.clientHeight;

      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(50, width / height, 1, 1000);
      camera.position.set(0, 0, 85);

      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(width, height);
      renderer.setPixelRatio(window.devicePixelRatio || 1);
      container.appendChild(renderer.domElement);
      hasWebGL = true;

      // Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
      scene.add(ambientLight);

      const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
      dirLight.position.set(30, 40, 50);
      scene.add(dirLight);

      let frameId: number;
      function animate() {
        frameId = requestAnimationFrame(animate);
        if (graphGroup && viewMode === '3d') {
          graphGroup.rotation.y += 0.002;
          graphGroup.rotation.x += 0.001;
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
      console.warn('WebGL init failed in EpistasisGraph, using 2D fallback:', e);
      hasWebGL = false;
      viewMode = '2d';
      render2dNetwork();
      return undefined;
    }
  }

  function handle2dCanvasClick(e: MouseEvent) {
    if (!canvas2d || !container || !surveillance.epistasisGraph) return;
    const rect = canvas2d.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    const w = container.clientWidth;
    const h = container.clientHeight;
    const centerX = w / 2;
    const centerY = h / 2;
    const radius = Math.min(w, h) * 0.38;

    const nodes = surveillance.epistasisGraph.nodes;
    for (let idx = 0; idx < nodes.length; idx++) {
      const angle = (idx / nodes.length) * Math.PI * 2 - Math.PI / 2;
      const nx = centerX + Math.cos(angle) * radius;
      const ny = centerY + Math.sin(angle) * radius;
      const dist = Math.hypot(clickX - nx, clickY - ny);
      if (dist <= 12) {
        surveillance.setFocalCodon(nodes[idx].id);
        break;
      }
    }
  }

  $effect(() => {
    const _e = surveillance.epistasisGraph;
    const _f = surveillance.focalCodon;
    if (hasWebGL && viewMode === '3d') {
      buildGraph();
    } else {
      render2dNetwork();
    }
  });

  onMount(() => {
    const cleanup = initThree();
    if (hasWebGL && viewMode === '3d') {
      buildGraph();
    } else {
      render2dNetwork();
    }

    const observer = new ResizeObserver(() => {
      if (renderer && camera && container && viewMode === '3d') {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      } else {
        render2dNetwork();
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
      <span class="w-2 h-2 rounded-full bg-purple-500"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT E: 3D EPISTATIC CO-SELECTION</span>
      <span class="text-[10px] font-mono text-slate-500">CESI &ge; 1.5</span>
    </div>

    <!-- View Mode Toggle & Status -->
    <div class="flex items-center space-x-2 text-[10px] font-mono">
      {#if hasWebGL}
        <button
          type="button"
          onclick={() => (viewMode = viewMode === '3d' ? '2d' : '3d')}
          class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-purple-300 transition-colors"
        >
          {viewMode === '3d' ? '2D Graph' : '3D Orbit'}
        </button>
      {/if}
      <span class="text-slate-400">
        Sectors: {surveillance.epistasisGraph?.sectors?.length || 0} &bull; Edges: {surveillance.epistasisGraph?.edges?.length || 0}
      </span>
    </div>
  </div>

  <!-- Graph Canvas Container -->
  <div class="flex-1 w-full h-full relative overflow-hidden" bind:this={container}>
    <!-- 2D Network Canvas -->
    <canvas
      bind:this={canvas2d}
      onclick={handle2dCanvasClick}
      class="absolute inset-0 w-full h-full block {hasWebGL && viewMode === '3d' ? 'pointer-events-none opacity-0' : 'opacity-100 cursor-pointer'}"
    ></canvas>

    <!-- Legend Overlay -->
    <div class="absolute bottom-2 left-3 pointer-events-none text-[10px] font-mono text-slate-400 bg-dark-950/80 px-2 py-1 rounded border border-slate-800/60 backdrop-blur z-10">
      Nodes = Codons &bull; Edges = Composite Epistatic Selection Index &bull; Sectors = Co-selected Units
    </div>
  </div>
</div>
