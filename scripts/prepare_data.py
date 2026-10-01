import os
import shutil

os.makedirs('data/training', exist_ok=True)
if os.path.exists('data/training/candidate_job_pairs_v1.csv'):
    shutil.copy('data/training/candidate_job_pairs_v1.csv', 'data/training/prepared_v1.csv')
    print("Prepared data.")
else:
    print("No training data found.")
