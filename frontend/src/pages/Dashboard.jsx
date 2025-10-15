import { useEffect, useState } from "react";
import api from "../services/api";
import AlertFrequencyChart from "../components/Charts/AlertFrequencyChart";
import ConfidenceChart from "../components/Charts/ConfidenceChart";
import AlertFeed from "../components/AlertFeed";

export default function Dashboard() {
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    api.get("/logs/").then((res) => setLogs(res.data || []));
    api.get("/logs/alerts").then((res) => setAlerts(res.data || []));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen text-gray-800">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-blue-700">
          Security Dashboard
        </h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Logout
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <AlertFrequencyChart data={alerts} />
        <ConfidenceChart data={alerts} />
      </div>

      <AlertFeed logs={logs} />
    </div>
  );
}
