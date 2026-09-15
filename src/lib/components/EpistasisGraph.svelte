<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { onMount } from 'svelte';
  import * as THREE from 'three';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

  let container: HTMLDivElement;
  let canvas2d: HTMLCanvasElement;
  let renderer: THREE.WebGLRenderer | null = null;
  let scene: THREE.Scene | null = null;
  let camera: THREE.PerspectiveCamera | null = null;
  let controls: OrbitControls | null = null;
  let graphGroup: THREE.Group | null = null;
  let nodeObjects: { id: number; mesh: THREE.Mesh; pos: THREE.Vector3; codon: number }[] = [];
  let raycaster = new THREE.Raycaster();
  let mouse = new THREE.Vector2();

  let hasWebGL = $state(true);
  let viewMode = $state<'3d' | '2d'>('3d');
  let selectedSectorId = $state<number | null>(null);
  let isRotating = $state(false);
  let showRoster = $state(true);

  let hoveredNode = $state<{
    codon: number;
    name: string;
    domain: string;
    degree: number;
    sector: { id: number; name: string } | null;
    topPartners: { codon: number; cesi: number }[];
    screenX: number;
    screenY: number;
  } | null>(null);

  const SECTOR_PALETTE = [
    '#06b6d4', // Sector 1: Cyan
    '#a855f7', // Sector 2: Purple
    '#10b981', // Sector 3: Emerald
    '#f59e0b', // Sector 4: Amber
    '#f43f5e', // Sector 5: Rose
    '#3b82f6', // Sector 6: Blue
    '#ec4899', // Sector 7: Pink
    '#8b5cf6', // Sector 8: Violet
    '#14b8a6', // Sector 9: Teal
  ];

  function getSectorColor(sectorId: number): string {
    const idx = (sectorId - 1) % SECTOR_PALETTE.length;
    return SECTOR_PALETTE[idx >= 0 ? idx : 0];
  }

  function getSectorForCodon(codon: number): { id: number; name: string; coherence: number } | null {
    const sectors = surveillance.epistasisGraph?.sectors;
    if (!sectors) return null;
    for (const s of sectors) {
      if (s.members.includes(codon)) {
        return { id: s.sector_id, name: s.name || `Sector #${s.sector_id}`, coherence: s.coherence };
      }
    }
    return null;
  }

  function getTopPartners(codon: number) {
    const edges = surveillance.epistasisGraph?.edges || [];
    return edges
      .filter((e) => e.source === codon || e.target === codon)
      .sort((a, b) => b.cesi - a.cesi)
      .slice(0, 3)
      .map((e) => ({
        codon: e.source === codon ? e.target : e.source,
        cesi: e.cesi,
      }));
  }

  function getFilteredNodes() {
    const epi = surveillance.epistasisGraph;
    if (!epi || !epi.nodes.length) return [];
    if (selectedSectorId === null) return epi.nodes;

    const sector = epi.sectors.find((s) => s.sector_id === selectedSectorId);
    if (!sector) return epi.nodes;
    const memberSet = new Set(sector.members);
    return epi.nodes.filter((n) => memberSet.has(n.codon || n.id));
  }

  function getFilteredEdges() {
    const epi = surveillance.epistasisGraph;
    if (!epi || !epi.edges.length) return [];
    if (selectedSectorId === null) return epi.edges;

    const sector = epi.sectors.find((s) => s.sector_id === selectedSectorId);
    if (!sector) return epi.edges;
    const memberSet = new Set(sector.members);
    return epi.edges.filter((e) => memberSet.has(e.source) && memberSet.has(e.target));
  }

  function buildGraph() {
    if (!scene) return;

    if (graphGroup) {
      scene.remove(graphGroup);
      graphGroup.clear();
    }
    graphGroup = new THREE.Group();
    nodeObjects = [];

    const nodes = getFilteredNodes();
    const edges = getFilteredEdges();
    if (!nodes.length) return;

    const nodeCount = nodes.length;
    const radius = 34;

    const nodeMap = new Map<number, THREE.Vector3>();
    const nodeGeom = new THREE.SphereGeometry(1.35, 16, 16);

    nodes.forEach((n, idx) => {
      const codon = n.codon || n.id;
      const phi = Math.acos(-1 + (2 * idx) / Math.max(1, nodeCount));
      const theta = Math.sqrt(nodeCount * Math.PI) * phi;
      const x = radius * Math.cos(theta) * Math.sin(phi);
      const y = radius * Math.sin(theta) * Math.sin(phi);
      const z = radius * Math.cos(phi);
      const pos = new THREE.Vector3(x, y, z);
      nodeMap.set(codon, pos);

      const isFocal = surveillance.focalCodon === codon;
      const sector = getSectorForCodon(codon);
      const baseColor = sector ? getSectorColor(sector.id) : '#94a3b8';

      const mat = new THREE.MeshStandardMaterial({
        color: isFocal ? 0x38bdf8 : new THREE.Color(baseColor),
        roughness: 0.35,
        metalness: 0.3,
      });

      const mesh = new THREE.Mesh(nodeGeom, mat);
      mesh.position.copy(pos);
      graphGroup!.add(mesh);
      nodeObjects.push({ id: codon, codon, mesh, pos });
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

    edges.slice(0, 200).forEach((e) => {
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

    const nodes = getFilteredNodes();
    const edges = getFilteredEdges();

    if (!nodes.length) {
      ctx.fillStyle = '#64748b';
      ctx.font = '11px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText('No Epistatic Co-selection Edges (CESI ≥ 1.5)', w / 2, h / 2);
      return;
    }

    const centerX = w / 2;
    const centerY = h / 2;
    const radius = Math.min(w, h) * 0.36;

    const posMap = new Map<number, [number, number]>();
    const nodeCount = nodes.length;

    nodes.forEach((n, idx) => {
      const codon = n.codon || n.id;
      const angle = (idx / nodeCount) * Math.PI * 2 - Math.PI / 2;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      posMap.set(codon, [x, y]);
    });

    // 1. Draw Edges
    const focal = surveillance.focalCodon;
    const hoveredCodon = hoveredNode?.codon || null;

    for (const e of edges.slice(0, 150)) {
      const p1 = posMap.get(e.source);
      const p2 = posMap.get(e.target);
      if (!p1 || !p2) continue;

      const isTouchingFocal = focal === e.source || focal === e.target;
      const isTouchingHover = hoveredCodon === e.source || hoveredCodon === e.target;

      ctx.beginPath();
      ctx.moveTo(p1[0], p1[1]);
      ctx.lineTo(p2[0], p2[1]);

      if (isTouchingFocal) {
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2.0;
      } else if (isTouchingHover) {
        ctx.strokeStyle = '#c084fc';
        ctx.lineWidth = 1.8;
      } else {
        ctx.strokeStyle = 'rgba(168, 85, 247, 0.22)';
        ctx.lineWidth = 1.0;
      }
      ctx.stroke();
    }

    // 2. Draw Nodes
    for (const n of nodes) {
      const codon = n.codon || n.id;
      const pos = posMap.get(codon);
      if (!pos) continue;

      const isFocal = focal === codon;
      const isHovered = hoveredCodon === codon;
      const r = isFocal ? 7.5 : isHovered ? 6.5 : 4.5;
      const sector = getSectorForCodon(codon);
      const color = sector ? getSectorColor(sector.id) : '#a855f7';

      // Outer glow for focal
      if (isFocal || isHovered) {
        ctx.fillStyle = isFocal ? 'rgba(56, 189, 248, 0.35)' : 'rgba(192, 132, 252, 0.3)';
        ctx.beginPath();
        ctx.arc(pos[0], pos[1], r + 4, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.fillStyle = isFocal ? '#38bdf8' : color;
      ctx.beginPath();
      ctx.arc(pos[0], pos[1], r, 0, Math.PI * 2);
      ctx.fill();

      // Label
      if (isFocal || isHovered || nodes.length <= 25) {
        ctx.fillStyle = isFocal ? '#38bdf8' : '#e2e8f0';
        ctx.font = `${isFocal ? 'bold ' : ''}9px JetBrains Mono, monospace`;
        ctx.textAlign = pos[0] >= centerX ? 'left' : 'right';
        const offset = pos[0] >= centerX ? 8 : -8;
        ctx.fillText(String(codon), pos[0] + offset, pos[1] + 3);
      }
    }
  }

  function handle2dPointerMove(e: MouseEvent) {
    if (!canvas2d || !container) return;
    const rect = canvas2d.getBoundingClientRect();
    const clientX = e.clientX - rect.left;
    const clientY = e.clientY - rect.top;

    const w = container.clientWidth;
    const h = container.clientHeight;
    const centerX = w / 2;
    const centerY = h / 2;
    const radius = Math.min(w, h) * 0.36;

    const nodes = getFilteredNodes();
    let found = false;

    for (let idx = 0; idx < nodes.length; idx++) {
      const codon = nodes[idx].codon || nodes[idx].id;
      const angle = (idx / nodes.length) * Math.PI * 2 - Math.PI / 2;
      const nx = centerX + Math.cos(angle) * radius;
      const ny = centerY + Math.sin(angle) * radius;
      const dist = Math.hypot(clientX - nx, clientY - ny);

      if (dist <= 14) {
        const sector = getSectorForCodon(codon);
        hoveredNode = {
          codon,
          name: nodes[idx].name || `Codon #${codon}`,
          domain: nodes[idx].domain || 'Core',
          degree: nodes[idx].degree || 1,
          sector,
          topPartners: getTopPartners(codon),
          screenX: clientX,
          screenY: clientY,
        };
        found = true;
        break;
      }
    }

    if (!found) {
      hoveredNode = null;
    }
    render2dNetwork();
  }

  function handle3dPointerMove(e: MouseEvent) {
    if (!renderer || !camera || !nodeObjects.length) {
      hoveredNode = null;
      return;
    }
    const rect = renderer.domElement.getBoundingClientRect();
    const clientX = e.clientX - rect.left;
    const clientY = e.clientY - rect.top;

    mouse.x = (clientX / rect.width) * 2 - 1;
    mouse.y = -(clientY / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const meshes = nodeObjects.map((no) => no.mesh);
    const intersects = raycaster.intersectObjects(meshes);

    if (intersects.length > 0) {
      const hit = nodeObjects.find((no) => no.mesh === intersects[0].object);
      if (hit) {
        const epiNodes = surveillance.epistasisGraph?.nodes || [];
        const nData = epiNodes.find((n) => (n.codon || n.id) === hit.codon);
        const sector = getSectorForCodon(hit.codon);

        hoveredNode = {
          codon: hit.codon,
          name: nData?.name || `Codon #${hit.codon}`,
          domain: nData?.domain || 'Core',
          degree: nData?.degree || 1,
          sector,
          topPartners: getTopPartners(hit.codon),
          screenX: clientX,
          screenY: clientY,
        };
        return;
      }
    }
    hoveredNode = null;
  }

  function handlePointerClick(e: MouseEvent) {
    if (viewMode === '3d') {
      if (!renderer || !camera || !nodeObjects.length) return;
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const meshes = nodeObjects.map((no) => no.mesh);
      const intersects = raycaster.intersectObjects(meshes);

      if (intersects.length > 0) {
        const hit = nodeObjects.find((no) => no.mesh === intersects[0].object);
        if (hit) {
          surveillance.setFocalCodon(hit.codon);
        }
      }
    } else {
      if (hoveredNode) {
        surveillance.setFocalCodon(hoveredNode.codon);
      }
    }
  }

  function initThree(): (() => void) | undefined {
    if (!container) return;

    try {
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

      controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.08;
      controls.rotateSpeed = 0.8;
      controls.zoomSpeed = 1.0;
      controls.panSpeed = 0.8;

      controls.addEventListener('start', () => {
        isRotating = false;
      });

      const ambientLight = new THREE.AmbientLight(0xffffff, 0.95);
      scene.add(ambientLight);

      const dirLight = new THREE.DirectionalLight(0xffffff, 1.1);
      dirLight.position.set(40, 50, 60);
      scene.add(dirLight);

      let frameId: number;
      function animate() {
        frameId = requestAnimationFrame(animate);
        if (controls) controls.update();

        if (graphGroup && isRotating) {
          graphGroup.rotation.y += 0.003;
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
      console.warn('WebGL init failed in EpistasisGraph, using 2D fallback:', e);
      hasWebGL = false;
      viewMode = '2d';
      render2dNetwork();
      return undefined;
    }
  }

  $effect(() => {
    const _e = surveillance.epistasisGraph;
    const _f = surveillance.focalCodon;
    const _s = selectedSectorId;
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

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative select-none">
  <!-- Header Bar -->
  <div class="h-10 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/70 shrink-0 z-10">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-purple-500"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT E: CESI EPISTATIC CLUSTERS</span>
      <span class="text-[10px] font-mono text-slate-500">CESI &ge; 1.5</span>
    </div>

    <!-- Controls -->
    <div class="flex items-center space-x-2 text-[10px] font-mono">
      <button
        type="button"
        onclick={() => (showRoster = !showRoster)}
        class="px-2 py-0.5 rounded transition-colors {showRoster ? 'bg-purple-950 text-purple-300 border border-purple-600/40' : 'bg-slate-800 text-slate-400'}"
        title="Toggle residue chips drawer"
      >
        Residues {showRoster ? '▾' : '▸'}
      </button>

      {#if hasWebGL}
        <button
          type="button"
          onclick={() => (viewMode = viewMode === '3d' ? '2d' : '3d')}
          class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-purple-300 transition-colors"
        >
          {viewMode === '3d' ? '2D Ring' : '3D Orbit'}
        </button>
      {/if}

      {#if viewMode === '3d'}
        <button
          type="button"
          onclick={() => (isRotating = !isRotating)}
          class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
        >
          {isRotating ? 'Pause' : 'Spin'}
        </button>
      {/if}
    </div>
  </div>

  <!-- Sector / Cluster Selector Strip -->
  {#if surveillance.epistasisGraph && surveillance.epistasisGraph.sectors?.length > 0}
    <div class="h-8 border-b border-slate-800/80 bg-dark-950/60 px-2.5 flex items-center space-x-1.5 overflow-x-auto text-[10px] font-mono shrink-0">
      <span class="text-slate-500 mr-1 shrink-0">Clusters:</span>
      <button
        type="button"
        onclick={() => (selectedSectorId = null)}
        class="px-2 py-0.5 rounded shrink-0 transition-colors {selectedSectorId === null ? 'bg-slate-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
      >
        All ({surveillance.epistasisGraph.nodes.length})
      </button>

      {#each surveillance.epistasisGraph.sectors as sector}
        {@const color = getSectorColor(sector.sector_id)}
        <button
          type="button"
          onclick={() => (selectedSectorId = selectedSectorId === sector.sector_id ? null : sector.sector_id)}
          class="px-2 py-0.5 rounded shrink-0 flex items-center space-x-1.5 border transition-all {selectedSectorId === sector.sector_id ? 'border-sky-400 bg-dark-900 font-bold text-white shadow-sm' : 'border-slate-800 text-slate-400 hover:text-slate-200'}"
        >
          <span class="w-2 h-2 rounded-full" style="background-color: {color};"></span>
          <span>Sector #{sector.sector_id}</span>
          <span class="text-[9px] opacity-60">({sector.members.length})</span>
        </button>
      {/each}
    </div>
  {/if}

  <!-- Interactive Residue Roster Grid (Shows ALL residues in the cluster) -->
  {#if showRoster && surveillance.epistasisGraph?.nodes?.length}
    {@const activeNodes = getFilteredNodes()}
    <div class="max-h-24 overflow-y-auto border-b border-slate-800/80 bg-dark-950/90 p-2 text-[10px] font-mono shrink-0">
      <div class="flex items-center justify-between mb-1.5 text-slate-400 text-[10px]">
        <span>
          Residues in {selectedSectorId ? `Sector #${selectedSectorId}` : 'Co-selection Network'} ({activeNodes.length} sites):
        </span>
        <span class="text-[9px] text-slate-500">Click any residue to focus in 3D & Waterfall</span>
      </div>

      <div class="flex flex-wrap gap-1">
        {#each activeNodes as n}
          {@const codon = n.codon || n.id}
          {@const isFocal = surveillance.focalCodon === codon}
          {@const sector = getSectorForCodon(codon)}
          {@const color = sector ? getSectorColor(sector.id) : '#94a3b8'}
          <button
            type="button"
            onclick={() => surveillance.setFocalCodon(codon)}
            onmouseenter={() => {
              hoveredNode = {
                codon,
                name: n.name || `Codon #${codon}`,
                domain: n.domain || 'Core',
                degree: n.degree || 1,
                sector,
                topPartners: getTopPartners(codon),
                screenX: 120,
                screenY: 80,
              };
            }}
            class="px-1.5 py-0.5 rounded flex items-center space-x-1 border transition-all {isFocal ? 'border-sky-400 bg-sky-950 text-sky-200 font-bold' : 'border-slate-800 bg-dark-900 text-slate-300 hover:border-slate-600'}"
            title="Focus Codon #{codon} ({n.domain || 'Core'})"
          >
            <span class="w-1.5 h-1.5 rounded-full" style="background-color: {color};"></span>
            <span>#{codon}</span>
            {#if n.domain}
              <span class="text-[8px] text-slate-500 truncate max-w-[50px]">{n.domain.split(' ')[0]}</span>
            {/if}
          </button>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Graph Canvas Container -->
  <div
    class="flex-1 w-full h-full relative overflow-hidden"
    bind:this={container}
    onmousemove={viewMode === '3d' ? handle3dPointerMove : handle2dPointerMove}
    onclick={handlePointerClick}
    role="region"
    aria-label="Epistatic co-selection network view"
  >
    <!-- 2D Network Canvas -->
    <canvas
      bind:this={canvas2d}
      class="absolute inset-0 w-full h-full block {hasWebGL && viewMode === '3d' ? 'pointer-events-none opacity-0' : 'opacity-100 cursor-pointer'}"
    ></canvas>

    <!-- Floating Interactive Tooltip -->
    {#if hoveredNode}
      {@const posX = Math.min(hoveredNode.screenX + 16, (container?.clientWidth || 500) - 260)}
      {@const posY = Math.max(12, Math.min(hoveredNode.screenY - 30, (container?.clientHeight || 400) - 170))}
      <div
        class="absolute pointer-events-none z-30 flex flex-col p-3 rounded-xl bg-dark-950/95 border border-slate-700/90 shadow-2xl backdrop-blur text-xs font-mono max-w-[250px] animate-in fade-in duration-100"
        style="left: {posX}px; top: {posY}px;"
      >
        <!-- Header -->
        <div class="flex items-center justify-between pb-1.5 border-b border-slate-800">
          <div class="flex items-center space-x-1.5 font-bold text-sky-300 text-sm">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            <span>Codon #{hoveredNode.codon}</span>
          </div>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-dark-900 border border-slate-700 text-slate-300">
            {hoveredNode.domain}
          </span>
        </div>

        <!-- Details -->
        <div class="py-2 space-y-1.5 text-[11px]">
          {#if hoveredNode.sector}
            <div class="flex items-center justify-between text-purple-400 font-semibold">
              <span>{hoveredNode.sector.name}</span>
              <span class="text-[9px] text-slate-400">Deg: {hoveredNode.degree}</span>
            </div>
          {/if}

          {#if hoveredNode.topPartners?.length}
            <div class="pt-1 text-[10px]">
              <div class="text-slate-500 mb-0.5">Top Co-selected Partners:</div>
              <div class="space-y-0.5">
                {#each hoveredNode.topPartners as p}
                  <div class="flex items-center justify-between text-slate-300">
                    <span>Codon #{p.codon}</span>
                    <span class="text-purple-400 font-bold">CESI {p.cesi.toFixed(2)}</span>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        </div>

        <div class="pt-1.5 border-t border-slate-800 text-[9px] text-sky-400/80 flex items-center justify-between">
          <span>Click to select focal codon</span>
          <span>↗</span>
        </div>
      </div>
    {/if}

    {#if !surveillance.epistasisGraph || !surveillance.epistasisGraph.nodes.length}
      <div class="absolute inset-0 flex flex-col items-center justify-center p-6 text-center pointer-events-none z-10">
        <div class="p-4 rounded-xl bg-dark-900/80 border border-slate-800 text-slate-400 max-w-xs shadow-lg backdrop-blur">
          <div class="text-xs font-semibold text-slate-300">Sparse Epistatic Network</div>
          <div class="text-[11px] font-mono text-slate-500 mt-1">
            No pairwise co-selection edges exceed threshold (CESI &ge; 1.5) across the sampled window.
          </div>
        </div>
      </div>
    {/if}

    <!-- Legend Overlay -->
    <div class="absolute bottom-2 left-3 pointer-events-none text-[10px] font-mono text-slate-400 bg-dark-950/80 px-2 py-1 rounded border border-slate-800/60 backdrop-blur z-10">
      Nodes = Codons &bull; Colors = Epistatic Clusters &bull; Edges = CESI Pairwise Strength
    </div>
  </div>
</div>
