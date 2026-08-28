import { BookOpen, ChevronRight } from 'lucide-react';
import type { LearningPathItem } from '../types';

const difficultyColors: Record<string, string> = {
  Beginner: 'border-emerald-300 bg-emerald-50',
  Intermediate: 'border-amber-300 bg-amber-50',
  Advanced: 'border-rose-300 bg-rose-50',
};

interface LearningPathProps {
  careerName: string;
  path: LearningPathItem[];
}

export default function LearningPath({ careerName, path }: LearningPathProps) {
  if (path.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-6 py-10 text-center">
        <BookOpen className="mx-auto h-8 w-8 text-slate-400" />
        <p className="mt-2 text-sm text-slate-500">
          No learning path available for {careerName}.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6">
      <div className="mb-6 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
          <BookOpen className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-900">
            {careerName} Learning Path
          </h3>
          <p className="text-sm text-slate-500">
            Recommended skill order based on prerequisite relationships
          </p>
        </div>
      </div>

      <ol className="space-y-3">
        {path.map((item, index) => {
          const colorClass =
            difficultyColors[item.difficulty] ?? 'border-slate-200 bg-slate-50';
          return (
            <li key={item.name} className="flex items-stretch gap-3">
              <div className="flex flex-col items-center">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-600 text-sm font-bold text-white">
                  {item.order}
                </span>
                {index < path.length - 1 && (
                  <div className="mt-1 w-0.5 flex-1 bg-brand-200" />
                )}
              </div>
              <div
                className={`mb-1 flex-1 rounded-lg border-l-4 p-4 ${colorClass}`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h4 className="font-semibold text-slate-900">{item.name}</h4>
                    <p className="mt-0.5 text-xs font-medium text-slate-500">
                      {item.category}
                    </p>
                  </div>
                  <span className="shrink-0 rounded-full bg-white/80 px-2 py-0.5 text-xs font-medium text-slate-600">
                    {item.difficulty}
                  </span>
                </div>
                {item.description && (
                  <p className="mt-2 text-sm text-slate-600">{item.description}</p>
                )}
              </div>
              {index < path.length - 1 && (
                <ChevronRight className="mt-2 hidden h-5 w-5 shrink-0 text-brand-300 sm:block" />
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
}
