import React from 'react'
import { NavLink } from 'react-router-dom'

const base =
  'flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors'
const activeClasses = 'bg-blue-600 text-white'
const inactiveClasses = 'text-slate-600 hover:bg-slate-200'

export default function Sidebar() {
  return (
    <aside className="w-60 bg-white border-r border-slate-200 h-[calc(100vh-52px)] p-4 space-y-2">
      <NavLink
        to="/"
        end
        className={({ isActive }) => `${base} ${isActive ? activeClasses : inactiveClasses}`}
      >
        Dashboard
      </NavLink>
      <NavLink
        to="/alerts"
        className={({ isActive }) => `${base} ${isActive ? activeClasses : inactiveClasses}`}
      >
        Suspicious Queries
      </NavLink>
      <NavLink
        to="/logs"
        className={({ isActive }) => `${base} ${isActive ? activeClasses : inactiveClasses}`}
      >
        Query Logs
      </NavLink>
      <NavLink
        to="/system"
        className={({ isActive }) => `${base} ${isActive ? activeClasses : inactiveClasses}`}
      >
        System Control
      </NavLink>
    </aside>
  )
}
