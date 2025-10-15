import { useState } from "react";
import api from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    const { data } = await api.post("/auth/login", { email, password });
    localStorage.setItem("token", data.access_token);
    window.location.href = "/";
  };

  return (
    <form onSubmit={onSubmit} className="p-6 max-w-sm mx-auto">
      <input className="border p-2 w-full mb-2" placeholder="Email" value={email} onChange={(e)=>setEmail(e.target.value)} />
      <input className="border p-2 w-full mb-4" placeholder="Password" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
      <button className="border px-4 py-2" type="submit">Login</button>
    </form>
  );
}
