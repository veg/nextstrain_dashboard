<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { getVelocityColor } from '$lib/utils/colorScales';
  import { onMount } from 'svelte';

  let canvas: HTMLCanvasElement;
  let container: HTMLDivElement;
  let hoveredCodonInfo: any = $state(null);

  function renderWaterfall() {
    if (!canvas || !container) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = container.clientWidth;
    const height = container.clientHeight;
    const dpr = window.devicePixelRatio || 1;

    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    const vData = surveillance.velocityMatrix;
    if (!vData || !vData.codons.length || !vData.time_points.length) {
      ctx.fillStyle = '#64748b';
      ctx.font = '12px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Loading HyphAeon Selection Velocity Matrix...', width / 2, height / 2);
      return;
    }

    const { codons, time_points, matrix, domains, confirmed_sweeps, rescued_sweeps } = vData;
    const padding = { top: 25, right: 30, bottom: 25, left: 60 };
    const domainWidth = 12;

    const plotX = padding.left + domainWidth + 6;
    const plotW = width - plotX - padding.right;
    const plotH = height - padding.top - padding.bottom;

    const tMin = time_points[0];
    const tMax = time_points[time_points.length - 1];

    // Filter codons based on sweepFilterMode
    let displayCodons: number[] = [];
    if (surveillance.sweepFilterMode === 'confirmed') {
      const confSet = new Set(confirmed_sweeps.map(s => s.codon));
      displayCodons = codons.filter(c => confSet.has(c));
    } else if (surveillance.sweepFilterMode === 'rescued') {
      const rescSet = new Set(rescued_sweeps.map(s => s.codon));
      displayCodons = codons.filter(c => rescSet.has(c));
    } else {
      displayCodons = codons;
    }

    if (!displayCodons.length) {
      displayCodons = codons.slice(0, 60); // fallback
    }

    const nCodons = displayCodons.length;
    const cellH = Math.max(2, plotH / nCodons);
    const cellW = plotW / time_points.length;

    // 1. Draw Domain Band on the Left
    const minCodon = Math.min(...displayCodons);
    const maxCodon = Math.max(...displayCodons);
    for (const domain of domains) {
      const dStart = Math.max(minCodon, domain.start);
      const dEnd = Math.min(maxCodon, domain.end);
      if (dStart > maxCodon || dEnd < minCodon) continue;

      const yStart = padding.top + ((dStart - minCodon) / Math.max(1, maxCodon - minCodon)) * plotH;
      const yEnd = padding.top + ((dEnd - minCodon) / Math.max(1, maxCodon - minCodon)) * plotH;
      const h = Math.max(3, yEnd - yStart);

      ctx.fillStyle = domain.color || '#3b82f6';
      ctx.fillRect(padding.left, yStart, domainWidth, h);
    }

    // 2. Draw Velocity Heatmap Cells
    for (let cIdx = 0; cIdx < nCodons; cIdx++) {
      const codon = displayCodons[cIdx];
      const origIdx = codons.indexOf(codon);
      if (origIdx === -1) continue;

      const y = padding.top + cIdx * cellH;
      const row = matrix[origIdx];
      const isFocal = surveillance.focalCodon === codon;

      // Focal Codon Background Highlight
      if (isFocal) {
        ctx.fillStyle = 'rgba(56, 189, 248, 0.18)';
        ctx.fillRect(plotX, y - 1, plotW, cellH + 2);
      }

      for (let tIdx = 0; tIdx < time_points.length; tIdx++) {
        const x = plotX + tIdx * cellW;
        const vel = row[tIdx] || 0;
        if (vel > 0.0005) {
          ctx.fillStyle = getVelocityColor(vel, 0.035);
          ctx.fillRect(x, y, Math.ceil(cellW), Math.ceil(cellH));
        }
      }

      // Draw Codon Label on Left
      if (cellH >= 10 || isFocal || cIdx % 5 === 0) {
        ctx.fillStyle = isFocal ? '#38bdf8' : '#94a3b8';
        ctx.font = `${isFocal ? 'bold ' : ''}9px JetBrains Mono, monospace`;
        ctx.textAlign = 'right';
        ctx.fillText(String(codon), padding.left - 4, y + cellH * 0.8);
      }
    }

    // 3. Time Grid Line & Labels
    ctx.fillStyle = '#64748b';
    ctx.font = '10px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    const nTicks = 5;
    for (let i = 0; i <= nTicks; i++) {
      const t = tMin + (i / nTicks) * (tMax - tMin);
      const x = plotX + (i / nTicks) * plotW;
      ctx.fillText(t.toFixed(1), x, height - 8);
    }

    // 4. Synchronized Global Scrubber Cursor
    const cursorX = plotX + ((surveillance.currentDate - tMin) / Math.max(0.1, tMax - tMin)) * plotW;
    if (cursorX >= plotX && cursorX <= plotX + plotW) {
      ctx.save();
      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(cursorX, padding.top);
      ctx.lineTo(cursorX, height - padding.bottom);
      ctx.stroke();

      ctx.fillStyle = '#f43f5e';
      ctx.beginPath();
      ctx.arc(cursorX, padding.top - 3, 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  $effect(() => {
    const _d = surveillance.currentDate;
    const _v = surveillance.velocityMatrix;
    const _f = surveillance.focalCodon;
    const _m = surveillance.sweepFilterMode;
    renderWaterfall();
  });

  onMount(() => {
    const observer = new ResizeObserver(() => renderWaterfall());
    observer.observe(container);
    renderWaterfall();
    return () => observer.disconnect();
  });

  function handleCanvasClick(e: MouseEvent) {
    if (!canvas || !container || !surveillance.velocityMatrix) return;
    const rect = canvas.getBoundingClientRect();
    const y = e.clientY - rect.top;
    const padding = { top: 25, bottom: 25 };
    const plotH = container.clientHeight - padding.top - padding.bottom;

    const vData = surveillance.velocityMatrix;
    let displayCodons = vData.codons;
    if (surveillance.sweepFilterMode === 'confirmed') {
      const confSet = new Set(vData.confirmed_sweeps.map(s => s.codon));
      displayCodons = displayCodons.filter(c => confSet.has(c));
    }

    const codonIdx = Math.floor(((y - padding.top) / plotH) * displayCodons.length);
    if (codonIdx >= 0 && codonIdx < displayCodons.length) {
      surveillance.setFocalCodon(displayCodons[codonIdx]);
    }
  }
</script>

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative" bind:this={container}>
  <!-- Header Bar -->
  <div class="h-9 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/60 select-none">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-rose-500"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">VIEWPORT B: SWEEP VELOCITY WATERFALL</span>
      <span class="text-[10px] font-mono text-slate-500">v_s(t) = max(0, da/dt)</span>
    </div>

    <!-- Filter Toggles -->
    <div class="flex items-center space-x-1 text-[10px] font-mono">
      <button
        onclick={() => (surveillance.sweepFilterMode = 'confirmed')}
        class="px-2 py-0.5 rounded {surveillance.sweepFilterMode === 'confirmed' ? 'bg-rose-950 text-rose-300 font-bold border border-rose-600/50' : 'text-slate-400 hover:text-slate-200'}"
      >
        Confirmed Sweeps ({surveillance.velocityMatrix?.confirmed_sweeps?.length || 0})
      </button>
      <button
        onclick={() => (surveillance.sweepFilterMode = 'rescued')}
        class="px-2 py-0.5 rounded {surveillance.sweepFilterMode === 'rescued' ? 'bg-amber-950 text-amber-300 font-bold border border-amber-600/50' : 'text-slate-400 hover:text-slate-200'}"
      >
        Rescued Sweeps ({surveillance.velocityMatrix?.rescued_sweeps?.length || 0})
      </button>
      <button
        onclick={() => (surveillance.sweepFilterMode = 'all')}
        class="px-2 py-0.5 rounded {surveillance.sweepFilterMode === 'all' ? 'bg-slate-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
      >
        All Sites ({surveillance.velocityMatrix?.codons?.length || 0})
      </button>
    </div>
  </div>

  <!-- Canvas Surface -->
  <div class="flex-1 relative overflow-hidden">
    <canvas
      bind:this={canvas}
      onclick={handleCanvasClick}
      class="w-full h-full block cursor-pointer"
    ></canvas>

    <!-- Legend Overlay -->
    <div class="absolute top-2 right-3 pointer-events-none flex items-center space-x-2 text-[10px] font-mono bg-dark-950/80 px-2.5 py-1 rounded border border-slate-800/60 backdrop-blur">
      <span class="text-slate-400">Velocity:</span>
      <span class="w-2.5 h-2 rounded bg-sky-400"></span>
      <span class="text-slate-400">Low</span>
      <span class="w-2.5 h-2 rounded bg-amber-400"></span>
      <span class="text-slate-400">Med</span>
      <span class="w-2.5 h-2 rounded bg-rose-500"></span>
      <span class="text-slate-400">High (&gt;0.035)</span>
    </div>
  </div>
</div>
