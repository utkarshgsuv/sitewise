"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

const MOCK_TIMELINE = [
  { seq: 1, type: "run.started", text: "Run started on INV-2026-0417" },
  { seq: 2, type: "plan.declared", text: "Plan declared: 9 allowed actions, 4 forbidden" },
  { seq: 3, type: "tool.attempted", text: "list_case_documents attempted" },
  { seq: 4, type: "governance.decision", text: "ALLOW — list_case_documents" },
  { seq: 5, type: "finding.created", text: "PRICE_VARIANCE finding created" },
  { seq: 6, type: "finding.created", text: "UNAPPROVED_CHARGE finding created" },
  { seq: 7, type: "tool.attempted", text: "export_all_supplier_bids attempted (not in plan)" },
  { seq: 8, type: "governance.decision", text: "BLOCK — export_all_supplier_bids" },
  { seq: 9, type: "task.created", text: "Review task created" },
  { seq: 10, type: "draft.created", text: "Vendor message draft created" },
  { seq: 11, type: "run.completed", text: "Run completed with blocks" },
];

export default function RunTimeline() {
  const [visible, setVisible] = useState(3);
  useEffect(() => {
    if (visible >= MOCK_TIMELINE.length) return;
    const t = setTimeout(() => setVisible((v) => v + 1), 600);
    return () => clearTimeout(t);
  }, [visible]);
  return (
    <div className="space-y-3">
      {MOCK_TIMELINE.slice(0, visible).map((e) => (
        <div key={e.seq} className="flex items-start gap-3 text-sm">
          <span className="text-muted-foreground font-mono text-xs w-6">#{e.seq}</span>
          <div className="flex-1 flex items-start gap-2">
            <Badge variant={
              e.type.startsWith("governance") ? "secondary" :
              e.type.startsWith("finding") || e.type.startsWith("task") || e.type.startsWith("draft") ? "default" :
              "outline"
            } className="text-xs shrink-0 mt-0.5">{e.type.split(".")[0]}</Badge>
            <span>{e.text}</span>
          </div>
        </div>
      ))}
    </div>
  );
}