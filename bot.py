from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest
import os
import asyncio
import sys

# ============================================================
#   TOKEN BOT — dibaca dari Environment Variable "BOT_TOKEN"
#   Di Railway: Settings > Variables > tambahkan BOT_TOKEN
#   Untuk testing lokal, bisa juga pakai file .env (lihat README)
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN belum diset! "
        "Set environment variable BOT_TOKEN dengan token dari @BotFather."
    )

# ============================================================
#   Group ID orderan & Channel username
# ============================================================
GROUP_ID   = -1003796810319
CHANNEL_ID = "@jastipperi"   # channel yang wajib di-subscribe

# ============================================================
#   FOTO
# ============================================================
PHOTOS = {
    "regulation": "foto_regulation.jpg",
    "catalogue":  "foto_catalogue.jpg",
    "pricelist":  "foto_pricelist.jpg",
}

# ============================================================
#   EMOJI PREMIUM ID
# ============================================================
E1 = "<tg-emoji emoji-id=\"5417952350272771717\">🌸</tg-emoji>"
E2 = "<tg-emoji emoji-id=\"6116165572762799489\">✨</tg-emoji>"
E3 = "<tg-emoji emoji-id=\"5350560151575211828\">🩷</tg-emoji>"
E4 = "<tg-emoji emoji-id=\"6145486305175275098\">💫</tg-emoji>"

# emoji catalogue baru
EC1 = "<tg-emoji emoji-id=\"5418031983261401952\">🐕‍🦺</tg-emoji>"
EC2 = "<tg-emoji emoji-id=\"5418038885273851139\">🦋</tg-emoji>"
EC3 = "<tg-emoji emoji-id=\"5416103448456219676\">🍨</tg-emoji>"
EC4 = "<tg-emoji emoji-id=\"5415970858520824028\">🍓</tg-emoji>"
EC5 = "<tg-emoji emoji-id=\"5415965197753928294\">🌺</tg-emoji>"

# emoji pesan konfirmasi order
EPAWS = "<tg-emoji emoji-id=\"6316314695183637770\">🐾</tg-emoji>"
EHEART = "<tg-emoji emoji-id=\"5350560151575211828\">🩷</tg-emoji>"

# ============================================================
#   TEKS
# ============================================================

WELCOME_TEXT = (
    f"Haii {{name}}! 👋🏻\n\n"
    f"Welcome to <b>Jastip Peri</b> {E3}✨\n\n"
    f"Yuk pilih menu di bawah ini dan klik <b>Format</b> "
    f"jika kamu ingin order yang kami sediakan! 🛍️\n\n"
    f"Percill siap melayani mu dengan ramah {E3}🌸💕"
)

NOT_SUBSCRIBED_TEXT = (
    f"Haii! 👋🏻\n\n"
    f"Sebelum menggunakan bot ini, kamu wajib subscribe channel kami dulu ya Kak! {E3}\n\n"
    f"📢 Channel: @jastipperi\n\n"
    f"Klik tombol <b>Subscribe</b> di bawah, lalu klik <b>✅ Sudah Subscribe</b> "
    f"untuk melanjutkan! 🌸"
)

REGULATION_TEXT = (
    f"( .. <b>REGULATION</b>    {E1} {E2}\n"
    f"    a regulation on the use of sharp chemical weapons to be safe and avoid the various dangers that lurk around.\n\n"
    f"        <b>E.X.P</b>   ── .✦ tight player control  {E4}\n\n"
    f"                                 │   <b>RULES</b>     ── .✦        <b>EFFECTIVE</b>                    │   <b>VERIFIED</b>  ❦ <b>MANDATORY</b>             \n"
    f"read the applicable regulations\n"
    f"prohibited from breaking the rules ༄.°\n\n"
    f"           {E4} .ᐟ . <b>DIRECTIONS</b> ❩  {E1}   <b>ONE</b>   {E2}\n"
    f"     sebelum mengisi format jastip pastikan sudah subs @jastipperi terlebih dahulu, agar tidak ketinggian informasi penting. lalu send format ke @jastipperibot\n\n"
    f"      {E4} .ᐟ. <b>DIRECTIONS</b> ❩  {E1}   <b>TWO</b>   {E2}\n"
    f"      send format = fix order. uang yg sudah di terima oleh admin tidak dapat di reffund dalam hal apapun, kecuali ada alasan yg jelas &amp; kesalahan dari pihak admin.\n\n"
    f"      {E4} .ᐟ . <b>DIRECTIONS</b> ❩  {E1}   <b>THREE</b>   {E2}\n"
    f"      order sesuatu di pastikan format sudah benar, sebelum di send ke bot. dan wajib barang mu milik sendiri! bukan barang hasil curian, scam, yg intinya punya daftar hitam.\n\n"
    f"      {E4} .ᐟ. <b>DIRECTIONS</b> ❩  {E1}   <b>FOUR</b>   {E2}\n"
    f"        transaksi pembayaran di lakukan di awal, agar tidak kejadian hal yg tidak di ingin kan &amp; pembayaran hanya di lakukan di @jastipperibot. kecuali, dari pihak bot mengarah kan untuk hit admin jastip peri.  dan pasti kan bukpem TIDAK DI EDIT &amp; DI CROP!\n\n"
    f"       {E4} .ᐟ . <b>DIRECTIONS</b> ❩  {E1}   <b>FIVE</b>   {E2}\n"
    f"        jika orderan/pelayanan belum di handle oleh admin kurang dari 1 - 5 jam, di mohonkan untuk resend kembali ke bot. dan di wajibkan untuk crosscheck list admin, agar tidak terjadi clonning nya penipuan.\n\n"
    f"       {E4} .ᐟ . <b>DIRECTIONS</b> ❩  {E1}  <b>SIX</b>   {E2}\n"
    f"     di larang untuk memplagiat jastip kami, jika ketahuan akan di beri sanksi sebesar 300.000! dan di berikan peringatan.\n\n"
    f"          {E4}   II.  settings  ───  obey the rules          \n"
    f"(  ••  )  <b>ATTACHMENT .. DOC</b> {E3}"
)

CATALOGUE_TEXT = (
    f"<b>E.X.P</b>  ───────── 200\" .. ★ ˎˊ˗\n\n"
    f"♡  CIRCUMFERENCE     𓍯  ITEM'S {EC1}\n"
    f"            the contents of everything that is sold\n"
    f"            enemy shooting equipment danger\n"
    f"    ❦  (  .. EQUIPMENT  \"  OBJECT\n"
    f"             THE CATALOGUE'S\n"
    f"           ■ supplement provider  .^᪲᪲᪲\n"
    f"         {EC2}  X.P.A    • necessities\n\n"
    f"{EC3} ── .✦  ..  <b>JASTIP NEED'S</b>\n\n"
    f"        ᝰ.ᐟ  ──  JASTIP GIFT UPGRADE\n"
    f"        ᝰ.ᐟ  ──  JASTIP NOKPREM\n"
    f"        ᝰ.ᐟ  ──  JASTIP ACC INC\n"
    f"                   GIFT LIMITED\n"
    f"        ᝰ.ᐟ  ──  JASTIP CHANEL STORE\n"
    f"        ᝰ.ᐟ  ──  JASTIP CHANEL PRIBADI\n"
    f"        ᝰ.ᐟ  ──  JASTIP GC RESSELLER\n"
    f"        ᝰ.ᐟ  ──  JASTIP ACC GAME\n"
    f"        ᝰ.ᐟ  ──  JASTIP ACC SOSMED\n\n"
    f"{EC4} 𓂃 ִֶָ𐀔  ..  <b>OTHER'S NEED'S</b>  ❦\n\n"
    f"        ༄.°   ──  Jaseb offer gift\n"
    f"        ༄.°   ──  Convert gift to idr\n"
    f"        ༄.°   ──  Gadai gift upgrade\n"
    f"        ༄.°   ──  Jasa jubell gift\n"
    f"                    market place\n"
    f"        ༄.°   ──  Jasa cek range\n"
    f"        ༄.°   ──  Telegram premium\n"
    f"        ༄.°   ──  Telegram stars\n\n"
    f"             STUFFING  ⋆. 𐙚 ˚ : order weapon equipment items to the chairman. send your weapon order attachment to the admin ↺ {EC5}\n\n"
)

PRICELIST_TEXT = (
    f". ᕱ⑅︎ᕱ   ⌕  <b>PRICELIST</b>  ── .✦\n"
    f"  [ &amp;. ]  . .  STEEPED IN DOOM   \" REVOLT? \"\n\n"
    f"  𐙚  ── .✦  <b>JASTIP NEEDS</b>\n"
    f"  <i>Writing names in blinding blood,\n"
    f"  reborn in lightnings storm.</i>\n\n"
    f"   𐙚 .. II：  Jastip gift upgrade\n"
    f"             ꩜.ᐟ . 4.000\n"
    f"   𐙚 .. II：  Jastip nokprem\n"
    f"             ꩜.ᐟ . 5.000\n"
    f"   𐙚 .. II：  Jastip acc inc gift limited\n"
    f"             ꩜.ᐟ . 5.000\n"
    f"   𐙚 .. II：  Jastip channel store\n"
    f"        ꩜.ᐟ . 100s - 500s = 2.000\n"
    f"        ꩜.ᐟ . 600s - 1.1ks = 4.000\n"
    f"        ꩜.ᐟ . 1.2ks - 1.7ks = 6.000\n"
    f"   𐙚 .. II：  Jastip channel pribadi\n"
    f"        ꩜.ᐟ . 100s - 500s = 2.000\n"
    f"        ꩜.ᐟ . 600s - 1.1ks = 4.000\n"
    f"        ꩜.ᐟ . 1.2ks - 1.7ks = 5.000\n"
    f"   𐙚 .. II：  Jastip gc reseller\n"
    f"        ꩜.ᐟ . 100m - 500m = 2.000\n"
    f"        ꩜.ᐟ . 600m - 1.1km = 4.000\n"
    f"        ꩜.ᐟ . 1.2km - 1.7km = 5.000\n"
    f"   𐙚 .. II：  Jastip acc game\n"
    f"             ꩜.ᐟ . 4.000\n"
    f"   𐙚 .. II：  Jastip acc sosmed\n"
    f"             ꩜.ᐟ . 4.000\n\n"
    f"  𐙚  ── .✦  <b>OTHER'S NEEDS</b>\n"
    f"  <i>Writing names in blinding blood,\n"
    f"  reborn in lightnings storm.</i>\n\n"
    f"    𐙚 .. II：  Jaseb offer gift\n"
    f"             ꩜.ᐟ . 2.000\n"
    f"    𐙚 .. II：  Convert gift to idr\n"
    f"             ꩜.ᐟ . harga qs/floor - 5%\n"
    f"    𐙚 .. II：  Gadai gift\n"
    f"             ꩜.ᐟ . hold\n"
    f"    𐙚 .. II：  Jasa jubell gift market place\n"
    f"             ꩜.ᐟ . login : 10k\n"
    f"             ꩜.ᐟ . nolog : 15k\n"
    f"    𐙚 .. II：  Jasa cek range gift\n"
    f"             ꩜.ᐟ . 3.000\n"
    f"    𐙚 .. II：  Telegram premium\n"
    f"             ꩜.ᐟ . <a href=\"https://t.me/archive_jastipperi/5\">[ here ]</a>\n"
    f"    𐙚 .. II：  Telegram stars\n"
    f"             ꩜.ᐟ . <a href=\"https://t.me/archive_jastipperi/5\">[ here ]</a>\n\n"
    f"►   ATTENTION ❗️ CAREFULLY   ★ ˎˊ˗ {E3}"
)

OWNER_TEXT = (
    f"👑 <b>Owner Jastip Peri</b>\n\n"
    f"Halo! Saya Percill, owner dari Jastip Peri {E3}\n\n"
    f"📱 Telegram: @vperi\n"
    f"<i>Jangan ragu untuk hubungi saya ya!</i> 🌸💕"
)

OUR_STORE_TEXT = (
    f"🏪 <b>Our Store</b>\n\n"
    f"Selamat datang di toko kami! {E3}\n\n"
    f"📱 Store: @jastipperi\n\n"
    f"<i>Kami siap melayani dengan sepenuh hati!</i> ✨🌸"
)

CV_GADAI_TEXT = (
    f"⌕  ── <b>PENGERTIAN JASTIP</b>\n"
    f"Jastip adalah = jasa titip barang yang ingin di jual kan melalui pihak ketiga dan lalu di promosikan oleh admin hingga barang nya sold!\n"
    f"<i>note : admin tidak mempunyai pertanggung jawaban transaksi seller ⇆ buyyer atas penitipan barang! jadi, agar transaksi lebih aman dan menghindarkan kasus clonning &amp; penipuan maka di saran kan memakai rekber @rekberfamous.</i>\n\n"
    f"⌕  ── <b>PENGERTIAN CV GIFT UPG TO IDR</b>\n"
    f"Cv gift upg to idr = convert gift upgrade yg akan di jadikan idr.\n"
    f"transaksi seller &amp; buyyer, yg memakai sistem quick sale/floor market place dan real time ton @ratetonidr lalu akan di kenakan biaya -5% dari jumlah tersebut.\n\n"
    f"<b>contoh :</b>\n"
    f"gift vice ice cream harga qs/floor di 3 ton lalu akan di kalikan dengan rate real time ton, semisalnya rate ton 23k.\n"
    f"jadi, 23k × 3 = 69k\n"
    f"     69k - 5% = 65,55k\n"
    f"and, totall bersih semua yg akan di terima buyyer adalah 65.55k!\n"
    f"<i>simpel nya = harga qs/floor gift × real time ton, lalu - 5%</i>\n"
    f"<i>note : buyyer wajib tfo gift duluan, dan sebelum tfo di pastikan harus sudah fix &amp; cocok dengan jumlah bersih yg telah di total kan.</i>\n\n"
    f"⌕  ── <b>PENGERTIAN GADAI GIFT UPGRADE</b>\n"
    f"gadai gift upg = jasa penitipan gift kepada admin, dan akan mendapatkan uang pinjaman dengan cepat. lalu, akan di kembalikan 1 minggu kemudian. dengan jumlah yang di berikan + fee pegadaian\n\n"
    f"<b>sistem :</b> buyyer tfo gift kepada admin, lalu admin akan memberikan kan uang yang sudah di total kan bersih kepada buyyer. setelah 1 week, buyyer mengembalikan uang gadai + fee sebesar 12k kepada admin, untuk biaya tfo.\n\n"
    f"<b>cara penghitungan :</b> harga qs/floor gift × harga real time ton. lalu, di - 30%!\n"
    f"<i>note : jika lebih dari 1 minggu akan di kenakan biaya 5,5% perday. dengan syarat, sudah di bicarakan dari awall sebelum masa sewa berlangsung. jika, baru di bicarakan di tengah/akhir masa penyewaan, maka jika lewat 1 minggu, gift tetap di nyatakan hangus!</i>\n\n"
    f"untuk jastipan akan di promosikan ke beberapa base, yaitu =\n"
    f"@wantgift, @giftwtb, @giftfesss, @lpm_gift, @lpmgifts, @lapakgiftcs, @LpmGGift, @promosigift, @lapakgiftcs @lpm_upsubsuupfoll\n\n"
    f"by : @jastipperi {E3}"
)

FORMAT_PAGE1_TEXT = f"✨ <b>Format Layanan</b> — Halaman 1\n\nPilih layanan yang kamu inginkan yuk Kak! {E3}"
FORMAT_PAGE2_TEXT = f"✨ <b>Format Layanan</b> — Halaman 2\n\nMasih banyak lagi nih Kak! {E3}"

FORMAT_TEMPLATES = {
    "jastip_gift": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP GIFT UPGRADE\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ jenis gift ⌲ \n"
        f" ૮◟ link gift  ⌲\n"
        f" ૮◟ fix price &amp; nett price ⌲ \n"
        f" ૮◟ detail ⌲ ( nomin/min, avneg, avail nyicil, keep wdp ) \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jastip_nokprem": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP NOKPREM\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ username nokprem ⌲ \n"
        f" ૮◟ include  ⌲\n"
        f" ૮◟ price ⌲ \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jastip_acc_inc": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP ACC INC GIFT LIMITED\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ username akun ⌲ \n"
        f" ૮◟ include &amp; detail  ⌲\n"
        f" ૮◟ price ⌲ \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jastip_ch_store": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP CHANNEL STORE\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ username channel ⌲ \n"
        f" ૮◟ jumlah subs ⌲\n"
        f" ૮◟ berapa % buyyer/ma/reg  ⌲\n"
        f" ૮◟ bekas channel apa ⌲  \n"
        f" ૮◟ include &amp; detail  ⌲\n"
        f" ૮◟ price ⌲ \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jastip_ch_pribadi": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP CHANNEL PRIBADI\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ username channel ⌲ \n"
        f" ૮◟ jumlah subs ⌲\n"
        f" ૮◟ berapa % ma/reg  ⌲\n"
        f" ૮◟ include &amp; detail  ⌲\n"
        f" ૮◟ price ⌲ \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jastip_gc_ress": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP GC RESSELLER\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ link gc resseller ⌲ \n"
        f" ૮◟ jumlah member ⌲\n"
        f" ૮◟ berapa % buyyer/ma/reg  ⌲\n"
        f" ૮◟ bekas ress apa ⌲  \n"
        f" ૮◟ include &amp; detail  ⌲\n"
        f" ૮◟ price ⌲ \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jastip_acc_game": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP ACC GAME\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ jenis acc game ⌲  \n"
        f" ૮◟ include &amp; detail  ⌲\n"
        f" ૮◟ price ⌲ \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jastip_acc_sosmed": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASTIP ACC SOSMED\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ jenis acc sosmed ⌲  \n"
        f" ૮◟ detail  ⌲\n"
        f" ૮◟ price ⌲ \n"
        f" ૮◟ purchase contact  ⌲ @\n\n"
        f"KETERANGAN : #READY\n\n"
        f"Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous atau jika belum terlalu paham rekber bisa di tanyakan terlebih dahulu ke @jastipperibot ꩜.ᐟ</code> {E3}"
    ),
    "jaseb_gift": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASEB OFFER GIFT UPGRADE\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ link gift ⌲ \n"
        f" ૮◟ link offeran  ⌲\n"
        f" ૮◟ end ⌲  \n"
        f" ૮◟ purchase contact  ⌲ @</code>\n\n"
        f"<i>Note: pihak kami hanya sebatas perantara, have no responsibility, dengan barang yg di jualkan. jadi, agar terhindar dari kasus clonning &amp; penipuan wajib menggunakan rekber @rekberfamous ꩜.ᐟ</i>\n\n"
        f"CARD  ─────  66\" ..  ꩜.ᐟ 形状\n"
        f"<i>Eldritch symposium sways,\nRiven with argentine veins.</i> {E3}"
    ),
    "gadai_gift": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── GADAI GIFT UPGRADE\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ jenis gift ⌲  \n"
        f" ૮◟ link ⌲\n"
        f" ૮◟ contact  ⌲ @</code>\n\n"
        f"CARD  ─────  66\" ..  ꩜.ᐟ 形状\n"
        f"<i>Eldritch symposium sways,\nRiven with argentine veins.</i> {E3}"
    ),
    "jasa_jubel": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASA JUBEL GIFT MARKET PLACE\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ jenis gift ⌲  \n"
        f" ૮◟ link ⌲\n"
        f" ૮◟ login/nolog ⌲\n"
        f" ૮◟ contact  ⌲ @</code>\n\n"
        f"CARD  ─────  66\" ..  ꩜.ᐟ 形状\n"
        f"<i>Eldritch symposium sways,\nRiven with argentine veins.</i> {E3}"
    ),
    "cek_range": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── JASA CEK RANGE GIFT\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ jenis gift ⌲  \n"
        f" ૮◟ link ⌲\n"
        f" ૮◟ contact  ⌲ @</code>\n\n"
        f"CARD  ─────  66\" ..  ꩜.ᐟ 形状\n"
        f"<i>Eldritch symposium sways,\nRiven with argentine veins.</i> {E3}"
    ),
    "teleprem_login": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── TELEPREM VIA LOGIN\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ nama &amp; username  ⌲ \n"
        f" ૮◟ usn akun yg di prem  ⌲\n"
        f" ૮◟ durasi ⌲ \n"
        f" ૮◟ nomor tele ⌲ \n"
        f" ૮◟ pw 2 step verif  ⌲ (kalo ada) \n"
        f" ૮◟ payment ⌲</code>\n\n"
        f"CARD  ─────  66\" ..  ꩜.ᐟ 形状\n"
        f"<i>Eldritch symposium sways,\nRiven with argentine veins.</i> {E3}"
    ),
    "teleprem_gift": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── TELEPREM VIA GIFT\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ nama &amp; username  ⌲ \n"
        f" ૮◟ usn akun yg di prem  ⌲\n"
        f" ૮◟ durasi ⌲ \n"
        f" ૮◟ nomor tele ⌲ \n"
        f" ૮◟ pw 2 step verif  ⌲ (kalo ada) \n"
        f" ૮◟ payment ⌲</code>\n\n"
        f"CARD  ─────  66\" ..  ꩜.ᐟ 形状\n"
        f"<i>Eldritch symposium sways,\nRiven with argentine veins.</i> {E3}"
    ),
    "topup_stars": (
        f"<code>. ᕱ⑅︎ᕱ   ⌕  ── TOPUP STARS/GIFT\n"
        f"𐙚. AUTOCOPY ALERT\n\n"
        f"Hello, I'm  want to fill my needs forum with the following!\n"
        f" ૮◟ nama &amp; username  ⌲ \n"
        f" ૮◟ jumlah order  ⌲\n"
        f" ૮◟ gift/topup  ⌲ \n"
        f" ૮◟ emoji + note ( jika gift ) ⌲\n"
        f" ૮◟ payment ⌲</code>\n\n"
        f"CARD  ─────  66\" ..  ꩜.ᐟ 形状\n"
        f"<i>Eldritch symposium sways,\nRiven with argentine veins.</i> {E3}"
    ),
}

waiting_order = {}
order_message_map = {}
photo_message_map = {}  # simpan (chat_id, foto_msg_id, teks_msg_id) per user


# ============================================================
#   HELPER — cek subscription
# ============================================================

async def is_subscribed(context, user_id: int) -> bool:
    """Return True jika user sudah subscribe CHANNEL_ID."""
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status not in ("left", "kicked")
    except Exception:
        return True


async def send_photo_menu(context, chat_id, photo_key, caption, keyboard, user_id=None):
    markup = InlineKeyboardMarkup(keyboard)
    photo_file = PHOTOS.get(photo_key, "")
    if photo_file and os.path.exists(photo_file):
        with open(photo_file, "rb") as f:
            photo_msg = await context.bot.send_photo(
                chat_id=chat_id,
                photo=f,
            )
        text_msg = await context.bot.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode="HTML",
            reply_markup=markup,
        )
        if user_id:
            photo_message_map[user_id] = (chat_id, photo_msg.message_id, text_msg.message_id)
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode="HTML",
            reply_markup=markup,
        )


# ============================================================
#   KEYBOARD
# ============================================================

def subscribe_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 subscribe @jastipperi", url="https://t.me/jastipperi")],
        [InlineKeyboardButton("✅ sudah subscribe", callback_data="check_subscribe")],
    ])

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 regulation", callback_data="regulation"),
            InlineKeyboardButton("🛍️ catalogue", callback_data="catalogue"),
        ],
        [
            InlineKeyboardButton("📝 format", callback_data="format_page_1"),
            InlineKeyboardButton("💰 pricelist", callback_data="pricelist"),
        ],
        [
            InlineKeyboardButton("👑 owner", callback_data="owner"),
            InlineKeyboardButton("🏪 our store", callback_data="our_store"),
        ],
        [
            InlineKeyboardButton("💡 pengertian cv gift & gadai gift", callback_data="cv_gadai"),
        ],
    ])

def format_page_1_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎁 jastip gift", callback_data="fmt_jastip_gift"),
            InlineKeyboardButton("🌟 jastip nokprem", callback_data="fmt_jastip_nokprem"),
        ],
        [
            InlineKeyboardButton("💎 jastip acc inc gift", callback_data="fmt_jastip_acc_inc"),
            InlineKeyboardButton("🏬 jastip ch store", callback_data="fmt_jastip_ch_store"),
        ],
        [
            InlineKeyboardButton("👤 jastip ch pribadi", callback_data="fmt_jastip_ch_pribadi"),
            InlineKeyboardButton("🎲 jastip gc ress", callback_data="fmt_jastip_gc_ress"),
        ],
        [
            InlineKeyboardButton("🕹️ jastip acc game", callback_data="fmt_jastip_acc_game"),
            InlineKeyboardButton("📱 jastip acc sosmed", callback_data="fmt_jastip_acc_sosmed"),
        ],
        [
            InlineKeyboardButton("➡️ next »", callback_data="format_page_2"),
            InlineKeyboardButton("🏠 menu utama", callback_data="main_menu"),
        ],
    ])

def format_page_2_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎀 jaseb gift upgrade", callback_data="fmt_jaseb_gift"),
            InlineKeyboardButton("🔒 gadai gift", callback_data="fmt_gadai_gift"),
        ],
        [
            InlineKeyboardButton("🛒 jasa jubel marketplace", callback_data="fmt_jasa_jubel"),
            InlineKeyboardButton("🔍 cek range gift", callback_data="fmt_cek_range"),
        ],
        [
            InlineKeyboardButton("🔐 teleprem via login", callback_data="fmt_teleprem_login"),
            InlineKeyboardButton("🎁 teleprem via gift", callback_data="fmt_teleprem_gift"),
        ],
        [
            InlineKeyboardButton("⭐ topup stars/gift", callback_data="fmt_topup_stars"),
        ],
        [
            InlineKeyboardButton("« back", callback_data="format_page_1"),
            InlineKeyboardButton("🏠 menu utama", callback_data="main_menu"),
        ],
    ])

def back_keyboard(back_to="main_menu"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 kembali", callback_data=back_to)],
        [InlineKeyboardButton("🏠 menu utama", callback_data="main_menu")],
    ])


# ============================================================
#   HANDLER
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "Kak"

    if not await is_subscribed(context, user.id):
        await update.message.reply_text(
            NOT_SUBSCRIBED_TEXT,
            parse_mode="HTML",
            reply_markup=subscribe_keyboard(),
        )
        return

    await update.message.reply_text(
        WELCOME_TEXT.format(name=name),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    name = user.first_name or "Kak"
    chat_id = query.message.chat_id

    if data == "check_subscribe":
        if await is_subscribed(context, user.id):
            await query.edit_message_text(
                WELCOME_TEXT.format(name=name),
                parse_mode="HTML",
                reply_markup=main_menu_keyboard(),
            )
        else:
            await query.answer(
                "❌ Kamu belum subscribe @jastipperi ya Kak!\nSubscribe dulu lalu coba lagi 🌸",
                show_alert=True,
            )
        return

    if data in ("regulation", "catalogue", "pricelist"):
        await query.message.delete()
        texts = {
            "regulation": REGULATION_TEXT,
            "catalogue":  CATALOGUE_TEXT,
            "pricelist":  PRICELIST_TEXT,
        }
        await send_photo_menu(context, chat_id, data, texts[data], back_keyboard().inline_keyboard, user_id=user.id)

    elif data == "main_menu":
        if user.id in photo_message_map:
            try:
                saved_chat_id, foto_id, teks_id = photo_message_map.pop(user.id)
                await context.bot.delete_message(chat_id=saved_chat_id, message_id=foto_id)
                await context.bot.delete_message(chat_id=saved_chat_id, message_id=teks_id)
            except Exception:
                pass
            await context.bot.send_message(
                chat_id=chat_id,
                text=WELCOME_TEXT.format(name=name),
                parse_mode="HTML",
                reply_markup=main_menu_keyboard(),
            )
        else:
            await query.edit_message_text(
                WELCOME_TEXT.format(name=name),
                parse_mode="HTML",
                reply_markup=main_menu_keyboard(),
            )
    elif data == "owner":
        await query.edit_message_text(OWNER_TEXT, parse_mode="HTML", reply_markup=back_keyboard())
    elif data == "our_store":
        await query.edit_message_text(OUR_STORE_TEXT, parse_mode="HTML", reply_markup=back_keyboard())
    elif data == "cv_gadai":
        await query.edit_message_text(CV_GADAI_TEXT, parse_mode="HTML", reply_markup=back_keyboard())
    elif data == "format_page_1":
        await query.edit_message_text(FORMAT_PAGE1_TEXT, parse_mode="HTML", reply_markup=format_page_1_keyboard())
    elif data == "format_page_2":
        await query.edit_message_text(FORMAT_PAGE2_TEXT, parse_mode="HTML", reply_markup=format_page_2_keyboard())

    elif data.startswith("fmt_"):
        key = data[4:]
        template = FORMAT_TEMPLATES.get(key)
        if template:
            waiting_order[user.id] = True
            page_1_keys = {
                "jastip_gift", "jastip_nokprem", "jastip_acc_inc", "jastip_ch_store",
                "jastip_ch_pribadi", "jastip_gc_ress", "jastip_acc_game", "jastip_acc_sosmed"
            }
            back_to = "format_page_1" if key in page_1_keys else "format_page_2"
            if key in page_1_keys:
                text = template + f"\n\n<i>Salin form di atas, isi lengkap, lalu kirim ke sini ya Kak!</i> {E3}"
            else:
                text = template
            await query.edit_message_text(text, parse_mode="HTML", reply_markup=back_keyboard(back_to))


async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Diteruskan ke grup setiap user kirim pesan teks di private chat.
    - Kalau user sebelumnya klik tombol format (waiting_order == True),
      pesan dilabeli sebagai ORDER MASUK.
    - Kalau user kirim pesan bebas tanpa pilih format dulu (misal nanya2),
      pesan dilabeli sebagai PESAN MASUK / PERTANYAAN.
    """
    user = update.effective_user
    message = update.message

    is_order = waiting_order.pop(user.id, False)

    username = f"@{user.username}" if user.username else "(tidak ada username)"
    nama = user.first_name or "?"

    if is_order:
        label = "🛍️ <b>ORDER MASUK!</b>"
    else:
        label = "💬 <b>PESAN / PERTANYAAN MASUK!</b>"

    header = (
        f"{label}\n"
        f"👤 Nama: {nama}\n"
        f"📱 Username: {username}\n"
        f"🆔 User ID: <code>{user.id}</code>\n"
        f"─────────────────\n\n"
    )

    try:
        sent = await context.bot.send_message(
            chat_id=GROUP_ID,
            text=header + message.text,
            parse_mode="HTML",
        )
        order_message_map[sent.message_id] = user.id
    except Exception as e:
        print(f"❌ Gagal kirim ke grup: {e}")
        await update.message.reply_text(
            "⚠️ Maaf Kak, terjadi kendala saat meneruskan pesan kamu ke admin. "
            "Coba kirim ulang sebentar lagi ya 🙏"
        )
        return

    if is_order:
        reply_text = (
            f". ᕱ⑅︎ᕱ ㅤpaws paws! {EPAWS}\n"
            f"꒰⑅ˊ‌ ˙‌ ˋ‌⑅꒱\n"
            f"hii, order format has been received, kak!\n"
            f"silahkan tunggu sampaii admin merespon yaa! {EHEART}\n\n"
            f"jika dalam 30 menit admin tidak merespon, silahkan untuk kirim ulang format nya di bot ini. thank you-!!\n\n"
            f"ketik /start untuk kembali ke menu utama."
        )
    else:
        reply_text = (
            f". ᕱ⑅︎ᕱ ㅤpaws paws! {EPAWS}\n"
            f"꒰⑅ˊ‌ ˙‌ ˋ‌⑅꒱\n"
            f"hii kak, pesan kamu sudah diterima! {EHEART}\n"
            f"silahkan tunggu ya, admin akan segera membalas pesan mu.\n\n"
            f"jika dalam 30 menit admin tidak merespon, silahkan kirim ulang pesan nya. thank you-!!\n\n"
            f"ketik /start untuk kembali ke menu utama."
        )

    await update.message.reply_text(reply_text, parse_mode="HTML")


async def receive_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.chat_id != GROUP_ID:
        return
    if not message.reply_to_message:
        return

    replied_msg_id = message.reply_to_message.message_id
    target_user_id = order_message_map.get(replied_msg_id)

    if not target_user_id:
        return

    await context.bot.send_message(
        chat_id=target_user_id,
        text=(
            f"💌 <b>Balasan dari Admin Jastip Peri</b>\n"
            f"─────────────────\n\n"
            f"{message.text}\n\n"
            f"─────────────────\n"
            f"<i>Jika ada pertanyaan, jangan ragu tanya lagi ya Kak!</i> {E3}"
        ),
        parse_mode="HTML",
    )

    await message.reply_text("✅ Pesan sudah terkirim ke user!")


# ============================================================
#   ERROR HANDLER
# ============================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    from telegram.error import BadRequest, NetworkError, TimedOut
    err = context.error
    if isinstance(err, BadRequest):
        if "not modified" in str(err).lower():
            return
        print(f"⚠️ BadRequest: {err}")
    elif isinstance(err, (NetworkError, TimedOut)):
        pass
    else:
        print(f"❌ Error: {err}")


# ============================================================
#   MAIN
# ============================================================

def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
        receive_order
    ))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Chat(GROUP_ID) & filters.REPLY,
        receive_admin_reply
    ))
    app.add_error_handler(error_handler)

    print("🩷 Bot Jastip Peri sedang berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
