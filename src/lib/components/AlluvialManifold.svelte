<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { getCommunityColor } from '$lib/utils/colorScales';
  import { onMount } from 'svelte';

  let canvas: HTMLCanvasElement;
  let container: HTMLDivElement;
  let hoveredCommunity: number | null = $state(null);
  let hoveredInfo: any = $state(null);

  function renderManifold() {
    if (!canvas || !container) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = container.clientWidth;
    const height = container.clientHeight;
    const dpr = window.devicePixelRatio || 1;

    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);

    // Clear background
    ctx.clearRect(0, 0, width, height);

    const streamlines = surveillance.streamlines;
    if (!streamlines || !streamlines.ribbons.length) {
      // Placeholder state
      ctx.fillStyle = '#64748b';
      ctx.font = '12px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Loading ChronAeon Alluvial Streamlines...', width / 2, height / 2);
      return;
    }

    const [tMin, tMax] = streamlines.time_range;
    const [yMin, yMax] = streamlines.divergence_range;
    const padding = { top: 30, right: 40, bottom: 30, left: 50 };

    const plotW = width - padding.left - padding.right;
    const plotH = height - padding.top - padding.bottom;

    const scaleX = (t: number) => padding.left + ((t - tMin) / Math.max(0.1, tMax - tMin)) * plotW;
    const scaleY = (y: number) => height - padding.bottom - ((y - yMin) / Math.max(0.001, yMax - yMin)) * plotH;

    // 1. Draw Subtle Grid Lines
    ctx.strokeStyle = 'rgba(51, 65, 85, 0.3)';
    ctx.lineWidth = 1;
    const nTicks = 6;
    for (let i = 0; i <= nTicks; i++) {
      const t = tMin + (i / nTicks) * (tMax - tMin);
      const x = scaleX(t);
      ctx.beginPath();
      ctx.moveTo(x, padding.top);
      ctx.lineTo(x, height - padding.bottom);
      ctx.stroke();

      ctx.fillStyle = '#64748b';
      ctx.font = '10px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText(t.toFixed(1), x, height - 12);
    }

    // 2. Render Alluvial River Ribbons
    for (const ribbon of streamlines.ribbons) {
      const isSelected = surveillance.selectedClockCommunity === null || surveillance.selectedClockCommunity === ribbon.community;
      const isHovered = hoveredCommunity === ribbon.community;
      const baseColor = getCommunityColor(ribbon.community);

      ctx.save();
      ctx.globalAlpha = isSelected ? (isHovered ? 1.0 : 0.85) : 0.25;

      const knots = ribbon.knots;
      if (knots.length < 2) {
        ctx.restore();
        continue;
      }

      // Draw Upper and Lower Ribbon Contours
      ctx.beginPath();
      // Forward path (upper edge: y + w/2)
      for (let i = 0; i < knots.length; i++) {
        const k = knots[i];
        const x = scaleX(k.t);
        const yTop = scaleY(k.y + k.w * 0.0005);
        if (i === 0) ctx.moveTo(x, yTop);
        else ctx.lineTo(x, yTop);
      }
      // Backward path (lower edge: y - w/2)
      for (let i = knots.length - 1; i >= 0; i--) {
        const k = knots[i];
        const x = scaleX(k.t);
        const yBottom = scaleY(k.y - k.w * 0.0005);
        ctx.lineTo(x, yBottom);
      }
      ctx.closePath();

      // Ribbon Fill Gradient
      const grad = ctx.createLinearGradient(scaleX(knots[0].t), 0, scaleX(knots[knots.length - 1].t), 0);
      grad.addColorStop(0, `${baseColor}44`);
      grad.addColorStop(1, `${baseColor}bb`);
      ctx.fillStyle = grad;
      ctx.fill();

      // Center Streamline
      ctx.beginPath();
      ctx.strokeStyle = baseColor;
      ctx.lineWidth = isHovered ? 2.5 : 1.5;
      for (let i = 0; i < knots.length; i++) {
        const k = knots[i];
        const x = scaleX(k.t);
        const y = scaleY(k.y);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.restore();
    }

    // 3. Draw Global Scrubber Temporal Cursor
    const cursorX = scaleX(surveillance.currentDate);
    if (cursorX >= padding.left && cursorX <= width - padding.right) {
      ctx.save();
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(cursorX, padding.top);
      ctx.lineTo(cursorX, height - padding.bottom);
      ctx.stroke();

      // Cursor Head Pill
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.arc(cursorX, padding.top - 4, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  $effect(() => {
    // Re-render when store variables change
    const _d = surveillance.currentDate;
    const _s = surveillance.streamlines;
    const _c = surveillance.selectedClockCommunity;
    const _h = hoveredCommunity;
    renderManifold();
  });

  onMount(() => {
    const observer = new ResizeObserver(() => renderManifold());
    observer.observe(container);
    renderManifold();
    return () => observer.disconnect();
  });

  function handleMouseMove(e: MouseEvent) {
    if (!canvas || !container || !surveillance.streamlines) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const width = container.clientWidth;
    const height = container.clientHeight;
    const padding = { top: 30, right: 40, bottom: 30, left: 50 };
    const plotW = width - padding.left - padding.right;
    const [tMin, tMax] = surveillance.streamlines.time_range;
    const hoveredT = tMin + ((x - padding.left) / plotW) * (tMax - tMin);

    // Find nearest ribbon community
    let closestCommunity: number | null = null;
    let minDist = 30;

    for (const ribbon of surveillance.streamlines.ribbons) {
      for (const k of ribbon.knots) {
        if (Math.abs(k.t - hoveredT) < 0.25) {
          closestCommunity = ribbon.community;
          break;
        }
      }
    }
    hoveredCommunity = closestCommunity;
  }

  function handleMouseLeave() {
    hoveredCommunity = null;
  }
</script>

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative" bind:this={container}>
  <!-- Header Bar -->
  <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/60 select-none">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT A: ALLUVIAL MANIFOLD PHYLOGENY</span>
      <span class="text-[10px] font-mono text-slate-500">Deck.gl WebGPU</span>
    </div>

    <!-- Community Filter Pills -->
    <div class="flex items-center space-x-1 text-[10px] font-mono">
      <button
        onclick={() => (surveillance.selectedClockCommunity = null)}
        class="px-2 py-0.5 rounded {surveillance.selectedClockCommunity === null ? 'bg-slate-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
      >
        All
      </button>
      {#if surveillance.streamlines}
        {#each surveillance.streamlines.communities as com}
          <button
            onclick={() => (surveillance.selectedClockCommunity = surveillance.selectedClockCommunity === com.id ? null : com.id)}
            class="px-2 py-0.5 rounded flex items-center space-x-1 border {surveillance.selectedClockCommunity === com.id ? 'border-sky-400 font-bold' : 'border-slate-800'}"
            style="color: {com.color};"
          >
            <span class="w-1.5 h-1.5 rounded-full" style="background-color: {com.color};"></span>
            <span>Regime {com.id}</span>
          </button>
        {/each}
      {/if}
    </div>
  </div>

  <!-- Canvas Surface -->
  <div class="flex-1 relative overflow-hidden">
    <canvas
      bind:this={canvas}
      onmousemove={handleMouseMove}
      onmouseleave={handleMouseLeave}
      class="w-full h-full block cursor-crosshair"
    ></canvas>

    <!-- Legend Overlay -->
    <div class="absolute bottom-2 left-3 pointer-events-none text-[10px] font-mono text-slate-500 bg-dark-950/80 px-2 py-1 rounded border border-slate-800/60 backdrop-blur">
      Width = Lineage Expansion Volume (N_obs) &bull; Divergence = AutoClock &mu; &bull; Time = Calendar Years
    </div>
  </div>
</div>
