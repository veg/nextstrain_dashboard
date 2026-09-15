<script lang="ts">
  import HeaderNav from '$lib/components/HeaderNav.svelte';
  import TimeScrubber from '$lib/components/TimeScrubber.svelte';
  import AlluvialManifold from '$lib/components/AlluvialManifold.svelte';
  import SweepWaterfall from '$lib/components/SweepWaterfall.svelte';
  import StructureViewer from '$lib/components/StructureViewer.svelte';
  import EpistasisGraph from '$lib/components/EpistasisGraph.svelte';
  import EpistasisTable from '$lib/components/EpistasisTable.svelte';
  import ClockRadar from '$lib/components/ClockRadar.svelte';
  import DispatchReader from '$lib/components/DispatchReader.svelte';
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { onMount } from 'svelte';

  onMount(() => {
    surveillance.loadRegistry();
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const hash = window.location.hash.replace('#', '');
      const initial = params.get('pathogen') || hash || 'sars-cov-2';
      const tab = params.get('tab') as 'briefing' | 'clocks' | 'selection' | 'structure';
      if (tab && ['briefing', 'clocks', 'selection', 'structure'].includes(tab)) {
        surveillance.activeTab = tab;
      }
      surveillance.loadPathogen(initial).then(() => {
        const codonParam = params.get('codon');
        if (codonParam) {
          const c = parseInt(codonParam);
          if (!isNaN(c)) surveillance.setFocalCodon(c);
        }
        const dateParam = params.get('date');
        if (dateParam) {
          const d = parseFloat(dateParam);
          if (!isNaN(d)) surveillance.setCurrentDate(d);
        }
      });
    } else {
      surveillance.loadPathogen('sars-cov-2');
    }
  });
</script>

<div class="h-screen w-screen flex flex-col bg-dark-950 text-slate-100 overflow-hidden select-none">
  <!-- Top Global Header (Pathogen Selector + Workspace Switcher) -->
  <HeaderNav />

  <!-- Dynamic Focus Workspace Area -->
  <main class="flex-1 min-h-0 p-3 overflow-hidden">
    {#if surveillance.activeTab === 'briefing'}
      <!-- Workspace 1: Briefing & Executive Summary -->
      <div class="h-full w-full flex flex-col space-y-3 min-h-0 overflow-hidden">
        <!-- Top Executive KPI Summary Row -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 shrink-0">
          <!-- Card 1: Alert & Threat Status -->
          <div class="glass-panel p-3 rounded-xl border border-slate-800/80 bg-dark-900/60 flex flex-col justify-between">
            <div class="flex items-center justify-between text-[10px] font-mono text-slate-500 uppercase tracking-wider">
              <span>Surveillance Alert</span>
              <span class="w-2 h-2 rounded-full {surveillance.deltaReport?.alert_level?.includes('Tier-1') ? 'bg-rose-500 animate-pulse' : 'bg-emerald-400'}"></span>
            </div>
            <div class="mt-1 font-semibold text-xs {surveillance.deltaReport?.alert_level?.includes('Tier-1') ? 'text-rose-300' : 'text-slate-200'} truncate">
              {surveillance.deltaReport?.alert_level || 'Tier-1 High Velocity Sweep'}
            </div>
            <div class="text-[10px] text-slate-400 mt-1 flex items-center justify-between font-mono">
              <span>{surveillance.velocityMatrix?.protein || (surveillance.currentPathogen === 'avian-flu-h5n1' ? 'HA' : 'Spike')}</span>
              <span class="text-sky-400">t={surveillance.currentDate.toFixed(2)}</span>
            </div>
          </div>

          <!-- Card 2: Confirmed Sweeps -->
          <div class="glass-panel p-3 rounded-xl border border-slate-800/80 bg-dark-900/60 flex flex-col justify-between">
            <div class="flex items-center justify-between text-[10px] font-mono text-slate-500 uppercase tracking-wider">
              <span>Emergent Sweeps</span>
              <button
                type="button"
                onclick={() => surveillance.setActiveTab('selection')}
                class="text-sky-400 hover:underline flex items-center space-x-0.5 text-[10px]"
              >
                <span>Waterfall</span>
                <span>↗</span>
              </button>
            </div>
            <div class="mt-1 flex items-center space-x-2">
              <span class="text-base font-bold text-slate-100 font-mono">
                {surveillance.velocityMatrix?.confirmed_sweeps?.length || 0}
              </span>
              <span class="text-[11px] text-slate-400">Confirmed Sweeps</span>
            </div>
            <div class="text-[10px] text-slate-400 mt-1 flex items-center space-x-1 font-mono">
              <span>Focal:</span>
              {#each (surveillance.velocityMatrix?.confirmed_sweeps?.slice(0, 3) || []) as s}
                <button
                  type="button"
                  onclick={() => surveillance.jumpToKeyframe(surveillance.currentDate, s.codon, 'selection')}
                  class="px-1.5 py-0.2 rounded bg-rose-950 text-rose-300 border border-rose-800/60 hover:bg-rose-900 transition-colors"
                  title="Inspect Codon {s.codon} in Waterfall"
                >
                  #{s.codon}
                </button>
              {/each}
            </div>
          </div>

          <!-- Card 3: AutoClock Regimes -->
          <div class="glass-panel p-3 rounded-xl border border-slate-800/80 bg-dark-900/60 flex flex-col justify-between">
            <div class="flex items-center justify-between text-[10px] font-mono text-slate-500 uppercase tracking-wider">
              <span>AutoClock Regimes</span>
              <button
                type="button"
                onclick={() => surveillance.setActiveTab('clocks')}
                class="text-emerald-400 hover:underline flex items-center space-x-0.5 text-[10px]"
              >
                <span>Phylogeny</span>
                <span>↗</span>
              </button>
            </div>
            <div class="mt-1 flex items-center space-x-2">
              <span class="text-base font-bold text-slate-100 font-mono">
                {surveillance.streamlines?.communities?.length || 2}
              </span>
              <span class="text-[11px] text-slate-400">Rate Communities</span>
            </div>
            <div class="text-[10px] text-slate-400 mt-1 font-mono truncate">
              &mu; &approx; {surveillance.autoClockTriage?.communities?.[0]?.rate?.toExponential(2) || '1.00e-3'} subs/site/yr
            </div>
          </div>

          <!-- Card 4: LOOCV Triage Outliers -->
          <div class="glass-panel p-3 rounded-xl border border-slate-800/80 bg-dark-900/60 flex flex-col justify-between">
            <div class="flex items-center justify-between text-[10px] font-mono text-slate-500 uppercase tracking-wider">
              <span>Residual Outliers</span>
              <button
                type="button"
                onclick={() => surveillance.setActiveTab('clocks')}
                class="text-amber-400 hover:underline flex items-center space-x-0.5 text-[10px]"
              >
                <span>Triage</span>
                <span>↗</span>
              </button>
            </div>
            <div class="mt-1 flex items-center space-x-2">
              <span class="text-base font-bold text-amber-400 font-mono">
                {surveillance.autoClockTriage?.outliers?.length || 0}
              </span>
              <span class="text-[11px] text-slate-400">Flagged (|Z| &ge; 3.0)</span>
            </div>
            <div class="text-[10px] text-slate-400 mt-1 font-mono">
              Closed-Form Studentized LOOCV
            </div>
          </div>
        </div>

        <!-- Centered Dispatch Document Viewport -->
        <div class="flex-1 min-h-0 max-w-4xl mx-auto w-full">
          <DispatchReader />
        </div>
      </div>

    {:else if surveillance.activeTab === 'clocks'}
      <!-- Workspace 2: Phylogeny & Molecular Clocks -->
      <div class="h-full w-full flex flex-col space-y-3 min-h-0 overflow-hidden">
        <!-- Top: Alluvial Manifold Phylogeny (56% height) -->
        <div class="h-[56%] min-h-0">
          <AlluvialManifold />
        </div>
        <!-- Bottom: AutoClock Communities & LOOCV Triage (44% height) -->
        <div class="h-[44%] min-h-0">
          <ClockRadar split={true} />
        </div>
      </div>

    {:else if surveillance.activeTab === 'selection'}
      <!-- Workspace 3: Selection Waterfall -->
      <div class="h-full w-full min-h-0 overflow-hidden">
        <SweepWaterfall />
      </div>

    {:else if surveillance.activeTab === 'structure'}
      <!-- Workspace 4: 3D Structure & Epistasis -->
      <div class="h-full w-full grid grid-cols-12 gap-3 min-h-0 overflow-hidden">
        <!-- Left: 3D Protein Structure Viewer (7 cols / 58% width) -->
        <div class="col-span-12 lg:col-span-7 h-full min-h-0">
          <StructureViewer />
        </div>
        <!-- Right: Epistasis 3D Orbit / 2D Chord Network + Co-selection Partners (5 cols / 42% width) -->
        <div class="col-span-12 lg:col-span-5 h-full min-h-0 flex flex-col space-y-3">
          <div class="h-[55%] min-h-0">
            <EpistasisGraph />
          </div>
          <div class="h-[45%] min-h-0">
            <EpistasisTable />
          </div>
        </div>
      </div>
    {/if}
  </main>

  <!-- Bottom Synchronized Scrubber Bar -->
  <TimeScrubber />
</div>
