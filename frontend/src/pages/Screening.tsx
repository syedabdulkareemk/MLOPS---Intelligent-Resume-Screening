import { useState, useEffect } from 'react';
import { UploadCloud, CheckCircle2, FileText, ChevronRight, Loader2, List, Activity, Target, AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Screening() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedJob, setSelectedJob] = useState<string>('');
  const [files, setFiles] = useState<File[]>([]);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'processing' | 'done'>('idle');
  const [progress, setProgress] = useState({ current: 0, total: 0, step: '' });
  const [results, setResults] = useState<any[]>([]);
  const [modelDeployed, setModelDeployed] = useState<boolean | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/api/jobs').then(res => setJobs(res.data)).catch(console.error);
    
    // Check if model is deployed
    api.get('/api/mlops/status').then(res => {
      setModelDeployed(!!res.data.champion_version);
    }).catch(console.error);
  }, []);

  if (modelDeployed === false) {
    return (
      <div className='p-12 max-w-2xl mx-auto mt-20 text-center bg-red-50 border border-red-200 rounded-xl'>
        <AlertTriangle className='w-16 h-16 text-red-500 mx-auto mb-4'/>
        <h2 className='text-2xl font-bold text-red-800 mb-2'>Matching model not deployed yet.</h2>
        <p className='text-red-600 mb-6'>Ask an ML administrator to complete the initial training pipeline before screening candidates.</p>
        <button onClick={() => navigate('/mlops')} className='bg-red-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-red-700'>
          GO TO MLOPS
        </button>
      </div>
    );
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleAnalyze = async () => {
    if (!selectedJob || files.length === 0) return;
    
    setStatus('processing');
    const newResults = [];
    setProgress({ current: 0, total: files.length, step: 'Uploading & Parsing' });

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      setProgress({ current: i + 1, total: files.length, step: `Processing ${file.name}` });
      
      try {
        const formData = new FormData();
        formData.append('file', file);
        const candRes = await api.post('/api/candidates/upload', formData);
        const candId = candRes.data.candidate_id;

        const matchRes = await api.post(`/api/match?candidate_id=${candId}&job_id=${selectedJob}`);
        newResults.push({
          candidate_id: candId,
          name: candRes.data.name,
          ...matchRes.data
        });
      } catch (e) {
        console.error(`Failed to process ${file.name}`, e);
      }
    }
    
    // Sort by Current Fit
    newResults.sort((a, b) => b.current_fit - a.current_fit);
    setResults(newResults);
    setStatus('done');
  };

  const activeJobName = jobs.find(j => j.id === selectedJob)?.title || 'Select a Job';

  return (
    <div className='p-8 max-w-5xl mx-auto'>
      <div className='mb-8 border-b pb-4'>
        <h1 className='text-3xl font-bold text-slate-800 mb-2'>Screen Candidates</h1>
        <p className='text-slate-500'>Batch process resumes against an active job description.</p>
      </div>

      <div className='grid grid-cols-3 gap-8'>
        
        {/* Left Col - Config */}
        <div className='col-span-1 space-y-6'>
          <div className='bg-white p-5 rounded-xl border border-slate-200 shadow-sm'>
            <h2 className='font-bold text-slate-700 mb-3'>1. Select Job</h2>
            <select 
              value={selectedJob} 
              onChange={e => setSelectedJob(e.target.value)}
              className='w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded outline-none focus:border-blue-500'
            >
              <option value="">-- Choose Job --</option>
              {jobs.map(j => (
                <option key={j.id} value={j.id}>{j.title}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Right Col - Upload & Results */}
        <div className='col-span-2 space-y-6'>
          
          {status === 'idle' && (
            <div className='bg-white p-6 rounded-xl border border-slate-200 shadow-sm'>
              <h2 className='font-bold text-slate-700 mb-4'>2. Upload Resumes</h2>
              <p className='text-sm text-slate-500 mb-4'>Selected Job: <span className='font-bold text-slate-700'>{activeJobName}</span></p>
              
              <div className='border-2 border-dashed border-slate-300 rounded-xl p-8 text-center bg-slate-50 hover:bg-slate-100 transition-colors relative'>
                <input 
                  type="file" 
                  multiple 
                  className='absolute inset-0 w-full h-full opacity-0 cursor-pointer'
                  onChange={handleFileChange}
                />
                <UploadCloud className='w-10 h-10 text-slate-400 mx-auto mb-3'/>
                <p className='font-medium text-slate-700'>Drop resumes here or Browse files</p>
                <p className='text-xs text-slate-500 mt-1'>PDF / DOCX / TXT</p>
              </div>

              {files.length > 0 && (
                <div className='mt-6 border-t pt-4'>
                  <div className='flex justify-between items-center mb-3'>
                    <h3 className='font-bold text-slate-700'>Selected Files</h3>
                    <span className='text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded'>{files.length} resumes</span>
                  </div>
                  <ul className='space-y-2 mb-6 max-h-48 overflow-y-auto'>
                    {files.map((f, i) => (
                      <li key={i} className='flex items-center gap-2 text-sm text-slate-600 bg-slate-50 p-2 rounded border'>
                        <CheckCircle2 className='w-4 h-4 text-green-500'/> {f.name}
                      </li>
                    ))}
                  </ul>
                  <div className='flex gap-3'>
                    <button onClick={() => setFiles([])} className='px-4 py-2 text-sm text-red-600 font-bold border border-red-200 rounded hover:bg-red-50'>REMOVE ALL</button>
                    <button onClick={handleAnalyze} disabled={!selectedJob} className='flex-1 bg-blue-600 text-white font-bold px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50'>
                      ANALYZE {files.length} RESUMES
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {status === 'processing' && (
            <div className='bg-white p-12 rounded-xl border border-slate-200 shadow-sm text-center'>
              <Loader2 className='w-12 h-12 text-blue-600 animate-spin mx-auto mb-4'/>
              <h2 className='text-xl font-bold text-slate-800 mb-2'>{progress.step}</h2>
              <p className='text-slate-500'>Candidate {progress.current} of {progress.total}</p>
              <div className='w-full max-w-md mx-auto bg-slate-100 rounded-full h-2 mt-6'>
                <div className='bg-blue-600 h-2 rounded-full transition-all duration-300' style={{width: `${(progress.current/progress.total)*100}%`}}></div>
              </div>
            </div>
          )}

          {status === 'done' && (
            <div className='bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden'>
              <div className='p-6 border-b flex justify-between items-center bg-slate-50'>
                <div>
                  <h2 className='text-xl font-bold text-slate-800'>Screening Results</h2>
                  <p className='text-sm text-slate-500'>Job: {activeJobName} | {results.length} processed</p>
                </div>
                <button onClick={() => {setStatus('idle'); setFiles([]);}} className='text-sm text-blue-600 font-bold hover:underline'>New Batch</button>
              </div>
              <div className='overflow-x-auto'>
                <table className='w-full text-left'>
                  <thead className='bg-slate-50 text-xs uppercase text-slate-500 border-b'>
                    <tr>
                      <th className='p-4'>Rank</th>
                      <th className='p-4'>Candidate</th>
                      <th className='p-4 text-center'>Current Fit</th>
                      <th className='p-4 text-center'>Potential Fit</th>
                      <th className='p-4'>Top Gap</th>
                      <th className='p-4'></th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.map((r, idx) => (
                      <tr key={r.candidate_id} className='border-b hover:bg-slate-50 transition-colors'>
                        <td className='p-4 text-center font-bold text-slate-400'>#{idx + 1}</td>
                        <td className='p-4 font-medium text-slate-800'>{r.name}</td>
                        <td className='p-4 text-center font-bold text-blue-700'>{(r.current_fit * 100).toFixed(0)}%</td>
                        <td className='p-4 text-center font-bold text-indigo-700'>{(r.potential_fit * 100).toFixed(0)}%</td>
                        <td className='p-4 text-sm text-red-500 font-medium'>
                           {r.missing_skills?.[0] || 'None'}
                        </td>
                        <td className='p-4 text-right'>
                          <button onClick={() => navigate(`/candidates/${r.candidate_id}?job_id=${r.job_id}`)} className='text-sm font-bold text-blue-600 hover:text-blue-800 flex items-center justify-end gap-1'>
                            Detail <ChevronRight className='w-4 h-4'/>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
