import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Network, Users, Briefcase, FileSearch, Activity, LayoutDashboard, Zap } from 'lucide-react';
import api from './api';
import Dashboard from './pages/Dashboard';
import Candidates from './pages/Candidates';
import CandidateDetail from './pages/CandidateDetail';
import Jobs from './pages/Jobs';
import Screening from './pages/Screening';
import SkillGraph from './pages/SkillGraph';
import MLOps from './pages/MLOps';

function Sidebar() {
  const location = useLocation();
  const triggerDemoMode = async () => {
    try {
      await api.post('/api/demo');
      alert('Demo workspace loaded successfully!');
      window.location.reload();
    } catch (e) {
      console.error(e);
      alert('Demo mode failed. Ensure backend is running.');
    }
  };

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/candidates', icon: Users, label: 'Candidates' },
    { path: '/jobs', icon: Briefcase, label: 'Jobs' },
    { path: '/screening', icon: FileSearch, label: 'Screening' },
    { path: '/skill-graph', icon: Network, label: 'Skill Graph' },
    { path: '/mlops', icon: Activity, label: 'MLOps' },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen sticky top-0 shrink-0">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Network className="w-6 h-6 text-blue-500" />
          TalentLens
        </h1>
        <p className="text-xs mt-2 text-slate-500 uppercase font-semibold tracking-wider">AI Recruitment Intelligence</p>
      </div>
      
      <nav className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path || location.pathname.startsWith(item.path + '/');
          return (
            <Link key={item.path} to={item.path} className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 hover:text-white'}`}>
              <Icon className="w-5 h-5" /> {item.label}
            </Link>
          );
        })}
      </nav>
      
      <div className="p-4 border-t border-slate-800">
        <button 
          onClick={triggerDemoMode}
          className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium transition-colors"
        >
          <Zap className="w-4 h-4" /> Load Demo Workspace
        </button>
      </div>
    </aside>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 flex">
        <Sidebar />
        <main className="flex-1 overflow-auto h-screen">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/candidates" element={<Candidates />} />
            <Route path="/candidates/:id" element={<CandidateDetail />} />
            <Route path="/jobs" element={<Jobs />} />
            <Route path="/screening" element={<Screening />} />
            <Route path="/skill-graph" element={<SkillGraph />} />
            <Route path="/mlops" element={<MLOps />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
