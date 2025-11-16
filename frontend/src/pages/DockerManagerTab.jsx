import { useEffect, useState } from "react";
import api from "../api";

export default function DockerManagerTab() {
  const [containers, setContainers] = useState([]);
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(false);

  const [showLogs, setShowLogs] = useState(false);
  const [logs, setLogs] = useState("");
  const [activeContainer, setActiveContainer] = useState("");

  const loadContainers = async () => {
    const res = await api.get("/api/docker/containers");
    setContainers(res.data);
  };

  const loadStats = async () => {
    const res = await api.get("/api/docker/stats");
    setStats(res.data);
  };

  const action = async (name, type) => {
    setLoading(true);
    await api.post(`/api/docker/${name}/${type}`);
    await loadContainers();
    await loadStats();
    setLoading(false);
  };

  const openLogs = async (name) => {
    setActiveContainer(name);
    const res = await api.get(`/api/docker/${name}/logs`);
    setLogs(res.data.logs);
    setShowLogs(true);
  };

  useEffect(() => {
    loadContainers();
    loadStats();
    const interval = setInterval(() => {
      loadContainers();
      loadStats();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const getStats = (name) => stats.find((s) => s.name === name);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-4 text-slate-800">
        Docker System Control & Health Monitor
      </h2>

      {loading && <p className="text-blue-600 mb-2">Performing action...</p>}

      <table className="w-full bg-white shadow rounded text-sm">
        <thead className="bg-slate-100">
          <tr>
            <th className="p-3 border">Name</th>
            <th className="p-3 border">Status</th>
            <th className="p-3 border">CPU %</th>
            <th className="p-3 border">RAM %</th>
            <th className="p-3 border">Uptime</th>
            <th className="p-3 border">Actions</th>
          </tr>
        </thead>

        <tbody>
          {containers.map((c) => {
            const st = getStats(c.name) || {};
            return (
              <tr key={c.id}>
                <td className="p-3 border">{c.name}</td>
                <td className="p-3 border">
                  <span
                    className={
                      c.status === "running"
                        ? "text-green-600 font-semibold"
                        : "text-red-600 font-semibold"
                    }
                  >
                    {c.status}
                  </span>
                </td>

                <td className="p-3 border">{st.cpu ?? "—"}%</td>
                <td className="p-3 border">{st.memory ?? "—"}%</td>
                <td className="p-3 border text-xs">{st.uptime}</td>

                <td className="p-3 border space-x-2">
                  {c.status === "running" ? (
                    <button
                      className="bg-red-500 text-white px-3 py-1 rounded"
                      onClick={() => action(c.name, "stop")}
                    >
                      Stop
                    </button>
                  ) : (
                    <button
                      className="bg-green-600 text-white px-3 py-1 rounded"
                      onClick={() => action(c.name, "start")}
                    >
                      Start
                    </button>
                  )}

                  <button
                    className="bg-blue-500 text-white px-3 py-1 rounded"
                    onClick={() => action(c.name, "restart")}
                  >
                    Restart
                  </button>

                  <button
                    className="bg-slate-700 text-white px-3 py-1 rounded"
                    onClick={() => openLogs(c.name)}
                  >
                    Logs
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Logs Modal */}
      {showLogs && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50">
          <div className="bg-white p-5 rounded-lg w-2/3 h-3/4 overflow-auto shadow-xl">
            <h3 className="text-lg font-semibold mb-3">{activeContainer} Logs</h3>
            <pre className="bg-slate-900 text-green-400 p-3 rounded h-full text-xs overflow-auto">
              {logs}
            </pre>

            <button
              className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
              onClick={() => setShowLogs(false)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
