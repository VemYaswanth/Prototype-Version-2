import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()

  const logout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <nav className="flex items-center justify-between px-6 py-3 bg-slate-900 text-white">
      <div className="flex items-center gap-2">
        <span className="font-semibold text-lg">AI Security Dashboard</span>
        <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/40">
          Live
        </span>
      </div>
      <button
        onClick={logout}
        className="text-sm px-3 py-1 rounded-lg border border-slate-500 hover:bg-slate-800"
      >
        Logout
      </button>
    </nav>
  )
}
