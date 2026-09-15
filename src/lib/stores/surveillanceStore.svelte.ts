import type {
  AutoClockPayload,
  DeltaReport,
  DispatchPayload,
  EpistasisEdge,
  EpistasisPayload,
  StreamlinePayload,
  VelocityPayload,
} from '$lib/types/surveillance';
import { base } from '$app/paths';

export function resolveAssetUrl(path: string): string {
  const clean = path.startsWith('/') ? path.slice(1) : path;
  if (base) {
    return `${base}/${clean}`;
  }
  if (typeof window !== 'undefined' && window.location.pathname.includes('/nextstrain_dashboard')) {
    return `/nextstrain_dashboard/${clean}`;
  }
  return `/${clean}`;
}

export class SurveillanceStore {
  // Navigation & Time
  currentPathogen = $state<string>('sars-cov-2');
  currentDate = $state<number>(2024.4);
  isPlaying = $state<boolean>(false);
  playbackSpeed = $state<number>(1.0);
  timeRange = $state<[number, number]>([2020.0, 2026.6]);
  activeTab = $state<'briefing' | 'clocks' | 'selection' | 'structure'>('briefing');

  // Interactive Filters
  focalCodon = $state<number | null>(456);
  hoveredCodon = $state<number | null>(null);
  selectedClockCommunity = $state<number | null>(null);
  sweepFilterMode = $state<'all' | 'confirmed' | 'rescued'>('confirmed');

  // Loaded Data Payloads
  streamlines = $state<StreamlinePayload | null>(null);
  velocityMatrix = $state<VelocityPayload | null>(null);
  epistasisGraph = $state<EpistasisPayload | null>(null);
  autoClockTriage = $state<AutoClockPayload | null>(null);
  deltaReport = $state<DeltaReport | null>(null);
  currentDispatch = $state<DispatchPayload | null>(null);
  registry = $state<any>(null);
  isLoading = $state<boolean>(true);

  // Derived: Interpolated residue velocities at cursor date
  activeResidueVelocities = $derived.by(() => {
    const velMap = new Map<number, number>();
    if (!this.velocityMatrix) return velMap;

    const { codons, time_points, matrix } = this.velocityMatrix;
    if (!codons.length || !time_points.length || !matrix.length) return velMap;

    // Find bounding time indices for linear interpolation
    const t = this.currentDate;
    let idxA = 0;
    let idxB = time_points.length - 1;

    for (let i = 0; i < time_points.length - 1; i++) {
      if (t >= time_points[i] && t <= time_points[i + 1]) {
        idxA = i;
        idxB = i + 1;
        break;
      }
    }

    const tA = time_points[idxA];
    const tB = time_points[idxB];
    const alpha = tB > tA ? (t - tA) / (tB - tA) : 0;

    for (let i = 0; i < codons.length; i++) {
      const codon = codons[i];
      const row = matrix[i];
      if (!row) continue;
      const vA = row[idxA] || 0;
      const vB = row[idxB] || 0;
      const vInterp = vA + (vB - vA) * alpha;
      velMap.set(codon, Math.max(0, vInterp));
    }

    return velMap;
  });

  // Derived: Active epistatic edges touching focal codon
  activeEpistaticEdges = $derived.by(() => {
    if (!this.epistasisGraph) return [];
    if (this.focalCodon === null) return this.epistasisGraph.edges.slice(0, 40);
    return this.epistasisGraph.edges.filter(
      (e: EpistasisEdge) => e.source === this.focalCodon || e.target === this.focalCodon
    );
  });

  // Derived: Quarantined outliers matching current community or temporal window
  activeQuarantinedOutliers = $derived.by(() => {
    if (!this.autoClockTriage) return [];
    const outliers = this.autoClockTriage.outliers || [];
    if (this.selectedClockCommunity !== null) {
      return outliers.filter((o) => o.community === this.selectedClockCommunity);
    }
    return outliers;
  });

  async loadRegistry() {
    try {
      const res = await fetch(resolveAssetUrl('data/registry.json'));
      if (res.ok) {
        this.registry = await res.json();
      }
    } catch (e) {
      console.warn('Failed to load registry:', e);
    }
  }

  async loadPathogen(pathogenId: string) {
    this.isLoading = true;
    this.currentPathogen = pathogenId;
    this.selectedClockCommunity = null;
    this.focalCodon = null;
    this.hoveredCodon = null;

    try {
      const [streamlinesRes, velocityRes, epistasisRes, triageRes, deltaRes] = await Promise.allSettled([
        fetch(resolveAssetUrl(`data/${pathogenId}/manifold_streamlines.json`)),
        fetch(resolveAssetUrl(`data/${pathogenId}/sweep_velocity.json`)),
        fetch(resolveAssetUrl(`data/${pathogenId}/epistasis_cesi.json`)),
        fetch(resolveAssetUrl(`data/${pathogenId}/autoclock_triage.json`)),
        fetch(resolveAssetUrl(`data/${pathogenId}/delta_report.json`)),
      ]);

      if (streamlinesRes.status === 'fulfilled' && streamlinesRes.value.ok) {
        this.streamlines = await streamlinesRes.value.json();
        if (this.streamlines?.time_range) {
          this.timeRange = this.streamlines.time_range;
          this.currentDate = this.timeRange[1]; // Default to most recent surveillance date
        }
      } else {
        this.streamlines = null;
      }

      if (velocityRes.status === 'fulfilled' && velocityRes.value.ok) {
        this.velocityMatrix = await velocityRes.value.json();
        // Pre-select first confirmed sweep or key surveillance codon
        if (this.velocityMatrix?.confirmed_sweeps?.length) {
          this.focalCodon = this.velocityMatrix.confirmed_sweeps[0].codon;
        } else if (this.velocityMatrix?.surveillance_codons?.length) {
          this.focalCodon = this.velocityMatrix.surveillance_codons[0];
        } else if (this.velocityMatrix?.codons?.length) {
          this.focalCodon = this.velocityMatrix.codons[0];
        }
      } else {
        this.velocityMatrix = null;
      }

      if (epistasisRes.status === 'fulfilled' && epistasisRes.value.ok) {
        this.epistasisGraph = await epistasisRes.value.json();
      } else {
        this.epistasisGraph = null;
      }

      if (triageRes.status === 'fulfilled' && triageRes.value.ok) {
        this.autoClockTriage = await triageRes.value.json();
      } else {
        this.autoClockTriage = null;
      }

      if (deltaRes.status === 'fulfilled' && deltaRes.value.ok) {
        this.deltaReport = await deltaRes.value.json();
      } else {
        this.deltaReport = null;
      }
    } catch (err) {
      console.error('Error loading surveillance payloads:', err);
    } finally {
      this.isLoading = false;
    }
  }

  setFocalCodon(codon: number | null) {
    this.focalCodon = codon;
  }

  setCurrentDate(d: number) {
    this.currentDate = Math.max(this.timeRange[0], Math.min(this.timeRange[1], d));
  }

  togglePlay() {
    this.isPlaying = !this.isPlaying;
  }

  setPlaybackSpeed(speed: number) {
    this.playbackSpeed = speed;
  }

  setActiveTab(tab: 'briefing' | 'clocks' | 'selection' | 'structure') {
    this.activeTab = tab;
    if (typeof window !== 'undefined') {
      const url = new URL(window.location.href);
      url.searchParams.set('tab', tab);
      window.history.replaceState({}, '', url.toString());
    }
  }

  jumpToKeyframe(date: number, codon?: number, targetTab?: 'briefing' | 'clocks' | 'selection' | 'structure') {
    this.setCurrentDate(date);
    if (codon !== undefined) {
      this.setFocalCodon(codon);
    }
    if (targetTab) {
      this.setActiveTab(targetTab);
    }
  }

  tick(deltaMs: number) {
    if (!this.isPlaying) return;
    const yearDelta = (deltaMs / 1000) * 0.15 * this.playbackSpeed;
    let nextDate = this.currentDate + yearDelta;
    if (nextDate > this.timeRange[1]) {
      nextDate = this.timeRange[0];
    }
    this.currentDate = nextDate;
  }
}

export const surveillance = new SurveillanceStore();
