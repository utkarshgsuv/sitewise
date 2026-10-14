"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";

export default function SiteHeader() {
  const path = usePathname();
  const [name, setName] = useState("Guest");
  const [initial, setInitial] = useState("G");
  useEffect(() => {
    try {
      const raw = localStorage.getItem("sitewise-user");
      if (raw) {
        const u = JSON.parse(raw);
        const display = u.display_name ?? u.email ?? "Guest";
        setName(display);
        setInitial(display.trim().charAt(0).toUpperCase());
      }
    } catch {
      setName("Guest");
      setInitial("G");
    }
  }, [path]);

  return (
    <header className="flex h-16 items-center gap-4 border-b bg-background px-6">
      <Link href="/cases" className="flex items-center gap-2 font-bold text-xl tracking-tight">
        Sitewise
        <span className="text-primary">.</span>
      </Link>
      <nav className="flex-1 flex justify-center">
        <div className="flex items-center gap-1 rounded-full bg-secondary p-1">
          <Link href="/cases" className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            path.startsWith("/cases") ? "bg-background text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
          }`}>
            Cases
          </Link>
          <Link href="/login" className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            path.startsWith("/login") ? "bg-background text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
          }`}>
            Login
          </Link>
        </div>
      </nav>
      <div className="flex items-center gap-3">
        <Badge variant="secondary" className="text-xs font-medium">MOCK</Badge>
        <Separator orientation="vertical" className="h-6" />
        <div className="flex items-center gap-2 text-sm font-medium">
          <Avatar className="h-8 w-8">
            <AvatarImage src="" alt={name} />
            <AvatarFallback>{initial}</AvatarFallback>
          </Avatar>
          <span className="hidden sm:block">{name}</span>
        </div>
      </div>
    </header>
  );
}