from django.db import connections


def db_connections(connection_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            conn = connections[connection_name]
            cursor = conn.cursor()
            result = func(*args, **kwargs, cursor=cursor)
            cursor.close()
            conn.close()
            return result
        return wrapper
    return decorator
