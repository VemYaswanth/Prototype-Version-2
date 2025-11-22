import React, { useState } from "react";
import axios from "../api";
import { useNavigate } from "react-router-dom";

export default function MfaPage() {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleVerify = async () => {
    setError("");

    const mfaToken = localStorage.getItem("mfa_token");
    if (!mfaToken) {
      setError("MFA session expired. Please login again.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post(
        "/auth/mfa/verify",
        { code },
        {
          headers: {
            Authorization: "Bearer " + mfaToken,
          },
        }
      );

      // ✅ On success: save final access token
      localStorage.setItem("token", res.data.access_token);
      localStorage.removeItem("mfa_token");

      navigate("/");
    } catch (err) {
      console.error(err);
      setError("Invalid or expired code.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <div className="bg-white shadow-xl rounded-xl p-10 w-96">
        <h2 className="text-3xl font-semibold text-center mb-6 text-blue-600">
          Enter 6-digit Code
        </h2>

        {error && (
          <div className="text-red-600 text-center mb-4 text-sm">{error}</div>
        )}

        <input
          type="text"
          maxLength={6}
          className="w-full p-3 border rounded mb-4 text-center tracking-[0.4em] text-xl"
          placeholder="123456"
          value={code}
          onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
        />

        <button
          onClick={handleVerify}
          disabled={loading || code.length !== 6}
          className="w-full p-3 bg-blue-600 text-white rounded font-medium disabled:opacity-60"
        >
          {loading ? "Verifying..." : "Verify Code"}
        </button>

        <button
          className="mt-3 w-full text-sm text-blue-600 underline"
          onClick={() => navigate("/login")}
        >
          Back to login
        </button>
      </div>
    </div>
  );
}
