
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
            // This is the "Master Key" - it allows everything
            value: "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:; " +
                   "script-src * 'unsafe-inline' 'unsafe-eval'; " +
                   "style-src * 'unsafe-inline'; " +
                   "img-src * data: blob:; " +
                   "connect-src * data: blob:; " +
                   "font-src * data:; " +
                   "frame-src *; " +
                   "worker-src * blob:; " +
                   "child-src * blob:;"
          },
        ],
      },
    ];
  },
};

export default nextConfig;