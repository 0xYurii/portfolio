#!/usr/bin/env python3
# Build the static multi-page site + a single-file clickable preview
# from one shared content source, with EN/FR/AR i18n.
# Run from portfolio-new/: python3 tools/build.py
import json, os, base64, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
ICONS = json.load(open("tools/_icons.json"))

CV_PREVIEW_URL = "https://pub.hyperagent.com/api/published/pbf01KY7C19AA_9GAZN59EWMD7XTHV/Younes-Hebaiche-CV.pdf"
SITE = "https://0xyuri.vercel.app"
ANALYTICS_SCRIPT = '<script defer src="https://cdn.vercel-insights.com/v1/script.js"></script>'
esc = lambda s: html.escape(s, quote=False)

# ---------------- icons / sprite ----------------
SYMS = {
 'node':'si:nodedotjs','express':'si:express','typescript':'si:typescript','javascript':'si:javascript',
 'postgresql':'si:postgresql','prisma':'si:prisma','redis':'si:redis','docker':'si:docker',
 'socketio':'si:socketdotio','jest':'si:jest','ghactions':'si:githubactions','linux':'si:linux',
 'react':'si:react','html5':'si:html5','css':'si:css','github':'si:github','linkedin':'si:linkedin',
 'mail':'lu:mail','download':'lu:download','arrow':'lu:arrow-up-right','back':'lu:arrow-left',
 'copy':'lu:copy','check':'lu:check','sun':'lu:sun','moon':'lu:moon','menu':'lu:menu','ext':'lu:external-link',
}
NEUTRAL = {'si:express','si:prisma','si:socketdotio','si:github'}
NEUTRAL_SIDS = {sid for sid, key in SYMS.items() if key in NEUTRAL}

def sprite():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">']
    for sid, key in SYMS.items():
        ic = ICONS[key]; vb = ic.get("viewBox","0 0 24 24")
        if ic["kind"] == "stroke":
            out.append(f'<symbol id="i-{sid}" viewBox="{vb}" fill="none" stroke="currentColor" '
                       f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ic["inner"]}</symbol>')
        else:
            out.append(f'<symbol id="i-{sid}" viewBox="{vb}" fill="currentColor">{ic["inner"]}</symbol>')
    out.append('</svg>')
    return "\n".join(out)

def ico(sid, cls=""):
    parts = ["ico", "ic-" + sid]
    if sid in NEUTRAL_SIDS: parts.append("ic-neutral")
    if cls: parts.append(cls)
    return f'<svg class="{" ".join(parts)}" aria-hidden="true"><use href="#i-{sid}"/></svg>'

# ---------------- i18n registry ----------------
EN, FR, AR = {}, {}, {}
def reg(key, en, fr, ar):
    EN[key] = en; FR[key] = fr; AR[key] = ar
    return key

def S(key):   # English text for the HTML source
    return esc(EN[key])

def tspan(key, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-i18n="{key}">{S(key)}</{tag}>'

# --- global UI strings ---
reg("nav.work","Work","Projets","المشاريع")
reg("nav.about","About","À propos","نبذة")
reg("nav.skills","Skills","Compétences","المهارات")
reg("nav.contact","Contact","Contact","تواصل")
reg("nav.cv","CV","CV","السيرة")
reg("hero.kicker","backend developer — node.js / typescript","développeur backend — node.js / typescript","مطوّر backend — node.js / typescript")
reg("hero.lede","I build server-side systems — API gateways, REST services, and the data layers underneath them.",
    "Je conçois des systèmes côté serveur — passerelles d’API, services REST et les couches de données qui les soutiennent.",
    "أبني أنظمة من جهة الخادم — بوّابات API، وخدمات REST، وطبقات البيانات تحتها.")
reg("hero.sub","Computer science student at ESI-SBA — École Supérieure en Informatique de Sidi Bel Abbès. Based in Chlef, Algeria. Goes by Yuri.",
    "Étudiant en informatique à l’ESI-SBA — École Supérieure en Informatique de Sidi Bel Abbès. Basé à Chlef, en Algérie. Surnommé Yuri.",
    "طالب علوم حاسوب في ESI-SBA — المدرسة العليا للإعلام الآلي بسيدي بلعباس. مقيم في الشلف، الجزائر. يُعرف باسم Yuri.")
reg("hero.viewwork","View work","Voir les projets","استعراض المشاريع")
reg("btn.cv","Download CV","Télécharger le CV","تحميل السيرة الذاتية")
reg("sec.work","Selected work","Projets sélectionnés","أعمال مختارة")
reg("sec.about","About","À propos","نبذة عني")
reg("sec.skills","Skills","Compétences","المهارات")
reg("sec.contact","Contact","Contact","تواصل")
reg("card.cta","View project","Voir le projet","عرض المشروع")
reg("about.p1","I’m a backend developer and computer science student at ESI-SBA. Most of what I build lives in the Node.js / TypeScript ecosystem: REST APIs, authentication systems, and PostgreSQL schemas designed to stay sane as products grow.",
    "Je suis développeur backend et étudiant en informatique à l’ESI-SBA. L’essentiel de ce que je construis vit dans l’écosystème Node.js / TypeScript : des API REST, des systèmes d’authentification et des schémas PostgreSQL pensés pour rester maintenables à mesure que les produits grandissent.",
    "أنا مطوّر backend وطالب علوم حاسوب في ESI-SBA. معظم ما أبنيه ضمن منظومة Node.js / TypeScript: واجهات REST، وأنظمة مصادقة، ومخططات PostgreSQL مصمّمة لتبقى واضحة مع نموّ المنتجات.")
reg("about.p2","I started on the frontend — components, layouts, the usual React path — and kept drifting toward the questions behind the interface: where the data lives, how requests fail, what happens under load. Eventually I stopped drifting and made the server side home. The frontend years still earn their keep: I ship full-stack when a project calls for it, and I think about the developers consuming my APIs the way frontend taught me to think about users.",
    "J’ai commencé côté frontend — composants, mises en page, le parcours React habituel — puis j’ai glissé vers les questions derrière l’interface : où vivent les données, comment les requêtes échouent, ce qui se passe sous la charge. J’ai fini par m’installer côté serveur. Les années frontend restent utiles : je livre en full-stack quand un projet l’exige, et je pense aux développeurs qui consomment mes API comme le frontend m’a appris à penser aux utilisateurs.",
    "بدأت في الواجهة الأمامية — المكوّنات والتخطيطات ومسار React المعتاد — ثم انجذبت إلى الأسئلة خلف الواجهة: أين تُخزَّن البيانات، وكيف تفشل الطلبات، وماذا يحدث تحت الضغط. في النهاية استقرّ بي المقام في جانب الخادم. وما زالت سنوات الواجهة الأمامية مفيدة: أطوّر full-stack عند الحاجة، وأفكّر في المطوّرين الذين يستهلكون واجهاتي كما علّمتني الواجهة الأمامية التفكير في المستخدمين.")
reg("about.p3","Lately the work has an infrastructure flavor — Aegis, my from-scratch API gateway, exists because I wanted to know exactly what NGINX and Kong do all day. Based in Chlef, Algeria (UTC+1); comfortable working remote and async.",
    "Depuis peu, mon travail prend une teinte infrastructure — Aegis, ma passerelle d’API écrite de zéro, existe parce que je voulais savoir exactement ce que font NGINX et Kong à longueur de journée. Basé à Chlef, en Algérie (UTC+1) ; à l’aise en télétravail et en asynchrone.",
    "مؤخّرًا صار العمل ذا طابع بنية تحتية — Aegis، بوّابة API التي كتبتها من الصفر، وُجدت لأنني أردت أن أعرف بالضبط ما تفعله NGINX وKong طوال اليوم. مقيم في الشلف، الجزائر (UTC+1)؛ معتاد على العمل عن بُعد وبشكل غير متزامن.")
reg("skills.g1","Backend & runtime","Backend & runtime","الخلفية والتشغيل")
reg("skills.g2","Data & state","Données & état","البيانات والحالة")
reg("skills.g3","Infra & delivery","Infra & déploiement","البنية والنشر")
reg("skills.g4","Testing & realtime","Tests & temps réel","الاختبار والزمن الفعلي")
reg("skills.g5","Frontend origins","Origines frontend","الجذور الأمامية")
reg("contact.lede","The inbox is open.","La boîte est ouverte.","البريد مفتوح.")
reg("contact.sub","Internships, freelance backend work, or a hard problem you want to talk through — I read everything.",
    "Stages, missions backend en freelance, ou un problème épineux à discuter — je lis tout.",
    "تدريبات، أو أعمال backend حرّة، أو مشكلة تقنية صعبة تريد مناقشتها — أقرأ كل الرسائل.")
reg("contact.copy","Copy","Copier","نسخ")
reg("contact.copied","Copied","Copié","تم النسخ")
reg("contact.copyfail","Copy failed","Échec","فشل النسخ")
reg("detail.back","Back to work","Retour aux projets","العودة إلى المشاريع")
reg("detail.highlights","Highlights","Points clés","أبرز النقاط")
reg("detail.tech","Tech","Technologies","التقنيات")
reg("detail.links","Links","Liens","روابط")
reg("detail.viewsource","View source","Voir le code","عرض الكود")
reg("aegis.diagcap","fig.01 — one request through Aegis: rate limiting → auth → circuit breaking → load balancing, traced end-to-end by UUID.",
    "fig.01 — une requête à travers Aegis : limitation de débit → authentification → disjoncteur → répartition de charge, tracée de bout en bout par UUID.",
    "شكل 01 — طلب واحد عبر Aegis: تحديد المعدّل ← المصادقة ← قاطع الدارة ← توزيع الحِمل، متتبَّع من الطرف إلى الطرف عبر UUID.")
reg("a11y.langgroup","Language","Langue","اللغة")

# ---------------- content ----------------
SOCIALS = [
    ('github','https://github.com/0xYurii','GitHub'),
    ('linkedin','https://www.linkedin.com/in/younes-hebaiche-750676358','LinkedIn'),
    ('mail','mailto:y.hebaiche@esi-sba.dz','Email'),
]
SKILL_GROUPS = [
    ("skills.g1", [('node','Node.js'),('express','Express'),('typescript','TypeScript'),('javascript','JavaScript')]),
    ("skills.g2", [('postgresql','PostgreSQL'),('prisma','Prisma'),('redis','Redis')]),
    ("skills.g3", [('docker','Docker'),('ghactions','GitHub Actions'),('linux','Linux')]),
    ("skills.g4", [('jest','Jest'),('socketio','Socket.IO')]),
    ("skills.g5", [('react','React'),('html5','HTML5'),('css','CSS')]),
]

DIAGRAM = '''<figure class="diagram">
  <div class="dg-scroll">
  <svg viewBox="0 0 920 330" role="img" aria-labelledby="dgt dgd" xmlns="http://www.w3.org/2000/svg">
    <title id="dgt">Aegis request path</title>
    <desc id="dgd">A request flows from a client through the Aegis gateway (rate limiter, JWT auth, circuit breaker, load balancer) out to service instances; one instance is circuit-open and receives no traffic.</desc>
    <rect class="dg-box" x="24" y="132" width="96" height="52" rx="4"/>
    <text class="dg-strong" x="72" y="162" text-anchor="middle">client</text>
    <line class="dg-line" x1="120" y1="158" x2="204" y2="158"/>
    <path class="dg-chev" d="M196 152 l8 6 -8 6"/>
    <text class="dg-sm" x="162" y="146" text-anchor="middle">x-request-id</text>
    <rect class="dg-box" x="208" y="76" width="392" height="164" rx="4"/>
    <circle class="dg-ok" cx="226" cy="97" r="3.5"/>
    <text class="dg-strong" x="238" y="101">aegis — gateway :8080</text>
    <rect class="dg-stage" x="222" y="136" width="86" height="48" rx="4"/>
    <text class="dg-txt" x="265" y="163" text-anchor="middle">rate limiter</text>
    <rect class="dg-stage" x="316" y="136" width="86" height="48" rx="4"/>
    <text class="dg-txt" x="359" y="163" text-anchor="middle">jwt auth</text>
    <rect class="dg-stage" x="410" y="136" width="86" height="48" rx="4"/>
    <text class="dg-txt" x="453" y="158" text-anchor="middle">circuit</text>
    <text class="dg-txt" x="453" y="170" text-anchor="middle">breaker</text>
    <rect class="dg-stage" x="504" y="136" width="86" height="48" rx="4"/>
    <text class="dg-txt" x="547" y="163" text-anchor="middle">load balancer</text>
    <line class="dg-line" x1="308" y1="160" x2="316" y2="160"/>
    <line class="dg-line" x1="402" y1="160" x2="410" y2="160"/>
    <line class="dg-line" x1="496" y1="160" x2="504" y2="160"/>
    <line class="dg-line dg-dash" x1="265" y1="184" x2="265" y2="278"/>
    <rect class="dg-box" x="222" y="278" width="86" height="34" rx="4"/>
    <text class="dg-txt" x="265" y="299" text-anchor="middle">redis :6379</text>
    <line class="dg-line" x1="600" y1="160" x2="636" y2="160"/>
    <line class="dg-line" x1="636" y1="96" x2="636" y2="160"/>
    <line class="dg-line dg-dash" x1="636" y1="160" x2="636" y2="224"/>
    <line class="dg-line" x1="636" y1="96" x2="668" y2="96"/>
    <line class="dg-line" x1="636" y1="160" x2="668" y2="160"/>
    <line class="dg-line dg-dash" x1="636" y1="224" x2="668" y2="224"/>
    <path class="dg-chev" d="M660 90 l8 6 -8 6"/>
    <path class="dg-chev" d="M660 154 l8 6 -8 6"/>
    <rect class="dg-box" x="668" y="72" width="204" height="48" rx="4"/>
    <circle class="dg-ok" cx="686" cy="96" r="3.5"/>
    <text class="dg-strong" x="700" y="92">users-svc</text>
    <text class="dg-sm" x="700" y="107">:8081 · healthy</text>
    <rect class="dg-box" x="668" y="136" width="204" height="48" rx="4"/>
    <circle class="dg-ok" cx="686" cy="160" r="3.5"/>
    <text class="dg-strong" x="700" y="156">orders-svc</text>
    <text class="dg-sm" x="700" y="171">:8082 · healthy</text>
    <rect class="dg-box dg-dash" x="668" y="200" width="204" height="48" rx="4"/>
    <circle class="dg-bad" cx="686" cy="224" r="3.5"/>
    <text class="dg-strong" x="700" y="220">billing-svc</text>
    <text class="dg-sm" x="700" y="235">:8083 · circuit: open</text>
    <text class="dg-sm" x="668" y="266">half-open probe in 12s</text>
  </svg>
  </div>
  <figcaption data-i18n="aegis.diagcap">''' + S("aegis.diagcap") + '''</figcaption>
</figure>'''

# projects: translatable fields are (en, fr, ar)
PROJECTS = [
 {"slug":"aegis","num":1,"diagram":True,"links":{"source":"https://github.com/0xYurii/Aegis"},
  "kicker":("API Gateway","Passerelle d’API","بوّابة API"),
  "sub":("Custom API gateway & microservice orchestrator","Passerelle d’API et orchestrateur de microservices sur mesure","بوّابة API مخصّصة ومنسّق خدمات مصغّرة"),
  "role":("Solo project","Projet solo","مشروع فردي"),
  "dates":("04.2026 — 05.2026","04.2026 — 05.2026","04.2026 — 05.2026"),
  "hook":("An API gateway written from scratch in Node.js and TypeScript — no NGINX, no Kong — owning every layer between a request and the service that answers it.",
          "Une passerelle d’API écrite de zéro en Node.js et TypeScript — sans NGINX ni Kong — qui maîtrise chaque couche entre une requête et le service qui y répond.",
          "بوّابة API مكتوبة من الصفر بـ Node.js وTypeScript — دون NGINX أو Kong — تتحكّم في كل طبقة بين الطلب والخدمة التي تجيب عليه."),
  "overview":[
    ("Aegis is a custom API gateway and microservice orchestrator built to understand — and own — everything that sits between a client request and the service that answers it. Instead of reaching for NGINX or Kong, I implemented the routing, resilience, and security layers myself, in Node.js and TypeScript.",
     "Aegis est une passerelle d’API et un orchestrateur de microservices conçus pour comprendre — et maîtriser — tout ce qui se trouve entre la requête d’un client et le service qui y répond. Plutôt que d’utiliser NGINX ou Kong, j’ai implémenté moi-même les couches de routage, de résilience et de sécurité, en Node.js et TypeScript.",
     "Aegis بوّابة API ومنسّق خدمات مصغّرة صُمّمت لفهم — والتحكّم في — كل ما يقع بين طلب العميل والخدمة التي تجيب عليه. وبدلاً من استخدام NGINX أو Kong، نفّذت بنفسي طبقات التوجيه والمرونة والأمان بـ Node.js وTypeScript."),
    ("The result is a nine-service system wired together with Docker Compose, with every request traceable end-to-end by a UUID that follows it across service boundaries.",
     "Le résultat est un système de neuf services reliés par Docker Compose, où chaque requête est traçable de bout en bout grâce à un UUID qui la suit à travers les services.",
     "النتيجة نظام من تسع خدمات مربوطة عبر Docker Compose، مع إمكانية تتبّع كل طلب من الطرف إلى الطرف عبر مُعرّف UUID يرافقه بين الخدمات."),
  ],
  "highlights":[
    ("Round-robin load balancer fronted by a custom three-state circuit breaker (closed / open / half-open) that reroutes around failing instances and self-heals on recovery.",
     "Répartiteur de charge round-robin précédé d’un disjoncteur à trois états (fermé / ouvert / semi-ouvert) qui contourne les instances défaillantes et se rétablit automatiquement.",
     "موزّع حِمل round-robin يسبقه قاطع دارة بثلاث حالات (مغلق / مفتوح / نصف مفتوح) يعيد التوجيه بعيدًا عن النسخ المتعطّلة ويتعافى تلقائيًا."),
    ("Distributed, Redis-backed rate limiter shared across gateway replicas.",
     "Limiteur de débit distribué, adossé à Redis et partagé entre les répliques de la passerelle.",
     "محدّد معدّل موزّع معتمد على Redis ومشترك بين نسخ البوّابة."),
    ("Centralized JWT middleware that verifies tokens once and injects sanitized user context into downstream services.",
     "Middleware JWT centralisé qui vérifie les jetons une seule fois et injecte un contexte utilisateur assaini dans les services en aval.",
     "وسيط JWT مركزي يتحقّق من الرموز مرة واحدة ويحقن سياق مستخدم منقّى في الخدمات التالية."),
    ("100% Jest coverage on the core logic (breaker, balancer, limiter).",
     "Couverture Jest de 100 % sur la logique centrale (disjoncteur, répartiteur, limiteur).",
     "تغطية اختبارات Jest بنسبة 100% للمنطق الأساسي (القاطع، الموزّع، المحدّد)."),
    ("GitHub Actions CI that runs the test suite and publishes Docker images to GHCR on every merge.",
     "CI GitHub Actions qui exécute la suite de tests et publie les images Docker sur GHCR à chaque fusion.",
     "تكامل مستمر عبر GitHub Actions يشغّل الاختبارات وينشر صور Docker إلى GHCR عند كل دمج."),
    ("UUID-based request tracing across all nine services via a custom logging plugin.",
     "Traçage des requêtes par UUID à travers les neuf services via un plugin de journalisation maison.",
     "تتبّع الطلبات بمُعرّف UUID عبر الخدمات التسع جميعها بواسطة إضافة تسجيل مخصّصة."),
  ]},
 {"slug":"wasselni","num":2,"diagram":False,"links":{},
  "kicker":("Carpooling Platform","Plateforme de covoiturage","منصّة مشاركة الركوب"),
  "sub":("Full-stack North African carpooling platform","Plateforme de covoiturage nord-africaine full-stack","منصّة مشاركة ركوب مغاربية متكاملة"),
  "role":("Backend lead · team of 5","Responsable backend · équipe de 5","قائد الـ backend · فريق من 5"),
  "dates":("03.2026 — present","03.2026 — présent","03.2026 — الآن"),
  "hook":("A localized ride-sharing platform built around real transportation friction in the region. I lead the backend on a five-person team.",
          "Une plateforme de covoiturage localisée, pensée pour les vrais problèmes de transport de la région. Je dirige le backend au sein d’une équipe de cinq personnes.",
          "منصّة مشاركة ركوب محلّية بُنيت حول مشكلات النقل الحقيقية في المنطقة. أقود جانب الـ backend ضمن فريق من خمسة أشخاص."),
  "note":("Private team repository — source not public.","Dépôt d’équipe privé — code non public.","مستودع فريق خاص — الكود غير عمومي."),
  "overview":[
    ("Wasselni is a carpooling platform aimed at real transportation friction across North Africa. I lead the backend for a five-person team, owning the API architecture, the data model, and every flow from searching for a ride to a booked seat.",
     "Wasselni est une plateforme de covoiturage qui s’attaque aux véritables frictions de transport en Afrique du Nord. Je dirige le backend d’une équipe de cinq personnes, responsable de l’architecture de l’API, du modèle de données et de chaque parcours, de la recherche d’un trajet à la réservation d’une place.",
     "Wasselni منصّة مشاركة ركوب تعالج مشكلات النقل الحقيقية في شمال إفريقيا. أقود جانب الـ backend لفريق من خمسة أشخاص، وأتولّى بنية الـ API ونموذج البيانات وكل مسار من البحث عن رحلة إلى حجز مقعد."),
    ("The backend is a modular Express/TypeScript REST API over a PostgreSQL database modeled with Prisma — a schema that keeps users, rides, vehicles, and bookings coherent as features grow.",
     "Le backend est une API REST modulaire en Express/TypeScript sur une base PostgreSQL modélisée avec Prisma — un schéma qui garde utilisateurs, trajets, véhicules et réservations cohérents à mesure que les fonctionnalités évoluent.",
     "الـ backend واجهة REST معيارية بـ Express/TypeScript فوق قاعدة PostgreSQL مُنمذجة بـ Prisma — مخطّط يحافظ على تماسك المستخدمين والرحلات والمركبات والحجوزات مع تنامي الميزات."),
  ],
  "highlights":[
    ("PostgreSQL + Prisma schema covering users, rides, vehicles, and bookings.",
     "Schéma PostgreSQL + Prisma couvrant utilisateurs, trajets, véhicules et réservations.",
     "مخطّط PostgreSQL + Prisma يغطّي المستخدمين والرحلات والمركبات والحجوزات."),
    ("Secure JWT authentication and session handling.",
     "Authentification JWT sécurisée et gestion des sessions.",
     "مصادقة JWT آمنة وإدارة للجلسات."),
    ("Advanced ride search and filtering, plus a complete end-to-end booking flow.",
     "Recherche et filtrage avancés de trajets, ainsi qu’un parcours de réservation complet de bout en bout.",
     "بحث وتصفية متقدّمان للرحلات، إضافة إلى مسار حجز كامل من البداية إلى النهاية."),
    ("Separate driver and passenger dashboards on a clean, modular REST API.",
     "Tableaux de bord distincts pour conducteurs et passagers sur une API REST claire et modulaire.",
     "لوحتا تحكّم منفصلتان للسائق والراكب على واجهة REST نظيفة ومعيارية."),
  ]},
 {"slug":"nodetalk","num":3,"diagram":False,"links":{"source":"https://github.com/0xYurii/node-talk"},
  "kicker":("Developer Social Network","Réseau social de développeurs","شبكة اجتماعية للمطوّرين"),
  "sub":("A social network for developers, with real-time chat","Un réseau social pour développeurs, avec messagerie en temps réel","شبكة اجتماعية للمطوّرين مع دردشة فورية"),
  "role":("Solo project","Projet solo","مشروع فردي"),
  "dates":("01.2026 — 02.2026","01.2026 — 02.2026","01.2026 — 02.2026"),
  "hook":("“The social network for developers who read documentation.” Full-stack, with real-time 1:1 chat over Socket.IO.",
          "« Le réseau social des développeurs qui lisent la documentation. » Full-stack, avec messagerie 1:1 en temps réel via Socket.IO.",
          "«الشبكة الاجتماعية للمطوّرين الذين يقرؤون التوثيق.» متكاملة، مع دردشة فردية فورية عبر Socket.IO."),
  "overview":[
    ("NodeTalk is a full-stack social network tailored to developers. The interesting problems live in two places: the relational data model, and a real-time messaging layer.",
     "NodeTalk est un réseau social full-stack conçu pour les développeurs. Les problèmes intéressants se trouvent à deux endroits : le modèle de données relationnel et la couche de messagerie en temps réel.",
     "NodeTalk شبكة اجتماعية متكاملة مصمّمة للمطوّرين. تكمن المسائل المثيرة في موضعين: نموذج البيانات العلائقي، وطبقة الرسائل الفورية."),
    ("The data model — feeds, follows, follow-requests, and conversations — is handled in PostgreSQL via Prisma. Real-time 1:1 chat runs over Socket.IO, and authentication supports three strategies at once.",
     "Le modèle de données — fils d’actualité, abonnements, demandes d’abonnement et conversations — est géré dans PostgreSQL via Prisma. La messagerie 1:1 en temps réel repose sur Socket.IO, et l’authentification prend en charge trois stratégies à la fois.",
     "يُدار نموذج البيانات — الخلاصات والمتابعات وطلبات المتابعة والمحادثات — في PostgreSQL عبر Prisma. وتعمل الدردشة الفردية الفورية عبر Socket.IO، وتدعم المصادقة ثلاث استراتيجيات في آنٍ واحد."),
  ],
  "highlights":[
    ("Real-time private 1:1 messaging over WebSockets (Socket.IO).",
     "Messagerie privée 1:1 en temps réel via WebSockets (Socket.IO).",
     "رسائل خاصة فردية فورية عبر WebSockets (Socket.IO)."),
    ("Relational feed / follow / conversation model in PostgreSQL + Prisma.",
     "Modèle relationnel fil / abonnement / conversation dans PostgreSQL + Prisma.",
     "نموذج علائقي للخلاصة / المتابعة / المحادثة في PostgreSQL + Prisma."),
    ("Multi-strategy authentication: local credentials, guest access, and GitHub OAuth.",
     "Authentification multi-stratégies : identifiants locaux, accès invité et OAuth GitHub.",
     "مصادقة متعدّدة الاستراتيجيات: بيانات اعتماد محلّية، ووصول كضيف، وGitHub OAuth."),
  ]},
 {"slug":"mapreach","num":4,"diagram":False,"links":{"source":"https://github.com/0xYurii/MapReach"},
  "kicker":("Chrome Extension","Extension Chrome","إضافة Chrome"),
  "sub":("Turn Google Maps listings into organized outreach leads","Transformer les fiches Google Maps en prospects organisés","تحويل نتائج خرائط Google إلى قائمة عملاء محتملين منظّمة"),
  "role":("Built for my own workflow","Créé pour mon propre usage","صُنع لسير عملي الخاص"),
  "dates":("Open source","Open source","مفتوح المصدر"),
  "hook":("A Chrome extension that turns Google Maps listings into organized outreach leads — collect, dedupe, and export prospects without leaving the map.",
          "Une extension Chrome qui transforme les fiches Google Maps en prospects organisés — collecter, dédupliquer et exporter sans quitter la carte.",
          "إضافة Chrome تحوّل نتائج خرائط Google إلى قائمة عملاء محتملين منظّمة — تجميع وإزالة تكرار وتصدير دون مغادرة الخريطة."),
  "overview":[
    ("MapReach is a small tool for an honest problem: I needed a faster way to build prospect lists while freelancing, so I built a Chrome extension that captures business listings straight from Google Maps.",
     "MapReach est un petit outil pour un problème bien réel : il me fallait un moyen plus rapide de constituer des listes de prospects en freelance, alors j’ai créé une extension Chrome qui capture les fiches d’entreprises directement depuis Google Maps.",
     "MapReach أداة صغيرة لمشكلة حقيقية: احتجت طريقة أسرع لبناء قوائم العملاء أثناء العمل الحر، فطوّرت إضافة Chrome تلتقط بيانات الأنشطة التجارية مباشرة من خرائط Google."),
    ("It collects listings, dedupes them, and exports a clean lead list — then I open-sourced it because the problem isn’t mine alone.",
     "Elle collecte les fiches, supprime les doublons et exporte une liste de prospects propre — puis je l’ai rendue open source, car le problème n’est pas le mien seul.",
     "تجمع النتائج وتزيل المكرّر منها وتصدّر قائمة عملاء نظيفة — ثم جعلتها مفتوحة المصدر لأن المشكلة ليست مشكلتي وحدي."),
  ],
  "highlights":[
    ("Collects business listings directly from the Google Maps UI.",
     "Collecte les fiches d’entreprises directement depuis l’interface Google Maps.",
     "تجمع بيانات الأنشطة مباشرة من واجهة خرائط Google."),
    ("Dedupes and organizes prospects into an exportable list.",
     "Déduplique et organise les prospects dans une liste exportable.",
     "تزيل التكرار وتنظّم العملاء في قائمة قابلة للتصدير."),
    ("Open source, built to scratch a real freelance-outreach itch.",
     "Open source, né d’un vrai besoin de prospection en freelance.",
     "مفتوح المصدر، وُلد من حاجة حقيقية للتنقيب عن عملاء العمل الحر."),
  ]},
]

# register project strings
for p in PROJECTS:
    sl = p["slug"]
    for f in ("kicker","sub","role","dates","hook"):
        reg(f"{sl}.{f}", *p[f])
    if p.get("note"): reg(f"{sl}.note", *p["note"])
    for i,tr in enumerate(p["overview"]):  reg(f"{sl}.ov.{i}", *tr)
    for i,tr in enumerate(p["highlights"]): reg(f"{sl}.hl.{i}", *tr)

# ---------------- render context ----------------
class Ctx:
    def __init__(self, target, assets=None):
        self.target = target            # 'index' | 'proj' | 'preview'
        self.assets = assets or {}
    def a(self, path):
        return ("../" + path) if self.target == "proj" else path
    def home(self):
        return {"index":"#top","proj":"../index.html","preview":"#/"}[self.target]
    def proj(self, slug):
        if self.target == "preview": return f"#/{slug}"
        if self.target == "proj":    return f"{slug}.html"
        return f"projects/{slug}.html"
    def nav(self, sec):
        if self.target == "preview": return ("#/", f' data-nav="#{sec}"')
        if self.target == "proj":    return (f"../index.html#{sec}", "")
        return (f"#{sec}", "")
    def cover(self, slug):
        if self.target == "preview": return self.assets.get("cover:"+slug, "")
        return self.a(f"img/covers/{slug}.jpg")
    def avatar(self):
        if self.target == "preview": return self.assets.get("avatar","")
        return self.a("img/avatar.jpg")
    def cv(self):
        return CV_PREVIEW_URL if self.target == "preview" else self.a("cv/Younes-Hebaiche-CV.pdf")
    def favicon(self):
        return self.assets.get("favicon","") if self.target == "preview" else self.a("favicon.svg")

def social_row(ctx, cls="socials"):
    items = []
    for sym, href, label in SOCIALS:
        ext = "" if href.startswith("mailto:") else ' target="_blank" rel="noopener noreferrer"'
        items.append(f'<a href="{href}"{ext} aria-label="{label}">{ico(sym)}</a>')
    return f'<div class="{cls}">' + "".join(items) + '</div>'

def tech_chips(tech):
    return '<div class="chips">' + "".join(ico(s, "chip") for s,_ in tech) + '</div>'

def logo_grid(tech, cls="logo-grid"):
    items = "".join(f'<div class="logo-item">{ico(s,"ico-lg")}<span>{esc(l)}</span></div>' for s,l in tech)
    return f'<div class="{cls}">{items}</div>'

def langs():
    return ('<div class="langs" role="group" data-i18n-aria="a11y.langgroup" aria-label="'+S("a11y.langgroup")+'">'
            '<button type="button" class="lang-btn" data-lang="en">EN</button>'
            '<button type="button" class="lang-btn" data-lang="fr">FR</button>'
            '<button type="button" class="lang-btn" data-lang="ar">AR</button></div>')

# ---------------- partials ----------------
def head(ctx, title, desc, canonical, page_extra=""):
    return f'''<!DOCTYPE html>
<html lang="en" data-scheme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="Younes Hebaiche">
<meta name="theme-color" content="#0A0C10">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="0xYurii">
<meta property="og:image" content="{SITE}/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}/img/og.png">
<link rel="icon" type="image/svg+xml" href="{ctx.favicon()}">
<link rel="apple-touch-icon" href="{ctx.a('img/apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
{ANALYTICS_SCRIPT}
{page_extra}
</head>
<body>
<script>
try{{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-scheme',t);
var l=localStorage.getItem('lang');if(!l){{var n=(navigator.language||'en').slice(0,2).toLowerCase();l=(n==='fr'||n==='ar')?n:'en';}}
document.documentElement.lang=l;document.documentElement.dir=(l==='ar'?'rtl':'ltr');}}catch(e){{}}
</script>
<a class="skip-link" href="#main" data-i18n="a11y.skip">Skip to content</a>'''

def header(ctx):
    navitems = [("work","nav.work"),("about","nav.about"),("skills","nav.skills"),("contact","nav.contact")]
    links = []
    for sec,key in navitems:
        href, extra = ctx.nav(sec)
        links.append(f'<a href="{href}"{extra} data-i18n="{key}">{S(key)}</a>')
    nav_links = "".join(links)
    return f'''<header class="site-head"><div class="wrap head-in">
<a class="brand" href="{ctx.home()}">0xYurii</a>
<div class="head-right">
<nav class="nav" id="nav">
{nav_links}
<a class="cv-btn" href="{ctx.cv()}" download>{ico('download')}<span data-i18n="nav.cv">{S("nav.cv")}</span></a>
{langs()}
<button class="icon-btn theme-toggle" id="theme-toggle" aria-label="Toggle theme">{ico('sun','ico-sun')}{ico('moon','ico-moon')}</button>
</nav>
<img class="avatar" src="{ctx.avatar()}" alt="Younes Hebaiche" width="38" height="38">
<button class="icon-btn menu-btn" id="menu-btn" aria-label="Menu" aria-expanded="false">{ico('menu')}</button>
</div></div></header>'''

def footer(ctx):
    return f'''<footer class="footer"><div class="wrap foot-in">
<p>© <span id="year">2026</span> Younes Hebaiche</p>
{social_row(ctx,'socials small')}
</div></footer>'''

def scripts(ctx):
    if ctx.target == "preview":
        return ("<script>window.__I18N__=" + I18N_JSON + ";</script>\n"
                "<script>\n" + JS + "\n</script>")
    return (f'<script src="{ctx.a("i18n.js")}"></script>\n'
            f'<script src="{ctx.a("script.js")}"></script>')

def page(ctx, head_html, main_html, extra_scripts=""):
    return (head_html + "\n" + sprite() + "\n" + header(ctx) + "\n" + main_html + "\n"
            + footer(ctx) + "\n" + scripts(ctx) + "\n" + extra_scripts + "\n</body>\n</html>\n")

# ---------------- home ----------------
def home_main(ctx):
    cards = []
    for p in PROJECTS:
        sl = p["slug"]
        cards.append(f'''<a class="card" href="{ctx.proj(sl)}">
<div class="card-cover"><img src="{ctx.cover(sl)}" alt="{esc(EN[sl+'.sub'])}" loading="lazy" width="1600" height="900"></div>
<div class="card-body">
<div class="card-head"><h3>{TITLE[sl]}</h3><span class="card-meta" data-i18n="{sl}.dates">{S(sl+'.dates')}</span></div>
<p class="card-role" data-i18n="{sl}.sub">{S(sl+'.sub')}</p>
<p class="card-desc" data-i18n="{sl}.hook">{S(sl+'.hook')}</p>
{tech_chips(p['tech']) if 'tech' in p else tech_chips(TECH[sl])}
<span class="card-cta"><span data-i18n="card.cta">{S('card.cta')}</span> {ico('arrow')}</span>
</div></a>''')
    cards_html = '<div class="cards">' + "\n".join(cards) + '</div>'

    skills = []
    for gkey, items in SKILL_GROUPS:
        skills.append(f'<div class="skill-group">{tspan(gkey,"h4")}{logo_grid(items)}</div>')
    skills_html = '<div class="skills-wrap">' + "\n".join(skills) + '</div>'

    work_href, work_extra = ctx.nav('work')
    return f'''<main id="main" data-view="home">
<section class="hero" id="top"><div class="wrap">
<p class="kicker"><span class="prompt">$</span> <span data-i18n="hero.kicker">{S('hero.kicker')}</span></p>
<h1>Younes Hebaiche</h1>
<p class="lede" data-i18n="hero.lede">{S('hero.lede')}</p>
<p class="sub" data-i18n="hero.sub">{S('hero.sub')}</p>
<div class="hero-actions">
<a class="btn btn-primary" href="{work_href}"{work_extra}><span data-i18n="hero.viewwork">{S('hero.viewwork')}</span> {ico('arrow')}</a>
<a class="btn btn-ghost" href="{ctx.cv()}" download>{ico('download')} <span data-i18n="btn.cv">{S('btn.cv')}</span></a>
</div>
{social_row(ctx)}
</div></section>

<section id="work" class="section"><div class="wrap">
<header class="sec-head"><span class="sec-num">01</span>{tspan('sec.work','h2')}<span class="rule"></span></header>
{cards_html}
</div></section>

<section id="about" class="section"><div class="wrap">
<header class="sec-head"><span class="sec-num">02</span>{tspan('sec.about','h2')}<span class="rule"></span></header>
<div class="prose">
<p data-i18n="about.p1">{S('about.p1')}</p>
<p data-i18n="about.p2">{S('about.p2')}</p>
<p data-i18n="about.p3">{S('about.p3')}</p>
</div>
</div></section>

<section id="skills" class="section"><div class="wrap">
<header class="sec-head"><span class="sec-num">03</span>{tspan('sec.skills','h2')}<span class="rule"></span></header>
{skills_html}
</div></section>

<section id="contact" class="section"><div class="wrap">
<header class="sec-head"><span class="sec-num">04</span>{tspan('sec.contact','h2')}<span class="rule"></span></header>
<p class="contact-lede" data-i18n="contact.lede">{S('contact.lede')}</p>
<p class="contact-sub" data-i18n="contact.sub">{S('contact.sub')}</p>
<div class="contact-actions">
<a class="btn btn-primary" href="mailto:y.hebaiche@esi-sba.dz">{ico('mail')} y.hebaiche@esi-sba.dz</a>
<button class="btn btn-ghost copy-btn" type="button" data-copy="y.hebaiche@esi-sba.dz">{ico('copy','ico-copy')}{ico('check','ico-check')} <span class="copy-label" data-i18n="contact.copy">{S('contact.copy')}</span></button>
<a class="btn btn-ghost" href="{ctx.cv()}" download>{ico('download')} <span data-i18n="btn.cv">{S('btn.cv')}</span></a>
</div>
{social_row(ctx)}
</div></section>
</main>'''

# tech per project (icons)
TECH = {
 "aegis":[('typescript','TypeScript'),('node','Node.js'),('redis','Redis'),('docker','Docker'),('jest','Jest'),('ghactions','GitHub Actions')],
 "wasselni":[('node','Node.js'),('express','Express'),('typescript','TypeScript'),('postgresql','PostgreSQL'),('prisma','Prisma')],
 "nodetalk":[('node','Node.js'),('express','Express'),('socketio','Socket.IO'),('postgresql','PostgreSQL'),('prisma','Prisma')],
 "mapreach":[('javascript','JavaScript'),('html5','HTML5'),('css','CSS')],
}
TITLE = {"aegis":"Aegis","wasselni":"Wasselni","nodetalk":"NodeTalk","mapreach":"MapReach"}

# ---------------- project detail ----------------
def project_main(ctx, p):
    sl = p["slug"]
    linkbits = []
    if p["links"].get("source"):
        linkbits.append(f'<a class="btn btn-primary" href="{p["links"]["source"]}" target="_blank" rel="noopener noreferrer">{ico("github")} <span data-i18n="detail.viewsource">{S("detail.viewsource")}</span> {ico("ext","ico-ext")}</a>')
    if not p["links"].get("source") and p.get("note"):
        linkbits.append(f'<p class="aside-note" data-i18n="{sl}.note">{S(sl+".note")}</p>')
    links_html = "".join(linkbits)

    overview = "".join(f'<p data-i18n="{sl}.ov.{i}">{S(f"{sl}.ov.{i}")}</p>' for i in range(len(p["overview"])))
    highlights = "".join(f'<li data-i18n="{sl}.hl.{i}">{S(f"{sl}.hl.{i}")}</li>' for i in range(len(p["highlights"])))
    diagram = ("\n" + DIAGRAM) if p.get("diagram") else ""
    cover_block = "" if p.get("diagram") else f'<div class="detail-cover"><img src="{ctx.cover(sl)}" alt="{esc(EN[sl+".sub"])}" width="1600" height="900"></div>'

    return f'''<main id="main" class="detail" data-view="{sl}">
<div class="wrap">
<a class="back" href="{ctx.home()}"{' data-nav="#work"' if ctx.target=='preview' else ''}>{ico('back')} <span data-i18n="detail.back">{S('detail.back')}</span></a>
<p class="kicker"><span class="sec-num">{p['num']:02d}</span> — <span data-i18n="{sl}.kicker">{S(sl+'.kicker')}</span></p>
<h1 class="detail-title">{TITLE[sl]}</h1>
<p class="detail-sub" data-i18n="{sl}.sub">{S(sl+'.sub')}</p>
<p class="detail-meta"><span data-i18n="{sl}.dates">{S(sl+'.dates')}</span> · <span data-i18n="{sl}.role">{S(sl+'.role')}</span></p>
{cover_block}
<div class="detail-grid">
<div class="detail-body">
{overview}
{tspan('detail.highlights','h3','block-h')}
<ul class="facts">{highlights}</ul>{diagram}
</div>
<aside class="detail-aside">
<div class="aside-block">{tspan('detail.tech','h4')}{logo_grid(TECH[sl],'logo-grid tight')}</div>
<div class="aside-block">{tspan('detail.links','h4')}{links_html}</div>
</aside>
</div>
</div>
</main>'''

# attach tech + finalize
for p in PROJECTS: p["tech"] = TECH[p["slug"]]

# ---------------- assets ----------------
CSS = open(os.path.join("tools","site.css")).read()
JS  = open(os.path.join("tools","site.js")).read()
I18N_JSON = json.dumps({"en":EN,"fr":FR,"ar":AR}, ensure_ascii=False)

# extra i18n strings used only by JS / a11y (register defaults so 'en' restore works)
EN.setdefault("a11y.skip","Skip to content"); FR.setdefault("a11y.skip","Aller au contenu"); AR.setdefault("a11y.skip","تخطٍّ إلى المحتوى")
I18N_JSON = json.dumps({"en":EN,"fr":FR,"ar":AR}, ensure_ascii=False)

# ---------------- emit ----------------
def write(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path,"w").write(content); print("wrote", path, len(content))

open("styles.css","w").write(CSS)
open("script.js","w").write(JS)
open("i18n.js","w").write("window.__I18N__=" + I18N_JSON + ";\n")

# index
ctx = Ctx("index")
h = head(ctx, "Younes Hebaiche — Backend Developer",
         "Backend developer and CS student at ESI-SBA. Node.js, TypeScript, PostgreSQL — API gateways, REST services, and the data layers underneath. Based in Chlef, Algeria.",
         SITE + "/", page_extra='<link rel="stylesheet" href="styles.css">')
write("index.html", page(ctx, h, home_main(ctx)))

# project pages
for p in PROJECTS:
    ctx = Ctx("proj")
    h = head(ctx, f"{TITLE[p['slug']]} — Younes Hebaiche", EN[p['slug']+'.hook'],
             f"{SITE}/projects/{p['slug']}.html", page_extra='<link rel="stylesheet" href="../styles.css">')
    write(f"projects/{p['slug']}.html", page(ctx, h, project_main(ctx, p)))

# ---------------- preview (single file, hash-routed) ----------------
def datauri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path,"rb").read()).decode()

assets = {"cover:"+p["slug"]: datauri(f"img/covers/{p['slug']}.jpg","image/jpeg") for p in PROJECTS}
assets["favicon"] = datauri("favicon.svg","image/svg+xml")
assets["avatar"]  = datauri("img/avatar.jpg","image/jpeg")

pv = Ctx("preview", assets=assets)
h = head(pv, "Younes Hebaiche — Backend Developer",
         "Backend developer and CS student at ESI-SBA. Node.js, TypeScript, PostgreSQL.",
         SITE + "/", page_extra="<style>\n"+CSS+"\n</style>")
bodies = home_main(pv) + "\n" + "\n".join(project_main(pv, p) for p in PROJECTS)
router = '''<script>
(function(){
  function route(){
    var h=(location.hash||'').replace(/^#\\/?/,'');
    var views=document.querySelectorAll('[data-view]'); var shown=false;
    views.forEach(function(v){var m=(v.getAttribute('data-view')===(h||'home'));v.hidden=!m;if(m)shown=true;});
    if(!shown){var hm=document.querySelector('[data-view="home"]');if(hm)hm.hidden=false;}
    window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',route); route();
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-nav]'); if(!a)return;
    e.preventDefault(); var t=a.getAttribute('data-nav');
    if(location.hash&&location.hash!=='#/'){location.hash='#/';}
    var hm=document.querySelector('[data-view="home"]'); if(hm)hm.hidden=false;
    document.querySelectorAll('[data-view]').forEach(function(v){if(v.getAttribute('data-view')!=='home')v.hidden=true;});
    setTimeout(function(){var el=document.querySelector(t);if(el)el.scrollIntoView({behavior:'smooth'});},30);
  });
})();
</script>'''
write("preview.html", page(pv, h, bodies, extra_scripts=router))
print("DONE")
