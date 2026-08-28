import { ArrowRight, Briefcase, GitBranch, Layers, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';
import CareerCard from '../components/CareerCard';
import ErrorState from '../components/ErrorState';
import LoadingState from '../components/LoadingState';
import SearchBar from '../components/SearchBar';
import type { Career, Stats } from '../types';

interface HomeProps {
  careers: Career[];
  stats: Stats | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
}

export default function Home({ careers, stats, loading, error, onRetry }: HomeProps) {
  if (loading) return <LoadingState message="Loading SkillGraph AI..." />;
  if (error) return <ErrorState message={error} onRetry={onRetry} />;

  return (
    <div>
      {/* Hero */}
      <section className="border-b border-slate-200 bg-gradient-to-br from-brand-50 via-white to-indigo-50">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-brand-100 px-3 py-1 text-sm font-medium text-brand-700">
              <Sparkles className="h-4 w-4" />
              Powered by CognoDB Graph Database
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
              SkillGraph AI
            </h1>
            <p className="mt-4 text-lg leading-relaxed text-slate-600">
              Explore career paths, discover skill prerequisites, and visualize
              how technologies connect — all powered by graph traversal over
              real relationship data.
            </p>
            <p className="mt-2 text-sm text-slate-500">
              &ldquo;If I want to become a particular type of software professional,
              what skills should I learn, in what order, and how are those skills connected?&rdquo;
            </p>

            <div className="mt-8 flex justify-center">
              <SearchBar />
            </div>

            <Link
              to={`/career/${encodeURIComponent(careers[0]?.name ?? 'Frontend Developer')}`}
              className="mt-6 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-brand-700"
            >
              Explore Career Paths
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      {stats && (
        <section className="border-b border-slate-200 bg-white">
          <div className="mx-auto grid max-w-7xl grid-cols-1 divide-y divide-slate-200 sm:grid-cols-3 sm:divide-x sm:divide-y-0">
            {[
              { label: 'Career Paths', value: stats.careers, icon: Briefcase },
              { label: 'Skills', value: stats.skills, icon: Layers },
              { label: 'Relationships', value: stats.relationships, icon: GitBranch },
            ].map(({ label, value, icon: Icon }) => (
              <div key={label} className="flex items-center justify-center gap-4 px-6 py-8">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600">
                  <Icon className="h-6 w-6" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-slate-900">{value}</p>
                  <p className="text-sm text-slate-500">{label}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Career cards */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold text-slate-900">Available Career Paths</h2>
        <p className="mt-1 text-slate-600">
          Select a career to explore required skills, learning paths, and project recommendations.
        </p>
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {careers.map((career) => (
            <CareerCard key={career.name} career={career} />
          ))}
        </div>
      </section>
    </div>
  );
}
