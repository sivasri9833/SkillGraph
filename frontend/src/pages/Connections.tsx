import { ArrowRight, Link2, Search } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import ErrorState from '../components/ErrorState';
import LoadingState from '../components/LoadingState';
import { api } from '../services/api';
import type { ConnectionResult, Skill } from '../types';

export default function Connections() {
  const location = useLocation();
  const initialSource = (location.state as { source?: string })?.source ?? '';

  const [skills, setSkills] = useState<Skill[]>([]);
  const [source, setSource] = useState(initialSource);
  const [target, setTarget] = useState('');
  const [result, setResult] = useState<ConnectionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [skillsLoading, setSkillsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getSkills()
      .then(setSkills)
      .catch(() => setError('Failed to load skills list.'))
      .finally(() => setSkillsLoading(false));
  }, []);

  async function findConnection() {
    if (!source || !target) return;
    if (source === target) {
      setError('Please select two different skills.');
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await api.getConnections(source, target);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to find connection.');
    } finally {
      setLoading(false);
    }
  }

  if (skillsLoading) return <LoadingState message="Loading skills..." />;

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-100 text-brand-600">
          <Link2 className="h-7 w-7" />
        </div>
        <h1 className="mt-4 text-3xl font-bold text-slate-900">Relationship Explorer</h1>
        <p className="mt-2 text-slate-600">
          Discover how two skills are connected through the graph — paths that would
          require complex recursive joins in a relational database.
        </p>
      </div>

      <div className="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid gap-4 sm:grid-cols-[1fr_auto_1fr] sm:items-end">
          <div>
            <label className="mb-1.5 block text-sm font-medium text-slate-700">
              Source Skill
            </label>
            <select
              value={source}
              onChange={(e) => setSource(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100"
            >
              <option value="">Select a skill...</option>
              {skills.map((s) => (
                <option key={s.name} value={s.name}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>

          <div className="hidden justify-center sm:flex">
            <ArrowRight className="mb-3 h-5 w-5 text-slate-400" />
          </div>

          <div>
            <label className="mb-1.5 block text-sm font-medium text-slate-700">
              Target Skill
            </label>
            <select
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100"
            >
              <option value="">Select a skill...</option>
              {skills.map((s) => (
                <option key={s.name} value={s.name}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          onClick={findConnection}
          disabled={!source || !target || loading}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 px-4 py-3 text-sm font-semibold text-white transition-colors hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Search className="h-4 w-4" />
          {loading ? 'Searching graph...' : 'Find Connection'}
        </button>
      </div>

      {error && (
        <div className="mt-6">
          <ErrorState message={error} onRetry={findConnection} />
        </div>
      )}

      {result && (
        <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          {result.found ? (
            <>
              <p className="text-sm text-slate-600">{result.message}</p>
              <div className="mt-4 flex flex-wrap items-center gap-2">
                {result.path_nodes.map((node, i) => (
                  <div key={`${node}-${i}`} className="flex items-center gap-2">
                    <span className="rounded-lg bg-brand-50 px-3 py-1.5 text-sm font-medium text-brand-800">
                      {node}
                    </span>
                    {i < result.path_nodes.length - 1 && (
                      <ArrowRight className="h-4 w-4 text-slate-400" />
                    )}
                  </div>
                ))}
              </div>

              {result.steps.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-sm font-semibold text-slate-700">Path Details</h3>
                  <ol className="mt-3 space-y-2">
                    {result.steps.map((step, i) => (
                      <li
                        key={i}
                        className="flex items-center gap-3 rounded-lg bg-slate-50 px-4 py-2.5 text-sm"
                      >
                        <span className="font-medium text-slate-900">{step.from_node}</span>
                        <span className="rounded bg-white px-2 py-0.5 text-xs font-medium text-brand-600">
                          {step.relationship.replace(/_/g, ' ')}
                        </span>
                        <ArrowRight className="h-3 w-3 text-slate-400" />
                        <span className="font-medium text-slate-900">{step.to_node}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-6">
              <p className="text-slate-600">{result.message}</p>
              <p className="mt-2 text-sm text-slate-400">
                Try different skill pairs like React → SQL or JavaScript → Machine Learning.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
