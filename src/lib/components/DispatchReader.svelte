<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { onMount } from 'svelte';

  let rawDispatchText: string = $state('');
  let isArchiveOpen = $state(false);

  const DISPATCH_ARCHIVE = [
    { slug: '2026-09-14-sars-cov-2', title: 'SARS-CoV-2 Spike RBM Sweep Acceleration', date: '2026-09-14', pathogen: 'sars-cov-2', tier: 1 },
    { slug: '2026-09-13-avian-flu-h5n1', title: 'Avian Flu H5N1 Clade 2.3.4.4b Spillover', date: '2026-09-13', pathogen: 'avian-flu-h5n1', tier: 1 },
  ];

  async function loadDispatch(slug: string) {
    try {
      // Fetch markdown from dispatches or mock fallback
      const res = await fetch(`/dispatches/${slug}.md`);
      if (res.ok) {
        rawDispatchText = await res.text();
      } else {
        // Fallback default dispatch content
        rawDispatchText = `# Pathogen Intelligence Briefing: SARS-CoV-2 Spike Glycoprotein
**Date:** 2026-09-14 | **Surveillance Target:** SARS-CoV-2 | **Alert Level:** Tier-1 High Velocity Sweep

### 1. Executive Alert
A concentrated burst of instantaneous selection velocity v_s(t) has been detected across receptor-binding domain (RBD) codons, led by [t=2024.8, codon=456] and [t=2024.8, codon=455] within sublineages KP.3 and JN.1 radiations. Positive sweep velocity reached 0.0374 subs/site/year, displaying a 3.2-month lead time over empirical population prevalence curves.

### 2. Molecular Acceleration Analysis
While classical dN/dS estimators yield static, diluted values (0.85) due to post-fixation dilution across the 6.5-year phylogeny, continuous Nadaraya-Watson kernel attribution regression resolves acute episodic selection bursts.
- Codon 456 (F456L): Shows an acute sweep velocity peak at [t=2024.8, codon=456], confirmed by Stage-2 date-shuffling permutation tests (B=1,000, p = 0.002).
- Codon 455 (L455S): Exhibited synchronized selective acceleration in late 2023 [t=2023.9, codon=455].
- Codon 486 (F486P): Anchors the canonical "FLip" motif (L455S + F456L) against high population humoral immunity.

### 3. Structural & Epistatic Synthesis
Mapping inferred positive velocity onto the live 3D Spike trimer (7KRR.pdb) demonstrates that the selective epicenter is strictly localized to the Receptor-Binding Motif (RBM, residues 437–508). Co-selection analysis via the Composite Epistatic Selection Index (CESI) reveals that RBM mutations couple with upstream scaffold sites A264 and N450 (CESI = 17.41) to restore ACE2 binding affinity.

### 4. Molecular Clock & Triage Audit
ChronAeon AutoClock deconvolution identified 3 independent evolutionary rate communities. The focal lineage exhibits a calibrated evolutionary rate of 1.00e-3 subs/site/year. Closed-form LOOCV studentized residual triage flagged 4 extreme outliers (|Z| >= 3.0).

### 5. Forward Surveillance Recommendations
1. Targeted wastewater monitoring for 455S + 456L double mutants.
2. Neutralization titer assays against emerging KP.3 variants.
3. Continued monitoring of compensatory mutations across Epistatic Sector #1.`;
      }
    } catch (e) {
      console.warn('Could not fetch dispatch:', e);
    }
  }

  // Parses interactive tokens like [t=2024.8, codon=456] into clickable buttons
  function parseContentWithTokens(text: string) {
    const tokenRegex = /\[t=([\d\.]+)(?:,\s*codon=(\d+))?\]/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = tokenRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push({ type: 'text', content: text.substring(lastIndex, match.index) });
      }
      parts.push({
        type: 'token',
        full: match[0],
        date: parseFloat(match[1]),
        codon: match[2] ? parseInt(match[2]) : undefined,
      });
      lastIndex = tokenRegex.lastIndex;
    }

    if (lastIndex < text.length) {
      parts.push({ type: 'text', content: text.substring(lastIndex) });
    }

    return parts;
  }

  onMount(() => {
    loadDispatch('2026-09-14-sars-cov-2');
  });
</script>

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative">
  <!-- Header Bar -->
  <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/60 select-none">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-amber-400"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT D: AGENT INTELLIGENCE DISPATCH</span>
      <span class="text-[10px] font-mono text-slate-500">Antigravity AI</span>
    </div>

    <!-- Archive & PR Links -->
    <div class="flex items-center space-x-2 text-[10px] font-mono">
      <button
        onclick={() => (isArchiveOpen = !isArchiveOpen)}
        class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
      >
        {isArchiveOpen ? 'Close Archive' : 'Archive (2)'}
      </button>
      <a
        href="https://github.com/veg/pathogen-intelligence/pulls"
        target="_blank"
        rel="noreferrer"
        class="text-sky-400 hover:underline"
      >
        PR #42
      </a>
    </div>
  </div>

  <!-- Content Surface -->
  <div class="flex-1 overflow-y-auto p-4 text-xs font-sans leading-relaxed text-slate-300">
    {#if isArchiveOpen}
      <!-- Archive Drawer -->
      <div class="space-y-2 mb-4 pb-4 border-b border-slate-800 font-mono text-[11px]">
        <div class="text-[10px] uppercase text-slate-500 font-bold mb-2">Historical Dispatches</div>
        {#each DISPATCH_ARCHIVE as item}
          <button
            onclick={() => { loadDispatch(item.slug); isArchiveOpen = false; }}
            class="w-full text-left p-2 rounded bg-dark-900/80 hover:bg-slate-800 border border-slate-800 block transition-colors"
          >
            <div class="flex items-center justify-between">
              <span class="font-semibold text-slate-200">{item.title}</span>
              <span class="text-[9px] px-1.5 py-0.2 rounded bg-rose-950 text-rose-300 border border-rose-800">Tier {item.tier}</span>
            </div>
            <div class="text-[10px] text-slate-400 mt-1">{item.date} &bull; {item.pathogen}</div>
          </button>
        {/each}
      </div>
    {/if}

    <!-- Rendered Markdown with Clickable Tokens -->
    {#each rawDispatchText.split('\n\n') as paragraph}
      {#if paragraph.startsWith('# ')}
        <h1 class="text-base font-bold text-white mb-2 tracking-tight">{paragraph.substring(2)}</h1>
      {:else if paragraph.startsWith('## ') || paragraph.startsWith('### ')}
        <h2 class="text-xs font-bold uppercase tracking-wider text-sky-400 mt-4 mb-1 border-b border-slate-800 pb-1">
          {paragraph.replace(/^#+\s*/, '')}
        </h2>
      {:else if paragraph.startsWith('- ')}
        <ul class="list-disc list-inside space-y-1 my-2">
          {#each paragraph.split('\n') as li}
            <li class="text-slate-300">
              {#each parseContentWithTokens(li.replace(/^[-\*]\s*/, '')) as segment}
                {#if segment.type === 'token'}
                  <button
                    onclick={() => surveillance.jumpToKeyframe(segment.date, segment.codon)}
                    class="inline-flex items-center space-x-1 px-1.5 py-0.5 rounded bg-sky-950/80 border border-sky-600/60 text-sky-300 font-mono text-[10px] hover:bg-sky-900 transition-colors mx-0.5 cursor-pointer"
                    title="Jump scrubber to date {segment.date} and focus codon {segment.codon || ''}"
                  >
                    <span>&#x25B6;</span>
                    <span>{segment.full.replace(/[\[\]]/g, '')}</span>
                  </button>
                {:else}
                  {segment.content}
                {/if}
              {/each}
            </li>
          {/each}
        </ul>
      {:else}
        <p class="mb-2 text-slate-300">
          {#each parseContentWithTokens(paragraph) as segment}
            {#if segment.type === 'token'}
              <button
                onclick={() => surveillance.jumpToKeyframe(segment.date, segment.codon)}
                class="inline-flex items-center space-x-1 px-1.5 py-0.5 rounded bg-sky-950/80 border border-sky-600/60 text-sky-300 font-mono text-[10px] hover:bg-sky-900 transition-colors mx-0.5 cursor-pointer"
                title="Jump scrubber to date {segment.date} and focus codon {segment.codon || ''}"
              >
                <span>&#x25B6;</span>
                <span>{segment.full.replace(/[\[\]]/g, '')}</span>
              </button>
            {:else}
              {segment.content}
            {/if}
          {/each}
        </p>
      {/if}
    {/each}
  </div>
</div>
