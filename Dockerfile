# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar el código
COPY bot.py /app/

# Instalar dependencias
RUN pip install requests

# Definir variables de entorno
ENV TELEGRAM_TOKEN="8330161799:AAG7-p_upiOA2eTuKig1TkkWvg5lmTlPoA8"
ENV KICK_CHANNEL="Allyssxn"
ENV CHECK_INTERVAL=30

# Ejecutar el bot
CMD ["python", "bot.py"]
