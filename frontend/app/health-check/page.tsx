/**
 * Strona Health Check - testuje połączenie z backendem
 * WCAG 2.1 Level AA Compliant
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
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Health Check</h1>
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
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Health Check</h1>
        <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6">
          <h2 className="text-xl font-bold text-red-900 mb-2">❌ Error</h2>
          <p className="text-red-800">{error}</p>
          <p className="text-sm text-gray-800 mt-4">
            Upewnij się że backend działa na http://localhost:8000
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Health Check</h1>

      {health && (
        <div className="bg-green-50 border-2 border-green-300 rounded-lg p-6">
          <h2 className="text-xl font-bold text-green-900 mb-2">
            ✅ {health.status === 'ok' ? 'API is Running' : 'Status: ' + health.status}
          </h2>
          <p className="text-gray-800 mb-4">{health.message}</p>

          <div className="space-y-2">
            {health.database && (
              <div className="flex items-center space-x-2">
                <span className="font-bold text-gray-900">Database:</span>
                <span className={health.database === 'connected' ? 'text-green-700 font-medium' : 'text-red-700 font-medium'}>
                  {health.database}
                </span>
              </div>
            )}
            {health.redis && (
              <div className="flex items-center space-x-2">
                <span className="font-bold text-gray-900">Redis:</span>
                <span className={health.redis === 'connected' ? 'text-green-700 font-medium' : 'text-red-700 font-medium'}>
                  {health.redis}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="mt-8 p-4 bg-gray-50 border-2 border-gray-300 rounded-lg">
        <h3 className="font-bold text-gray-900 mb-2">Raw JSON Response:</h3>
        <pre className="bg-gray-800 text-green-400 p-4 rounded overflow-x-auto text-sm">
          {JSON.stringify(health, null, 2)}
        </pre>
      </div>
    </div>
  )
}
