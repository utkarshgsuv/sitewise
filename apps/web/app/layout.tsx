import "./globals.css";
import SiteHeader from "../components/SiteHeader";

export const metadata = { title: "Sitewise" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SiteHeader />
        <div className="wrap">{children}</div>
      </body>
    </html>
  );
}
