import React, { useEffect, useState } from 'react'
import api from '../api'

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchMetrics = async () => {
      setLoading(true)
      try {
        const res = await api.get('/metrics/summary')
        console.log('Metrics from backend:', res.data)
        setMetrics(res.data)
      } catch (err) {
        console.error('Failed to load metrics:', err)
        setMetrics(null)
      } finally {
        setLoading(false)
      }
    }
    fetchMetrics()
  }, [])

  const total = metrics?.total_queries ?? 0
  const suspicious = metrics?.suspicious_queries ?? 0
  const openAlerts = metrics?.open_alerts ?? 0
  const verifiedPct = metrics?.blockchain_verified ?? 0

  const chartData = [
    { label: 'Total', value: total },
    { label: 'Suspicious', value: suspicious },
    { label: 'Alerts', value: openAlerts }
  ]
  const maxVal = Math.max(...chartData.map(d => d.value), 1)

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-slate-800">
          Overview
        </h2>
        {loading && (
          <span className="text-xs text-slate-500">
            Updating metrics…
          </span>
        )}
      </div>

      {/* Top stats row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-xs text-slate-500">Total Queries (24h)</p>
          <p className="mt-2 text-3xl font-semibold text-slate-900">
            {metrics ? total.toLocaleString() : '—'}
          </p>
          <p className="mt-1 text-xs text-slate-400">
            All queries observed in the last 24 hours.
          </p>
        </div>

        <div className="card">
          <p className="text-xs text-slate-500">Suspicious Queries</p>
          <p className="mt-2 text-3xl font-semibold text-amber-600">
            {metrics ? suspicious.toLocaleString() : '—'}
          </p>
          <p className="mt-1 text-xs text-slate-400">
            Flagged by the AI scoring engine.
          </p>
        </div>

        <div className="card">
          <p className="text-xs text-slate-500">Open Alerts</p>
          <p className="mt-2 text-3xl font-semibold text-red-600">
            {metrics ? openAlerts.toLocaleString() : '—'}
          </p>
          <p className="mt-1 text-xs text-slate-400">
            Still requiring manual review.
          </p>
        </div>

        <div className="card">
          <p className="text-xs text-slate-500">Blockchain Verified Logs (%)</p>
          <p className="mt-2 text-3xl font-semibold text-emerald-600">
            {metrics ? `${verifiedPct}%` : '—%'}
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

      {/* Bottom section: left = info cards, right = mini graph sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          <div className="card">
            <h3 className="font-semibold mb-1">Recent Alerts</h3>
            <p className="text-sm text-slate-500">
              Use the <span className="font-semibold">Suspicious Queries</span> tab to
              review and mark queries as safe or resolved. Alerts update in real time as
              new anomalous queries are detected.
            </p>
          </div>

          <div className="card">
            <h3 className="font-semibold mb-1">System Health</h3>
            <p className="text-sm text-slate-500">
              Use the <span className="font-semibold">System Control</span> tab to
              start/stop Docker services from the dashboard instead of the terminal.
              Keep the data generator, analyzer, and API healthy for accurate detection.
            </p>
          </div>
        </div>

        {/* “Graph sidebar” on the right */}
        <div className="card flex flex-col">
          <h3 className="font-semibold mb-2">Traffic Snapshot</h3>
          <p className="text-xs text-slate-500 mb-3">
            Relative volume of total vs suspicious queries and open alerts.
          </p>

          <div className="flex items-end gap-3 flex-1">
            {chartData.map((item) => (
              <div key={item.label} className="flex flex-col items-center flex-1">
                <div className="w-full bg-slate-100 rounded-lg h-24 flex items-end overflow-hidden">
                  <div
                    className={
                      item.label === 'Suspicious'
                        ? 'w-full bg-amber-500'
                        : item.label === 'Alerts'
                        ? 'w-full bg-red-500'
                        : 'w-full bg-blue-500'
                    }
                    style={{ height: `${(item.value / maxVal) * 100 || 5}%` }}
                  />
                </div>
                <span className="mt-1 text-xs text-slate-500">{item.label}</span>
                <span className="text-xs font-semibold text-slate-800">
                  {metrics ? item.value.toLocaleString() : '—'}
                </span>
              </div>
            ))}
          </div>

          {!metrics && (
            <p className="mt-3 text-[11px] text-slate-400">
              Metrics not loaded yet – check that <code>/metrics/summary</code> is reachable.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
