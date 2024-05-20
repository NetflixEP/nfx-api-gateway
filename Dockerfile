FROM nginx:latest

RUN apt-get update && apt-get install python -y
RUN apt-get install pip -y && pip install flask && pip install jwt && pip install requests

COPY ./jwt_checker.py ~/jwt_checker/jwt_checker.py

RUN python jwt_checker.py