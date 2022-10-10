# syntax = edrevo/dockerfile-plus
INCLUDE+ base.Dockerfile

CMD ['gunicorn', 'backend_sl.wsgi:application', '--bind', '0.0.0.0:6123']