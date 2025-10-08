/**
 * ErrorBoundary - Komponent do obsługi błędów React
 *
 * ErrorBoundary łapie błędy JavaScript w dowolnym miejscu drzewa komponentów,
 * loguje te błędy i wyświetla zastępczy UI zamiast crashowania całej aplikacji.
 *
 * Użycie:
 * <ErrorBoundary>
 *   <TwojKomponent />
 * </ErrorBoundary>
 *
 * WCAG 2.1 Level AA Compliant
 * - Wysokie kontrasty kolorów (4.5:1 dla tekstu)
 * - Semantyczny HTML
 * - Czytelne komunikaty błędów
 */
'use client' // ErrorBoundary MUSI być Client Component

import React, { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode // Opcjonalny custom fallback UI
}

interface State {
  hasError: boolean
  error?: Error
  errorInfo?: React.ErrorInfo
}

/**
 * ErrorBoundary - łapie błędy React i pokazuje fallback UI
 *
 * Kiedy używać:
 * - Owijaj strony które mogą crashować (np. /scan, /portfolio)
 * - Owijaj komponenty które fetchują dane z API
 * - Owijaj komponenty które renderują dane użytkownika
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    // State początkowy - brak błędu
    this.state = { hasError: false }
  }

  /**
   * getDerivedStateFromError - wywoływany gdy component child rzuci błąd
   * Zwraca nowy state aby następny render pokazał fallback UI
   */
  static getDerivedStateFromError(error: Error): State {
    // Update state żeby następny render pokazał fallback UI
    return { hasError: true, error }
  }

  /**
   * componentDidCatch - wywoływany po złapaniu błędu
   * Możesz tu zalogować błąd do serwisu monitorującego jak Sentry
   */
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Loguj błąd do konsoli (w produkcji możesz wysłać do Sentry/LogRocket)
    console.error('❌ ErrorBoundary złapał błąd:', error)
    console.error('📍 Component stack:', errorInfo.componentStack)

    // Zapisz errorInfo do state (opcjonalnie, dla debugowania)
    this.setState({ errorInfo })
  }

  /**
   * handleReset - resetuje stan błędu i próbuje ponownie wyrenderować
   */
  handleReset = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined })
  }

  render() {
    // Jeśli wystąpił błąd, pokaż fallback UI
    if (this.state.hasError) {
      // Custom fallback przekazany przez props
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Domyślny fallback UI
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full bg-white rounded-lg shadow-xl border-2 border-red-300 p-8">
            <div className="text-center">
              {/* Ikona błędu - duża i wyraźna */}
              <div className="text-7xl mb-4" role="img" aria-label="Błąd">
                ⚠️
              </div>

              {/* Tytuł błędu */}
              <h1 className="text-3xl font-bold text-gray-900 mb-3">
                Coś poszło nie tak
              </h1>

              {/* Opis błędu dla użytkownika */}
              <p className="text-base text-gray-700 mb-6">
                Wystąpił nieoczekiwany błąd w aplikacji. Spróbuj odświeżyć stronę lub wrócić do strony głównej.
              </p>

              {/* Przyciski akcji */}
              <div className="flex gap-4 justify-center mb-6">
                <button
                  onClick={() => window.location.reload()}
                  className="bg-blue-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-blue-700 transition shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  🔄 Odśwież stronę
                </button>

                <button
                  onClick={() => window.location.href = '/'}
                  className="bg-gray-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-gray-700 transition shadow-md focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                >
                  🏠 Strona główna
                </button>
              </div>

              {/* Szczegóły błędu - tylko w dev mode */}
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <details className="mt-6 text-left bg-gray-100 rounded-lg p-4 border-2 border-gray-300">
                  <summary className="cursor-pointer text-base font-bold text-gray-800 hover:text-gray-900 mb-2">
                    🔍 Szczegóły błędu (tylko dev mode)
                  </summary>

                  {/* Nazwa błędu */}
                  <div className="mb-3">
                    <p className="text-sm font-bold text-gray-700 mb-1">Typ błędu:</p>
                    <p className="text-sm text-red-700 font-mono bg-red-50 p-2 rounded border border-red-200">
                      {this.state.error.name}
                    </p>
                  </div>

                  {/* Komunikat błędu */}
                  <div className="mb-3">
                    <p className="text-sm font-bold text-gray-700 mb-1">Komunikat:</p>
                    <p className="text-sm text-red-700 font-mono bg-red-50 p-2 rounded border border-red-200">
                      {this.state.error.message}
                    </p>
                  </div>

                  {/* Stack trace */}
                  {this.state.error.stack && (
                    <div className="mb-3">
                      <p className="text-sm font-bold text-gray-700 mb-1">Stack trace:</p>
                      <pre className="text-xs text-gray-800 bg-gray-50 p-3 rounded border border-gray-300 overflow-auto max-h-64">
                        {this.state.error.stack}
                      </pre>
                    </div>
                  )}

                  {/* Component stack */}
                  {this.state.errorInfo?.componentStack && (
                    <div>
                      <p className="text-sm font-bold text-gray-700 mb-1">Component stack:</p>
                      <pre className="text-xs text-gray-800 bg-gray-50 p-3 rounded border border-gray-300 overflow-auto max-h-64">
                        {this.state.errorInfo.componentStack}
                      </pre>
                    </div>
                  )}
                </details>
              )}

              {/* Pomocne wskazówki dla użytkownika */}
              <div className="mt-6 pt-6 border-t-2 border-gray-200">
                <p className="text-sm font-bold text-gray-700 mb-2">💡 Możliwe rozwiązania:</p>
                <ul className="text-sm text-gray-600 text-left space-y-1 max-w-md mx-auto">
                  <li>• Sprawdź czy backend działa na <code className="bg-gray-200 px-1 rounded">localhost:8000</code></li>
                  <li>• Upewnij się że symbole akcji są poprawne (np. AAPL, MSFT)</li>
                  <li>• Wyczyść cache przeglądarki (Ctrl+Shift+Delete)</li>
                  <li>• Sprawdź połączenie z internetem</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )
    }

    // Brak błędu - renderuj normalne children
    return this.props.children
  }
}
