import { Network, AlertCircle } from 'lucide-react';

export default function SkillGraph() {
  return (
    <div className='p-8 max-w-6xl mx-auto'>
      <div className='flex justify-between items-center mb-8'>
        <h1 className='text-3xl font-bold text-slate-800'>Career Intelligence Graph</h1>
      </div>
      
      <div className='bg-slate-50 border border-slate-200 rounded-xl p-12 text-center h-[500px] flex flex-col items-center justify-center'>
        <Network className='w-16 h-16 text-slate-300 mb-4'/>
        <h2 className='text-2xl font-bold text-slate-700 mb-2'>Neo4j Infrastructure Required</h2>
        <p className='text-slate-500 max-w-lg mb-6'>
          The interactive visualization of the Candidate ↔ Job bipartite graph and Career Pathway nodes requires the Neo4j database to be actively running.
        </p>
        <div className='bg-white p-4 rounded border border-amber-200 flex items-start gap-3 text-left max-w-md mx-auto shadow-sm'>
          <AlertCircle className='w-5 h-5 text-amber-500 shrink-0 mt-0.5'/>
          <div>
            <p className='font-bold text-amber-800 text-sm'>Local CPU Mode</p>
            <p className='text-xs text-amber-700 mt-1'>
              Please deploy the full Docker Compose stack to enable graph persistence and visual career traversal. The hybrid matcher is currently using fallback static edge logic for transferable skills.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
