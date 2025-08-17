#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic script for Avito API access
"""

import json
import requests

def check_avito_api_access():
    """Check what Avito API access is available"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка чтения config.json: {e}")
        return

    avito_config = config.get('avito', {})
    api_key = avito_config.get('api_key')
    user_id = avito_config.get('user_id')
    
    print("🔍 Диагностика Avito API доступа")
    print(f"📋 API Key: {api_key[:10]}..." if api_key else "❌ API Key отсутствует")
    print(f"👤 User ID: {user_id[:10]}..." if user_id else "❌ User ID отсутствует")
    
    if not api_key or not user_id:
        print("\n❌ Недостаточно данных для тестирования")
        return
    
    # Test 1: Try direct API key authentication (older method)
    print("\n🧪 Тест 1: Прямая аутентификация по API ключу")
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Try to get user info
        url = f'https://api.avito.ru/core/v1/accounts/{user_id}'
        response = requests.get(url, headers=headers)
        
        print(f"📊 Статус: {response.status_code}")
        if response.status_code == 200:
            print("✅ Прямая аутентификация работает!")
            data = response.json()
            print(f"📝 Аккаунт: {data.get('name', 'Неизвестно')}")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
    
    # Test 2: Check available API methods
    print("\n🧪 Тест 2: Проверка доступных методов API")
    try:
        # Try different endpoints to see what's available
        endpoints = [
            f'https://api.avito.ru/core/v1/accounts/{user_id}',
            f'https://api.avito.ru/core/v1/accounts/{user_id}/items',
            f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats'
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, headers=headers)
                endpoint_name = endpoint.split('/')[-1] or endpoint.split('/')[-2]
                
                if response.status_code == 200:
                    print(f"✅ {endpoint_name}: Доступен")
                elif response.status_code == 403:
                    print(f"🔒 {endpoint_name}: Нет доступа (403)")
                elif response.status_code == 401:
                    print(f"🚫 {endpoint_name}: Не авторизован (401)")
                else:
                    print(f"❓ {endpoint_name}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {endpoint_name}: Ошибка - {e}")
                
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
    
    print("\n📋 Рекомендации:")
    print("1. Проверьте, что у вас есть доступ к Avito API для бизнеса")
    print("2. Убедитесь, что API ключ активен в личном кабинете")
    print("3. Возможно, нужно запросить доступ к Messenger API отдельно")
    print("4. Рассмотрите использование веб-скрапинга как альтернативу")

if __name__ == "__main__":
    check_avito_api_access()
