// src/pages/ResetPasswordPage.jsx
import React, { useState } from "react";
import axios from "../api";
import { useParams, Link, useNavigate } from "react-router-dom";

export default function ResetPasswordPage() {
  const { token } = useParams();
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [info, setInfo] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleReset = async (e) => {
    e.preventDefault();
    setError("");
    setInfo("");

    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);

    try {
      await axios.post("/auth/reset-password", {
        token,
        new_password: password,
      });

      setInfo("Password updated successfully. You can now log in.");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      console.error(err);
      setError("Reset link is invalid or expired.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-md">
        <h2 className="text-2xl font-semibold text-center mb-2 text-slate-900">
          Choose a new password
        </h2>
        <p className="text-sm text-slate-500 mb-6 text-center">
          Enter a strong password and keep it safe.
        </p>

        {info && (
          <div className="mb-4 text-sm bg-emerald-50 text-emerald-700 px-3 py-2 rounded-md">
            {info}
          </div>
        )}

        {error && (
          <div className="mb-4 text-sm bg-red-50 text-red-700 px-3 py-2 rounded-md">
            {error}
          </div>
        )}

        <form onSubmit={handleReset} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              New Password
            </label>
            <input
              type="password"
              className="w-full p-3 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Confirm Password
            </label>
            <input
              type="password"
              className="w-full p-3 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-3 rounded-lg bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed transition"
          >
            {loading ? "Updating password..." : "Update password"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm">
          <Link to="/login" className="text-blue-600 hover:text-blue-700">
            Back to login
          </Link>
        </div>
      </div>
    </div>
  );
}
