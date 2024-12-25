from datetime import datetime

def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def get_timestamp() -> str:
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

