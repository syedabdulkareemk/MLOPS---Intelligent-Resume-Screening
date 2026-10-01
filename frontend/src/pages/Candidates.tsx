import { useState, useEffect } from 'react';
import { Users, Loader2 } from 'lucide-react';
import api from '../api';

export default function Candidates() {
  const [candidates, setCandidates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/api/candidates').then(res => setCandidates(res.data)).catch(console.error).finally(() => setLoading(false));
  }, []);

  return (
    <div className='p-8 max-w-6xl mx-auto'>
      <h1 className='text-3xl font-bold text-slate-800 mb-8'>Candidates Pool</h1>
      
      {loading ? (
        <div className='flex justify-center p-12'><Loader2 className='w-8 h-8 animate-spin text-blue-500'/></div>
      ) : candidates.length === 0 ? (
        <div className='bg-white p-12 text-center rounded-xl border border-slate-200'>
          <Users className='w-12 h-12 text-slate-300 mx-auto mb-4'/>
          <h2 className='text-xl font-bold text-slate-700 mb-2'>No candidates found</h2>
          <p className='text-slate-500 mb-6'>Load the demo workspace or upload resumes via the Screening page.</p>
        </div>
      ) : (
        <div className='grid grid-cols-2 gap-6'>
          {candidates.map(c => (
            <div key={c.id} className='bg-white p-6 rounded-xl border border-slate-200 hover:shadow-md transition-shadow'>
              <h2 className='text-xl font-bold text-slate-800'>{c.name}</h2>
              <p className='text-slate-500 text-sm mt-1'>{c.years_experience} Years Experience</p>
              <div className='flex flex-wrap gap-2 mt-4'>
                {c.skills_list.slice(0, 8).map((s: string) => <span key={s} className='text-xs font-bold bg-blue-50 text-blue-700 px-2 py-1 rounded'>{s}</span>)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
