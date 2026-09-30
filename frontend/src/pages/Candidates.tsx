import { CandidateCard } from '../components/CandidateCard';

export default function Candidates() {
  const mockCandidates = [
    {
      id: 1,
      name: "Alice Chen",
      role: "Senior Data Scientist",
      currentFit: 92,
      potentialFit: 98,
      strongSkills: ["Python", "PyTorch", "Machine Learning", "SQL"],
      criticalGaps: ["Apache Kafka"],
      transferableSkills: ["Data Engineering", "MLOps"]
    },
    {
      id: 2,
      name: "Bob Smith",
      role: "Machine Learning Engineer",
      currentFit: 78,
      potentialFit: 85,
      strongSkills: ["TensorFlow", "AWS", "Python"],
      criticalGaps: ["System Design", "Kubernetes"],
      transferableSkills: ["Backend Development"]
    }
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Candidates</h1>
        <p className="text-slate-500 mt-2">AI-driven analysis of candidate profiles and skill matching.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {mockCandidates.map(candidate => (
          <CandidateCard key={candidate.id} {...candidate} />
        ))}
      </div>
    </div>
  );
}
