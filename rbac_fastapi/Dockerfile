# fastapi/Dockerfile
FROM python:3.9

WORKDIR /rbac_fastapi

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "sleep 30 && uvicorn main:app --host 0.0.0.0 --port 80 --reload"]