#!/usr/bin/env python3
"""
🌐 API VOLTIO - Configurador de CORS
===================================
Script para configurar CORS dinámicamente
===================================
"""

import os
import argparse
from pathlib import Path

def update_env_file(key, value, env_file=".env"):
    """Actualizar o agregar variable en archivo .env"""
    
    env_path = Path(env_file)
    
    # Leer contenido actual
    if env_path.exists():
        with open(env_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Buscar si la variable ya existe
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break
    
    # Si no existe, agregarla
    if not updated:
        lines.append(f"{key}={value}\n")
    
    # Escribir archivo
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Actualizado {key} en {env_file}")

def configure_cors_development():
    """Configurar CORS para desarrollo"""
    
    print("🛠️ Configurando CORS para DESARROLLO...")
    
    origins = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:4200",
        "http://localhost:5000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173"
    ]
    
    cors_origins = ",".join(origins)
    
    # Actualizar variables de entorno
    update_env_file("CORS_ORIGINS", cors_origins)
    update_env_file("CORS_ALLOW_CREDENTIALS", "true")
    update_env_file("CORS_ALLOW_METHODS", "GET,POST,PUT,PATCH,DELETE,OPTIONS")
    update_env_file("CORS_MAX_AGE", "600")
    
    print(f"✅ CORS configurado para desarrollo con {len(origins)} orígenes")

def configure_cors_production(domains):
    """Configurar CORS para producción"""
    
    print("🚀 Configurando CORS para PRODUCCIÓN...")
    
    # Validar que sean HTTPS
    valid_domains = []
    for domain in domains:
        if not domain.startswith("https://"):
            print(f"⚠️ Agregando HTTPS a: {domain}")
            domain = f"https://{domain}"
        valid_domains.append(domain)
    
    cors_origins = ",".join(valid_domains)
    
    # Actualizar variables de entorno
    update_env_file("CORS_ORIGINS", cors_origins)
    update_env_file("CORS_ALLOW_CREDENTIALS", "true") 
    update_env_file("CORS_ALLOW_METHODS", "GET,POST,PUT,PATCH,DELETE,OPTIONS")
    update_env_file("CORS_MAX_AGE", "3600")  # 1 hora en producción
    
    print(f"✅ CORS configurado para producción con {len(valid_domains)} dominios:")
    for domain in valid_domains:
        print(f"   • {domain}")

def add_cors_origin(origin):
    """Agregar un origen a la configuración existente"""
    
    print(f"➕ Agregando origen: {origin}")
    
    # Leer configuración actual
    env_path = Path(".env")
    current_origins = []
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("CORS_ORIGINS="):
                    current_value = line.split("=", 1)[1].strip()
                    if current_value:
                        current_origins = [o.strip() for o in current_value.split(",")]
                    break
    
    # Agregar nuevo origen si no existe
    if origin not in current_origins:
        current_origins.append(origin)
        cors_origins = ",".join(current_origins)
        update_env_file("CORS_ORIGINS", cors_origins)
        print(f"✅ Origen agregado. Total: {len(current_origins)} orígenes")
    else:
        print(f"⚠️ El origen ya existe en la configuración")

def show_current_config():
    """Mostrar configuración actual de CORS"""
    
    print("📋 CONFIGURACIÓN ACTUAL DE CORS:")
    print("=" * 40)
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Archivo .env no encontrado")
        return
    
    cors_vars = {
        "CORS_ORIGINS": "Orígenes permitidos",
        "CORS_ALLOW_CREDENTIALS": "Permitir credenciales", 
        "CORS_ALLOW_METHODS": "Métodos permitidos",
        "CORS_ALLOW_HEADERS": "Headers permitidos",
        "CORS_EXPOSE_HEADERS": "Headers expuestos",
        "CORS_MAX_AGE": "Tiempo de cache (segundos)"
    }
    
    with open(env_path, 'r') as f:
        for line in f:
            for var, description in cors_vars.items():
                if line.startswith(f"{var}="):
                    value = line.split("=", 1)[1].strip()
                    print(f"🔧 {description}:")
                    
                    if var == "CORS_ORIGINS" and value:
                        origins = [o.strip() for o in value.split(",")]
                        for i, origin in enumerate(origins, 1):
                            print(f"   {i}. {origin}")
                    else:
                        print(f"   {value}")
                    print()
                    break

def main():
    parser = argparse.ArgumentParser(description='Configurador de CORS para API VOLTIO')
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Desarrollo
    dev_parser = subparsers.add_parser('dev', help='Configurar para desarrollo')
    
    # Producción
    prod_parser = subparsers.add_parser('prod', help='Configurar para producción')
    prod_parser.add_argument('domains', nargs='+', help='Dominios permitidos')
    
    # Agregar origen
    add_parser = subparsers.add_parser('add', help='Agregar un origen')
    add_parser.add_argument('origin', help='Origen a agregar')
    
    # Mostrar configuración
    show_parser = subparsers.add_parser('show', help='Mostrar configuración actual')
    
    args = parser.parse_args()
    
    print("🌐 API VOLTIO - Configurador de CORS")
    print("=" * 50)
    
    if args.command == 'dev':
        configure_cors_development()
        
    elif args.command == 'prod':
        configure_cors_production(args.domains)
        
    elif args.command == 'add':
        add_cors_origin(args.origin)
        
    elif args.command == 'show':
        show_current_config()
        
    else:
        parser.print_help()
        print("\nEjemplos de uso:")
        print("  python configure_cors.py dev")
        print("  python configure_cors.py prod dashboard.voltio.com app.voltio.com")
        print("  python configure_cors.py add https://nuevo-dominio.com")
        print("  python configure_cors.py show")

if __name__ == "__main__":
    main()
