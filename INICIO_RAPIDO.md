# 🚀 GUÍA DE INICIO RÁPIDO

## ¿Ya tienes las APIs? ¡Perfecto! Sigue estos pasos:

### 📋 PASO 1: Configurar credenciales (5 minutos)

1. **Abre el archivo `config.py`**

2. **Completa con tus credenciales:**
   ```python
   TELEGRAM_BOT_TOKEN = "pega_aquí_tu_token_de_telegram"
   DROPBOX_APP_KEY = "pega_aquí_tu_app_key"
   DROPBOX_APP_SECRET = "pega_aquí_tu_app_secret"
   ```

3. **Guarda el archivo**

### 🔑 PASO 2: Generar Refresh Token (2 minutos)

```bash
python generate_token.py
```

- Ingresa tu App Key y App Secret cuando te lo pida
- Abre la URL que te muestra en el navegador
- Autoriza la app en Dropbox
- Copia el código que te da Dropbox
- Pégalo en el terminal
- **COPIA el Refresh Token** que te genera
- Pégalo en `config.py` en `DROPBOX_REFRESH_TOKEN`

### ✅ PASO 3: Verificar configuración (30 segundos)

```bash
python check_config.py
```

Esto verificará que todo está bien configurado. Si muestra errores, corrígelos.

### 🎯 PASO 4: ¡Ejecutar el bot! (1 minuto)

```bash
python bot.py
```

Si todo está bien, verás:
```
🤖 BOT DE TELEGRAM INICIADO
✅ El bot está funcionando
```

### 📱 PASO 5: Probar el bot

1. Abre Telegram
2. Busca tu bot por su username
3. Envía `/start`
4. Envía una foto o archivo
5. ¡Listo! El bot lo subirá a Dropbox

---

## ❓ ¿Problemas?

### "No encuentro config.py"
→ Copia `config.example.py` a `config.py`

### "AuthError de Dropbox"
→ Regenera el refresh token con `python generate_token.py`

### "El bot no responde"
→ Verifica que `python bot.py` esté ejecutándose

### "ModuleNotFoundError"
→ Instala dependencias: `pip install -r requirements.txt`

---

## 📚 ¿Necesitas más detalles?

Lee el archivo `README.md` para la guía completa paso a paso.

---

## ⚡ Resumen de comandos

```bash
# Instalar dependencias
pip install -r requirements.txt

# Generar refresh token (una sola vez)
python generate_token.py

# Verificar configuración
python check_config.py

# Ejecutar el bot
python bot.py
```

¡Eso es todo! 🎉
