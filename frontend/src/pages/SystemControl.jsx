import React, { useState } from 'react'
import api from '../api'

export default function SystemControl() {
  const [output, setOutput] = useState('')
  const [busy, setBusy] = useState(false)

  const callAction = async (action) => {
    setBusy(true)
    try {
      // These endpoints must exist in backend;
      // they only wrap docker compose, no backend logic needs to change.
      const res = await api.post(`/system/${action}`)
      setOutput(res.data.message || JSON.stringify(res.data, null, 2))
    } catch (err) {
      setOutput('Error: ' + (err.response?.data?.message || err.message))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-semibold text-slate-800">
        System Control
      </h2>
      <p className="text-sm text-slate-500 mb-2">
        Use these controls to manage Docker containers from the UI instead of the terminal.
        This will not modify backend logic; it only invokes existing Docker commands.
      </p>

      <div className="flex flex-wrap gap-3">
        <button
          className="btn btn-danger text-sm"
          disabled={busy}
          onClick={() => callAction('stop')}
        >
          Stop Containers
        </button>
        <button
          className="btn btn-success text-sm"
          disabled={busy}
          onClick={() => callAction('start')}
        >
          Start Containers
        </button>
        <button
          className="btn btn-primary text-sm"
          disabled={busy}
          onClick={() => callAction('restart')}
        >
          Restart Containers
        </button>
      </div>

      <div className="card">
        <p className="text-xs font-mono text-slate-500 mb-1">
          Command Output
        </p>
        <pre className="text-xs bg-slate-900 text-slate-50 rounded-lg p-3 max-h-80 overflow-auto">
{output || 'No commands executed yet.'}
        </pre>
      </div>
    </div>
  )
}
