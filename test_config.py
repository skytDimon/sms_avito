#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования конфигурации и соединений
"""

import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





def test_telegram_config(telegram_config):
    """Тестирование Telegram настроек"""
    print("🔍 Тестирование Telegram настроек...")
    
    try:
        bot_token = telegram_config.get('bot_token')
        chat_ids = telegram_config.get('chat_ids', [])
        
        # Поддержка старого формата
        if not chat_ids and telegram_config.get('chat_id'):
            chat_ids = [telegram_config.get('chat_id')]
        
        if not all([bot_token, chat_ids]):
            print("❌ Не все Telegram настройки заполнены")
            return False
        
        # Тестовый запрос к API
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url)
        response.raise_for_status()
        
        bot_info = response.json()
        if not bot_info.get('ok'):
            print("❌ Неверный токен бота")
            return False
        
        print(f"✅ Бот найден: {bot_info['result']['first_name']}")
        
        # Отправляем тестовые сообщения во все чаты
        success_count = 0
        for i, chat_id in enumerate(chat_ids):
            send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': f'🔔 Тест - Avito Message Forwarder работает! (Чат {i+1}/{len(chat_ids)})'
            }
            
            try:
                response = requests.post(send_url, data=data)
                response.raise_for_status()
                
                result = response.json()
                if result.get('ok'):
                    print(f"✅ Сообщение отправлено в chat_id: {chat_id}")
                    success_count += 1
                else:
                    print(f"❌ Ошибка отправки в chat_id {chat_id}: {result}")
            except Exception as e:
                print(f"❌ Ошибка отправки в chat_id {chat_id}: {e}")
        
        if success_count > 0:
            print(f"✅ Telegram настройки работают корректно ({success_count}/{len(chat_ids)} чатов)")
            return True
        else:
            print("❌ Не удалось отправить сообщения ни в один чат")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка Telegram настроек: {e}")
        return False


def get_avito_access_token(client_id, client_secret):
    """Получение access token для Avito API"""
    try:
        auth_url = 'https://api.avito.ru/token'
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        response = requests.post(auth_url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            print(f"❌ Ошибка получения токена: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при получении токена: {e}")
        return None


def test_avito_config(avito_config):
    """Тестирование Avito настроек"""
    print("🔍 Тестирование Avito настроек...")
    
    method = avito_config.get('method', 'api')
    
    if method == 'api':
        client_secret = avito_config.get('api_key')  # это client_secret
        client_id = avito_config.get('user_id')     # это client_id
        
        if not all([client_secret, client_id]):
            print("❌ Client ID или Client Secret не заполнены")
            return False
        
        try:
            # Получаем access token
            access_token = get_avito_access_token(client_id, client_secret)
            
            if not access_token:
                print("❌ Не удалось получить access token")
                return False
            
            print("✅ Access token получен успешно")
            
            # Тестируем API с полученным токеном
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Простой тест - проверяем доступность базового API
            try:
                print("🔍 Тестируем базовый API endpoint...")
                test_url = 'https://api.avito.ru/core/v1/accounts/self'
                response = requests.get(test_url, headers=headers)
                
                if response.status_code == 200:
                    print("✅ Базовый API работает корректно")
                    print("⚠️ Но API мессенджера может быть недоступен для данного типа приложения")
                    print("💡 Рекомендуется использовать веб-скрапинг или обратиться в поддержку Avito")
                    return True
                elif response.status_code == 403:
                    print("⚠️ API доступен, но нет прав на данный endpoint")
                    print("💡 Возможно, нужно запросить доступ к API мессенджера у Avito")
                    return True
                else:
                    print(f"⚠️ Ответ API: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"⚠️ Ошибка запроса: {e}")
            
            print("❌ API недоступен или требует дополнительной настройки")
            print("💡 Рекомендации:")
            print("   1. Обратитесь в поддержку Avito для получения доступа к API мессенджера")
            print("   2. Используйте метод 'scraping' в config.json")
            print("   3. Проверьте, что ваше приложение имеет необходимые разрешения")
            return False
                
        except Exception as e:
            print(f"❌ Ошибка подключения к Avito API: {e}")
            return False
    
    elif method == 'scraping':
        print("⚠️ Веб-скрапинг настроен, но требует дополнительной настройки ChromeDriver")
        return True
    
    elif method == 'disabled':
        print("ℹ️ Avito интеграция отключена - работает только Telegram")
        return True
    
    else:
        print(f"❌ Неизвестный метод: {method}")
        return False


def main():
    """Главная функция тестирования"""
    print("🚀 Запуск тестирования конфигурации Avito Message Forwarder\n")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Файл config.json не найден!")
        print("📝 Создайте файл config.json на основе примера в README.md")
        return
    except json.JSONDecodeError:
        print("❌ Ошибка в формате файла config.json")
        return
    
    results = []
    
    # Тестируем каждый компонент
    if 'telegram' in config:
        results.append(test_telegram_config(config['telegram']))
    else:
        print("❌ Секция 'telegram' не найдена в config.json")
        results.append(False)
    
    print()
    
    if 'avito' in config:
        results.append(test_avito_config(config['avito']))
    else:
        print("❌ Секция 'avito' не найдена в config.json")
        results.append(False)
    
    print("\n" + "="*50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"Telegram: {'✅' if results[0] else '❌'}")
    print(f"Avito: {'✅' if results[1] else '❌'}")
    
    if all(results):
        print("\n🎉 Все настройки работают корректно!")
        print("🚀 Можно запускать основную программу: python main.py")
    else:
        print("\n⚠️ Есть проблемы с настройками. Проверьте config.json")
        print("📖 Подробности в README.md")


if __name__ == "__main__":
    main()
