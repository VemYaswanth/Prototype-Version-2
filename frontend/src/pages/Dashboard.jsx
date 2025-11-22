import React, { useEffect, useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate(); // ✅ MUST be here, NOT inside JSX

  useEffect(() => {
    const fetchMetrics = async () => {
      setLoading(true);
      try {
        const res = await api.get("/metrics/summary");
        console.log("Metrics from backend:", res.data);
        setMetrics(res.data);
      } catch (err) {
        console.error("Failed to load metrics:", err);
        setMetrics(null);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  const total = metrics?.total_queries ?? 0;
  const suspicious = metrics?.suspicious_queries ?? 0;
  const openAlerts = metrics?.open_alerts ?? 0;
  const verifiedPct = metrics?.blockchain_verified ?? 0;

  const chartData = [
    { label: "Total", value: total },
    { label: "Suspicious", value: suspicious },
    { label: "Alerts", value: openAlerts },
  ];
  const maxVal = Math.max(...chartData.map((d) => d.value), 1);

  return (
    <div className="p-6 space-y-6">
      {/* Header section */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-slate-800">Overview</h2>

        <div className="flex items-center gap-3">
          {loading && (
            <span className="text-xs text-slate-500">Updating metrics…</span>
          )}

          {/* 🔐 Enable MFA Button */}
          <button
            onClick={() => navigate("/mfa-setup")}
            className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg shadow hover:bg-blue-700 transition"
          >
            Enable Google Authenticator
          </button>
        </div>
      </div>

      {/* Top stats row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-xs text-slate-500">Total Queries (24h)</p>
          <p className="mt-2 text-3xl font-semibold text-slate-900">
            {metrics ? total.toLocaleString() : "—"}
          </p>
          <p className="mt-1 text-xs text-slate-400">
            All queries observed in the last 24 hours.
          </p>
        </div>

        <div className="card">
          <p className="text-xs text-slate-500">Suspicious Queries</p>
          <p className="mt-2 text-3xl font-semibold text-amber-600">
            {metrics ? suspicious.toLocaleString() : "—"}
          </p>
          <p className="mt-1 text-xs text-slate-400">
            Flagged by the AI scoring engine.
          </p>
        </div>

        <div className="card">
          <p className="text-xs text-slate-500">Open Alerts</p>
          <p className="mt-2 text-3xl font-semibold text-red-600">
            {metrics ? openAlerts.toLocaleString() : "—"}
          </p>
          <p className="mt-1 text-xs text-slate-400">
            Still requiring manual review.
          </p>
        </div>

        <div className="card">
          <p className="text-xs text-slate-500">Blockchain Verified Logs (%)</p>
          <p className="mt-2 text-3xl font-semibold text-emerald-600">
            {metrics ? `${verifiedPct}%` : "—%"}
          </p>
          <div className="mt-2 h-2 rounded-full bg-emerald-100 overflow-hidden">
            <div
              className="h-full bg-emerald-500 transition-all"
              style={{ width: `${Math.min(verifiedPct, 100)}%` }}
            />
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Logs anchored to the blockchain.
          </p>
        </div>
      </div>

      {/* Bottom section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          <div className="card">
            <h3 className="font-semibold mb-1">Recent Alerts</h3>
            <p className="text-sm text-slate-500">
              Use the <span className="font-semibold">Suspicious Queries</span>{" "}
              tab to review alerts flagged by the anomaly detector.
            </p>
          </div>

          <div className="card">
            <h3 className="font-semibold mb-1">System Health</h3>
            <p className="text-sm text-slate-500">
              Manage real-time system state using the{" "}
              <span className="font-semibold">System Control</span> tab.
            </p>
          </div>
        </div>

        {/* Sidebar mini chart */}
        <div className="card flex flex-col">
          <h3 className="font-semibold mb-2">Traffic Snapshot</h3>
          <p className="text-xs text-slate-500 mb-3">
            Relative volume of total vs suspicious queries and alerts.
          </p>

          <div className="flex items-end gap-3 flex-1">
            {chartData.map((item) => (
              <div
                key={item.label}
                className="flex flex-col items-center flex-1"
              >
                <div className="w-full bg-slate-100 rounded-lg h-24 flex items-end overflow-hidden">
                  <div
                    className={
                      item.label === "Suspicious"
                        ? "w-full bg-amber-500"
                        : item.label === "Alerts"
                        ? "w-full bg-red-500"
                        : "w-full bg-blue-500"
                    }
                    style={{
                      height: `${(item.value / maxVal) * 100 || 5}%`,
                    }}
                  />
                </div>
                <span className="mt-1 text-xs text-slate-500">
                  {item.label}
                </span>
                <span className="text-xs font-semibold text-slate-800">
                  {metrics ? item.value.toLocaleString() : "—"}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
