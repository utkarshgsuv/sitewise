"use client";

import { useEffect, useState } from "react";
import { MOCK_TIMELINE } from "../lib/mock";

export default function RunTimeline() {
  const [visible, setVisible] = useState(3);
  useEffect(() => {
    if (visible >= MOCK_TIMELINE.length) return;
    const t = setTimeout(() => setVisible((v) => v + 1), 600);
    return () => clearTimeout(t);
  }, [visible]);
  return (
    <ol className="timeline">
      {MOCK_TIMELINE.slice(0, visible).map((e) => (
        <li key={e.seq} className={`ev-${e.type.split(".")[0]}`}>
          <span className="seq">#{e.seq}</span> <b>{e.type}</b> — {e.text}
        </li>
      ))}
    </ol>
  );
}
