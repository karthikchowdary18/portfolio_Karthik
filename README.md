# Portfolio Website

A bilingual FastAPI portfolio for Karthik Chowdary Nunna focused on autonomous mobility, robotics, and software systems.

## Stack

- FastAPI
- Jinja2 templates
- Vanilla JavaScript
- Custom CSS
- SQLite
- Docker
- Render

## Local Run

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Project Structure

```text
portfolio-website/
|- app/
|  |- main.py
|  |- routers/
|  |- templates/
|  |- static/
|  |- database/
|  \- schemas/
|- requirements.txt
|- Dockerfile
|- render.yaml
\- README.md
```

## API Routes

- `GET /api/health`
- `GET /api/projects`
- `POST /api/projects`
- `PUT /api/projects/{project_id}`
- `DELETE /api/projects/{project_id}`

## Render Deployment

This project is prepared for a Docker-based Render free web service.

### Important note about SQLite on the free tier

Render free web services use an ephemeral filesystem. That means local SQLite changes are lost when the service redeploys, restarts, or spins down. This portfolio will still work because it automatically recreates and reseeds the database from `app/database/models.py` when the database is empty.

### Deploy steps

1. Push this project to GitHub.
2. In Render, create a new Blueprint or Web Service from that repository.
3. If you use the included `render.yaml`, Render will use:
   - free web service plan
   - `Dockerfile`
   - region `frankfurt`
   - health check path `/api/health`
4. Deploy and open the generated `onrender.com` URL.

### If you deploy without Blueprint

Use these settings in Render:

- Runtime: `Docker`
- Plan: `Free`
- Dockerfile Path: `./Dockerfile`
- Docker Context: `.`
- Health Check Path: `/api/health`

## Notes

- The local development database file is intentionally ignored from Git and Docker builds.
- On first start, the app seeds the database from `app/database/models.py` if the database is empty.
