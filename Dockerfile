# Usar imagen base de Python con soporte para Chrome
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para Chrome y Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias adicionales de Selenium
#RUN pip install selenium webdriver-manager

# Copiar todos los archivos del proyecto
COPY . .

# Crear directorio para capturas
RUN mkdir -p /app/capturas

# Establecer variables de entorno
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# Exponer puerto de la API
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["fastapi", "run"]
