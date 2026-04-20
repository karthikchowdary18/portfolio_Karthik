import json
import os
import re
import sqlite3
from pathlib import Path

from app.database.models import PROJECT_SEED_DATA
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

BASE_DIR = Path(__file__).resolve().parent


def _resolve_db_path() -> Path:
    configured_path = os.getenv("PORTFOLIO_DB_PATH", "").strip()

    if not configured_path:
        return BASE_DIR / "portfolio.db"

    path = Path(configured_path).expanduser()

    if not path.is_absolute():
        path = BASE_DIR / path

    return path


DB_PATH = _resolve_db_path()
MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}
FEATURED_PROJECT_TIEBREAK = {
    "Heavy-Transport Route Planning Platform": 0,
    "ElDrive - Autonomous Shuttle for Elderly Users in Bavarian Region": 1,
    "Autonomous Shuttle HMI Suite": 2,
    "Landmark-Based Autonomous Navigation": 3,
    "QR-Based User Authentication System": 4,
    "Real-Time Object Detection on Model Car": 5,
    "Glass Manufacturing Analytics and AI Chatbot": 6,
}


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_en TEXT NOT NULL,
                title_de TEXT NOT NULL,
                summary_en TEXT NOT NULL,
                summary_de TEXT NOT NULL,
                impact_en TEXT NOT NULL,
                impact_de TEXT NOT NULL,
                tech_stack TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                category TEXT NOT NULL,
                featured INTEGER NOT NULL DEFAULT 0,
                live_url TEXT NOT NULL DEFAULT '',
                repo_url TEXT NOT NULL DEFAULT ''
            )
            """
        )

        project_count = connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0]

        if project_count == 0:
            connection.executemany(
                """
                INSERT INTO projects (
                    title_en,
                    title_de,
                    summary_en,
                    summary_de,
                    impact_en,
                    impact_de,
                    tech_stack,
                    timeframe,
                    category,
                    featured,
                    live_url,
                    repo_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        project["title_en"],
                        project["title_de"],
                        project["summary_en"],
                        project["summary_de"],
                        project["impact_en"],
                        project["impact_de"],
                        json.dumps(project["tech_stack"]),
                        project["timeframe"],
                        project["category"],
                        int(project["featured"]),
                        project["live_url"],
                        project["repo_url"],
                    )
                    for project in PROJECT_SEED_DATA
                ],
            )


def count_projects() -> int:
    with get_connection() as connection:
        return connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0]


def _row_to_project(row: sqlite3.Row) -> Project:
    payload = dict(row)
    payload["tech_stack"] = json.loads(payload["tech_stack"])
    payload["featured"] = bool(payload["featured"])
    return Project(**payload)


def _parse_time_token(token: str, *, period_end: bool) -> tuple[int, int]:
    normalized = token.strip().lower()

    if not normalized:
        return (0, 12 if period_end else 1)

    if normalized.isdigit():
        year = int(normalized)
        return (year, 12 if period_end else 1)

    parts = normalized.split()

    if len(parts) >= 2 and parts[1].isdigit():
        month = MONTHS.get(parts[0][:3])

        if month is not None:
            return (int(parts[1]), month)

    return (0, 12 if period_end else 1)


def _parse_timeframe(timeframe: str) -> tuple[bool, tuple[int, int], tuple[int, int]]:
    normalized = timeframe.strip().replace("–", "-")
    parts = re.split(r"\s+\bto\b\s+|\s*-\s*", normalized, maxsplit=1, flags=re.IGNORECASE)

    start_token = parts[0].strip() if parts else ""
    end_token = parts[1].strip() if len(parts) > 1 else start_token
    is_present = end_token.lower() == "present"

    start_date = _parse_time_token(start_token, period_end=False)
    end_date = (9999, 12) if is_present else _parse_time_token(end_token, period_end=True)

    return is_present, start_date, end_date


def _project_sort_key(project: Project) -> tuple[int, int, int, int, int, int, int]:
    is_present, start_date, end_date = _parse_timeframe(project.timeframe)
    tie_break = FEATURED_PROJECT_TIEBREAK.get(
        project.title_en,
        len(FEATURED_PROJECT_TIEBREAK) + project.id,
    )

    return (
        0 if is_present else 1,
        -end_date[0],
        -end_date[1],
        tie_break,
        -start_date[0],
        -start_date[1],
        project.id,
    )


def list_projects(featured_only: bool = False) -> list[Project]:
    query = "SELECT * FROM projects"
    parameters: tuple[object, ...] = ()

    if featured_only:
        query += " WHERE featured = ?"
        parameters = (1,)

    query += " ORDER BY featured DESC, id ASC"

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()

    projects = [_row_to_project(row) for row in rows]

    if featured_only:
        return sorted(projects, key=_project_sort_key)

    featured_projects = [project for project in projects if project.featured]
    other_projects = [project for project in projects if not project.featured]

    return sorted(featured_projects, key=_project_sort_key) + other_projects


def get_project(project_id: int) -> Project | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_project(row)


def create_project(payload: ProjectCreate) -> Project:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO projects (
                title_en,
                title_de,
                summary_en,
                summary_de,
                impact_en,
                impact_de,
                tech_stack,
                timeframe,
                category,
                featured,
                live_url,
                repo_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.title_en,
                payload.title_de,
                payload.summary_en,
                payload.summary_de,
                payload.impact_en,
                payload.impact_de,
                json.dumps(payload.tech_stack),
                payload.timeframe,
                payload.category,
                int(payload.featured),
                payload.live_url,
                payload.repo_url,
            ),
        )
        project_id = cursor.lastrowid

    return get_project(project_id)


def update_project(project_id: int, payload: ProjectUpdate) -> Project | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE projects
            SET
                title_en = ?,
                title_de = ?,
                summary_en = ?,
                summary_de = ?,
                impact_en = ?,
                impact_de = ?,
                tech_stack = ?,
                timeframe = ?,
                category = ?,
                featured = ?,
                live_url = ?,
                repo_url = ?
            WHERE id = ?
            """,
            (
                payload.title_en,
                payload.title_de,
                payload.summary_en,
                payload.summary_de,
                payload.impact_en,
                payload.impact_de,
                json.dumps(payload.tech_stack),
                payload.timeframe,
                payload.category,
                int(payload.featured),
                payload.live_url,
                payload.repo_url,
                project_id,
            ),
        )

    if cursor.rowcount == 0:
        return None

    return get_project(project_id)


def delete_project(project_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM projects WHERE id = ?",
            (project_id,),
        )

    return cursor.rowcount > 0
