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

This project is prepared for a Docker-based Render deploy.

### Important note about SQLite

Render services use an ephemeral filesystem by default, so local SQLite data is lost on redeploy unless you attach a persistent disk. This repo includes `render.yaml` configured for a persistent disk and stores the database at `/var/data/portfolio.db` in production.

### Deploy steps

1. Create a GitHub repository and push this project.
2. In Render, create a new Blueprint or Web Service from that repository.
3. If you use the included `render.yaml`, Render will use:
   - `Dockerfile`
   - region `frankfurt`
   - health check path `/api/health`
   - persistent disk mount `/var/data`
4. Deploy and open the generated `onrender.com` URL.

### If you deploy without Blueprint

Use these settings in Render:

- Runtime: `Docker`
- Dockerfile Path: `./Dockerfile`
- Docker Context: `.`
- Health Check Path: `/api/health`
- Environment Variable: `PORTFOLIO_DB_PATH=/var/data/portfolio.db`
- Persistent Disk Mount Path: `/var/data`

## Notes

- The local development database file is intentionally ignored from Git and Docker builds.
- On first start, the app seeds the database from `app/database/models.py` if the database is empty.
