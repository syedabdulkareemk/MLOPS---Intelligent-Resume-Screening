import os

res_dir = "data/demo/resumes"
jobs_dir = "data/demo/jobs"

os.makedirs(res_dir, exist_ok=True)
os.makedirs(jobs_dir, exist_ok=True)

with open(f"{jobs_dir}/mlops_engineer.txt", "w") as f:
    f.write("Job: Senior MLOps Engineer\nRequirements: 5+ years experience. Must have Python, Docker, Kubernetes, AWS, and CI/CD.")

with open(f"{jobs_dir}/ml_engineer.txt", "w") as f:
    f.write("Job: ML Engineer\nRequirements: Python, PyTorch, TensorFlow, SQL.")

resumes = {
    "candidate_01_arun.txt": "Arun\nExperience: 5 years\nSkills: Python, Docker, Kubernetes, AWS, CI/CD, Terraform\nProjects: Built scalable MLOps pipelines.",
    "candidate_02_priya.txt": "Priya\nExperience: 4 years\nSkills: Python, TensorFlow, PyTorch, SQL\nProjects: Trained deep learning models for NLP.",
    "candidate_03_rahul.txt": "Rahul\nExperience: 6 years\nSkills: Docker, Linux, AWS, Terraform, CI/CD\nProjects: Managed infrastructure and deployment.",
    "candidate_04_karthik.txt": "Karthik\nExperience: 3 years\nSkills: SQL, Python, Spark, Hadoop\nProjects: Big data ETL pipelines.",
    "candidate_05_meena.txt": "Meena\nExperience: 1 year\nSkills: Python, HTML, CSS, JavaScript\nProjects: Built a small web application."
}

for name, content in resumes.items():
    with open(f"{res_dir}/{name}", "w") as f:
        f.write(content)

print("Demo resumes created.")
