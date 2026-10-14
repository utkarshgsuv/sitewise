"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function SiteHeader() {
  const path = usePathname();
  const [name, setName] = useState("Guest");
  useEffect(() => {
    try {
      const raw = localStorage.getItem("sitewise-user");
      if (raw) {
        const u = JSON.parse(raw);
        setName((u.display_name ?? u.email ?? "Guest").split(" ")[0]);
      }
    } catch {
      setName("Guest");
    }
  }, [path]);
  const tab = path.startsWith("/login") ? "Login" : "Cases";
  return (
    <header className="topbar">
      <a className="brand" href="/cases">Sitewise<span>.</span></a>
      <nav className="pillnav">
        <a href="/cases" className={tab === "Cases" ? "active" : ""}>Cases</a>
        <a href="/login" className={tab === "Login" ? "active" : ""}>Login</a>
      </nav>
      <span className="mockdot">MOCK</span>
      <span className="userchip">
        <span className="avatar">{name.charAt(0).toUpperCase()}</span>
        {name}
      </span>
    </header>
  );
}
