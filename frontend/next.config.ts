
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  typescript: { 
    ignoreBuildErrors: true 
  },

  // REMOVE the rewrites - they're causing issues
  // async rewrites() { ... } 

  // ULTRA-PERMISSIVE CSP - Allows EVERYTHING
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: "default-src * 'unsafe-inline' 'unsafe-eval' data: blob: filesystem:; script-src * 'unsafe-inline' 'unsafe-eval'; connect-src * 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src *; style-src * 'unsafe-inline';"
          },
          {
            key: 'X-Content-Security-Policy',
            value: "default-src * 'unsafe-inline' 'unsafe-eval' data: blob: filesystem:;"
          },
          {
            key: 'X-WebKit-CSP',
            value: "default-src * 'unsafe-inline' 'unsafe-eval' data: blob: filesystem:;"
          },
          {
            key: 'Access-Control-Allow-Origin',
            value: '*'
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET, POST, PUT, DELETE, OPTIONS'
          },
          {
            key: 'Access-Control-Allow-Headers',
            value: '*'
          }
        ],
      },
    ];
  },
};

export default nextConfig;