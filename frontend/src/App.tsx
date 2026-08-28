import { useCallback, useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import { api } from './services/api';
import type { Career, Stats } from './types';
import CareerExplorer from './pages/CareerExplorer';
import Connections from './pages/Connections';
import Home from './pages/Home';

export default function App() {
  const [careers, setCareers] = useState<Career[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadHomeData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [careersData, statsData] = await Promise.all([
        api.getCareers(),
        api.getStats(),
      ]);
      setCareers(careersData);
      setStats(statsData);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Unable to connect to the backend.';
      setError(
        message.includes('503') || message.includes('unavailable')
          ? 'The database is currently unavailable. Please check your CognoDB connection and try again.'
          : message,
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHomeData();
  }, [loadHomeData]);

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route
            path="/"
            element={
              <Home
                careers={careers}
                stats={stats}
                loading={loading}
                error={error}
                onRetry={loadHomeData}
              />
            }
          />
          <Route path="/career/:careerName" element={<CareerExplorer />} />
          <Route path="/connections" element={<Connections />} />
        </Routes>
      </main>
      <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-400">
        SkillGraph AI — Wexa AI Take-Home Assignment · Graph data powered by CognoDB
      </footer>
    </div>
  );
}
