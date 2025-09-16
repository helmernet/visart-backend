from datetime import datetime, timezone


def to_iso(dt: datetime) -> str:
    """Convierte un datetime a string ISO 8601 con zona horaria UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()