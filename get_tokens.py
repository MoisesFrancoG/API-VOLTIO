#!/usr/bin/env python3
"""
🔐 API VOLTIO - Generador de Tokens via Login
============================================
Script para obtener tokens mediante login tradicional (funciona en producción)
============================================
"""

import requests
import json
import argparse
from typing import Dict, Any

# URLs de la API
API_URLS = {
    "local": "http://localhost:8000/api/v1",
    "prod": "https://voltioapi.acstree.xyz/api/v1"
}

# Credenciales de prueba
TEST_CREDENTIALS = {
    "superadmin": {
        "email": "superadmin@voltio.com",
        "password": "SuperAdmin123!"
    },
    "admin": {
        "email": "admin@voltio.com", 
        "password": "Admin123!"
    },
    "user": {
        "email": "user@voltio.com",
        "password": "User123!"
    },
    "guest": {
        "email": "guest@voltio.com",
        "password": "Guest123!"
    }
}

def login_user(base_url: str, email: str, password: str) -> Dict[str, Any]:
    """Hacer login y obtener token"""
    try:
        login_data = {
            "email": email,
            "password": password
        }
        
        response = requests.post(
            f"{base_url}/users/login", 
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Login failed - HTTP {response.status_code}", 
                "detail": response.text
            }
            
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def test_token(base_url: str, token: str) -> Dict[str, Any]:
    """Probar un token obtenido"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/users/me", headers=headers)
        
        if response.status_code == 200:
            return {"status": "✅ Token válido", "user": response.json()}
        else:
            return {"status": "❌ Token inválido", "error": response.text}
            
    except Exception as e:
        return {"status": "❌ Error de conexión", "error": str(e)}

def get_all_tokens(base_url: str) -> Dict[str, Any]:
    """Obtener tokens de todos los usuarios de prueba"""
    tokens = {}
    
    for user_type, credentials in TEST_CREDENTIALS.items():
        print(f"🔐 Obteniendo token para {user_type} ({credentials['email']})...")
        
        result = login_user(base_url, credentials['email'], credentials['password'])
        
        if "error" in result:
            tokens[user_type] = {
                "email": credentials['email'],
                "status": "❌ Error",
                "error": result['error']
            }
        else:
            tokens[user_type] = {
                "email": credentials['email'], 
                "status": "✅ Success",
                "access_token": result['access_token'],
                "token_type": result['token_type'],
                "expires_in": result.get('expires_in', 1800),
                "user_id": result.get('user_id', 'N/A')
            }
    
    return tokens

def main():
    parser = argparse.ArgumentParser(description='Obtener tokens via login para API VOLTIO')
    parser.add_argument('--env', choices=['local', 'prod'], default='prod',
                        help='Ambiente (local o prod)')
    parser.add_argument('--user', choices=['superadmin', 'admin', 'user', 'guest'],
                        help='Tipo de usuario específico')
    parser.add_argument('--all', action='store_true',
                        help='Obtener tokens de todos los usuarios')
    parser.add_argument('--test', type=str, metavar='TOKEN',
                        help='Probar un token específico')
    parser.add_argument('--custom', nargs=2, metavar=('EMAIL', 'PASSWORD'),
                        help='Login con credenciales personalizadas')
    
    args = parser.parse_args()
    
    base_url = API_URLS[args.env]
    
    print(f"🚀 API VOLTIO - Tokens via Login")
    print(f"{'='*50}")
    print(f"🌐 Ambiente: {args.env.upper()}")
    print(f"🔗 URL: {base_url}")
    print(f"{'='*50}")
    
    # Probar token específico
    if args.test:
        print(f"\n🧪 PROBANDO TOKEN:")
        result = test_token(base_url, args.test)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    # Login con credenciales personalizadas
    if args.custom:
        email, password = args.custom
        print(f"\n🔐 LOGIN PERSONALIZADO: {email}")
        result = login_user(base_url, email, password)
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            return
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Mostrar ejemplo de uso
        token = result["access_token"]
        print(f"\n💡 EJEMPLO DE USO:")
        print(f"{'='*30}")
        print(f"curl -H 'Authorization: Bearer {token[:20]}...' \\")
        print(f"     {base_url}/users/me")
        return
    
    # Obtener todos los tokens
    if args.all:
        print(f"\n👥 OBTENIENDO TOKENS DE TODOS LOS USUARIOS:")
        tokens = get_all_tokens(base_url)
        
        print(f"\n📊 RESULTADOS:")
        print(f"{'='*50}")
        
        for user_type, token_data in tokens.items():
            status = token_data["status"]
            email = token_data["email"]
            
            print(f"\n{status} {user_type.upper()}: {email}")
            
            if "access_token" in token_data:
                token = token_data["access_token"]
                user_id = token_data.get("user_id", "N/A")
                print(f"   � User ID: {user_id}")
                print(f"   🔑 Token: {token[:20]}...")
                print(f"   📝 Curl: curl -H 'Authorization: Bearer {token}' {base_url}/users/me")
            elif "error" in token_data:
                print(f"   ❌ Error: {token_data['error']}")
        
        return
    
    # Obtener token de usuario específico
    if args.user:
        credentials = TEST_CREDENTIALS[args.user]
        print(f"\n🔐 LOGIN COMO {args.user.upper()}: {credentials['email']}")
        
        result = login_user(base_url, credentials['email'], credentials['password'])
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            return
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Mostrar ejemplo de uso
        token = result["access_token"]
        print(f"\n💡 EJEMPLO DE USO:")
        print(f"{'='*30}")
        print(f"curl -H 'Authorization: Bearer {token[:20]}...' \\")
        print(f"     {base_url}/users/me")
        return
    
    # Por defecto, obtener token de SuperAdmin
    credentials = TEST_CREDENTIALS["superadmin"]
    print(f"\n🔐 LOGIN COMO SUPERADMIN: {credentials['email']}")
    
    result = login_user(base_url, credentials['email'], credentials['password'])
    
    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
        return
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Mostrar ejemplo de uso
    token = result["access_token"]
    print(f"\n💡 EJEMPLO DE USO:")
    print(f"{'='*30}")
    print(f"curl -H 'Authorization: Bearer {token[:20]}...' \\")
    print(f"     {base_url}/users/me")

if __name__ == "__main__":
    main()
