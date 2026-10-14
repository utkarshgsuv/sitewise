import { TooltipProvider } from "@/components/ui/tooltip";
import SiteHeader from "@/components/SiteHeader";
import "./globals.css";

export const metadata = { title: "Sitewise" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <TooltipProvider>
          <SiteHeader />
          <main className="mx-auto w-full max-w-6xl px-6 pb-16">{children}</main>
        </TooltipProvider>
      </body>
    </html>
  );
}
