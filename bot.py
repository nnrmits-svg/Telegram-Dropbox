"""
Bot de Telegram que sube archivos a Dropbox
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import dropbox
from dropbox.exceptions import ApiError, AuthError
import os

import os

# --- INICIO DE LA CONFIGURACIÓN HÍBRIDA (CORREGIDO) ---

try:
    # PLAN A: Intentamos importar desde el archivo local config.py (Codespace/Local)
    import config
    
    print("✅ Iniciando en modo LOCAL (Codespace)")
    # Asignamos las variables leyendo del archivo config
    # NOTA: Ahora uso los nombres EXACTOS que tu código usa más abajo
    TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
    DROPBOX_APP_KEY = config.DROPBOX_APP_KEY          # Aquí estaba el error de nombre
    DROPBOX_APP_SECRET = config.DROPBOX_APP_SECRET
    DROPBOX_REFRESH_TOKEN = config.DROPBOX_REFRESH_TOKEN
    DROPBOX_FOLDER = config.DROPBOX_FOLDER
except ImportError:
    # PLAN B: Si falla lo anterior, leemos de las Variables de Entorno (Render)
    print("🚀 Iniciando en modo NUBE (Render)")
    
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
    DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
    DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")
    DROPBOX_FOLDER = os.getenv("DROPBOX_FOLDER")
# --- FIN DE LA CONFIGURACIÓN ---

# Verificación rápida para asegurarnos de que cargó
if not DROPBOX_APP_KEY:
    raise ValueError("Error: Falta la variable DROPBOX_APP_KEY")

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DropboxUploader:
    """Clase para manejar la subida de archivos a Dropbox"""
    
    def __init__(self):
        """Inicializar conexión con Dropbox"""
        try:
            self.dbx = dropbox.Dropbox(
                app_key=DROPBOX_APP_KEY,
                app_secret=DROPBOX_APP_SECRET,
                oauth2_refresh_token=DROPBOX_REFRESH_TOKEN
            )
            # Verificar que la conexión funciona
            self.dbx.users_get_current_account()
            logger.info("✅ Conexión con Dropbox establecida correctamente")
        except AuthError as e:
            logger.error(f"❌ Error de autenticación con Dropbox: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error al conectar con Dropbox: {e}")
            raise
    
    def upload_file(self, file_path: str, dropbox_path: str) -> str:
        """
        Subir archivo a Dropbox
        
        Args:
            file_path: Ruta local del archivo
            dropbox_path: Ruta destino en Dropbox
            
        Returns:
            URL compartida del archivo
        """
        try:
            # Leer el archivo
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Subir a Dropbox
            self.dbx.files_upload(
                file_data,
                dropbox_path,
                mode=dropbox.files.WriteMode.overwrite
            )
            
            # Crear enlace compartido
            try:
                shared_link = self.dbx.sharing_create_shared_link(dropbox_path)
                url = shared_link.url.replace('?dl=0', '?dl=1')  # Forzar descarga directa
            except ApiError:
                # Si ya existe un enlace, obtenerlo
                links = self.dbx.sharing_list_shared_links(path=dropbox_path)
                if links.links:
                    url = links.links[0].url.replace('?dl=0', '?dl=1')
                else:
                    url = "Archivo subido (no se pudo crear enlace)"
            
            logger.info(f"✅ Archivo subido: {dropbox_path}")
            return url
            
        except ApiError as e:
            logger.error(f"❌ Error al subir archivo: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            raise

# Instancia global del uploader
uploader = DropboxUploader()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    welcome_message = """
🤖 *Bot de Telegram - Dropbox*

¡Hola! Soy tu bot para subir archivos a Dropbox.

*Comandos disponibles:*
/start - Mostrar este mensaje
/help - Ayuda
/status - Ver estado de conexiones

*¿Cómo usarme?*
📎 Simplemente envíame cualquier archivo (foto, documento, video, etc.)
☁️ Lo subiré automáticamente a tu Dropbox
🔗 Te enviaré el enlace de descarga

*Límites:*
📏 Tamaño máximo: {MAX_FILE_SIZE_MB} MB por archivo
    """.format(MAX_FILE_SIZE_MB=50)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    help_text = """
*Ayuda del Bot*

*Tipos de archivos soportados:*
📷 Fotos
📄 Documentos (PDF, Word, Excel, etc.)
🎥 Videos
🎵 Audio
📦 Archivos comprimidos (ZIP, RAR, etc.)

*Proceso de subida:*
1️⃣ Envía el archivo
2️⃣ Espera la confirmación
3️⃣ Recibe el enlace de Dropbox

*Límites:*
• Tamaño máximo: {MAX_FILE_SIZE_MB} MB
• Formatos: Todos los tipos de archivo

*¿Problemas?*
• Si el archivo es muy grande, comprimelo primero
• Asegúrate de tener espacio en Dropbox
    """.format(MAX_FILE_SIZE_MB=MAX_FILE_SIZE_MB)
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status - Verificar conexiones"""
    try:
        # Verificar Dropbox
        account = uploader.dbx.users_get_current_account()
        dropbox_status = f"✅ Conectado como: {account.name.display_name}"
    except Exception as e:
        dropbox_status = f"❌ Error: {str(e)}"
    
    status_message = f"""
*Estado del Bot*

🤖 *Telegram:* ✅ Activo
☁️ *Dropbox:* {dropbox_status}
📁 *Carpeta destino:* `{DROPBOX_FOLDER}`
    """
    
    await update.message.reply_text(status_message, parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar documentos enviados"""
    document = update.message.document
    
    # Verificar tamaño
    file_size_mb = document.file_size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        await update.message.reply_text(
            f"❌ El archivo es muy grande ({file_size_mb:.1f} MB).\n"
            f"Tamaño máximo permitido: {MAX_FILE_SIZE_MB} MB"
        )
        return
    
    # Enviar mensaje de procesamiento
    processing_msg = await update.message.reply_text("⏳ Descargando archivo...")
    
    try:
        # Descargar archivo de Telegram
        file = await context.bot.get_file(document.file_id)
        local_path = f"/tmp/{document.file_name}"
        await file.download_to_drive(local_path)
        
        await processing_msg.edit_text("☁️ Subiendo a Dropbox...")
        
        # Subir a Dropbox
        dropbox_path = f"{DROPBOX_FOLDER}/{document.file_name}"
        url = uploader.upload_file(local_path, dropbox_path)
        
        # Limpiar archivo temporal
        os.remove(local_path)
        
        # Mensaje de éxito
        success_msg = f"""
✅ *Archivo subido exitosamente*

📄 *Nombre:* `{document.file_name}`
📏 *Tamaño:* {file_size_mb:.2f} MB
🔗 *Enlace:* [Descargar desde Dropbox]({url})

_(El enlace permite descarga directa)_
        """
        
        await processing_msg.edit_text(success_msg, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error al procesar documento: {e}")
        await processing_msg.edit_text(f"❌ Error al subir archivo: {str(e)}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar fotos enviadas"""
    photo = update.message.photo[-1]  # Obtener la foto de mayor calidad
    
    # Enviar mensaje de procesamiento
    processing_msg = await update.message.reply_text("⏳ Descargando foto...")
    
    try:
        # Descargar foto de Telegram
        file = await context.bot.get_file(photo.file_id)
        file_name = f"photo_{photo.file_id}.jpg"
        local_path = f"/tmp/{file_name}"
        await file.download_to_drive(local_path)
        
        await processing_msg.edit_text("☁️ Subiendo a Dropbox...")
        
        # Subir a Dropbox
        dropbox_path = f"{DROPBOX_FOLDER}/{file_name}"
        url = uploader.upload_file(local_path, dropbox_path)
        
        # Limpiar archivo temporal
        os.remove(local_path)
        
        # Mensaje de éxito
        file_size_mb = photo.file_size / (1024 * 1024)
        success_msg = f"""
✅ *Foto subida exitosamente*

📷 *Tamaño:* {file_size_mb:.2f} MB
🔗 *Enlace:* [Ver en Dropbox]({url})
        """
        
        await processing_msg.edit_text(success_msg, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error al procesar foto: {e}")
        await processing_msg.edit_text(f"❌ Error al subir foto: {str(e)}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar videos enviados"""
    video = update.message.video
    
    # Verificar tamaño
    file_size_mb = video.file_size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        await update.message.reply_text(
            f"❌ El video es muy grande ({file_size_mb:.1f} MB).\n"
            f"Tamaño máximo permitido: {MAX_FILE_SIZE_MB} MB"
        )
        return
    
    # Enviar mensaje de procesamiento
    processing_msg = await update.message.reply_text("⏳ Descargando video...")
    
    try:
        # Descargar video de Telegram
        file = await context.bot.get_file(video.file_id)
        file_name = video.file_name or f"video_{video.file_id}.mp4"
        local_path = f"/tmp/{file_name}"
        await file.download_to_drive(local_path)
        
        await processing_msg.edit_text("☁️ Subiendo a Dropbox...")
        
        # Subir a Dropbox
        dropbox_path = f"{DROPBOX_FOLDER}/{file_name}"
        url = uploader.upload_file(local_path, dropbox_path)
        
        # Limpiar archivo temporal
        os.remove(local_path)
        
        # Mensaje de éxito
        success_msg = f"""
✅ *Video subido exitosamente*

🎥 *Nombre:* `{file_name}`
📏 *Tamaño:* {file_size_mb:.2f} MB
🔗 *Enlace:* [Ver en Dropbox]({url})
        """
        
        await processing_msg.edit_text(success_msg, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error al procesar video: {e}")
        await processing_msg.edit_text(f"❌ Error al subir video: {str(e)}")

def main():
    """Función principal para iniciar el bot"""
    try:
        # Crear la aplicación
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Registrar handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("status", status_command))
        
        # Handlers para diferentes tipos de archivos
        application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.VIDEO, handle_video))
        
        # Iniciar el bot
        logger.info("🚀 Bot iniciado correctamente")
        print("=" * 50)
        print("🤖 BOT DE TELEGRAM INICIADO")
        print("=" * 50)
        print("✅ El bot está funcionando")
        print("📱 Abre Telegram y busca tu bot")
        print("💬 Envía /start para comenzar")
        print("\n⏹️  Presiona Ctrl+C para detener el bot")
        print("=" * 50)
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Error al iniciar el bot: {e}")
        raise

if __name__ == '__main__':
    main()
