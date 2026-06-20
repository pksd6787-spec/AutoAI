const jobs = [
  ["trend_discovery", "completed", "1", "no"],
  ["research", "running", "1", "yes"],
  ["fact_verification", "queued", "0", "no"],
  ["media_generation", "queued", "0", "yes"],
];

export default function WorkflowsPage(){return <section><h2>Workflow Engine</h2><p className="muted">Queue, retry, resume, pause, cancel, and parallel processing control for daily documentary runs.</p><div className="grid"><div className="card"><strong>Active workflow</strong><p>daily_documentary</p><small className="muted">Project: default-channel</small></div><div className="card"><strong>Queue depth</strong><p className="score">4</p><small className="muted">Pending jobs</small></div></div><table className="table"><thead><tr><th>Job</th><th>Status</th><th>Attempts</th><th>Parallel</th></tr></thead><tbody>{jobs.map(row=><tr key={row[0]}>{row.map(cell=><td key={cell}>{cell}</td>)}</tr>)}</tbody></table></section>}
