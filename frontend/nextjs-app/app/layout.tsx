import './globals.css'

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
      <body>{children}</body>
    </html>
  )
}

