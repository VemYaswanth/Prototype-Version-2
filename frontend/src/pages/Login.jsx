// src/pages/Login.jsx
import React, { useState } from "react";
import axios from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Login({ setAuth }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await axios.post("/auth/login", { email, password });

      // 🔐 MFA required — redirect to MFA page
      if (res.data.mfa_required) {
        localStorage.setItem("mfa_token", res.data.mfa_token);
        navigate("/mfa");
        return;
      }

      // 🔓 Normal login (no MFA required)
      if (res.data.access_token) {
        localStorage.setItem("token", res.data.access_token);
        if (setAuth) setAuth(true);
        navigate("/");
        return;
      }

      setError("Invalid credentials");
    } catch (err) {
      console.error(err);
      setError("Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-md">
        <h1 className="text-center text-xs font-semibold tracking-[0.25em] text-slate-500 mb-2">
          AI · BLOCKCHAIN · SECURITY
        </h1>
        <h2 className="text-2xl font-semibold text-center mb-6 text-slate-900">
          Admin Console Login
        </h2>

        {error && (
          <div className="mb-4 text-sm bg-red-50 text-red-700 px-3 py-2 rounded-md">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Email
            </label>
            <input
              type="email"
              className="w-full p-3 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="admin@ssems.net"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Password
            </label>
            <input
              type="password"
              className="w-full p-3 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>

          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400">
              Use your SSEMS admin credentials
            </span>
            <Link
              to="/forgot-password"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Forgot password?
            </Link>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-3 rounded-lg bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed transition"
          >
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
