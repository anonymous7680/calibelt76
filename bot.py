from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.error import BadRequest, NetworkError
import logging
import asyncio
import os

# Charge les variables d'environnement
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

# Cache pour les fichiers médias
MEDIA_CACHE = {}

# Cache pour les claviers réutilisés
KEYBOARD_CACHE = {
    "start": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
        [InlineKeyboardButton("Information", callback_data="info")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+NYNe1lR1HellMGI0")]
    ]),
    "menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("Hash 🍫", callback_data="hash")],
        [InlineKeyboardButton("Weed 🌳", callback_data="weed")],
        [InlineKeyboardButton("🔙 Retour", callback_data="back")]
    ]),
    "info": InlineKeyboardMarkup([
        [InlineKeyboardButton("Information", callback_data="info_details")],
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
        [InlineKeyboardButton("CALI US 🇺🇸", callback_data="cali_us")],
        [InlineKeyboardButton("🔙 Retour", callback_data="menu")]
    ]),
    "weed_back": InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Retour 🔙", callback_data="weed")]
    ]),
    "back": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
        [InlineKeyboardButton("Information", callback_data="info")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+ayptPdxw1WEzNDVk")]
    ])
}

# Active le logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_or_edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, photo=None, video=None, caption=None, parse_mode=constants.ParseMode.MARKDOWN_V2):
    chat = update.effective_chat
    logger.info(f"Envoi d'un message à {chat.id}")

    if context.user_data.get('sending_message'):
        logger.warning("Message déjà en cours d'envoi, annulation.")
        return None

    context.user_data['sending_message'] = True
    try:
        # Supprimer le message précédent
        last_message_id = context.user_data.get('last_bot_message_id')
        if last_message_id:
            try:
                await chat.delete_message(last_message_id)
                logger.info(f"Message {last_message_id} supprimé")
            except BadRequest:
                logger.warning(f"Message {last_message_id} introuvable ou déjà supprimé")
            except NetworkError as e:
                logger.error(f"Erreur réseau lors de la suppression du message {last_message_id}: {e}")

        # Envoyer le nouveau message
        if photo:
            sent_message = await chat.send_photo(
                photo=photo,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        elif video:
            sent_message = await chat.send_video(
                video=video,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        else:
            sent_message = await chat.send_message(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        
        context.user_data['last_bot_message_id'] = sent_message.message_id
        logger.info(f"Nouveau message envoyé, ID: {sent_message.message_id}")
        return sent_message

    except BadRequest as e:
        logger.error(f"Erreur lors de l'envoi du message (possible problème de Markdown): {e}")
        await chat.send_message(
            "*Une erreur s'est produite\\. Essaie à nouveau\\.*",
            parse_mode=constants.ParseMode.MARKDOWN_V2
        )
        return None
    except NetworkError as e:
        logger.error(f"Erreur réseau lors de l'envoi du message: {e}")
        return None
    finally:
        context.user_data['sending_message'] = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    logger.info(f"Commande /start reçue de {name}")
    reply_markup = KEYBOARD_CACHE["start"]
    try:
        photo = MEDIA_CACHE.get("chat.JPG")
        if photo is None:
            logger.warning("Fichier chat.jpg non en cache, chargement direct")
            with open("chat.jpg", "rb") as image:
                photo = image.read()
                MEDIA_CACHE["chat.JPG"] = photo
        await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
            caption=(
                f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                "*/start \\- Pour redémarrer le Bot*\n"
                "*Ce Bot te servira à consulter notre menu 📖*\n"
                "*👉 Utilise les boutons ci\\-dessous 👇*"
            ))
    except FileNotFoundError:
        logger.error("Fichier chat.jpg introuvable")
        await update.message.reply_text("*Erreur : Image chat\\.jpg introuvable\\.*", parse_mode=constants.ParseMode.MARKDOWN_V2)

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
            text="*Choisis une option :*",
            reply_markup=KEYBOARD_CACHE["info"])
    elif query.data == "info_details":
        await send_or_edit_message(update, context,
            text="*INFORMATION*\n\n"
                 "*SERVICE MEET\\-UP 🏠*\n"
                 "*ROUEN 76 📍*\n"
                 "*\\-15% Pour Ta comande ✅*\n"
                 "*Vous pouvez directement passer au meet\\-up la miff 🚶*\n"
                 "*Prévenir et faire votre com\\*and Juste avant de passer en privé\\.*\n\n"
                 "*SERVICE L\\*VRA\\*SON 🚚*\n"
                 "*Livraison dans tout le 76 / 27 et 14 et Tout alentours De Normandie \\!🚗 🌆*\n"
                 "*\\- 76 20\\-50€*\n"
                 "*——————*\n"
                 "*10 à 20e de frais selon La distance*\n"
                 "*\\- 30klm 110€*\n"
                 "*\\- 50Klm 230€*\n"
                 "*\\- 100klm 350€*\n"
                 "*\\- 150klm 450€*\n\n"
                 "*Contact :*\n"
                 "*@calibelt76 🐺*",
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
                        "*\\- Forbiden 🍑🍓🍉*\n"
                        "*5G 60€*\n"
                        "*10G 100€*\n"
                        "*25G 240€*",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier barbe_noir.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo barbe_noir\\.mp4 introuvable\\.*", parse_mode=constants.ParseMode.MARKDOWN_V2)
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
                        "*\\- California 🌴🇺🇸*\n"
                        "*\\- Coco mangue 🥥🥭*\n"
                        "*5G 70€*\n"
                        "*10G 130€*\n"
                        "*20G 270€*\n"
                        "*25G 330€*\n"
                        "*50G 430€*",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier hash_dry.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo hash_dry\\.mp4 introuvable\\.*", parse_mode=constants.ParseMode.MARKDOWN_V2)
    elif query.data == "weed":
        await send_or_edit_message(update, context,
            text="*Choisis une option pour Weed 🌳 :*",
            reply_markup=KEYBOARD_CACHE["weed"])
    elif query.data == "cali_us":
        reply_markup = KEYBOARD_CACHE["weed_back"]
        try:
            video = MEDIA_CACHE.get("cali_us.mp4")
            if video is None:
                logger.warning("Fichier cali_us.mp4 non en cache, chargement direct")
                with open("cali_us.mp4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["cali_us.mp4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*CALI US 🇺🇸*\n\n"
                        "*\\- Cherry Bomb 🍒🍦💣*\n"
                        "*5G 70€*\n"
                        "*10G 140€*\n"
                        "*20G 270€*\n"
                        "*25G 330€*",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier cali_us.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo cali_us\\.mp4 introuvable\\.*", parse_mode=constants.ParseMode.MARKDOWN_V2)
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
                    "*/start \\- Pour redémarrer le Bot*\n"
                    "*Ce Bot te servira à consulter notre menu 📖*\n"
                    "*👉 Utilise les boutons ci\\-dessous 👇*"
                ))
        except FileNotFoundError:
            logger.error("Fichier chat.jpg introuvable")
            await query.message.reply_text("*Erreur : Image chat\\.jpg introuvable\\.*", parse_mode=constants.ParseMode.MARKDOWN_V2)
    else:
        logger.warning(f"Callback inconnu : {query.data}")
        await send_or_edit_message(update, context,
            text="*Option invalide\\. Veuillez sélectionner une option valide\\.*",
            reply_markup=KEYBOARD_CACHE["info"])

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
        await update.message.reply_text("*Erreur : Image chat\\.jpg introuvable\\.*", parse_mode=constants.ParseMode.MARKDOWN_V2)

if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("photo", send_photo))
        app.add_handler(CallbackQueryHandler(button_click))
        print("🚀 Bot lancé.")
        logger.info("Démarrage du bot...")
        asyncio.run(app.run_polling(timeout=30, drop_pending_updates=True))
    except ValueError as e:
        logger.error(f"Erreur : Token invalide - {e}")
