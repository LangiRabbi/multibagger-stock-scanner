/**
 * Navbar - pasek nawigacji aplikacji
 */
import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="bg-gray-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl">📈</span>
            <span className="font-bold text-xl">Multibagger Scanner</span>
          </Link>

          {/* Menu */}
          <div className="flex space-x-6">
            <Link
              href="/"
              className="hover:text-blue-400 transition-colors"
            >
              Home
            </Link>
            <Link
              href="/health-check"
              className="hover:text-blue-400 transition-colors"
            >
              Health Check
            </Link>
            <Link
              href="/scan"
              className="hover:text-blue-400 transition-colors"
            >
              Scan
            </Link>
            <Link
              href="/portfolio"
              className="hover:text-blue-400 transition-colors"
            >
              Portfolio
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
