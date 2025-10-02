from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
import asyncio
import os

# Charge les variables d'environnement (pour Render ou local avec .env)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8297261611:AAFB0kKhr_HPwP89UKH4d5E1Jvl5EjZJ9Kw")

# Cache pour les fichiers médias
MEDIA_CACHE = {}

# Cache pour les claviers réutilisés
KEYBOARD_CACHE = {
    "start": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
        [InlineKeyboardButton("Informations", callback_data="info")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+NYNe1lR1HellMGI0")]
    ]),
    "menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("Hash 🍫", callback_data="hash")],
        [InlineKeyboardButton("Weed 🌳", callback_data="weed")],
        [InlineKeyboardButton("🔙 Retour", callback_data="back")]
    ]),
    "hash": InlineKeyboardMarkup([
        [InlineKeyboardButton("Barbe Noir 73u 🏴‍☠️", callback_data="barbe_noir")],
        [InlineKeyboardButton("Hash Dry 90u", callback_data="hash_dry")],
        [InlineKeyboardButton("Popeye armz 🗼🥇", callback_data="popeye_armz")],
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
        [InlineKeyboardButton("Informations", callback_data="info")],
        [InlineKeyboardButton("Contact", url="https://t.me/Calibelt76")],
        [InlineKeyboardButton("Canal telegram", url="https://t.me/+ayptPdxw1WEzNDVk")]
    ])
}

# Active le logging pour déboguer
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def load_media_file(filename: str, media_type: str) -> bytes:
    """Charge un fichier média et le met en cache, ou retourne None si introuvable."""
    try:
        media = MEDIA_CACHE.get(filename)
        if media is None:
            logger.warning(f"Fichier {filename} non en cache, chargement direct")
            with open(filename, "rb") as file:
                media = file.read()
                MEDIA_CACHE[filename] = media
        return media
    except FileNotFoundError:
        logger.error(f"Fichier {filename} introuvable")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    logger.info(f"Commande /start reçue de {name}")
    reply_markup = KEYBOARD_CACHE["start"]
    logger.info(f"Envoi du menu initial avec boutons: {reply_markup.inline_keyboard}")
    photo = await load_media_file("chat.jpg", "image")
    if photo:
        await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
            caption=(
                f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                "*/start - Pour redémarrer le Bot*\n"
                "*/help - Pour obtenir de l'aide*\n"
                "*Ce Bot te servira à consulter notre menu 📖*\n"
                "*👉 Utilise les boutons ci-dessous 👇*"
            ))
    else:
        await update.message.reply_text("*Erreur : Image chat.jpg introuvable.*", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /help pour guider les utilisateurs."""
    logger.info(f"Commande /help reçue de {update.effective_user.first_name}")
    await send_or_edit_message(update, context,
        text=(
            "*Aide pour utiliser le Bot 📖*\n\n"
            "Voici les commandes disponibles :\n"
            "*/start* - Démarre le bot et affiche le menu principal.\n"
            "*/help* - Affiche cette aide.\n"
            "*/photo* - Envoie une photo.\n\n"
            "*Navigation* :\n"
            "- Utilise les boutons pour explorer le menu (Hash 🍫, Weed 🌳).\n"
            "- Clique sur *Informations* pour les détails sur les meet-ups et livraisons.\n"
            "- Clique sur *Contact* pour discuter avec @Calibelt76.\n"
            "- Rejoins notre *Canal Telegram* pour plus d'infos.\n\n"
            "Si tu rencontres un problème, contacte @Calibelt76 directement."
        ),
        reply_markup=KEYBOARD_CACHE["start"]
    )

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
            text=(
                "*SERVICE MEET-UP 🏠*\n\n"
                "*ROUEN 76 📍*\n"
                "*Vous pouvez directement passer et meet-up la miff 🚶 ✈️*\n"
                "*Prévenir et faire votre com*and Juste avant de passer en privé.*\n\n"
                "*SERVICE L*VRA*SON 🚚*\n\n"
                "*Service Livraison dans toute la Normandie et c’est Alentour*\n"
                "*76 /27/14 et tout la Normandie ! 🗺️ 🚚*\n\n"
                "*76 30-50e*\n"
                "*—————————*\n"
                "*10 à 20e de Frais Par Klm.*\n\n"
                "*-30klm-110*\n"
                "*- 50Klm - 250e*\n"
                "*- 70klm- 340e*\n"
                "*- 100Klm - 450e*\n\n"
                "*Contact: @calibelt76🐺*"
            ),
            reply_markup=KEYBOARD_CACHE["back"])
    elif query.data == "hash":
        await send_or_edit_message(update, context,
            text="*Choisis une option pour Hash 🍫 :*",
            reply_markup=KEYBOARD_CACHE["hash"])
    elif query.data == "barbe_noir":
        reply_markup = KEYBOARD_CACHE["hash_back"]
        video = await load_media_file("barbe_noir.mp4", "video")
        if video:
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*Barbe Noir 🏴‍☠️*\n\n"
                        "*73u*\n"
                        "*- Forbiden 🍑🍓🍉*\n"
                        "*5G 60€*\n"
                        "*10G 100€*\n"
                        "*25G 240€*\n",
                reply_markup=reply_markup)
        else:
            await query.message.reply_text("*Erreur : Vidéo barbe_noir.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "hash_dry":
        reply_markup = KEYBOARD_CACHE["hash_back"]
        video = await load_media_file("hash_dry.mp4", "video")
        if video:
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
        else:
            await query.message.reply_text("*Erreur : Vidéo hash_dry.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "popeye_armz":
        reply_markup = KEYBOARD_CACHE["hash_back"]
        video = await load_media_file("popeye_armz.mp4", "video")
        if video:
            await send_or_edit_message(update, context,
                text="", video=video,
                caption=(
                    "*Format [eggs 🥚]*\n\n"
                    "*Popeye armz 🗼🥇*\n"
                    "*Egss 10G*\n\n"
                    "*- tiramisu 🧁☕️*\n"
                    "*- zmo x papaya 🍬🥭*\n\n"
                    "*5G 80€*\n"
                    "*10G 160€*\n"
                    "*25G 340€*"
                ),
                reply_markup=reply_markup)
        else:
            await query.message.reply_text("*Erreur : Vidéo popeye_armz.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "weed":
        await send_or_edit_message(update, context,
            text="*Choisis une option pour Weed 🌳 :*",
            reply_markup=KEYBOARD_CACHE["weed"])
    elif query.data == "cali_us":
        reply_markup = KEYBOARD_CACHE["weed_back"]
        video = await load_media_file("cali_us.mp4", "video")
        if video:
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*CALI US 🇺🇸*\n\n"
                        "*- Cherry Bomb 🍒🍦💣*\n"
                        "*5G 70€*\n"
                        "*10G 140€*\n"
                        "*20G 270€*\n"
                        "*25G 330€*\n",
                reply_markup=reply_markup)
        else:
            await query.message.reply_text("*Erreur : Vidéo cali_us.mp4 introuvable.*", parse_mode="Markdown")
    elif query.data == "back":
        user = update.effective_user
        name = user.first_name
        reply_markup = KEYBOARD_CACHE["back"]
        photo = await load_media_file("chat.jpg", "image")
        if photo:
            await send_or_edit_message(update, context, text="", reply_markup=reply_markup, photo=photo,
                caption=(
                    f"*Bienvenue {name} sur notre Bot Télégram 📱*\n\n"
                    "*/start - Pour redémarrer le Bot*\n"
                    "*/help - Pour obtenir de l'aide*\n"
                    "*Ce Bot te servira à consulter notre menu 📖*\n"
                    "*👉 Utilise les boutons ci-dessous 👇*"
                ))
        else:
            await query.message.reply_text("*Erreur : Image chat.jpg introuvable.*", parse_mode="Markdown")

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await load_media_file("chat.jpg", "image")
    if photo:
        await send_or_edit_message(update, context, text="", photo=photo, caption="*Voici une jolie photo 📸*")
    else:
        await update.message.reply_text("*Erreur : Image chat.jpg introuvable.*", parse_mode="Markdown")

if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("photo", send_photo))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CallbackQueryHandler(button_click))
        print("🚀 Bot lancé.")
        logger.info("Démarrage du bot...")
        asyncio.run(app.run_polling(timeout=30, drop_pending_updates=True))
    except ValueError as e:
        logger.error(f"Erreur : Token invalide - {e}")
