import type { Metadata } from "next";
import { Inter, Noto_Serif, Public_Sans } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const notoSerif = Noto_Serif({ subsets: ["latin"], variable: "--font-noto-serif" });
const publicSans = Public_Sans({ subsets: ["latin"], variable: "--font-public-sans" });

export const metadata: Metadata = {
  title: "LexGuard | AI Rights & Contract Intelligence System",
  description: "LexGuard is an AI-powered contract intelligence platform designed to analyze legal and quasi-legal documents before users agree to them.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${notoSerif.variable} ${publicSans.variable} font-body antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
