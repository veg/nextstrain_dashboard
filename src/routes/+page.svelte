<script lang="ts">
  import HeaderNav from '$lib/components/HeaderNav.svelte';
  import TimeScrubber from '$lib/components/TimeScrubber.svelte';
  import AlluvialManifold from '$lib/components/AlluvialManifold.svelte';
  import SweepWaterfall from '$lib/components/SweepWaterfall.svelte';
  import StructureViewer from '$lib/components/StructureViewer.svelte';
  import EpistasisGraph from '$lib/components/EpistasisGraph.svelte';
  import ClockRadar from '$lib/components/ClockRadar.svelte';
  import DispatchReader from '$lib/components/DispatchReader.svelte';
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { onMount } from 'svelte';

  let bottomPanelTab: 'epistasis' | 'clock' = $state('epistasis');

  onMount(() => {
    surveillance.loadRegistry();
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const hash = window.location.hash.replace('#', '');
      const initial = params.get('pathogen') || hash || 'sars-cov-2';
      surveillance.loadPathogen(initial);
    } else {
      surveillance.loadPathogen('sars-cov-2');
    }
  });
</script>

<div class="h-screen w-screen flex flex-col bg-dark-950 text-slate-100 overflow-hidden select-none">
  <!-- Top Global Header -->
  <HeaderNav />

  <!-- Main Multi-Viewport Grid Cockpit -->
  <main class="flex-1 min-h-0 p-3 grid grid-cols-12 gap-3 overflow-hidden">
    <!-- Left Column (8 cols): Viewport A, Viewport B, Viewport C & E/Clock -->
    <section class="col-span-12 lg:col-span-8 flex flex-col space-y-3 min-h-0 overflow-hidden">
      <!-- Top Row: Viewport A (Alluvial Manifold Streamlines) -->
      <div class="h-52 shrink-0">
        <AlluvialManifold />
      </div>

      <!-- Middle Row: Viewport B (Sweep Velocity Waterfall) -->
      <div class="h-52 shrink-0">
        <SweepWaterfall />
      </div>

      <!-- Bottom Row: Viewport C (3D Mol* Structure) + Viewport E (3D Epistasis Network / Clock Radar) -->
      <div class="flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 gap-3">
        <!-- Viewport C: 3D Protein Structure Dynamics -->
        <div class="h-full">
          <StructureViewer />
        </div>

        <!-- Viewport E / Auxiliary: Epistasis or Clock Radar -->
        <div class="h-full flex flex-col">
          <div class="flex items-center justify-between mb-1 px-1">
            <div class="flex items-center space-x-1 text-[10px] font-mono">
              <button
                onclick={() => (bottomPanelTab = 'epistasis')}
                class="px-2 py-0.5 rounded {bottomPanelTab === 'epistasis' ? 'bg-purple-950 text-purple-300 font-bold border border-purple-600/50' : 'text-slate-500 hover:text-slate-300'}"
              >
                Epistasis 3D Graph
              </button>
              <button
                onclick={() => (bottomPanelTab = 'clock')}
                class="px-2 py-0.5 rounded {bottomPanelTab === 'clock' ? 'bg-emerald-950 text-emerald-300 font-bold border border-emerald-600/50' : 'text-slate-500 hover:text-slate-300'}"
              >
                AutoClock &amp; Triage
              </button>
            </div>
          </div>

          <div class="flex-1 min-h-0">
            {#if bottomPanelTab === 'epistasis'}
              <EpistasisGraph />
            {:else}
              <ClockRadar />
            {/if}
          </div>
        </div>
      </div>
    </section>

    <!-- Right Column (4 cols): Viewport D (Agent Intelligence Dispatch & Archive) -->
    <aside class="col-span-12 lg:col-span-4 h-full min-h-0">
      <DispatchReader />
    </aside>
  </main>

  <!-- Bottom Synchronized Scrubber Bar -->
  <TimeScrubber />
</div>
