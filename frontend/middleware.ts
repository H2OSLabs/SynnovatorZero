import type { NextRequest } from "next/server"
import { NextResponse } from "next/server"

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === "/@vite/client") {
    return new NextResponse("export {}\n", {
      headers: {
        "content-type": "application/javascript; charset=utf-8",
        "cache-control": "no-store",
      },
    })
  }
  return NextResponse.next()
}

export const config = {
  matcher: ["/@vite/client"],
}
