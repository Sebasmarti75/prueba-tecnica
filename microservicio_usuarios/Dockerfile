FROM python:3.10
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y iputils-ping && ping -c 4 google.com
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]