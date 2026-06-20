const rows = [
  ["Space debris economy", "87", "74", "81", "approved"],
  ["AI chip supply chain", "76", "63", "88", "watchlist"],
  ["Lost city rediscovery", "69", "80", "55", "rejected"],
];
export default function OpportunitiesPage(){return <section><h2>Opportunities</h2><p className="muted">Trend discoveries ranked by viral, opportunity, and monetization thresholds.</p><table className="table"><thead><tr><th>Topic</th><th>Viral</th><th>Opportunity</th><th>Money</th><th>Status</th></tr></thead><tbody>{rows.map(row=><tr key={row[0]}>{row.map(cell=><td key={cell}>{cell}</td>)}</tr>)}</tbody></table></section>}
