import React, { useEffect, useState } from 'react'
import api from '../api'

export default function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(false)

  const loadAlerts = async () => {
    setLoading(true)
    try {
      // Adjust if your backend has a different route for suspicious alerts
      const res = await api.get('/alerts/suspicious')
      setAlerts(res.data)
    } catch {
      setAlerts([])
    } finally {
      setLoading(false)
    }
  }

  const markSafe = async (alertId) => {
    await api.post(`/alerts/${alertId}/mark-safe`)
    loadAlerts()
  }

  const resolveAlert = async (alertId) => {
    await api.post(`/alerts/${alertId}/resolve`)
    loadAlerts()
  }

  useEffect(() => {
    loadAlerts()
  }, [])

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold text-slate-800">
          Suspicious Queries
        </h2>
        <button
          onClick={loadAlerts}
          className="btn btn-primary text-sm"
        >
          Refresh
        </button>
      </div>

      {loading && <p className="text-sm text-slate-500">Loading…</p>}

      {alerts.length === 0 && !loading && (
        <p className="text-sm text-slate-500">
          No suspicious queries at the moment.
        </p>
      )}

      <div className="space-y-3 mt-3">
        {alerts.map((alert) => (
          <div key={alert.alert_id} className="card">
            <div className="flex justify-between items-start gap-4">
              <div>
                <p className="text-sm font-semibold text-red-600">
                  {alert.alert_type || 'Suspicious Query'}
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  Score: {alert.confidence?.toFixed?.(2) ?? alert.confidence ?? '—'} |
                  Status: {alert.status}
                </p>
                {alert.query_text && (
                  <pre className="mt-2 text-xs bg-slate-900 text-slate-100 p-2 rounded-lg overflow-x-auto">
                    {alert.query_text}
                  </pre>
                )}
              </div>
              <div className="flex flex-col gap-2">
                <button
                  className="btn btn-success text-xs"
                  onClick={() => markSafe(alert.alert_id)}
                >
                  Mark as Safe
                </button>
                <button
                  className="btn btn-danger text-xs"
                  onClick={() => resolveAlert(alert.alert_id)}
                >
                  Resolve
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
