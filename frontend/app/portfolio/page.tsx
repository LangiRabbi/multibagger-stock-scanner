/**
 * Strona Portfolio - zarzadzanie portfolio
 * WCAG 2.1 Level AA Compliant
 */
'use client'

import { useState, useEffect } from 'react'
import { ErrorBoundary } from '@/components/ErrorBoundary'

interface PortfolioItem {
  id: number
  user_id: number
  symbol: string
  entry_price: number
  quantity: number
  notes: string | null
  added_at: string
}

export default function PortfolioPage() {
  const [items, setItems] = useState<PortfolioItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Form state (dodawanie nowej pozycji)
  const [showAddForm, setShowAddForm] = useState(false)
  const [newSymbol, setNewSymbol] = useState('')
  const [newPrice, setNewPrice] = useState('')
  const [newQuantity, setNewQuantity] = useState('')
  const [newNotes, setNewNotes] = useState('')

  // Fetch portfolio
  const fetchPortfolio = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/portfolio')
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to fetch portfolio`)
      }
      const data = await response.json()
      setItems(data)
      setError(null) // Clear any previous errors
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('Unknown error occurred')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPortfolio()
  }, [])

  // Add new item
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const response = await fetch('http://localhost:8000/api/portfolio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: newSymbol.toUpperCase(),
          entry_price: parseFloat(newPrice),
          quantity: parseFloat(newQuantity),
          notes: newNotes || null,
        }),
      })

      if (!response.ok) throw new Error('Failed to add item')

      // Reset form
      setNewSymbol('')
      setNewPrice('')
      setNewQuantity('')
      setNewNotes('')
      setShowAddForm(false)

      // Refresh list
      fetchPortfolio()
    } catch (err: unknown) {
      if (err instanceof Error) {
        alert('Error: ' + err.message)
      }
    }
  }

  // Delete item
  const handleDelete = async (id: number) => {
    if (!confirm('Na pewno usunac ta pozycje?')) return

    try {
      const response = await fetch(`http://localhost:8000/api/portfolio/${id}`, {
        method: 'DELETE',
      })

      if (!response.ok) throw new Error('Failed to delete item')

      // Refresh list
      fetchPortfolio()
    } catch (err: unknown) {
      if (err instanceof Error) {
        alert('Error: ' + err.message)
      }
    }
  }

  if (loading) {
    return (
      <ErrorBoundary>
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Portfolio</h1>
          <div className="animate-pulse">
            <div className="h-32 bg-gray-200 rounded"></div>
          </div>
        </div>
      </ErrorBoundary>
    )
  }

  if (error) {
    return (
      <ErrorBoundary>
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Portfolio</h1>
          <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6">
            <p className="text-red-800 font-medium">Error: {error}</p>
            <p className="text-sm text-gray-800 mt-2">
              Upewnij się że backend działa na http://localhost:8000
            </p>
          </div>
        </div>
      </ErrorBoundary>
    )
  }

  return (
    <ErrorBoundary>
      <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">My Portfolio</h1>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="bg-blue-600 text-white font-semibold px-4 py-2 rounded hover:bg-blue-700"
        >
          {showAddForm ? 'Cancel' : '+ Add Stock'}
        </button>
      </div>

      {/* Add form */}
      {showAddForm && (
        <form onSubmit={handleAdd} className="bg-white p-6 rounded-lg shadow-md mb-6 border-2 border-gray-300">
          <h2 className="text-xl font-bold mb-4 text-gray-900">Add New Stock</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label htmlFor="newSymbol" className="block text-sm font-bold mb-2 text-gray-900">Symbol</label>
              <input
                id="newSymbol"
                type="text"
                value={newSymbol}
                onChange={(e) => setNewSymbol(e.target.value)}
                className="w-full border-2 border-gray-400 rounded px-3 py-2 bg-white text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                placeholder="AAPL"
                required
              />
            </div>

            <div>
              <label htmlFor="newPrice" className="block text-sm font-bold mb-2 text-gray-900">Entry Price</label>
              <input
                id="newPrice"
                type="number"
                step="0.01"
                value={newPrice}
                onChange={(e) => setNewPrice(e.target.value)}
                className="w-full border-2 border-gray-400 rounded px-3 py-2 bg-white text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                placeholder="150.00"
                required
              />
            </div>

            <div>
              <label htmlFor="newQuantity" className="block text-sm font-bold mb-2 text-gray-900">Quantity</label>
              <input
                id="newQuantity"
                type="number"
                step="0.01"
                value={newQuantity}
                onChange={(e) => setNewQuantity(e.target.value)}
                className="w-full border-2 border-gray-400 rounded px-3 py-2 bg-white text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                placeholder="10"
                required
              />
            </div>

            <div>
              <label htmlFor="newNotes" className="block text-sm font-bold mb-2 text-gray-900">Notes (optional)</label>
              <input
                id="newNotes"
                type="text"
                value={newNotes}
                onChange={(e) => setNewNotes(e.target.value)}
                className="w-full border-2 border-gray-400 rounded px-3 py-2 bg-white text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                placeholder="Long term hold"
              />
            </div>
          </div>

          <button
            type="submit"
            className="bg-green-600 text-white font-semibold px-6 py-2 rounded hover:bg-green-700"
          >
            Add to Portfolio
          </button>
        </form>
      )}

      {/* Portfolio list */}
      <div className="bg-white p-6 rounded-lg shadow-md border-2 border-gray-300">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          Your Stocks (<span className="text-blue-700">{items.length}</span>)
        </h2>

        {items.length === 0 ? (
          <p className="text-gray-800 font-medium">Brak akcji w portfolio. Dodaj pierwsza!</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-100 border-b-2 border-gray-300">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Symbol</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Entry Price</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Quantity</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Notes</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Added</th>
                  <th className="px-4 py-3 text-left text-sm font-bold text-gray-900">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className="border-b border-gray-200 hover:bg-gray-50">
                    <td className="px-4 py-3 font-bold text-gray-900 text-base">{item.symbol}</td>
                    <td className="px-4 py-3 text-gray-800 font-medium">${item.entry_price}</td>
                    <td className="px-4 py-3 text-gray-800">{item.quantity}</td>
                    <td className="px-4 py-3 text-gray-800">{item.notes || '—'}</td>
                    <td className="px-4 py-3 text-gray-700 text-sm">
                      {new Date(item.added_at).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="text-red-700 hover:text-red-900 font-bold"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      </div>
    </ErrorBoundary>
  )
}
