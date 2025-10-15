export default function ConfidenceChart({ data }){
  const avg = data.length ? (data.reduce((s,a)=>s+(a.confidence||0),0)/data.length).toFixed(2) : 0;
  return <div className="border rounded p-4">Avg Confidence (placeholder): {avg}</div>;
}
