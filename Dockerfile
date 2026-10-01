FROM python:3.9-slim
WORKDIR /app
COPY src/ ./src/
CMD ["python", "-u", "src/edge_agent.py"]
