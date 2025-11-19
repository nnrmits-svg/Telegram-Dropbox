"""
Script de verificación de configuración
Ejecuta este script para verificar que todo está configurado correctamente
"""

import sys

def check_configuration():
    """Verificar que la configuración esté completa"""
    
    print("=" * 60)
    print("🔍 VERIFICADOR DE CONFIGURACIÓN")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # Verificar que config.py existe
    print("1️⃣  Verificando archivo config.py...")
    try:
        import config
        print("   ✅ Archivo config.py encontrado")
    except ImportError:
        print("   ❌ No se encuentra config.py")
        errors.append("Archivo config.py no encontrado. Copia config.example.py a config.py")
        return False
    
    # Verificar Token de Telegram
    print("\n2️⃣  Verificando Token de Telegram...")
    if hasattr(config, 'TELEGRAM_BOT_TOKEN'):
        token = config.TELEGRAM_BOT_TOKEN
        if token == "TU_TOKEN_DE_TELEGRAM_AQUI" or not token:
            print("   ❌ Token de Telegram no configurado")
            errors.append("Debes configurar TELEGRAM_BOT_TOKEN en config.py")
        elif ':' in token and len(token) > 40:
            print(f"   ✅ Token configurado (longitud: {len(token)})")
        else:
            print("   ⚠️  Token parece inválido")
            warnings.append("El formato del token de Telegram parece incorrecto")
    else:
        print("   ❌ TELEGRAM_BOT_TOKEN no definido")
        errors.append("Falta definir TELEGRAM_BOT_TOKEN en config.py")
    
    # Verificar App Key de Dropbox
    print("\n3️⃣  Verificando credenciales de Dropbox...")
    if hasattr(config, 'DROPBOX_APP_KEY'):
        app_key = config.DROPBOX_APP_KEY
        if app_key == "TU_APP_KEY_AQUI" or not app_key:
            print("   ❌ App Key no configurada")
            errors.append("Debes configurar DROPBOX_APP_KEY en config.py")
        else:
            print(f"   ✅ App Key configurada (longitud: {len(app_key)})")
    else:
        print("   ❌ DROPBOX_APP_KEY no definida")
        errors.append("Falta definir DROPBOX_APP_KEY en config.py")
    
    # Verificar App Secret de Dropbox
    if hasattr(config, 'DROPBOX_APP_SECRET'):
        app_secret = config.DROPBOX_APP_SECRET
        if app_secret == "TU_APP_SECRET_AQUI" or not app_secret:
            print("   ❌ App Secret no configurada")
            errors.append("Debes configurar DROPBOX_APP_SECRET en config.py")
        else:
            print(f"   ✅ App Secret configurada (longitud: {len(app_secret)})")
    else:
        print("   ❌ DROPBOX_APP_SECRET no definida")
        errors.append("Falta definir DROPBOX_APP_SECRET en config.py")
    
    # Verificar Refresh Token de Dropbox
    if hasattr(config, 'DROPBOX_REFRESH_TOKEN'):
        refresh_token = config.DROPBOX_REFRESH_TOKEN
        if refresh_token == "TU_REFRESH_TOKEN_AQUI" or not refresh_token:
            print("   ❌ Refresh Token no configurado")
            errors.append("Debes generar el Refresh Token ejecutando: python generate_token.py")
        else:
            print(f"   ✅ Refresh Token configurado (longitud: {len(refresh_token)})")
    else:
        print("   ❌ DROPBOX_REFRESH_TOKEN no definido")
        errors.append("Falta definir DROPBOX_REFRESH_TOKEN en config.py")
    
    # Verificar dependencias
    print("\n4️⃣  Verificando dependencias de Python...")
    
    try:
        import telegram
        print("   ✅ python-telegram-bot instalado")
    except ImportError:
        print("   ❌ python-telegram-bot no instalado")
        errors.append("Ejecuta: pip install -r requirements.txt")
    
    try:
        import dropbox
        print("   ✅ dropbox instalado")
    except ImportError:
        print("   ❌ dropbox no instalado")
        errors.append("Ejecuta: pip install -r requirements.txt")
    
    # Verificar configuración adicional
    print("\n5️⃣  Verificando configuración adicional...")
    if hasattr(config, 'DROPBOX_FOLDER'):
        print(f"   ✅ Carpeta destino: {config.DROPBOX_FOLDER}")
    else:
        warnings.append("DROPBOX_FOLDER no definida, se usará '/TelegramBot'")
    
    if hasattr(config, 'MAX_FILE_SIZE_MB'):
        print(f"   ✅ Tamaño máximo: {config.MAX_FILE_SIZE_MB} MB")
    else:
        warnings.append("MAX_FILE_SIZE_MB no definida, se usará 20 MB")
    
    # Mostrar resumen
    print()
    print("=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    if errors:
        print(f"\n❌ Se encontraron {len(errors)} errores:\n")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} advertencias:\n")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    if not errors and not warnings:
        print("\n✅ ¡CONFIGURACIÓN CORRECTA!")
        print("\n🚀 Puedes ejecutar el bot con: python bot.py")
        return True
    elif not errors:
        print("\n⚠️  Configuración funcional pero con advertencias")
        print("\n🚀 Puedes ejecutar el bot con: python bot.py")
        return True
    else:
        print("\n❌ Por favor corrige los errores antes de continuar")
        return False
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    try:
        success = check_configuration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print()
        print(f"❌ Error al verificar configuración: {e}")
        sys.exit(1)
