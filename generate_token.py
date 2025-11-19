"""
Script para generar el Refresh Token de Dropbox
Ejecuta este script UNA VEZ para obtener tu refresh token
"""

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

def generate_refresh_token(app_key, app_secret):
    """
    Genera un refresh token para Dropbox usando OAuth2
    
    Args:
        app_key: App Key de tu aplicación Dropbox
        app_secret: App Secret de tu aplicación Dropbox
    """
    print("=" * 60)
    print("GENERADOR DE REFRESH TOKEN PARA DROPBOX")
    print("=" * 60)
    print()
    
    # Iniciar flujo OAuth2
    auth_flow = DropboxOAuth2FlowNoRedirect(
        app_key,
        app_secret,
        token_access_type='offline'  # Esto genera un refresh token
    )
    
    # Obtener URL de autorización
    authorize_url = auth_flow.start()
    
    print("1️⃣  Abre esta URL en tu navegador:")
    print()
    print(f"   {authorize_url}")
    print()
    print("2️⃣  Autoriza la aplicación")
    print("3️⃣  Copia el código que te muestra Dropbox")
    print()
    
    # Solicitar el código de autorización
    auth_code = input("📋 Pega aquí el código de autorización: ").strip()
    
    try:
        # Obtener el refresh token
        oauth_result = auth_flow.finish(auth_code)
        
        print()
        print("=" * 60)
        print("✅ ¡REFRESH TOKEN GENERADO EXITOSAMENTE!")
        print("=" * 60)
        print()
        print("🔑 Tu Refresh Token:")
        print()
        print(f"   {oauth_result.refresh_token}")
        print()
        print("=" * 60)
        print()
        print("📝 IMPORTANTE:")
        print("   1. Copia este refresh token")
        print("   2. Pégalo en config.py en DROPBOX_REFRESH_TOKEN")
        print("   3. ¡NO compartas este token con nadie!")
        print("   4. Guárdalo en un lugar seguro")
        print()
        print("=" * 60)
        
        # Verificar que funciona
        print()
        print("🔍 Verificando el token...")
        dbx = dropbox.Dropbox(
            app_key=app_key,
            app_secret=app_secret,
            oauth2_refresh_token=oauth_result.refresh_token
        )
        account = dbx.users_get_current_account()
        print(f"✅ Token válido! Conectado como: {account.name.display_name}")
        print(f"📧 Email: {account.email}")
        
        return oauth_result.refresh_token
        
    except Exception as e:
        print()
        print(f"❌ Error al generar el token: {e}")
        print()
        print("Posibles causas:")
        print("  • El código de autorización es incorrecto")
        print("  • El código ya fue usado (son de un solo uso)")
        print("  • Las credenciales de la app son incorrectas")
        print()
        print("Intenta ejecutar el script nuevamente.")
        return None

if __name__ == '__main__':
    print()
    print("Necesitas tener:")
    print("  • App Key de tu aplicación Dropbox")
    print("  • App Secret de tu aplicación Dropbox")
    print()
    
    app_key = input("🔑 Ingresa tu App Key: ").strip()
    app_secret = input("🔐 Ingresa tu App Secret: ").strip()
    
    if app_key and app_secret:
        generate_refresh_token(app_key, app_secret)
    else:
        print("❌ Debes ingresar ambos valores.")
