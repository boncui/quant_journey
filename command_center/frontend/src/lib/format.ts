/** Consistent, tabular number/date formatting across the terminal. */

export function num(x: number | null | undefined, digits = 2): string {
  if (x == null || !Number.isFinite(x)) return "–";
  return x.toLocaleString("en-US", { minimumFractionDigits: digits, maximumFractionDigits: digits });
}

export function bytes(n: number): string {
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  let v = n;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(i === 0 ? 0 : 1)}${units[i]}`;
}

export function ymd(iso: string | null | undefined): string {
  return iso ? iso.slice(0, 10) : "–";
}
