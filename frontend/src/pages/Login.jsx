import React, { useState } from "react";
import axios from "../api";
import { useNavigate } from "react-router-dom";

export default function Login({ setAuth }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post("/auth/login", { email, password });

      if (!res.data.access_token) {
        alert("Invalid credentials");
        return;
      }

      // Save token
      localStorage.setItem("token", res.data.access_token);

      // Mark user as authenticated
      if (setAuth) setAuth(true);

      // Redirect to dashboard
      navigate("/");
    } catch (e) {
      console.error(e);
      alert("Invalid credentials");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <div className="bg-white shadow-xl rounded-xl p-10 w-96">
        <h2 className="text-3xl font-semibold text-center mb-6 text-blue-600">
          Security Dashboard Login
        </h2>

        <input
          type="email"
          className="w-full p-3 border rounded mb-3"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="w-full p-3 border rounded mb-3"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="w-full p-3 bg-blue-600 text-white rounded font-medium"
        >
          Login
        </button>
      </div>
    </div>
  );
}
