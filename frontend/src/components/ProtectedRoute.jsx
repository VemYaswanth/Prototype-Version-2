import React from "react";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  const mfaToken = localStorage.getItem("mfa_token");

  // ❌ If user is in MFA stage → must go to /mfa
  if (mfaToken && !token) {
    return <Navigate to="/mfa" replace />;
  }

  // ❌ If no final token → go to login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // ❌ Reject tokens that contain "mfa": true
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    if (payload.mfa === true) {
      // MFA-in-progress tokens should not access dashboard
      return <Navigate to="/mfa" replace />;
    }
  } catch (e) {
    // Invalid token → force logout
    localStorage.clear();
    return <Navigate to="/login" replace />;
  }

  // ✅ Full access — final verified token
  return children;
}
