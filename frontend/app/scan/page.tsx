/**
 * Strona Stock Scanner - skanowanie akcji
 * WCAG 2.1 Level AA Compliant
 */
'use client'

import { useState } from 'react'
import toast from 'react-hot-toast'
import { ErrorBoundary } from '@/components/ErrorBoundary'

interface ScanResult {
  symbol: string
  price: number
  volume: number
  price_change_7d: number | null
  price_change_30d: number | null
  meets_criteria: boolean
}

interface ScanResponse {
  total_scanned: number
  matches: number
  results: ScanResult[]
}

export default function ScanPage() {
  const [symbols, setSymbols] = useState('AAPL, MSFT, TSLA, GOOGL, AMZN')
  const [minVolume, setMinVolume] = useState('1000000')
  const [minPriceChange, setMinPriceChange] = useState('')
  const [loading, setLoading] = useState(false)
  const [scanProgress, setScanProgress] = useState<string>('')
  const [results, setResults] = useState<ScanResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setScanProgress('Przygotowywanie skanowania...')
    setError(null)
    setResults(null)

    try {
      const symbolList = symbols.split(',').map(s => s.trim().toUpperCase())

      setScanProgress('Łączenie z API...')
      const response = await fetch('http://localhost:8000/api/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbols: symbolList,
          min_volume: parseInt(minVolume),
          min_price_change_percent: minPriceChange ? parseFloat(minPriceChange) : null,
        }),
      })

      if (!response.ok) {
        throw new Error('Scan failed')
      }

      setScanProgress('Pobieranie wyników...')
      const data: ScanResponse = await response.json()

      setScanProgress('Gotowe!')
      setResults(data)

      // ✅ Toast sukcesu - informacja o liczbie znalezionych akcji
      const matchCount = data.matches || 0
      const totalScanned = data.total_scanned || 0

      toast.success(
        `✅ Skanowanie ukończone! Znaleziono ${matchCount} z ${totalScanned} akcji spełniających kryteria.`,
        { duration: 4000 }
      )

      // ⚠️ Ostrzeżenie jeśli niektóre symbole nie zostały znalezione
      const expectedCount = symbolList.length
      const actualCount = data.results?.length || 0

      if (actualCount < expectedCount) {
        const missingCount = expectedCount - actualCount
        toast.error(
          `⚠️ Nie znaleziono ${missingCount} symboli. Sprawdź czy są poprawne (np. AAPL, MSFT).`,
          { duration: 5000 }
        )
      }

    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message)

        // ❌ Toast błędu - wyraźna informacja o problemie
        toast.error(
          `❌ Błąd podczas skanowania: ${err.message}. Sprawdź czy backend działa na localhost:8000.`,
          { duration: 6000 }
        )
      } else {
        setError('An unknown error occurred')

        toast.error(
          '❌ Nieznany błąd podczas skanowania. Spróbuj ponownie lub sprawdź symbole akcji.',
          { duration: 5000 }
        )
      }
      setScanProgress('Błąd podczas skanowania')
    } finally {
      setLoading(false)
      // Reset progress po 1 sekundzie
      setTimeout(() => setScanProgress(''), 1000)
    }
  }

  return (
    <ErrorBoundary>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Stock Scanner</h1>

      {/* Formularz skanowania */}
      <form onSubmit={handleScan} className="bg-white p-6 rounded-lg shadow-md border-2 border-gray-300 mb-6">
        <div className="mb-4">
          <label htmlFor="symbols" className="block text-sm font-bold mb-2 text-gray-900">
            Stock Symbols (oddziel przecinkiem)
          </label>
          <input
            id="symbols"
            type="text"
            value={symbols}
            onChange={(e) => setSymbols(e.target.value)}
            className="w-full border-2 border-gray-400 bg-white text-gray-900 placeholder-gray-500 rounded px-3 py-2 focus:border-blue-500 focus:outline-none"
            placeholder="AAPL, MSFT, TSLA"
            required
          />
          <p className="text-xs text-gray-700 mt-1">
            Np. AAPL, MSFT, TSLA, GOOGL, AMZN
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label htmlFor="minVolume" className="block text-sm font-bold mb-2 text-gray-900">
              Min Volume
            </label>
            <input
              id="minVolume"
              type="number"
              value={minVolume}
              onChange={(e) => setMinVolume(e.target.value)}
              className="w-full border-2 border-gray-400 bg-white text-gray-900 placeholder-gray-500 rounded px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="1000000"
            />
          </div>

          <div>
            <label htmlFor="minPriceChange" className="block text-sm font-bold mb-2 text-gray-900">
              Min Price Change % (7 dni) - opcjonalne
            </label>
            <input
              id="minPriceChange"
              type="number"
              step="0.1"
              value={minPriceChange}
              onChange={(e) => setMinPriceChange(e.target.value)}
              className="w-full border-2 border-gray-400 bg-white text-gray-900 placeholder-gray-500 rounded px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="Np. 2.0 dla +2%"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 px-4 rounded-lg font-bold text-base transition-all duration-200 ${
            loading
              ? 'bg-gray-400 cursor-not-allowed text-gray-700'
              : 'bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg'
          }`}
        >
          {loading ? 'Skanowanie w toku...' : 'Scan Stocks'}
        </button>
      </form>

      {/* Loading Indicator - Progress feedback dla użytkownika */}
      {loading && (
        <div className="mb-6 bg-blue-50 border-2 border-blue-300 rounded-lg p-5 shadow-md">
          <div className="flex items-center gap-4">
            {/* Animated Spinner - wskaźnik aktywności */}
            <svg
              className="animate-spin h-6 w-6 text-blue-600"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-label="Ładowanie"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>

            {/* Progress Text - informacja o stanie */}
            <div className="flex-1">
              <p className="text-base font-bold text-blue-900">{scanProgress}</p>
              <p className="text-sm text-blue-700 mt-1">
                ⏳ Pierwsze skanowanie może potrwać 5-10 sekund (yfinance + Finnhub API)
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border-2 border-red-300 rounded-lg p-4 mb-6">
          <p className="text-red-800 font-medium">Error: {error}</p>
          <p className="text-sm text-gray-800 mt-2">
            Upewnij sie ze backend dziala na http://localhost:8000
          </p>
        </div>
      )}

      {/* Wyniki */}
      {results && (
        <div className="bg-white p-6 rounded-lg shadow-md border-2 border-gray-300">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">
            Scan Results: <span className="text-green-700">{results.matches}</span> / {results.total_scanned} akcji spelnia kryteria
          </h2>

          {results.results.length === 0 ? (
            <p className="text-gray-800">Brak wynikow</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-100 border-b-2 border-gray-300">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Symbol</th>
                    <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Price</th>
                    <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Volume</th>
                    <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Change 7d</th>
                    <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Change 30d</th>
                    <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {results.results.map((result, idx) => (
                    <tr
                      key={idx}
                      className={result.meets_criteria ? 'bg-green-50 border-b-2 border-green-200' : 'bg-white border-b border-gray-200'}
                    >
                      <td className="px-4 py-3 font-bold text-gray-900 text-base">{result.symbol}</td>
                      <td className="px-4 py-3 text-gray-800 font-medium">${result.price}</td>
                      <td className="px-4 py-3 text-gray-800">{result.volume.toLocaleString()}</td>
                      <td className={`px-4 py-3 font-bold ${result.price_change_7d && result.price_change_7d > 0 ? 'text-green-700' : 'text-red-700'}`}>
                        {result.price_change_7d ? `${result.price_change_7d > 0 ? '+' : ''}${result.price_change_7d}%` : 'N/A'}
                      </td>
                      <td className={`px-4 py-3 font-bold ${result.price_change_30d && result.price_change_30d > 0 ? 'text-green-700' : 'text-red-700'}`}>
                        {result.price_change_30d ? `${result.price_change_30d > 0 ? '+' : ''}${result.price_change_30d}%` : 'N/A'}
                      </td>
                      <td className="px-4 py-3">
                        {result.meets_criteria ? (
                          <span className="text-green-700 font-bold text-base">✓ Match</span>
                        ) : (
                          <span className="text-gray-700 font-medium">—</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
      </div>
    </ErrorBoundary>
  )
}
