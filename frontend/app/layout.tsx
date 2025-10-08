import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { Toaster } from 'react-hot-toast';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Multibagger Stock Scanner",
  description: "Automated stock scanner for finding multibagger opportunities",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>

        {/* Toast Notifications - globalne powiadomienia dla użytkownika */}
        <Toaster
          position="top-right"
          toastOptions={{
            // Domyślne ustawienia dla wszystkich toastów
            duration: 4000,
            style: {
              background: '#1f2937', // gray-800
              color: '#fff',
              fontWeight: '600',
              fontSize: '0.95rem',
              borderRadius: '0.5rem',
              padding: '1rem 1.25rem',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.3)',
            },
            // Toast sukcesu - zielona ikonka
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10b981', // green-500
                secondary: '#fff',
              },
              style: {
                background: '#065f46', // green-800
                color: '#fff',
              },
            },
            // Toast błędu - czerwona ikonka, dłuższy czas wyświetlania
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444', // red-500
                secondary: '#fff',
              },
              style: {
                background: '#991b1b', // red-800
                color: '#fff',
              },
            },
            // Toast ostrzeżenia - żółta ikonka
            loading: {
              iconTheme: {
                primary: '#3b82f6', // blue-500
                secondary: '#fff',
              },
            },
          }}
        />
      </body>
    </html>
  );
}
