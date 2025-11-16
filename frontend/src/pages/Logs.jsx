import React, { useEffect, useState } from "react"
import api from "../api"

export default function Logs() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)

  const loadLogs = async () => {
    setLoading(true)
    try {
      const res = await api.get("/logs/")
      setLogs(res.data)
    } catch (err) {
      console.error("Error loading logs:", err)
      setLogs([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadLogs()
  }, [])

  const formatTime = (ts) => {
    if (!ts) return "—"
    try {
      return new Date(ts).toLocaleString()
    } catch {
      return ts
    }
  }

  const opColor = {
    SELECT: "bg-blue-100 text-blue-700",
    INSERT: "bg-emerald-100 text-emerald-700",
    UPDATE: "bg-amber-100 text-amber-700",
    DELETE: "bg-red-100 text-red-700",
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-2xl font-semibold text-slate-800">
          Recent Query Logs
        </h2>
        <button
          onClick={loadLogs}
          className="px-3 py-1.5 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700 transition"
        >
          Refresh
        </button>
      </div>

      {loading && (
        <p className="text-sm text-slate-500 mb-3">Loading…</p>
      )}

      {/* Logs Table */}
      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-50 text-slate-500">
            <tr>
              <th className="px-3 py-2 text-left">Time</th>
              <th className="px-3 py-2 text-left">User</th>
              <th className="px-3 py-2 text-left">Operation</th>
              <th className="px-3 py-2 text-left">Query</th>
              <th className="px-3 py-2 text-left">Blockchain Hash</th>
            </tr>
          </thead>

          <tbody>
            {logs.map((log) => (
              <tr
                key={log.log_id}
                className="border-t border-slate-100 hover:bg-slate-50"
              >
                {/* Time */}
                <td className="px-3 py-2 text-xs">
                  {formatTime(log.executed_at)}
                </td>

                {/* User */}
                <td className="px-3 py-2 text-xs">
                  User {log.user_id}
                </td>

                {/* Operation badge */}
                <td className="px-3 py-2 text-xs">
                  <span
                    className={`px-2 py-0.5 rounded-full ${
                      opColor[log.operation_type] || "bg-slate-200 text-slate-700"
                    }`}
                  >
                    {log.operation_type}
                  </span>
                </td>

                {/* Query text */}
                <td className="px-3 py-2 text-xs max-w-lg truncate font-mono">
                  {log.query_text}
                </td>

                {/* Hash */}
                <td className="px-3 py-2 text-xs font-mono">
                  {log.blockchain_hash ? log.blockchain_hash : "—"}
                </td>
              </tr>
            ))}

            {/* Empty State */}
            {!loading && logs.length === 0 && (
              <tr>
                <td
                  colSpan={5}
                  className="px-3 py-6 text-center text-sm text-slate-500"
                >
                  No logs available.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}