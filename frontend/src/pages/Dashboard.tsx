import { Link } from 'react-router-dom';
import { FileSearch, Users, Briefcase, Activity, Network } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className='p-8 max-w-6xl mx-auto'>
      <div className='mb-12'>
        <h1 className='text-4xl font-bold text-slate-800 mb-4'>TalentLens Intelligence</h1>
        <p className='text-lg text-slate-600 max-w-3xl'>
          Welcome to the MLOps-driven recruitment platform. TalentLens uses hybrid semantic matching and career twin extraction to accurately evaluate candidate fit beyond keywords.
        </p>
      </div>

      <div className='grid grid-cols-3 gap-6 mb-12'>
        <Link to="/screening" className='bg-blue-600 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow flex flex-col gap-4 group'>
          <FileSearch className='w-10 h-10 group-hover:scale-110 transition-transform'/>
          <h2 className='text-2xl font-bold'>Run Screening</h2>
          <p className='text-blue-100 text-sm'>Upload a JD and Resume to execute the 6-stage Hybrid Matcher pipeline.</p>
        </Link>

        <Link to="/jobs" className='bg-white border border-slate-200 text-slate-800 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow flex flex-col gap-4 group'>
          <Briefcase className='w-10 h-10 text-blue-600 group-hover:scale-110 transition-transform'/>
          <h2 className='text-2xl font-bold'>Active Jobs</h2>
          <p className='text-slate-500 text-sm'>Manage parsed job descriptions and requirement skill structures.</p>
        </Link>

        <Link to="/candidates" className='bg-white border border-slate-200 text-slate-800 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow flex flex-col gap-4 group'>
          <Users className='w-10 h-10 text-blue-600 group-hover:scale-110 transition-transform'/>
          <h2 className='text-2xl font-bold'>Candidate Pool</h2>
          <p className='text-slate-500 text-sm'>Browse extracted candidate career twins and evidence records.</p>
        </Link>
      </div>

      <div className='grid grid-cols-2 gap-6'>
        <div className='bg-slate-900 p-8 rounded-2xl text-white'>
          <Network className='w-8 h-8 text-blue-400 mb-4'/>
          <h3 className='text-xl font-bold mb-2'>Knowledge Graph Offline</h3>
          <p className='text-slate-400 text-sm mb-6'>The Neo4j database is currently disconnected in this local CPU environment. Deep graph traversal and taxonomy-based transferable skill detection are running in fallback mode.</p>
          <Link to="/mlops" className='text-blue-400 font-medium hover:text-blue-300'>View Infrastructure Status &rarr;</Link>
        </div>
        
        <div className='bg-indigo-50 p-8 rounded-2xl border border-indigo-100'>
          <Activity className='w-8 h-8 text-indigo-600 mb-4'/>
          <h3 className='text-xl font-bold text-indigo-900 mb-2'>Local ML Engine Active</h3>
          <p className='text-indigo-700 text-sm mb-6'>The PyTorch `sentence-transformers` models are successfully loaded in memory. Semantic embeddings and lexical extraction will process normally.</p>
          <span className='inline-flex items-center gap-2 bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full text-xs font-bold'>
            <span className='w-2 h-2 rounded-full bg-indigo-600 animate-pulse'></span> all-MiniLM-L6-v2
          </span>
        </div>
      </div>
    </div>
  );
}
