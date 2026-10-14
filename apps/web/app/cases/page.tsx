"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listCases } from "@/lib/api";
import type { CaseSummary } from "@/lib/mock";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";

export default function CasesPage() {
  const [cases, setCases] = useState<CaseSummary[] | null>(null);
  const [err, setErr] = useState("");
  useEffect(() => {
    listCases().then(setCases).catch((e) => setErr(e.message));
  }, []);
  if (err) return <p className="text-destructive">{err}</p>;
  if (!cases) return <div className="flex h-64 items-center justify-center text-muted-foreground">Loading…</div>;
  return (
    <div className="space-y-6">
      <div>
        <Badge variant="secondary" className="text-xs mb-2">All projects / Meridian Infra</Badge>
        <h1 className="text-3xl font-bold tracking-tight">Cases</h1>
        <p className="text-muted-foreground">{cases.length} open investigation{cases.length === 1 ? "" : "s"}</p>
      </div>
      <div className="space-y-3">
        {cases.map((c) => (
          <Card key={c.id} className="hover:shadow-md transition-shadow cursor-pointer">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <h3 className="text-lg font-semibold">{c.invoice_number}</h3>
                  <Badge variant="secondary">{c.status}</Badge>
                </div>
                <Link href={`/cases/${c.id}`}>
                  <Button variant="ghost" size="sm" className="gap-1">
                    Open
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
              <p className="mt-2 text-sm text-muted-foreground">{c.vendor} · {c.total}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}