import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Briefcase, ArrowRight, Loader2, Plus, UploadCloud } from 'lucide-react';
import api from '../api';

export default function Jobs() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [title, setTitle] = useState('');
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [createLoading, setCreateLoading] = useState(false);
  const navigate = useNavigate();

  const loadJobs = () => {
    setLoading(true);
    api.get('/api/jobs').then(res => setJobs(res.data)).catch(console.error).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadJobs();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !jdFile) return;
    setCreateLoading(true);
    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('file', jdFile);
      await api.post('/api/jobs/upload', formData);
      setShowCreate(false);
      setTitle('');
      setJdFile(null);
      loadJobs();
    } catch (e) {
      console.error(e);
      alert('Failed to create job');
    } finally {
      setCreateLoading(false);
    }
  };

  return (
    <div className='p-8 max-w-6xl mx-auto'>
      <div className='flex justify-between items-center mb-8 border-b pb-4'>
        <div>
          <h1 className='text-3xl font-bold text-slate-800'>Active Jobs</h1>
          <p className='text-slate-500 mt-1'>Manage requisitions and screening batches.</p>
        </div>
        <button onClick={() => setShowCreate(!showCreate)} className='bg-slate-800 text-white px-4 py-2 rounded font-bold flex items-center gap-2 hover:bg-slate-700'>
          <Plus className='w-4 h-4'/> CREATE JOB
        </button>
      </div>

      {showCreate && (
        <div className='bg-white p-6 rounded-xl border border-slate-200 shadow-sm mb-8'>
          <h2 className='text-xl font-bold text-slate-800 mb-4'>Create New Job</h2>
          <form onSubmit={handleCreate} className='space-y-4 max-w-2xl'>
            <div>
              <label className='block text-sm font-bold text-slate-700 mb-1'>Job Title</label>
              <input type="text" value={title} onChange={e => setTitle(e.target.value)} required className='w-full px-3 py-2 border rounded outline-none focus:border-blue-500' placeholder='e.g. Senior Data Engineer'/>
            </div>
            <div>
              <label className='block text-sm font-bold text-slate-700 mb-1'>Job Description File (PDF/TXT/DOCX)</label>
              <input type="file" required onChange={e => e.target.files && setJdFile(e.target.files[0])} className='w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'/>
            </div>
            <button type="submit" disabled={createLoading || !title || !jdFile} className='bg-blue-600 text-white px-4 py-2 rounded font-bold hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2'>
              {createLoading ? <Loader2 className='w-4 h-4 animate-spin'/> : <UploadCloud className='w-4 h-4'/>}
              CREATE & ANALYZE JOB
            </button>
          </form>
        </div>
      )}
      
      {loading ? (
        <div className='flex justify-center p-12'><Loader2 className='w-8 h-8 animate-spin text-blue-500'/></div>
      ) : jobs.length === 0 ? (
        <div className='bg-slate-50 p-12 text-center rounded-xl border border-dashed border-slate-300'>
          <Briefcase className='w-12 h-12 text-slate-300 mx-auto mb-4'/>
          <h2 className='text-xl font-bold text-slate-700 mb-2'>No active jobs</h2>
          <p className='text-slate-500 mb-6'>Load the demo workspace from the sidebar or create your first job.</p>
        </div>
      ) : (
        <div className='grid gap-4'>
          {jobs.map(j => (
            <div key={j.id} className='bg-white p-6 rounded-xl border border-slate-200 flex justify-between items-center hover:shadow-md transition-shadow'>
              <div>
                <div className='flex items-center gap-3 mb-1'>
                  <h2 className='text-xl font-bold text-slate-800'>{j.title}</h2>
                  <span className='bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-bold border border-green-200'>ACTIVE</span>
                </div>
                <p className='text-sm text-slate-500 mb-3'>ID: <span className='font-mono text-xs'>{j.id}</span></p>
                <div className='flex gap-2 flex-wrap max-w-2xl'>
                  {j.skills_list.map((s: string) => <span key={s} className='text-xs font-bold bg-slate-100 text-slate-600 px-2 py-1 rounded border border-slate-200'>{s}</span>)}
                </div>
              </div>
              <div className='flex gap-3'>
                <button onClick={() => navigate('/screening')} className='flex items-center gap-2 bg-blue-50 text-blue-700 border border-blue-200 px-4 py-2 rounded font-bold hover:bg-blue-100 transition-colors'>
                  SCREEN CANDIDATES <ArrowRight className='w-4 h-4'/>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
