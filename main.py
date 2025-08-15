#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Программа для отправки сообщений с Avito на почту и в Telegram
"""

import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import time
from avito_client import AvitoClient

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('avito_forwarder.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AvitoMessageForwarder:
    """Класс для пересылки сообщений с Avito в Telegram"""
    
    def __init__(self, config: Dict):
        """
        Инициализация с конфигурацией
        
        Args:
            config: Словарь с настройками (telegram, avito)
        """
        self.config = config
        self.telegram_config = config.get('telegram', {})
        self.avito_config = config.get('avito', {})
        
        # Инициализируем клиент Avito
        self.avito_client = AvitoClient(self.avito_config)
        
        # Telegram настройки
        self.bot_token = self.telegram_config.get('bot_token')
        self.chat_ids = self.telegram_config.get('chat_ids', [])
        # Поддержка старого формата с одним chat_id
        if not self.chat_ids and self.telegram_config.get('chat_id'):
            self.chat_ids = [self.telegram_config.get('chat_id')]
        

    
    def send_telegram_message(self, message: str) -> bool:
        """
        Отправка сообщения в Telegram на все настроенные chat_id
        
        Args:
            message: Текст сообщения
            
        Returns:
            bool: Успешность отправки (True если хотя бы одно сообщение отправлено)
        """
        if not self.chat_ids:
            logger.error("Не настроены chat_ids для Telegram")
            return False
            
        success_count = 0
        total_count = len(self.chat_ids)
        
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
                
                logger.info(f"Telegram сообщение отправлено успешно в chat_id: {chat_id}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"Ошибка отправки Telegram сообщения в chat_id {chat_id}: {e}")
        
        if success_count > 0:
            logger.info(f"Telegram сообщения отправлены в {success_count} из {total_count} чатов")
            return True
        else:
            logger.error("Не удалось отправить Telegram сообщения ни в один чат")
            return False
    
    def get_avito_messages(self) -> List[Dict]:
        """
        Получение сообщений с Avito
        
        Returns:
            List[Dict]: Список сообщений
        """
        try:
            messages = self.avito_client.get_messages()
            logger.info(f"Получено {len(messages)} сообщений с Avito")
            return messages
            
        except Exception as e:
            logger.error(f"Ошибка получения сообщений Avito: {e}")
            return []
    

    
    def format_message_for_telegram(self, avito_message: Dict) -> str:
        """
        Форматирование сообщения для Telegram
        
        Args:
            avito_message: Сообщение с Avito
            
        Returns:
            str: Отформатированное сообщение
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
🔔 <b>Новое сообщение с Avito</b>

📅 <b>Время:</b> {timestamp}
👤 <b>От:</b> {avito_message.get('sender', 'Неизвестно')}
📋 <b>Объявление:</b> {avito_message.get('ad_title', 'Неизвестно')}

💬 <b>Сообщение:</b>
{avito_message.get('text', 'Пустое сообщение')}

---
<i>Отправлено автоматически</i>
        """.strip()
        
        return message
    
    def process_messages(self):
        """Основной метод обработки сообщений"""
        logger.info("Начинаем проверку новых сообщений...")
        
        # Получаем сообщения с Avito
        messages = self.get_avito_messages()
        
        if not messages:
            logger.info("Новых сообщений не найдено")
            return
        
        logger.info(f"Найдено {len(messages)} новых сообщений")
        
        # Обрабатываем каждое сообщение
        for message in messages:
            try:
                # Отправляем в Telegram
                telegram_message = self.format_message_for_telegram(message)
                telegram_sent = self.send_telegram_message(telegram_message)
                
                if telegram_sent:
                    logger.info("Сообщение успешно переслано в Telegram")
                else:
                    logger.error("Не удалось отправить сообщение в Telegram")
                    
            except Exception as e:
                logger.error(f"Ошибка обработки сообщения: {e}")
    
    def run_continuous(self, check_interval: int = 300):
        """
        Запуск в режиме постоянной проверки
        
        Args:
            check_interval: Интервал проверки в секундах (по умолчанию 5 минут)
        """
        logger.info(f"Запуск в режиме постоянной проверки (интервал: {check_interval} сек)")
        
        while True:
            try:
                self.process_messages()
                time.sleep(check_interval)
            except KeyboardInterrupt:
                logger.info("Остановка программы по запросу пользователя")
                break
            except Exception as e:
                logger.error(f"Неожиданная ошибка: {e}")
                time.sleep(60)  # Ждем минуту перед повторной попыткой


def main():
    """Главная функция"""
    # Загружаем конфигурацию
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error("Файл config.json не найден. Создайте его с необходимыми настройками.")
        return
    except json.JSONDecodeError:
        logger.error("Ошибка в формате файла config.json")
        return
    
    # Создаем и запускаем форвардер
    forwarder = AvitoMessageForwarder(config)
    
    # Можно запустить однократную проверку или в режиме постоянной работы
    # forwarder.process_messages()  # Однократная проверка
    forwarder.run_continuous()  # Постоянная работа


if __name__ == "__main__":
    main()
