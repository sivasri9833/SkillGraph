import { ArrowRight, Briefcase } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { Career } from '../types';

const difficultyColors: Record<string, string> = {
  Beginner: 'bg-emerald-100 text-emerald-700',
  Intermediate: 'bg-amber-100 text-amber-700',
  Advanced: 'bg-rose-100 text-rose-700',
};

interface CareerCardProps {
  career: Career;
}

export default function CareerCard({ career }: CareerCardProps) {
  const badgeClass =
    difficultyColors[career.difficulty] ?? 'bg-slate-100 text-slate-700';

  return (
    <Link
      to={`/career/${encodeURIComponent(career.name)}`}
      className="group flex flex-col rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition-all hover:border-brand-300 hover:shadow-md"
    >
      <div className="mb-4 flex items-start justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600 transition-colors group-hover:bg-brand-100">
          <Briefcase className="h-5 w-5" />
        </div>
        <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${badgeClass}`}>
          {career.difficulty}
        </span>
      </div>

      <h3 className="text-lg font-semibold text-slate-900 group-hover:text-brand-700">
        {career.name}
      </h3>
      <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-400">
        {career.category}
      </p>
      <p className="mt-3 flex-1 text-sm leading-relaxed text-slate-600 line-clamp-3">
        {career.description}
      </p>

      <div className="mt-4 flex items-center gap-1 text-sm font-medium text-brand-600 opacity-0 transition-opacity group-hover:opacity-100">
        Explore path
        <ArrowRight className="h-4 w-4" />
      </div>
    </Link>
  );
}
