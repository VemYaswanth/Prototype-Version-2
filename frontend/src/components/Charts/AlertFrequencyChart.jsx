import { useMemo } from "react";

export default function AlertFrequencyChart({ data }){
  // Replace with recharts later; simple placeholder
  const count = useMemo(() => data.length, [data]);
  return <div className="border rounded p-4">Alert Count (placeholder): {count}</div>;
}
