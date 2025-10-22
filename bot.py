# =============================================
# CALIBELT 76 - BOT TELEGRAM (VERSION FINALE)
# Admin ID: 8313494819
# Annonce braderie Hash Dry 90u intégrée
# =============================================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
import asyncio
import os
import json
import hashlib

# === CONFIGURATION ===
BOT_TOKEN = "8210774698:AAEkMMI2hoduhKy1moKgpZ4c37C_rI5MRRI"  # À CHANGER SI TU VEUX
ADMIN_ID = 8313494819  # TON ID ADMIN

# === LOGGING ===
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# === STOCKAGE UTILISATEURS ===
USER_IDS = set()
USERS_FILE = "users.json"

def load_users():
    global USER_IDS
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                USER_IDS = set(json.load(f))
            logger.info(f"{len(USER_IDS)} utilisateurs chargés")
        except:
            USER_IDS = set()
    else:
        logger.info("users.json inexistant → démarrage vide")

def save_users():
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(USER_IDS), f)
        logger.info("users.json sauvegardé")
    except Exception as e:
        logger.error(f"Erreur sauvegarde users: {e}")

load_users()

# === CACHE MÉDIAS ===
MEDIA_CACHE = {}

def load_media(filename):
    if filename in MEDIA_CACHE:
        return MEDIA_CACHE[filename]
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            data = f.read()
            MEDIA_CACHE[filename] = data
            logger.info(f"Média chargé : {filename}")
            return data
    return None

# === CLAVIERS ===
def kb(data):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=cd)] for text, cd in data])

KEYBOARDS = {
    "start": kb([
        ("Menu", "menu"),
        ("Livraison", "delivery"),
        ("Meet-Up", "meet_up"),
        ("Contact", "https://t.me/Calibelt76"),
        ("Canal TG", "https://t.me/+NYNe1lR1HellMGI0"),
        ("Instagram", "https://instagram.com/calibelt76"),
        ("Potato", "https://ptwdym158.org/ARRA7Rz09H")
    ]),
    "menu": kb([("Hash", "hash"), ("Weed", "weed"), ("Retour", "back")]),
    "hash": kb([("Hash Dry 90u", "hash_dry"), ("90u KGF Frozen", "kgf_frozen"), ("Retour", "menu")]),
    "weed": kb([("CALI US", "cali_us"), ("Retour", "menu")]),
    "back": kb([("Retour au menu", "start")]),
    "delivery": kb([("Retour", "back")]),
    "meet_up": kb([("Retour", "back")])
}

# === ENVOI INTELLIGENT ===
async def send(update: Update, context: ContextTypes.DEFAULT_TYPE, text="", photo=None, video=None, caption="", kb=None):
    chat = update.effective_chat
    last_id = context.user_data.get("last_msg")
    if last_id:
        try: await context.bot.delete_message(chat.id, last_id)
        except: pass
    try:
        if photo:
            msg = await chat.send_photo(photo=photo, caption=caption, reply_markup=kb, parse_mode="Markdown")
        elif video:
            msg = await chat.send_video(video=video, caption=caption, reply_markup=kb, parse_mode="Markdown")
        else:
            msg = await chat.send_message(text=text, reply_markup=kb, parse_mode="Markdown")
        context.user_data["last_msg"] = msg.message_id
        return msg
    except Exception as e:
        logger.error(f"Erreur envoi: {e}")
        await chat.send_message("*Erreur temporaire. Réessaie.*", parse_mode="Markdown")
        return None

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    USER_IDS.add(user.id)
    save_users()
    logger.info(f"/start → {user.full_name} (@{user.username})")

    photo = load_media("start.jpg")
    await send(
        update, context,
        photo=photo,
        caption=(
            f"*Yo {user.first_name} !*\n\n"
            "Utilise le *menu* pour voir les produits\n"
            "Livraison 76 & Normandie\n"
            "Meet-up à Rouen"
        ),
        kb=KEYBOARDS["start"]
    )

# === /announce → BRADERIE HASH DRY 90u ===
async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Accès refusé.")
        return

    if not USER_IDS:
        await update.message.reply_text("Aucun utilisateur.")
        return

    text = (
        "*BRADERIE EXCLUSIVE*\n\n"
        "*Hash Dry 90u*\n"
        "*- California*\n"
        "*- Coco mangue*\n\n"
        "*120€ les 30G*\n"
        "*Hash Glassy d’où on brade les prix carré à fumer et faire curée*\n\n"
        "Dispo *livraison* & *meet-up Rouen*\n"
        "Contact : @Calibelt76\n"
        "*Premier arrivé, premier servi !*"
    )

    media = load_media("hash_promo.jpg") or load_media("hash_promo.mp4") or load_media("hash_dry.mp4")

    success = failed = 0
    total = len(USER_IDS)
    await update.message.reply_text(f"Envoi en cours... 0/{total}")

    for i, uid in enumerate(list(USER_IDS)):
        try:
            if media:
                await context.bot.send_photo(uid, photo=media, caption=text, parse_mode="Markdown")
            else:
                await context.bot.send_message(uid, text=text, parse_mode="Markdown")
            success += 1
            if i % 10 == 0:
                await update.message.edit_text(f"Envoi : {i}/{total}")
            await asyncio.sleep(0.035)  # Anti-flood
        except Exception as e:
            failed += 1
            logger.warning(f"Échec {uid}: {e}")

    await update.message.reply_text(
        f"*Annonce envoyée !*\n"
        f"Résultat: {success} | Échec: {failed}",
        parse_mode="Markdown"
    )
    logger.info(f"Annonce braderie envoyée → {success}/{total}")

# === BOUTONS ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "start":
        await start(update, context)

    elif data == "menu":
        await send(update, context, text="*Choisis :*", kb=KEYBOARDS["menu"])

    elif data == "hash":
        await send(update, context, text="*Hash dispo :*", kb=KEYBOARDS["hash"])

    elif data == "hash_dry":
        video = load_media("hash_dry.mp4")
        await send(
            update, context,
            video=video,
            caption=(
                "*Hash Dry 90u*\n"
                "*- California*\n"
                "*- Coco mangue*\n\n"
                "5G → 50€\n"
                "10G → 80€\n"
                "*30G → 120€ (BRADERIE !)*"
            ),
            kb=KEYBOARDS["back"]
        )

    elif data == "kgf_frozen":
        video = load_media("kgf_frozen.mp4")
        await send(
            update, context,
            video=video,
            caption=(
                "*90u KGF Frozen*\n"
                "*- Lamponi*\n\n"
                "5G → 60€\n"
                "10G → 120€\n"
                "25G → 260€"
            ),
            kb=KEYBOARDS["back"]
        )

    elif data == "cali_us":
        video = load_media("cali_us.mp4")
        await send(
            update, context,
            video=video,
            caption=(
                "*CALI US*\n"
                "*- Cherry Bomb*\n\n"
                "5G → 70€\n"
                "10G → 140€\n"
                "25G → 330€"
            ),
            kb=KEYBOARDS["back"]
        )

    elif data == "delivery":
        await send(
            update, context,
            text=(
                "*LIVRAISON*\n\n"
                "*76/27/14 + Normandie*\n"
                "Frais : 10-20€/km\n"
                "Ex : 100km → 450€\n\n"
                "*Contact : @Calibelt76*"
            ),
            kb=KEYBOARDS["delivery"]
        )

    elif data == "meet_up":
        await send(
            update, context,
            text=(
                "*MEET-UP ROUEN*\n\n"
                "Passe directement\n"
                "Préviens en privé avant\n\n"
                "*@Calibelt76*"
            ),
            kb=KEYBOARDS["meet_up"]
        )

# === /stop ===
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in USER_IDS:
        USER_IDS.remove(uid)
        save_users()
        await update.message.reply_text("Tu ne recevras plus d'annonces.")
    else:
        await update.message.reply_text("Tu n’étais pas inscrit.")

# === DEMARRAGE ===
if __name__ == "__main__":
    logger.info("Démarrage du bot CALIBELT 76 - Admin: 8313494819")
    print("BOT CALIBELT 76 EN LIGNE")
    print("Envoie /announce pour lancer la braderie Hash Dry 90u !")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("announce", announce))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CallbackQueryHandler(button))

    try:
        app.run_polling(drop_pending_updates=True, timeout=30)
    except KeyboardInterrupt:
        logger.info("Bot arrêté manuellement")
    except Exception as e:
        logger.critical(f"ERREUR FATALE: {e}")
