import React, { useEffect, useState } from 'react'
import api from '../api'

// Simple toast system
const Toast = ({ message }) => (
  <div className="fixed top-4 right-4 bg-green-600 text-white px-4 py-2 rounded shadow-lg animate-fade-in">
    {message}
  </div>
)

export default function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(false)
  const [toastMsg, setToastMsg] = useState('')
  const [filter, setFilter] = useState('Open') // Default filter
  const [hideAnimation, setHideAnimation] = useState({})

  // Fetch alerts from backend
  const loadAlerts = async () => {
    setLoading(true)
    try {
      const res = await api.get('/logs/alerts')

      // Apply filter
      let filtered = res.data

      if (filter !== 'All') {
        filtered = filtered.filter(a => a.status === filter)
      }

      setAlerts(filtered)
    } catch {
      setAlerts([])
    } finally {
      setLoading(false)
    }
  }

  // Show toast for 2 seconds
  const showToast = (msg) => {
    setToastMsg(msg)
    setTimeout(() => setToastMsg(''), 2000)
  }

  // Handle Safe button
  const markSafe = async (alertId) => {
    setHideAnimation(prev => ({ ...prev, [alertId]: true }))
    await api.post(`/logs/alerts/${alertId}/mark-safe`)
    showToast('Alert marked as safe!')
    setTimeout(loadAlerts, 300) // Delay to allow animation
  }

  // Handle Resolve button
  const resolveAlert = async (alertId) => {
    setHideAnimation(prev => ({ ...prev, [alertId]: true }))
    await api.post(`/logs/alerts/${alertId}/resolve`)
    showToast('Alert resolved!')
    setTimeout(loadAlerts, 300)
  }

  // Auto-refresh every 5 seconds
  useEffect(() => {
    loadAlerts()
    const interval = setInterval(loadAlerts, 5000)
    return () => clearInterval(interval)
  }, [filter]) // refetch when filter changes

  const statusColors = {
    Open: 'bg-red-100 text-red-700',
    Safe: 'bg-emerald-100 text-emerald-700',
    Resolved: 'bg-blue-100 text-blue-700'
  }

  return (
    <div className="p-6">

      {/* Toast */}
      {toastMsg && <Toast message={toastMsg} />}

      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-2xl font-semibold text-slate-800">Alerts</h2>
        <button onClick={loadAlerts} className="btn btn-primary text-sm">
          Refresh
        </button>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-3 mb-5">
        {['All','Open','Safe','Resolved'].map(tab => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-3 py-1.5 rounded-full text-sm border 
              ${filter === tab ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border-slate-300'}
            `}
          >
            {tab}
          </button>
        ))}
      </div>

      {loading && <p className="text-sm text-slate-500">Loading…</p>}

      {alerts.length === 0 && !loading && (
        <p className="text-sm text-slate-500">No alerts found.</p>
      )}

      {/* Alerts List */}
      <div className="space-y-3 mt-3">

        {alerts.map(alert => (
          <div
            key={alert.alert_id}
            className={`card transition-all duration-300 ${
              hideAnimation[alert.alert_id] ? 'opacity-0 -translate-y-2' : 'opacity-100'
            }`}
          >
            <div className="flex justify-between items-start gap-4">

              {/* Left Column */}
              <div>
                {/* Status badge */}
                <span
                  className={`px-2 py-1 text-xs rounded-full ${statusColors[alert.status]}`}
                >
                  {alert.status}
                </span>

                <p className="text-sm font-semibold text-red-600 mt-2">
                  {alert.alert_type || 'Suspicious Query'}
                </p>

                <p className="text-xs text-slate-500 mt-1">
                  Confidence: {(alert.confidence * 100).toFixed(1)}%
                </p>

                <p className="text-xs text-slate-400">
                  Created: {alert.created_at}
                </p>
              </div>

              {/* Buttons */}
              <div className="flex flex-col gap-2">
                {alert.status === 'Open' && (
                  <>
                    <button
                      className="btn btn-success text-xs"
                      onClick={() => markSafe(alert.alert_id)}
                    >
                      Mark Safe
                    </button>

                    <button
                      className="btn btn-danger text-xs"
                      onClick={() => resolveAlert(alert.alert_id)}
                    >
                      Resolve
                    </button>
                  </>
                )}

                {alert.status !== 'Open' && (
                  <span className="text-xs text-slate-400">No actions</span>
                )}
              </div>

            </div>
          </div>
        ))}

      </div>
    </div>
  )
}