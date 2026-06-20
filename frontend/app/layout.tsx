import "./globals.css";
import Link from "next/link";
import { navigation } from "../lib/navigation";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body><aside className="sidebar"><h1>DocuForge Autonomous</h1>{navigation.map(item => <Link key={item.href} href={item.href}><strong>{item.label}</strong><span>{item.description}</span></Link>)}</aside><main>{children}</main></body></html>;
}
