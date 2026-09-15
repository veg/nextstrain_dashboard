<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import type { EpistasisEdge } from '$lib/types/surveillance';

  function getCodonDomain(codon: number): string {
    const domains = surveillance.velocityMatrix?.domains;
    if (!domains) return 'Core';
    for (let i = domains.length - 1; i >= 0; i--) {
      if (codon >= domains[i].start && codon <= domains[i].end) {
        return domains[i].name;
      }
    }
    return 'Core';
  }

  function getPartnerEdges(): { edge: EpistasisEdge; partnerCodon: number; domain: string }[] {
    const epi = surveillance.epistasisGraph;
    if (!epi || !epi.edges?.length) return [];

    const focal = surveillance.focalCodon;
    if (focal !== null) {
      const connected = epi.edges
        .filter((e) => e.source === focal || e.target === focal)
        .sort((a, b) => b.cesi - a.cesi);

      return connected.map((e) => {
        const partnerCodon = e.source === focal ? e.target : e.source;
        return {
          edge: e,
          partnerCodon,
          domain: getCodonDomain(partnerCodon),
        };
      });
    }

    // Default: Top 20 overall edges
    return epi.edges
      .slice(0, 20)
      .sort((a, b) => b.cesi - a.cesi)
      .map((e) => ({
        edge: e,
        partnerCodon: e.target,
        domain: getCodonDomain(e.target),
      }));
  }

  let partners = $derived(getPartnerEdges());
</script>

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative">
  <!-- Header Bar -->
  <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/70 select-none shrink-0 z-10">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-purple-400"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">CO-SELECTION PARTNERS</span>
      {#if surveillance.focalCodon !== null}
        <span class="text-[10px] font-mono text-sky-400 font-bold">for Codon #{surveillance.focalCodon}</span>
      {:else}
        <span class="text-[10px] font-mono text-slate-400">Top Global Pairs</span>
      {/if}
    </div>

    <!-- Action links -->
    <div class="flex items-center space-x-2 text-[10px] font-mono">
      <button
        type="button"
        onclick={() => surveillance.setActiveTab('selection')}
        class="px-2 py-0.5 rounded bg-sky-950 hover:bg-sky-900 text-sky-300 border border-sky-700/50 transition-colors flex items-center space-x-1"
      >
        <span>View in Waterfall</span>
        <span>↗</span>
      </button>
    </div>
  </div>

  <!-- Table Body -->
  <div class="flex-1 overflow-y-auto p-2.5 text-xs font-mono min-h-0">
    {#if partners.length > 0}
      <div class="space-y-1.5">
        {#each partners as item}
          <div class="p-2 rounded-lg bg-dark-900/80 hover:bg-slate-800/70 border border-slate-800/70 flex items-center justify-between transition-colors">
            <!-- Left: Codon Pair & Domain -->
            <div class="flex items-center space-x-2.5 min-w-0">
              <button
                type="button"
                onclick={() => surveillance.setFocalCodon(item.partnerCodon)}
                class="font-bold text-sky-400 hover:underline flex items-center space-x-1"
                title="Click to focus Codon #{item.partnerCodon}"
              >
                {#if surveillance.focalCodon !== null}
                  <span>Codon #{item.partnerCodon}</span>
                {:else}
                  <span>#{item.edge.source} &harr; #{item.edge.target}</span>
                {/if}
              </button>

              <span class="text-[10px] px-1.5 py-0.2 rounded bg-dark-950 text-slate-400 border border-slate-800 truncate max-w-[140px]">
                {item.domain}
              </span>
            </div>

            <!-- Right: CESI Metric & Shared Branches -->
            <div class="flex items-center space-x-3 text-[11px] shrink-0">
              <span class="text-[10px] text-slate-500 hidden sm:inline">
                {item.edge.shared_branches} branches
              </span>

              <div class="px-2 py-0.5 rounded bg-purple-950/80 border border-purple-600/40 text-purple-300 font-bold text-[10px]">
                CESI {item.edge.cesi.toFixed(2)}
              </div>

              <button
                type="button"
                onclick={() => surveillance.setFocalCodon(item.partnerCodon)}
                class="text-[10px] text-slate-400 hover:text-sky-300 px-1 py-0.5 rounded bg-slate-800"
                title="Set as focal codon"
              >
                Focus
              </button>
            </div>
          </div>
        {/each}
      </div>
    {:else}
      <div class="h-full flex flex-col items-center justify-center p-6 text-center">
        <div class="p-4 rounded-xl bg-dark-900/80 border border-slate-800 text-slate-400 max-w-sm">
          <div class="text-xs font-semibold text-slate-200 mb-1">No Coupled Epistatic Partners</div>
          <div class="text-[11px] text-slate-500 leading-relaxed">
            {#if surveillance.focalCodon !== null}
              Codon #{surveillance.focalCodon} shows independent selective acceleration without strong pairwise epistatic coupling (CESI &ge; 1.5).
            {:else}
              Epistatic co-selection network for this pathogen is sparse or pending full-depth deconvolution.
            {/if}
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
