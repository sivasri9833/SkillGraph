import {
  ArrowLeft,
  BookOpen,
  FolderKanban,
  Layers,
  Network,
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import ErrorState from '../components/ErrorState';
import LearningPath from '../components/LearningPath';
import LoadingState from '../components/LoadingState';
import SkillGraph from '../components/SkillGraph';
import { api } from '../services/api';
import type { CareerDetail, GraphData, LearningPath as LearningPathType } from '../types';

type Tab = 'overview' | 'graph' | 'learning-path';

export default function CareerExplorer() {
  const { careerName } = useParams<{ careerName: string }>();
  const decodedName = decodeURIComponent(careerName ?? '');

  const [career, setCareer] = useState<CareerDetail | null>(null);
  const [graph, setGraph] = useState<GraphData | null>(null);
  const [learningPath, setLearningPath] = useState<LearningPathType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('overview');

  async function loadData() {
    if (!decodedName) return;
    setLoading(true);
    setError(null);
    try {
      const [careerData, graphData, pathData] = await Promise.all([
        api.getCareer(decodedName),
        api.getCareerGraph(decodedName),
        api.getLearningPath(decodedName),
      ]);
      setCareer(careerData);
      setGraph(graphData);
      setLearningPath(pathData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load career data.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [decodedName]);

  const tabs: { id: Tab; label: string; icon: typeof Network }[] = [
    { id: 'overview', label: 'Overview', icon: Layers },
    { id: 'graph', label: 'Skill Graph', icon: Network },
    { id: 'learning-path', label: 'Learning Path', icon: BookOpen },
  ];

  if (loading) return <LoadingState message={`Loading ${decodedName}...`} />;
  if (error || !career)
    return (
      <div className="mx-auto max-w-3xl px-4 py-12">
        <ErrorState message={error ?? 'Career not found.'} onRetry={loadData} />
      </div>
    );

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <Link
        to="/"
        className="mb-6 inline-flex items-center gap-1.5 text-sm text-slate-500 transition-colors hover:text-brand-600"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Home
      </Link>

      {/* Header */}
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-brand-600">
              {career.category}
            </p>
            <h1 className="mt-1 text-3xl font-bold text-slate-900">{career.name}</h1>
            <p className="mt-3 max-w-2xl text-slate-600">{career.description}</p>
          </div>
          <span className="rounded-full bg-brand-100 px-3 py-1 text-sm font-medium text-brand-700">
            {career.difficulty}
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="mt-6 flex gap-1 overflow-x-auto rounded-xl border border-slate-200 bg-slate-100 p-1">
        {tabs.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            className={`flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors ${
              activeTab === id
                ? 'bg-white text-brand-700 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Icon className="h-4 w-4" />
            {label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="mt-6">
        {activeTab === 'overview' && (
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-xl border border-slate-200 bg-white p-6">
              <h3 className="flex items-center gap-2 text-lg font-semibold text-slate-900">
                <Layers className="h-5 w-5 text-brand-600" />
                Required Skills ({career.skills.length})
              </h3>
              <ul className="mt-4 space-y-3">
                {career.skills.map((skill) => (
                  <li
                    key={skill.name}
                    className="flex items-start justify-between rounded-lg border border-slate-100 bg-slate-50 p-3"
                  >
                    <div>
                      <p className="font-medium text-slate-900">{skill.name}</p>
                      <p className="text-xs text-slate-500">{skill.category}</p>
                    </div>
                    <span className="rounded-full bg-white px-2 py-0.5 text-xs text-slate-600">
                      {skill.difficulty}
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-6">
              <h3 className="flex items-center gap-2 text-lg font-semibold text-slate-900">
                <FolderKanban className="h-5 w-5 text-brand-600" />
                Recommended Projects ({career.projects.length})
              </h3>
              <ul className="mt-4 space-y-3">
                {career.projects.map((project) => (
                  <li
                    key={project.name}
                    className="rounded-lg border border-slate-100 bg-slate-50 p-3"
                  >
                    <div className="flex items-start justify-between">
                      <p className="font-medium text-slate-900">{project.name}</p>
                      <span className="rounded-full bg-white px-2 py-0.5 text-xs text-slate-600">
                        {project.difficulty}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-slate-600">{project.description}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {activeTab === 'graph' && graph && <SkillGraph graphData={graph} />}

        {activeTab === 'learning-path' && learningPath && (
          <LearningPath careerName={learningPath.career} path={learningPath.path} />
        )}
      </div>
    </div>
  );
}
