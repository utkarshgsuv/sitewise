import "./globals.css";

export const metadata = { title: "Sitewise (outline)" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav className="nav">
          <a href="/cases">Sitewise</a>
          <a href="/cases">Cases</a>
          <a href="/login">Login</a>
          <span className="mock">MOCK DATA — real API lands with P-01..P-03</span>
        </nav>
        <div className="wrap">{children}</div>
      </body>
    </html>
  );
}
