import { useEffect, useState } from "react";
import api from "../services/api";
import AlertFrequencyChart from "../components/Charts/AlertFrequencyChart";
import ConfidenceChart from "../components/Charts/ConfidenceChart";

export default function Dashboard(){
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    api.get("/logs/").then(({data}) => setLogs(data));
    api.get("/logs/alerts").then(({data}) => setAlerts(data));
  }, []);

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-2xl font-semibold">Security Dashboard</h1>
      <AlertFrequencyChart data={alerts} />
      <ConfidenceChart data={alerts} />
      <div className="border rounded p-4">
        <h2 className="font-semibold mb-2">Recent Query Logs</h2>
        <ul className="space-y-1">
          {logs.map(l => (
            <li key={l.id} className="text-sm">[{l.operation}] {l.query} <em className="opacity-60">{l.time}</em></li>
          ))}
        </ul>
      </div>
    </div>
  );
}
