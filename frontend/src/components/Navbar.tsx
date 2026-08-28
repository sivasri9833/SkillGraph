import { GitBranch, Home, Link2, Network } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Home', icon: Home },
  { to: '/connections', label: 'Connections', icon: Link2 },
];

export default function Navbar() {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2.5 transition-opacity hover:opacity-80">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600 text-white shadow-sm">
            <Network className="h-5 w-5" />
          </div>
          <div className="text-left">
            <span className="block text-lg font-bold tracking-tight text-slate-900">
              SkillGraph AI
            </span>
            <span className="hidden text-xs text-slate-500 sm:block">
              Career & Skill Explorer
            </span>
          </div>
        </Link>

        <nav className="flex items-center gap-1">
          {navItems.map(({ to, label, icon: Icon }) => {
            const active = location.pathname === to;
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  active
                    ? 'bg-brand-50 text-brand-700'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span className="hidden sm:inline">{label}</span>
              </Link>
            );
          })}
          <a
            href="https://cognodb.cloud"
            target="_blank"
            rel="noopener noreferrer"
            className="ml-2 hidden items-center gap-1.5 rounded-lg px-3 py-2 text-sm text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-700 md:flex"
          >
            <GitBranch className="h-4 w-4" />
            Powered by CognoDB
          </a>
        </nav>
      </div>
    </header>
  );
}
