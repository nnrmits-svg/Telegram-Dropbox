# 🤖 Bot de Telegram - Dropbox

Bot de Telegram que sube automáticamente archivos a Dropbox y devuelve enlaces de descarga.

## 📋 ¿Qué hace este bot?

- ✅ Recibe archivos por Telegram (fotos, documentos, videos)
- ☁️ Los sube automáticamente a tu Dropbox
- 🔗 Te devuelve un enlace de descarga directo
- 📱 Fácil de usar - solo envía el archivo

## 🚀 GUÍA DE CONFIGURACIÓN

### PASO 1: Crear el Bot de Telegram

1. **Abre Telegram** y busca `@BotFather`

2. **Envía el comando:** `/newbot`

3. **Sigue las instrucciones:**
   - Te pedirá un nombre para el bot (ej: "Mi Bot de Dropbox")
   - Te pedirá un username (debe terminar en 'bot', ej: "midropboxbot")

4. **Copia el token** que te da BotFather
   - Se ve así: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - 🔴 **¡GUÁRDALO! Lo necesitarás después**

### PASO 2: Crear la App de Dropbox

1. **Ve a:** https://www.dropbox.com/developers/apps

2. **Haz clic en** "Create app"

3. **Configura la app:**
   - Choose an API: **Scoped access**
   - Choose the type of access: **Full Dropbox** (o "App folder" si prefieres)
   - Name your app: Pon un nombre único (ej: "TelegramBotApp")
   - Acepta los términos y crea la app

4. **En la página de tu app:**
   
   **a) Copia las credenciales:**
   - **App key** (se ve así: `abc123xyz`)
   - **App secret** (se ve así: `abc123xyz456`)
   - 🔴 **¡GUÁRDALOS! Los necesitarás después**
   
   **b) Configura los permisos:**
   - Ve a la pestaña "Permissions"
   - Activa estos permisos:
     - ✅ `files.metadata.write`
     - ✅ `files.content.write`
     - ✅ `files.content.read`
     - ✅ `sharing.write`
   - Haz clic en "Submit"

### PASO 3: Instalar Python y Dependencias

1. **Verifica que tienes Python instalado:**
   ```bash
   python --version
   ```
   (Necesitas Python 3.7 o superior)

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

### PASO 4: Generar el Refresh Token de Dropbox

Este es un paso crucial. El refresh token permite que el bot acceda a tu Dropbox.

1. **Ejecuta el script:**
   ```bash
   python generate_token.py
   ```

2. **Sigue las instrucciones:**
   - Te pedirá tu App Key y App Secret
   - Te dará una URL para abrir en el navegador
   - Autoriza la aplicación en Dropbox
   - Copia el código que te muestra
   - Pégalo en el script

3. **Copia el Refresh Token** que te genera
   - 🔴 **¡GUÁRDALO! Lo necesitarás en el siguiente paso**

### PASO 5: Configurar las Credenciales

1. **Abre el archivo `config.py`**

2. **Reemplaza los valores:**
   ```python
   # ===== TELEGRAM BOT =====
   TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Token de BotFather

   # ===== DROPBOX =====
   DROPBOX_APP_KEY = "abc123xyz"              # App Key de Dropbox
   DROPBOX_APP_SECRET = "abc123xyz456"        # App Secret de Dropbox
   DROPBOX_REFRESH_TOKEN = "tu_refresh_token" # Token generado en PASO 4

   # ===== CONFIGURACIÓN ADICIONAL =====
   DROPBOX_FOLDER = "/TelegramBot"  # Carpeta donde se guardarán los archivos
   MAX_FILE_SIZE_MB = 20            # Tamaño máximo de archivo permitido
   ```

3. **Guarda el archivo**

### PASO 6: ¡Ejecutar el Bot!

1. **Inicia el bot:**
   ```bash
   python bot.py
   ```

2. **Si todo está bien, verás:**
   ```
   ==================================================
   🤖 BOT DE TELEGRAM INICIADO
   ==================================================
   ✅ El bot está funcionando
   📱 Abre Telegram y busca tu bot
   💬 Envía /start para comenzar
   
   ⏹️  Presiona Ctrl+C para detener el bot
   ==================================================
   ```

3. **Abre Telegram y busca tu bot**
   - Búscalo por el username que elegiste
   - Envía `/start`
   - ¡Envía un archivo para probar!

## 📱 Cómo Usar el Bot

### Comandos disponibles:
- `/start` - Mensaje de bienvenida
- `/help` - Ayuda y guía de uso
- `/status` - Ver estado de las conexiones

### Enviar archivos:
1. **Envía cualquier archivo** al bot:
   - 📷 Fotos
   - 📄 Documentos (PDF, Word, Excel, etc.)
   - 🎥 Videos
   - 🎵 Audio
   - 📦 Archivos comprimidos

2. **Espera la confirmación**
   - El bot descargará el archivo
   - Lo subirá a tu Dropbox
   - Te enviará el enlace de descarga

3. **Recibe el enlace**
   - El enlace permite descarga directa
   - Los archivos se guardan en `/TelegramBot` en tu Dropbox

## 🔧 Configuración Avanzada

### Cambiar la carpeta de destino:
Edita `config.py`:
```python
DROPBOX_FOLDER = "/MisCarpeta/Subcarpeta"
```

### Cambiar el límite de tamaño:
Edita `config.py`:
```python
MAX_FILE_SIZE_MB = 50  # Permite archivos de hasta 50MB
```

## ❗ Solución de Problemas

### Error: "AuthError"
- ✅ Verifica que el Refresh Token sea correcto
- ✅ Regenera el token ejecutando `generate_token.py`

### Error: "Bad Request: wrong file_id"
- ✅ El archivo puede ser muy antiguo
- ✅ Intenta enviar un archivo nuevo

### Error: "File too large"
- ✅ El archivo excede el límite configurado
- ✅ Comprime el archivo o aumenta `MAX_FILE_SIZE_MB`

### El bot no responde
- ✅ Verifica que el bot esté ejecutándose (`python bot.py`)
- ✅ Verifica que el token de Telegram sea correcto
- ✅ Revisa los logs en la terminal

### Error: "No space left on device"
- ✅ Verifica que tengas espacio en Dropbox
- ✅ El bot descarga archivos a `/tmp`, asegúrate de tener espacio local

## 🔒 Seguridad

- ⚠️ **NO compartas** tu Token de Telegram
- ⚠️ **NO compartas** tus credenciales de Dropbox
- ⚠️ **NO subas** `config.py` a repositorios públicos
- ✅ Usa variables de entorno en producción
- ✅ Mantén actualizado el bot

## 📁 Estructura del Proyecto

```
telegram-dropbox-bot/
│
├── bot.py              # Script principal del bot
├── config.py           # Configuración y credenciales
├── generate_token.py   # Script para generar refresh token
├── requirements.txt    # Dependencias de Python
└── README.md          # Este archivo
```

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa los logs en la terminal
2. Verifica que todas las credenciales sean correctas
3. Asegúrate de haber completado todos los pasos
4. Verifica que los permisos de Dropbox estén configurados

## 📝 Notas Importantes

- El bot debe estar ejecutándose para funcionar (no se detiene automáticamente)
- Los archivos se descargan temporalmente a `/tmp` y se eliminan después de subirse
- El enlace de Dropbox es público para quien lo tenga
- Puedes detener el bot con `Ctrl+C`

## ✅ Checklist de Configuración

Antes de ejecutar el bot, asegúrate de tener:

- [ ] Token de Telegram Bot (de BotFather)
- [ ] App Key de Dropbox
- [ ] App Secret de Dropbox
- [ ] Refresh Token generado
- [ ] Permisos configurados en Dropbox
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `config.py` configurado con todos los valores

¡Listo! 🎉
