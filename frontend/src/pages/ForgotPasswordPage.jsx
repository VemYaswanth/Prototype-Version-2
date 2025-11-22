// src/pages/ForgotPasswordPage.jsx
import React, { useState } from "react";
import axios from "../api";
import { Link } from "react-router-dom";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [info, setInfo] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setInfo("");
    setLoading(true);

    try {
      await axios.post("/auth/forgot-password", { email });
      setInfo("If the email exists, a reset link has been sent.");
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-md">
        <h2 className="text-2xl font-semibold text-center mb-2 text-slate-900">
          Reset your password
        </h2>
        <p className="text-sm text-slate-500 mb-6 text-center">
          Enter the email associated with your account and we’ll send a reset
          link.
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

        <form onSubmit={handleSubmit} className="space-y-4">
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
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-3 rounded-lg bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed transition"
          >
            {loading ? "Sending link..." : "Send reset link"}
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
