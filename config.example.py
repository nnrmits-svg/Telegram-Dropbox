# Configuración del Bot de Telegram y Dropbox
# ARCHIVO DE EJEMPLO - Copia este archivo a config.py y completa con tus credenciales

# ===== TELEGRAM BOT =====
# Token que obtuviste de BotFather
# Ejemplo: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_BOT_TOKEN = "TU_TOKEN_DE_TELEGRAM_AQUI"

# ===== DROPBOX =====
# Credenciales de tu app de Dropbox
# App Key - Ejemplo: "abc123xyz"
DROPBOX_APP_KEY = "TU_APP_KEY_AQUI"

# App Secret - Ejemplo: "abc123xyz456"
DROPBOX_APP_SECRET = "TU_APP_SECRET_AQUI"

# Refresh Token (se genera con generate_token.py)
DROPBOX_REFRESH_TOKEN = "TU_REFRESH_TOKEN_AQUI"

# ===== CONFIGURACIÓN ADICIONAL =====
# Carpeta en Dropbox donde se guardarán los archivos
# Puedes cambiar esto a cualquier ruta, ejemplo: "/MiCarpeta/Archivos"
DROPBOX_FOLDER = "/TelegramBot"

# Tamaño máximo de archivo en MB
# Telegram permite hasta 2GB, pero puedes limitar aquí
MAX_FILE_SIZE_MB = 20
