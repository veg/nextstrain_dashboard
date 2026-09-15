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

  const WORKSPACES = [
    {
      id: 'briefing' as const,
      label: 'Briefing & Summary',
      shortLabel: 'Briefing',
      icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z'
    },
    {
      id: 'clocks' as const,
      label: 'Phylogeny & Clocks',
      shortLabel: 'Clocks',
      icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    {
      id: 'selection' as const,
      label: 'Selection Waterfall',
      shortLabel: 'Selection',
      icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
    },
    {
      id: 'structure' as const,
      label: '3D Structure & Epistasis',
      shortLabel: 'Structure',
      icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4'
    }
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

<header class="h-14 border-b border-slate-800 bg-dark-900/95 backdrop-blur px-4 flex items-center justify-between select-none z-30 shrink-0">
  <!-- Left: Brand & Pathogen Selector -->
  <div class="flex items-center space-x-3">
    <div class="flex items-center space-x-2">
      <span class="inline-block w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#38bdf8]"></span>
      <span class="font-bold text-xs tracking-wider bg-gradient-to-r from-sky-400 via-teal-300 to-indigo-400 bg-clip-text text-transparent uppercase">
        NextGen Surveillance
      </span>
      <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-400 border border-slate-700/60 hidden sm:inline">
        v2.0
      </span>
    </div>

    <div class="h-4 w-px bg-slate-800 mx-1"></div>

    <!-- Pathogen Selector -->
    <div class="relative flex items-center">
      <select
        bind:value={surveillance.currentPathogen}
        onchange={onSelectPathogen}
        class="bg-dark-800 text-slate-200 text-xs font-medium pl-2.5 pr-7 py-1.5 rounded-lg border border-slate-700 hover:border-slate-600 focus:outline-none focus:ring-1 focus:ring-sky-500 transition-colors cursor-pointer appearance-none"
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
      <div class="pointer-events-none absolute right-2 top-2 text-slate-400 text-xs">
        ▾
      </div>
    </div>
  </div>

  <!-- Center: Workspace Switcher Tabs -->
  <nav class="flex items-center bg-dark-950/90 p-1 rounded-xl border border-slate-800 shadow-inner">
    {#each WORKSPACES as ws}
      <button
        type="button"
        onclick={() => surveillance.setActiveTab(ws.id)}
        class="flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 {surveillance.activeTab === ws.id ? 'bg-sky-500/15 text-sky-300 border border-sky-500/40 shadow-sm font-semibold' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 border border-transparent'}"
      >
        <svg class="w-3.5 h-3.5 shrink-0 stroke-current fill-none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={ws.icon} />
        </svg>
        <span class="hidden md:inline">{ws.label}</span>
        <span class="md:hidden">{ws.shortLabel}</span>

        {#if ws.id === 'briefing' && surveillance.deltaReport?.alert_level?.includes('Tier-1')}
          <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
        {/if}
      </button>
    {/each}
  </nav>

  <!-- Right: Status / GitHub Link -->
  <div class="flex items-center space-x-3 text-xs">
    {#if surveillance.deltaReport?.alert_level?.includes('Tier-1')}
      <div class="hidden xl:flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-rose-950/80 border border-rose-600/40 text-rose-300 text-[11px] font-mono">
        <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
        <span>ALERT: Tier-1 Surge</span>
      </div>
    {:else}
      <div class="hidden xl:flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-slate-400 text-[11px] font-mono">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span>Nominal Dynamics</span>
      </div>
    {/if}

    <a
      href="https://github.com/veg/nextstrain_dashboard"
      target="_blank"
      rel="noreferrer"
      class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
      title="View Source Repository on GitHub"
    >
      <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
      </svg>
      <span class="font-mono text-xs">Repo</span>
    </a>
  </div>
</header>
