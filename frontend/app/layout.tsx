import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Trendsetter Resume Helper - Beat ATS Bots',
  description: 'ATS-optimized resume analysis and optimization platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="light">
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
