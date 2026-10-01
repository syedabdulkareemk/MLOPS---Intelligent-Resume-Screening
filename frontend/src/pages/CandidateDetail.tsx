import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { CheckCircle2, AlertCircle, ArrowRight, Loader2, GitMerge } from 'lucide-react';
import api from '../api';

export default function CandidateDetail() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const jobId = searchParams.get('job_id');
  
  const [candidate, setCandidate] = useState<any>(null);
  const [job, setJob] = useState<any>(null);
  const [match, setMatch] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  const [simulateSkill, setSimulateSkill] = useState('');
  const [simLoading, setSimLoading] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [candRes, jobRes, matchRes] = await Promise.all([
          api.get(`/api/candidates/${id}`),
          api.get(`/api/jobs/${jobId}`),
          api.get(`/api/matches/${id}/${jobId}`)
        ]);
        setCandidate(candRes.data);
        setJob(jobRes.data);
        setMatch(matchRes.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [id, jobId]);

  const handleSimulate = async () => {
    if (!simulateSkill) return;
    setSimLoading(true);
    try {
      const res = await api.post(`/api/match?candidate_id=${id}&job_id=${jobId}&simulate_skill=${simulateSkill}`);
      setMatch(res.data);
      setSimulateSkill('');
    } catch (e) {
      console.error(e);
    } finally {
      setSimLoading(false);
    }
  };

  if (loading) return <div className='p-12 flex justify-center'><Loader2 className='animate-spin w-8 h-8 text-blue-600'/></div>;
  if (!candidate || !match) return <div className='p-8 text-red-500'>Failed to load candidate or match data.</div>;

  return (
    <div className='p-8 max-w-6xl mx-auto'>
      
      {/* Header */}
      <div className='flex justify-between items-start mb-8'>
        <div>
          <h1 className='text-3xl font-bold text-slate-800 mb-2'>{candidate.name}</h1>
          <p className='text-slate-500 text-lg'>Target Role: <span className='font-bold text-slate-700'>{job?.title}</span></p>
        </div>
        <div className='flex gap-4'>
          <div className='text-center p-4 bg-slate-100 rounded-xl border border-slate-200'>
            <p className='text-xs font-bold text-slate-500 uppercase tracking-wider mb-1'>Current Fit</p>
            <p className='text-4xl font-bold text-slate-800'>{(match.current_fit * 100).toFixed(0)}%</p>
          </div>
          <div className='text-center p-4 bg-blue-50 rounded-xl border border-blue-200'>
            <p className='text-xs font-bold text-blue-600 uppercase tracking-wider mb-1'>Potential Fit</p>
            <p className='text-4xl font-bold text-blue-800'>{(match.potential_fit * 100).toFixed(0)}%</p>
          </div>
        </div>
      </div>

      <div className='grid grid-cols-3 gap-8'>
        
        {/* Left Column - Gaps & Twin */}
        <div className='col-span-2 space-y-8'>
          
          <div className='bg-white p-6 rounded-xl border border-slate-200 shadow-sm'>
            <h2 className='text-xl font-bold mb-4 flex items-center gap-2'><CheckCircle2 className='text-green-600'/> Candidate Career Twin (Evidence)</h2>
            <div className='space-y-4'>
              <div>
                <h3 className='font-bold text-slate-700 mb-2'>Supported Skills (Parsed from Resume)</h3>
                <div className='flex flex-wrap gap-2'>
                  {match.matched_skills.map((s: string) => (
                    <span key={s} className='px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium border border-green-200'>
                      {s} ✓
                    </span>
                  ))}
                  {candidate.skills_list.filter((s: string) => !match.matched_skills.includes(s)).map((s: string) => (
                    <span key={s} className='px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm font-medium border border-slate-200'>
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            
            <div className='mt-6 pt-6 border-t'>
              <h3 className='font-bold text-slate-700 mb-2'>Extracted Resume Evidence</h3>
              <p className='text-sm text-slate-600 whitespace-pre-wrap bg-slate-50 p-4 rounded border'>
                {candidate.full_text}
              </p>
            </div>
          </div>

          <div className='bg-white p-6 rounded-xl border border-slate-200 shadow-sm'>
            <h2 className='text-xl font-bold mb-4 flex items-center gap-2'><AlertCircle className='text-amber-500'/> Skill Gap & Transferability</h2>
            <div className='space-y-6'>
              
              <div>
                <h3 className='text-sm font-bold text-slate-500 uppercase mb-3'>Missing Skills</h3>
                <div className='flex flex-wrap gap-2'>
                  {match.missing_skills.length === 0 && <span className='text-sm text-slate-500'>No missing skills detected.</span>}
                  {match.missing_skills.map((s: string) => (
                    <span key={s} className='px-3 py-1 bg-red-50 text-red-700 rounded border border-red-200 text-sm'>
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className='text-sm font-bold text-slate-500 uppercase mb-3'>Transferable Skills (Graph Logic)</h3>
                <div className='space-y-2'>
                  {match.transferable_skills.length === 0 && <span className='text-sm text-slate-500'>No transferable skills detected for missing requirements.</span>}
                  {match.transferable_skills.map((s: string, i: number) => (
                    <div key={i} className='flex items-center gap-3 p-3 bg-blue-50 rounded border border-blue-100 text-sm'>
                      <GitMerge className='w-4 h-4 text-blue-500'/>
                      <span className='font-medium text-blue-900'>{s}</span>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          </div>

        </div>

        {/* Right Column - Simulator & Breakdown */}
        <div className='space-y-8'>
          
          <div className='bg-slate-900 p-6 rounded-xl text-white shadow-lg'>
            <h2 className='text-xl font-bold mb-4 flex items-center gap-2'>Skill Gap Simulator</h2>
            <p className='text-slate-400 text-sm mb-4'>Test how acquiring a missing skill impacts the candidate's Fit Score via the ML Engine.</p>
            <div className='space-y-3'>
              <input 
                type="text" 
                value={simulateSkill}
                onChange={e => setSimulateSkill(e.target.value)}
                placeholder="e.g. Kubernetes"
                className='w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-white'
              />
              <button 
                onClick={handleSimulate}
                disabled={simLoading || !simulateSkill}
                className='w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 rounded transition-colors flex justify-center'
              >
                {simLoading ? <Loader2 className='w-5 h-5 animate-spin'/> : 'Recalculate Fit'}
              </button>
            </div>
          </div>

          <div className='bg-white p-6 rounded-xl border border-slate-200 shadow-sm'>
            <div className='mb-4'>
              <h2 className='font-bold text-slate-800'>Match Breakdown</h2>
              <p className='text-xs text-indigo-500 font-bold bg-indigo-50 inline-block px-2 py-1 rounded mt-1'>
                Model: {match.model_version_used || 'V1 (Fallback)'}
              </p>
            </div>
            <div className='space-y-4'>
              <div>
                <div className='flex justify-between text-sm mb-1'>
                  <span className='text-slate-600'>Semantic Match</span>
                  <span className='font-medium'>{(match.semantic_fit * 100).toFixed(0)}%</span>
                </div>
                <div className='w-full bg-slate-100 rounded-full h-2'><div className='bg-blue-500 h-2 rounded-full' style={{width: `${match.semantic_fit * 100}%`}}></div></div>
              </div>
              <div>
                <div className='flex justify-between text-sm mb-1'>
                  <span className='text-slate-600'>Canonical Skill Match</span>
                  <span className='font-medium'>{(match.skill_fit * 100).toFixed(0)}%</span>
                </div>
                <div className='w-full bg-slate-100 rounded-full h-2'><div className='bg-indigo-500 h-2 rounded-full' style={{width: `${match.skill_fit * 100}%`}}></div></div>
              </div>
              <div>
                <div className='flex justify-between text-sm mb-1'>
                  <span className='text-slate-600'>Evidence Context Match</span>
                  <span className='font-medium'>{(match.evidence_fit * 100).toFixed(0)}%</span>
                </div>
                <div className='w-full bg-slate-100 rounded-full h-2'><div className='bg-emerald-500 h-2 rounded-full' style={{width: `${match.evidence_fit * 100}%`}}></div></div>
              </div>
              <div>
                <div className='flex justify-between text-sm mb-1'>
                  <span className='text-slate-600'>Experience Match</span>
                  <span className='font-medium'>100%</span>
                </div>
                <div className='w-full bg-slate-100 rounded-full h-2'><div className='bg-amber-500 h-2 rounded-full' style={{width: `100%`}}></div></div>
              </div>
              <div>
                <div className='flex justify-between text-sm mb-1'>
                  <span className='text-slate-600'>Transferability Factor</span>
                  <span className='font-medium'>{(match.transferable_skills.length > 0 ? 100 : 0)}%</span>
                </div>
                <div className='w-full bg-slate-100 rounded-full h-2'><div className='bg-purple-500 h-2 rounded-full' style={{width: `${(match.transferable_skills.length > 0 ? 100 : 0)}%`}}></div></div>
              </div>
            </div>
            <p className='text-xs text-slate-400 mt-6 pt-4 border-t'>Scores computed via local SentenceTransformers CPU pipeline.</p>
          </div>

        </div>
      </div>
    </div>
  );
}
