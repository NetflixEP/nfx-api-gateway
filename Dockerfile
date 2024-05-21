FROM python:3.11-slim

WORKDIR /app/jwt_checker/

RUN apt-get update && apt-get install -y nginx procps python-is-python3 python3-venv

COPY ./jwt_checker.py /app/jwt_checker/jwt_checker.py

RUN python3 -m venv .venv
RUN . .venv/bin/activate && pip install flask pyjwt requests

RUN chmod +x /app/jwt_checker/jwt_checker.py
RUN chmod +x /app/jwt_checker/.venv/bin/python

EXPOSE 5000

CMD ["/app/jwt_checker/.venv/bin/python", "/app/jwt_checker/jwt_checker.py"]