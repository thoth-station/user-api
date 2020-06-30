"""Gunicorn configuration."""

accesslog = "-"

# Handcrafted to be JSON compatible:
#  https://docs.gunicorn.org/en/stable/settings.html#access-log-format
access_log_format = '{"remote": "%(h)s", "date": "%(t)s", "status": "%(s)s", "response_length": %(B)s, "referer": "%(f)s", "user_agent": "%(a)s", "request_method": "%(m)s", "url_path": "%(U)s", "protocol": "%(H)s", "request_time": %(T)s}'  # noqa: E501
