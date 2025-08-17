# Используем официальный Python образ
FROM python:3.11-slim

# Метаданные
LABEL maintainer="Avito Message Forwarder"
LABEL description="Telegram message forwarder for Avito notifications"

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем временную зону
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app

# Копируем исходный код приложения
COPY --chown=appuser:appuser . .

# Переключаемся на непривилегированного пользователя
USER appuser

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Проверка здоровья контейнера
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('https://api.telegram.org')" || exit 1

# Том для логов
VOLUME ["/app/logs"]

# Команда для запуска приложения
CMD ["python3", "main.py"]
