<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';

  const PATHOGEN_OPTIONS = [
    { id: 'sars-cov-2', name: 'SARS-CoV-2 (COVID-19)', tier: 1, gene: 'Spike', live: true },
    { id: 'avian-flu-h5n1', name: 'Avian Flu A/H5N1 (Clade 2.3.4.4b)', tier: 1, gene: 'HA', live: true },
    { id: 'influenza-h3n2', name: 'Influenza A/H3N2', tier: 1, gene: 'HA', live: false },
    { id: 'influenza-h1n1pdm', name: 'Influenza A/H1N1pdm', tier: 1, gene: 'HA', live: false },
    { id: 'mpox', name: 'Mpox Virus (Clades I & IIb)', tier: 1, gene: 'A35R', live: false },
    { id: 'dengue', name: 'Dengue Virus (DENV 1-4)', tier: 2, gene: 'Envelope', live: false },
    { id: 'ebola', name: 'Ebola Virus (Filovirus)', tier: 3, gene: 'GP', live: false },
  ];

  function onSelectPathogen(e: Event) {
    const select = e.target as HTMLSelectElement;
    surveillance.loadPathogen(select.value);
    if (typeof window !== 'undefined') {
      const url = new URL(window.location.href);
      url.searchParams.set('pathogen', select.value);
      window.history.replaceState({}, '', url.toString());
    }
  }
</script>

<header class="h-14 border-b border-slate-800 bg-dark-900/90 backdrop-blur px-4 flex items-center justify-between select-none z-30">
  <div class="flex items-center space-x-3">
    <div class="flex items-center space-x-2">
      <span class="inline-block w-3 h-3 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#38bdf8]"></span>
      <span class="font-bold text-sm tracking-wide bg-gradient-to-r from-sky-400 via-teal-300 to-indigo-400 bg-clip-text text-transparent">
        NEXTGEN SURVEILLANCE
      </span>
      <span class="text-[11px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
        v2.0 WebGPU
      </span>
    </div>

    <div class="h-4 w-px bg-slate-800 mx-2"></div>

    <!-- Pathogen Selector -->
    <div class="relative flex items-center">
      <select
        bind:value={surveillance.currentPathogen}
        onchange={onSelectPathogen}
        class="bg-dark-800 text-slate-200 text-xs font-medium pl-3 pr-8 py-1.5 rounded-lg border border-slate-700 hover:border-slate-600 focus:outline-none focus:ring-1 focus:ring-sky-500 transition-colors cursor-pointer appearance-none"
      >
        <optgroup label="Active Surveillance Targets (Live)">
          {#each PATHOGEN_OPTIONS.filter(p => p.live) as p}
            <option value={p.id}>
              {p.name} [{p.gene}] &bull; Tier {p.tier}
            </option>
          {/each}
        </optgroup>
        <optgroup label="Pipeline Ingestion Queue">
          {#each PATHOGEN_OPTIONS.filter(p => !p.live) as p}
            <option value={p.id}>
              {p.name} [{p.gene}] &bull; (Queue)
            </option>
          {/each}
        </optgroup>
      </select>
      <div class="pointer-events-none absolute right-2.5 top-2 text-slate-400 text-xs">
        ▾
      </div>
    </div>
  </div>

  <!-- Center: Alert Banner -->
  <div class="hidden md:flex items-center space-x-2">
    {#if surveillance.deltaReport?.alert_level?.includes('Tier-1')}
      <div class="flex items-center space-x-2 px-3 py-1 rounded-full bg-rose-950/80 border border-rose-500/50 text-rose-300 text-xs font-mono">
        <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
        <span class="font-semibold">ALERT:</span>
        <span class="truncate max-w-xs">{surveillance.deltaReport.alert_level} &bull; Codons {surveillance.deltaReport.newly_confirmed_sweeps.slice(0, 3).map(s => s.codon).join(', ')}</span>
      </div>
    {:else if surveillance.deltaReport?.alert_level}
      <div class="flex items-center space-x-2 px-3 py-1 rounded-full bg-amber-950/80 border border-amber-500/50 text-amber-300 text-xs font-mono">
        <span class="w-2 h-2 rounded-full bg-amber-500"></span>
        <span class="font-semibold">NOTICE:</span>
        <span class="truncate max-w-xs">{surveillance.deltaReport.alert_level}</span>
      </div>
    {:else}
      <div class="flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-slate-400 text-xs font-mono">
        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
        <span>NOMINAL DYNAMICS &bull; {surveillance.streamlines?.communities?.length || 2} AutoClock Communities</span>
      </div>
    {/if}
  </div>

  <!-- Right: Date & Status -->
  <div class="flex items-center space-x-3 text-xs">
    <div class="hidden lg:flex items-center space-x-1.5 font-mono text-slate-400">
      <span class="text-slate-500">Timespan:</span>
      <span class="text-slate-300">{surveillance.timeRange[0].toFixed(1)} - {surveillance.timeRange[1].toFixed(1)}</span>
    </div>

    <div class="h-4 w-px bg-slate-800"></div>

    <a
      href="https://github.com/veg/nextstrain_dashboard"
      target="_blank"
      rel="noreferrer"
      class="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
    >
      <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
      </svg>
      <span>GitHub</span>
    </a>
  </div>
</header>
