import type { Metadata } from "next"
import { getServerEnv } from "@/lib/env"
import "./globals.css"

export const metadata: Metadata = {
  title: "协创者 - Synnovator",
  description: "Creative collaboration platform",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Read environment variables on the server and inject into client
  const env = getServerEnv()

  return (
    <html lang="zh-CN" className="dark">
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `window.__ENV__=${JSON.stringify(env)}`,
          }}
        />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&family=Poppins:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="font-body antialiased">
        {children}
      </body>
    </html>
  )
}
