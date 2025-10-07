/**
 * Strona Stock Scanner - skanowanie akcji
 */
'use client'

import { useState } from 'react'

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
  const [results, setResults] = useState<ScanResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const symbolList = symbols.split(',').map(s => s.trim().toUpperCase())

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

      const data: ScanResponse = await response.json()
      setResults(data)
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('An unknown error occurred')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Stock Scanner</h1>

      {/* Formularz skanowania */}
      <form onSubmit={handleScan} className="bg-white p-6 rounded-lg shadow-md mb-6">
        <div className="mb-4">
          <label className="block text-sm font-semibold mb-2">
            Stock Symbols (oddziel przecinkiem)
          </label>
          <input
            type="text"
            value={symbols}
            onChange={(e) => setSymbols(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2"
            placeholder="AAPL, MSFT, TSLA"
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            Np. AAPL, MSFT, TSLA, GOOGL, AMZN
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-semibold mb-2">
              Min Volume
            </label>
            <input
              type="number"
              value={minVolume}
              onChange={(e) => setMinVolume(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="1000000"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2">
              Min Price Change % (7 dni) - opcjonalne
            </label>
            <input
              type="number"
              step="0.1"
              value={minPriceChange}
              onChange={(e) => setMinPriceChange(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="Np. 2.0 dla +2%"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Scanning...' : 'Scan Stocks'}
        </button>
      </form>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-700">Error: {error}</p>
          <p className="text-sm text-gray-600 mt-2">
            Upewnij sie ze backend dziala na http://localhost:8000
          </p>
        </div>
      )}

      {/* Wyniki */}
      {results && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">
            Scan Results: {results.matches} / {results.total_scanned} akcji spelnia kryteria
          </h2>

          {results.results.length === 0 ? (
            <p className="text-gray-500">Brak wynikow</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Symbol</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Price</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Volume</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Change 7d</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Change 30d</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {results.results.map((result, idx) => (
                    <tr
                      key={idx}
                      className={result.meets_criteria ? 'bg-green-50' : 'bg-gray-50'}
                    >
                      <td className="px-4 py-2 font-semibold">{result.symbol}</td>
                      <td className="px-4 py-2">${result.price}</td>
                      <td className="px-4 py-2">{result.volume.toLocaleString()}</td>
                      <td className={`px-4 py-2 ${result.price_change_7d && result.price_change_7d > 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {result.price_change_7d ? `${result.price_change_7d > 0 ? '+' : ''}${result.price_change_7d}%` : 'N/A'}
                      </td>
                      <td className={`px-4 py-2 ${result.price_change_30d && result.price_change_30d > 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {result.price_change_30d ? `${result.price_change_30d > 0 ? '+' : ''}${result.price_change_30d}%` : 'N/A'}
                      </td>
                      <td className="px-4 py-2">
                        {result.meets_criteria ? (
                          <span className="text-green-600 font-semibold">✓ Match</span>
                        ) : (
                          <span className="text-gray-400">—</span>
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
  )
}
