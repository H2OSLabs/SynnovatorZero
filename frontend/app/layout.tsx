import type { Metadata } from "next"
import { getServerEnv } from "@/lib/env"
import "./globals.css"
import { Providers } from "@/components/Providers"

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
    <html lang="zh-CN" className="dark" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `window.__ENV__=${JSON.stringify(env)}`,
          }}
        />
      </head>
      <body className="font-body antialiased" suppressHydrationWarning>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
