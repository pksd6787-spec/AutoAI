import "./globals.css";
import Link from "next/link";

const nav = ["dashboard","opportunities","research","scripts","scene-planner","media-library","voiceovers","videos","publishing","analytics","channel-brain","settings","billing","administration"];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body><aside className="sidebar"><h1>DocuForge Autonomous</h1>{nav.map(item => <Link key={item} href={`/${item}`}>{item.replaceAll("-", " ")}</Link>)}</aside><main>{children}</main></body></html>;
}
