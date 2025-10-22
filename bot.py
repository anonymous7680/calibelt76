from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
import asyncio
import os
import json

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# NOUVEAU TOKEN
BOT_TOKEN = "8210774698:AAEkMMI2hoduhKy1moKgpZ4c37C_rI5MRRI"

# Cache pour les fichiers médias
MEDIA_CACHE = {}

# Ensemble pour stocker les IDs des utilisateurs
USER_IDS = set()

# Fonction pour charger les utilisateurs
def load_users():
    try:
        with open("users.json", "r") as f:
            USER_IDS.update(json.load(f))
        logger.info(f"Chargement de {len(USER_IDS)} utilisateurs depuis users.json")
    except FileNotFoundError:
        logger.info("Fichier users.json non trouvé, démarrage avec une liste vide")

# Fonction pour sauvegarder les utilisateurs
def save_users():
    with open("users.json", "w") as f:
        json.dump(list(USER_IDS), f)
    logger.info("Utilisateurs sauvegardés dans users.json")

# Cache des claviers
KEYBOARD_CACHE = {
    "start": InlineKeyboardMarkup([
        [InlineKeyboardButton("Menu", callback_data="menu")],
        [InlineKeyboardButton("Service Livraison", callback_data="delivery")],
        [InlineKeyboardButton("Service Meet-Up", callback_data="meet_up")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+NYNe1lR1HellMGI0")],
        [InlineKeyboardButton("Instagram", url="https://www.instagram.com/calibelt76?igsh=b3ZjMGo4dGMxc2tz&utm_source=qr")],
        [InlineKeyboardButton("Canal Potato", url="https://ptwdym158.org/ARRA7Rz09H")]
    ]),
    "menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("Hash", callback_data="hash")],
        [InlineKeyboardButton("Weed", callback_data="weed")],
        [InlineKeyboardButton("Retour", callback_data="back")]
    ]),
    "hash": InlineKeyboardMarkup([
        [InlineKeyboardButton("Hash Dry 90u", callback_data="hash_dry")],
        [InlineKeyboardButton("90u kgf Frozen", callback_data="kgf_frozen")],
        [InlineKeyboardButton("Retour", callback_data="menu")]
    ]),
    "hash_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour", callback_data="menu")]
    ]),
    "weed": InlineKeyboardMarkup([
        [InlineKeyboardButton("CALI US", callback_data="cali_us")],
        [InlineKeyboardButton("Retour", callback_data="menu")]
    ]),
    "weed_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour", callback_data="weed")]
    ]),
    "back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Menu", callback_data="menu")],
        [InlineKeyboardButton("Service Livraison", callback_data="delivery")],
        [InlineKeyboardButton("Service Meet-Up", callback_data="meet_up")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+NYNe1lR1HellMGI0")],
        [InlineKeyboardButton("Instagram", url="https://www.instagram.com/calibelt76?igsh=b3ZjMGo4dGMxc2tz&utm_source=qr")],
        [InlineKeyboardButton("Canal Potato", url="https://ptwdym158.org/ARRA7Rz09H")]
    ]),
    "meet_up": InlineKeyboardMarkup([
        [InlineKeyboardButton("Retour", callback_data="back")]
    ]),
    "delivery": InlineKeyboardMarkup([
        [InlineKeyboardButton("Retour", callback_data="back")]
    ])
}

# Fonction d'envoi ou édition de message
async def send_or_edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, photo=None, video=None, caption=None):
    chat = update.effective_chat
    if context.user_data.get('sending_message'):
        return None
    context.user_data['sending_message'] = True
    last_message_id = context.user_data.get('last_bot_message_id')
    if last_message_id:
        try:
            await asyncio.shield(chat.delete_message(last_message_id))
        except Exception as e:
            logger.warning(f"Erreur suppression message {last_message_id}: {e}")
    try:
        if photo:
            sent_message = await chat.send_photo(photo=photo, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
        elif video:
            sent_message = await chat.send_video(video=video, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            sent_message = await chat.send_message(text=text, reply_markup=reply_markup, parse_mode="Markdown")
        context.user_data['last_bot_message_id'] = sent_message.message_id
        return sent_message
    except Exception as e:
        logger.error(f"Erreur envoi message: {e}")
        await chat.send_message("*Une erreur s'est produite. Réessaie.*", parse_mode="Markdown")
        return None
    finally:
        context.user_data['sending_message'] = False

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    username = f"@{user.username}" if user.username else "Pas de @"
    USER_IDS.add(user.id)
    save_users()
    logger.info(f"/start de {name} ({username}) - ID: {user.id}")
    reply_markup = KEYBOARD_CACHE["start"]
    try:
        photo = MEDIA_CACHE.get("chat.JPG")
        if photo is None:
            with open("chat.JPG", "rb") as image:
                photo = image.read()
                MEDIA_CACHE["chat.JPG"] = photo
        await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
            caption=(
                f"*Bienvenue {name} sur notre Bot Télégram*\n\n"
                "*/start - Redémarrer*\n"
                "*Consulte le menu ci-dessous*"
            ))
    except FileNotFoundError:
        await send_or_edit_message(update, context,
            text=f"*Bienvenue {name}*\n*/start - Redémarrer*\n*Utilise les boutons*", reply_markup=reply_markup)

# /listusers (admin)
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ADMIN_ID = 123456789  # À CHANGER avec ton ID
    if user.id != ADMIN_ID:
        await update.message.reply_text("Commande admin uniquement.")
        return
    if not USER_IDS:
        await update.message.reply_text("Aucun utilisateur.")
    else:
        user_list = "\n".join([f"ID: {uid}" for uid in USER_IDS])
        await update.message.reply_text(f"Utilisateurs :\n{user_list}")

# /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = f"@{update.effective_user.username}" if update.effective_user.username else "Pas de @"
    if user_id in USER_IDS:
        USER_IDS.remove(user_id)
        save_users()
        await update.message.reply_text("Tu ne recevras plus d'annonces. /start pour revenir.")
        logger.info(f"{username} s'est désinscrit")
    else:
        await update.message.reply_text("Tu n'es pas inscrit.")

# ANNONCE AUTOMATIQUE AU DÉMARRAGE
async def auto_announce(context: ContextTypes.DEFAULT_TYPE):
    announcement = (
        "*Hash Dry 90u*\n\n"
        "- *California* [flag_us]\n"
        "- *Coco mangue* [coconut] [mango]\n\n"
        "*120€ 30G hash dry 90U* [handshake]\n"
        "*Hash Glassy d’où on brade les prix carré à fumer et faire curée* [fire] [check]\n\n"
        "*/start pour commander*"
    )
    success = 0
    failed = 0
    for user_id in list(USER_IDS):
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=announcement,
                parse_mode="Markdown"
            )
            success += 1
            await asyncio.sleep(0.1)  # Anti-flood
        except Exception as e:
            logger.error(f"Échec envoi à {user_id}: {e}")
            failed += 1
    logger.info(f"Annonce auto envoyée : {success} OK, {failed} échecs")

# Gestion des boutons
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    username = f"@{user.username}" if user.username else "Pas de @"
    await query.answer()
    logger.info(f"Bouton '{query.data}' par {user.first_name} ({username})")

    if query.data == "menu":
        await send_or_edit_message(update, context, "*Choisis une option :*", reply_markup=KEYBOARD_CACHE["menu"])
    elif query.data == "delivery":
        await send_or_edit_message(update, context,
            "*SERVICE L*VRA*SON*\n\n"
            "*76 /27/14 et Normandie*\n"
            "*76 → 30-50€*\n"
            "*+10-20€/km*\n\n"
            "*Contact: @calibelt76*",
            reply_markup=KEYBOARD_CACHE["delivery"])
    elif query.data == "meet_up":
        await send_or_edit_message(update, context,
            "*MEET-UP ROUEN 76*\n\n"
            "RDV direct, préviens en privé avant.\n\n"
            "*@calibelt76*",
            reply_markup=KEYBOARD_CACHE["meet_up"])
    elif query.data == "hash":
        await send_or_edit_message(update, context, "*Hash*", reply_markup=KEYBOARD_CACHE["hash"])
    elif query.data == "hash_dry":
        try:
            video = MEDIA_CACHE.get("hash_dry.mp4")
            if not video:
                with open("hash_dry.mp4", "rb") as f:
                    video = f.read()
                    MEDIA_CACHE["hash_dry.mp4"] = video
            await send_or_edit_message(update, context, "", video=video,
                caption="*Hash Dry 90u*\n\n"
                        "- California\n"
                        "- Coco mangue\n\n"
                        "5G 50€ │ 10G 80€ │ 20G 160€ │ 25G 200€ │ 50G 350€",
                reply_markup=KEYBOARD_CACHE["hash_back"])
        except FileNotFoundError:
            await query.message.reply_text("*Vidéo manquante.*")
    elif query.data == "kgf_frozen":
        try:
            video = MEDIA_CACHE.get("kgf_frozen.mp4")
            if not video:
                with open("kgf_frozen.MP4", "rb") as f:
                    video = f.read()
                    MEDIA_CACHE["kgf_frozen.MP4"] = video
            await send_or_edit_message(update, context, "", video=video,
                caption="*90u kgf Frozen*\n\n"
                        "*Lamponi*\n\n"
                        "5G 60€ │ 10G 120€ │ 20G 230€ │ 25G 260€",
                reply_markup=KEYBOARD_CACHE["hash_back"])
        except FileNotFoundError:
            await query.message.reply_text("*Vidéo manquante.*")
    elif query.data == "weed":
        await send_or_edit_message(update, context, "*Weed*", reply_markup=KEYBOARD_CACHE["weed"])
    elif query.data == "cali_us":
        try:
            video = MEDIA_CACHE.get("cali_us.mp4")
            if not video:
                with open("cali_us.mp4", "rb") as f:
                    video = f.read()
                    MEDIA_CACHE["cali_us.mp4"] = video
            await send_or_edit_message(update, context, "", video=video,
                caption="*CALI US*\n\n"
                        "*Cherry Bomb*\n\n"
                        "5G 70€ │ 10G 140€ │ 20G 270€ │ 25G 330€",
                reply_markup=KEYBOARD_CACHE["weed_back"])
        except FileNotFoundError:
            await query.message.reply_text("*Vidéo manquante.*")
    elif query.data == "back":
        reply_markup = KEYBOARD_CACHE["back"]
        try:
            photo = MEDIA_CACHE.get("chat.JPG")
            if not photo:
                with open("chat.JPG", "rb") as f:
                    photo = f.read()
                    MEDIA_CACHE["chat.JPG"] = photo
            await send_or_edit_message(update, context, "", photo=photo,
                caption=f"*Bienvenue {user.first_name}*\n*/start - Redémarrer*\n*Menu ci-dessous*",
                reply_markup=reply_markup)
        except FileNotFoundError:
            await send_or_edit_message(update, context,
                f"*Bienvenue {user.first_name}*\n*/start - Redémarrer*", reply_markup=reply_markup)

# Lancement du bot + annonce auto
if __name__ == "__main__":
    try:
        load_users()
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("listusers", list_users))
        app.add_handler(CommandHandler("stop", stop))
        app.add_handler(CallbackQueryHandler(button_click))

        # PLANIFIER L'ANNONCE AU DÉMARRAGE
        async def start_with_announce():
            await app.initialize()
            await app.start()
            await app.updater.start_polling()

            # Attendre que le bot soit prêt
            await asyncio.sleep(3)

            # Envoyer l'annonce à tous
            job_queue = app.job_queue
            job_queue.run_once(auto_announce, when=1)

            print("Bot lancé + Annonce auto envoyée")
            logger.info("Bot démarré et annonce automatique lancée")

            # Garder le bot en vie
            await asyncio.Event().wait()

        asyncio.run(start_with_announce())

    except Exception as e:
        logger.error(f"Erreur critique : {e}")
