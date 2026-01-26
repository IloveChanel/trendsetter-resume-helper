
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  typescript: { 
    ignoreBuildErrors: true 
  },

  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
  key: 'Content-Security-Policy',
  value: 
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-eval' 'unsafe-inline' https://vercel.live; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' blob: data:; " +
    // ADDED 'blob:' and 'data:' to connect-src below
    "connect-src 'self' blob: data: https://vercel.live https://*.onrender.com; " + 
    "frame-src https://vercel.live; " +
    // ADDED worker-src for libraries that process files in the background
    "worker-src 'self' blob:;"
}
        ],
      },
    ];
  },
};

export default nextConfig;