import "./globals.css";

export const metadata = { title: "Sitewise (outline)" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <aside className="side">
            <a className="logo" href="/cases">
              Sitewise<small>GOVERNED OPS · OUTLINE</small>
            </a>
            <a className="navlink" href="/cases">Cases</a>
            <a className="navlink" href="/login">Login</a>
            <div className="spacer" />
            <div className="mock">MOCK DATA — swaps to live API with P-01..P-03. Set NEXT_PUBLIC_USE_MOCK=false then.</div>
          </aside>
          <main className="main">
            <div className="wrap">{children}</div>
          </main>
        </div>
      </body>
    </html>
  );
}
