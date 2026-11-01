# Static site generator (stdlib only). Edit text here, run `python3 _tools/build.py`, deploy the folder.
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(__file__))
from ill import ILL, phone
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("LAMDA_SITE", "https://zefitkolish1-oss.github.io/lamda")   # public URL, no trailing slash
BASE = os.environ.get("LAMDA_BASE", "/lamda")   # URL path prefix ("" for a root domain)
import re
def based(h): return re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{BASE}/', h)
SCRIPT = open(os.path.join(ROOT, "_tools/script_path.txt")).read().strip()
V = "2.2.1"

def t(ar, en): return f'<span lang="ar">{ar}</span><span lang="en">{en}</span>'
def blk(tag, ar, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} lang="ar">{ar}</{tag}><{tag}{c} lang="en">{en}</{tag}>'

ICON_DL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0l-5-5m5 5l5-5M5 20h14" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SOC = {
 "instagram": '<svg viewBox="0 0 24 24"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zm5 3.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9zm0 2a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM17.6 5.2a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4z"/></svg>',
 "tiktok": '<svg viewBox="0 0 24 24"><path d="M14 2h3a5 5 0 0 0 5 5v3a8 8 0 0 1-5-1.7V15a7 7 0 1 1-7-7h1v3.2A3.8 3.8 0 1 0 14 15z"/></svg>',
 "x": '<svg viewBox="0 0 24 24"><path d="M3 3h5l4.5 6.2L18 3h3l-7.2 8.2L21.5 21h-5l-5-6.8L5.5 21h-3l7.7-8.8z"/></svg>',
 "telegram": '<svg viewBox="0 0 24 24"><path d="M21.5 3.5L2.8 10.7c-1 .4-1 1.6.1 1.9l4.7 1.5 1.8 5.6c.3.8 1.3 1 1.9.4l2.6-2.5 4.9 3.6c.7.5 1.7.1 1.9-.7l3-15.4c.2-1-.8-1.9-1.7-1.6zM9.7 14.2l-.5 3.5-1.2-4 9.6-6.4z"/></svg>',
}

def head(title_ar, title_en, desc_ar, desc_en, path, extra=""):
    url = SITE + path
    return f'''<!doctype html>
<html lang="ar" dir="rtl" data-title-ar="{title_ar}" data-title-en="{title_en}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title_ar}</title>
<meta name="description" content="{desc_ar} — {desc_en}">
<meta name="theme-color" content="#7C3AED">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{url}"><link rel="alternate" hreflang="en" href="{url}?lang=en">
<meta property="og:type" content="website"><meta property="og:site_name" content="Lamda · لمدا">
<meta property="og:title" content="{title_ar} · {title_en}"><meta property="og:description" content="{desc_ar}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="ar_IQ"><meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@lamda.ai">
<meta name="twitter:title" content="{title_ar} · {title_en}"><meta name="twitter:description" content="{desc_en}"><meta name="twitter:image" content="{SITE}/assets/img/og.png">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/assets/css/style.css">
<script>document.documentElement.classList.add("js")</script>
{extra}</head>
<body>
<a class="skip" href="#main">{t("تخطى للمحتوى","Skip to content")}</a>
<header class="top"><div class="wrap nav">
  <a class="brand" href="/"><img src="/assets/img/orb.svg" alt="" width="38" height="38"><span>Lamda · لمدا</span></a>
  <nav aria-label="Main">
    <a href="/#features">{t("المميزات","Features")}</a><a href="/#how">{t("شلون تشتغل","How it works")}</a>
    <a href="/#pricing">{t("الأسعار","Pricing")}</a><a href="/install.html">{t("التنصيب","Install")}</a><a href="/#faq">{t("أسئلة","FAQ")}</a>
  </nav>
  <button class="lang" type="button">English</button>
</div></header>
<main id="main">'''

def foot():
    soc = "".join(f'<a data-social="{k}" href="#" rel="noopener" aria-label="{k} @lamda.ai">{v}</a>' for k, v in SOC.items())
    return f'''</main>
<footer><div class="wrap">
 <div class="foot">
  <div><a class="brand" href="/"><img src="/assets/img/orb.svg" alt="" width="38" height="38"><span>Lamda · لمدا</span></a>
   {blk("p","مساعدتك العراقية اللي تشتغل بدون نت.","Your Iraqi assistant that works offline.","fine")}
   <div class="social" aria-label="Social">{soc}</div><p class="fine">@lamda.ai</p></div>
  <div><h2 class="fh">{t("التطبيق","App")}</h2><a href="/install.html">{t("التنزيل والتنصيب","Download & install")}</a><a href="/pay.html">{t("الدفع","Payments")}</a><a href="/#faq">{t("أسئلة شائعة","FAQ")}</a></div>
  <div><h2 class="fh">{t("تواصل","Contact")}</h2><a data-mail href="#">hello@lamda.ai</a><a href="/privacy.html">{t("سياسة الخصوصية","Privacy policy")}</a><a href="/terms.html">{t("شروط الاستخدام","Terms of use")}</a></div>
 </div>
 <p class="fine">© <span id="year">2026</span> Lamda. {t("صُنع بالعراق بمحبة.","Made with love in Iraq.")}</p>
</div></footer>
<script src="/assets/js/config.js"></script><script src="/assets/js/main.js" defer></script>
</body></html>
'''

def dl_btn(big=True):
    return f'<a class="btn btn-primary{" btn-big" if big else ""}" data-apk href="#" rel="noopener">{ICON_DL}{t("نزّل التطبيق","Download for Android")}</a>'

# ───────────── index ─────────────
features = [
 ("iraqi", "تحچي عراقي", "Talks Iraqi", "احچي وياها بلهجتك مثل ما تحچي ويه صديقك. تفهم العراقي والإنگليزي وتجاوبك بنفس الروح.", "Chat in your own dialect. Lamda understands Iraqi Arabic and English and answers the same way."),
 ("apps", "تفتح وتسوي بالتطبيقات", "Opens and uses apps", "گلها «افتح يوتيوب»، «ارجع»، «اكتب…» أو «سكرول» وهي تسويها بدالك.", "Say “open YouTube”, “go back”, “type…” or “scroll” and Lamda does it for you."),
 ("offline", "تشتغل بدون نت", "Works offline", "العقل كله على تلفونك. بلا إنترنت تكدر تحچي وياها وتنفذلك أوامر.", "The brain runs on your phone. No internet needed to chat or run commands."),
 ("voice", "صوت طبيعي عربي وإنگليزي", "Natural Arabic + English voice", "أصوات طبيعية تشتغل على الجهاز، تكدر تختار الصوت والسرعة والنبرة.", "Natural on-device voices; choose the voice, speed and pitch."),
 ("bubble", "فقاعة عائمة", "Floating bubble", "لمدا تبقى فوق أي تطبيق كفقاعة صغيرة. دوس عليها أو صيح «لمدا».", "Lamda floats above any app as a small bubble. Tap it or just say “Lamda”."),
 ("privacy", "خصوصيتك أول شي", "Privacy first", "السوالف والذاكرة مشفرة على تلفونك. الأوامر ما تطلع من جهازك.", "Chats and memory are encrypted on your phone. Commands never leave your device."),
]
fc = "".join(f'<article class="card reveal">{ILL[k]}<h3>{t(a,e)}</h3>{blk("p",da,de)}</article>' for k, a, e, da, de in features)
steps = [("dl","نزّل التطبيق","Download","دوس على زر التنزيل ونصّب الملف. الدليل يشرحلك كل خطوة حسب نوع تلفونك.","Tap Download and install the file. The guide walks you through it for your phone brand."),
         ("perm","فعّل الأذونات","Enable permissions","لمدا تفهمك شنو كل إذن وليش تحتاجه، وتوديك للمكان الصح بدوسة وحدة.","Lamda explains each permission and takes you to the right switch in one tap."),
         ("talk","احچي وياها","Talk","صيح «لمدا» أو دوس الفقاعة، واطلب اللي تريده.","Say “Lamda” or tap the bubble and ask for anything.")]
sc = "".join(f'<article class="card step reveal">{ILL[k]}<h3>{t(a,e)}</h3>{blk("p",da,de)}</article>' for k, a, e, da, de in steps)
shots = [("30_splash_name_complete","شاشة البداية","Splash"),("26_chat_light_face","المحادثة","Chat"),("14_onboarding_accessibility","تفعيل الأذونات خطوة بخطوة","Guided permissions"),
         ("11_bubble_orb","الفقاعة فوق أي تطبيق","Bubble over any app"),("12_bubble_panel","لوحة الفقاعة","Bubble panel"),("15_settings_light_1","الإعدادات","Settings"),("15_settings_light_3","الصوت والموديلات","Voices & models")]
car = "".join(f'<figure class="slide"><div class="phone"><img src="/assets/img/shots/{f}.webp" width="540" height="1170" loading="lazy" decoding="async" alt="{e} — {a}"></div><figcaption>{t(a,e)}</figcaption></figure>' for f, a, e in shots)

def plan(name_ar, name_en, coins_ar, coins_en, m, y, per_ar_m, per_en_m, feats, pop=False, free=False):
    li = "".join(f"<li>{t(a,e)}</li>" for a, e in feats)
    if free:
        price = f'<p class="price">0 <small>{t("د.ع","IQD")}</small></p>'
    else:
        price = (f'<p class="price"><span data-m="{m}" data-y="{y}">{m}</span> <small>{t("د.ع","IQD")}</small> '
                 f'<small data-per="m">{t("/ شهر","/ month")}</small><small data-per="y" hidden>{t("/ سنة","/ year")}</small></p>')
    badge = f'<span class="badge">{t("الأكثر طلباً","Most popular")}</span>' if pop else ""
    return f'''<article class="card plan reveal{' pop' if pop else ''}">{badge}<h3>{t(name_ar,name_en)}</h3>{price}
<p>{t(coins_ar,coins_en)}</p><ul>{li}</ul><a class="btn {'btn-primary' if pop else 'btn-ghost'}" href="{'/install.html' if free else '/pay.html'}">{t("ابدأ مجاناً","Start free") if free else t("اشترك","Subscribe")}</a></article>'''
plans = (plan("مجاني","Free","500 كوين للبداية","500 coins to start","","","","",[("المساعد على الجهاز بلا نت","On-device assistant, offline"),("أوامر التطبيقات والفقاعة","App commands & bubble"),("أصوات طبيعية","Natural voices")],free=True)
 + plan("بلس","Plus","5,000 كوين كل شهر","5,000 coins every month","3,000","30,000","","",[("كل شي بالمجاني","Everything in Free"),("ميزات السحابة الذكية","Smart cloud features"),("أولوية بالتحديثات","Priority updates")],pop=True)
 + plan("برو","Pro","كوينات بلا حدود","Unlimited coins","7,000","65,000","","",[("كل شي ببلس","Everything in Plus"),("استخدام بلا حدود","Unlimited usage"),("دعم مباشر","Direct support")]))
faq = [
 ("هل التطبيق آمن؟","Is it safe?","إي. التطبيق موقّع وكل نسخة إلها بصمة SHA-256 تكدر تتأكد منها. الأذونات تنشرح قبل لا تفعلها، والأوامر والذاكرة تبقى على تلفونك ومشفرة. ما نطلب كلمات سر ولا نقرأها.","Yes. Every build is signed and has a published SHA-256 fingerprint you can check. Each permission is explained before you enable it, and commands and memory stay encrypted on your phone. Lamda never asks for or reads passwords."),
 ("ليش مو موجود على Google Play؟","Why isn't it on Google Play?","لمدا تستخدم خدمة إمكانية الوصول حتى تدوس وتكتب بدالك، وهاي الميزة Google تراجعها بشكل خاص. لحد ما نخلص المراجعة، نوزّع التطبيق مباشرة من موقعنا.","Lamda uses the Accessibility service to tap and type for you, which Google reviews separately. Until that review is done we distribute the app directly from this site."),
 ("شلون أنصّبه؟","How do I install it?",'نزّل الملف، اسمح بـ«تثبيت التطبيقات غير المعروفة» للمتصفح أو مدير الملفات، وبعدين افتح الملف. <a href="/install.html">الدليل خطوة بخطوة</a> لشاومي وسامسونگ وغيرها.','Download the file, allow “Install unknown apps” for your browser or Files app, then open it. See the <a href="/install.html">step-by-step guide</a> for Xiaomi, Samsung and others.'),
 ("شلون أدفع؟","How do I pay?",'الدفع راح يكون عن طريق زين كاش وفاست پاي وكي كارد. هسه الخدمة <strong>قريباً</strong>، وكل الميزات الأساسية مجانية. <a href="/pay.html">تفاصيل الدفع</a>.','Payments will be via ZainCash, FastPay and Qi Card. They are <strong>coming soon</strong>; the core features are free. See <a href="/pay.html">payments</a>.'),
]
fq = "".join(f'<details class="reveal"><summary>{t(qa,qe)}</summary>{blk("p",aa,ae)}</details>' for qa, qe, aa, ae in faq)
ld = json.dumps({"@context":"https://schema.org","@type":"SoftwareApplication","name":"Lamda","operatingSystem":"Android 8+","applicationCategory":"UtilitiesApplication","softwareVersion":V,"inLanguage":["ar","en"],"offers":{"@type":"Offer","price":"0","priceCurrency":"IQD"}}, ensure_ascii=False)
index = head("لمدا — مساعدتك العراقية اللي تشتغل بدون نت", "Lamda — your Iraqi assistant that works offline",
             "مساعدة ذكية تحچي عراقي، تفتح التطبيقات وتشتغل بدون إنترنت", "An Iraqi-Arabic voice assistant for Android that opens apps and works offline", "/",
             f'<script type="application/ld+json">{ld}</script>\n') + f'''
<section class="hero"><div class="wrap">
 <div class="stage" role="img" aria-label="{'Lamda character writing its name'}">
  <svg class="script" viewBox="0 0 1000 430" aria-hidden="true">
   <defs><linearGradient id="inkg" x1="0" x2="1000" y1="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#A78BFA"/><stop offset=".5" stop-color="#7C3AED"/><stop offset="1" stop-color="#C084FC"/></linearGradient></defs>
   <path id="inkglow" class="ink-glow" d="{SCRIPT}"/><path id="ink" class="ink" d="{SCRIPT}"/>
  </svg>
  <img class="orb" src="/assets/img/orb.svg" alt="" width="256" height="256" fetchpriority="high">
 </div>
 <h1>{t("مساعدتك العراقية اللي تشتغل بدون نت","Your Iraqi assistant that works offline")}</h1>
 {blk("p","احچي وياها بلهجتك، تفتحلك التطبيقات، تكتب، تدور وتجاوبك بصوت طبيعي — والعقل كله على تلفونك.","Talk in Iraqi Arabic or English. Lamda opens apps, types, searches and answers in a natural voice — with the brain running on your phone.","sub")}
 <div class="cta">{dl_btn()}<a class="btn btn-ghost btn-big" href="/install.html">{t("شلون أنصّبه؟","How to install")}</a></div>
 <p class="meta">{t("أندرويد 8 وفوك","Android 8+")} · <bdi>v<span data-version>{V}</span></bdi> · <bdi><span data-size>40.3</span> MB</bdi> · {t("مجاني","Free")}</p>
</div></section>

<section id="features"><div class="wrap center">
 <span class="eyebrow">{t("المميزات","Features")}</span>
 <h2>{t("كل اللي تحتاجه بمساعدة وحدة","Everything you need in one assistant")}</h2>
 {blk("p","مصممة للعراق: لهجتنا، تلفوناتنا، والنت اللي يروح ويجي.","Built for Iraq: our dialect, our phones, and internet that comes and goes.","lead")}
 <div class="grid g3" style="text-align:start">{fc}</div>
</div></section>

<section id="how"><div class="wrap center">
 <span class="eyebrow">{t("شلون تشتغل","How it works")}</span>
 <h2>{t("ثلاث خطوات وبس","Three steps, that's it")}</h2>
 <div class="grid g3 steps" style="text-align:start;margin-top:36px">{sc}</div>
</div></section>

<section id="shots"><div class="wrap center">
 <span class="eyebrow">{t("صور من التطبيق","Screenshots")}</span>
 <h2>{t("شوفها بعينك","See it for yourself")}</h2>
 <div class="carousel" aria-roledescription="carousel"><div class="track" tabindex="0" aria-label="Screenshots">{car}</div>
 <div class="car-btns"><button type="button" data-dir="-1" aria-label="Previous">‹</button><button type="button" data-dir="1" aria-label="Next">›</button></div></div>
</div></section>

<section id="pricing"><div class="wrap center">
 <span class="eyebrow">{t("الأسعار","Pricing")}</span>
 <h2>{t("ابدأ مجاناً، وطوّر وقت ما تحب","Start free, upgrade when you like")}</h2>
 {blk("p","الكوينات تُستخدم لميزات السحابة. المساعد على الجهاز يبقى مجاني. الاشتراكات راح تتفعل قريباً.","Coins are used for cloud features; the on-device assistant stays free. Subscriptions open soon.","lead")}
 <div class="toggle" role="group" aria-label="Billing period"><button type="button" data-period="m" aria-pressed="true">{t("شهري","Monthly")}</button><button type="button" data-period="y" aria-pressed="false">{t("سنوي","Yearly")}<span class="save">{t("وفّر ~17%","save ~17%")}</span></button></div>
 <div class="grid g3">{plans}</div>
 <div class="card topup reveal"><div style="text-align:start"><h3 style="margin:0">{t("شحن كوينات","Coin top-up")}</h3>{blk("p","1,000 كوين = 1,000 دينار. تنضاف لرصيدك وما تنتهي.","1,000 coins = 1,000 IQD. Added to your balance, never expire.")}</div><a class="btn btn-ghost" href="/pay.html">{t("اشحن","Top up")}</a></div>
</div></section>

<section id="faq"><div class="wrap" style="max-width:820px">
 <div class="center"><span class="eyebrow">{t("أسئلة شائعة","FAQ")}</span><h2>{t("عندك سؤال؟","Questions?")}</h2></div>
 {fq}
 <div class="center" style="margin-top:34px">{dl_btn()}</div>
</div></section>
''' + foot()

# ───────────── install ─────────────
def stepcards(items):
    return "".join(f'<div class="card reveal">{ill}<div><h2 class="h3" style="margin-top:0">{t(a,e)}</h2>{blk("p",da,de)}</div></div>' for ill, a, e, da, de in items)
P_DL = phone("p1", [(26, None), (40, False), (34, False), (30, False)])
P_ON = phone("p2", [(26, None), (24, True), (30, False), (28, False)])
P_INS = phone("p3", [(40, None), (30, False), (22, None), (44, False)])
P_RS = phone("p4", [(30, None), (26, False), (24, True), (20, False)])
P_OK = phone("p5", [(36, None), (26, True), (26, True), (26, True)])
common_dl = (P_DL, "نزّل الملف", "Download the file", 'دوس <a data-apk href="#">نزّل التطبيق</a>. ينفتح Google Drive — دوس زر التنزيل (السهم) وانتظر يكمل.', 'Tap <a data-apk href="#">Download</a>. Google Drive opens — tap the download arrow and wait for it to finish.')
common_rs = (P_RS, "اسمح بالإعدادات المقيدة (أندرويد 13+)", "Allow restricted settings (Android 13+)", "إذا ما خلاك تفعّل «إمكانية الوصول»: افتح معلومات تطبيق لمدا ← النقاط الثلاث ⋮ فوك ← «السماح بالإعدادات المقيدة»، وارجع فعّلها.", "If Android won't let you turn on Accessibility: open Lamda's App info → the ⋮ menu → “Allow restricted settings”, then try again.")
common_ok = (P_OK, "افتح لمدا وكمّل الإعداد", "Open Lamda and finish setup", "لمدا تمشيك على كل إذن خطوة بخطوة. تصوير الشاشة ينطلب بس وقت الحاجة.", "Lamda walks you through each permission. Screen capture is only asked when needed.")
brands = {
 "xiaomi": ("شاومي / ريدمي / پوكو", "Xiaomi / Redmi / POCO", [common_dl,
   (P_ON, "اسمح بالتثبيت من المصدر", "Allow this source", "افتح الملف من الإشعارات أو «مدير الملفات». إذا طلعت رسالة «لأمانك…»: دوس «الإعدادات» وفعّل «السماح من هذا المصدر». (أو: الإعدادات ← التطبيقات ← إدارة التطبيقات ← Chrome ← تثبيت تطبيقات غير معروفة).", "Open the file from the notification or File Manager. If you see “For your security…”, tap Settings and enable “Allow from this source”. (Or: Settings → Apps → Manage apps → Chrome → Install unknown apps.)"),
   (P_INS, "تجاوز فحص MIUI", "Get past the MIUI scan", "شاومي تسوي فحص أمان — انتظره يخلص، وبعدين دوس «متابعة التثبيت» أو «تثبيت على أي حال». إذا Play Protect سأل: «مزيد من التفاصيل» ← «التثبيت على أي حال».", "MIUI runs a security scan — let it finish, then tap “Continue installation” / “Install anyway”. If Play Protect asks: “More details” → “Install anyway”."),
   common_rs, (P_OK, "شغّل البداية التلقائية", "Allow Autostart", "بشاومي: معلومات التطبيق ← «التشغيل التلقائي» فعّله، و«توفير البطارية» ← «بلا قيود» حتى الفقاعة ما تنطفي.", "On Xiaomi: App info → enable “Autostart”, and Battery saver → “No restrictions” so the bubble isn't killed."), common_ok]),
 "samsung": ("سامسونگ", "Samsung", [common_dl,
   (P_ON, "اسمح بالتثبيت", "Allow installs", "افتح الملف من «ملفاتي» أو الإشعار. إذا رفض: الإعدادات ← التطبيقات ← ⋮ ← وصول خاص ← تثبيت تطبيقات غير معروفة ← اختار Chrome أو «ملفاتي» وفعّل «السماح».", "Open the file from My Files or the notification. If blocked: Settings → Apps → ⋮ → Special access → Install unknown apps → pick Chrome or My Files → Allow."),
   (P_INS, "طفّي «المانع التلقائي»", "Turn off Auto Blocker", "بـ One UI 6 وفوك: الإعدادات ← الأمان والخصوصية ← «المانع التلقائي» (Auto Blocker) ← إيقاف. تكدر ترجعه بعد التنصيب.", "On One UI 6+: Settings → Security and privacy → Auto Blocker → Off. You can turn it back on after installing."),
   common_rs, common_ok]),
 "other": ("باقي الأجهزة", "Other phones", [common_dl,
   (P_ON, "اسمح بتثبيت التطبيقات غير المعروفة", "Allow unknown apps", "الإعدادات ← التطبيقات ← وصول خاص للتطبيقات ← تثبيت تطبيقات غير معروفة ← المتصفح أو مدير الملفات ← سماح. (أوپو/ريلمي/هواوي: المكان قريب بالإعدادات ← الأمان).", "Settings → Apps → Special app access → Install unknown apps → your browser or Files → Allow. (Oppo/Realme/Huawei: similar, under Settings → Security.)"),
   (P_INS, "ثبّت", "Install", "افتح الملف ودوس «تثبيت». إذا Play Protect نبهك: «مزيد من التفاصيل» ← «التثبيت على أي حال».", "Open the file and tap Install. If Play Protect warns you: “More details” → “Install anyway”."),
   common_rs, common_ok]),
}
tabs = "".join(f'<button type="button" role="tab" id="t-{k}" aria-controls="{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{t(a,e)}</button>' for i, (k, (a, e, _)) in enumerate(brands.items()))
panels = "".join(f'<div role="tabpanel" id="{k}" aria-labelledby="t-{k}" class="howto"{"" if i == 0 else " hidden"}>{stepcards(items)}</div>' for i, (k, (_, _, items)) in enumerate(brands.items()))
install = head("تنزيل وتنصيب لمدا", "Download & install Lamda", "دليل تنصيب لمدا خطوة بخطوة لشاومي وسامسونگ وباقي الأجهزة", "Step-by-step install guide for Xiaomi, Samsung and other Android phones", "/install.html") + f'''
<div class="page"><div class="wrap">
 <span class="eyebrow">{t("التنصيب","Install")}</span>
 <h1>{t("نزّل لمدا ونصّبها","Download and install Lamda")}</h1>
 {blk("p","لمدا تنوزع مباشرة (مو من Play)، فأندرويد يطلب منك تسمح بالتثبيت مرة وحدة. اختار نوع تلفونك:","Lamda is distributed directly (not via Play), so Android asks you to allow the install once. Pick your phone:","lead")}
 <div class="cta" style="justify-content:flex-start">{dl_btn(False)}</div>
 <p class="fine"><bdi>v<span data-version>{V}</span></bdi> · <bdi><span data-size>40.3</span> MB</bdi> · SHA-256: <code data-sha style="word-break:break-all">a930cab27359075ebb7b67472ccdc80509dda524f0446ab8f839775eb0279b35</code></p>
 <div class="tabs" role="tablist" aria-label="Phone brand">{tabs}</div>
 {panels}
 <div class="notice">{t("ما نطلب منك أبداً كلمة سر أو رمز تحقق. إذا أحد طلب منك هيچ شي باسم لمدا، هذا احتيال.","We will never ask for a password or verification code. Anyone doing so in Lamda's name is a scam.")}</div>
</div></div>''' + foot()

# ───────────── pay ─────────────
pays = [("زين كاش","ZainCash","#E4003B","ZC","ادفع من محفظة زين كاش برقم تلفونك.","Pay from your ZainCash wallet with your phone number."),
        ("فاست پاي","FastPay","#1C4BD8","FP","ادفع من تطبيق FastPay بثواني.","Pay in seconds from the FastPay app."),
        ("كي كارد","Qi Card","#F7A600","Qi","ادفع بكارت كي أو ماستر كارد كي.","Pay with your Qi / Qi MasterCard.")]
pc = "".join(f'<div class="card pay reveal"><span class="logo" style="background:{c}" aria-hidden="true">{ab}</span><div style="flex:1"><h2 class="h3" style="margin:0">{t(a,e)}</h2>{blk("p",da,de)}</div><a class="btn btn-ghost" aria-disabled="true" role="link" tabindex="-1">{t("قريباً","Coming soon")}</a></div>' for a, e, c, ab, da, de in pays)
pay = head("الدفع — لمدا", "Payments — Lamda", "طرق الدفع لاشتراكات لمدا: زين كاش، فاست پاي، كي كارد", "Lamda payment methods: ZainCash, FastPay, Qi Card", "/pay.html") + f'''
<div class="page"><div class="wrap" style="max-width:820px">
 <span class="eyebrow">{t("الدفع","Payments")}</span>
 <h1>{t("طرق الدفع","Payment methods")}</h1>
 {blk("p","الاشتراكات وشحن الكوينات راح تتفعل قريباً. لحد ذاك الوقت، المساعد على الجهاز مجاني بالكامل.","Subscriptions and coin top-ups open soon. Until then the on-device assistant is completely free.","lead")}
 <div class="grid">{pc}</div>
 <div class="notice">{t("الأسعار: بلس 3,000 د.ع/شهر أو 30,000/سنة · برو 7,000 د.ع/شهر أو 65,000/سنة · 1,000 كوين = 1,000 د.ع.","Prices: Plus 3,000 IQD/mo or 30,000/yr · Pro 7,000 IQD/mo or 65,000/yr · 1,000 coins = 1,000 IQD.")}</div>
 <p><a href="/#pricing">{t("← رجوع للأسعار","← Back to pricing")}</a></p>
</div></div>''' + foot()

# ───────────── legal ─────────────
REVIEW = t("مسودة — تحتاج مراجعة قانونية قبل النشر الرسمي.", "DRAFT — needs legal review before official publication.")
def legal(path, ta, te, da, de, sections):
    body = "".join(f'<h2>{t(ha,he)}</h2>{blk("p",pa,pe)}' for ha, he, pa, pe in sections)
    return head(ta + " — لمدا", te + " — Lamda", da, de, path) + f'''
<div class="page"><div class="wrap prose"><span class="eyebrow">{t("قانوني","Legal")}</span><h1>{t(ta,te)}</h1>
<div class="notice" role="note">{REVIEW}</div><p class="fine">{t("آخر تحديث: ٢ تشرين الثاني ٢٠٢٦","Last updated: 2 November 2026")}</p>{body}
<h2>{t("تواصل","Contact")}</h2><p><a data-mail href="#">hello@lamda.ai</a></p></div></div>''' + foot()
privacy = legal("/privacy.html", "سياسة الخصوصية", "Privacy policy", "شلون لمدا تتعامل ويه بياناتك", "How Lamda handles your data", [
 ("شنو نجمع","What we collect","الأوامر الصوتية والنصية تنفهم على تلفونك. السوالف والذاكرة تنحفظ مشفرة على جهازك بس. ما نجمع أسماء أو أرقام أو مواقع.","Voice and text commands are understood on your phone. Chats and memory are stored encrypted on your device only. We don't collect names, numbers or locations."),
 ("ميزات السحابة","Cloud features","إذا حطيت مفتاح API مالتك أو استخدمت ميزة سحابية، النص (أو صورة الشاشة لما تطلبها) ينرسل للمزوّد اللي اخترته (مثل Google أو OpenAI أو Anthropic) حسب سياساتهم.","If you add your own API key or use a cloud feature, the text (or a screenshot when you ask for one) is sent to the provider you chose (e.g. Google, OpenAI or Anthropic) under their policies."),
 ("الأذونات","Permissions","إمكانية الوصول: حتى تدوس وتكتب بدالك؛ ما تقرأ حقول كلمات السر. المايك: حتى تسمعك. تصوير الشاشة: بس لما تطلب «شنو على شاشتي؟» وبموافقتك كل مرة.","Accessibility: to tap and type for you; password fields are never read. Microphone: to hear you. Screen capture: only when you ask “what's on my screen?”, with your consent each session."),
 ("الدفع","Payments","لما يتفعل الدفع، معلومات الدفع تتعالج عند مزوّد الدفع (زين كاش، فاست پاي، كي كارد) وإحنا ما نخزن بيانات الكارت.","When payments launch, payment details are processed by the payment provider (ZainCash, FastPay, Qi Card); we don't store card data."),
 ("حقوقك","Your rights","تكدر تمسح الذاكرة والسوالف من الإعدادات بأي وقت، أو تمسح التطبيق وكل بياناته تنمسح ويّاه.","You can delete memory and chats from Settings at any time, or uninstall the app to remove all of its data."),
])
terms = legal("/terms.html", "شروط الاستخدام", "Terms of use", "شروط استخدام تطبيق لمدا", "Terms for using the Lamda app", [
 ("القبول","Acceptance","باستخدامك لمدا توافق على هاي الشروط.","By using Lamda you agree to these terms."),
 ("الاستخدام","Use","تستخدم لمدا لأغراض قانونية بس، وإنت مسؤول عن الأوامر اللي تعطيها.","Use Lamda only for lawful purposes; you are responsible for the commands you give it."),
 ("الذكاء الاصطناعي","AI output","أجوبة الذكاء الاصطناعي ممكن تغلط. لا تعتمد عليها بقرارات طبية أو قانونية أو مالية.","AI answers can be wrong. Don't rely on them for medical, legal or financial decisions."),
 ("الاشتراكات والكوينات","Subscriptions & coins","الأسعار تنعرض بالدينار العراقي. الكوينات ما تنسترجع نقداً إلا إذا القانون يفرض غير هيچ.","Prices are shown in Iraqi dinars. Coins are not redeemable for cash unless required by law."),
 ("بلا ضمان","No warranty","التطبيق مقدّم «كما هو» بدون ضمانات، بالحدود اللي يسمح بيها القانون.","The app is provided “as is” without warranties, to the extent permitted by law."),
])

pages = {"index.html": index, "install.html": install, "pay.html": pay, "privacy.html": privacy, "terms.html": terms}
for n, h in pages.items(): open(os.path.join(ROOT, n), "w").write(based(h))
open(os.path.join(ROOT, "404.html"), "w").write(based(head("الصفحة مو موجودة","Page not found","الصفحة مو موجودة","Page not found","/404.html") +
     f'<div class="page"><div class="wrap center"><img src="/assets/img/orb.svg" alt="" width="140" height="140" style="margin:0 auto"><h1>{t("هاي الصفحة مو موجودة","This page doesn't exist")}</h1><p><a class="btn btn-primary" href="/">{t("رجوع للرئيسية","Back home")}</a></p></div></div>' + foot()))
today = datetime.date.today().isoformat()
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f'  <url><loc>{SITE}/{"" if n == "index.html" else n}</loc><lastmod>{today}</lastmod></url>\n' for n in pages) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(ROOT, "site.webmanifest"), "w").write(json.dumps({"name": "Lamda · لمدا", "short_name": "Lamda", "lang": "ar", "dir": "rtl", "start_url": BASE + "/", "scope": BASE + "/", "display": "standalone",
    "background_color": "#FFFFFF", "theme_color": "#7C3AED", "icons": [{"src": BASE + "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": BASE + "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=1))
open(os.path.join(ROOT, "_headers"), "w").write("/assets/*\n  Cache-Control: public, max-age=604800\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n")
print("built", list(pages))
