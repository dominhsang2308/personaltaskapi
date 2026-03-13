from datetime import datetime
import uuid

def format_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def generate_slug(text: str) -> str:
    return text.lower().replace(" ", "-")

def get_now():
    return datetime.utcnow()
