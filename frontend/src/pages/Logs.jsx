import React, { useEffect, useState } from 'react'
import api from '../api'

export default function Logs() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)

  const loadLogs = async () => {
    setLoading(true)
    try {
      // Adjust to your backend route for recent query logs
      const res = await api.get('/query-logs/recent')
      setLogs(res.data)
    } catch {
      setLogs([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadLogs()
  }, [])

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold text-slate-800">
          Recent Query Logs
        </h2>
        <button
          onClick={loadLogs}
          className="btn btn-primary text-sm"
        >
          Refresh
        </button>
      </div>

      {loading && <p className="text-sm text-slate-500">Loading…</p>}

      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-50 text-slate-500">
            <tr>
              <th className="px-3 py-2 text-left">Time</th>
              <th className="px-3 py-2 text-left">User</th>
              <th className="px-3 py-2 text-left">Operation</th>
              <th className="px-3 py-2 text-left">Client IP</th>
              <th className="px-3 py-2 text-left">Query</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.log_id} className="border-t border-slate-100">
                <td className="px-3 py-2 text-xs">
                  {log.executed_at}
                </td>
                <td className="px-3 py-2 text-xs">
                  {log.user_email || log.user_id}
                </td>
                <td className="px-3 py-2 text-xs">
                  <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                    {log.operation_type}
                  </span>
                </td>
                <td className="px-3 py-2 text-xs">
                  {log.client_ip}
                </td>
                <td className="px-3 py-2 text-xs max-w-xl truncate">
                  {log.query_text}
                </td>
              </tr>
            ))}

            {!loading && logs.length === 0 && (
              <tr>
                <td
                  colSpan={5}
                  className="px-3 py-4 text-center text-sm text-slate-500"
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
