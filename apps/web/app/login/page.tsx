"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "../../lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("asha@meridian.example.test");
  const [password, setPassword] = useState("Sitewise-Demo-1234");
  const [err, setErr] = useState("");
  const router = useRouter();
  return (
    <div className="login-page">
    <div className="card login-card">
      <h2>Welcome back</h2>
      <p className="hint">Seeded emails end in <code>.example.test</code> · password <code>Sitewise-Demo-1234</code></p>
      <div style={{ display: "grid", gap: 10 }}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
        <button
          className="login-btn"
          onClick={() => login(email, password).then(() => router.push("/cases")).catch((e) => setErr(e.message))}
        >
          Login
        </button>
        {err && <p className="error">{err}</p>}
      </div>
    </div>
    </div>
  );
}
