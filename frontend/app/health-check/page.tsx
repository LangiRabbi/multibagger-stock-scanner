/**
 * Strona Health Check - testuje połączenie z backendem
 */
'use client'

import { useEffect, useState } from 'react'

interface HealthResponse {
  status: string
  message: string
  database?: string
  redis?: string
}

export default function HealthCheckPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Wywołanie API backendu
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => {
        setHealth(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Health Check</h1>
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-32 bg-gray-200 rounded"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Health Check</h1>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-red-600 mb-2">❌ Error</h2>
          <p className="text-red-700">{error}</p>
          <p className="text-sm text-gray-600 mt-4">
            Upewnij się że backend działa na http://localhost:8000
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Health Check</h1>

      {health && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-green-600 mb-2">
            ✅ {health.status === 'ok' ? 'API is Running' : 'Status: ' + health.status}
          </h2>
          <p className="text-gray-700 mb-4">{health.message}</p>

          <div className="space-y-2">
            {health.database && (
              <div className="flex items-center space-x-2">
                <span className="font-semibold">Database:</span>
                <span className={health.database === 'connected' ? 'text-green-600' : 'text-red-600'}>
                  {health.database}
                </span>
              </div>
            )}
            {health.redis && (
              <div className="flex items-center space-x-2">
                <span className="font-semibold">Redis:</span>
                <span className={health.redis === 'connected' ? 'text-green-600' : 'text-red-600'}>
                  {health.redis}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold mb-2">Raw JSON Response:</h3>
        <pre className="bg-gray-800 text-green-400 p-4 rounded overflow-x-auto text-sm">
          {JSON.stringify(health, null, 2)}
        </pre>
      </div>
    </div>
  )
}
