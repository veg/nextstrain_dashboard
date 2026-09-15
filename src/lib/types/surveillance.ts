/**
 * TypeScript Data Contracts for the NextGen Pathogen Surveillance Cockpit
 */

export interface CommunityMeta {
  id: number;
  rate: number;          // subs/site/year
  r2: number;            // molecular clock linearity
  tmrca: number;         // emergence horizon
  taxa_count: number;
  color: string;
  timespan?: [number, number];
}

export interface StreamlineKnot {
  t: number;             // Decimal calendar year
  y: number;             // Manifold divergence
  w: number;             // Lineage volume / width
  community: number;     // AutoClock community index
  clade?: string;
  n_obs?: number;
}

export interface StreamlineRibbon {
  lineage_id: string;
  community: number;
  knots: StreamlineKnot[];
}

export interface StreamlinePayload {
  pathogen_id: string;
  name: string;
  time_range: [number, number];
  divergence_range: [number, number];
  communities: CommunityMeta[];
  ribbons: StreamlineRibbon[];
}

export interface ProteinDomain {
  name: string;
  start: number;
  end: number;
  color: string;
}

export interface ConfirmedSweep {
  codon: number;
  peak_velocity: number;
  peak_date: number;
  auc: number;
  p_perm: number;
  r2_wave: number;
}

export interface RescuedSweep {
  codon: number;
  peak_velocity: number;
  cumulative_dnds: number;
  dilution_factor: number;
  phenotype_note: string;
}

export interface VelocityPayload {
  pathogen_id: string;
  protein: string;
  gene: string;
  length: number;
  time_points: number[];
  codons: number[];
  matrix: number[][]; // [codon_idx][time_idx] -> velocity
  confirmed_sweeps: ConfirmedSweep[];
  rescued_sweeps: RescuedSweep[];
  domains: ProteinDomain[];
  surveillance_codons: number[];
}

export interface EpistasisNode {
  id: number;
  codon: number;
  name: string;
  degree: number;
  domain?: string;
}

export interface EpistasisEdge {
  source: number;
  target: number;
  cesi: number;
  sim: number;
  shared_branches: number;
}

export interface EpistasisSector {
  sector_id: number;
  members: number[];
  coherence: number;
  name?: string;
}

export interface EpistasisPayload {
  pathogen_id: string;
  nodes: EpistasisNode[];
  edges: EpistasisEdge[];
  sectors: EpistasisSector[];
}

export interface QuarantinedOutlier {
  strain: string;
  date: number;
  community: number;
  divergence: number;
  residual: number;
  studentized_residual: number;
  is_sus: boolean;
  classification: 'sequencing_artifact' | 'genuine_saltation';
  reasons: string[];
}

export interface AutoClockPayload {
  pathogen_id: string;
  optimal_k: number;
  communities: CommunityMeta[];
  outliers: QuarantinedOutlier[];
}

export interface SweepAcceleration {
  codon: number;
  previous_velocity: number;
  current_velocity: number;
  acceleration_factor: number;
}

export interface DeltaReport {
  date: string;
  pathogen_id: string;
  alert_level: 'Tier-1 High Velocity Sweep' | 'Tier-2 Moderate Velocity' | 'Nominal';
  newly_confirmed_sweeps: ConfirmedSweep[];
  accelerations: SweepAcceleration[];
  new_clock_communities: CommunityMeta[];
  new_quarantined_outliers: QuarantinedOutlier[];
  active_codons_summary: string[];
  executive_summary: string;
}

export interface DeepLinkToken {
  token: string;
  date: number;
  codon?: number;
  community?: number;
}

export interface DispatchMetadata {
  id: string;
  date: string;
  pathogen_id: string;
  pathogen_name: string;
  title: string;
  alert_tier: 1 | 2 | 3;
  focal_codons: number[];
  deep_links: DeepLinkToken[];
}

export interface DispatchPayload {
  metadata: DispatchMetadata;
  markdown: string;
}
