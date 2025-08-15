#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения chat_id Telegram
"""

import requests
import json

def get_chat_id(bot_token):
    """Получить chat_id из последних сообщений бота"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('ok'):
            print("❌ Ошибка получения обновлений")
            return None
        
        updates = data.get('result', [])
        
        if not updates:
            print("⚠️ Нет сообщений. Отправьте сообщение боту и попробуйте снова.")
            return None
        
        print("📨 Найденные чаты:")
        chat_ids = set()
        
        for update in updates:
            message = update.get('message', {})
            chat = message.get('chat', {})
            
            if chat:
                chat_id = chat.get('id')
                chat_type = chat.get('type', 'unknown')
                first_name = chat.get('first_name', '')
                username = chat.get('username', '')
                
                chat_ids.add(chat_id)
                
                print(f"  Chat ID: {chat_id}")
                print(f"  Тип: {chat_type}")
                print(f"  Имя: {first_name}")
                print(f"  Username: @{username}" if username else "  Username: не указан")
                print("  ---")
        
        return list(chat_ids)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def main():
    print("🔍 Получение Chat ID для Telegram бота\n")
    
    bot_token = input("Введите токен бота: ").strip()
    
    if not bot_token:
        print("❌ Токен не может быть пустым")
        return
    
    print("\n📡 Получаем информацию о боте...")
    
    # Проверяем токен
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url)
        response.raise_for_status()
        
        bot_info = response.json()
        
        if bot_info.get('ok'):
            bot_data = bot_info['result']
            print(f"✅ Бот найден: {bot_data['first_name']} (@{bot_data.get('username', 'без username')})")
        else:
            print("❌ Неверный токен бота")
            return
            
    except Exception as e:
        print(f"❌ Ошибка проверки токена: {e}")
        return
    
    print("\n📨 Ищем чаты...")
    chat_ids = get_chat_id(bot_token)
    
    if chat_ids:
        print(f"\n✅ Найдено {len(chat_ids)} уникальных чатов")
        print("\n📋 Для config.json используйте один из этих chat_id:")
        for chat_id in chat_ids:
            print(f"  {chat_id}")
    else:
        print("\n⚠️ Chat ID не найдены.")
        print("💡 Инструкция:")
        print("1. Отправьте сообщение боту в Telegram")
        print("2. Запустите этот скрипт снова")

if __name__ == "__main__":
    main()
