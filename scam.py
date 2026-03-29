import logging
import sqlite3
import asyncio
import urllib.request
import urllib.error
import json
import re
import random
from datetime import datetime
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.constants import ParseMode, ChatType
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.error import TelegramError

# ==========================================
# ⚙️ ADVANCED CONFIGURATION & SETUP ⚙️
# ==========================================

BOT_TOKEN = "8583222284:AAHHFwe2dm1ogYZjvW09eL67TxJdQs6_c8M"
ADMIN_IDS = [8709399313] 
BOT_LINK = "https://t.me/verox_info_bot"

# Customization Links & Media
FORCE_JOIN_PHOTO = "https://files.catbox.moe/ii7upg.jpg"
QR_CODE_PHOTO = "https://ibb.co/mF5Ry1pj"                 
UPI_ID = "rajdeeprg0001@fam"                 
TRX_ADDRESS = "TRry6XS8pHxjx6JLXarXNrNuAHydZcCfzd"        
BINANCE_ID = "1018426331"                                 

# API Endpoints
NUM1_API = "https://yttttttt./?key=DARKOSINT&num="
NUM2_API = "https://nuiservices.workers.dev/mobikup?key=CRYSTAAPI&mobile="
NUM3_API = "https://username-to-number.verdayne&num="

TG1_API = "https://telegram-to-num.vercel.ayy&term="
TG2_API = "https://ansh-apis.is-h&q="
TG3_API = "https://username-to-number.vercel.adayne&q="

ADHR_API = "https://aadasapiservices.workers.devid_num="
FAM_API  = "https://number8899.vercel.apadhar=" 
VEHICLE_API = "https://vehcile.vepp/api/rc-search?nber="
IFSC_API = "https://abbael.app/api/ifsc?ifsc="
IMEI_API = "https://imei-info.gaura6.workers.dev/?imei="

# Secure Tunnels Setup (Verification)
REQUIRED_CHATS = [
    {"id": -1003627302252, "url": "https://t.me/veroxprtl", "name": "💠 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 💠"},
    
    {"id": -1003292664118, "url": "https://t.me/verox_chats", "name": "💬 𝗩𝗜𝗣 𝗖𝗵𝗮𝘁 𝗟𝗼𝘂𝗻𝗴𝗲 💬"}
]

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

pending_admin_messages = {}
pending_checkouts = {}
user_search_state = {} 

PACKAGES = {
    "pkg120": {"credits": 120, "name": "120 Credits VIP"},
    "pkg250": {"credits": 250, "name": "250 Credits Elite"},
    "pkg550": {"credits": 550, "name": "550 Credits Master"},
    "pkg1000": {"credits": 1000, "name": "1000 Credits Supreme"}
}

# ==========================================
# 🌍 100% FULL SYSTEM LOCALIZATION 🌍
# ==========================================
LANGUAGES = {
    "en": {
        "name": "🇬🇧 English",
        "msg_greet": "🔥 *Welcome to the Advanced OSINT Terminal!*",
        "msg_main": "🎛 *Premium Command Dashboard Activated*\nUse the buttons below to navigate quickly!",
        "msg_back_main": "🎛 *Main Menu Restored*\nSelect an option below:",
        "stat": "📊 *Your Statistics:*", "status": "Status:", "searches": "Searches Done:", "refs": "Total Referrals:", "cred": "Available Credits:",
        "refer_promo": "💸 *REFER & EARN FREE SEARCHES* 💸\n━━━━━━━━━━━━━━━━━━━━━\nInvite your friends to our bot! For every friend that joins and verifies, you earn *+1 Premium Credit*.\n\n🔗 *Tap to copy your unique link:*\n",
        "lbl_live_db": "👤 *LIVE DATABASE IDENTITY*", "lbl_credits_support": "🛡️ System: Advanced OSINT Grid", "lbl_made_by": "🔐 Connection: Secure",
        # UI Buttons (Main Menu)
        "btn_num": "📱 Number Search", "btn_tg": "✈️ Telegram ID", "btn_adhr": "🪪 Aadhar Search", "btn_fam": "👥 Aadhar Family",
        "btn_veh": "🚗 Vehicle RC", "btn_ifsc": "🏦 Bank IFSC", "btn_imei": "📱 IMEI Info", "btn_unlim_search": "♾️ Unlimited Search Here",
        "btn_buy": "💎 Buy Premium", "btn_ref": "🎁 Refer & Earn Credits", "btn_redeem": "🎟️ Redeem Code", "btn_status": "👤 My Status",
        "btn_stats": "📊 Bot Stats", "btn_lead": "🏆 Leaderboard", "btn_admin": "👨‍💼 Admin Panel", "btn_dev": "👨‍💻 Architecture",
        # Sub Menus
        "btn_back_main": "🔙 Back to Main Menu", "btn_back_prem": "🔙 Back to Premium Menu", "btn_back_pay": "🔙 Back to Payment Methods",
        "btn_srv1": "💎 Server 1", "btn_srv2": "💎 Server 2", "btn_srv3": "💎 Server 3",
        "btn_tg1": "🆔 Server 1", "btn_tg2": "🆔 Server 2", "btn_tg3": "👤 Username to Num",
        "btn_adhr_lookup": "🏛️ Aadhar Lookup", "btn_fam_search": "👥 Family Search", "btn_veh_trace": "🏎️ Trace Vehicle RC",
        "btn_bank_intel": "🏦 Bank Intelligence", "btn_dev_trace": "📱 Device Trace",
        "btn_unlim_sub": "👑 Unlimited Refer Subscription", "btn_add_cred": "🪙 Add Credits",
        "btn_pay_upi": "💰 Pay with UPI (INR)", "btn_pay_trx": "🪙 Pay with Crypto (TRX)",
        # Plans & Pricing
        "btn_sub_3d": "⏳ 3 Days (10 🪙)", "btn_sub_7d": "⏳ 7 Days (21 🪙)", "btn_sub_15d": "⏳ 15 Days (35 🪙)", "btn_sub_30d": "⏳ 30 Days (50 🪙)",
        "btn_upi_120": "📦 UPI: 120 Credits (₹49)", "btn_upi_250": "📦 UPI: 250 Credits (₹99)", "btn_upi_550": "📦 UPI: 550 Credits (₹199)", "btn_upi_1000": "💎 UPI: 1000 Credits (₹399)",
        "btn_trx_120": "📦 TRX: 120 Credits (1.85 TRX)", "btn_trx_250": "📦 TRX: 250 Credits (3.75 TRX)", "btn_trx_550": "📦 TRX: 550 Credits (7.55 TRX)", "btn_trx_1000": "💎 TRX: 1000 Credits (15 TRX)",
        # Internal User Prompts
        "msg_store": "💎 *PREMIUM EXCLUSIVE STORE* 💎\n━━━━━━━━━━━━━━━━━━━━━\n\nWelcome to the VIP Premium Store. Elevate your OSINT experience with unlimited access and priority servers.\n\n👇 *Select a premium category below:*",
        "msg_subs": "👑 *UNLIMITED PREMIUM SUBSCRIPTIONS* 👑\n━━━━━━━━━━━━━━━━━━━━━\n\nUnlock *Zero-Deduction* unlimited searches. Choose a VIP plan below to activate instantly.\n\n✨ *Features included:* \n┠ 🚀 Priority Server Access\n┠ ♾️ No Credit Deductions\n┖ 🛡️ Advanced Identity Tracing",
        "msg_gateway": "🪙 *PURCHASE PREMIUM CREDITS* 🪙\n━━━━━━━━━━━━━━━━━━━━━\n\nTop up your account securely. Select your preferred high-speed payment gateway below:\n\n💳 *Supported Gateways:*\n┠ 🇮🇳 Secure UPI (India)\n┖ 🌐 Fast Crypto TRX (Global)",
        "msg_upi_checkout": "🏦 *SECURE UPI CHECKOUT (INR)* 🏦\n━━━━━━━━━━━━━━━━━━━━━\n\nSelect a premium credit package below to instantly generate your VIP checkout session:",
        "msg_trx_checkout": "🌐 *SECURE CRYPTO CHECKOUT (TRX)* 🌐\n━━━━━━━━━━━━━━━━━━━━━\n\nSelect a premium credit package below to instantly generate your VIP checkout session:",
        "msg_upi_inst": "1️⃣ Scan the QR Code attached or pay securely to this UPI ID:\n`{upi_id}`",
        "msg_trx_inst": "1️⃣ Send EXACTLY {amount_str} to this \n\nBinance ID: `{binance_id}`\n\nTRX Wallet Address:\n`{trx_address}`",
        "msg_dev": "👨‍💻 *SYSTEM ARCHITECTURE*\n━━━━━━━━━━━━━━━━━━━━━\n\nThis Terminal is maintained by the Advanced OSINT Grid. Direct contact has been disabled for security purposes.",
        "msg_redeem_prompt": "🎟️ *REDEEM GIFT CODE*\n━━━━━━━━━━━━━━━━━━━━━\n👆 *Please enter your Gift Code below:*",
        "msg_modules": "📱 *INTELLIGENCE MODULE*\n━━━━━━━━━━━━━━━━━━━━━\nPlease select a tool or server below to begin your search:",
        # Prompts
        "prompt_num1": "📡 *[ TELECOM INTEL: SERVER 1 ]*\n━━━━━━━━━━━━━━━━━━━━━\nProvide the target MSISDN for deep packet inspection.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `10-Digit Mobile Number`\n┠ *Test Value:* `9876543210`\n┖ *Constraint:* `Exclude country code (e.g., +91).`\n\n_Awaiting target input..._",
        "prompt_num2": "📡 *[ TELECOM INTEL: SERVER 2 ]*\n━━━━━━━━━━━━━━━━━━━━━\nProvide the target MSISDN for deep packet inspection.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `10-Digit Mobile Number`\n┠ *Test Value:* `9988776655`\n┖ *Constraint:* `Exclude country code (e.g., +91).`\n\n_Awaiting target input..._",
        "prompt_num3": "📡 *[ TELECOM INTEL: SERVER 3 ]*\n━━━━━━━━━━━━━━━━━━━━━\nProvide the target MSISDN for deep packet inspection.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `10-Digit Mobile Number`\n┠ *Test Value:* `9123456780`\n┖ *Constraint:* `Exclude country code (e.g., +91).`\n\n_Awaiting target input..._",
        "prompt_tg1": "🆔 *[ TELEGRAM OSINT: SERVER 1 ]*\n━━━━━━━━━━━━━━━━━━━━━\nProvide the target numerical Telegram ID.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `Numerical ID`\n┠ *Test Value:* `123456789`\n┖ *Constraint:* `Do NOT input @usernames.`\n\n_Awaiting target input..._",
        "prompt_tg2": "🆔 *[ TELEGRAM OSINT: SERVER 2 ]*\n━━━━━━━━━━━━━━━━━━━━━\nProvide the target numerical Telegram ID.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `Numerical ID`\n┠ *Test Value:* `987654321`\n┖ *Constraint:* `Do NOT input @usernames.`\n\n_Awaiting target input..._",
        "prompt_tg3": "👤 *[ USERNAME DE-ANONYMIZER ]*\n━━━━━━━━━━━━━━━━━━━━━\nTrace a Telegram alias to its origin node.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `Alphanumeric Alias`\n┠ *Test Value:* `STAR_PROOO`\n┖ *Constraint:* `Exclude the '@' symbol.`\n\n_Awaiting target input..._",
        "prompt_adhr": "🏛️ *[ NATIONAL IDENTITY TRACE ]*\n━━━━━━━━━━━━━━━━━━━━━\nQuery the UIDAI database for demographic data.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `12-Digit UID`\n┠ *Test Value:* `123456789012`\n┖ *Constraint:* `No spaces or dashes.`\n\n_Awaiting target input..._",
        "prompt_fam": "👥 *[ FAMILY NETWORK TRACE ]*\n━━━━━━━━━━━━━━━━━━━━━\nQuery demographic relationships linked to UID.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `12-Digit UID`\n┠ *Test Value:* `123456789012`\n┖ *Constraint:* `No spaces or dashes.`\n\n_Awaiting target input..._",
        "prompt_veh": "🏎️ *[ VEHICLE REGISTRY TRACE ]*\n━━━━━━━━━━━━━━━━━━━━━\nQuery VAHAN database for owner and chassis intel.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `Alphanumeric License Plate`\n┠ *Test Value:* `DL01AB1234`\n┖ *Constraint:* `No spaces (e.g., DL01AB1234).`\n\n_Awaiting target input..._",
        "prompt_ifsc": "🏦 *[ FINANCIAL NODE LOOKUP ]*\n━━━━━━━━━━━━━━━━━━━━━\nTrace Bank IFSC codes to physical branch nodes.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `11-Character IFSC`\n┠ *Test Value:* `SBIN0001234`\n┖ *Constraint:* `Must be valid Indian IFSC.`\n\n_Awaiting target input..._",
        "prompt_imei": "📱 *[ HARDWARE IDENTITY TRACE ]*\n━━━━━━━━━━━━━━━━━━━━━\nTrace device origins via IMEI fingerprint.\n\n📌 *PARAMETERS & SYNTAX:*\n┠ *Data Type:* `15-Digit IMEI`\n┠ *Test Value:* `123456789012345`\n┖ *Constraint:* `Numbers only.`\n\n_Awaiting target input..._",
        "cancel_prompt": "\nOr select *🔙 Back to Main Menu* to cancel.",
        # Admin Panel
        "msg_admin_panel": "🛠 *ADVANCED ADMIN CONTROL PANEL* 🛠\n━━━━━━━━━━━━━━━━━━━━━\nSelect an administration tool below:",
        "btn_admin_bc": "📢 Broadcast", "btn_admin_sc": "📋 See Codes", "btn_admin_ap": "➕ Add Point", "btn_admin_rp": "➖ Remove Point",
        "btn_admin_ban": "⛔️ Ban", "btn_admin_unban": "🟢 Unban", "btn_admin_addp": "💎 Add Premium", "btn_admin_rmp": "🗑 Remove Premium",
        "btn_admin_mc": "🎁 Make Code", "btn_admin_dc": "🗑 Delete Code", "btn_back_admin": "🔙 Back to Admin Menu",
        # Dynamic Search / Errors
        "search_fail": "📭 *DATA NOT AVAILABLE*\n━━━━━━━━━━━━━━━━━━━━━\n❌ *Search Info Not Found:*\nNo data is available in the database for this specific query.",
        "invalid_input": "❌ *[ SYNTAX ERROR ] Input format does not match required parameters.*",
        "invalid_num": "❌ *[ SYNTAX ERROR ] Invalid Number! Please enter a valid 10-digit mobile number.*",
        "invalid_tg": "❌ *[ SYNTAX ERROR ] Invalid Telegram ID/Username!*",
        "result_lbl": "Result",
        "result_no_data": "✨ No relevant data found.\n",
        "stat_tot": "Total Searches Run:", "stat_ded": "Deducted:", "stat_rem": "Remaining Credits:", "stat_acc": "Access Mode:",
        # Global Translation Additions
        "err_insuff_cred": "❌ *INSUFFICIENT CREDITS*\n\nYou need *{cost} Credits* to purchase the *{days}-Day VIP Plan*.\nYour current balance: *{curr_credits} Credits*.\n\n💡 *How to get more Credits:*\n💰 *Buy:* Go back and select 🪙 Add Credits to pay securely.\n🎁 *Refer:* Share your unique link via 🎁 Refer & Earn Credits to earn free credits!\n\nPlease gather enough credits to proceed.",
        "msg_sub_success": "🎉 *VIP SUBSCRIPTION ACTIVATED!* 🎉\n━━━━━━━━━━━━━━━━━━━━━\n\n✅ You have successfully unlocked *{days} Days* of Unlimited Searches!\n\n💰 *Balance Deducted:* `{cost} Credits`\n⏳ *Premium Valid Until:* `{expiry_dt}`\n\nEnjoy your exclusive priority access! 🚀",
        "msg_force_join": "⚠️ *Premium Verification Required*\n\n🚀 You must join all our private channels and groups to verify your account and unlock the bot features.",
        "msg_private_only": "👑 *PREMIUM PRIVATE ACCESS ONLY* 👑\n━━━━━━━━━━━━━━━━━━━━━\n\n🛑 *Group Usage Disabled*\nThis is an advanced private database bot. To protect your search queries and maintain extreme performance, group commands are strictly prohibited.\n\n🔗 *Tap here to use me privately:*",
        "msg_group_small": "🛑 *[ CRITICAL SYSTEM ERROR ]* 🛑\n━━━━━━━━━━━━━━━━━━━━━\n\n⚠️ *CONNECTION REFUSED:* Target Node insufficient.\n\nThis Cyber Terminal requires a massive computational node to bypass rate limits. The current group has less than the *500-member minimum* required.\n\n🛑 *Protocol:* `Severing Connection...`\n\n💡 _Expand this grid to 500+ agents and deploy me again!_",
        "msg_group_welcome": "👑 *[ ROOT ] OSINT TERMINAL INSTALLED* 👑\n━━━━━━━━━━━━━━━━━━━━━\n\n🟢 *System Status:* `Online & Bypassed`\n🎁 *Grid Perk:* `100% Free & Unlimited Traces!`\n\n⚡ *EXECUTE MODULES BELOW:* ⚡\n\n📱 *[ TELECOM INTELLIGENCE ]*\n ┣ 🟢 `/num1` ➔ Server 1 (Ex: `/num1 9876543210`)\n ┣ 🟡 `/num2` ➔ Server 2 (Ex: `/num2 9988776655`)\n ┗ 🔴 `/num3` ➔ Server 3 (Ex: `/num3 9123456780`)\n\n✈️ *[ TELEGRAM IDENTITY ]*\n ┣ 🆔 `/tg1` ➔ TG Server 1 (Ex: `/tg1 123456789`)\n ┣ 🆔 `/tg2` ➔ TG Server 2 (Ex: `/tg2 987654321`)\n ┗ 👤 `/tg3` ➔ Username (Ex: `/tg3 STAR_PROOO`)\n\n🪪 *[ NATIONAL DATABASE ]*\n ┣ 🏛️ `/adhr` ➔ Aadhar Info (Ex: `/adhr 123456789012`)\n ┗ 👥 `/fam`  ➔ Family Tree (Ex: `/fam 987654321098`)\n\n🏢 *[ REGISTRY & FINANCE ]*\n ┣ 🏎️ `/veh`  ➔ Vehicle RC (Ex: `/veh DL01AB1234`)\n ┣ 🏦 `/ifsc` ➔ Bank Details (Ex: `/ifsc SBIN0001234`)\n ┗ 📱 `/imi`  ➔ IMEI Trace (Ex: `/imi 123456789012345`)\n\n━━━━━━━━━━━━━━━━━━━━━\n💡 _Input a module command to extract live intelligence._",
        "msg_top_refs": "🏆 *TOP 10 REFERRAL LEADERBOARD* 🏆\n━━━━━━━━━━━━━━━━━━━━━\n\n",
        "msg_bot_stats": "📊 *Advanced Bot Statistics*\n━━━━━━━━━━━━━━━━━━━━━\n",
        "msg_checkout_init": "🛒 *VIP PAYMENT CHECKOUT INITIATED*\n━━━━━━━━━━━━━━━━━━━━━\n\n📦 *Package Selected:* {pkg_name}\n💵 *Amount Due:* {amount_str}\n\n🏦 *PAYMENT INSTRUCTIONS:*\n{instructions}\n\n2️⃣ Take a clear screenshot of your successful payment receipt.\n3️⃣ Send the screenshot directly HERE to this bot NOW!\n\n⏳ _Awaiting your receipt for instant automated verification..._",
        # Security & Core Features
        "msg_banned": "⛔️ *You are permanently banned from using this terminal.*",
        "msg_maintenance": "⚙️ *Terminal is currently under maintenance!* Please try again later.",
        "msg_verify_success": "✅ Verification Successful!",
        "msg_ref_unlocked": "🎉 *BOOM! NEW REFERRAL UNLOCKED!* 🎉\n━━━━━━━━━━━━━━━━━━━━━\n\n✅ *A new user joined using your link and verified their account!*\n\n🎁 *Reward Claimed:* `+1 Premium Credit` 🪙\n\n💡 _Keep sharing your link to earn more credits._",
        "msg_access_denied": "🛑 *ACCESS DENIED: INSUFFICIENT CREDITS* 🛑\n━━━━━━━━━━━━━━━━━━━━━\n\n⚠️ You need an active subscription or at least *1 Credit* to execute this search.",
        "msg_pls_init_buy": "❌ *Please initiate a purchase first!*\n\nClick the *💎 Buy Premium* button to select a package before sending payment screenshots.",
        "msg_receipt_received": "✅ *Receipt Received!* Sent to VIP admins for rapid verification. Please allow a few moments.",
        "status_title": "YOUR PREMIUM STATUS & PROFILE", "lbl_id_over": "Identity Overview:", "lbl_name": "Name:", "lbl_uname": "Username:", 
        "lbl_uid": "User ID:", "lbl_acc_stat": "Account Statistics:", "lbl_acc": "Account Type:", "lbl_cred": "Available Credits:", 
        "lbl_tot": "Total Searches:", "lbl_ref": "Total Referrals:", "lbl_join": "Joined System:", "msg_upgrade": "Want unlimited searches? Upgrade tier.",
        "lbl_vip": "👑 VIP PREMIUM\n┖ *Valid Till:*", "lbl_free": "🆓 STANDARD (Free Tier)",
        "ref_title": "REFER & EARN PREMIUM SYSTEM", "ref_sub": "Share your VIP link and earn free Search Credits!", 
        "ref_link_lbl": "Your Unique Link:", "ref_bal": "Your Balance:", "ref_tot": "Total Referrals:", 
        "ref_redeem": "REDEEM SUBSCRIPTIONS BELOW", "ref_use": "Use your earned credits to activate unlimited searches instantly!",
        # OSINT DB Keys for Translation
        "osint_keys": {
            "name": "Name", "address": "Address", "mobile": "Mobile", "phone": "Phone", 
            "father": "Father's Name", "mother": "Mother's Name", "dob": "Date of Birth", 
            "email": "Email", "gender": "Gender", "city": "City", "state": "State", 
            "zip": "Zip Code", "pincode": "Pincode", "aadhar": "Aadhar No.", "pan": "PAN No.",
            "bank": "Bank Name", "ifsc": "IFSC Code", "account": "Account No.", "branch": "Branch",
            "imei": "IMEI No.", "brand": "Brand", "model": "Model", "color": "Color",
            "operator": "Operator", "circle": "Telecom Circle", "vehicle": "Vehicle Class",
            "engine": "Engine No.", "chassis": "Chassis No.", "owner": "Owner Name"
        }
    }
}

# Fallback for other languages
for lang in ["hi", "es", "ar", "ru", "pt", "id"]:
    if lang not in LANGUAGES: 
        LANGUAGES[lang] = LANGUAGES["en"].copy()

REVERSE_BTN_MAP = {}
for lang_code, translations in LANGUAGES.items():
    for key, value in translations.items():
        if key.startswith("btn_"):
            REVERSE_BTN_MAP[value] = key

# ==========================================
# 🛠 CORE UTILITY FUNCTIONS 🛠
# ==========================================

def esc_md(text):
    if not text: return "None"
    return str(text).replace("_", "\\_").replace("*", "\\*").replace("`", "'").replace("[", "\\[")

def esc_html(text):
    if not text: return "None"
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def fetch_data_sync(url: str):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.getcode() == 200:
                raw_text = response.read().decode('utf-8')
                try: return json.loads(raw_text)
                except json.JSONDecodeError: return {"Result": raw_text}
            return None
    except Exception as e:
        logger.error(f"Sync fetch error for URL {url}: {e}")
        return None

# ==========================================
# 🗄️ MASTER DATABASE ENGINE 🗄️
# ==========================================

def run_query(query, args=(), fetchall=False, fetchone=False):
    conn = sqlite3.connect("bot_database.db", check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute(query, args)
        if fetchall: res = c.fetchall()
        elif fetchone: res = c.fetchone()
        else:
            conn.commit()
            res = True
        return res
    except sqlite3.Error as e: return None
    finally: conn.close()

def init_db():
    conn = sqlite3.connect("bot_database.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, total_searches INTEGER DEFAULT 0, referred_by INTEGER, referrals INTEGER DEFAULT 0, is_banned INTEGER DEFAULT 0, is_verified INTEGER DEFAULT 0, premium_expiry INTEGER DEFAULT 0)""")
    columns = [("is_banned", "INTEGER DEFAULT 0"), ("is_verified", "INTEGER DEFAULT 0"), ("joined_date", "TEXT"), ("credits", "INTEGER DEFAULT 1"), ("first_name", "TEXT"), ("username", "TEXT"), ("premium_expiry", "INTEGER DEFAULT 0"), ("language", "TEXT DEFAULT 'en'")]
    for col_name, col_type in columns:
        try: c.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError: pass

    c.execute("CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER PRIMARY KEY, group_name TEXT, joined_date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('maintenance', '0')")
    c.execute("CREATE TABLE IF NOT EXISTS gift_codes (code TEXT PRIMARY KEY, points INTEGER, max_uses INTEGER, used_count INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS claimed_codes (user_id INTEGER, code TEXT, PRIMARY KEY(user_id, code))")
    conn.commit()
    conn.close()

def add_user(user_id: int, referred_by: int = None, first_name: str = "Unknown", username: str = "None"):
    row = run_query("SELECT user_id FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    if not row:
        today = datetime.now().strftime("%Y-%m-%d")
        run_query("INSERT INTO users (user_id, referred_by, joined_date, credits, first_name, username, premium_expiry, language) VALUES (?, ?, ?, ?, ?, ?, 0, 'en')", (user_id, referred_by, today, 1, first_name, username))
        return True, referred_by
    else:
        run_query("UPDATE users SET first_name = ?, username = ? WHERE user_id = ?", (first_name, username, user_id))
        return False, None

def get_user_lang(user_id: int) -> str:
    row = run_query("SELECT language FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    return row[0] if row else "en"

def is_bot_maintenance():
    row = run_query("SELECT value FROM settings WHERE key = 'maintenance'", fetchone=True)
    return row and row[0] == '1'

def set_bot_maintenance(state: bool):
    val = '1' if state else '0'
    run_query("UPDATE settings SET value = ? WHERE key = 'maintenance'", (val,))

# ==========================================
# 🎛️ DYNAMIC LOCALIZED KEYBOARDS 🎛️
# ==========================================

async def setup_commands(application: Application):
    commands = [BotCommand("start", "Launch or Refresh the Bot System")]
    await application.bot.set_my_commands(commands)

def get_premium_keyboard(lang='en'):
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    keyboard = [
        [KeyboardButton(t["btn_num"]), KeyboardButton(t["btn_tg"])],
        [KeyboardButton(t["btn_adhr"]), KeyboardButton(t["btn_fam"])], 
        [KeyboardButton(t["btn_veh"]), KeyboardButton(t["btn_ifsc"])],
        [KeyboardButton(t["btn_imei"]), KeyboardButton(t["btn_buy"])],
        [KeyboardButton(t["btn_ref"]), KeyboardButton(t["btn_redeem"])],
        [KeyboardButton(t["btn_status"]), KeyboardButton(t["btn_stats"])],
        [KeyboardButton(t["btn_lead"]), KeyboardButton(t["btn_admin"])],
        [KeyboardButton(t["btn_dev"]), KeyboardButton(t["btn_unlim_search"])]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

def get_admin_keyboard(lang='en'):
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    keyboard = [
        [KeyboardButton(t["btn_admin_bc"]), KeyboardButton(t["btn_admin_sc"])],
        [KeyboardButton(t["btn_admin_ap"]), KeyboardButton(t["btn_admin_rp"])],
        [KeyboardButton(t["btn_admin_ban"]), KeyboardButton(t["btn_admin_unban"])],
        [KeyboardButton(t["btn_admin_addp"]), KeyboardButton(t["btn_admin_rmp"])],
        [KeyboardButton(t["btn_admin_mc"]), KeyboardButton(t["btn_admin_dc"])],
        [KeyboardButton(t["btn_back_main"])]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

def get_admin_cancel_keyboard(lang='en'):
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    return ReplyKeyboardMarkup([[KeyboardButton(t["btn_back_admin"])]], resize_keyboard=True, is_persistent=True)

def get_cancel_keyboard(lang='en'):
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    return ReplyKeyboardMarkup([[KeyboardButton(t["btn_back_main"])]], resize_keyboard=True, is_persistent=True)

def get_subscription_keyboard(lang='en'):
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    keyboard = [
        [KeyboardButton(t.get("btn_sub_3d", "⏳ 3 Days (10 🪙)")), KeyboardButton(t.get("btn_sub_7d", "⏳ 7 Days (21 🪙)"))],
        [KeyboardButton(t.get("btn_sub_15d", "⏳ 15 Days (35 🪙)")), KeyboardButton(t.get("btn_sub_30d", "⏳ 30 Days (50 🪙)"))],
        [KeyboardButton(t["btn_back_main"])]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

# ==========================================
# 🛡️ SECURITY, GROUPS, & VERIFICATION 🛡️
# ==========================================

async def notify_admins_group_event(context: ContextTypes.DEFAULT_TYPE, chat, user, event_type: str):
    try: member_count = await chat.get_member_count()
    except Exception: member_count = "Unknown"
        
    link = f"@{chat.username}" if chat.username else "Private Group / No Link"
    if not chat.username:
        try: link = await chat.export_invite_link()
        except Exception: pass

    safe_link = link.replace("_", "\\_") if "@" in link else link
    safe_name = esc_md(chat.title)
    
    if user:
        safe_user = esc_md(user.first_name)
        user_id = user.id
    else:
        safe_user = "System/Unknown"
        user_id = "0"

    msg = (
        "🚀 *SYSTEM VERSION UPDATE* 🚀\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💠 *BOT {event_type} DETECTED* 💠\n\n"
        f"📌 *Group Name:* {safe_name}\n"
        f"🔗 *Group Link:* {safe_link}\n"
        f"👥 *Total Members:* `{member_count}`\n"
        f"🆔 *Group ID:* `{chat.id}`\n"
        f"👤 *Action By:* {safe_user} (`{user_id}`)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )

    for admin_id in ADMIN_IDS:
        try: await context.bot.send_message(chat_id=admin_id, text=msg, parse_mode=ParseMode.MARKDOWN)
        except Exception: pass

async def send_group_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int, lang: str = "en"):
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    msg = t.get("msg_group_welcome")
    keyboard = [
        [InlineKeyboardButton("➕ Add to me your own group", url=f"{BOT_LINK}?startgroup=true")],
        [InlineKeyboardButton("♾️ Unlimited search here free", url="https://t.me/+IzVdb9z7Bvs4YWQ1")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    try:
        await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN, reply_markup=markup, disable_web_page_preview=True)
    except Exception: pass

async def on_new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """STRICT 500 MEMBER ENFORCEMENT & ADMIN OVERRIDE"""
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            chat = update.effective_chat
            adder = update.message.from_user 
            if not adder: return
            
            try:
                member_count = await chat.get_member_count()
            except Exception:
                member_count = 0
                
            is_admin = adder.id in ADMIN_IDS

            if member_count < 500 and not is_admin:
                lang = get_user_lang(adder.id) if adder else "en"
                t = LANGUAGES.get(lang, LANGUAGES['en'])
                leave_msg = t.get("msg_group_small")
                try:
                    await context.bot.send_message(chat_id=chat.id, text=leave_msg, parse_mode=ParseMode.MARKDOWN)
                    await asyncio.sleep(2)  
                    await chat.leave()
                    return 
                except Exception:
                    pass
            
            today = datetime.now().strftime("%Y-%m-%d")
            run_query("INSERT OR IGNORE INTO groups (chat_id, group_name, joined_date) VALUES (?, ?, ?)", (chat.id, chat.title, today))
            await notify_admins_group_event(context, chat, adder, "ADD")
            
            lang = get_user_lang(adder.id) if adder else "en"
            await send_group_welcome(update, context, chat.id, lang)

async def on_left_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member and update.message.left_chat_member.id == context.bot.id:
        chat = update.effective_chat
        remover = update.message.from_user
        run_query("DELETE FROM groups WHERE chat_id = ?", (chat.id,))
        await notify_admins_group_event(context, chat, remover, "REMOVE")

async def check_ban_and_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not update.effective_user: return False
        
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name or "Unknown"
    username = update.effective_user.username or "None"
    lang = get_user_lang(user_id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    referred_by = None
    if update.effective_message and update.effective_message.text and update.effective_message.text.startswith('/start'):
        parts = update.effective_message.text.split()
        if len(parts) > 1 and parts[1].isdigit():
            referred_by = int(parts[1])

    is_new, actual_ref = add_user(user_id, referred_by, first_name, username)

    if is_new:
        tot_users = run_query("SELECT COUNT(*) FROM users", fetchone=True)[0]
        safe_username = esc_md('@' + username) if username != "None" else "None"
        admin_msg = (
            "👤 *NEW AGENT DETECTED* 👤\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 *Name:* {esc_md(first_name)}\n"
            f"📛 *Username:* {safe_username}\n"
            f"🆔 *ID:* `{user_id}`\n\n"
            f"📈 *Total Database:* `{tot_users}` Agents\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        for ad in ADMIN_IDS:
            try: await context.bot.send_message(chat_id=ad, text=admin_msg, parse_mode=ParseMode.MARKDOWN)
            except Exception: pass 
            
        if actual_ref and actual_ref != user_id:
            ref_lang = get_user_lang(actual_ref)
            ref_t = LANGUAGES.get(ref_lang, LANGUAGES['en'])
            pending_msg = (
                "⏳ *INCOMING REFERRAL PENDING...* ⏳\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                "👤 *Someone just started the bot using your invite link!*\n\n"
                "⚠️ *Status:* `Waiting for User Verification...`\n"
                "💡 _They must join all our required private channels before your +1 Premium Credit is securely added to your account._\n\n"
                "━━━━━━━━━━━━━━━━━━━━━"
            )
            try: await context.bot.send_message(chat_id=actual_ref, text=pending_msg, parse_mode=ParseMode.MARKDOWN)
            except Exception: pass

    if is_bot_maintenance() and user_id not in ADMIN_IDS:
        if update.effective_message:
            await update.effective_message.reply_text(t.get("msg_maintenance"), parse_mode=ParseMode.MARKDOWN)
        return False

    user_data = run_query("SELECT is_banned FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    if user_data and user_data[0] == 1:
        if update.effective_message:
            await update.effective_message.reply_text(t.get("msg_banned"), parse_mode=ParseMode.MARKDOWN)
        return False

    not_joined = []
    for chat in REQUIRED_CHATS:
        try:
            member = await context.bot.get_chat_member(chat_id=chat["id"], user_id=user_id)
            if member.status in ['left', 'kicked']: not_joined.append(chat)
        except TelegramError:
            not_joined.append(chat)

    if not_joined:
        if update.effective_message:
            if update.effective_chat.type != ChatType.PRIVATE:
                markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔒 Sync via DM", url=BOT_LINK)]])
                await update.effective_message.reply_text(f"⚠️ {first_name}, establish secure connection in my DM first!", reply_markup=markup)
                return False

            buttons = []
            for i in range(0, len(not_joined), 2):
                row = [InlineKeyboardButton(f"{not_joined[i]['name']}", url=not_joined[i]["url"])]
                if i + 1 < len(not_joined):
                    row.append(InlineKeyboardButton(f"{not_joined[i+1]['name']}", url=not_joined[i+1]["url"]))
                buttons.append(row)
                
            buttons.append([
                InlineKeyboardButton("✅", callback_data="check_join"),
                InlineKeyboardButton("🔄", callback_data="check_join")
            ])
            markup = InlineKeyboardMarkup(buttons)
            await update.effective_message.reply_photo(photo=FORCE_JOIN_PHOTO, caption=t.get("msg_force_join"), reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return False
    return True

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    not_joined = []
    for chat in REQUIRED_CHATS:
        try:
            member = await context.bot.get_chat_member(chat_id=chat["id"], user_id=user_id)
            if member.status in ['left', 'kicked']: not_joined.append(chat)
        except TelegramError: not_joined.append(chat)
            
    if not_joined:
        try: await query.answer("❌ You must join ALL channels first! Please Re-check.", show_alert=True)
        except Exception: pass
        
        buttons = []
        for i in range(0, len(not_joined), 2):
            row = [InlineKeyboardButton(f"{not_joined[i]['name']}", url=not_joined[i]["url"])]
            if i + 1 < len(not_joined): row.append(InlineKeyboardButton(f"{not_joined[i+1]['name']}", url=not_joined[i+1]["url"]))
            buttons.append(row)
            
        buttons.append([
            InlineKeyboardButton("✅", callback_data="check_join"),
            InlineKeyboardButton("🔄", callback_data="check_join")
        ])
        markup = InlineKeyboardMarkup(buttons)
        try: await query.edit_message_reply_markup(reply_markup=markup)
        except Exception: pass
        return

    try: await query.answer(t.get("msg_verify_success", "✅ Verification Successful!"), show_alert=False)
    except Exception: pass
    
    try: await query.message.delete()
    except Exception: pass
    
    await verify_user_referral(user_id, context)
    await send_main_menu(update, context, user_id)

async def verify_user_referral(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    row = run_query("SELECT is_verified, referred_by FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    if row and row[0] == 0:
        referred_by = row[1]
        run_query("UPDATE users SET is_verified = 1 WHERE user_id = ?", (user_id,))
        if referred_by and referred_by != user_id:
            run_query("UPDATE users SET referrals = referrals + 1, credits = credits + 1 WHERE user_id = ?", (referred_by,))
            
            ref_lang = get_user_lang(referred_by)
            ref_t = LANGUAGES.get(ref_lang, LANGUAGES['en'])
            
            try: await context.bot.send_message(chat_id=referred_by, text=ref_t.get("msg_ref_unlocked"), parse_mode=ParseMode.MARKDOWN)
            except Exception: pass

async def check_can_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not await check_ban_and_channels(update, context): return False
    
    if update.effective_chat.type != ChatType.PRIVATE:
        return True # Groups are 100% Free
    
    user_id = update.effective_user.id
    current_time = int(datetime.now().timestamp())
    lang = get_user_lang(user_id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    row = run_query("SELECT referrals, premium_expiry, credits FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    referrals, premium_expiry, credits = row if row else (0, 0, 0)
    
    has_premium = premium_expiry > current_time
    
    if not has_premium and credits <= 0:
        await update.effective_message.reply_text(t.get("msg_access_denied"), parse_mode=ParseMode.MARKDOWN)
        return False
    return True

# 🌟 BEAUTIFUL MESSAGE DELETION SYSTEM 🌟
async def clear_message_later(message: telegram.Message, delay: int = 30):
    if not message: return
    await asyncio.sleep(delay)
    try: 
        await message.edit_text(
            "🗑 *Message Deleted Successfully*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🔒 _Protected under Telegram Privacy Policy._", 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None,
            disable_web_page_preview=True
        )
    except Exception: 
        try: await message.delete()
        except: pass

async def delete_user_message_later(message: telegram.Message, delay: int = 30):
    if not message: return
    await asyncio.sleep(delay)
    try: await message.delete()
    except: pass

def format_premium_result(data, lang_dict, indent="") -> str:
    emoji_map = {
        "name": "👤", "father": "👨‍🦳", "address": "🏠", "mobile": "📱", 
        "phone": "📞", "alt": "📳", "circle": "🌍", "state": "🗺️", "id": "🪪", 
        "aadhar": "🏛️", "email": "📧", "gender": "🚻", "dob": "🎂", 
        "operator": "📶", "city": "🏙️", "pincode": "📍", "zip": "📮", 
        "status": "✅", "vehicle": "🚗", "engine": "⚙️", "chassis": "🔩",
        "bank": "🏦", "branch": "🏢", "ifsc": "🔢", "imei": "📱", 
        "brand": "🏷️", "model": "📲", "color": "🎨", "owner": "👑",
        "uid": "🎮", "level": "⭐", "guild": "🛡️", "likes": "❤️"
    }
    
    ignore_keys = [
        "your usage", "your_usage", "key name", "key_name", "your limit", 
        "your_limit", "your usage today", "your_usage_today", 
        "your remaining today", "your_remaining_today", "note", "owner", 
        "usage", "by", "credit", "credits", "developer", "admin", "help group", "help_group"
    ]
    skip_strings = ["@ftgamer2", "@anuragxanuu", "hackedanurag", "https://t.me/hackedanurag"]
    
    formatted_text = ""
    
    if indent == "" and isinstance(data, dict):
        if "data" in data and isinstance(data["data"], (dict, list)):
            data = data["data"]
        elif "result" in data and isinstance(data["result"], (dict, list)):
            data = data["result"]
            
    if isinstance(data, dict):
        for key, value in data.items():
            if value is None or str(value).strip() == "": continue
            if str(key).lower().strip() in ignore_keys: continue
            
            skip_item = False
            for s in skip_strings:
                if s in str(value).lower() or s in str(key).lower():
                    skip_item = True
                    break
            if skip_item: continue
            
            clean_key = str(key).replace("_", " ").title()
            emoji = "✨" 
            
            for k, e in emoji_map.items():
                if k in str(key).lower():
                    emoji = e
                    break
                    
            osint_keys = lang_dict.get("osint_keys", {})
            for k, v in osint_keys.items():
                if k in str(key).lower():
                    clean_key = v
                    break
            
            if isinstance(value, (dict, list)):
                formatted_text += f"{indent}{emoji} <b>{esc_html(clean_key)}</b>:\n"
                formatted_text += format_premium_result(value, lang_dict, indent + "   ")
            else:
                safe_val = esc_html(value)
                formatted_text += f"{indent}{emoji} <b>{esc_html(clean_key)}</b>: <tg-spoiler>{safe_val}</tg-spoiler>\n"
                
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                formatted_text += format_premium_result(item, lang_dict, indent + "   ") + f"{indent}➖\n"
            else:
                skip_item = False
                for s in skip_strings:
                    if s in str(item).lower():
                        skip_item = True
                        break
                if skip_item: continue 
                safe_item = esc_html(item)
                formatted_text += f"{indent}✨ <tg-spoiler>{safe_item}</tg-spoiler>\n"
    else:
        skip_item = False
        for s in skip_strings:
            if s in str(data).lower():
                skip_item = True
                break
        if not skip_item:
            formatted_text += f"{indent}✨ {lang_dict['result_lbl']}: <tg-spoiler>{esc_html(data)}</tg-spoiler>\n"

    if indent == "":
        if formatted_text.strip() == "": formatted_text = lang_dict['result_no_data']
    return formatted_text

# ==========================================
# 🖥️ MAIN MENU & COMMAND LOGIC 🖥️
# ==========================================

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    lang = get_user_lang(user_id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    user_data = run_query("SELECT first_name, username, referrals, total_searches, premium_expiry, credits FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    fname, uname, referrals, total_searches, premium_expiry, credits = user_data if user_data else ("Unknown", "None", 0,0,0,0)
    
    current_time = int(datetime.now().timestamp())
    if premium_expiry > current_time:
        expiry_dt = datetime.fromtimestamp(premium_expiry).strftime('%Y-%m-%d %H:%M')
        premium_status = f"👑 Active until {expiry_dt}"
    else:
        premium_status = "🆓 Standard User"

    await update.effective_message.reply_text(
        t["msg_main"],
        reply_markup=get_premium_keyboard(lang),
        parse_mode=ParseMode.MARKDOWN
    )

    safe_name = esc_md(fname)
    safe_user = f"@{esc_md(uname)}" if uname and uname != "None" else "No Username"

    text = (
        f"{t['msg_greet']}\n\n"
        f"{t.get('lbl_live_db', '👤 *LIVE DATABASE IDENTITY*')}\n"
        f"┠ *{t.get('lbl_name', 'Name:')}* {safe_name}\n"
        f"┠ *{t.get('lbl_uname', 'Username:')}* {safe_user}\n"
        f"┖ *{t.get('lbl_uid', 'User ID:')}* `{user_id}`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{t['stat']}\n"
        f"┠ {t['status']} {premium_status}\n"
        f"┠ {t['searches']} {total_searches}\n"
        f"┠ {t['refs']} {referrals}\n"
        f"┖ {t['cred']} {credits} 🪙\n\n"
        f"{t['refer_promo']}`{BOT_LINK}?start={user_id}`\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{t.get('lbl_credits_support', '🛡️ System: Advanced OSINT Grid')}\n"
        f"{t.get('lbl_made_by', '🔐 Connection: Secure')}"
    )
    
    buttons = [
        [InlineKeyboardButton("➕ Add to me your own group", url=f"{BOT_LINK}?startgroup=true")],
        [InlineKeyboardButton("♾️ Unlimited search here free", url="https://t.me/verox_chats")]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != ChatType.PRIVATE:
        lang = get_user_lang(update.effective_user.id)
        await send_group_welcome(update, context, update.effective_chat.id, lang)
        return

    if not await check_ban_and_channels(update, context): return

    lang = get_user_lang(update.effective_user.id)
    
    # 🌟 MATRIX BLOCK START ANIMATION 🌟
    anim_msg = await update.effective_message.reply_text("💠 `[██░░░░░░░░]` 20%", parse_mode=ParseMode.MARKDOWN)
    
    hacker_frames = [
        "⚡ `[█████░░░░░]` 50%",
        "📁 `[████████░░]` 80%",
        "🔐 `[██████████]` 100%"
    ]
    
    for frame in hacker_frames:
        await asyncio.sleep(0.4)
        try: await anim_msg.edit_text(frame, parse_mode=ParseMode.MARKDOWN)
        except Exception: pass
        
    await asyncio.sleep(0.4)
    try: await anim_msg.delete()
    except Exception: pass

    user = update.effective_user
    args = context.args
    referred_by = int(args[0]) if args and args[0].isdigit() else None
    
    first_name = user.first_name or "Unknown"
    username = user.username or "None"
    
    is_new, actual_ref = add_user(user.id, referred_by, first_name, username)
    
    if is_new and actual_ref and actual_ref != user.id:
        ref_lang = get_user_lang(actual_ref)
        ref_t = LANGUAGES.get(ref_lang, LANGUAGES['en'])
        pending_msg = (
            "⏳ *INCOMING REFERRAL PENDING...* ⏳\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "👤 *Someone just started the bot using your invite link!*\n\n"
            "⚠️ *Status:* `Waiting for User Verification...`\n"
            "💡 _They must join all our required private channels before your +1 Premium Credit is securely added to your account._\n\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        try: await context.bot.send_message(chat_id=actual_ref, text=pending_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception: pass
        
    if is_new:
        tot_users = run_query("SELECT COUNT(*) FROM users", fetchone=True)[0]
        safe_username = esc_md('@' + username) if username != "None" else "None"
        admin_msg = (
            "👤 *NEW AGENT DETECTED* 👤\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 *Name:* {esc_md(first_name)}\n"
            f"📛 *Username:* {safe_username}\n"
            f"🆔 *ID:* `{user.id}`\n\n"
            f"📈 *Total Database:* `{tot_users}` Agents\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        for ad in ADMIN_IDS:
            try: await context.bot.send_message(chat_id=ad, text=admin_msg, parse_mode=ParseMode.MARKDOWN)
            except Exception: pass 

    await verify_user_referral(user.id, context)
    await send_main_menu(update, context, user.id)

async def cmd_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != ChatType.PRIVATE:
        lang = get_user_lang(update.effective_user.id)
        await send_group_welcome(update, context, update.effective_chat.id, lang)
        return

    if not await check_ban_and_channels(update, context): return
    
    lang = get_user_lang(update.effective_user.id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])

    keyboard = [
        [KeyboardButton(t["btn_unlim_sub"])],
        [KeyboardButton(t["btn_add_cred"])],
        [KeyboardButton(t["btn_back_main"])]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
    await update.effective_message.reply_text(t["msg_store"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

# ==========================================
# 🎁 REFERRAL COMMAND FUNCTIONS 🎁
# ==========================================
async def enforce_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type != ChatType.PRIVATE:
        lang = get_user_lang(update.effective_user.id)
        await send_group_welcome(update, context, update.effective_chat.id, lang)
        return False
    return True

async def cmd_myreferral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await enforce_private_chat(update, context): return
    if not await check_ban_and_channels(update, context): return
    
    user_id = update.effective_user.id
    user_data = run_query("SELECT referrals, language, credits FROM users WHERE user_id = ?", (user_id,), fetchone=True)
    referrals, lang, credits = user_data if user_data else (0, 'en', 0)
    ref_link = f"{BOT_LINK}?start={user_id}"
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    msg = (
        f"🎁 *{t.get('ref_title', 'REFER & EARN PREMIUM SYSTEM')}* 🎁\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"✨ *{t.get('ref_sub', 'Share your VIP link and earn free Search Credits!')}*\n"
        f"🔗 *{t.get('ref_link_lbl', 'Your Unique Link:')}* `{ref_link}`\n\n"
        f"🥇 `1 Referral` = `1 Credit` 🪙\n\n"
        f"💰 *{t.get('ref_bal', 'Your Balance:')}* `{credits} 🪙` Credits\n"
        f"👥 *{t.get('ref_tot', 'Total Referrals:')}* `{referrals}` Friends\n\n"
        f"💎 *{t.get('ref_redeem', 'REDEEM SUBSCRIPTIONS BELOW')}* 💎\n"
        f"{t.get('ref_use', 'Use your earned credits to activate unlimited searches instantly!')}\n"
    )
    await update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=get_subscription_keyboard(lang))

async def cmd_topreferrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await enforce_private_chat(update, context): return
    if not await check_ban_and_channels(update, context): return
    lang = get_user_lang(update.effective_user.id)
    await send_top_referrals(update.effective_message, get_cancel_keyboard(lang), lang)


def val_phone(p): return bool(re.match(r'^\d{10}$', p))
def val_aadhar(a): return bool(re.match(r'^\d{12}$', a))
def val_imei(i): return bool(re.match(r'^\d{15}$', i))
def val_ifsc(i): return bool(re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', i.upper()))
def val_tg(t): return bool(re.match(r'^\d{5,15}$', t))
def val_username(u): return bool(re.match(r'^[a-zA-Z0-9_]{4,32}$', u))

async def process_api_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE, api_key: str, validator, error_msg: str):
    if not await check_ban_and_channels(update, context): return
    
    lang = get_user_lang(update.effective_user.id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])

    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text(
            "⚠️ *[ SYNTAX ERROR: DM ENVIRONMENT ]* ⚠️\n\nUse the graphical interface modules below in private comms.\n💡 _Slash commands (e.g., `/num1`) only execute in multi-agent group nodes!_",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_premium_keyboard(lang)
        )
        return

    if not context.args:
        await update.message.reply_text(
            f"⚠️ *[ MALFORMED SYNTAX ]*\n\n*Execute:* `/{api_key} <target>`\n\n{error_msg}", 
            parse_mode=ParseMode.MARKDOWN
        )
        return
        
    query = context.args[0]
    if validator and not validator(query):
        await update.message.reply_text(
            error_msg, 
            parse_mode=ParseMode.MARKDOWN
        )
        return
        
    api_map = {
        "num1": NUM1_API, "num2": NUM2_API, "num3": NUM3_API,
        "tg1": TG1_API, "tg2": TG2_API, "tg3": TG3_API,
        "adhr": ADHR_API, "fam": FAM_API,
        "veh": VEHICLE_API, "ifsc": IFSC_API, "imi": IMEI_API
    }
    
    await handle_search(update, context, api_map[api_key], query, lang, api_key)

async def cmd_num1(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "num1", val_phone, "❌ *[ REJECTED ]* Inject 10-digit numerical target.")
async def cmd_num2(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "num2", val_phone, "❌ *[ REJECTED ]* Inject 10-digit numerical target.")
async def cmd_num3(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "num3", val_phone, "❌ *[ REJECTED ]* Inject 10-digit numerical target.")
async def cmd_tg1(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "tg1", val_tg, "❌ *[ REJECTED ]* Telegram ID must be numerical.")
async def cmd_tg2(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "tg2", val_tg, "❌ *[ REJECTED ]* Telegram ID must be numerical.")
async def cmd_tg3(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "tg3", val_username, "❌ *[ REJECTED ]* Invalid comms syntax.")
async def cmd_adhr(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "adhr", val_aadhar, "❌ *[ REJECTED ]* Aadhar stream expects 12 digits.")
async def cmd_fam(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "fam", val_aadhar, "❌ *[ REJECTED ]* Aadhar stream expects 12 digits.")
async def cmd_veh(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "veh", lambda x: bool(x), "❌ *[ REJECTED ]* Target RC required.")
async def cmd_ifsc(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "ifsc", val_ifsc, "❌ *[ REJECTED ]* 11-char IFSC code necessary.")
async def cmd_imi(u: Update, c: ContextTypes.DEFAULT_TYPE): await process_api_cmd(u, c, "imi", val_imei, "❌ *[ REJECTED ]* 15-digit hardware footprint required.")


# ==========================================
# ⌨️ HANDLE KEYBOARD CLICKS & TEXT CMDS ⌨️
# ==========================================

async def handle_keyboard_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_ban_and_channels(update, context): return
    text = update.message.text
    user_id = update.effective_user.id
    global user_search_state
    
    action = REVERSE_BTN_MAP.get(text, text)

    lang = get_user_lang(user_id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])

    if update.effective_chat.type != ChatType.PRIVATE:
        if action.startswith("btn_") or text.startswith("/"):
            await send_group_welcome(update, context, update.effective_chat.id, lang)
        return

    if action.startswith("btn_"):
        if user_id in user_search_state:
            del user_search_state[user_id]
            
    if user_id in user_search_state:
        state = user_search_state[user_id]
        input_text = text.strip()

        if state == "redeem":
            code = input_text
            del user_search_state[user_id]
            
            processing_msg = await update.message.reply_text("⏳ *Validating Gift Code...*", parse_mode=ParseMode.MARKDOWN)
            anim_frames = [
                "💠 `[██░░░░░░░░]` 25%",
                "⚡ `[█████░░░░░]` 50%",
                "📁 `[████████░░]` 75%",
                "🔐 `[██████████]` 100%"
            ]
            for frame in anim_frames:
                await asyncio.sleep(0.4) 
                try: await processing_msg.edit_text(frame, parse_mode=ParseMode.MARKDOWN)
                except Exception: pass
            
            await processing_msg.delete()
            
            if run_query("SELECT 1 FROM claimed_codes WHERE user_id = ? AND code = ?", (user_id, code), fetchone=True):
                await update.message.reply_text("❌ *You have already claimed this code!*", parse_mode=ParseMode.MARKDOWN, reply_markup=get_premium_keyboard(lang))
                return

            code_data = run_query("SELECT points, max_uses, used_count FROM gift_codes WHERE code = ?", (code,), fetchone=True)
            if not code_data: 
                await update.message.reply_text("❌ *Invalid or Expired Code.*", parse_mode=ParseMode.MARKDOWN, reply_markup=get_premium_keyboard(lang))
                return
            
            points, max_uses, used_count = code_data
            if used_count >= max_uses: 
                await update.message.reply_text("❌ *This code has reached its maximum usage limit.*", parse_mode=ParseMode.MARKDOWN, reply_markup=get_premium_keyboard(lang))
                return

            run_query("UPDATE users SET credits = credits + ? WHERE user_id = ?", (points, user_id))
            run_query("UPDATE gift_codes SET used_count = used_count + 1 WHERE code = ?", (code,))
            run_query("INSERT INTO claimed_codes (user_id, code) VALUES (?, ?)", (user_id, code))
            
            success_msg = (
                "🎉 *GIFT CODE REDEEMED SUCCESSFULLY!* 🎉\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎟 *Code:* `{code}`\n"
                f"🎁 *Reward Added:* `+{points} Credits`\n\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"🛡️ *System Secured by Advanced OSINT Grid*"
            )
            await update.message.reply_text(success_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=get_premium_keyboard(lang))
            return

        api_map = {
            "num1": NUM1_API, "num2": NUM2_API, "num3": NUM3_API,
            "tg1": TG1_API, "tg2": TG2_API, "tg3": TG3_API,
            "adhr": ADHR_API, "fam": FAM_API,
            "veh": VEHICLE_API, "ifsc": IFSC_API, "imi": IMEI_API
        }

        if state in api_map:
            is_valid = False
            error_msg = t.get("invalid_input", "❌ *Invalid Input!*")
            
            if state in ["num1", "num2", "num3"]:
                is_valid = val_phone(input_text)
                error_msg = t.get("invalid_num", "❌ *Invalid Number!* Please enter a valid 10-digit mobile number.")
            elif state in ["tg1", "tg2"]:
                is_valid = val_tg(input_text)
                error_msg = t.get("invalid_tg", "❌ *Invalid Telegram ID!* Please enter a valid numerical Telegram ID.")
            elif state == "tg3":
                is_valid = val_username(input_text)
                error_msg = t.get("invalid_tg", "❌ *Invalid Username!* Please enter a valid Telegram username (without @).")
            elif state in ["adhr", "fam"]:
                is_valid = val_aadhar(input_text)
                error_msg = t.get("invalid_input", "❌ *Invalid Aadhar!* Please enter a valid 12-digit Aadhar number.")
            elif state == "veh":
                is_valid = bool(input_text)
                error_msg = t.get("invalid_input", "❌ *Invalid Vehicle Number!*")
            elif state == "ifsc":
                is_valid = val_ifsc(input_text)
                error_msg = t.get("invalid_input", "❌ *Invalid IFSC!* Please enter a valid 11-character Bank IFSC Code.")
            elif state == "imi":
                is_valid = val_imei(input_text)
                error_msg = t.get("invalid_input", "❌ *Invalid IMEI!* Please enter a valid 15-digit IMEI number.")

            if is_valid:
                api = api_map[state]
                del user_search_state[user_id]
                await handle_search(update, context, api, input_text, lang, state)
            else:
                await update.message.reply_text(error_msg + t.get("cancel_prompt", "\nOr select *🔙 Back to Main Menu* to cancel."), parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
            return

    if action == "btn_unlim_search":
        msg = (
            "♾️ *[ ZERO-DAY EXPLOIT ]* ♾️\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Bypass credit deductions entirely.\n\n"
            "Two recognized vectors for 100% FREE unlimited traces:\n"
            "1️⃣ *Unlimited Search Here:* Join our official group node.\n"
            "2️⃣ *Deploy Custom Relay:* Add this bot to your own node (Must be 500+ agents).\n\n"
            "👇 *Execute vector:* "
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Unlimited search here", url="https://t.me/+IzVdb9z7Bvs4YWQ1")],
            [InlineKeyboardButton("➕ Add to me your own group", url=f"{BOT_LINK}?startgroup=true")]
        ])
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
        return

    elif action == "btn_status":
        user_data = run_query("SELECT first_name, username, joined_date, referrals, total_searches, premium_expiry, credits FROM users WHERE user_id = ?", (user_id,), fetchone=True)
        fname, uname, joined, referrals, total_searches, premium_expiry, credits = user_data if user_data else ("Unknown", "None", "Unknown", 0,0,0,0)
        
        current_time = int(datetime.now().timestamp())
        if premium_expiry > current_time:
            expiry_dt = datetime.fromtimestamp(premium_expiry).strftime('%Y-%m-%d %H:%M')
            premium_status = f"{t.get('lbl_vip', '👑 VIP PREMIUM')}\n┖ *Valid Till:* `{expiry_dt}`"
        else:
            premium_status = t.get('lbl_free', "🆓 STANDARD (Free Tier)")
            
        safe_name = esc_md(fname)
        safe_user = f"@{esc_md(uname)}" if uname and uname != "None" else "No Username"
        
        status_msg = (
            f"💠 *{t.get('status_title', 'YOUR PREMIUM STATUS & PROFILE')}* 💠\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 *{t.get('lbl_id_over', 'Identity Overview:')}*\n"
            f"┠ *{t.get('lbl_name', 'Name:')}* {safe_name}\n"
            f"┠ *{t.get('lbl_uname', 'Username:')}* {safe_user}\n"
            f"┖ *{t.get('lbl_uid', 'User ID:')}* `{user_id}`\n\n"
            f"📊 *{t.get('lbl_acc_stat', 'Account Statistics:')}*\n"
            f"┠ *{t.get('lbl_acc', 'Account Type:')}* {premium_status}\n"
            f"┠ *{t.get('lbl_cred', 'Available Credits:')}* `{credits} 🪙`\n"
            f"┠ *{t.get('lbl_tot', 'Total Searches:')}* `{total_searches}`\n"
            f"┠ *{t.get('lbl_ref', 'Total Referrals:')}* `{referrals}`\n"
            f"┖ *{t.get('lbl_join', 'Joined System:')}* `{joined}`\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 _{t.get('msg_upgrade', 'Want unlimited searches? Upgrade tier.')}_"
        )
        await update.message.reply_text(status_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return

    elif action == "btn_num":
        keyboard = [
            [KeyboardButton(t["btn_srv1"]), KeyboardButton(t["btn_srv2"])],
            [KeyboardButton(t["btn_srv3"])],
            [KeyboardButton(t["btn_back_main"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_modules"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
    elif action == "btn_srv1":
        user_search_state[user_id] = "num1"
        await update.message.reply_text(t["prompt_num1"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
    elif action == "btn_srv2":
        user_search_state[user_id] = "num2"
        await update.message.reply_text(t["prompt_num2"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
    elif action == "btn_srv3":
        user_search_state[user_id] = "num3"
        await update.message.reply_text(t["prompt_num3"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return

    elif action == "btn_tg":
        keyboard = [
            [KeyboardButton(t["btn_tg1"]), KeyboardButton(t["btn_tg2"])],
            [KeyboardButton(t["btn_tg3"])],
            [KeyboardButton(t["btn_back_main"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_modules"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
    elif action == "btn_tg1":
        user_search_state[user_id] = "tg1"
        await update.message.reply_text(t["prompt_tg1"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
    elif action == "btn_tg2":
        user_search_state[user_id] = "tg2"
        await update.message.reply_text(t["prompt_tg2"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
    elif action == "btn_tg3":
        user_search_state[user_id] = "tg3"
        await update.message.reply_text(t["prompt_tg3"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return

    elif action in ["btn_adhr", "btn_fam"]:
        keyboard = [
            [KeyboardButton(t["btn_adhr_lookup"]), KeyboardButton(t["btn_fam_search"])],
            [KeyboardButton(t["btn_back_main"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_modules"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
    elif action == "btn_adhr_lookup":
        user_search_state[user_id] = "adhr"
        await update.message.reply_text(t["prompt_adhr"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
    elif action == "btn_fam_search":
        user_search_state[user_id] = "fam"
        await update.message.reply_text(t["prompt_fam"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
        
    elif action == "btn_veh":
        keyboard = [
            [KeyboardButton(t["btn_veh_trace"])], 
            [KeyboardButton(t["btn_back_main"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_modules"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
    elif action == "btn_veh_trace":
        user_search_state[user_id] = "veh"
        await update.message.reply_text(t["prompt_veh"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
        
    elif action == "btn_ifsc":
        keyboard = [
            [KeyboardButton(t["btn_bank_intel"])], 
            [KeyboardButton(t["btn_back_main"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_modules"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
    elif action == "btn_bank_intel":
        user_search_state[user_id] = "ifsc"
        await update.message.reply_text(t["prompt_ifsc"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return
        
    elif action == "btn_imei":
        keyboard = [
            [KeyboardButton(t["btn_dev_trace"])], 
            [KeyboardButton(t["btn_back_main"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_modules"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
    elif action == "btn_dev_trace":
        user_search_state[user_id] = "imi"
        await update.message.reply_text(t["prompt_imei"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return

    elif action == "btn_redeem":
        user_search_state[user_id] = "redeem"
        await update.message.reply_text(t["msg_redeem_prompt"], parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return

    elif action in ["btn_buy", "btn_back_prem"]:
        keyboard = [
            [KeyboardButton(t["btn_unlim_sub"])],
            [KeyboardButton(t["btn_add_cred"])],
            [KeyboardButton(t["btn_back_main"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_store"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
        
    elif action in ["btn_unlim_sub", "btn_sub_3d", "btn_sub_7d", "btn_sub_15d", "btn_sub_30d"]:
        if action in ["btn_sub_3d", "btn_sub_7d", "btn_sub_15d", "btn_sub_30d"]:
            subs_map = {
                "btn_sub_3d": (3, 10),
                "btn_sub_7d": (7, 21),
                "btn_sub_15d": (15, 35),
                "btn_sub_30d": (30, 50)
            }
            days, cost = subs_map[action]
            
            row = run_query("SELECT credits, premium_expiry FROM users WHERE user_id = ?", (user_id,), fetchone=True)
            curr_credits, curr_expiry = row if row else (0, 0)
            
            if curr_credits < cost:
                err = t["err_insuff_cred"].format(cost=cost, days=days, curr_credits=curr_credits)
                await update.message.reply_text(err, parse_mode=ParseMode.MARKDOWN)
            else:
                now = int(datetime.now().timestamp())
                base_time = curr_expiry if curr_expiry > now else now
                new_expiry = base_time + (days * 86400)
                
                run_query("UPDATE users SET credits = credits - ?, premium_expiry = ? WHERE user_id = ?", (cost, new_expiry, user_id))
                
                expiry_dt = datetime.fromtimestamp(new_expiry).strftime('%Y-%m-%d %H:%M:%S')
                success_msg = t["msg_sub_success"].format(days=days, cost=cost, expiry_dt=expiry_dt)
                await update.message.reply_text(success_msg, parse_mode=ParseMode.MARKDOWN)
            return
            
        user_row = run_query("SELECT credits FROM users WHERE user_id = ?", (user_id,), fetchone=True)
        curr_credits = user_row[0] if user_row else 0
        
        subs_text = f"💰 *Your Current Balance:* `{curr_credits} 🪙` Credits\n\n{t['msg_subs']}"
        await update.message.reply_text(subs_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_subscription_keyboard(lang))
        return
        
    elif action == "btn_ref":
        user_data = run_query("SELECT referrals, credits FROM users WHERE user_id = ?", (user_id,), fetchone=True)
        referrals, credits = user_data if user_data else (0, 0)
        ref_link = f"{BOT_LINK}?start={user_id}"
        
        msg = (
            f"🎁 *{t.get('ref_title', 'REFER & EARN PREMIUM SYSTEM')}* 🎁\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"✨ *{t.get('ref_sub', 'Share your VIP link and earn free Search Credits!')}*\n"
            f"🔗 *{t.get('ref_link_lbl', 'Your Unique Link:')}* `{ref_link}`\n\n"
            f"🥇 `1 Referral` = `1 Credit` 🪙\n\n"
            f"💰 *{t.get('ref_bal', 'Your Balance:')}* `{credits} 🪙` Credits\n"
            f"👥 *{t.get('ref_tot', 'Total Referrals:')}* `{referrals}` Friends\n\n"
            f"💎 *{t.get('ref_redeem', 'REDEEM SUBSCRIPTIONS BELOW')}* 💎\n"
            f"{t.get('ref_use', 'Use your earned credits to activate unlimited searches instantly!')}\n"
        )
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=get_subscription_keyboard(lang))
        return

    elif action in ["btn_add_cred", "btn_back_pay"]:
        keyboard = [
            [KeyboardButton(t["btn_pay_upi"]), KeyboardButton(t["btn_pay_trx"])],
            [KeyboardButton(t["btn_back_prem"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t["msg_gateway"], parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
        
    elif action == "btn_pay_upi":
        keyboard = [
            [KeyboardButton(t.get("btn_upi_120")), KeyboardButton(t.get("btn_upi_250"))],
            [KeyboardButton(t.get("btn_upi_550")), KeyboardButton(t.get("btn_upi_1000"))],
            [KeyboardButton(t["btn_back_pay"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t.get("msg_upi_checkout"), parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return
        
    elif action == "btn_pay_trx":
        keyboard = [
            [KeyboardButton(t.get("btn_trx_120")), KeyboardButton(t.get("btn_trx_250"))],
            [KeyboardButton(t.get("btn_trx_550")), KeyboardButton(t.get("btn_trx_1000"))],
            [KeyboardButton(t["btn_back_pay"])]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
        await update.message.reply_text(t.get("msg_trx_checkout"), parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        return

    if action.startswith("btn_upi_") or action.startswith("btn_trx_"):
        global pending_checkouts
        
        parts = action.split("_")
        method = parts[1]
        pkg_id = f"pkg{parts[2]}"
        
        pkg_name = PACKAGES[pkg_id]["name"]
        
        if method == "upi":
            amounts = {"pkg120": "₹49", "pkg250": "₹99", "pkg550": "₹199", "pkg1000": "₹399"}
            amount_str = amounts[pkg_id]
            photo_url = QR_CODE_PHOTO 
            instructions = t.get("msg_upi_inst").format(upi_id=UPI_ID)
        else:
            amounts = {"pkg120": "1.85 TRX", "pkg250": "3.75 TRX", "pkg550": "7.55 TRX", "pkg1000": "15 TRX"}
            amount_str = amounts[pkg_id]
            photo_url = None
            instructions = t.get("msg_trx_inst").format(amount_str=amount_str, binance_id=BINANCE_ID, trx_address=TRX_ADDRESS)

        pending_checkouts[user_id] = {"method": method, "pkg": pkg_id, "amount": amount_str, "name": pkg_name}
        checkout_msg = t["msg_checkout_init"].format(pkg_name=pkg_name, amount_str=amount_str, instructions=instructions)
        
        try:
            if photo_url:
                await context.bot.send_photo(chat_id=user_id, photo=photo_url, caption=checkout_msg, parse_mode=ParseMode.MARKDOWN)
            else:
                await context.bot.send_message(chat_id=user_id, text=checkout_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Failed to send checkout message: {e}.")
            await context.bot.send_message(chat_id=user_id, text=checkout_msg, parse_mode=ParseMode.MARKDOWN)
        return

    elif action == "btn_back_main":
        await update.message.reply_text(
            t["msg_back_main"], 
            parse_mode=ParseMode.MARKDOWN, 
            reply_markup=get_premium_keyboard(lang)
        )
        return

    elif action == "btn_admin":
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ You are not authorized to use this command.")
            return
        await update.message.reply_text(
            t["msg_admin_panel"],
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_admin_keyboard(lang)
        )
        return

    elif action in ["btn_admin_bc", "btn_admin_ap", "btn_admin_rp", "btn_admin_addp", "btn_admin_rmp", "btn_admin_ban", "btn_admin_unban", "btn_admin_mc", "btn_admin_sc", "btn_admin_dc"]:
        if user_id not in ADMIN_IDS: return
        
        admin_cancel_kb = get_admin_cancel_keyboard(lang)
        
        if action == "btn_admin_bc":
            await update.message.reply_text("📢 *BROADCAST SYSTEM*\n━━━━━━━━━━━━━━━━━━━━━\nTo broadcast, **reply to any message/photo/video** with:\n`/broadcast` (To Users)\n`/broadcastgroup` (To Groups)", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_ap":
            await update.message.reply_text("➕ *ADD POINTS*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/addpoint <user_id> <amount>`\nExample: `/addpoint 123456789 50`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_rp":
            await update.message.reply_text("➖ *REMOVE POINTS*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/rmpoint <user_id> <amount>`\nExample: `/rmpoint 123456789 10`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_addp":
            await update.message.reply_text("💎 *ADD PREMIUM*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/addpremium <user_id> <days>`\nExample: `/addpremium 123456789 30`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_rmp":
            await update.message.reply_text("🗑 *REMOVE PREMIUM*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/removepremium <user_id>`\nExample: `/removepremium 123456789`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_ban":
            await update.message.reply_text("⛔️ *BAN USER*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/ban <user_id>`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_unban":
            await update.message.reply_text("🟢 *UNBAN USER*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/unban <user_id>`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_mc":
            await update.message.reply_text("🎁 *MAKE GIFT CODE*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/makecode <code_name> <credits> <max_uses>`\nExample: `/makecode FREE50 50 100`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_sc":
            codes = run_query("SELECT code, points, used_count, max_uses FROM gift_codes", fetchall=True)
            if not codes: 
                await update.message.reply_text("No active gift codes.", reply_markup=admin_cancel_kb)
            else:
                txt = "📋 *DATABASE: ACTIVE GIFT CODES* 📋\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                for code, pts, used, max_use in codes:
                    status = "🟢 Active" if used < max_use else "🔴 Exhausted"
                    txt += f"🎟 *Code:* `{code}`\n┠ 💰 *Value:* `{pts} Credits`\n┠ 👥 *Claims:* `{used}/{max_use}`\n┖ 📊 *Status:* {status}\n\n"
                txt += "━━━━━━━━━━━━━━━━━━━━━\n🗑 _To remove a code, type_ `/delcode <code>`"
                await update.message.reply_text(txt, parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        elif action == "btn_admin_dc":
            await update.message.reply_text("🗑 *DELETE CODE*\n━━━━━━━━━━━━━━━━━━━━━\nUsage: `/delcode <code>`\nExample: `/delcode FREE50`", parse_mode=ParseMode.MARKDOWN, reply_markup=admin_cancel_kb)
        return

    elif action == "btn_back_admin":
        if user_id not in ADMIN_IDS: return
        await update.message.reply_text(
            t["msg_admin_panel"],
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_admin_keyboard(lang)
        )
        return

    elif action == "btn_lead":
        await send_top_referrals(update.effective_message, reply_markup=get_cancel_keyboard(lang), lang=lang)
        return
        
    elif action == "btn_stats":
        await bot_stats(update, context, reply_markup=get_cancel_keyboard(lang))
        return

    elif action == "btn_dev":
        dev_msg = t.get("msg_dev")
        await update.message.reply_text(dev_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=get_cancel_keyboard(lang))
        return

# ==========================================
# 💳 PAYMENT CHECKOUT SYSTEM (PHOTO LOGIC) 💳
# ==========================================

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pending_admin_messages
    if update.effective_chat.type != ChatType.PRIVATE: return
    
    user = update.effective_user
    lang = get_user_lang(user.id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])

    if not update.message.photo: return

    if user.id not in pending_checkouts:
        return await update.message.reply_text(t.get("msg_pls_init_buy"), parse_mode=ParseMode.MARKDOWN)
    
    checkout_info = pending_checkouts[user.id]
    pkg_id = checkout_info["pkg"]
    pkg_name = checkout_info["name"]
    amount_str = checkout_info["amount"]
    method = checkout_info["method"].upper()

    photo = update.message.photo[-1].file_id
    
    await update.message.reply_text(t.get("msg_receipt_received"), parse_mode=ParseMode.MARKDOWN)
    
    caption = (
        "📸 *VIP INTEL: PAYMENT RECEIPT* 📸\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 *User:* {esc_md(user.first_name)}\n"
        f"📛 *Username:* {esc_md('@' + (user.username or 'None'))}\n"
        f"🆔 *ID:* `{user.id}`\n\n"
        f"📦 *Package Selected:* {pkg_name}\n"
        f"💵 *Expected Amount:* {amount_str} ({method})\n\n"
        "⚠️ *Action Required:* Review screenshot below.\n"
        f"Grant VIP access using buttons below:\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )
    
    keyboard = [
        [InlineKeyboardButton(f"✅ Approve {pkg_name}", callback_data=f"approve_{user.id}_{pkg_id}")],
        [InlineKeyboardButton("❌ Reject Payment", callback_data=f"reject_{user.id}")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    
    if user.id not in pending_admin_messages:
        pending_admin_messages[user.id] = []
        
    for admin_id in ADMIN_IDS:
        try:
            msg = await context.bot.send_photo(chat_id=admin_id, photo=photo, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
            pending_admin_messages[user.id].append({'chat_id': admin_id, 'msg_id': msg.message_id, 'type': 'photo', 'content': caption})
        except Exception as e:
            logger.error(f"Failed to forward payment photo to Admin: {e}")

async def admin_approve_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pending_admin_messages, pending_checkouts
    query = update.callback_query
    if update.effective_user.id not in ADMIN_IDS:
        try: await query.answer("❌ You are not authorized to do this!", show_alert=True)
        except Exception: pass
        return
    
    try: await query.answer("Processing update...")
    except Exception: pass
    
    if query.data.startswith("approve_"):
        parts = query.data.split("_")
        target_id = int(parts[1])
        pkg_id = parts[2]
        
        pkg_data = PACKAGES.get(pkg_id)
        if not pkg_data:
            try: await query.answer("Invalid Package ID", show_alert=True)
            except Exception: pass
            return
        
        credits_to_add = pkg_data["credits"]
        pkg_name = pkg_data["name"]

        run_query("UPDATE users SET credits = credits + ? WHERE user_id = ?", (credits_to_add, target_id))
            
        new_caption = (
            "✅ *PAYMENT VERIFIED & GRANTED* ✅\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Target ID: `{target_id}`\n"
            f"Package: *{pkg_name}*\n"
            f"Processed By: Admin `{update.effective_user.id}`\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        
        if target_id in pending_checkouts: del pending_checkouts[target_id]
        
        if target_id in pending_admin_messages:
            for msg_info in pending_admin_messages[target_id]:
                try:
                    if msg_info['type'] == 'text':
                        await context.bot.edit_message_text(text=new_caption, chat_id=msg_info['chat_id'], message_id=msg_info['msg_id'], parse_mode=ParseMode.MARKDOWN, reply_markup=None)
                    elif msg_info['type'] == 'photo':
                        await context.bot.edit_message_caption(caption=new_caption, chat_id=msg_info['chat_id'], message_id=msg_info['msg_id'], parse_mode=ParseMode.MARKDOWN, reply_markup=None)
                except Exception: pass
            del pending_admin_messages[target_id]
        else:
            try:
                if query.message.photo: await query.edit_message_caption(caption=new_caption, parse_mode=ParseMode.MARKDOWN, reply_markup=None)
                else: await query.edit_message_text(text=new_caption, parse_mode=ParseMode.MARKDOWN, reply_markup=None)
            except Exception: pass
        
        target_lang = get_user_lang(target_id)
        t_target = LANGUAGES.get(target_lang, LANGUAGES['en'])
        
        try:
            user_success_msg = (
                f"🎉 *PAYMENT VERIFIED & GRANTED!* 🎉\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📦 `+{credits_to_add}` Premium VIP Credits have been added to your account.\n\n"
                "Thank you for your premium purchase! You can instantly use these credits to purchase an Unlimited VIP Subscription.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"🛡️ *System Secured by Advanced OSINT Grid*"
            )
            await context.bot.send_message(chat_id=target_id, text=user_success_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception: pass

    elif query.data.startswith("reject_"):
        parts = query.data.split("_")
        target_id = int(parts[1])
        
        new_caption = (
            "❌ *PAYMENT REJECTED* ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Target ID: `{target_id}`\n"
            f"Processed By: Admin `{update.effective_user.id}`\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        
        if target_id in pending_checkouts: del pending_checkouts[target_id]

        if target_id in pending_admin_messages:
            for msg_info in pending_admin_messages[target_id]:
                try:
                    if msg_info['type'] == 'text':
                        await context.bot.edit_message_text(text=new_caption, chat_id=msg_info['chat_id'], message_id=msg_info['msg_id'], parse_mode=ParseMode.MARKDOWN, reply_markup=None)
                    elif msg_info['type'] == 'photo':
                        await context.bot.edit_message_caption(caption=new_caption, chat_id=msg_info['chat_id'], message_id=msg_info['msg_id'], parse_mode=ParseMode.MARKDOWN, reply_markup=None)
                except Exception: pass
            del pending_admin_messages[target_id]
        else:
            try:
                if query.message.photo: await query.edit_message_caption(caption=new_caption, parse_mode=ParseMode.MARKDOWN, reply_markup=None)
                else: await query.edit_message_text(text=new_caption, parse_mode=ParseMode.MARKDOWN, reply_markup=None)
            except Exception: pass
        
        user_reject_msg = (
            "⚠️ *PAYMENT REJECTED* ⚠️\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "❌ *Verification Failed:*\n"
            "We were unable to securely verify your recent payment transaction.\n\n"
            "🛑 *Action Taken:*\n"
            "Your VIP credits have not been added to your account.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ *System Secured by Advanced OSINT Grid*"
        )
        try: await context.bot.send_message(chat_id=target_id, text=user_reject_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception: pass

# ==========================================
# 🎁 REFERRAL & REWARD SYSTEM 🎁
# ==========================================

async def send_top_referrals(message, reply_markup=None, lang='en'):
    if not message: return
    top_users = run_query("SELECT user_id, first_name, username, referrals FROM users WHERE referrals > 0 ORDER BY referrals DESC LIMIT 10", fetchall=True)
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    msg = t.get("msg_top_refs", "🏆 *TOP 10 REFERRAL LEADERBOARD* 🏆\n━━━━━━━━━━━━━━━━━━━━━\n\n")
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    if not top_users:
        msg += "No referrals yet! Share your link to be #1! 🚀\n\n"
    else:
        for idx, (uid, fname, uname, refs) in enumerate(top_users):
            name = esc_md(fname if fname else "User")
            uname_text = f"(@{esc_md(uname)})" if uname and uname != "None" else ""
            msg += f"{medals[idx]} *{name}* {uname_text}\n"
            msg += f"    └ 🆔 `{uid}` ➡️ *{refs} Referrals*\n\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━━\n"
    msg += "🎁 *Rank 1st this week to win +50 FREE CREDITS!*\n"
    msg += "⚠️ *Minimum refer 30*"
    
    await message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

# ==========================================
# 🔍 SEARCH ENGINE API & ANIMATIONS 🔍
# ==========================================

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE, api_url: str, query: str, lang: str, search_type: str = ""):
    if not await check_can_search(update, context): return
    user_id = update.effective_user.id
    
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    # 🌟 PREMIUM MATRIX ANIMATION BLOCKS 🌟
    anim_frames = []
    if "num" in search_type:
        anim_frames = [
            "📞 *[ TELECOM PING ]*\n💠 `[██░░░░░░░░]` 20%", 
            "📞 *[ TELECOM PING ]*\n⚡ `[█████░░░░░]` 50%", 
            "📞 *[ TELECOM PING ]*\n📁 `[████████░░]` 80%", 
            "📞 *[ TELECOM PING ]*\n🔐 `[██████████]` 100%"
        ]
    elif "tg" in search_type:
        anim_frames = [
            "✈️ *[ MTPROTO UPLINK ]*\n💠 `[██░░░░░░░░]` 20%", 
            "✈️ *[ MTPROTO UPLINK ]*\n⚡ `[█████░░░░░]` 50%", 
            "✈️ *[ MTPROTO UPLINK ]*\n📁 `[████████░░]` 80%", 
            "✈️ *[ MTPROTO UPLINK ]*\n🔐 `[██████████]` 100%"
        ]
    elif search_type in ["adhr", "fam"]:
        anim_frames = [
            "🏛️ *[ GOV FIREWALL ]*\n💠 `[██░░░░░░░░]` 20%", 
            "🏛️ *[ GOV FIREWALL ]*\n⚡ `[█████░░░░░]` 50%", 
            "🏛️ *[ GOV FIREWALL ]*\n📁 `[████████░░]` 80%", 
            "🏛️ *[ GOV FIREWALL ]*\n🔐 `[██████████]` 100%"
        ]
    elif search_type == "veh":
        anim_frames = [
            "🚗 *[ VAHAN UPLINK ]*\n💠 `[██░░░░░░░░]` 20%", 
            "🚗 *[ VAHAN UPLINK ]*\n⚡ `[█████░░░░░]` 50%", 
            "🚗 *[ VAHAN UPLINK ]*\n📁 `[████████░░]` 80%", 
            "🚗 *[ VAHAN UPLINK ]*\n🔐 `[██████████]` 100%"
        ]
    elif search_type == "ifsc":
        anim_frames = [
            "🏦 *[ BANK PING ]*\n💠 `[██░░░░░░░░]` 20%", 
            "🏦 *[ BANK PING ]*\n⚡ `[█████░░░░░]` 50%", 
            "🏦 *[ BANK PING ]*\n📁 `[████████░░]` 80%", 
            "🏦 *[ BANK PING ]*\n🔐 `[██████████]` 100%"
        ]
    elif search_type == "imi":
        anim_frames = [
            "📱 *[ IMEI BROADCAST ]*\n💠 `[██░░░░░░░░]` 20%", 
            "📱 *[ IMEI BROADCAST ]*\n⚡ `[█████░░░░░]` 50%", 
            "📱 *[ IMEI BROADCAST ]*\n📁 `[████████░░]` 80%", 
            "📱 *[ IMEI BROADCAST ]*\n🔐 `[██████████]` 100%"
        ]
    else:
        anim_frames = [
            "💠 `[██░░░░░░░░]` 20%", 
            "⚡ `[█████░░░░░]` 50%", 
            "📁 `[████████░░]` 80%", 
            "🔐 `[██████████]` 100%"
        ]
    
    processing_msg = await update.effective_message.reply_text(anim_frames[0], parse_mode=ParseMode.MARKDOWN)

    for frame in anim_frames[1:]:
        await asyncio.sleep(0.4) 
        try: await processing_msg.edit_text(frame, parse_mode=ParseMode.MARKDOWN)
        except Exception: pass

    try:
        data = await asyncio.to_thread(fetch_data_sync, api_url + query)
        await processing_msg.delete()
        
        if data and isinstance(data, dict) and len(data) == 0:
            data = None
            
        if data:
            current_time = int(datetime.now().timestamp())
            user_row = run_query("SELECT premium_expiry, credits, total_searches FROM users WHERE user_id = ?", (user_id,), fetchone=True)
            premium_expiry, current_credits, t_searches = user_row
            new_t_searches = t_searches + 1
            has_premium = premium_expiry > current_time
            
            offer_block = ""
            
            user_name = esc_html(update.effective_user.first_name)
            user_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'
            
            tag_footer = (
                f"\n━━━━━━━━━━━━━━━\n"
                f"🌟 <b>Target Locked For:</b> {user_link}\n"
                f"🔒 <i>Protected under Privacy Policy</i>"
            )

            if update.effective_chat.type != ChatType.PRIVATE:
                run_query("UPDATE users SET total_searches = total_searches + 1 WHERE user_id = ?", (user_id,))
                deduction_block = (
                    f"\n➖\n\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📊 <b>{t.get('stat_tot', 'Total Searches Run:')}</b> {new_t_searches}\n"
                    f"💳 <b>{t.get('stat_acc', 'Access Mode:')}</b> ♾️ Public Node (Free)\n"
                    f"➖ <b>{t.get('stat_ded', 'Deducted:')}</b> 0 🪙\n"
                    f"⏳ <i>Auto-Destructing in 30 Seconds...</i>\n"
                    f"{tag_footer}"
                )
            elif has_premium:
                run_query("UPDATE users SET total_searches = total_searches + 1 WHERE user_id = ?", (user_id,))
                deduction_block = (
                    f"\n➖\n\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📊 <b>{t.get('stat_tot', 'Total Searches Run:')}</b> {new_t_searches}\n"
                    f"💳 <b>{t.get('stat_acc', 'Access Mode:')}</b> 👑 Active Subscription\n"
                    f"➖ <b>{t.get('stat_ded', 'Deducted:')}</b> 0 🪙\n"
                    f"{tag_footer}"
                )
            else:
                run_query("UPDATE users SET total_searches = total_searches + 1, credits = credits - 1 WHERE user_id = ?", (user_id,))
                remaining = current_credits - 1
                deduction_block = (
                    f"\n➖\n\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📊 <b>{t.get('stat_tot', 'Total Searches Run:')}</b> {new_t_searches}\n"
                    f"💳 <b>Total Balance:</b> {current_credits} 🪙\n"
                    f"➖ <b>{t.get('stat_ded', 'Deducted:')}</b> 1 🪙\n"
                    f"💰 <b>{t.get('stat_rem', 'Remaining Credits:')}</b> {remaining} 🪙\n"
                    f"{tag_footer}"
                )
            
            result_text = offer_block + format_premium_result(data, t) + deduction_block
            
            final_markup = get_premium_keyboard(lang) if update.effective_chat.type == ChatType.PRIVATE else ReplyKeyboardRemove()
            result_msg = await update.effective_message.reply_text(result_text, parse_mode=ParseMode.HTML, reply_markup=final_markup, disable_web_page_preview=True)
            
            # Auto-Delete logic for GROUPS only (30 Seconds)
            if update.effective_chat.type != ChatType.PRIVATE:
                asyncio.create_task(clear_message_later(result_msg, 30))
                if update.effective_message: asyncio.create_task(delete_user_message_later(update.effective_message, 30))

        else:
            err_text = t.get("search_fail", "📭 *DATA NOT AVAILABLE*")
            final_markup = get_premium_keyboard(lang) if update.effective_chat.type == ChatType.PRIVATE else ReplyKeyboardRemove()
            err_msg = await update.effective_message.reply_text(err_text, parse_mode=ParseMode.MARKDOWN, reply_markup=final_markup)
            
            if update.effective_chat.type != ChatType.PRIVATE:
                asyncio.create_task(clear_message_later(err_msg, 30))
                if update.effective_message: asyncio.create_task(delete_user_message_later(update.effective_message, 30))
            
    except Exception as e:
        logger.error(f"Search API Error: {e}")
        try: await processing_msg.delete()
        except Exception: pass
        
        err_text = t.get("search_fail", "📭 *DATA NOT AVAILABLE*")
        final_markup = get_premium_keyboard(lang) if update.effective_chat.type == ChatType.PRIVATE else ReplyKeyboardRemove()
        err_msg = await update.effective_message.reply_text(err_text, parse_mode=ParseMode.MARKDOWN, reply_markup=final_markup)
        
        if update.effective_chat.type != ChatType.PRIVATE:
            asyncio.create_task(clear_message_later(err_msg, 30))
            if update.effective_message: asyncio.create_task(delete_user_message_later(update.effective_message, 30))

# ==========================================
# 🛑 COMMAND HELPERS (ADMIN & BOT COMMANDS) 🛑
# ==========================================

async def bot_stats(update: Update, context: ContextTypes.DEFAULT_TYPE, reply_markup=None):
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = int(datetime.now().timestamp())
    lang = get_user_lang(update.effective_user.id)
    t = LANGUAGES.get(lang, LANGUAGES['en'])
    
    total_users = run_query("SELECT COUNT(*) FROM users", fetchone=True)[0]
    total_groups = run_query("SELECT COUNT(*) FROM groups", fetchone=True)[0]
    total_searches = run_query("SELECT SUM(total_searches) FROM users", fetchone=True)[0] or 0
    total_premium = run_query("SELECT COUNT(*) FROM users WHERE premium_expiry > ?", (current_time,), fetchone=True)[0]
    total_banned = run_query("SELECT COUNT(*) FROM users WHERE is_banned = 1", fetchone=True)[0]
    joined_today = run_query("SELECT COUNT(*) FROM users WHERE joined_date = ?", (today,), fetchone=True)[0]
    status_emoji = "🔴 STOPPED (Maintenance)" if is_bot_maintenance() else "🟢 ACTIVE (Live)"
    
    text = (
        f"{t.get('msg_bot_stats', '📊 *Advanced Bot Statistics*\n━━━━━━━━━━━━━━━━━━━━━\n')}"
        f"🤖 *Bot Status:* {status_emoji}\n\n"
        f"👥 *Total Users:* `{total_users}`\n"
        f"🏢 *Total Groups:* `{total_groups}`\n"
        f"🆕 *Joined Today:* `{joined_today}`\n"
        f"🔍 *Total API Searches:* `{total_searches}`\n\n"
        f"👑 *Active Subscribers:* `{total_premium}`\n"
        f"⛔️ *Total Banned Users:* `{total_banned}`\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )
    await update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

async def toggle_maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    command = update.effective_message.text.split()[0].lower()
    
    if command == "/botstop":
        set_bot_maintenance(True)
        await update.effective_message.reply_text("🔴 *Bot is now STOPPED (Maintenance Mode).* Regular users cannot use it.", parse_mode=ParseMode.MARKDOWN)
    elif command == "/botlive":
        set_bot_maintenance(False)
        await update.effective_message.reply_text("🟢 *Bot is now LIVE (Active).* Everyone can use it again.", parse_mode=ParseMode.MARKDOWN)

async def modify_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    command = update.effective_message.text.split()[0].lower()
    
    if len(context.args) != 2 or not context.args[0].isdigit() or not context.args[1].isdigit():
        return await update.effective_message.reply_text(f"Usage: `{command} <user_id> <credits>`", parse_mode=ParseMode.MARKDOWN)
    
    target_id, points = int(context.args[0]), int(context.args[1])
    
    if run_query("SELECT 1 FROM users WHERE user_id = ?", (target_id,), fetchone=True):
        if command == "/addpoint":
            run_query("UPDATE users SET credits = credits + ? WHERE user_id = ?", (points, target_id))
            admin_msg = (
                "💎 *PREMIUM CREDITS ADDED* 💎\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"✅ Successfully added `+{points}` Credits to User ID: `{target_id}`.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━"
            )
            await update.effective_message.reply_text(admin_msg, parse_mode=ParseMode.MARKDOWN)
            
            target_lang = get_user_lang(target_id)
            t_target = LANGUAGES.get(target_lang, LANGUAGES['en'])
            
            user_msg = (
                "🎉 *CREDITS ADDED!* 🎉\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎁 Good news! An admin has manually added `+{points}` Search Credits to your account.\n\n"
                "Enjoy your premium searches!\n\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"🛡️ *System Secured by Advanced OSINT Grid*"
            )
            try:
                await context.bot.send_message(chat_id=target_id, text=user_msg, parse_mode=ParseMode.MARKDOWN)
            except Exception: pass

        elif command == "/rmpoint":
            run_query("UPDATE users SET credits = MAX(0, credits - ?) WHERE user_id = ?", (points, target_id))
            admin_msg = (
                "⚠️ *PREMIUM CREDITS REMOVED* ⚠️\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"✅ Successfully removed `-{points}` Credits from User ID: `{target_id}`.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━"
            )
            await update.effective_message.reply_text(admin_msg, parse_mode=ParseMode.MARKDOWN)
            user_msg = (
                "⚠️ *CREDITS DEDUCTED* ⚠️\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📉 Note: An admin has removed `-{points}` Search Credits from your account.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"🛡️ *System Secured by Advanced OSINT Grid*"
            )
            try:
                await context.bot.send_message(chat_id=target_id, text=user_msg, parse_mode=ParseMode.MARKDOWN)
            except Exception: pass
    else:
        await update.effective_message.reply_text("❌ *User not found in the database.*", parse_mode=ParseMode.MARKDOWN)

async def admin_gift_codes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    command = update.effective_message.text.split()[0].lower()
    
    if command == "/makecode":
        if len(context.args) != 3: return await update.effective_message.reply_text("Usage: `/makecode <code_name> <credits> <max_uses>`", parse_mode=ParseMode.MARKDOWN)
        code, pts, uses = context.args[0], context.args[1], context.args[2]
        if not pts.isdigit() or not uses.isdigit(): return await update.effective_message.reply_text("Credits and max uses must be numbers.")
        
        try:
            run_query("INSERT INTO gift_codes (code, points, max_uses) VALUES (?, ?, ?)", (code, int(pts), int(uses)))
            msg = (
                "💎 *NEW PREMIUM GIFT CODE* 💎\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎟 *Access Code:* `{code}`\n"
                f"💰 *Credit Value:* `+{pts} Credits`\n"
                f"👥 *Usage Limit:* `{uses} Claims`\n"
                f"🟢 *Status:* `Active & Ready`\n\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"📣 *Share this code with users to claim:* Tap the 🎟️ Redeem Code button."
            )
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Live Recheck Claims", callback_data=f"recheck_code_{code}")]])
            await update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
        except sqlite3.IntegrityError:
            await update.effective_message.reply_text("❌ *Code already exists.*", parse_mode=ParseMode.MARKDOWN)
            
    elif command == "/seecodes":
        codes = run_query("SELECT code, points, used_count, max_uses FROM gift_codes", fetchall=True)
        if not codes: return await update.effective_message.reply_text("No active gift codes.")
        text = "📋 *DATABASE: ACTIVE GIFT CODE S* 📋\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        for code, pts, used, max_use in codes:
            status = "🟢 Active" if used < max_use else "🔴 Exhausted"
            text += f"🎟 *Code:* `{code}`\n┠ 💰 *Value:* `{pts} Credits`\n┠ 👥 *Claims:* `{used}/{max_use}`\n┖ 📊 *Status:* {status}\n\n"
        text += "━━━━━━━━━━━━━━━━━━━━━\n🗑 _To remove a code, type_ `/delcode <code>`"
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        
    elif command == "/delcode":
        if len(context.args) != 1: return await update.effective_message.reply_text("Usage: `/delcode <code>`", parse_mode=ParseMode.MARKDOWN)
        code = context.args[0]
        run_query("DELETE FROM gift_codes WHERE code = ?", (code,))
        run_query("DELETE FROM claimed_codes WHERE code = ?", (code,))
        await update.effective_message.reply_text(f"🗑 *DELETED CODE:* `{code}`\nIt has been effectively removed from the master database.", parse_mode=ParseMode.MARKDOWN)

async def admin_recheck_code_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if update.effective_user.id not in ADMIN_IDS:
        try: await query.answer("❌ You are not authorized!", show_alert=True)
        except Exception: pass
        return
        
    if query.data.startswith("recheck_code_"):
        code = query.data.replace("recheck_code_", "")
        code_data = run_query("SELECT points, max_uses, used_count FROM gift_codes WHERE code = ?", (code,), fetchone=True)
        
        if code_data:
            pts, max_uses, used_count = code_data
            msg = (
                "💎 *GIFT CODE STATUS LIVE* 💎\n"
                "━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎟 *Access Code:* `{code}`\n"
                f"💰 *Credit Value:* `+{pts} Credits`\n"
                f"👥 *Live Claims:* `{used_count}/{max_uses} Users`\n\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"📣 *Share this code with users to claim:* Tap the 🎟️ Redeem Code button."
            )
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Live Recheck Claims", callback_data=f"recheck_code_{code}")]])
            try:
                await query.edit_message_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
                await query.answer("Stats live updated!", show_alert=False)
            except telegram.error.BadRequest:
                try: await query.answer("Stats are already up to date!", show_alert=False)
                except Exception: pass
        else:
            try: await query.edit_message_text("❌ *This code no longer exists or was deleted.*", parse_mode=ParseMode.MARKDOWN)
            except Exception: pass

async def broadcast_task(context, msg_to_broadcast, target_ids, status_msg):
    success, failed = 0, 0
    for target in target_ids:
        try:
            await context.bot.copy_message(chat_id=target, from_chat_id=msg_to_broadcast.chat_id, message_id=msg_to_broadcast.message_id)
            success += 1
            await asyncio.sleep(0.05) 
        except Exception: failed += 1
    await status_msg.edit_text(f"✅ *Broadcast Complete!*\n\nSuccessful: {success}\nFailed: {failed}", parse_mode=ParseMode.MARKDOWN)

async def handle_broadcasts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    command = update.effective_message.text.split()[0].lower()
    
    if not update.effective_message.reply_to_message:
        return await update.effective_message.reply_text("⚠️ Please reply to the media/text you want to broadcast.")
        
    msg_to_broadcast = update.effective_message.reply_to_message
    
    if command == "/broadcast":
        users = [row[0] for row in run_query("SELECT user_id FROM users", fetchall=True)]
        if not users:
            return await update.effective_message.reply_text("⚠️ No users found in the database.")
        status_msg = await update.effective_message.reply_text(f"🚀 Broadcasting instantly to {len(users)} users...")
        asyncio.create_task(broadcast_task(context, msg_to_broadcast, users, status_msg))
        
    elif command == "/broadcastgroup":
        groups = [row[0] for row in run_query("SELECT chat_id FROM groups", fetchall=True)]
        if not groups:
            return await update.effective_message.reply_text("⚠️ No groups found in the database.")
        status_msg = await update.effective_message.reply_text(f"📢 Broadcasting instantly to {len(groups)} groups...")
        asyncio.create_task(broadcast_task(context, msg_to_broadcast, groups, status_msg))

async def ban_user(u, c): 
    if u.effective_user.id in ADMIN_IDS and len(c.args)==1: run_query("UPDATE users SET is_banned=1 WHERE user_id=?", (c.args[0],)); await u.effective_message.reply_text("✅ Banned")
async def unban_user(u, c): 
    if u.effective_user.id in ADMIN_IDS and len(c.args)==1: run_query("UPDATE users SET is_banned=0 WHERE user_id=?", (c.args[0],)); await u.effective_message.reply_text("✅ Unbanned")

async def add_premium(u, c): 
    if u.effective_user.id in ADMIN_IDS and len(c.args) == 2:
        target = int(c.args[0])
        days = int(c.args[1])
        now = int(datetime.now().timestamp())
        
        row = run_query("SELECT premium_expiry FROM users WHERE user_id=?", (target,), fetchone=True)
        if not row: return await u.effective_message.reply_text("❌ User not found.")
        
        curr_expiry = row[0]
        base_time = curr_expiry if curr_expiry > now else now
        new_expiry = base_time + (days * 86400)
        
        run_query("UPDATE users SET premium_expiry=? WHERE user_id=?", (new_expiry, target))
        dt = datetime.fromtimestamp(new_expiry).strftime('%Y-%m-%d %H:%M')
        await u.effective_message.reply_text(f"✅ Added {days} days of Premium. New expiry: {dt}")
        
async def remove_premium(u, c): 
    if u.effective_user.id in ADMIN_IDS and len(c.args)==1: 
        run_query("UPDATE users SET premium_expiry=0 WHERE user_id=?", (c.args[0],))
        await u.effective_message.reply_text("✅ Premium Removed")

async def auto_approve_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try: await context.bot.approve_chat_join_request(chat_id=update.chat_join_request.chat.id, user_id=update.chat_join_request.from_user.id)
    except Exception as e: logger.error(f"Auto-approve fail: {e}")

# ==========================================
# 🚀 MAIN APPLICATION LOOP 🚀
# ==========================================

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).post_init(setup_commands).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_new_chat_members))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, on_left_chat_member))

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", cmd_buy)) 
    
    app.add_handler(CallbackQueryHandler(check_join_callback, pattern="^check_join$"))
    app.add_handler(CallbackQueryHandler(admin_approve_callbacks, pattern="^(approve_|reject_)"))
    app.add_handler(CallbackQueryHandler(admin_recheck_code_callback, pattern="^recheck_code_"))
    
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(ChatJoinRequestHandler(auto_approve_join))

    app.add_handler(CommandHandler("myreferral", cmd_myreferral))
    app.add_handler(CommandHandler("topreferrals", cmd_topreferrals))

    app.add_handler(CommandHandler("num1", cmd_num1))
    app.add_handler(CommandHandler("num2", cmd_num2))
    app.add_handler(CommandHandler("num3", cmd_num3))
    app.add_handler(CommandHandler("tg1", cmd_tg1))
    app.add_handler(CommandHandler("tg2", cmd_tg2))
    app.add_handler(CommandHandler("tg3", cmd_tg3))
    app.add_handler(CommandHandler("adhr", cmd_adhr))
    app.add_handler(CommandHandler("fam", cmd_fam))
    app.add_handler(CommandHandler("veh", cmd_veh))
    app.add_handler(CommandHandler("ifsc", cmd_ifsc))
    app.add_handler(CommandHandler("imi", cmd_imi))

    app.add_handler(CommandHandler("makecode", admin_gift_codes))
    app.add_handler(CommandHandler("seecodes", admin_gift_codes))
    app.add_handler(CommandHandler("delcode", admin_gift_codes))
    app.add_handler(CommandHandler("addpoint", modify_points))
    app.add_handler(CommandHandler("rmpoint", modify_points))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("addpremium", add_premium))
    app.add_handler(CommandHandler("removepremium", remove_premium))
    app.add_handler(CommandHandler("stats", bot_stats))
    app.add_handler(CommandHandler("botstop", toggle_maintenance))
    app.add_handler(CommandHandler("botlive", toggle_maintenance))
    app.add_handler(CommandHandler("broadcast", handle_broadcasts))
    app.add_handler(CommandHandler("broadcastgroup", handle_broadcasts)) 

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard_clicks))

    print("==================================================")
    print("✅ Advanced Master Bot Running on Pydroid3!")
    print("✅ MATRIX BLOCKS: Beautiful text-based `[████░░░]` loading blocks implemented.")
    print("✅ SMART DELETION: Group searches beautifully auto-replace with '🗑️ Message Deleted' after 30s.")
    print("✅ BEAUTIFUL TAGGING: User who searched is tagged flawlessly in result footer.")
    print("✅ EXPLICIT TAGS REMOVED: Telegram Privacy & Support explicitly removed.")
    print("✅ COMPLIANCE: Admin info blocked & user overrides successfully applied.")
    print("✅ ZERO-DAY DIRECT LINKS ADDED")
    print("==================================================")
    
    app.run_polling()

if __name__ == "__main__":
    main()
