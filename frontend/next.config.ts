
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
              "font-src 'self' data:; " +
              "connect-src 'self' blob: data: https://vercel.live https://*.onrender.com https://trendsetter-resume-helper.onrender.com; " + 
              "frame-src 'self' https://vercel.live; " +
              "worker-src 'self' blob:; " +
              "child-src 'self' blob:; " +
              "object-src 'none'; " +
              "base-uri 'self';"
          },
        ],
      },
    ];
  },
};

export default nextConfig;
