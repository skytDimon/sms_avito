# Avito Message Forwarder

Программа для автоматической пересылки сообщений с Avito на email и в Telegram бота.

## Возможности

- ✅ Получение сообщений с Avito через API или веб-скрапинг
- ✅ Отправка уведомлений на email (dimdimich112008@gmail.com)
- ✅ Отправка уведомлений в Telegram бота (@business_assistant1_bot)
- ✅ Красивое форматирование сообщений
- ✅ Логирование всех операций
- ✅ Режим постоянной работы с настраиваемым интервалом проверки

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте файл `config.json` (см. раздел "Настройка")

3. Запустите программу:
```bash
python main.py
```

## Настройка

### 1. Email настройки

Для отправки на Gmail нужно:

1. Включить двухфакторную аутентификацию в Google аккаунте
2. Создать пароль приложения:
   - Перейти в настройки Google аккаунта
   - Безопасность → Пароли приложений
   - Создать новый пароль для "Почта"
3. Указать данные в `config.json`:

```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "your_email@gmail.com",
        "password": "your_app_password",
        "recipient": "dimdimich112008@gmail.com"
    }
}
```

### 2. Telegram настройки

1. Создайте бота у @BotFather (если еще не создан)
2. Получите токен бота
3. Найдите chat_id:
   - Отправьте сообщение боту @business_assistant1_bot
   - Перейдите по ссылке: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Найдите chat_id в ответе

```json
{
    "telegram": {
        "bot_token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
        "chat_id": "123456789"
    }
}
```

### 3. Avito настройки

#### Вариант 1: Через API (рекомендуется)

1. Получите API ключ в личном кабинете Avito для бизнеса
2. Найдите ваш user_id

```json
{
    "avito": {
        "api_key": "your_avito_api_key",
        "user_id": "your_avito_user_id",
        "method": "api"
    }
}
```

#### Вариант 2: Через веб-скрапинг

```json
{
    "avito": {
        "method": "scraping",
        "username": "your_avito_username",
        "password": "your_avito_password"
    }
}
```

**Внимание:** Для веб-скрапинга нужно установить ChromeDriver.

## Использование

### Однократная проверка
```python
from main import AvitoMessageForwarder
import json

with open('config.json', 'r') as f:
    config = json.load(f)

forwarder = AvitoMessageForwarder(config)
forwarder.process_messages()
```

### Постоянная работа
```bash
python main.py
```

Программа будет проверять новые сообщения каждые 5 минут (по умолчанию).

## Структура проекта

```
sms_avito/
├── main.py              # Основная программа
├── avito_client.py      # Модуль для работы с Avito
├── config.json          # Конфигурация
├── requirements.txt     # Зависимости
├── README.md           # Документация
└── avito_forwarder.log # Логи программы
```

## Логирование

Все операции логируются в файл `avito_forwarder.log` и выводятся в консоль.

Уровни логирования:
- `INFO` - Обычные операции
- `WARNING` - Предупреждения
- `ERROR` - Ошибки

## Безопасность

⚠️ **Важно:**
- Не добавляйте `config.json` в систему контроля версий
- Используйте пароли приложений для email
- Храните токены в безопасном месте

## Поддержка

При возникновении проблем проверьте:
1. Правильность настроек в `config.json`
2. Логи в файле `avito_forwarder.log`
3. Доступность интернет-соединения
4. Валидность API ключей и токенов

## Примеры сообщений

### Email
```
Тема: Новое сообщение с Avito - 2024-01-15 10:30:00

Новое сообщение с Avito

Время: 2024-01-15 10:30:00
От: Покупатель123
Объявление: Продам iPhone 15

Сообщение:
Здравствуйте! Интересует ваш товар. Можно встретиться сегодня?
```

### Telegram
```
🔔 Новое сообщение с Avito

📅 Время: 2024-01-15 10:30:00
👤 От: Покупатель123
📋 Объявление: Продам iPhone 15

💬 Сообщение:
Здравствуйте! Интересует ваш товар. Можно встретиться сегодня?
```
# sms_avito
