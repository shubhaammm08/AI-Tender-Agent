import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Tender Agent",
  description: "AI Tender Agent - Find, Check, and Bid for Tenders",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" />
      </head>
      <body>
        {children}
      </body>
    </html>
  );
}
