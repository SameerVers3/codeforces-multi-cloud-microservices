import './globals.css'
import Navigation from '@/components/Navigation'

export const metadata = {
  title: 'Codeforces Platform',
  description: 'Multi-cloud competitive programming platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Navigation />
        {children}
      </body>
    </html>
  )
}

