import time
import requests
import concurrent.futures

url = "http://localhost:8000/api/match?candidate_id=cand_1&job_id=job_1"

def fetch():
    start = time.time()
    try:
        r = requests.post(url)
        return r.status_code, time.time() - start
    except Exception as e:
        return 500, time.time() - start

def run_load_test():
    print("Starting lightweight load benchmark for TalentLens...")
    requests_count = 50
    concurrency = 5
    
    successes = 0
    failures = 0
    latencies = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(fetch) for _ in range(requests_count)]
        for future in concurrent.futures.as_completed(futures):
            status, latency = future.result()
            if status == 200:
                successes += 1
                latencies.append(latency)
            else:
                failures += 1
                
    if not latencies:
        print("All requests failed. Make sure the backend is running.")
        return
        
    latencies.sort()
    avg_latency = sum(latencies) / len(latencies)
    p50 = latencies[int(len(latencies) * 0.5)]
    p95 = latencies[int(len(latencies) * 0.95)]
    
    print("\n--- LOAD TEST RESULTS ---")
    print(f"Request count: {requests_count}")
    print(f"Concurrency: {concurrency}")
    print(f"Average latency: {avg_latency:.3f}s")
    print(f"P50 latency: {p50:.3f}s")
    print(f"P95 latency: {p95:.3f}s")
    print(f"Failure rate: {(failures / requests_count) * 100:.1f}%")
    print("\nNote: This benchmark reflects the tested local environment and is not a production capacity guarantee.")
    
    with open("docs/TEST_REPORT.md", "w") as f:
        f.write("# TEST REPORT\n\n")
        f.write("## Lightweight Load Benchmark\n")
        f.write(f"- **Request count**: {requests_count}\n")
        f.write(f"- **Concurrency**: {concurrency}\n")
        f.write(f"- **Average latency**: {avg_latency:.3f}s\n")
        f.write(f"- **P50 latency**: {p50:.3f}s\n")
        f.write(f"- **P95 latency**: {p95:.3f}s\n")
        f.write(f"- **Failure rate**: {(failures / requests_count) * 100:.1f}%\n\n")
        f.write("> This benchmark reflects the tested local environment and is not a production capacity guarantee.\n")

if __name__ == "__main__":
    run_load_test()
