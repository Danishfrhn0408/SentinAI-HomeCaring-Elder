# Guna Python versi ringan
FROM python:3.11-slim

# Tetapkan folder kerja dalam server
WORKDIR /app

# Copy fail requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua koding korang ke dalam server
COPY . .

# Dedahkan port 8080 (Cloud Run guna port ni)
EXPOSE 8080

# Arahan untuk hidupkan Uvicorn bila server berjalan
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]