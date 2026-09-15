<script lang="ts">
  import { surveillance } from '$lib/stores/surveillanceStore.svelte';
  import { getVelocityColor } from '$lib/utils/colorScales';
  import { onMount } from 'svelte';

  let canvas: HTMLCanvasElement;
  let container: HTMLDivElement;
  let searchQuery: string = $state('');
  let searchError: string = $state('');
  let hoveredCell = $state<{
    codon: number;
    t: number;
    dateStr: string;
    vel: number;
    x: number;
    y: number;
    domain: { name: string; color: string; start: number; end: number } | null;
    confirmed: any | null;
    rescued: any | null;
  } | null>(null);

  function formatDateDisplay(decimalYear: number): string {
    const year = Math.floor(decimalYear);
    const dayFraction = decimalYear - year;
    const monthIdx = Math.min(11, Math.floor(dayFraction * 12));
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${months[monthIdx]} ${year}`;
  }

  function getDisplayCodons(vData: any, mode: string): number[] {
    if (!vData || !vData.codons) return [];
    const { codons, confirmed_sweeps = [], rescued_sweeps = [], surveillance_codons = [] } = vData;
    let list: number[] = [];

    if (mode === 'confirmed') {
      const confSet = new Set(confirmed_sweeps.map((s: any) => s.codon));
      list = codons.filter((c: number) => confSet.has(c));
    } else if (mode === 'rescued') {
      const rescSet = new Set(rescued_sweeps.map((s: any) => s.codon));
      list = codons.filter((c: number) => rescSet.has(c));
    } else {
      list = codons;
    }

    // If filter mode returns very few codons (< 3), supplement with surveillance codons or variable codons
    if (list.length < 3) {
      if (mode === 'confirmed' && surveillance_codons.length) {
        const fullSet = new Set([...list, ...surveillance_codons]);
        list = codons.filter((c: number) => fullSet.has(c));
      }
      if (list.length < 3) {
        list = codons;
      }
    }
    return list;
  }

  function getCodonDomain(codon: number): { name: string; color: string; start: number; end: number } | null {
    const domains = surveillance.velocityMatrix?.domains;
    if (!domains) return null;
    // Search in reverse so nested specific domains (e.g. RBM within RBD) take precedence
    for (let i = domains.length - 1; i >= 0; i--) {
      if (codon >= domains[i].start && codon <= domains[i].end) {
        return domains[i];
      }
    }
    return null;
  }

  function getFocalSweepInfo() {
    const codon = surveillance.focalCodon;
    if (codon === null || !surveillance.velocityMatrix) return null;
    const { confirmed_sweeps = [], rescued_sweeps = [] } = surveillance.velocityMatrix;
    const conf = confirmed_sweeps.find((s: any) => s.codon === codon);
    const resc = rescued_sweeps.find((s: any) => s.codon === codon);
    const domain = getCodonDomain(codon);
    const currentVel = surveillance.activeResidueVelocities.get(codon) || 0;

    return {
      codon,
      domain,
      currentVel,
      confirmed: conf,
      rescued: resc,
    };
  }

  let focalInfo = $derived(getFocalSweepInfo());

  function handleSearchKey(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      const num = parseInt(searchQuery.trim());
      if (isNaN(num)) {
        searchError = 'Enter a valid codon number';
        return;
      }
      const vData = surveillance.velocityMatrix;
      if (!vData || !vData.codons) return;

      if (vData.codons.includes(num)) {
        searchError = '';
        surveillance.setFocalCodon(num);
        // If not in current filter list, switch to all sites so it's visible
        const currentList = getDisplayCodons(vData, surveillance.sweepFilterMode);
        if (!currentList.includes(num)) {
          surveillance.sweepFilterMode = 'all';
        }
      } else {
        searchError = `Codon ${num} has no variable sweep trajectory`;
        setTimeout(() => (searchError = ''), 3000);
      }
    }
  }

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
    if (!vData || !vData.codons?.length || !vData.time_points?.length) {
      ctx.fillStyle = '#64748b';
      ctx.font = '12px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(
        surveillance.isLoading
          ? `Loading HyphAeon Selection Velocity for ${surveillance.currentPathogen}...`
          : `No Velocity Matrix available for ${surveillance.currentPathogen}`,
        width / 2,
        height / 2
      );
      return;
    }

    const { codons, time_points, matrix, domains } = vData;
    const padding = { top: 25, right: 35, bottom: 38, left: 65 };
    const domainWidth = 14;

    const plotX = padding.left + domainWidth + 8;
    const plotW = width - plotX - padding.right;
    const plotH = height - padding.top - padding.bottom;

    const tMin = time_points[0];
    const tMax = time_points[time_points.length - 1];

    const displayCodons = getDisplayCodons(vData, surveillance.sweepFilterMode);
    const nCodons = displayCodons.length;
    const cellH = Math.max(3, plotH / Math.max(1, nCodons));
    const cellW = plotW / Math.max(1, time_points.length);

    // 1. Draw Domain Band on the Left (aligned to displayed codon rows)
    if (domains && domains.length) {
      for (const domain of domains) {
        const matchingIndices: number[] = [];
        for (let i = 0; i < nCodons; i++) {
          if (displayCodons[i] >= domain.start && displayCodons[i] <= domain.end) {
            matchingIndices.push(i);
          }
        }
        if (!matchingIndices.length) continue;

        const firstIdx = matchingIndices[0];
        const lastIdx = matchingIndices[matchingIndices.length - 1];
        const yStart = padding.top + firstIdx * cellH;
        const yEnd = padding.top + (lastIdx + 1) * cellH;
        const h = Math.max(4, yEnd - yStart);

        ctx.fillStyle = domain.color || '#3b82f6';
        ctx.fillRect(padding.left, yStart, domainWidth, h);
      }
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
        ctx.fillStyle = 'rgba(56, 189, 248, 0.22)';
        ctx.fillRect(plotX, y - 1, plotW, cellH + 2);
      }

      for (let tIdx = 0; tIdx < time_points.length; tIdx++) {
        const x = plotX + tIdx * cellW;
        const vel = row ? (row[tIdx] || 0) : 0;
        if (vel > 0.0005) {
          ctx.fillStyle = getVelocityColor(vel, 0.035);
          ctx.fillRect(x, y, Math.ceil(cellW), Math.ceil(cellH));
        }
      }

      // Draw Codon Label on Left
      if (cellH >= 12 || isFocal || cIdx % 5 === 0) {
        ctx.fillStyle = isFocal ? '#38bdf8' : '#94a3b8';
        ctx.font = `${isFocal ? 'bold ' : ''}10px JetBrains Mono, monospace`;
        ctx.textAlign = 'right';
        ctx.fillText(String(codon), padding.left - 6, y + cellH * 0.8);
      }
    }

    // 3. Draw Hovered Cell Frame & Crosshairs
    if (hoveredCell) {
      const cIdx = displayCodons.indexOf(hoveredCell.codon);
      if (cIdx !== -1) {
        const hY = padding.top + cIdx * cellH;
        ctx.fillStyle = 'rgba(56, 189, 248, 0.14)';
        ctx.fillRect(plotX, hY, plotW, cellH);

        const tIdx = time_points.indexOf(hoveredCell.t);
        if (tIdx !== -1) {
          const hX = plotX + tIdx * cellW;
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 1.5;
          ctx.strokeRect(hX, hY, Math.ceil(cellW), Math.ceil(cellH));
        }
      }
    }

    // 4. Draw Temporal Cursor Line
    const cursorProgress = (surveillance.currentDate - tMin) / Math.max(0.01, tMax - tMin);
    const cursorX = plotX + Math.max(0, Math.min(1, cursorProgress)) * plotW;

    ctx.save();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(cursorX, padding.top);
    ctx.lineTo(cursorX, height - padding.bottom);
    ctx.stroke();

    ctx.fillStyle = '#38bdf8';
    ctx.beginPath();
    ctx.arc(cursorX, padding.top - 3, 3.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  $effect(() => {
    const _d = surveillance.currentDate;
    const _v = surveillance.velocityMatrix;
    const _f = surveillance.focalCodon;
    const _m = surveillance.sweepFilterMode;
    const _h = hoveredCell;
    renderWaterfall();
  });

  onMount(() => {
    const observer = new ResizeObserver(() => renderWaterfall());
    observer.observe(container);
    renderWaterfall();
    return () => observer.disconnect();
  });

  function handleMouseMove(e: MouseEvent) {
    if (!canvas || !container || !surveillance.velocityMatrix) {
      hoveredCell = null;
      return;
    }
    const rect = canvas.getBoundingClientRect();
    const clientX = e.clientX - rect.left;
    const clientY = e.clientY - rect.top;

    const width = container.clientWidth;
    const height = container.clientHeight;
    const vData = surveillance.velocityMatrix;
    const { codons, time_points, matrix } = vData;
    if (!codons?.length || !time_points?.length) {
      hoveredCell = null;
      return;
    }

    const padding = { top: 25, right: 35, bottom: 38, left: 65 };
    const domainWidth = 14;
    const plotX = padding.left + domainWidth + 8;
    const plotW = width - plotX - padding.right;
    const plotH = height - padding.top - padding.bottom;

    if (clientX < plotX || clientX > plotX + plotW || clientY < padding.top || clientY > padding.top + plotH) {
      hoveredCell = null;
      return;
    }

    const displayCodons = getDisplayCodons(vData, surveillance.sweepFilterMode);
    const nCodons = displayCodons.length;
    if (!nCodons) {
      hoveredCell = null;
      return;
    }

    const cIdx = Math.floor(((clientY - padding.top) / plotH) * nCodons);
    const tIdx = Math.floor(((clientX - plotX) / plotW) * time_points.length);

    if (cIdx >= 0 && cIdx < nCodons && tIdx >= 0 && tIdx < time_points.length) {
      const codon = displayCodons[cIdx];
      const t = time_points[tIdx];
      const origIdx = codons.indexOf(codon);
      const row = origIdx !== -1 ? matrix[origIdx] : null;
      const vel = row ? (row[tIdx] || 0) : 0;
      const domain = getCodonDomain(codon);
      const conf = vData.confirmed_sweeps?.find((s: any) => s.codon === codon);
      const resc = vData.rescued_sweeps?.find((s: any) => s.codon === codon);

      hoveredCell = {
        codon,
        t,
        dateStr: formatDateDisplay(t),
        vel,
        x: clientX,
        y: clientY,
        domain,
        confirmed: conf,
        rescued: resc,
      };
    } else {
      hoveredCell = null;
    }
  }

  function handleMouseLeave() {
    hoveredCell = null;
  }

  function handleCanvasClick(e: MouseEvent) {
    if (!canvas || !container || !surveillance.velocityMatrix) return;
    const rect = canvas.getBoundingClientRect();
    const y = e.clientY - rect.top;
    const padding = { top: 25, bottom: 25 };
    const plotH = container.clientHeight - padding.top - padding.bottom;

    const displayCodons = getDisplayCodons(surveillance.velocityMatrix, surveillance.sweepFilterMode);
    if (!displayCodons.length) return;

    const codonIdx = Math.floor(((y - padding.top) / plotH) * displayCodons.length);
    if (codonIdx >= 0 && codonIdx < displayCodons.length) {
      surveillance.setFocalCodon(displayCodons[codonIdx]);
    }
  }
</script>

<div class="h-full w-full flex flex-col glass-panel rounded-xl overflow-hidden relative">
  <!-- Top Navigation & Controls Bar -->
  <div class="h-10 border-b border-slate-800/80 px-3 flex items-center justify-between bg-dark-900/70 select-none shrink-0 z-10">
    <div class="flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-rose-500"></span>
      <span class="text-xs font-semibold tracking-wide text-slate-200">SELECTION SWEEP VELOCITY WATERFALL</span>
      <span class="text-[10px] font-mono text-slate-500">v_s(t) = max(0, da/dt)</span>
    </div>

    <!-- Center: Search Input -->
    <div class="hidden sm:flex items-center space-x-2">
      <div class="relative flex items-center">
        <input
          type="text"
          placeholder="Codon # (e.g. 456)..."
          bind:value={searchQuery}
          onkeydown={handleSearchKey}
          class="bg-dark-950 text-slate-200 text-xs font-mono px-2.5 py-1 rounded-lg border border-slate-700/80 focus:outline-none focus:border-sky-500 w-44 placeholder-slate-500"
        />
        {#if searchError}
          <div class="absolute -bottom-5 left-0 text-[10px] text-rose-400 font-mono whitespace-nowrap bg-dark-950 px-1 rounded">
            {searchError}
          </div>
        {/if}
      </div>
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
        Rescued ({surveillance.velocityMatrix?.rescued_sweeps?.length || 0})
      </button>
      <button
        onclick={() => (surveillance.sweepFilterMode = 'all')}
        class="px-2 py-0.5 rounded {surveillance.sweepFilterMode === 'all' ? 'bg-slate-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}"
      >
        All ({surveillance.velocityMatrix?.codons?.length || 0})
      </button>
    </div>
  </div>

  <!-- Focal Codon Inspector Strip -->
  {#if focalInfo}
    <div class="h-9 border-b border-sky-900/40 bg-sky-950/20 px-3 flex items-center justify-between text-xs select-none shrink-0">
      <div class="flex items-center space-x-3 text-[11px] font-mono truncate">
        <div class="flex items-center space-x-1.5 text-sky-300 font-bold">
          <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></span>
          <span>Codon #{focalInfo.codon}</span>
        </div>

        {#if focalInfo.domain}
          <span class="px-1.5 py-0.2 rounded text-[10px] bg-dark-900/80 border border-slate-700 text-slate-300" style="border-left: 3px solid {focalInfo.domain.color};">
            {focalInfo.domain.name}
          </span>
        {/if}

        <div class="text-slate-400 hidden md:inline">
          Velocity at {surveillance.currentDate.toFixed(2)}:
          <span class="text-rose-400 font-semibold">{focalInfo.currentVel.toFixed(4)} subs/site/yr</span>
        </div>

        {#if focalInfo.confirmed}
          <span class="px-1.5 py-0.2 rounded bg-rose-950 text-rose-300 border border-rose-800 text-[9px] hidden lg:inline">
            Peak: {focalInfo.confirmed.peak_velocity} (t={focalInfo.confirmed.peak_date.toFixed(2)}) &bull; p={focalInfo.confirmed.p_perm}
          </span>
        {:else if focalInfo.rescued}
          <span class="px-1.5 py-0.2 rounded bg-amber-950 text-amber-300 border border-amber-800 text-[9px] hidden lg:inline">
            Rescued from post-fixation dilution
          </span>
        {/if}
      </div>

      <div class="flex items-center space-x-2 text-[10px] font-mono">
        <button
          type="button"
          onclick={() => surveillance.setActiveTab('structure')}
          class="px-2.5 py-1 rounded bg-indigo-900/60 hover:bg-indigo-800/80 text-indigo-200 border border-indigo-500/40 transition-colors flex items-center space-x-1"
        >
          <span>Inspect in 3D Structure</span>
          <span>↗</span>
        </button>
        <button
          type="button"
          onclick={() => surveillance.setFocalCodon(null)}
          class="px-1.5 py-0.5 text-slate-400 hover:text-slate-200"
          title="Clear focal selection"
        >
          &times;
        </button>
      </div>
    </div>
  {:else}
    <div class="h-7 border-b border-slate-800/60 bg-dark-900/40 px-3 flex items-center text-[11px] font-mono text-slate-500 select-none shrink-0">
      <span>Click any codon row or enter a codon number above to lock a focal sweep trajectory.</span>
    </div>
  {/if}

  <!-- Canvas Surface -->
  <div class="flex-1 relative overflow-hidden" bind:this={container}>
    <canvas
      bind:this={canvas}
      onclick={handleCanvasClick}
      onmousemove={handleMouseMove}
      onmouseleave={handleMouseLeave}
      class="w-full h-full block cursor-pointer"
    ></canvas>

    <!-- Interactive Floating Tooltip -->
    {#if hoveredCell}
      {@const posX = Math.min(hoveredCell.x + 16, (container?.clientWidth || 800) - 270)}
      {@const posY = Math.max(12, Math.min(hoveredCell.y - 30, (container?.clientHeight || 500) - 170))}
      <div
        class="absolute pointer-events-none z-30 flex flex-col p-3 rounded-xl bg-dark-950/95 border border-slate-700/90 shadow-2xl backdrop-blur text-xs font-mono max-w-[260px] animate-in fade-in duration-100"
        style="left: {posX}px; top: {posY}px;"
      >
        <!-- Header -->
        <div class="flex items-center justify-between pb-1.5 border-b border-slate-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            <span class="font-bold text-sky-300 text-sm">Codon #{hoveredCell.codon}</span>
          </div>
          {#if hoveredCell.domain}
            <span
              class="text-[10px] px-1.5 py-0.5 rounded border font-semibold truncate max-w-[120px]"
              style="background-color: {hoveredCell.domain.color}22; color: {hoveredCell.domain.color}; border-color: {hoveredCell.domain.color}55;"
            >
              {hoveredCell.domain.name}
            </span>
          {/if}
        </div>

        <!-- Metrics -->
        <div class="py-2 space-y-1.5 text-[11px]">
          <div class="flex items-center justify-between text-slate-400">
            <span>Date:</span>
            <span class="text-slate-200 font-semibold">{hoveredCell.dateStr} <span class="text-slate-500">({hoveredCell.t.toFixed(2)})</span></span>
          </div>

          <div class="flex items-center justify-between">
            <span class="text-slate-400">Velocity v_s(t):</span>
            <div class="flex items-center space-x-1.5">
              <span
                class="w-2 h-2 rounded-full"
                style="background-color: {getVelocityColor(hoveredCell.vel, 0.035)};"
              ></span>
              <span class="font-bold" style="color: {hoveredCell.vel > 0.005 ? '#f43f5e' : '#94a3b8'};">
                {hoveredCell.vel.toFixed(4)}
              </span>
              <span class="text-[9px] text-slate-500">subs/yr</span>
            </div>
          </div>

          {#if hoveredCell.confirmed}
            <div class="mt-1 pt-1.5 border-t border-slate-800/80">
              <div class="text-[10px] text-rose-400 font-semibold flex items-center space-x-1">
                <span>⚡ Confirmed Adaptive Sweep</span>
              </div>
              <div class="text-[9px] text-slate-400 mt-0.5">
                Peak: {hoveredCell.confirmed.peak_velocity.toFixed(3)} at {hoveredCell.confirmed.peak_date.toFixed(2)} (p={hoveredCell.confirmed.p_perm})
              </div>
            </div>
          {:else if hoveredCell.rescued}
            <div class="mt-1 pt-1.5 border-t border-slate-800/80">
              <div class="text-[10px] text-amber-400 font-semibold flex items-center space-x-1">
                <span>🛡️ Rescued Selection Sweep</span>
              </div>
              <div class="text-[9px] text-slate-400 mt-0.5">
                Transient acceleration restored post-fixation
              </div>
            </div>
          {/if}
        </div>

        <!-- Footer Hint -->
        <div class="pt-1.5 border-t border-slate-800 text-[9px] text-sky-400/80 flex items-center space-x-1">
          <span>Click row to lock focal trajectory ↗</span>
        </div>
      </div>
    {/if}

    <!-- Legend Overlay -->
    <div class="absolute top-2 right-3 pointer-events-none flex items-center space-x-2 text-[10px] font-mono bg-dark-950/80 px-2.5 py-1 rounded border border-slate-800/60 backdrop-blur z-10">
      <span class="text-slate-400">Velocity:</span>
      <span class="w-2.5 h-2 rounded bg-sky-400"></span>
      <span class="text-slate-400">Low</span>
      <span class="w-2.5 h-2 rounded bg-amber-400"></span>
      <span class="text-slate-400">Med</span>
      <span class="w-2.5 h-2 rounded bg-rose-500"></span>
      <span class="text-slate-400">High (&gt;0.035)</span>
    </div>

    <div class="absolute bottom-2 left-3 pointer-events-none text-[10px] font-mono text-slate-500 bg-dark-950/80 px-2 py-1 rounded border border-slate-800/60 backdrop-blur z-10">
      Left Strip = Domain Architecture &bull; Rows = Codon Positions &bull; Heatmap = Nadaraya-Watson Instantaneous Velocity v_s(t)
    </div>
  </div>
</div>
