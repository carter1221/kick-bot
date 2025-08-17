# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar el código
COPY bot.py /app/

# Instalar dependencias
RUN pip install requests

# Definir variables de entorno
ENV TELEGRAM_TOKEN=""
ENV KICK_CHANNEL=""
ENV CHECK_INTERVAL=10

# Ejecutar el bot
CMD ["python", "bot.py"]


