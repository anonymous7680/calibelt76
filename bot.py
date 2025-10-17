from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, JobQueue
import logging
import asyncio
import os
import json
from datetime import timedelta

# Configuration du logging avec fichier
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),  # Sauvegarde les logs dans bot.log
        logging.StreamHandler()  # Affiche aussi dans la console
    ]
)
logger = logging.getLogger(__name__)

# Charge les variables d'environnement
BOT_TOKEN = os.getenv("BOT_TOKEN", "8139705130:AAH-3uo8OMmNS79hzWJFuLwYOdeDacfNch8")

# Cache pour les fichiers médias
MEDIA_CACHE = {}

# Ensemble pour stocker les IDs des utilisateurs ayant utilisé le bot
USER_IDS = set()

# Fonction pour charger les utilisateurs depuis un fichier JSON
def load_users():
    try:
        with open("users.json", "r") as f:
            USER_IDS.update(json.load(f))
        logger.info(f"Chargement de {len(USER_IDS)} utilisateurs depuis users.json")
    except FileNotFoundError:
        logger.info("Fichier users.json non trouvé, démarrage avec une liste vide")

# Fonction pour sauvegarder les utilisateurs dans un fichier JSON
def save_users():
    with open("users.json", "w") as f:
        json.dump(list(USER_IDS), f)
    logger.info("Utilisateurs sauvegardés dans users.json")

# Cache pour les claviers réutilisés
KEYBOARD_CACHE = {
    "start": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
        [InlineKeyboardButton("Service Livraison", callback_data="delivery")],
        [InlineKeyboardButton("Service Meet-Up", callback_data="meet_up")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+NYNe1lR1HellMGI0")],
        [InlineKeyboardButton("Instagram", url="https://www.instagram.com/calibelt76?igsh=b3ZjMGo4dGMxc2tz&utm_source=qr")],
        [InlineKeyboardButton("Canal Potato", url="https://ptwdym158.org/ARRA7Rz09H")]
    ]),
    "menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("Hash 🍫", callback_data="hash")],
        [InlineKeyboardButton("Weed 🌳", callback_data="weed")],
        [InlineKeyboardButton("🔙 Retour", callback_data="back")]
    ]),
    "hash": InlineKeyboardMarkup([
        [InlineKeyboardButton("Hash Dry 90u", callback_data="hash_dry")],
        [InlineKeyboardButton("90u kgf Frozen 🧊", callback_data="kgf_frozen")],
        [InlineKeyboardButton("🔙 Retour", callback_data="menu")]
    ]),
    "hash_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour 🔙", callback_data="menu")]
    ]),
    "weed": InlineKeyboardMarkup([
        [InlineKeyboardButton("CALI US 🇺🇸", callback_data="cali_us")],
        [InlineKeyboardButton("🔙 Retour", callback_data="menu")]
    ]),
    "weed_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour 🔙", callback_data="weed")]
    ]),
    "back": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
        [InlineKeyboardButton("Service Livraison", callback_data="delivery")],
        [InlineKeyboardButton("Service Meet-Up", callback_data="meet_up")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+NYNe1lR1HellMGI0")],
        [InlineKeyboardButton("Instagram", url="https://www.instagram.com/calibelt76?igsh=b3ZjMGo4dGMxc2tz&utm_source=qr")],
        [InlineKeyboardButton("Canal Potato", url="https://ptwdym158.org/ARRA7Rz09H")]
    ]),
    "meet_up": InlineKeyboardMarkup([
        [InlineKeyboardButton("Retour 🔙", callback_data="back")]
    ]),
    "delivery": InlineKeyboardMarkup([
        [InlineKeyboardButton("Retour 🔙", callback_data="back")]
    ])
}

async def send_or_edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, photo=None, video=None, caption=None):
    chat = update.effective_chat
    logger.info(f"Envoi d'un message à {chat.id}")
    if context.user_data.get('sending_message'):
        logger.warning("Message déjà en cours d'envoi, annulation.")
        return None
    context.user_data['sending_message'] = True
    last_message_id = context.user_data.get('last_bot_message_id')
    if last_message_id:
        try:
            await asyncio.shield(chat.delete_message(last_message_id))
            logger.info(f"Message {last_message_id} supprimé")
        except Exception as e:
            logger.warning(f"Erreur lors de la suppression du message {last_message_id}: {e}")
    try:
        if photo:
            sent_message = await chat.send_photo(photo=photo, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
        elif video:
            sent_message = await chat.send_video(video=video, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            sent_message = await chat.send_message(text=text, reply_markup=reply_markup, parse_mode="Markdown")
        context.user_data['last_bot_message_id'] = sent_message.message_id
        logger.info(f"Nouveau message envoyé, ID: {sent_message.message_id}")
        return sent_message
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message: {e}")
        await chat.send_message("*Une erreur s'est produite. Essaie à nouveau.*", parse_mode="Markdown")
        return None
    finally:
        context.user_data['sending_message'] = False

# /start avec log du @username
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    username = user.username
    username_str = f"@{username}" if username else "Pas de @"
    USER_IDS.add(user.id)
    save_users()  # Sauvegarde après ajout
    logger.info(f"Commande /start reçue de {name} ({username_str}), ID ajouté: {user.id}")
    reply_markup = KEYBOARD_CACHE["start"]
    try:
        photo = MEDIA_CACHE.get("chat.JPG")
        if photo is None:
            logger.warning("Fichier chat.JPG non en cache, chargement direct")
            with open("chat.JPG", "rb") as image:
                photo = image.read()
                MEDIA_CACHE["chat.JPG"] = photo
        await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
            caption=(
                f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                "*/start - Pour redémarrer le Bot*\n"
                "*Ce Bot te servira à consulter notre menu 📖*\n"
                "*👉 Utilise les boutons ci-dessous 👇*"
            ))
    except FileNotFoundError:
        logger.error("Fichier chat.JPG introuvable, envoi du message sans image")
        await send_or_edit_message(update, context,
            text=(
                f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                "*/start - Pour redémarrer le Bot*\n"
                "*Ce Bot te servira à consulter notre menu 📖*\n"
                "*👉 Utilise les boutons ci-dessous 👇*"
            ),
            reply_markup=reply_markup)

# /listusers pour admin
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ADMIN_ID = 123456789  # Remplace par ton ID Telegram (@userinfobot pour le trouver)
    if user.id != ADMIN_ID:
        await update.message.reply_text("Désolé, cette commande est réservée aux administrateurs.")
        logger.info(f"Tentative /listusers par non-admin {user.id}")
        return
    if not USER_IDS:
        await update.message.reply_text("Aucun utilisateur n'a utilisé le bot pour le moment.")
        logger.info("Commande /listusers exécutée : aucun utilisateur")
    else:
        user_list = "\n".join([f"ID: {uid}" for uid in USER_IDS])
        await update.message.reply_text(f"Utilisateurs ayant utilisé le bot :\n{user_list}")
        logger.info(f"Commande /listusers exécutée par admin {user.id} - {len(USER_IDS)} utilisateurs")

# /stop pour se désinscrire des annonces
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    username_str = f"@{username}" if username else "Pas de @"
    if user_id in USER_IDS:
        USER_IDS.remove(user_id)
        save_users()
        await update.message.reply_text("Vous ne recevrez plus d'annonces. Utilisez /start pour vous réinscrire.")
        logger.info(f"Utilisateur {username_str} (ID: {user_id}) s'est désinscrit des annonces")
    else:
        await update.message.reply_text("Vous n'êtes pas inscrit aux annonces.")
        logger.info(f"Utilisateur {username_str} (ID: {user_id}) a tenté de se désinscrire mais n'était pas inscrit")

# Fonction d'annonce pour le nouvel arrivage (envoyée à tous les utilisateurs qui ont utilisé /start)
async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ADMIN_ID = 123456789  # Remplace par ton ID Telegram (@userinfobot pour le trouver)
    if user.id != ADMIN_ID:
        await update.message.reply_text("Désolé, cette commande est réservée aux administrateurs.")
        logger.info(f"Tentative /announce par non-admin {user.id}")
        return
    if not USER_IDS:
        await update.message.reply_text("Aucun utilisateur à notifier.")
        logger.info("Commande /announce exécutée : aucun utilisateur")
        return
    announcement_text = (
        "*🔥 NOUVEL ARRIVAGE ! 🔥*\n\n"
        "Découvrez notre nouveau produit : *90u kgf Frozen 🧊*\n\n"
        "*🦊 BY KGF x TERPHOGZ 🦊*\n"
        "*Une Des Meilleurs Farm Sur le marché il est méchant la Team 🔥*\n\n"
        "*-Lamponi 🍦🍓*\n\n"
        "*-5G 60€*\n"
        "*-10G 120€*\n"
        "*-20G 230€*\n"
        "*-25G 260€*\n\n"
        "Consultez le menu avec /start pour plus de détails ! 📋"
    )
    success_count = 0
    failed_count = 0
    for user_id in USER_IDS:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=announcement_text,
                parse_mode="Markdown"
            )
            success_count += 1
            logger.info(f"Annonce envoyée à l'utilisateur {user_id}")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'annonce à {user_id}: {e}")
            failed_count += 1
    await update.message.reply_text(
        f"Annonce envoyée avec succès à {success_count} utilisateurs. "
        f"Échecs : {failed_count}."
    )
    logger.info(f"Commande /announce exécutée par admin {user.id} - Succès: {success_count}, Échecs: {failed_count}")

# Gestion des clics sur boutons avec log du @username
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    name = user.first_name
    username = user.username
    username_str = f"@{username}" if username else "Pas de @"
    await query.answer()
    logger.info(f"Bouton cliqué '{query.data}' par {name} ({username_str}), ID: {user.id}")
    if query.data == "menu":
        await send_or_edit_message(update, context,
            text="*Choisis une option dans le menu :*",
            reply_markup=KEYBOARD_CACHE["menu"])
    elif query.data == "delivery":
        await send_or_edit_message(update, context,
            text="*SERVICE L*VRA*SON 🚚*\n\n"
                 "*Service Livraison dans toute la Normandie et c’est Alentour*\n"
                 "*76 /27/14 et tout la Normandie ! 🗺️ 🚚*\n\n"
                 "*76 30-50e*\n"
                 "—————————\n"
                 "*10 à 20e de Frais Par Klm.*\n\n"
                 "*-30klm-110*\n\n"
                 "*-50Klm - 250e*\n\n"
                 "*-70klm- 340e*\n\n"
                 "*-100Klm - 450e*\n\n"
                 "*Contact: @calibelt76🐺*",
            reply_markup=KEYBOARD_CACHE["delivery"])
    elif query.data == "meet_up":
        await send_or_edit_message(update, context,
            text="*SERVICE MEET-UP 🏠*\n\n"
                 "*ROUEN 76 📍*\n\n"
                 "Vous pouvez directement passer et meet-up la miff 🚶 ✈️\n\n"
                 "Prévenir et faire votre com*and Juste avant de passer en privé.\n\n"
                 "*@calibelt76 🐺*",
            reply_markup=KEYBOARD_CACHE["meet_up"])
    elif query.data == "hash":
        await send_or_edit_message(update, context,
            text="*Choisis une option pour Hash 🍫 :*",
            reply_markup=KEYBOARD_CACHE["hash"])
    elif query.data == "hash_dry":
        reply_markup = KEYBOARD_CACHE["hash_back"]
        try:
            video = MEDIA_CACHE.get("hash_dry.MP4")
            if video is None:
                logger.warning("Fichier hash_dry.mp4 non en cache, chargement direct")
                with open("hash_dry.mp4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["hash_dry.mp4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*Hash Dry 90u*\n\n"
                        "*- California 🌴🇺🇸*\n"
                        "*- Coco mangue 🥥🥭*\n\n"
                        "*-5G 50€*\n\n"
                        "*-10G 80€*\n\n"
                        "*-20G 160€*\n\n"
                        "*-25G 200€*\n\n"
                        "*-50G 350€*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier hash_dry.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo hash_dry.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "kgf_frozen":
        reply_markup = KEYBOARD_CACHE["hash_back"]
        try:
            video = MEDIA_CACHE.get("kgf_frozen.mp4")
            if video is None:
                logger.warning("Fichier kgf_frozen.MP4 non en cache, chargement direct")
                with open("kgf_frozen.MP4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["kgf_frozen.MP4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*90u kgf Frozen 🧊*\n\n"
                        "*🦊 BY KGF x TERPHOGZ 🦊*\n"
                        "*Une Des Meilleurs Farm Sur le marché il est méchant la Team 🔥*\n\n"
                        "*-Lamponi 🍦🍓*\n\n"
                        "*-5G 60€*\n\n"
                        "*-10G 120€*\n\n"
                        "*-20G 230€*\n\n"
                        "*-25G 260€*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier kgf_frozen.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo kgf_frozen.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "weed":
        await send_or_edit_message(update, context,
            text="*Choisis une option pour Weed 🌳 :*",
            reply_markup=KEYBOARD_CACHE["weed"])
    elif query.data == "cali_us":
        reply_markup = KEYBOARD_CACHE["weed_back"]
        try:
            video = MEDIA_CACHE.get("cali_us.MP4")
            if video is None:
                logger.warning("Fichier cali_us.mp4 non en cache, chargement direct")
                with open("cali_us.mp4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["cali_us.mp4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*CALI US 🇺🇸*\n\n"
                        "*- Cherry Bomb 🍒🍦💣*\n\n"
                        "*-5G 70€*\n\n"
                        "*-10G 140€*\n\n"
                        "*-20G 270€*\n\n"
                        "*-25G 330€*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier cali_us.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo cali_us.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "back":
        user = update.effective_user
        name = user.first_name
        username = user.username
        username_str = f"@{username}" if username else "Pas de @"
        logger.info(f"Bouton 'back' cliqué par {name} ({username_str}), ID: {user.id}")
        reply_markup = KEYBOARD_CACHE["back"]
        try:
            photo = MEDIA_CACHE.get("chat.JPG")
            if photo is None:
                logger.warning("Fichier chat.JPG non en cache, chargement direct")
                with open("chat.JPG", "rb") as image:
                    photo = image.read()
                    MEDIA_CACHE["chat.JPG"] = photo
            await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
                caption=(
                    f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                    "*/start - Pour redémarrer le Bot*\n"
                    "*Ce Bot te servira à consulter notre menu 📖*\n"
                    "*👉 Utilise les boutons ci-dessous 👇*"
                ))
        except FileNotFoundError:
            logger.error("Fichier chat.JPG introuvable, envoi du message sans image")
            await send_or_edit_message(update, context,
                text=(
                    f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                    "*/start - Pour redémarrer le Bot*\n"
                    "*Ce Bot te servira à consulter notre menu 📖*\n"
                    "*👉 Utilise les boutons ci-dessous 👇*"
                ),
                reply_markup=reply_markup)

# /photo optionnel
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username
    username_str = f"@{username}" if username else "Pas de @"
    logger.info(f"Commande /photo exécutée par {user.first_name} ({username_str}), ID: {user.id}")
    try:
        photo = MEDIA_CACHE.get("chat.JPG")
        if photo is None:
            logger.warning("Fichier chat.JPG non en cache, chargement direct")
            with open("chat.JPG", "rb") as image:
                photo = image.read()
                MEDIA_CACHE["chat.JPG"] = photo
        await send_or_edit_message(update, context, text="", photo=photo, caption="*Voici une jolie photo 📸*")
    except FileNotFoundError:
        logger.error("Fichier chat.JPG introuvable, envoi du message sans image")
        await send_or_edit_message(update, context,
            text="*Impossible de charger l'image. Voici le menu :*",
            reply_markup=KEYBOARD_CACHE["start"])

if __name__ == "__main__":
    try:
        # Charge les utilisateurs au démarrage
        load_users()
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("photo", send_photo))
        app.add_handler(CommandHandler("listusers", list_users))
        app.add_handler(CommandHandler("stop", stop))
        app.add_handler(CommandHandler("announce", announce))
        app.add_handler(CallbackQueryHandler(button_click))
        print("🚀 Bot lancé.")
        logger.info("Démarrage du bot...")
        asyncio.run(app.run_polling(timeout=30, drop_pending_updates=True))
    except ValueError as e:
        logger.error(f"Erreur : Token invalide - {e}")
