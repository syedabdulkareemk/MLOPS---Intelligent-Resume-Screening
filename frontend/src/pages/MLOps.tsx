import { useState, useEffect } from 'react';
import { Activity, Server, Database, CheckCircle2, XCircle, Play, AlertTriangle, ArrowRight, Loader2, BarChart2, RotateCcw, ArrowUpCircle } from 'lucide-react';
import api from '../api';

export default function MLOps() {
  const [pipelineState, setPipelineState] = useState<any>(null);
  const [driftState, setDriftState] = useState<any>(null);
  const [deployStatus, setDeployStatus] = useState<any>({ champion_version: null, challenger_version: null });
  const [loading, setLoading] = useState(false);
  const [action, setAction] = useState('');

  useEffect(() => {
    refreshStatus();
  }, []);

  const refreshStatus = () => {
    api.get('/api/mlops/status').then(res => setDeployStatus(res.data)).catch(console.error);
  };

  const runPipeline = async () => {
    setLoading(true);
    setAction('Running Pipeline (V1)...');
    try {
      const res = await api.post('/api/mlops/pipeline');
      setPipelineState(res.data);
      refreshStatus();
    } catch (e) {
      console.error(e);
      alert('Pipeline failed');
    } finally {
      setLoading(false);
      setAction('');
    }
  };

  const runDrift = async () => {
    setLoading(true);
    setAction('Analyzing Reference vs Current Dataset...');
    try {
      const res = await api.post('/api/mlops/drift');
      setDriftState(res.data);
    } catch (e) {
      console.error(e);
      alert('Drift check failed');
    } finally {
      setLoading(false);
      setAction('');
    }
  };

  const runRetrain = async () => {
    setLoading(true);
    setAction('Retraining Candidate Model (V2)...');
    try {
      const res = await api.post('/api/mlops/retrain');
      setPipelineState(res.data);
      refreshStatus();
    } catch (e) {
      console.error(e);
      alert('Retraining failed');
    } finally {
      setLoading(false);
      setAction('');
    }
  };

  const runPromote = async () => {
    setLoading(true);
    setAction('Promoting Challenger to Champion...');
    try {
      await api.post('/api/mlops/promote');
      refreshStatus();
    } catch (e) {
      console.error(e);
      alert('Promotion failed');
    } finally {
      setLoading(false);
      setAction('');
    }
  };

  const runRollback = async () => {
    setLoading(true);
    setAction('Rolling back to V1...');
    try {
      await api.post('/api/mlops/rollback');
      refreshStatus();
    } catch (e) {
      console.error(e);
      alert('Rollback failed');
    } finally {
      setLoading(false);
      setAction('');
    }
  };

  return (
    <div className='p-8 max-w-6xl mx-auto'>
      <div className='mb-8 border-b pb-4'>
        <h1 className='text-3xl font-bold text-slate-800 mb-2'>MLOps Control Center</h1>
        <p className='text-slate-500'>End-to-End Model Lifecycle, Drift Detection, and Promotion Workflow</p>
      </div>
      
      {/* Overview Dashboard */}
      <div className='grid grid-cols-4 gap-6 mb-8'>
        <div className='bg-white p-4 rounded-xl border border-slate-200 shadow-sm'>
          <p className='text-xs font-bold text-slate-400 uppercase mb-1'>Model</p>
          <p className='text-lg font-bold text-slate-800'>TalentLens-Ranker</p>
          <div className='mt-3 space-y-1 text-sm'>
            <div className='flex justify-between'><span className='text-slate-500'>Champion:</span> <span className='font-bold text-green-600'>V{deployStatus.champion_version || 'None'}</span></div>
            <div className='flex justify-between'><span className='text-slate-500'>Challenger:</span> <span className='font-bold text-blue-600'>V{deployStatus.challenger_version || 'None'}</span></div>
          </div>
        </div>
        
        <div className='bg-white p-4 rounded-xl border border-slate-200 shadow-sm'>
          <p className='text-xs font-bold text-slate-400 uppercase mb-1'>Data & Lineage</p>
          <div className='mt-3 space-y-1 text-sm'>
            <div className='flex justify-between'><span className='text-slate-500'>Code Rev:</span> <span className='font-mono bg-slate-100 px-1 rounded'>{deployStatus.git_commit || 'a83f91d'}</span></div>
            <div className='flex justify-between'><span className='text-slate-500'>Training DVC:</span> <span className='font-mono'>v1</span></div>
            <div className='flex justify-between'><span className='text-slate-500'>Reference DVC:</span> <span className='font-mono'>v1</span></div>
          </div>
        </div>

        <div className='bg-white p-4 rounded-xl border border-slate-200 shadow-sm'>
          <p className='text-xs font-bold text-slate-400 uppercase mb-1'>Drift Status</p>
          {driftState ? (
             <div className='mt-2 flex items-center gap-2'>
               {driftState.drift_detected ? <AlertTriangle className='text-amber-500 w-5 h-5'/> : <CheckCircle2 className='text-green-500 w-5 h-5'/>}
               <span className={`font-bold ${driftState.drift_detected ? 'text-amber-600' : 'text-green-600'}`}>
                 {driftState.drift_detected ? 'Detected' : 'Normal'}
               </span>
             </div>
          ) : <p className='text-slate-400 mt-2 text-sm'>Not Run</p>}
        </div>

        <div className='bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-center gap-2'>
           <button onClick={runPipeline} disabled={loading} className='w-full bg-slate-800 text-white px-3 py-2 rounded text-sm font-bold flex justify-center items-center gap-2 hover:bg-slate-700 disabled:opacity-50'>
              RUN TRAINING
           </button>
           <button onClick={runDrift} disabled={loading} className='w-full border border-slate-300 text-slate-700 px-3 py-2 rounded text-sm font-bold flex justify-center items-center hover:bg-slate-50 disabled:opacity-50'>
              RUN DRIFT CHECK
           </button>
        </div>
      </div>

      {loading && (
        <div className='mb-8 p-4 bg-blue-50 text-blue-800 rounded border border-blue-200 flex items-center gap-3 animate-pulse'>
          <Loader2 className='w-5 h-5 animate-spin'/>
          <span className='font-bold'>{action}</span>
        </div>
      )}

      <div className='grid grid-cols-3 gap-8'>
        {/* Left Column - Pipeline Steps */}
        <div className='col-span-1 bg-white p-6 rounded-xl border border-slate-200 shadow-sm'>
          <h2 className='text-lg font-bold mb-4 border-b pb-2'>Pipeline Execution</h2>
          <ul className='space-y-4'>
            {['DATA', 'VALIDATE', 'PREPROCESS', 'FEATURES', 'TRAIN', 'EVALUATE', 'MLFLOW', 'REGISTRY', 'DEPLOY'].map((step, idx) => (
              <li key={step} className='flex items-center gap-3'>
                {pipelineState ? <CheckCircle2 className='w-5 h-5 text-green-500'/> : <div className='w-5 h-5 rounded-full border-2 border-slate-200'/>}
                <span className={`text-sm font-bold ${pipelineState ? 'text-slate-700' : 'text-slate-400'}`}>{step}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Right Column - Registry & Drift */}
        <div className='col-span-2 space-y-8'>
          
          {/* Active Model Run Result */}
          <div className='bg-white p-6 rounded-xl border border-slate-200 shadow-sm'>
            <h2 className='text-lg font-bold mb-4 flex items-center gap-2'><Database className='w-5 h-5 text-blue-600'/> Latest Training Run</h2>
            {pipelineState ? (
              <div className='bg-slate-50 border rounded-lg p-4'>
                <div className='flex justify-between items-start mb-4'>
                  <div>
                    <h3 className='text-xl font-bold text-slate-800'>Version {pipelineState.version.toUpperCase()}</h3>
                    <p className='text-slate-500 text-sm'>Run ID: <span className='font-mono text-xs'>{pipelineState.run_id}</span></p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${pipelineState.status === 'Champion' ? 'bg-green-100 text-green-800 border border-green-200' : 'bg-blue-100 text-blue-800 border border-blue-200'}`}>
                    {pipelineState.status}
                  </span>
                </div>
                <div className='grid grid-cols-3 gap-4 border-t pt-4'>
                  <div><p className='text-xs text-slate-500 uppercase font-bold mb-1'>F1 Score</p><p className='text-xl font-bold'>{(pipelineState.f1_score * 100).toFixed(1)}%</p></div>
                  <div><p className='text-xs text-slate-500 uppercase font-bold mb-1'>Precision</p><p className='text-xl font-bold'>{(pipelineState.precision * 100).toFixed(1)}%</p></div>
                  <div><p className='text-xs text-slate-500 uppercase font-bold mb-1'>Recall</p><p className='text-xl font-bold'>{(pipelineState.recall * 100).toFixed(1)}%</p></div>
                </div>

                {pipelineState.status === 'Challenger' && (
                   <div className='mt-6 pt-4 border-t flex justify-end gap-3'>
                     <button onClick={runPromote} disabled={loading} className='bg-green-600 text-white px-4 py-2 rounded text-sm font-bold flex items-center gap-2 hover:bg-green-700'>
                        <ArrowUpCircle className='w-4 h-4'/> PROMOTE CHALLENGER
                     </button>
                   </div>
                )}
              </div>
            ) : (
              <div className='p-8 text-center text-slate-500 border border-dashed rounded-lg bg-slate-50'>No model trained yet. Run Training pipeline.</div>
            )}
          </div>

          {/* Drift & Monitoring */}
          <div className='bg-white p-6 rounded-xl border border-slate-200 shadow-sm'>
            <h2 className='text-lg font-bold flex items-center gap-2 mb-4'><BarChart2 className='w-5 h-5 text-blue-600'/> Drift Monitoring Alert</h2>
            
            {driftState ? (
              <div className={`p-4 rounded-lg border ${driftState.drift_detected ? 'bg-amber-50 border-amber-200' : 'bg-green-50 border-green-200'}`}>
                <div className='flex items-start gap-3'>
                  {driftState.drift_detected ? <AlertTriangle className='w-6 h-6 text-amber-500 shrink-0 mt-1'/> : <CheckCircle2 className='w-6 h-6 text-green-500 shrink-0 mt-1'/>}
                  <div className='flex-1'>
                    <h3 className={`font-bold ${driftState.drift_detected ? 'text-amber-800' : 'text-green-800'}`}>
                      {driftState.drift_detected ? 'Model Drift Detected!' : 'No Drift Detected'}
                    </h3>
                    <p className={`text-sm mt-1 mb-4 ${driftState.drift_detected ? 'text-amber-700' : 'text-green-700'}`}>
                      Reference Semantic Mean: {driftState.reference_semantic_mean.toFixed(2)}<br/>
                      Current Data Semantic Mean: {driftState.current_semantic_mean.toFixed(2)}<br/>
                      Difference exceeds threshold ({driftState.drift_threshold}).
                    </p>
                    {driftState.drift_detected && (
                      <div className='flex gap-3'>
                        <button onClick={runRetrain} disabled={loading} className='bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded text-sm font-bold flex items-center gap-2'>
                          RETRAIN (CREATE V2) <ArrowRight className='w-4 h-4'/>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className='p-8 text-center text-slate-500 border border-dashed rounded-lg bg-slate-50'>Run a drift check to compare inference inputs against reference.</div>
            )}
          </div>
          
          <div className='flex justify-end'>
            <button onClick={runRollback} disabled={loading} className='flex items-center gap-2 text-sm font-bold text-red-600 hover:text-red-800 px-4 py-2 border border-red-200 rounded-lg hover:bg-red-50 transition-colors'>
               <RotateCcw className='w-4 h-4'/> ROLLBACK TO V1
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}
