/**
 * Strona główna aplikacji
 * WCAG 2.1 Level AA Compliant
 */
export default function Home() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Multibagger Stock Scanner 📈
      </h1>

      <p className="text-gray-800 mb-8">
        Automatyczne skanowanie akcji w poszukiwaniu okazji inwestycyjnych
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Feature 1 */}
        <div className="border-2 border-gray-300 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">🔍 Stock Scanner</h2>
          <p className="text-gray-800">
            Skanuj tysiące akcji według konfigurowalnych kryteriów (volume, RSI, moving averages)
          </p>
          <p className="text-sm text-gray-700 mt-4 font-medium">Coming in Sprint 2</p>
        </div>

        {/* Feature 2 */}
        <div className="border-2 border-gray-300 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">💼 Portfolio</h2>
          <p className="text-gray-800">
            Zapisuj ciekawe akcje i śledź ich rozwój w czasie rzeczywistym
          </p>
          <p className="text-sm text-gray-700 mt-4 font-medium">Coming in Sprint 2</p>
        </div>

        {/* Feature 3 */}
        <div className="border-2 border-gray-300 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">📊 Dashboard</h2>
          <p className="text-gray-800">
            Wykresy, analizy i wizualizacje danych rynkowych
          </p>
          <p className="text-sm text-gray-700 mt-4 font-medium">Coming in Sprint 3</p>
        </div>

        {/* Feature 4 */}
        <div className="border-2 border-gray-300 rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">🔔 Alerts</h2>
          <p className="text-gray-800">
            Powiadomienia email/Slack o nowych okazjach
          </p>
          <p className="text-sm text-gray-700 mt-4 font-medium">Coming in Sprint 3</p>
        </div>
      </div>

      <div className="mt-12 p-6 bg-blue-50 border-2 border-blue-200 rounded-lg">
        <h3 className="text-xl font-bold text-gray-900 mb-2">✅ Sprint 1 MVP</h3>
        <p className="text-gray-800 mb-4">
          Aktualnie dostępne:
        </p>
        <ul className="list-disc list-inside space-y-2 text-gray-800">
          <li>Backend FastAPI z PostgreSQL</li>
          <li>Frontend Next.js z Tailwind CSS</li>
          <li>Docker Compose setup</li>
          <li>Health check endpoint</li>
        </ul>
      </div>
    </div>
  )
}
