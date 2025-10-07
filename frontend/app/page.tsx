/**
 * Strona główna aplikacji
 */
export default function Home() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-4">
        Multibagger Stock Scanner 📈
      </h1>

      <p className="text-gray-600 mb-8">
        Automatyczne skanowanie akcji w poszukiwaniu okazji inwestycyjnych
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Feature 1 */}
        <div className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-2">🔍 Stock Scanner</h2>
          <p className="text-gray-600">
            Skanuj tysiące akcji według konfigurowalnych kryteriów (volume, RSI, moving averages)
          </p>
          <p className="text-sm text-gray-400 mt-4">Coming in Sprint 2</p>
        </div>

        {/* Feature 2 */}
        <div className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-2">💼 Portfolio</h2>
          <p className="text-gray-600">
            Zapisuj ciekawe akcje i śledź ich rozwój w czasie rzeczywistym
          </p>
          <p className="text-sm text-gray-400 mt-4">Coming in Sprint 2</p>
        </div>

        {/* Feature 3 */}
        <div className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-2">📊 Dashboard</h2>
          <p className="text-gray-600">
            Wykresy, analizy i wizualizacje danych rynkowych
          </p>
          <p className="text-sm text-gray-400 mt-4">Coming in Sprint 3</p>
        </div>

        {/* Feature 4 */}
        <div className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-2">🔔 Alerts</h2>
          <p className="text-gray-600">
            Powiadomienia email/Slack o nowych okazjach
          </p>
          <p className="text-sm text-gray-400 mt-4">Coming in Sprint 3</p>
        </div>
      </div>

      <div className="mt-12 p-6 bg-blue-50 rounded-lg">
        <h3 className="text-xl font-semibold mb-2">✅ Sprint 1 MVP</h3>
        <p className="text-gray-700 mb-4">
          Aktualnie dostępne:
        </p>
        <ul className="list-disc list-inside space-y-2 text-gray-600">
          <li>Backend FastAPI z PostgreSQL</li>
          <li>Frontend Next.js z Tailwind CSS</li>
          <li>Docker Compose setup</li>
          <li>Health check endpoint</li>
        </ul>
      </div>
    </div>
  )
}
