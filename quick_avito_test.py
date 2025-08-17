#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test for Avito API credentials
"""

import json
import requests

def test_avito_auth():
    """Quick test of Avito authentication"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка чтения config.json: {e}")
        return False
    
    avito_config = config.get('avito', {})
    client_secret = avito_config.get('api_key')  # это client_secret
    client_id = avito_config.get('user_id')     # это client_id
    
    if not all([client_secret, client_id]):
        print("❌ Client ID или Client Secret не заполнены")
        return False
    
    print(f"🔍 Тестируем аутентификацию с client_id: {client_id[:8]}...")
    
    try:
        auth_url = 'https://api.avito.ru/token'
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        response = requests.post(auth_url, data=data)
        
        print(f"📊 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            if token_data.get('access_token'):
                print("✅ Access token получен успешно!")
                print(f"🔑 Токен: {token_data['access_token'][:20]}...")
                return True
            else:
                print("❌ Access token не найден в ответе")
                print(f"Ответ: {response.text}")
                return False
        else:
            print(f"❌ Ошибка получения токена: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при запросе: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Быстрый тест Avito API")
    success = test_avito_auth()
    print(f"\n📊 Результат: {'✅ Успех' if success else '❌ Ошибка'}")
