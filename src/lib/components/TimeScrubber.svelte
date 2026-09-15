<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { onMount } from 'svelte';

  let animationFrameId: number;
  let lastTimestamp: number = 0;

  function loop(timestamp: number) {
    if (lastTimestamp && surveillance.isPlaying) {
      const dt = timestamp - lastTimestamp;
      surveillance.tick(dt);
    }
    lastTimestamp = timestamp;
    animationFrameId = requestAnimationFrame(loop);
  }

  onMount(() => {
    animationFrameId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animationFrameId);
  });

  function formatDateDisplay(decimalYear: number): string {
    const year = Math.floor(decimalYear);
    const dayFraction = decimalYear - year;
    const monthIdx = Math.min(11, Math.floor(dayFraction * 12));
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${months[monthIdx]} ${year}`;
  }

  function handleSlider(e: Event) {
    const val = parseFloat((e.target as HTMLInputElement).value);
    surveillance.setCurrentDate(val);
  }

  const SARS_KEYFRAMES = [
    { label: 'Alpha', date: 2020.95, codon: 501 },
    { label: 'Delta', date: 2021.45, codon: 452 },
    { label: 'BA.1', date: 2021.90, codon: 484 },
    { label: 'BA.5', date: 2022.45, codon: 486 },
    { label: 'JN.1', date: 2023.85, codon: 455 },
    { label: 'KP.3', date: 2024.35, codon: 456 },
  ];

  const H5N1_KEYFRAMES = [
    { label: 'Caprine Spillover', date: 2024.15, codon: 143 },
    { label: 'Texas Dairy Index', date: 2024.19, codon: 143 },
    { label: 'Bovine Expansion', date: 2024.22, codon: 143 },
    { label: 'Active Surveillance', date: 2024.26, codon: 143 },
  ];

  let currentKeyframes = $derived(
    surveillance.currentPathogen === 'avian-flu-h5n1' ? H5N1_KEYFRAMES : SARS_KEYFRAMES
  );
</script>

<div class="h-16 border-t border-slate-800 bg-dark-900/95 backdrop-blur px-6 flex items-center justify-between select-none z-30">
  <!-- Left: Playback Controls -->
  <div class="flex items-center space-x-3">
    <!-- Play/Pause -->
    <button
      onclick={() => surveillance.togglePlay()}
      class="w-9 h-9 rounded-full bg-sky-500 hover:bg-sky-400 text-dark-950 flex items-center justify-center font-bold transition-transform active:scale-95 shadow-md shadow-sky-500/20"
      title={surveillance.isPlaying ? 'Pause' : 'Play'}
    >
      {#if surveillance.isPlaying}
        <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg>
      {:else}
        <svg class="w-4 h-4 fill-current ml-0.5" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
      {/if}
    </button>

    <!-- Step Buttons -->
    <button
      onclick={() => surveillance.setCurrentDate(surveillance.currentDate - 0.1)}
      class="w-7 h-7 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center text-xs"
      title="Step Back 1 Month"
    >
      &lsaquo;
    </button>
    <button
      onclick={() => surveillance.setCurrentDate(surveillance.currentDate + 0.1)}
      class="w-7 h-7 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center text-xs"
      title="Step Forward 1 Month"
    >
      &rsaquo;
    </button>

    <!-- Speed Toggles -->
    <div class="flex items-center space-x-1 bg-dark-950 rounded-lg p-0.5 border border-slate-800 text-[11px] font-mono">
      {#each [0.5, 1.0, 2.0, 4.0] as sp}
        <button
          onclick={() => surveillance.setPlaybackSpeed(sp)}
          class="px-1.5 py-0.5 rounded {surveillance.playbackSpeed === sp ? 'bg-sky-500 text-dark-950 font-bold' : 'text-slate-400 hover:text-slate-200'}"
        >
          {sp}x
        </button>
      {/each}
    </div>
  </div>

  <!-- Center: Scrub Slider & Keyframes -->
  <div class="flex-1 max-w-2xl mx-6 flex flex-col justify-center space-y-1">
    <div class="flex items-center justify-between text-[11px] font-mono text-slate-400">
      <span>{surveillance.timeRange[0].toFixed(1)}</span>
      <div class="flex items-center space-x-2">
        <span class="text-sky-400 font-semibold text-xs">{formatDateDisplay(surveillance.currentDate)}</span>
        <span class="text-slate-500">({surveillance.currentDate.toFixed(2)})</span>
      </div>
      <span>{surveillance.timeRange[1].toFixed(1)}</span>
    </div>

    <!-- Range Input -->
    <div class="relative flex items-center">
      <input
        type="range"
        min={surveillance.timeRange[0]}
        max={surveillance.timeRange[1]}
        step="0.01"
        value={surveillance.currentDate}
        oninput={handleSlider}
        class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-sky-400 hover:accent-sky-300"
      />
    </div>

    <!-- Keyframe Markers -->
    <div class="flex items-center justify-between px-1">
      {#each currentKeyframes as kf}
        {#if kf.date >= surveillance.timeRange[0] && kf.date <= surveillance.timeRange[1]}
          <button
            onclick={() => surveillance.jumpToKeyframe(kf.date, kf.codon)}
            class="text-[10px] font-mono px-1.5 py-0.2 rounded hover:bg-slate-800 transition-colors {Math.abs(surveillance.currentDate - kf.date) < 0.2 ? 'text-sky-400 font-bold' : 'text-slate-500'}"
            title="Jump to {kf.label} ({kf.date})"
          >
            {kf.label}
          </button>
        {/if}
      {/each}
    </div>
  </div>

  <!-- Right: Active Selection Pill -->
  <div class="hidden sm:flex items-center space-x-3 text-xs font-mono">
    {#if surveillance.focalCodon !== null}
      <div class="px-2.5 py-1 rounded bg-sky-950/80 border border-sky-600/40 text-sky-300 flex items-center space-x-1.5">
        <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
        <span>Focal Codon: <strong>{surveillance.focalCodon}</strong></span>
        <button
          onclick={() => surveillance.setFocalCodon(null)}
          class="ml-1 text-slate-400 hover:text-slate-200"
          title="Clear Focal Codon"
        >
          &times;
        </button>
      </div>
    {:else}
      <div class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-500">
        Click any codon to focus
      </div>
    {/if}
  </div>
</div>
