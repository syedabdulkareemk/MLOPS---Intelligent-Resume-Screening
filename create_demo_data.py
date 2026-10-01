import os
import pandas as pd
import json

os.makedirs('data/demo', exist_ok=True)
os.makedirs('data/mlops', exist_ok=True)

# 1. MLOps Demo Data (Small dataset for the Logistic Regression model)
# We want features: semantic, canonical_skill, evidence, experience, label (0 or 1)
data = []
for i in range(150):
    semantic = 0.5 + (0.5 * (i/150))
    skill = 0.4 + (0.6 * (i/150))
    evidence = 0.5 + (0.5 * (i/150))
    exp = 1.0 if i > 50 else 0.5
    # Add some noise
    semantic += (i%10)/100
    label = 1 if (semantic + skill + evidence) > 2.0 else 0
    data.append([semantic, skill, evidence, exp, label])

df = pd.DataFrame(data, columns=['semantic', 'canonical_skill', 'evidence', 'experience', 'label'])
df.to_csv('data/mlops/reference_data.csv', index=False)

# Drift dataset (Current Data) -> Different distribution
drift_data = []
for i in range(150):
    semantic = 0.3 + (0.4 * (i/150)) # Lower semantic match on average (drift!)
    skill = 0.2 + (0.5 * (i/150))
    evidence = 0.4 + (0.4 * (i/150))
    exp = 1.0 if i > 80 else 0.5
    label = 1 if (semantic + skill + evidence) > 1.8 else 0
    drift_data.append([semantic, skill, evidence, exp, label])

drift_df = pd.DataFrame(drift_data, columns=['semantic', 'canonical_skill', 'evidence', 'experience', 'label'])
drift_df.to_csv('data/mlops/current_data.csv', index=False)


# 2. Demo JDs and Resumes for the UI testing
with open('data/demo/job_mlops_engineer.txt', 'w') as f:
    f.write("""Job Title: Senior MLOps Engineer
We are seeking a Senior MLOps Engineer to deploy and monitor ML models.
Requirements:
- 4+ years of experience
- Strong Python programming
- Experience with Kubernetes and Docker
- Familiarity with CI/CD pipelines
- MLflow or DVC experience is a plus
""")

with open('data/demo/candidate_01_resume.txt', 'w') as f:
    f.write("""Jane Doe
Experienced Backend and ML Engineer
Skills: Python, AWS, Docker, Terraform, CI/CD, SQL
Experience: 4 years working as a Data Engineer building scalable pipelines.
Projects: Built an automated training pipeline in AWS using Python.
""")

print("Demo data generated successfully.")
