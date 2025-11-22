import React, { useEffect, useState } from "react";
import axios from "../api";
import { QRCodeSVG } from "qrcode.react";
import { useNavigate } from "react-router-dom";

export default function MfaSetupPage() {
  const [secret, setSecret] = useState("");
  const [qrUrl, setQrUrl] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const setup = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          setError("Please login first.");
          return;
        }

        const res = await axios.get("/auth/mfa/setup", {
          headers: {
            Authorization: "Bearer " + token,
          },
        });

        setSecret(res.data.secret);
        setQrUrl(res.data.otpauth_url);

      } catch (err) {
        setError("Unable to load MFA setup.");
      }
    };

    setup();
  }, []);

  return (
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <div className="bg-white shadow-xl rounded-xl p-10 w-96">

        <h2 className="text-3xl font-semibold text-center mb-6 text-blue-600">
          Set Up Google Authenticator
        </h2>

        {error && (
          <div className="text-red-600 text-center mb-4">{error}</div>
        )}

        {qrUrl ? (
          <>
            <p className="text-center mb-4 text-gray-700">
              Scan the QR code using Google Authenticator:
            </p>

            <div className="flex justify-center mb-6">
              <QRCodeSVG value={qrUrl} size={200} />
            </div>

            <p className="text-center text-gray-600 text-sm mb-4">
              Or enter this secret manually:
            </p>

            <div className="bg-gray-100 p-3 rounded text-center mb-6">
              <code className="text-sm">{secret}</code>
            </div>

            <button
              className="w-full bg-blue-600 text-white rounded p-3 font-semibold"
              onClick={() => navigate("/login")}
            >
              Continue to Login
            </button>
          </>
        ) : (
          <p className="text-gray-600 text-center">Loading...</p>
        )}
      </div>
    </div>
  );
}
