#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для работы с Avito API и получения сообщений
"""

import requests
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import time

logger = logging.getLogger(__name__)


class AvitoClient:
    """Клиент для работы с Avito"""
    
    def __init__(self, config: Dict):
        """
        Инициализация клиента
        
        Args:
            config: Конфигурация Avito
        """
        self.config = config
        self.api_key = config.get('api_key')
        self.user_id = config.get('user_id')
        self.method = config.get('method', 'api')  # 'api' или 'scraping'
        self.base_url = 'https://api.avito.ru'
        self.processed_messages = set()  # Для отслеживания обработанных сообщений
        
    def get_access_token(self) -> Optional[str]:
        """
        Получение access token через OAuth 2.0
        
        Returns:
            Optional[str]: Access token или None при ошибке
        """
        try:
            auth_url = 'https://api.avito.ru/token'
            
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.user_id,
                'client_secret': self.api_key
            }
            
            response = requests.post(auth_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                return token_data.get('access_token')
            else:
                logger.error(f"Ошибка получения токена: {response.status_code}, {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка при получении токена: {e}")
            return None

    def get_messages_via_api(self) -> List[Dict]:
        """
        Получение сообщений через официальный API Avito
        
        Returns:
            List[Dict]: Список сообщений
        """
        messages = []
        
        if not self.api_key or not self.user_id:
            logger.error("Client ID или Client Secret не настроены")
            return messages
        
        # Получаем access token
        access_token = self.get_access_token()
        if not access_token:
            logger.error("Не удалось получить access token")
            return messages
            
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Получаем список чатов
            chats_url = f'{self.base_url}/messenger/v1/accounts/{self.user_id}/chats'
            response = requests.get(chats_url, headers=headers)
            response.raise_for_status()
            
            chats_data = response.json()
            
            # Обрабатываем каждый чат
            for chat in chats_data.get('chats', []):
                chat_id = chat.get('id')
                if not chat_id:
                    continue
                    
                # Получаем сообщения из чата
                messages_url = f'{self.base_url}/messenger/v1/accounts/{self.user_id}/chats/{chat_id}/messages'
                messages_response = requests.get(messages_url, headers=headers)
                messages_response.raise_for_status()
                
                messages_data = messages_response.json()
                
                # Обрабатываем новые сообщения
                for message in messages_data.get('messages', []):
                    message_id = message.get('id')
                    
                    # Пропускаем уже обработанные сообщения
                    if message_id in self.processed_messages:
                        continue
                        
                    # Пропускаем свои сообщения
                    if message.get('author_id') == self.user_id:
                        continue
                        
                    processed_message = {
                        'id': message_id,
                        'text': message.get('content', {}).get('text', ''),
                        'sender': message.get('author_id'),
                        'timestamp': message.get('created'),
                        'chat_id': chat_id,
                        'ad_title': chat.get('context', {}).get('value', {}).get('title', 'Неизвестно'),
                        'ad_url': chat.get('context', {}).get('value', {}).get('url', '')
                    }
                    
                    messages.append(processed_message)
                    self.processed_messages.add(message_id)
                    
        except requests.RequestException as e:
            logger.error(f"Ошибка API запроса к Avito: {e}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении сообщений через API: {e}")
            
        return messages
    
    def get_messages_via_scraping(self) -> List[Dict]:
        """
        Получение сообщений через веб-скрапинг (упрощенная версия без Selenium)
        
        Returns:
            List[Dict]: Список сообщений
        """
        messages = []
        logger.warning("Метод скрапинга недоступен без Selenium. Используйте API метод.")
        logger.info("Для работы через API настройте 'method': 'api' в config.json")
        return messages
    
    def get_messages(self) -> List[Dict]:
        """
        Получение сообщений (выбирает метод в зависимости от конфигурации)
        
        Returns:
            List[Dict]: Список новых сообщений
        """
        if self.method == 'api':
            return self.get_messages_via_api()
        elif self.method == 'scraping':
            return self.get_messages_via_scraping()
        elif self.method == 'disabled':
            logger.info("Avito интеграция отключена - используется только Telegram")
            return []
        else:
            logger.error(f"Неизвестный метод получения сообщений: {self.method}")
            return []
    
    def mark_message_as_read(self, message_id: str, chat_id: str) -> bool:
        """
        Отметить сообщение как прочитанное
        
        Args:
            message_id: ID сообщения
            chat_id: ID чата
            
        Returns:
            bool: Успешность операции
        """
        if self.method != 'api' or not self.api_key or not self.user_id:
            return False
        
        # Получаем access token
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            url = f'{self.base_url}/messenger/v1/accounts/{self.user_id}/chats/{chat_id}/messages/{message_id}/read'
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отметки сообщения как прочитанного: {e}")
            return False
