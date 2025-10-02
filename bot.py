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
    "hash": InlineKeyboardMarkup([
        [InlineKeyboardButton("Barbe Noir 73u 🏴‍☠️", callback_data="barbe_noir")],
        [InlineKeyboardButton("Hash Dry 90u", callback_data="hash_dry")],
        [InlineKeyboardButton("Popeye armz 🗼🥇", callback_data="popeye_armz")],  # New product button
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
            text="*INFORMATION*\n\n"
                 "*SERVICE MEET-UP 🏠*\n"
                 "*ROUEN 76 📍*\n"
                 "*-15% Pour Ta comande ✅*\n"
                 "*Vous pouvez directement passer au meet-up la miff 🚶*\n"
                 "*Prévenir et faire votre com*and Juste avant de passer en privé.*\n\n"
                 "*SERVICE L*VRA*SON 🚚*\n"
                 "*Livraison dans tout le 76 / 27 et 14 et Tout alentours De Normandie !🚗 🌆*\n"
                 "*- 76 20-50€*\n"
                 "*——————*\n"
                 "*10 à 20e de frais selon La distance*\n"
                 "*- 30klm 110€*\n"
                 "*- 50Klm 230€*\n"
                 "*- 100klm 350€*\n"
                 "*- 150klm 450€*\n\n"
                 "*Contact :*\n"
                 "*@calibelt76 🐺*",
            reply_markup=KEYBOARD_CACHE["back"])
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
    elif query.data == "popeye_armz":  # New product handler
        reply_markup = KEYBOARD_CACHE["hash_back"]
        try:
            video = MEDIA_CACHE.get("popeye_armz.mp4")
            if video is None:
                logger.warning("Fichier popeye_armz.mp4 non en cache, chargement direct")
                with open("popeye_armz.mp4", "rb") as video_file:
                    video = video_file.read()
                    MEDIA_CACHE["popeye_armz.mp4"] = video
            await send_or_edit_message(update, context,
                text="", video=video,
                caption="*Popeye armz 🗼🥇*\n\n"
                        "*Egss 10G*\n"
                        "*- Papaya Dawg 🥭🍉*\n"
                        "*- Chardonay Biscuit 🍪🍰*\n"
                        "*5G 80€*\n"
                        "*10G 160€*\n"
                        "*25G 340€*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier popeye_armz.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo popeye_armz.mp4 introuvable.*", parse_mode="Markdown")
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
                        "*- Cherry Bomb 🍒🍦💣*\n"
                        "*5G 70€*\n"
                        "*10G 140€*\n"
                        "*20G 270€*\n"
                        "*25G 330€*\n",
                reply_markup=reply_markup)
        except FileNotFoundError:
            logger.error("Fichier cali_us.mp4 introuvable")
            await query.message.reply_text("*Erreur : Vidéo cali_us.mp4 introuvable.*", parse_mode="Markdown")
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
