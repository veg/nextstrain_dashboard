/**
 * Color scales and palette helpers for surveillance visualization
 */

export const COMMUNITY_PALETTE = [
  '#3b82f6', // Sapphire Blue
  '#10b981', // Emerald Green
  '#f59e0b', // Amber
  '#ec4899', // Rose Pink
  '#8b5cf6', // Violet
  '#06b6d4', // Cyan
  '#f97316', // Orange
  '#84cc16', // Lime
];

export function hexToRgb(hex: string): [number, number, number] {
  const cleanHex = hex.replace('#', '');
  const r = parseInt(cleanHex.substring(0, 2), 16) || 0;
  const g = parseInt(cleanHex.substring(2, 4), 16) || 0;
  const b = parseInt(cleanHex.substring(4, 6), 16) || 0;
  return [r, g, b];
}

export function getCommunityColor(communityId: number): string {
  return COMMUNITY_PALETTE[Math.abs(communityId) % COMMUNITY_PALETTE.length];
}

export function getCommunityRgb(communityId: number): [number, number, number] {
  return hexToRgb(getCommunityColor(communityId));
}

/**
 * Maps positive sweep velocity v to continuous flame / glow color.
 * Low: transparent/muted cyan -> Moderate: gold/amber -> High: fiery crimson
 */
export function getVelocityColor(v: number, maxV: number = 0.04): string {
  if (v <= 0.0005) return 'rgba(30, 41, 59, 0.4)';
  const norm = Math.min(1.0, Math.max(0.0, v / maxV));

  if (norm < 0.25) {
    // Cyan to blue
    return `rgba(56, 189, 248, ${0.4 + norm * 1.5})`;
  } else if (norm < 0.6) {
    // Amber to gold
    return `rgba(245, 158, 11, ${0.7 + (norm - 0.25) * 0.8})`;
  } else {
    // Intense crimson flame
    return `rgba(239, 68, 68, ${0.85 + (norm - 0.6) * 0.35})`;
  }
}

export function getVelocityRgb(v: number, maxV: number = 0.04): [number, number, number] {
  if (v <= 0.0005) return [51, 65, 85];
  const norm = Math.min(1.0, Math.max(0.0, v / maxV));

  if (norm < 0.25) {
    return [56, 189, 248];
  } else if (norm < 0.6) {
    return [245, 158, 11];
  } else {
    return [239, 68, 68];
  }
}
