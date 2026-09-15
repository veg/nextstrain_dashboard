<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { onMount } from 'svelte';
  import * as THREE from 'three';

  let container: HTMLDivElement;
  let renderer: THREE.WebGLRenderer | null = null;
  let scene: THREE.Scene;
  let camera: THREE.PerspectiveCamera;
  let graphGroup: THREE.Group;
  let nodeObjects: { id: number; mesh: THREE.Mesh; pos: THREE.Vector3 }[] = [];

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
      const phi = Math.acos(-1 + (2 * idx) / nodeCount);
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
      graphGroup.add(mesh);
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
      graphGroup.add(line);
    });

    scene.add(graphGroup);
  }

  function initThree() {
    if (!container) return;
    const width = container.clientWidth;
    const height = container.clientHeight;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(50, width / height, 1, 1000);
    camera.position.set(0, 0, 85);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio || 1);
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
    dirLight.position.set(30, 40, 50);
    scene.add(dirLight);

    let frameId: number;
    function animate() {
      frameId = requestAnimationFrame(animate);
      if (graphGroup) {
        graphGroup.rotation.y += 0.002;
        graphGroup.rotation.x += 0.001;
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
    const _e = surveillance.epistasisGraph;
    const _f = surveillance.focalCodon;
    buildGraph();
  });

  onMount(() => {
    const cleanup = initThree();
    buildGraph();

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
      <span class="w-2 h-2 rounded-full bg-purple-500"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT E: 3D EPISTATIC CO-SELECTION</span>
      <span class="text-[10px] font-mono text-slate-500">CESI &ge; 1.5</span>
    </div>

    <!-- Active Sector Count -->
    <div class="text-[10px] font-mono text-slate-400">
      <span>Sectors: <strong>{surveillance.epistasisGraph?.sectors?.length || 0}</strong></span>
      <span class="mx-1.5">&bull;</span>
      <span>Edges: <strong>{surveillance.epistasisGraph?.edges?.length || 0}</strong></span>
    </div>
  </div>

  <!-- 3D Canvas -->
  <div class="flex-1 w-full h-full relative" bind:this={container}>
    <!-- Overlay Badge -->
    <div class="absolute bottom-2 left-3 pointer-events-none text-[10px] font-mono text-slate-400 bg-dark-950/80 px-2 py-1 rounded border border-slate-800/60 backdrop-blur z-10">
      Nodes = Codons &bull; Edges = Composite Epistatic Selection Index &bull; Clusters = Sectors
    </div>
  </div>
</div>
