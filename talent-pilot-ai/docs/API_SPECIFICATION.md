# API Specification

Primary source of truth: interactive OpenAPI at `/docs` when the app is running.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Liveness |
| GET | `/` | No | UI |
| POST | `/api/v1/analyze` | Optional | Analyze resume (saves if signed in) |
| POST | `/api/v1/auth/register` | No | Register |
| POST | `/api/v1/auth/login` | No | Login |
| POST | `/api/v1/auth/logout` | No | Logout |
| GET | `/api/v1/auth/me` | Yes | Current user |
| GET | `/api/v1/history` | Yes | Saved analyses |
| GET | `/api/v1/history/{id}` | Yes | Saved analysis detail |
| GET | `/api/v1/samples/job-description` | No | Sample JD |
| GET | `/api/v1/samples/resume` | No | Sample PDF |

## Error envelope

```json
{
  "success": false,
  "error": { "code": "INVALID_FILE", "message": "..." }
}
```

See also [openapi.yaml](openapi.yaml) (may lag; prefer `/docs`).
