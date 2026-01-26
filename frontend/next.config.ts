
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
              "connect-src 'self' https://vercel.live https://*.onrender.com; " + 
              "frame-src https://vercel.live;"
          },
        ],
      },
    ];
  },
};

export default nextConfig;