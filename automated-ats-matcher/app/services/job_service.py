import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

class JobService:
    def __init__(self, evaluation):
        self.evaluation = evaluation
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.jobs, self.lock = {}, threading.Lock()

    def submit(self, docs, jd):
        job_id = str(uuid.uuid4())
        with self.lock:
            self.jobs[job_id] = {"job_id": job_id, "status": "queued"}
        future = self.executor.submit(self.evaluation.evaluate_batch, docs, jd)

        def done(f):
            try:
                value = {"job_id": job_id, "status": "completed", "results": f.result()}
            except Exception as e:
                value = {"job_id": job_id, "status": "failed", "error": str(e)}
            with self.lock:
                self.jobs[job_id] = value
        future.add_done_callback(done)
        return job_id

    def get(self, job_id):
        with self.lock:
            return self.jobs.get(job_id)
