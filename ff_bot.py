import requests
import os
from datetime import datetime, timezone, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

IST = timezone(timedelta(hours=5, minutes=30))

BOT_TOKEN = os.getenv("BOT_TOKEN")

CH1_ID = os.getenv("CH1_ID")
CH1_LINK = os.getenv("CH1_LINK")

CH2_ID = os.getenv("CH2_ID")
CH2_LINK = os.getenv("CH2_LINK")

CH3_ID = os.getenv("CH3_ID")
CH3_LINK = os.getenv("CH3_LINK")

CH4_ID = os.getenv("CH4_ID")
CH4_LINK = os.getenv("CH4_LINK")

CH5_ID = os.getenv("CH5_ID")
CH5_LINK = os.getenv("CH5_LINK")

INFO_API = os.getenv("INFO_API")
IMAGE_API = os.getenv("IMAGE_API")

def ts_to_ist(ts):
    if not ts:
        return "Not Found"
    try:
        dt = datetime.fromtimestamp(int(ts), tz=IST)
        return dt.strftime("%d %B %Y at %I:%M:%S %p (IST)")
    except:
        return "Not Found"

RANK_MAP = {
    0: "Unranked", 1: "Bronze III", 2: "Bronze II", 3: "Bronze I",
    4: "Silver III", 5: "Silver II", 6: "Silver I",
    7: "Gold III", 8: "Gold II", 9: "Gold I",
    10: "Platinum III", 11: "Platinum II", 12: "Platinum I",
    13: "Diamond III", 14: "Diamond II", 15: "Diamond I",
    16: "Heroic", 17: "Elite Heroic I", 18: "Elite Heroic II",
    19: "Elite Heroic III", 20: "Elite Heroic IV", 21: "Elite Heroic V",
    22: "Elite Heroic VI", 23: "Master", 24: "Grandmaster",
}

CS_RANK_MAP = {
    0: "Unranked", 1: "Bronze III", 2: "Bronze II", 3: "Bronze I",
    4: "Silver III", 5: "Silver II", 6: "Silver I",
    7: "Gold III", 8: "Gold II", 9: "Gold I",
    10: "Platinum III", 11: "Platinum II", 12: "Platinum I",
    13: "Diamond III", 14: "Diamond II", 15: "Diamond I",
    16: "Heroic", 17: "Master", 18: "Grandmaster",
}

PET_NAMES = {
    1300000114: "Mr. Waggor", 1300000004: "Poring", 1300000006: "Kitty",
    1300000007: "Falco", 1300000009: "Beaston", 1300000013: "Night Panther",
    1300000016: "Detective Panda", 1300000021: "Mechanical Pup",
    1300000031: "Ottero", 1300000043: "Spirit Fox", 1300000051: "Dreki",
    1300000061: "Moony", 1300000071: "Robo", 1300000081: "Chomper",
}

SKILL_NAMES = {
    1: "Kelly", 2: "Andrew", 3: "Ford", 4: "Nikita", 5: "Antonio",
    6: "Olivia", 7: "Maxim", 8: "Misha", 9: "Laura", 10: "Miguel",
    11: "Caroline", 12: "Hayato", 13: "Kla", 14: "Jai", 16: "Rafael",
    106: "Alok", 206: "Wukong", 306: "Maro", 406: "Chrono", 506: "Skyler",
    606: "Dimitri", 706: "Thiva", 806: "Kenta", 1106: "Alvaro",
    1306: "Shirou", 1606: "D-Bee", 3406: "Moco Enigma", 5701: "Morse",
    6906: "Clu", 2101: "Steffie", 2201: "Dasha", 2501: "Shani",
}

FF_LEVEL_EXP = {
    1: 0, 2: 48, 3: 202, 4: 544, 5: 1012,
    6: 1844, 7: 2792, 8: 3800, 9: 4870, 10: 6004,
    11: 7192, 12: 8448, 13: 9760, 14: 11140, 15: 12566,
    16: 14060, 17: 15610, 18: 17224, 19: 18902, 20: 20632,
    21: 22424, 22: 24278, 23: 26192, 24: 28166, 25: 30200,
    26: 32294, 27: 34448, 28: 37804, 29: 41274, 30: 44870,
    31: 48582, 32: 53394, 33: 58566, 34: 64096, 35: 69994,
    36: 76460, 37: 83506, 38: 91128, 39: 99322, 40: 108092,
    41: 120144, 42: 133266, 43: 147472, 44: 162760, 45: 179126,
    46: 196572, 47: 215368, 48: 235516, 49: 257010, 50: 279860,
    51: 304056, 52: 348318, 53: 394982, 54: 444044, 55: 495508,
    56: 549364, 57: 633756, 58: 721744, 59: 813336, 60: 908522,
    61: 1041438, 62: 1180352, 63: 1325266, 64: 1476184, 65: 1634300,
    66: 1840946, 67: 2056594, 68: 2281242, 69: 2514880, 70: 2757530,
    71: 3059506, 72: 3372284, 73: 3699456, 74: 4041030, 75: 4397002,
    76: 4829104, 77: 5282204, 78: 5756304, 79: 6251404, 80: 6767502,
    81: 7381324, 82: 8043154, 83: 8752982, 84: 9510808, 85: 10316638,
    86: 11277190, 87: 12291748, 88: 13360304, 89: 14482858, 90: 15659418,
    91: 17026708, 92: 18453950, 93: 19941280, 94: 21488570, 95: 23095858,
    96: 24763138, 97: 26490428, 98: 28277708, 99: 30124996, 100: 32032284,
}

# ── Join Check ───────────────────────────────────────────────────────────────

async def is_user_joined(bot, user_id):
    try:
        mem1 = await bot.get_chat_member(CH1_ID, user_id)
        ch1 = mem1.status not in ['left', 'kicked']
        mem2 = await bot.get_chat_member(CH2_ID, user_id)
        ch2 = mem2.status not in ['left', 'kicked']
        mem3 = await bot.get_chat_member(CH3_ID, user_id)
        ch3 = mem3.status not in ['left', 'kicked']
        mem4 = await bot.get_chat_member(CH4_ID, user_id)
        ch4 = mem4.status not in ['left', 'kicked']
        mem5 = await bot.get_chat_member(CH5_ID, user_id)
        ch5 = mem5.status not in ['left', 'kicked']
        return ch1 and ch2 and ch3 and ch4 and ch5
    except Exception as e:
        print(f"Join check error: {e}")
        return True

def get_join_message(user_name):
    text = (
        f"Hey {user_name} 👋\n\n"
        "Please Join All My Update Channels To Use Me! 🔒"
    )
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/ruchika_ownss"),
            InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/v4nshera"),
            InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/backupvnsh"),
            InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/ruchikaa_owns"),
            InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/ruchii_owns"),
        ],
        [InlineKeyboardButton("♻️ Try Again", callback_data="verify_join")],
    ])
    return text, markup

# ── Decorator for join check ─────────────────────────────────────────────────

def require_join(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        joined = await is_user_joined(context.bot, user.id)
        if not joined:
            user_name = user.first_name or "User"
            text, markup = get_join_message(user_name)
            await update.message.reply_text(text, reply_markup=markup)
            return
        return await func(update, context)
    wrapper.__name__ = func.__name__
    return wrapper

# ── Callback: Verify Join ────────────────────────────────────────────────────

async def verify_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    joined = await is_user_joined(context.bot, user.id)

    if joined:
        await query.answer("☬ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ ᴄᴏᴍᴘʟᴇᴛᴇ ☬\n🔓 ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ", show_alert=True)
        try:
            await query.message.delete()
        except:
            pass
        success = (
            "┏━━━「 ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ 🎉 」━━━┓\n"
            "┃\n"
            "┃ 🔓 *ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴʟᴏᴄᴋᴇᴅ!*\n"
            "┃\n"
            "┃ 👉 Type /start to begin!\n"
            "┃\n"
            "┗━━━━━━━━━━━━━━━━━━━━┛"
        )
        await context.bot.send_message(query.message.chat.id, success, parse_mode="Markdown")
    else:
        await query.answer("❌ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ • ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ", show_alert=True)

# ── Helper functions ─────────────────────────────────────────────────────────

def get_exp_to_next_level(current_level, current_exp):
    if current_level >= 100:
        return 0, 0
    next_level_start = FF_LEVEL_EXP.get(current_level + 1, 0)
    max_level_start = FF_LEVEL_EXP.get(100, 0)
    exp_needed = max(0, next_level_start - current_exp)
    exp_to_100 = max(0, max_level_start - current_exp)
    return exp_needed, exp_to_100

def get_br_rank(rank_id, points=None):
    rank = RANK_MAP.get(rank_id, f"Unknown({rank_id})")
    return f"{rank} ({points})" if points else rank

def get_cs_rank(rank_id, points=None):
    rank = CS_RANK_MAP.get(rank_id, f"Unknown({rank_id})")
    return f"{rank} ({points} pts)" if points else rank

def parse_skills(equipped_skills):
    seen = []
    result = []
    for i in range(0, len(equipped_skills), 4):
        chunk = equipped_skills[i:i+4]
        if len(chunk) < 2:
            continue
        skill_id = chunk[0]
        slot_type = chunk[2] if len(chunk) > 2 else 1
        if skill_id in seen or skill_id == 0:
            continue
        seen.append(skill_id)
        name = SKILL_NAMES.get(skill_id, f"Skill#{skill_id}")
        stype = "Active" if slot_type == 2 else "Passive"
        result.append(f"{name} ({stype})")
    return ", ".join(result) if result else "Not Found"

def safe_get_url(url):
    response = requests.get(url, timeout=3)
    response.raise_for_status()
    return response

# ── API helpers ──────────────────────────────────────────────────────────────

def fetch_player_isbanner_data_by_uid_or_name(search_parameter):
    if search_parameter.isdigit():
        url = f"{INFO_API}/bancheck?uid={search_parameter}"
    else:
        url = f"{INFO_API}/bancheck?name={search_parameter}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return (data.get("accountId"), data.get("name"), data.get("region", "Not Choosen"), data)

def fetch_player_wishlist_data_by_uid_or_name(search_parameter):
    if search_parameter.isdigit():
        url = f"{INFO_API}/wishlist?uid={search_parameter}"
    else:
        url = f"{INFO_API}/wishlist?name={search_parameter}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    player = data.get("player")
    if not player:
        return None
    return (player.get("uid"), player.get("name"), player.get("region", "Not Choosen"), data)

def fetch_player_data_by_uid_or_name(search_parameter):
    if search_parameter.isdigit():
        url = f"{INFO_API}/player-info?uid={search_parameter}"
    else:
        url = f"{INFO_API}/player-info?name={search_parameter}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    basic_info = data.get("basicInfo", {})
    return (basic_info.get("accountId"), basic_info.get("nickname"), basic_info.get("region", "Not Choosen"), data)

def fetch_leader_data_by_uid_or_name(search_parameter):
    result = fetch_player_data_by_uid_or_name(search_parameter)
    if result is None:
        return None
    account_id, player_name, region, data = result
    captain_information = data.get("captainBasicInfo", {})
    if not captain_information.get("accountId"):
        return None
    leader_uid = captain_information.get("accountId")
    url = f"{INFO_API}/player-info?uid={leader_uid}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    leader_data = response.json()
    basic_info = leader_data.get("basicInfo", {})
    return (basic_info.get("accountId"), basic_info.get("nickname"), basic_info.get("region", "Not Choosen"), leader_data)

def fetch_banner_image(player_data):
    basic_information = player_data.get("basicInfo", {})
    clan_information = player_data.get("clanBasicInfo", {})
    frame = "true" if basic_information.get("primeLevel", {}).get("level") == 8 else "false"
    url = (
        f"{IMAGE_API}/banner-image"
        f"?headPic={basic_information.get('headPic','')}"
        f"&bannerId={basic_information.get('bannerId','')}"
        f"&name={basic_information.get('nickname','').replace('#','%23').replace('&','%26')}"
        f"&level={basic_information.get('level',2)}"
        f"&guild={clan_information.get('clanName','').replace('#','%23').replace('&','%26')}"
        f"&pinId={basic_information.get('pinId','900000012')}"
        f"&celebrity={basic_information.get('celebrityStatus',0)}"
        f"&primeLevel={basic_information.get('primeLevel',{}).get('level',0)}"
        f"&frame={frame}"
    )
    return safe_get_url(url).content

def fetch_outfit_image(player_data):
    basic_information = player_data.get("basicInfo", {})
    profile_information = player_data.get("profileInfo", {})
    equipped_weapons = basic_information.get("weaponSkinShows", [])
    equipped_outfits = profile_information.get("clothes", [])
    character_id = profile_information.get("avatarId", "102000007")
    outfit_ids = ",".join(str(item) for item in (equipped_outfits + equipped_weapons)) if (equipped_outfits or equipped_weapons) else ""
    url = f"{IMAGE_API}/outfit-image?avatar_id={character_id}&clothes={outfit_ids}"
    return safe_get_url(url).content

# ── Command handlers ─────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    joined = await is_user_joined(context.bot, user.id)
    if not joined:
        user_name = user.first_name or "User"
        text, markup = get_join_message(user_name)
        await update.message.reply_text(text, reply_markup=markup)
        return

    await update.message.reply_text(
        "🎮 *Free Fire Bot*\n\n"
        "Commands:\n"
        "• `/info <uid/name>` — Full player info\n",
        "• `/level <uid/name>` — Level & EXP details\n",
        "• `/bancheck <uid/name>` — Ban status check\n",
        "• `/isban <uid/name>` — Ban status check (tree view)\n",
        "• `/wishlist <uid/name>` — Wishlist items check\n",
        "• `/guildleader <uid/name>` — Guild leader info\n",
        "• `/invite5 <uid>` — 5-Lobby invite bhejo\n",
        parse_mode="Markdown"
    )

@require_join
async def level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/level <uid or name>`", parse_mode="Markdown")
        return

    search = " ".join(context.args).strip()
    msg = await update.message.reply_text("🔍 Fetching level info...")

    result = fetch_player_data_by_uid_or_name(search)
    if not result:
        await msg.edit_text("❌ Player not found or API error.")
        return

    account_id, name, region, data = result
    b = data.get("basicInfo", {})

    current_level = b.get("level", 0)
    current_exp = b.get("exp", 0)
    likes = b.get("liked", 0)
    exp_needed, exp_to_100 = get_exp_to_next_level(current_level, current_exp)

    text = (
        f"📊 *Level Information*\n"
        f"┌ Level Information\n"
        f"├─ UID: {account_id}\n"
        f"├─ Username: {name}\n"
        f"├─ Region: {region}\n"
        f"├─ Level: {current_level}\n"
        f"├─ Exp: {current_exp}\n"
        f"├─ Likes: {likes}\n"
    )
    if current_level >= 100:
        text += f"└─ Max Level Reached! 🏆\n"
    else:
        text += (
            f"├─ Exp needed for next level: {exp_needed:,}\n"
            f"└─ Total Exp to reach level 100: {exp_to_100:,}\n"
        )

    try:
        banner_bytes = fetch_banner_image(data)
        await update.message.reply_photo(photo=banner_bytes, caption=text, parse_mode="Markdown")
        await msg.delete()
    except Exception:
        await msg.edit_text(text, parse_mode="Markdown")

@require_join
async def bancheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/bancheck <uid or name>`", parse_mode="Markdown")
        return

    search = " ".join(context.args).strip()
    msg = await update.message.reply_text("🔍 Checking ban status...")

    result = fetch_player_isbanner_data_by_uid_or_name(search)
    if not result:
        await msg.edit_text("❌ Player not found or API error.")
        return

    account_id, name, region, data = result
    is_banned = data.get("isBanned", False)
    ban_period = data.get("banPeriod", "N/A")
    ban_reason = data.get("banReason", "N/A")

    status_emoji = "🚫" if is_banned else "✅"
    status_text = "BANNED" if is_banned else "SAFE"

    text = (
        f"{status_emoji} *Ban Check Result*\n\n"
        f"👤 Name: `{name}`\n"
        f"🆔 UID: `{account_id}`\n"
        f"🌍 Region: `{region}`\n"
        f"📊 Status: *{status_text}*\n"
    )
    if is_banned:
        text += f"⏳ Ban Period: `{ban_period}`\n"
        text += f"📝 Reason: `{ban_reason}`\n"

    try:
        player_data_result = fetch_player_data_by_uid_or_name(str(account_id))
        if player_data_result:
            _, _, _, player_data = player_data_result
            banner_bytes = fetch_banner_image(player_data)
            await update.message.reply_photo(photo=banner_bytes, caption=text, parse_mode="Markdown")
            await msg.delete()
        else:
            await msg.edit_text(text, parse_mode="Markdown")
    except Exception:
        await msg.edit_text(text, parse_mode="Markdown")

@require_join
async def isban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/isban <uid or name>`", parse_mode="Markdown")
        return

    search = " ".join(context.args).strip()
    msg = await update.message.reply_text("🔍 Checking ban status...")

    result = fetch_player_isbanner_data_by_uid_or_name(search)
    if not result:
        await msg.edit_text("❌ Player not found or API error.")
        return

    account_id, name, region, data = result
    is_banned = data.get("isBanned", False)
    ban_period = data.get("banPeriod", "N/A")
    ban_reason = data.get("banReason", "N/A")
    lv = data.get("level", "N/A")
    likes = data.get("likes", data.get("liked", "N/A"))
    status_text = "Banned ⛔" if is_banned else "Not Banned ✅"

    text = (
        f"🚫 *Bancheck Information*\n"
        f"┌ Bancheck Information\n"
        f"├─ UID: {account_id}\n"
        f"├─ Username: {name}\n"
        f"├─ Region: {region}\n"
        f"├─ Level: {lv}\n"
        f"├─ Likes: {likes}\n"
        f"└─ Status: {status_text}\n"
    )
    if is_banned:
        text += f"\n⏳ Ban Period: `{ban_period}`\n"
        text += f"📝 Reason: `{ban_reason}`\n"

    try:
        player_data_result = fetch_player_data_by_uid_or_name(str(account_id))
        if player_data_result:
            _, _, _, player_data = player_data_result
            banner_bytes = fetch_banner_image(player_data)
            await update.message.reply_photo(photo=banner_bytes, caption=text, parse_mode="Markdown")
            await msg.delete()
        else:
            await msg.edit_text(text, parse_mode="Markdown")
    except Exception:
        await msg.edit_text(text, parse_mode="Markdown")

@require_join
async def wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/wishlist <uid or name>`", parse_mode="Markdown")
        return

    search = " ".join(context.args).strip()
    msg = await update.message.reply_text("🔍 Fetching wishlist...")

    result = fetch_player_wishlist_data_by_uid_or_name(search)
    if not result:
        await msg.edit_text("❌ Player not found or API error.")
        return

    uid, name, region, data = result
    items = data.get("wishlist", [])

    text = (
        f"🎁 *Wishlist Check*\n\n"
        f"👤 Name: `{name}`\n"
        f"🆔 UID: `{uid}`\n"
        f"🌍 Region: `{region}`\n"
        f"📦 Total Wishlist Items : {len(items)}\n\n"
    )

    if items:
        text += "🛒 *Wishlist Items:*\n"
        for i, item in enumerate(items, 1):
            item_name = (item.get("itemName") or item.get("name") or f"Item {item.get('itemId','?')}")
            text += f"{i}. {item_name}\n"
    else:
        text += "_(Wishlist is empty)_"

    await msg.edit_text(text, parse_mode="Markdown")

@require_join
async def guildleader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/guildleader <uid or name>`", parse_mode="Markdown")
        return

    search = " ".join(context.args).strip()
    msg = await update.message.reply_text("🔍 Fetching guild leader info...")

    result = fetch_leader_data_by_uid_or_name(search)
    if not result:
        await msg.edit_text("❌ Player not found, no guild, or API error.")
        return

    leader_uid, leader_name, leader_region, leader_data = result
    basic_info = leader_data.get("basicInfo", {})
    clan_info = leader_data.get("clanBasicInfo", {})

    text = (
        f"👑 *Guild Leader Info*\n\n"
        f"👤 Name: `{leader_name}`\n"
        f"🆔 UID: `{leader_uid}`\n"
        f"🌍 Region: `{leader_region}`\n"
        f"⭐ Level: `{basic_info.get('level', 'N/A')}`\n"
        f"❤️ Likes: `{basic_info.get('liked', 'N/A')}`\n"
        f"🏰 Guild: `{clan_info.get('clanName', 'N/A')}`\n"
        f"👥 Members: `{clan_info.get('memberNum', 'N/A')}`\n"
    )

    try:
        banner_bytes = fetch_banner_image(leader_data)
        outfit_bytes = fetch_outfit_image(leader_data)
        await update.message.reply_photo(photo=banner_bytes, caption=text, parse_mode="Markdown")
        await update.message.reply_photo(photo=outfit_bytes, caption="👕 Leader's Outfit")
        await msg.delete()
    except Exception:
        try:
            banner_bytes = fetch_banner_image(leader_data)
            await update.message.reply_photo(photo=banner_bytes, caption=text, parse_mode="Markdown")
            await msg.delete()
        except Exception:
            await msg.edit_text(text, parse_mode="Markdown")

@require_join
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/info <uid or name>`", parse_mode="Markdown")
        return

    search = " ".join(context.args).strip()
    msg = await update.message.reply_text("🔍 Fetching player info...")

    result = fetch_player_data_by_uid_or_name(search)
    if not result:
        await msg.edit_text("❌ Player not found or API error.")
        return

    _, _, _, data = result
    b = data.get("basicInfo", {})
    p = data.get("profileInfo", {})
    clan = data.get("clanBasicInfo", {})
    cap = data.get("captainBasicInfo", {})
    social = data.get("socialInfo", {})
    pet = data.get("petInfo", {})
    credit = data.get("creditScoreInfo", {})
    craftland = data.get("craftlandMapInfoList", [])
    history = data.get("historyEpInfo", [])

    prime = b.get("primeLevel", {})
    prime_level = prime.get("level", 0) if isinstance(prime, dict) else 0

    bp_str = "None"
    bp_badge = "N/A"
    if history:
        cur = history[0]
        bp_badge = cur.get("badgeCnt", "N/A")
        bp_str = "Premium" if cur.get("ownedPass") else "None"

    br_rank_id = b.get("rank", 0)
    br_points = b.get("rankingPoints", 0)
    br_rank_str = get_br_rank(br_rank_id, br_points)

    cs_rank_id = b.get("csRank", 0)
    cs_points = b.get("csRankingPoints", 0)
    cs_rank_str = get_cs_rank(cs_rank_id, cs_points if cs_points else None)

    show_rank = social.get("rankShow", "None")
    gender = social.get("gender", "Male")
    skills_str = parse_skills(p.get("equippedSkills", []))
    time_active = social.get("timeActive", "Not Set") or "Not Set"
    mode_prefer = social.get("modePrefer", "None") or "None"
    days_active = "Not Set"

    pet_equipped = "Yes" if pet else "No"
    pet_id = pet.get("id")
    pet_name = PET_NAMES.get(pet_id, f"Pet#{pet_id}") if pet_id else "Not Equipped"
    pet_exp = pet.get("exp", "N/A")
    pet_level = pet.get("level", "N/A")

    guild_name = clan.get("clanName", "Not Found") or "Not Found"
    guild_id = clan.get("clanId", "Not Found") or "Not Found"
    guild_level = clan.get("clanLevel", "Not Found")
    guild_members = f"{clan.get('memberNum','?')}/{clan.get('capacity','?')}"

    leader_section = ""
    if cap and cap.get("accountId"):
        l_br_rank_id = cap.get("rank", 0)
        l_br_points = cap.get("rankingPoints", 0)
        l_br_str = get_br_rank(l_br_rank_id, l_br_points)
        l_cs_rank_id = cap.get("csRank", 0)
        l_cs_points = cap.get("csRankingPoints", 0)
        l_cs_str = get_cs_rank(l_cs_rank_id, l_cs_points if l_cs_points else None)
        l_prime = cap.get("primeLevel", {})
        l_prime_level = l_prime.get("level", 0) if isinstance(l_prime, dict) else 0
        l_bp = "Premium" if cap.get("hasElitePass") else "None"
        l_bp_badge = cap.get("badgeCnt", "N/A")
        leader_section = (
            f"    ├─ Leader Name: {cap.get('nickname','Not Found')}\n"
            f"    ├─ Leader UID: {cap.get('accountId','Not Found')}\n"
            f"    ├─ Leader Level: {cap.get('level','?')} (Exp: {cap.get('exp','?')})\n"
            f"    ├─ Leader Region: {cap.get('region','Not Found')}\n"
            f"    ├─ Leader Booyah Pass: {l_bp}\n"
            f"    ├─ Leader Created At: {ts_to_ist(cap.get('createAt'))}\n"
            f"    ├─ Leader Last Login: {ts_to_ist(cap.get('lastLoginAt'))}\n"
            f"    ├─ Leader Most Recent OB: {cap.get('releaseVersion','Not Found')}\n"
            f"    ├─ Leader Title Name: {cap.get('title','Not Found') or 'Not Found'}\n"
            f"    ├─ Leader Current Bp Badges: {l_bp_badge}\n"
            f"    ├─ Leader Br Rank: {l_br_str}\n"
            f"    └─ Leader Cs Rank: {l_cs_str}\n"
        )

    craft_str = "Not Found"
    if craftland:
        craft_str = "\n".join([f"• {m.get('mapName','Unknown')} (ID: {m.get('mapId','?')})" for m in craftland[:5]])

    signature = social.get("signature", "Not Found") or "Not Found"

    text = (
        f"🎮 *Account Information:*\n"
        f"┌ Basic Information:\n"
        f"├─ Prime Level: {prime_level}\n"
        f"├─ Name: {b.get('nickname','Not Found')}\n"
        f"├─ UID: {b.get('accountId','Not Found')}\n"
        f"├─ Level: {b.get('level','?')} (Exp: {b.get('exp','?')})\n"
        f"├─ Region: {b.get('region','Not Found')}\n"
        f"├─ Likes: {b.get('liked','0')}\n"
        f"├─ Honor Score: {credit.get('creditScore','100')}\n"
        f"├─ Celebrity Status: {bool(b.get('celebrityStatus', 0))}\n"
        f"├─ Title Name: {b.get('title','Not Found') or 'Not Found'}\n"
        f"└─ Signature: {signature}\n\n"
        f"┌ Activity Information:\n"
        f"├─ Most Recent OB: {b.get('releaseVersion','Not Found')}\n"
        f"├─ Booyah Pass: {bp_str}\n"
        f"├─ Current Bp Badges: {bp_badge}\n"
        f"├─ Br Rank: {br_rank_str}\n"
        f"├─ Cs Rank: {cs_rank_str}\n"
        f"├─ Gender: {gender}\n"
        f"├─ Show Rank: {show_rank}\n"
        f"├─ Show Br Rank: {b.get('showBrRank', True)}\n"
        f"├─ Show Cs Rank: {b.get('showCsRank', True)}\n"
        f"├─ Created At: {ts_to_ist(b.get('createAt'))}\n"
        f"└─ Last Login: {ts_to_ist(b.get('lastLoginAt'))}\n\n"
        f"┌ Overview Information:\n"
        f"├─ Avatar Name: Not Found\n"
        f"├─ Banner Name: Not Found\n"
        f"├─ Pin Name: Not Found\n"
        f"├─ Active Time: {time_active}\n"
        f"├─ Active Days: {days_active}\n"
        f"├─ Mode Prefer: {mode_prefer}\n"
        f"├─ Equipped Skills: {skills_str}\n"
        f"├─ Language: {social.get('language','Not Found') or 'Not Found'}\n"
        f"├─ Equipped Battle Card Name: Not Equipped\n"
        f"├─ Equipped Gun Name: Not Found\n"
        f"├─ Equipped Animation Name: Not Found\n"
        f"├─ Transform Animation Name: Not Found\n"
        f"└─ Outfits: Graphically Presented Below\n\n"
        f"┌ Pet Details:\n"
        f"├─ Equipped?: {pet_equipped}\n"
        f"├─ Pet Name: {pet_name}\n"
        f"├─ Pet Type: {pet_name}\n"
        f"├─ Pet Exp: {pet_exp}\n"
        f"└─ Pet Level: {pet_level}\n\n"
        f"┌ Guild Information:\n"
        f"├─ Guild Name: {guild_name}\n"
        f"├─ Guild ID: {guild_id}\n"
        f"├─ Guild Level: {guild_level}\n"
        f"├─ Live Members: {guild_members}\n"
        f"└─ Leader Information:\n"
        f"{leader_section}"
        f"┌ Public Craftland Maps\n"
        f"{craft_str}"
    )

    try:
        banner_bytes = fetch_banner_image(data)
        outfit_bytes = fetch_outfit_image(data)
        caption = text[:1024]
        rest = text[1024:]
        await update.message.reply_photo(photo=banner_bytes, caption=caption, parse_mode="Markdown")
        if rest:
            await update.message.reply_text(rest, parse_mode="Markdown")
        await update.message.reply_photo(photo=outfit_bytes, caption="👕 Outfit")
        await msg.delete()
    except Exception:
        chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
        await msg.edit_text(chunks[0], parse_mode="Markdown")
        for chunk in chunks[1:]:
            await update.message.reply_text(chunk, parse_mode="Markdown")

async def invite5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/invite5 <uid>`", parse_mode="Markdown")
        return

    uid = context.args[0].strip()
    if not uid.isdigit():
        await update.message.reply_text("❌ UID sirf numbers mein hona chahiye.", parse_mode="Markdown")
        return

    msg = await update.message.reply_text("📨 5-Lobby invite bhej raha hoon...")

    try:
        url = f"https://emoteapi-5lobbyapi.stargmr.pro/api/public/5?uid={uid}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") == "success":
            total_bots = data.get("total_bots", "?")
            message = data.get("message", "Invite sent!")
            text = (
                f"✅ *5-Lobby Invite Sent!*\n\n"
                f"🆔 UID: `{uid}`\n"
                f"🤖 Bots Used: `{total_bots}`\n"
                f"📨 Message: `{message}`"
            )
        else:
            text = f"❌ Invite fail hua.\n\nResponse: `{data}`"

        await msg.edit_text(text, parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(f"❌ Error aaya: `{e}`", parse_mode="Markdown")

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    async def post_init(application):
        await application.bot.delete_webhook(drop_pending_updates=True)

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_join_callback, pattern="^verify_join$"))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("level", level))
    app.add_handler(CommandHandler("bancheck", bancheck))
    app.add_handler(CommandHandler("isban", isban))
    app.add_handler(CommandHandler("wishlist", wishlist))
    app.add_handler(CommandHandler("guildleader", guildleader))
    app.add_handler(CommandHandler("invite5", invite5))
    print("Bot started...")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
