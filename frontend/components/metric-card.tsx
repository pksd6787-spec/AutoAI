export function MetricCard({ label, value, hint }: { label: string; value: string; hint: string }) {
  return <div className="card"><div className="score">{value}</div><p>{label}</p><small className="muted">{hint}</small></div>;
}
