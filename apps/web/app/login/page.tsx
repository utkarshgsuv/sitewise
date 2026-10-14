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
    <div className="card" style={{ maxWidth: 420 }}>
      <h2>Login (mock)</h2>
      <p style={{ fontSize: 14 }}>Seeded emails end in <code>.example.test</code>; password is <code>Sitewise-Demo-1234</code>.</p>
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
  );
}
