<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { getCommunityColor } from '$lib/utils/colorScales';

  let activeTab: 'communities' | 'quarantine' = $state('communities');
</script>

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative">
  <!-- Header Bar -->
  <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/60 select-none">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">AUTOCLOCK REGIMES &amp; LOOCV TRIAGE</span>
    </div>

    <!-- Tabs -->
    <div class="flex items-center space-x-1 text-[10px] font-mono">
      <button
        onclick={() => (activeTab = 'communities')}
        class="px-2 py-0.5 rounded {activeTab === 'communities' ? 'bg-slate-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
      >
        Clock Regimes ({surveillance.autoClockTriage?.communities?.length || 0})
      </button>
      <button
        onclick={() => (activeTab = 'quarantine')}
        class="px-2 py-0.5 rounded {activeTab === 'quarantine' ? 'bg-amber-950 text-amber-300 font-bold border border-amber-600/40' : 'text-slate-400 hover:text-slate-200'}"
      >
        Quarantine Tray ({surveillance.autoClockTriage?.outliers?.length || 0})
      </button>
    </div>
  </div>

  <!-- Content Surface -->
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
                  <div class="text-[9px] text-slate-500 uppercase">Clock Linearity</div>
                  <div class="text-slate-200 font-semibold">R&sup2; = {com.r2.toFixed(3)}</div>
                </div>
                <div>
                  <div class="text-[9px] text-slate-500 uppercase">Horizon</div>
                  <div class="text-slate-200 font-semibold">t_MRCA {com.tmrca.toFixed(2)}</div>
                </div>
              </div>
            </button>
          {/each}
        {:else}
          <div class="text-center text-slate-500 py-6">Loading AutoClock Communities...</div>
        {/if}
      </div>
    {:else}
      <!-- Quarantine Outlier Table -->
      <div class="space-y-2">
        {#if surveillance.activeQuarantinedOutliers.length}
          {#each surveillance.activeQuarantinedOutliers as o}
            <div class="p-2.5 rounded-lg border border-amber-900/40 bg-amber-950/20 text-[11px]">
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center space-x-2 truncate">
                  <span class="px-1.5 py-0.2 rounded text-[9px] font-bold uppercase {o.classification === 'sequencing_artifact' ? 'bg-rose-950 text-rose-300 border border-rose-700/50' : 'bg-amber-900 text-amber-200 border border-amber-600/50'}">
                    {o.classification === 'sequencing_artifact' ? 'Artifact' : 'Saltation'}
                  </span>
                  <span class="text-slate-200 font-semibold truncate max-w-[180px]" title={o.strain}>{o.strain}</span>
                </div>
                <span class="text-amber-400 font-bold">|Z| = {Math.abs(o.studentized_residual).toFixed(2)}</span>
              </div>

              <div class="text-[10px] text-slate-400 mt-1">
                <span>Date: {o.date.toFixed(2)}</span>
                <span class="mx-1">&bull;</span>
                <span>Div: {o.divergence.toFixed(4)}</span>
                <span class="mx-1">&bull;</span>
                <span>Community: {o.community}</span>
              </div>

              {#if o.reasons?.length}
                <div class="text-[10px] text-slate-500 mt-1 italic">
                  {o.reasons[0]}
                </div>
              {/if}
            </div>
          {/each}
        {:else}
          <div class="text-center text-slate-500 py-6">No quarantined outliers in active filter.</div>
        {/if}
      </div>
    {/if}
  </div>
</div>
