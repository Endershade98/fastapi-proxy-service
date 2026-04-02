FROM python:3.12-slim

WORKDIR /app

# Copia requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il progetto
COPY . .

# Espone porta
EXPOSE 8000

# Avvio server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]