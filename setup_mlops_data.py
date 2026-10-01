import os
import pandas as pd
import json

# Define directories
dirs = [
    'data/source',
    'data/training',
    'data/inference_demo',
    'data/monitoring'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. Source: O*NET Subset
onet_data = {
    'occupation': ['Software Developers', 'Data Scientists', 'Machine Learning Engineers'],
    'skills': ['Programming', 'Mathematics', 'Complex Problem Solving'],
    'technology_skills': ['Python', 'SQL', 'TensorFlow']
}
pd.DataFrame(onet_data).to_csv('data/source/onet_subset_v31.csv', index=False)

# 2. Training Data V1
def generate_training_data(n, semantic_base, skill_base, evidence_base, exp_thresh, label_logic):
    data = []
    for i in range(n):
        sem = semantic_base + (0.3 * (i/n))
        sk = skill_base + (0.4 * (i/n))
        ev = evidence_base + (0.3 * (i/n))
        exp = 1.0 if i > exp_thresh else 0.5
        trans = 0.5 + (0.5 * (i/n))
        label = label_logic(sem, sk, ev)
        data.append([f'c_{i}', f'j_{i%5}', sem, sk, ev, exp, trans, label])
    return pd.DataFrame(data, columns=['candidate_id', 'job_id', 'semantic_score', 'skill_score', 'evidence_score', 'experience_score', 'transferability_score', 'label'])

df_v1 = generate_training_data(150, 0.4, 0.4, 0.4, 50, lambda s,k,e: 1 if (s+k+e)>1.8 else 0)
df_v1.to_csv('data/training/candidate_job_pairs_v1.csv', index=False)

# 3. Training Data V2 (Demo for retraining)
df_v2 = generate_training_data(150, 0.2, 0.3, 0.3, 70, lambda s,k,e: 1 if (s+k+e)>1.4 else 0) # Different distribution
df_v2.to_csv('data/training/candidate_job_pairs_v2_demo.csv', index=False)

# 4. Monitoring Data (Drift)
df_v1[['semantic_score', 'skill_score', 'evidence_score']].to_csv('data/monitoring/reference_jobs.csv', index=False)
df_v2[['semantic_score', 'skill_score', 'evidence_score']].to_csv('data/monitoring/current_jobs_drift_demo.csv', index=False)

# 5. Inference Demo (Recruiter uploads)
with open('data/inference_demo/job_ml_engineer.txt', 'w') as f:
    f.write("Job: ML Engineer\nSkills: Python, TensorFlow, Kubernetes, AWS\nExperience: 3 years")
with open('data/inference_demo/resume_01.txt', 'w') as f:
    f.write("Jane Doe\nExperience: 4 years\nSkills: Python, AWS, Docker, CI/CD\nProjects: Built models with Python.")
with open('data/inference_demo/resume_02.txt', 'w') as f:
    f.write("John Smith\nExperience: 2 years\nSkills: SQL, Tableau\nProjects: Dashboard creation.")
with open('data/inference_demo/resume_03.txt', 'w') as f:
    f.write("Alice Dev\nExperience: 5 years\nSkills: Python, Kubernetes, TensorFlow, AWS, PyTorch\nProjects: Deployed Kubernetes clusters for MLflow tracking and trained TensorFlow models on AWS.")

print("Data structures generated.")
