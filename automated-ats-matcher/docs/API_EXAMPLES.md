# API examples

## Health

```bash
curl http://127.0.0.1:5000/api/health
```

## Upload

```bash
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "files=@data/resumes/resume_01.txt"
```

## Single evaluation

Use a multipart request with `resume` and `job_description`.

## Batch

Use repeated `resumes` fields and one `job_description` field. ZIP archives are also accepted.
