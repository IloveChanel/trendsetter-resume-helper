import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Explicitly allowing Render backend connections and eval for Next.js 16
  response.headers.set(
    'Content-Security-Policy',
    "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:; " +
    "script-src * 'unsafe-inline' 'unsafe-eval' data: blob:; " +
    "script-src-elem * 'unsafe-inline' 'unsafe-eval' data: blob:; " +
    "connect-src * data: blob:; " +
    "worker-src * data: blob:; " +
    "style-src * 'unsafe-inline';"
  );

  return response;
}

export const config = {
  matcher: '/((?!api|_next/static|_next/image|favicon.ico).*)',
};
