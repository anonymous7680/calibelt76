from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
import asyncio
import os

# Charge les variables d'environnement (pour Render ou local avec .env)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8465189645:AAH1OOmNfgXNOfNB-puSnbjNntHYBnSc54Q")

# Cache pour les fichiers médias
MEDIA_CACHE = {}

# Cache pour les claviers réutilisés
KEYBOARD_CACHE = {
    "start": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
        [InlineKeyboardButton("Information", callback_data="info")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+ReFc7y_qhoMzNWE8")],
        [InlineKeyboardButton("Canal Potato", url="https://ptdym198.org/joinchat/vlNUyjhhgWD8SfEaRTwUCQ")]
    ]),
    "menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("Hash 🍫", callback_data="hash")],
        [InlineKeyboardButton("Weed 🌳", callback_data="weed")],
        [InlineKeyboardButton("🔙 Retour", callback_data="back")]
    ]),
    "info": InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Retour", callback_data="back")]
    ]),
    "hash": InlineKeyboardMarkup([
        [InlineKeyboardButton("Barbe Noir 73u 🏴‍☠️", callback_data="barbe_noir")],
        [InlineKeyboardButton("Hash Dry 90u", callback_data="hash_dry")],
        [InlineKeyboardButton("🔙 Retour", callback_data="menu")]
    ]),
    "hash_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour 🔙", callback_data="menu")]
    ]),
    "weed": InlineKeyboardMarkup([
        [InlineKeyboardButton("🍍Pineapple", callback_data="pineapple")],
        [InlineKeyboardButton("🔙 Retour", callback_data="menu")]
    ]),
    "weed_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour 🔙", callback_data="weed")]
    ]),
    "pineapple_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour 🔙", callback_data="weed")]
    ]),
    "back": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
        [InlineKeyboardButton("Information", callback_data="info")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+ayptPdxw1WEzNDVk")],
        [InlineKeyboardButton("Canal Potato", url="https://ptdym198.org/joinchat/vlNUyjhhgWD8SfEaRTwUCQ")]
    ])
}

# Active le logging pour déboguer
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_or_edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, photo=None, video=None, caption=None):
    chat = update.effective_chat
    logger.info(f"Envoi d'un message à {chat.id}")
    # Vérifie si un message est déjà en cours d'envoi pour éviter les redondances
    if context.user_data.get('sending_message'):
        logger.warning("Message déjà en cours d'envoi, annulation.")
        return None
    context.user_data['sending_message'] = True
    # Supprime le message précédent si stocké, sans bloquer
    last_message_id = context.user_data.get('last_bot_message_id')
    if last_message_id:
        try:
            await asyncio.shield(chat.delete_message(last_message_id))
            logger.info(f"Message {last_message_id} supprimé")
        except Exception as e:
            logger.warning(f"Erreur lors de la suppression du message {last_message_id}: {e}")
    # Envoie un nouveau message
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

# /start avec bouton
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    logger.info(f"Commande /start reçue de {name}")
    reply_markup = KEYBOARD_CACHE["start"]
    logger.info(f"Envoi du menu initial avec boutons: {reply_markup.inline_keyboard}")
    try:
        photo = MEDIA_CACHE.get("chat.jpg")
        if photo is None:
            logger.warning("Fichier chat.jpg non en cache, chargement direct")
            with open("chat.jpg", "rb") as image:
                photo = image.read()
                MEDIA_CACHE["chat.jpg"] = photo
        await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
            caption=(
                f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                "*/start - Pour redémarrer le Bot*\n"
                "*Ce Bot te servira à consulter notre menu 📖*\n"
                "*👉 Utilise les boutons ci-dessous 👇*"
            ))
    except FileNotFoundError:
        logger.error("Fichier chat.jpg introuvable")
        await update.message.reply_text("*Erreur : Image chat.jpg introuvable.*", parse_mode="Markdown")

# Gestion du clic sur bouton
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    logger.info(f"Bouton cliqué : {query.data}")
    if query.data == "menu":
        await send_or_edit_message(update, context,
            text="*Choisis une option dans le menu :*",
            reply_markup=KEYBOARD_CACHE["menu"])
    elif query.data == "info":
        await send_or_edit_message(update, context,
            text="*Voici les informations du bot :*\n\n"
                 "*✨ Merci de votre confiance ! ✨*\n"
                 "*Chez [Dry.Coffee76], on répond rapidement à vos messages en privé 💬.*\n"
                 "*On met un point d’honneur à vous offrir de la qualité au top à chaque commande 💎.*\n\n"
                 "*⚠️ Pour toute demande de commande, merci de nous envoyer une vidéo :*\n"
                 "*cela nous permet de garantir un meilleur suivi et plus de sécurité pour vous comme pour nous 🎥🔒.*\n\n"
                 "*Au plaisir de vous satisfaire 💛*\n"
                 "*Ce bot vous permet de consulter notre menu et de contacter notre équipe pour plus de détails.*\n"
                 "*Pour toute question, contactez @Calibelt76.*",
            reply_markup=KEYBOARD_CACHE["info"])
    elif query.data == "hash":
        await send_or_edit_message(update, context,
            text="*Choisis une option pour Hash 🍫 :*",
            reply_markup=KEYBOARD_CACHE["hash"])
    elif query.data == "barbe_noir":
        reply_markup = KEYBOARD_CACHE["hash_back"]
        try:
            video = MEDIA_CACHE.get("barbe_noir.mp4")
            if video is None:
                logger.warning("Fichier barbe_noir.mp4 non en cache, chargement direct")
                with open("barbe_noir.mp4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["barbe_noir.mp4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*Barbe Noir 🏴‍☠️*\n\n"
                        "*73u*\n"
                        "*- Forbiden 🍑🍓🍉*\n"
                        "*5G 60€*\n"
                        "*10G 100€*\n"
                        "*25G 240€*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier barbe_noir.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo barbe_noir.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "hash_dry":
        reply_markup = KEYBOARD_CACHE["hash_back"]
        try:
            video = MEDIA_CACHE.get("hash_dry.mp4")
            if video is None:
                logger.warning("Fichier hash_dry.mp4 non en cache, chargement direct")
                with open("hash_dry.mp4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["hash_dry.mp4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*Hash Dry 90u*\n\n"
                        "*- California 🌴🇺🇸*\n"
                        "*- Coco mangue 🥥🥭*\n"
                        "*5G 70€*\n"
                        "*10G 130€*\n"
                        "*20G 270€*\n"
                        "*25G 330€*\n"
                        "*50G 430€*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier hash_dry.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo hash_dry.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "weed":
        await send_or_edit_message(update, context,
            text="*Choisis une option pour Weed 🌳 :*",
            reply_markup=KEYBOARD_CACHE["weed"])
    elif query.data == "pineapple":
        reply_markup = KEYBOARD_CACHE["pineapple_back"]
        try:
            video = MEDIA_CACHE.get("pineapple.mp4")
            if video is None:
                logger.warning("Fichier pineapple.mp4 non en cache, chargement direct")
                with open("pineapple.mp4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["pineapple.mp4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*🍍Pineapple*\n\n"
                        "*TOP SHELF🏅*\n\n"
                        "*🍍5G=60€*\n"
                        "*🍍10G=100€*\n"
                        "*🍍25G=180€*\n"
                        "*🍍50G=340€*\n\n"
                        "*Diffusent un parfum fruité d’ananas🍍, elle donne une sensation de relaxation légère☁️*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier pineapple.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo pineapple.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "back":
        user = update.effective_user
        name = user.first_name
        reply_markup = KEYBOARD_CACHE["back"]
        try:
            photo = MEDIA_CACHE.get("chat.jpg")
            if photo is None:
                logger.warning("Fichier chat.jpg non en cache, chargement direct")
                with open("chat.jpg", "rb") as image:
                    photo = image.read()
                    MEDIA_CACHE["chat.jpg"] = photo
            await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
                caption=(
                    f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                    "*/start - Pour redémarrer le Bot*\n"
                    "*Ce Bot te servira à consulter notre menu 📖*\n"
                    "*👉 Utilise les boutons ci-dessous 👇*"
                ))
        except FileNotFoundError:
            logger.error("Fichier chat.jpg introuvable")
            await query.message.reply_text("*Erreur : Image chat.jpg introuvable.*", parse_mode="Markdown")

# /photo optionnel
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = MEDIA_CACHE.get("chat.jpg")
        if photo is None:
            logger.warning("Fichier chat.jpg non en cache, chargement direct")
            with open("chat.jpg", "rb") as image:
                photo = image.read()
                MEDIA_CACHE["chat.jpg"] = photo
        await send_or_edit_message(update, context, text="", photo=photo, caption="*Voici une jolie photo 📸*")
    except FileNotFoundError:
        logger.error("Fichier chat.jpg introuvable")
        await update.message.reply_text("*Erreur : Image chat.jpg introuvable.*", parse_mode="Markdown")

if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("photo", send_photo))
        app.add_handler(CallbackQueryHandler(button_click))
        print("🚀 Bot lancé.")
        logger.info("Démarrage du bot...")
        # Ajout d'un timeout pour éviter un blocage infini
        asyncio.run(app.run_polling(timeout=30, drop_pending_updates=True))
    except ValueError as e:
        logger.error(f"Erreur : Token invalide - {e}")
