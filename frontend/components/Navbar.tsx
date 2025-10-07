/**
 * Navbar - pasek nawigacji aplikacji
 * WCAG 2.1 Level AA Compliant
 */
import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="bg-gray-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 hover:text-blue-300 transition-colors">
            <span className="text-2xl" aria-hidden="true">📈</span>
            <span className="font-bold text-xl">Multibagger Scanner</span>
          </Link>

          {/* Menu */}
          <div className="flex space-x-6">
            <Link
              href="/"
              className="font-medium hover:text-blue-300 transition-colors focus:outline-2 focus:outline-offset-2 focus:outline-blue-400"
            >
              Home
            </Link>
            <Link
              href="/health-check"
              className="font-medium hover:text-blue-300 transition-colors focus:outline-2 focus:outline-offset-2 focus:outline-blue-400"
            >
              Health Check
            </Link>
            <Link
              href="/scan"
              className="font-medium hover:text-blue-300 transition-colors focus:outline-2 focus:outline-offset-2 focus:outline-blue-400"
            >
              Scan
            </Link>
            <Link
              href="/portfolio"
              className="font-medium hover:text-blue-300 transition-colors focus:outline-2 focus:outline-offset-2 focus:outline-blue-400"
            >
              Portfolio
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
