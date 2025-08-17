# Docker Deployment Guide

## Быстрый запуск

### 1. С Docker Compose (рекомендуется)
```bash
# Запуск в фоновом режиме
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 2. С обычным Docker
```bash
# Сборка образа
docker build -t avito-forwarder .

# Запуск контейнера
docker run -d \
  --name avito-forwarder \
  --restart unless-stopped \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/logs:/app/logs \
  -e TZ=Europe/Moscow \
  avito-forwarder

# Просмотр логов
docker logs -f avito-forwarder

# Остановка
docker stop avito-forwarder
docker rm avito-forwarder
```

## Управление контейнером

### Проверка статуса
```bash
# Статус сервисов
docker-compose ps

# Здоровье контейнера
docker inspect --format='{{.State.Health.Status}}' avito-forwarder
```

### Логи и отладка
```bash
# Просмотр логов в реальном времени
docker-compose logs -f avito-forwarder

# Последние 100 строк логов
docker-compose logs --tail=100 avito-forwarder

# Вход в контейнер для отладки
docker-compose exec avito-forwarder /bin/bash
```

### Обновление
```bash
# Пересборка и перезапуск
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Важные моменты

1. **config.json** монтируется как read-only том
2. **Логи** сохраняются в папку `./logs/`
3. **Автоперезапуск** настроен для стабильной работы
4. **Health check** проверяет доступность Telegram API
5. **Временная зона** установлена на Moscow

## Мониторинг

### Проверка работы
```bash
# Быстрая проверка
curl -f http://localhost:8080/health || echo "Service down"

# Проверка через Docker
docker exec avito-forwarder python3 test_config.py
```

### Ротация логов
Логи автоматически ротируются:
- Максимальный размер файла: 10MB
- Количество файлов: 3
- Общий размер: ~30MB
