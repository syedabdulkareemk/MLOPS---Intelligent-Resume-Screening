import React from 'react';
import { User, CheckCircle2, AlertTriangle, ArrowUpRight } from 'lucide-react';

interface CandidateProps {
  name: string;
  role: string;
  currentFit: number;
  potentialFit: number;
  strongSkills: string[];
  criticalGaps: string[];
  transferableSkills: string[];
}

export const CandidateCard: React.FC<CandidateProps> = ({
  name, role, currentFit, potentialFit, strongSkills, criticalGaps, transferableSkills
}) => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
      <div className="flex justify-between items-start mb-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
            <User className="w-6 h-6 text-slate-600" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">{name}</h3>
            <p className="text-sm text-slate-500">{role}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center gap-2 mb-1 justify-end">
            <span className="text-sm font-medium text-slate-600">Current Fit</span>
            <span className="px-2 py-1 bg-green-100 text-green-700 rounded-md text-sm font-bold">{currentFit}%</span>
          </div>
          <div className="flex items-center gap-2 justify-end">
            <span className="text-sm font-medium text-slate-600">Potential Fit</span>
            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-sm font-bold">{potentialFit}%</span>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-semibold text-slate-700 flex items-center gap-2 mb-2">
            <CheckCircle2 className="w-4 h-4 text-green-500" /> Strong Skills
          </h4>
          <div className="flex flex-wrap gap-2">
            {strongSkills.map(skill => (
              <span key={skill} className="px-2 py-1 bg-slate-100 text-slate-700 text-xs rounded-md">{skill}</span>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="text-sm font-semibold text-slate-700 flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" /> Critical Gaps
          </h4>
          <div className="flex flex-wrap gap-2">
            {criticalGaps.map(skill => (
              <span key={skill} className="px-2 py-1 bg-amber-50 text-amber-700 border border-amber-200 text-xs rounded-md">{skill}</span>
            ))}
          </div>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-slate-700 flex items-center gap-2 mb-2">
            <ArrowUpRight className="w-4 h-4 text-purple-500" /> Transferable Skills
          </h4>
          <div className="flex flex-wrap gap-2">
            {transferableSkills.map(skill => (
              <span key={skill} className="px-2 py-1 bg-purple-50 text-purple-700 border border-purple-200 text-xs rounded-md">{skill}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
