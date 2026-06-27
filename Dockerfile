FROM python:3.12-slim

# Instalar dependencias del sistema necesarias para compilar librerías LDAP
RUN apt-get update && apt-get install -y \
    gcc \
    libldap2-dev \
    libsasl2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar las versiones estables más recientes de Flask y ldap3
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir flask==3.1.3 ldap3==2.9.1

CMD ["python", "app.py"]