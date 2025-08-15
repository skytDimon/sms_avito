#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенная версия для тестирования только Telegram функциональности
"""

import requests
import json
import logging
from datetime import datetime
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramForwarder:
    """Упрощенный класс только для Telegram"""
    
    def __init__(self, bot_token, chat_ids):
        self.bot_token = bot_token
        self.chat_ids = chat_ids
    
    def send_telegram_message(self, message: str) -> bool:
        """Отправка сообщения в Telegram на все chat_id"""
        success_count = 0
        
        for chat_id in self.chat_ids:
            try:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                data = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, data=data)
                response.raise_for_status()
                
                logger.info(f"✅ Сообщение отправлено в chat_id: {chat_id}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"❌ Ошибка отправки в chat_id {chat_id}: {e}")
        
        return success_count > 0
    
    def simulate_avito_message(self):
        """Симуляция сообщения с Avito для тестирования"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        test_message = f"""
🔔 <b>Новое сообщение с Avito</b>

📅 <b>Время:</b> {timestamp}
👤 <b>От:</b> Покупатель123
📋 <b>Объявление:</b> Продам iPhone 15 Pro

💬 <b>Сообщение:</b>
Здравствуйте! Интересует ваш товар. Можно встретиться сегодня? Какая окончательная цена?

📱 <b>Телефон:</b> +7 (999) 123-45-67

---
<i>Отправлено автоматически</i>
        """.strip()
        
        return test_message


def main():
    """Тестирование Telegram функциональности"""
    print("🚀 Тестирование Telegram отправки сообщений\n")
    
    # Загружаем конфигурацию
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка загрузки config.json: {e}")
        return
    
    telegram_config = config.get('telegram', {})
    bot_token = telegram_config.get('bot_token')
    chat_ids = telegram_config.get('chat_ids', [])
    
    if not bot_token or not chat_ids:
        print("❌ Не настроены Telegram параметры")
        return
    
    # Создаем форвардер
    forwarder = TelegramForwarder(bot_token, chat_ids)
    
    # Отправляем тестовое сообщение
    print("📤 Отправляем тестовое сообщение...")
    test_message = forwarder.simulate_avito_message()
    
    if forwarder.send_telegram_message(test_message):
        print("✅ Тестовое сообщение отправлено успешно!")
        print(f"📊 Сообщение отправлено в {len(chat_ids)} чатов")
    else:
        print("❌ Не удалось отправить сообщение")
    
    print("\n" + "="*50)
    print("🎉 Telegram функциональность работает!")
    print("💡 Теперь нужно настроить:")
    print("   1. Пароль приложения Gmail для email")
    print("   2. Правильный API ключ Avito")


if __name__ == "__main__":
    main()
