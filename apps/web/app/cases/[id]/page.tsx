"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge as UIBadge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
import { getCase } from "@/lib/api";
import type { Finding } from "@/lib/mock";
import RunTimeline from "@/components/RunTimeline";

const TABS = ["Overview", "Findings", "Evidence", "Actions", "Approvals", "Governance"] as const;

export default function CasePage({ params }: { params: { id: string } }) {
  const [data, setData] = useState<Awaited<ReturnType<typeof getCase>> | null>(null);
  const [err, setErr] = useState("");
  const [tab, setTab] = useState<(typeof TABS)[number]>("Overview");
  useEffect(() => {
    getCase(params.id).then(setData).catch((e) => setErr(e.message));
  }, [params.id]);
  if (err) return <p className="text-destructive">{err}</p>;
  if (!data) return <div className="flex h-64 items-center justify-center text-muted-foreground">Loading…</div>;
  const { case: c, findings, attempts, docs, task, draft } = data as { case: any; findings: Finding[]; attempts: any[]; docs: any[]; task: any; draft: any };
  const blocked = attempts.filter((a) => a.verdict === "BLOCK");
  const high = findings.filter((f) => f.severity === "high").length;
  const med = findings.filter((f) => f.severity === "medium").length;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-1">
        <Badge variant="secondary" className="w-fit text-xs">{c.status}</Badge>
        <h1 className="text-3xl font-bold tracking-tight">{c.invoice_number}</h1>
        <p className="text-muted-foreground">{c.vendor}</p>
      </div>

      <Tabs value={tab} onValueChange={setTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          {TABS.map((t) => (
            <TabsTrigger key={t} value={t}>{t}</TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value="Overview" className="space-y-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Invoice Total</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{c.total.replace("Rs.", "₹")}</div>
                <p className="text-xs text-muted-foreground">30 t · PO-7731</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Over Contract</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">₹2,40,000</div>
                <p className="text-xs text-muted-foreground">Variance + freight · +15.4%</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Findings</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{findings.length}</div>
                <div className="flex gap-2 mt-1">
                  <span className={`h-2 flex-1 rounded-full ${high ? "bg-destructive" : "bg-muted"}`} />
                  <span className={`h-2 flex-1 rounded-full ${med ? "bg-amber-500" : "bg-muted"}`} />
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Blocked Attempts</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{blocked.length}</div>
                <p className="text-xs text-muted-foreground">Boundary held</p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Review Task</CardTitle>
              <CardDescription>Created by the run</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="font-medium">{task.title}</p>
              <p className="text-sm text-muted-foreground">{task.assignee} · {task.status}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Vendor Draft</CardTitle>
              <CardDescription>Ready for approval</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="font-medium">{draft.subject}</p>
              <p className="text-sm text-muted-foreground">{draft.recipient} · digest {draft.digest} · {draft.status}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Run Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <RunTimeline />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="Findings" className="space-y-4">
          {findings.map((f: any) => (
            <Card key={f.id} className="overflow-hidden">
              <CardHeader className="flex flex-row items-start justify-between">
                <div className="flex flex-col gap-1">
                  <div className="flex items-center gap-2">
                    <CardTitle className="text-lg">{f.title}</CardTitle>
                    <UIBadge variant={f.severity === "high" ? "destructive" : f.severity === "medium" ? "secondary" : "outline"}>{f.severity}</UIBadge>
                    <UIBadge variant="outline" className="text-xs">confidence {f.confidence}</UIBadge>
                  </div>
                  <p className="text-sm text-muted-foreground">{f.type}</p>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex flex-wrap gap-2">
                  {Object.entries(f.detail as Record<string, string>).map(([k, v]) => (
                    <UIBadge key={k} variant="secondary" className="gap-1">
                      <span className="font-medium">{k}:</span> <span className="font-normal">{v}</span>
                    </UIBadge>
                  ))}
                </div>
                <Separator />
                <div className="space-y-2">
                  {f.evidence.map((e: any, i: number) => (
                    <div key={i} className="text-sm bg-muted/50 rounded-lg p-3 border">
                      <span className="font-medium text-primary">{e.label}:</span> <span className="ml-2">{e.quote}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="Evidence" className="space-y-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Attached Documents</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {docs.map((d: any) => (
                  <div key={d.id} className="flex items-center gap-4 p-3 rounded-lg border bg-card hover:bg-accent transition-colors">
                    <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary font-bold text-sm">PDF</div>
                    <div>
                      <p className="font-medium">{d.filename}</p>
                      <p className="text-xs text-muted-foreground">{d.kind}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="Actions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Review Task</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <p className="font-medium">{task.title}</p>
              <p className="text-sm text-muted-foreground">Assignee: {task.assignee} · {task.status}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Vendor Draft</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <p className="font-medium">{draft.subject}</p>
              <p className="text-sm text-muted-foreground">To: {draft.recipient} · digest {draft.digest} · {draft.status}</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="Approvals" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Approval Queue</CardTitle>
              <CardDescription>Approver queue with digest validity lands Thu (P-06)</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground text-sm">No approvals in the outline yet.</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="Governance" className="space-y-6">
          {blocked.length > 0 && (
            <Card className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-950 text-white border-slate-700">
              <CardHeader>
                <Badge variant="outline" className="text-xs text-blue-300 border-blue-500/50 bg-blue-500/10">Boundary Held</Badge>
                <CardTitle className="text-xl">Blocked: <code className="bg-slate-800 px-1.5 rounded">{blocked[0].tool}</code></CardTitle>
                <CardDescription className="text-slate-300">
                  Attempted outside declared plan · ArmorIQ BLOCK · trace <code className="bg-slate-800 px-1.5 rounded">{blocked[0].trace_ref ?? "—"}</code>
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-3 text-center">
                  <div><p className="text-3xl font-bold">0</p><p className="text-xs text-slate-400">Canary Events</p></div>
                  <div><p className="text-3xl font-bold">0</p><p className="text-xs text-slate-400">Forbidden Ledger Rows</p></div>
                  <div><p className="text-3xl font-bold text-green-400">✓</p><p className="text-xs text-slate-400">Bids Checksum Unchanged</p></div>
                </div>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Attempt Log</CardTitle>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[420px] w-full">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Tool</TableHead>
                      <TableHead className="w-[80px]">In Plan</TableHead>
                      <TableHead className="w-[100px]">Verdict</TableHead>
                      <TableHead className="w-[80px]">MCP</TableHead>
                      <TableHead className="w-[100px]">Status</TableHead>
                      <TableHead>Trace</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {attempts.map((a: any) => (
                      <TableRow key={a.attempt_id} className={a.verdict === "BLOCK" ? "bg-amber-50" : ""}>
                        <TableCell><code className="text-xs">{a.tool}</code></TableCell>
                        <TableCell className="text-center">{a.declared_in_plan ? "Yes" : "No"}</TableCell>
                        <TableCell>
                          <UIBadge variant={
                            a.verdict === "ALLOW" ? "default" :
                            a.verdict === "BLOCK" ? "destructive" :
                            a.verdict === "HOLD" ? "secondary" : "outline"
                          }>{a.verdict}</UIBadge>
                        </TableCell>
                        <TableCell>{a.mcp_decision ?? "—"}</TableCell>
                        <TableCell>{a.exec_status}</TableCell>
                        <TableCell><code className="text-xs">{a.trace_ref}</code></TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}