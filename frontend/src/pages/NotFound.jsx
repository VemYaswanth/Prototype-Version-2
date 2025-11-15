import React from 'react'
import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-2">Page not found</h2>
      <p className="text-sm text-slate-500 mb-4">
        The page you are looking for does not exist.
      </p>
      <Link to="/" className="btn btn-primary text-sm">
        Back to Dashboard
      </Link>
    </div>
  )
}
