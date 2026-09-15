<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { getCommunityColor } from '$lib/utils/colorScales';

  let { split = true } = $props<{ split?: boolean }>();
  let activeTab: 'communities' | 'quarantine' = $state('communities');
</script>

{#if split}
  <!-- Two-Panel Split Layout for Dedicated Workspace -->
  <div class="h-full w-full grid grid-cols-1 md:grid-cols-2 gap-3 min-h-0">
    <!-- Left Panel: AutoClock Rate Communities -->
    <div class="h-full flex flex-col glass-panel rounded-xl overflow-hidden relative min-h-0">
      <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/70 select-none shrink-0">
        <div class="flex items-center space-x-2">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span class="text-xs font-semibold tracking-wide text-slate-200">AUTOCLOCK EVOLUTIONARY RATE REGIMES</span>
        </div>
        <span class="text-[10px] font-mono text-slate-400">
          {surveillance.autoClockTriage?.communities?.length || 0} Inferred Regimes
        </span>
      </div>

      <div class="flex-1 overflow-y-auto p-3 text-xs font-mono space-y-2">
        {#if surveillance.autoClockTriage?.communities?.length}
          {#each surveillance.autoClockTriage.communities as com}
            <button
              type="button"
              class="w-full text-left p-2.5 rounded-lg border bg-dark-900/80 hover:bg-dark-800/80 transition-all cursor-pointer {surveillance.selectedClockCommunity === com.id ? 'border-sky-400 bg-sky-950/30 shadow-[0_0_12px_rgba(56,189,248,0.15)]' : 'border-slate-800/80'}"
              onclick={() => (surveillance.selectedClockCommunity = surveillance.selectedClockCommunity === com.id ? null : com.id)}
            >
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center space-x-2">
                  <span class="w-2.5 h-2.5 rounded-full" style="background-color: {com.color};"></span>
                  <span class="font-bold text-slate-100">Clock Regime #{com.id}</span>
                  {#if surveillance.selectedClockCommunity === com.id}
                    <span class="text-[9px] px-1.5 py-0.2 rounded bg-sky-950 text-sky-300 border border-sky-600/40">Focal Filter</span>
                  {/if}
                </div>
                <span class="text-[10px] text-slate-400">{com.taxa_count} taxa</span>
              </div>

              <div class="grid grid-cols-3 gap-2 text-[11px] text-slate-400 mt-2 bg-dark-950/60 p-2 rounded border border-slate-800/60">
                <div>
                  <div class="text-[9px] text-slate-500 uppercase tracking-wider">Rate (&mu;)</div>
                  <div class="text-slate-100 font-semibold">{com.rate.toExponential(2)}</div>
                  <div class="text-[9px] text-slate-500">subs/site/yr</div>
                </div>
                <div>
                  <div class="text-[9px] text-slate-500 uppercase tracking-wider">Clock Fit</div>
                  <div class="text-slate-100 font-semibold">R&sup2; = {com.r2.toFixed(3)}</div>
                  <div class="text-[9px] text-slate-500">Root-to-tip</div>
                </div>
                <div>
                  <div class="text-[9px] text-slate-500 uppercase tracking-wider">Origin Horizon</div>
                  <div class="text-slate-100 font-semibold">{com.tmrca.toFixed(2)}</div>
                  <div class="text-[9px] text-slate-500">t_MRCA</div>
                </div>
              </div>
            </button>
          {/each}
        {:else}
          <div class="text-center text-slate-500 py-8">Loading AutoClock Communities...</div>
        {/if}
      </div>
    </div>

    <!-- Right Panel: Closed-Form LOOCV Studentized Residual Triage -->
    <div class="h-full flex flex-col glass-panel rounded-xl overflow-hidden relative min-h-0">
      <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/70 select-none shrink-0">
        <div class="flex items-center space-x-2">
          <span class="w-2 h-2 rounded-full bg-amber-400"></span>
          <span class="text-xs font-semibold tracking-wide text-slate-200">LOOCV STUDENTIZED RESIDUAL OUTLIER TRIAGE</span>
        </div>
        <div class="flex items-center space-x-2 text-[10px] font-mono">
          {#if surveillance.selectedClockCommunity !== null}
            <span class="text-sky-300">Regime {surveillance.selectedClockCommunity}</span>
          {/if}
          <span class="text-amber-400 font-semibold">
            {surveillance.activeQuarantinedOutliers.length} Flagged (|Z| &ge; 3.0)
          </span>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-3 text-xs font-mono space-y-2">
        {#if surveillance.activeQuarantinedOutliers.length}
          {#each surveillance.activeQuarantinedOutliers as o}
            <div class="p-2.5 rounded-lg border border-amber-900/30 bg-amber-950/15 hover:bg-amber-950/25 transition-colors text-[11px]">
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center space-x-2 truncate">
                  <span class="px-1.5 py-0.2 rounded text-[9px] font-bold uppercase {o.classification === 'sequencing_artifact' ? 'bg-rose-950 text-rose-300 border border-rose-700/50' : 'bg-amber-900 text-amber-200 border border-amber-600/50'}">
                    {o.classification === 'sequencing_artifact' ? 'Artifact' : 'Saltation'}
                  </span>
                  <span class="text-slate-200 font-semibold truncate max-w-[240px]" title={o.strain}>{o.strain}</span>
                </div>
                <span class="text-amber-400 font-bold">|Z| = {Math.abs(o.studentized_residual).toFixed(2)}</span>
              </div>

              <div class="text-[10px] text-slate-400 mt-1 flex items-center space-x-3">
                <span>Sampling: <strong>{o.date.toFixed(2)}</strong></span>
                <span>Divergence: <strong>{o.divergence.toFixed(4)}</strong></span>
                <span>Regime: <strong>#{o.community}</strong></span>
              </div>

              {#if o.reasons?.length}
                <div class="text-[10px] text-slate-400/90 mt-1.5 p-1.5 rounded bg-dark-950/50 border border-slate-800/60 italic">
                  {o.reasons[0]}
                </div>
              {/if}
            </div>
          {/each}
        {:else}
          <div class="text-center text-slate-500 py-8">
            {surveillance.selectedClockCommunity !== null
              ? `No quarantined outliers in Regime #${surveillance.selectedClockCommunity}`
              : 'No sequence outliers flagged in active surveillance.'}
          </div>
        {/if}
      </div>
    </div>
  </div>
{:else}
  <!-- Tabbed Compact Layout for Embedded Mode -->
  <div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative">
    <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/60 select-none">
      <div class="flex items-center space-x-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span class="text-xs font-semibold tracking-wide text-slate-200">AUTOCLOCK REGIMES &amp; LOOCV TRIAGE</span>
      </div>

      <div class="flex items-center space-x-1 text-[10px] font-mono">
        <button
          onclick={() => (activeTab = 'communities')}
          class="px-2 py-0.5 rounded {activeTab === 'communities' ? 'bg-slate-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
        >
          Regimes ({surveillance.autoClockTriage?.communities?.length || 0})
        </button>
        <button
          onclick={() => (activeTab = 'quarantine')}
          class="px-2 py-0.5 rounded {activeTab === 'quarantine' ? 'bg-amber-950 text-amber-300 font-bold border border-amber-600/40' : 'text-slate-400 hover:text-slate-200'}"
        >
          Quarantine ({surveillance.autoClockTriage?.outliers?.length || 0})
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto p-3 text-xs font-mono">
      {#if activeTab === 'communities'}
        <div class="space-y-2">
          {#if surveillance.autoClockTriage?.communities}
            {#each surveillance.autoClockTriage.communities as com}
              <button
                type="button"
                class="w-full text-left p-2.5 rounded-lg border bg-dark-900/80 hover:bg-dark-800/80 transition-colors cursor-pointer {surveillance.selectedClockCommunity === com.id ? 'border-sky-400 bg-sky-950/20' : 'border-slate-800'}"
                onclick={() => (surveillance.selectedClockCommunity = surveillance.selectedClockCommunity === com.id ? null : com.id)}
              >
                <div class="flex items-center justify-between mb-1">
                  <div class="flex items-center space-x-2">
                    <span class="w-2.5 h-2.5 rounded-full" style="background-color: {com.color};"></span>
                    <span class="font-bold text-slate-200">Rate Community #{com.id}</span>
                  </div>
                  <span class="text-[10px] text-slate-400">{com.taxa_count} taxa</span>
                </div>
                <div class="grid grid-cols-3 gap-2 text-[11px] text-slate-400 mt-2">
                  <div>
                    <div class="text-[9px] text-slate-500 uppercase">Rate (&mu;)</div>
                    <div class="text-slate-200 font-semibold">{com.rate.toExponential(2)}</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-slate-500 uppercase">Fit</div>
                    <div class="text-slate-200 font-semibold">R&sup2; = {com.r2.toFixed(3)}</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-slate-500 uppercase">Origin</div>
                    <div class="text-slate-200 font-semibold">{com.tmrca.toFixed(2)}</div>
                  </div>
                </div>
              </button>
            {/each}
          {/if}
        </div>
      {:else}
        <div class="space-y-2">
          {#if surveillance.activeQuarantinedOutliers.length}
            {#each surveillance.activeQuarantinedOutliers as o}
              <div class="p-2.5 rounded-lg border border-amber-900/40 bg-amber-950/20 text-[11px]">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-slate-200 font-semibold truncate max-w-[180px]">{o.strain}</span>
                  <span class="text-amber-400 font-bold">|Z| = {Math.abs(o.studentized_residual).toFixed(2)}</span>
                </div>
                <div class="text-[10px] text-slate-400">Date: {o.date.toFixed(2)} &bull; Div: {o.divergence.toFixed(4)}</div>
              </div>
            {/each}
          {/if}
        </div>
      {/if}
    </div>
  </div>
{/if}
