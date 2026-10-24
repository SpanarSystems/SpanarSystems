#!/usr/bin/env python3
"""Generates /solutions pages, sitemap.xml, robots.txt and the generated blocks in index.html.

Edit SALES_* below (set SALES_PHONE to show a phone number everywhere), then run:
    python3 tools/build_solutions.py
"""
import json, re, html, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from products_data import PRODUCTS
SITE = "https://www.spanarsystems.com"
SALES_EMAIL = "sales@spanarsystems.com"   # sales mailbox (same one Nova uses)
SALES_PHONE = "+91 74164 77658"           # call + WhatsApp; shown on every page, in schema and tel:/wa.me links
TODAY = date.today().isoformat()
e = html.escape

DOMAINS = [
 dict(slug="clinic-software", icon="✚", name="Clinic & Hospital Software",
  h1="Clinic management software that keeps every patient moving.",
  title="Clinic Management Software in India | Appointments, EMR, Billing | Spanar Systems",
  desc="Custom clinic and hospital management software: online appointments, electronic medical records, prescriptions, billing and WhatsApp reminders. Built by Spanar Systems, Hyderabad.",
  kw="clinic management software, hospital management software, EMR software India, doctor appointment app, clinic billing software, patient management system",
  lead="Appointments, patient records, prescriptions, billing and follow-ups in one calm workspace for clinics, diagnostic centres and small hospitals.",
  feats=[("Online appointments","Patients book slots by web or phone; reception sees the whole day at a glance."),("Electronic medical records","Visit history, vitals, diagnoses and attachments organised per patient."),("e-Prescriptions","Fast templates, drug search and printable or shareable prescriptions."),("Billing & insurance","Itemised invoices, packages, payments and outstanding balances."),("Reminders & follow-ups","Automated SMS/WhatsApp reminders reduce no-shows."),("Role-based access","Doctors, nurses and front desk see only what they need, with audit trail.")],
  mock=dict(app="ClinicOS", side=["Dashboard","Appointments","Patients","Prescriptions","Billing","Reports"],
   kpis=[("Today's visits","48"),("Waiting now","6"),("Revenue today","₹ 62,400"),("No-shows","3")],
   chart=("Visits this week",[38,45,52,41,48,30,22],["M","T","W","T","F","S","S"]),
   table=("Today's appointments",["Patient","Doctor","Time","Status"],[("Anita Rao","Dr. Mehta","10:00","In consult"),("Kiran Das","Dr. Iyer","10:15","Waiting"),("Sunil Verma","Dr. Mehta","10:30","Booked"),("Meena K.","Dr. Shah","10:45","Booked")]),
   phone=("Book appointment",[("Dr. Mehta · General","Today 4:30 PM"),("Dr. Iyer · Paediatrics","Tomorrow 11:00 AM"),("Dr. Shah · Dental","Fri 9:15 AM")],"Confirm booking")),
  faq=[("Can the software be customised for our clinic?","Yes. We configure workflows, forms, prescriptions templates and billing rules to match how your clinic works."),("Does it support multiple doctors and branches?","Yes. Multi-doctor scheduling and multi-branch reporting are part of the design."),("Is patient data secure?","We use role-based access, encrypted connections and audit logs, and design to your local data-protection requirements.")]),
 dict(slug="mobile-app-development", icon="▣", name="Mobile App Development",
  h1="Mobile apps people actually keep on their phones.",
  title="Mobile App Development Company in Hyderabad | Android & iOS | Spanar Systems",
  desc="Android, iOS and cross-platform mobile app development in Hyderabad. Product strategy, UI/UX, development, launch and support from Spanar Systems.",
  kw="mobile app development company Hyderabad, Android app development, iOS app development, cross platform app development, custom mobile app India, app development company",
  lead="From idea to App Store and Play Store: product thinking, design, engineering and long-term support for Android, iOS and cross-platform apps.",
  feats=[("Android & iOS","Native-quality apps for both stores, built with Flutter, React Native or native stacks as the product demands."),("UI/UX design","Clear flows, accessible interfaces and prototypes you can test before we build."),("Backend & APIs","Secure, scalable APIs, auth, payments, notifications and admin dashboards."),("AI features","Chat assistants, recommendations and automation woven into the experience."),("Launch & growth","Store listings, analytics, crash monitoring and release management."),("Maintenance","OS updates, performance tuning and new features after launch.")],
  mock=dict(app="Your App", side=["Overview","Users","Orders","Content","Push","Analytics"],
   kpis=[("Active users","12.4k"),("Sessions/day","31.8k"),("Crash-free","99.6%"),("Store rating","4.7★")],
   chart=("Daily active users",[8,9,11,10,12,14,13],["M","T","W","T","F","S","S"]),
   table=("Recent orders",["Order","Customer","Amount","Status"],[("#2041","Priya S.","₹ 1,299","Paid"),("#2040","Rahul M.","₹ 849","Shipped"),("#2039","Neha P.","₹ 2,150","Paid"),("#2038","Arjun T.","₹ 499","Refunded")]),
   phone=("Today",[("Welcome back, Priya","3 new offers"),("Order #2041","Out for delivery"),("Wishlist","5 items")],"Shop now")),
  faq=[("Do you build for both Android and iOS?","Yes. We build native or cross-platform apps and handle store submission for both."),("How long does an app take?","A focused first version typically takes 8–14 weeks depending on scope. We plan in short milestones with demos."),("Do you maintain the app after launch?","Yes, we offer support plans covering fixes, OS updates and feature releases.")]),
 dict(slug="security-services-software", icon="⛨", name="Security Services Software",
  h1="Run a security agency with live visibility, not paper registers.",
  title="Security Guard Management Software | Patrol, Attendance, Incidents | Spanar Systems",
  desc="Software for security agencies and facility teams: guard attendance, GPS patrol tracking, incident reports, shift rostering and client dashboards. By Spanar Systems.",
  kw="security guard management software, security agency software, guard patrol app, security services software India, guard attendance app, facility security management",
  lead="Guard rostering, geo-tagged attendance, checkpoint patrols and incident reporting with real-time dashboards for your clients and control room.",
  feats=[("Geo-tagged attendance","Selfie and location check-in prevents proxy attendance across sites."),("Patrol & checkpoints","QR/NFC checkpoints, route tracking and missed-round alerts."),("Incident reporting","Photos, severity and instant escalation to supervisors and clients."),("Shift rostering","Auto-build rosters, cover absences and manage overtime."),("Client portal","Clients see live site status, reports and SLA performance."),("Payroll-ready exports","Attendance data flows into wages and billing without re-keying.")],
  mock=dict(app="GuardView", side=["Live map","Sites","Guards","Patrols","Incidents","Reports"],
   kpis=[("Guards on duty","214"),("Sites live","38"),("Patrols done","96%"),("Open incidents","4")],
   chart=("Patrol completion",[91,94,92,97,96,95,96],["M","T","W","T","F","S","S"]),
   table=("Live site status",["Site","Guards","Last patrol","Status"],[("Orion Mall","12","2 min ago","OK"),("Tech Park B","18","6 min ago","OK"),("Warehouse 4","5","41 min ago","Alert"),("Skyline Apts","9","9 min ago","OK")]),
   phone=("Patrol round",[("Gate 1","Scanned 10:02"),("Parking B2","Scanned 10:14"),("Server room","Pending")],"Report incident")),
  faq=[("Is this cybersecurity or physical security?","This solution is for physical security agencies and facility teams. We also build secure software with strong auth, encryption and audit trails."),("Can clients get their own login?","Yes. Clients can have a read-only portal with live status and reports."),("Does it work offline at remote sites?","Check-ins and reports can be queued offline and synced when connectivity returns.")]),
 dict(slug="ca-accounting-software", icon="₹", name="CA & Accounting Firm Software",
  h1="Practice management built for Chartered Accountants.",
  title="CA Practice Management Software | GST, ITR, Client Portal | Spanar Systems",
  desc="Practice management software for CA and accounting firms: client onboarding, GST and ITR due-date tracking, document collection, task assignment and billing. Spanar Systems.",
  kw="CA practice management software, accounting firm software India, GST filing tracker, ITR client management, CA client portal, chartered accountant software",
  lead="Track every client, filing and deadline. Collect documents securely, assign work to your team and bill with confidence.",
  feats=[("Compliance calendar","GST, TDS, ITR and ROC due dates tracked per client with reminders."),("Document collection","Clients upload via a secure link; staff see what is pending."),("Task & team workflow","Assign, review and sign off work with a clear audit trail."),("Client portal","Clients see filing status, invoices and shared documents."),("Time & billing","Track effort, raise invoices and follow up on dues."),("Reports","Partner-level view of workload, realisation and overdue filings.")],
  mock=dict(app="PracticeDesk", side=["Dashboard","Clients","Compliance","Documents","Tasks","Billing"],
   kpis=[("Active clients","182"),("Due this week","27"),("Docs pending","41"),("Outstanding","₹ 4.2 L")],
   chart=("Filings completed",[12,18,25,31,22,14,9],["M","T","W","T","F","S","S"]),
   table=("Upcoming deadlines",["Client","Filing","Due","Owner"],[("Sharma Traders","GSTR-3B","20 Nov","Ravi"),("Nova Pharma","TDS 26Q","31 Oct","Asha"),("K. Reddy","ITR-3","31 Jul","Ravi"),("Bright Edu","ROC AOC-4","29 Nov","Isha")]),
   phone=("Upload documents",[("Bank statement","Received"),("Purchase invoices","Pending"),("Form 16","Received")],"Upload file")),
  faq=[("Does it file returns directly?","It manages tracking, documents, tasks and billing. Filing continues through the government portals you already use; integrations can be scoped."),("Can clients upload documents securely?","Yes, through private links with access control and logs."),("Can it be tailored to our firm?","Yes. We configure compliance types, workflows and invoice formats.")]),
 dict(slug="education-software", icon="✎", name="School & Coaching Software",
  h1="Run schools and coaching centres without the admin chaos.",
  title="School & Coaching Institute Management Software | Spanar Systems",
  desc="School ERP and coaching centre software: admissions, attendance, fee collection, timetables, exams and parent app. Custom built by Spanar Systems, Hyderabad.",
  kw="school management software, coaching institute software, school ERP India, fee management software, student attendance app, parent app school",
  lead="Admissions, attendance, fees, timetables, results and parent communication in one platform with web and mobile access.",
  feats=[("Admissions CRM","Capture enquiries, schedule visits and convert to admissions."),("Attendance","Class and biometric/QR attendance with instant parent alerts."),("Fee management","Instalments, receipts, reminders and online payments."),("Exams & results","Mark entry, report cards and performance analytics."),("Timetable","Conflict-free scheduling for teachers, rooms and batches."),("Parent & student app","Homework, notices, fees and results on mobile.")],
  mock=dict(app="CampusHub", side=["Dashboard","Students","Attendance","Fees","Exams","Notices"],
   kpis=[("Students","1,248"),("Present today","94%"),("Fees collected","₹ 8.6 L"),("Dues","₹ 1.9 L")],
   chart=("Attendance this week",[93,95,94,92,96,88,0],["M","T","W","T","F","S","S"]),
   table=("Fee dues",["Student","Class","Due","Status"],[("Aarav N.","8-B","₹ 12,000","Overdue"),("Diya R.","6-A","₹ 8,500","Due soon"),("Kabir S.","10-C","₹ 15,000","Paid"),("Isha V.","9-A","₹ 12,000","Due soon")]),
   phone=("Parent view",[("Attendance","Present today"),("Homework","Maths ch.5"),("Fee due","₹ 8,500")],"Pay fees")),
  faq=[("Is there a parent mobile app?","Yes, parents can view attendance, homework, notices and pay fees."),("Can it handle multiple branches?","Yes, with branch-wise and consolidated reporting."),("Can you migrate our existing data?","We can import student, fee and staff data from spreadsheets.")]),
 dict(slug="retail-pos-software", icon="▤", name="Retail, POS & Inventory",
  h1="Billing, stock and customers in one fast retail system.",
  title="Retail POS & Inventory Management Software | GST Billing | Spanar Systems",
  desc="POS and inventory software for shops and retail chains: GST billing, barcode scanning, stock alerts, multi-store reports and loyalty. Custom built by Spanar Systems.",
  kw="retail POS software India, inventory management software, GST billing software, barcode billing, multi store retail software, shop management app",
  lead="Fast billing, real-time stock, supplier purchasing and customer loyalty across one store or many.",
  feats=[("GST billing","Quick invoices with taxes, discounts and returns."),("Inventory control","Batch, expiry and low-stock alerts across locations."),("Barcode & scanner","Hardware-friendly billing at the counter."),("Purchasing","Supplier orders, goods receipt and payables."),("Loyalty & CRM","Customer history, offers and repeat-purchase insights."),("Multi-store reports","Sales, margin and stock by store, product and day.")],
  mock=dict(app="StoreFlow", side=["Dashboard","Billing","Inventory","Purchases","Customers","Reports"],
   kpis=[("Sales today","₹ 1.8 L"),("Bills","236"),("Low stock","14"),("Margin","21%")],
   chart=("Sales this week (₹ k)",[140,165,152,180,210,260,190],["M","T","W","T","F","S","S"]),
   table=("Low stock items",["Item","SKU","Stock","Reorder"],[("Basmati 5kg","BR-005","6","40"),("Olive oil 1L","OL-001","4","24"),("Green tea","GT-120","9","30"),("Notebook A4","NB-044","12","50")]),
   phone=("Quick bill",[("Basmati 5kg x2","₹ 1,240"),("Green tea x1","₹ 210"),("GST 5%","₹ 72")],"Collect ₹ 1,522")),
  faq=[("Does it work with barcode scanners and printers?","Yes. We support common scanners and receipt printers."),("Can I manage multiple stores?","Yes, with centralised stock and store-wise reporting."),("Does it support GST invoices?","Yes, GST-ready invoicing is core to the design.")]),
 dict(slug="real-estate-crm", icon="⌂", name="Real Estate CRM",
  h1="Turn property enquiries into site visits and closings.",
  title="Real Estate CRM Software for Builders & Brokers | Spanar Systems",
  desc="Real estate CRM for builders, brokers and agencies: lead capture, site-visit scheduling, inventory, payment plans and follow-up automation. By Spanar Systems.",
  kw="real estate CRM India, builder CRM software, property management software, broker lead management, site visit scheduling app, real estate software Hyderabad",
  lead="Capture leads from every channel, schedule site visits, manage unit inventory and payment schedules in one pipeline.",
  feats=[("Lead capture","Web, portals, WhatsApp and campaigns flow into one inbox."),("Pipeline & follow-ups","Never lose a lead with reminders and stage tracking."),("Unit inventory","Live availability, pricing and booking holds."),("Site visits","Schedule, remind and capture visit feedback."),("Payment schedules","Demand letters, instalments and collections tracking."),("Channel partners","Brokers see their leads, commissions and status.")],
  mock=dict(app="EstateDesk", side=["Pipeline","Leads","Inventory","Site visits","Payments","Partners"],
   kpis=[("New leads","64"),("Visits booked","18"),("Units available","112"),("Collections","₹ 3.4 Cr")],
   chart=("Leads this week",[44,52,61,58,64,72,40],["M","T","W","T","F","S","S"]),
   table=("Hot leads",["Lead","Project","Budget","Stage"],[("R. Kulkarni","Lakeview 3BHK","₹ 1.1 Cr","Visit set"),("S. Jain","Greens 2BHK","₹ 78 L","Negotiation"),("M. Fatima","Lakeview 2BHK","₹ 85 L","New"),("P. Nair","Plot 40","₹ 62 L","Follow-up")]),
   phone=("Today's visits",[("11:00 · R. Kulkarni","Lakeview"),("2:30 · S. Jain","Greens"),("5:00 · P. Nair","Plot 40")],"Navigate")),
  faq=[("Can brokers and partners log in?","Yes, with limited access to their own leads and commissions."),("Does it integrate with property portals?","Lead imports from portals and ad platforms can be integrated."),("Can it track payment schedules?","Yes, including demand letters and collection status.")]),
 dict(slug="logistics-fleet-software", icon="➜", name="Logistics & Fleet Software",
  h1="See every vehicle, delivery and proof of delivery live.",
  title="Logistics & Fleet Management Software | Tracking, Dispatch | Spanar Systems",
  desc="Fleet and logistics software: live vehicle tracking, route planning, driver app, proof of delivery and trip costing. Custom built by Spanar Systems, Hyderabad.",
  kw="fleet management software India, logistics software, vehicle tracking system, delivery management app, transport management system, proof of delivery app",
  lead="Dispatch, route planning, driver app, proof of delivery and trip costing with live visibility across your fleet.",
  feats=[("Live tracking","Vehicle location, ETA and exceptions on one map."),("Dispatch & routes","Assign loads and plan efficient routes."),("Driver app","Trips, navigation, status updates and e-POD."),("Proof of delivery","Photo, signature and OTP confirmation."),("Trip costing","Fuel, tolls and expenses per trip and vehicle."),("Customer tracking links","Share live status with consignees automatically.")],
  mock=dict(app="FleetPulse", side=["Live map","Trips","Vehicles","Drivers","Billing","Reports"],
   kpis=[("Vehicles live","86"),("Deliveries today","412"),("On-time","93%"),("Delayed","9")],
   chart=("Deliveries this week",[320,355,390,402,412,280,150],["M","T","W","T","F","S","S"]),
   table=("Active trips",["Trip","Driver","ETA","Status"],[("TR-8812","Ramesh","14:20","On route"),("TR-8813","Imran","15:05","Delayed"),("TR-8814","Suresh","13:50","Delivered"),("TR-8815","Kumar","16:30","On route")]),
   phone=("Trip TR-8812",[("Pickup · Hyderabad","Done"),("Stop 2 · Warangal","ETA 14:20"),("Drop · Karimnagar","Pending")],"Capture POD")),
  faq=[("Do you use GPS hardware?","We integrate with common GPS devices and also support smartphone-based tracking."),("Is there a driver mobile app?","Yes, with trip updates, navigation links and proof of delivery."),("Can customers track their delivery?","Yes, via shareable live tracking links.")]),
]

CSS_NAV = '<nav class="nav"><a class="brand brand-logo" href="../index.html" aria-label="Spanar Systems home"><img src="../assets/img/spanar-logo-official.png" alt="Spanar Systems"></a><div class="links"><a href="../products/">AI products</a><a href="../solutions/">Solutions</a><a href="../index.html#contact">Contact</a><button class="theme-toggle" id="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false"><span class="theme-track"><span class="theme-icon sun">☀</span><span class="theme-icon moon">☾</span><span class="theme-thumb"></span></span></button><a class="pill primary" href="../index.html#contact">Get a demo ↗</a></div></nav>'

def phone_html(prefix=""):
    if not SALES_PHONE: return ""
    tel = re.sub(r"[^\d+]", "", SALES_PHONE)
    wa = tel.lstrip("+")
    return f'<a href="tel:{tel}">{e(SALES_PHONE)}</a> <a class="wa" href="https://wa.me/{wa}" rel="noopener">WhatsApp</a>'

def mailto(subject):
    return f"mailto:{SALES_EMAIL}?subject={subject.replace(' ', '%20').replace('&', 'and')}"

def mock_desktop(m):
    mx = max(m["chart"][1]) or 1
    bars = "".join(f'<div class="bar" style="height:{max(4, round(v/mx*100))}%"><i>{l}</i></div>' for v, l in zip(m["chart"][1], m["chart"][2]))
    kpis = "".join(f'<div class="kpi"><small>{e(k)}</small><b>{e(v)}</b></div>' for k, v in m["kpis"])
    side = "".join(f'<li class="{"on" if i == 0 else ""}">{e(s)}</li>' for i, s in enumerate(m["side"]))
    t = m["table"]
    th = "".join(f"<th>{e(c)}</th>" for c in t[1])
    rows = "".join("<tr>" + "".join(f'<td>{e(c)}</td>' for c in r) + "</tr>" for r in t[2])
    return f'''<figure class="shot desk" aria-label="Sample {e(m["app"])} dashboard screenshot"><div class="shot-bar"><i></i><i></i><i></i><span>{e(m["app"])} · Sample screen</span></div><div class="shot-body"><aside><div class="shot-logo">{e(m["app"])}</div><ul>{side}</ul></aside><section><div class="kpis">{kpis}</div><div class="shot-grid"><div class="panel"><h4>{e(m["chart"][0])}</h4><div class="bars">{bars}</div></div><div class="panel"><h4>{e(t[0])}</h4><table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div></div></section></div><figcaption>Illustrative sample screen with dummy data.</figcaption></figure>'''

def mock_phone(m):
    title, items, cta = m["phone"]
    li = "".join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in items)
    return f'''<figure class="shot phone" aria-label="Sample {e(m["app"])} mobile screenshot"><div class="phone-frame"><div class="notch"></div><div class="phone-head">{e(m["app"])}</div><h4>{e(title)}</h4><ul>{li}</ul><button type="button" tabindex="-1">{e(cta)}</button></div><figcaption>Sample mobile view.</figcaption></figure>'''

def head(title, desc, kw, path, jsonld, depth="../"):
    url = f"{SITE}/{path}"
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="keywords" content="{e(kw)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="theme-color" content="#f6f8fb">
<link rel="canonical" href="{url}"><link rel="icon" type="image/svg+xml" href="{depth}assets/img/spanar-favicon.svg?v=4"><link rel="icon" type="image/png" sizes="32x32" href="{depth}assets/img/favicon.png?v=4"><link rel="icon" href="{depth}favicon.ico?v=4" sizes="48x48"><link rel="apple-touch-icon" href="{depth}assets/img/apple-touch-icon.png?v=4">
<meta property="og:type" content="website"><meta property="og:site_name" content="Spanar Systems"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/spanar-logo-official.png">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<link rel="stylesheet" href="{depth}assets/css/spanar-next.css"><link rel="stylesheet" href="{depth}assets/css/spanar-solutions.css">
<script>(()=>{{try{{if(localStorage.getItem('spanar-theme')==='dark')document.documentElement.dataset.theme='dark'}}catch(e){{}}}})()</script>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script></head>'''

def contact_strip(subject):
    ph = phone_html()
    return f'<section><div class="wrap"><div class="card cta-strip reveal"><div><div class="eyebrow">Talk to our sales team</div><h2>Want to see this built for your business?</h2><p>Tell us about your requirement. We respond within one business day.</p></div><div class="cta-actions"><a class="pill primary" href="{mailto(subject)}">Email sales ↗</a>{(" " + ph) if ph else ""}<span class="cta-mail">{e(SALES_EMAIL)}</span></div></div></div></section>'

def foot():
    ph = phone_html()
    return f'<footer><div class="wrap foot"><span>© <span data-year></span> Spanar Systems Private Limited · Hyderabad, India</span><span><a href="../privacy.html">Privacy</a> · <a href="../solutions/">Solutions</a> · <a href="mailto:{SALES_EMAIL}">{SALES_EMAIL}</a>{(" · " + ph) if ph else ""}</span></div></footer>'

def org_ld():
    cp = {"@type": "ContactPoint", "contactType": "sales", "email": SALES_EMAIL, "areaServed": "IN", "availableLanguage": ["English", "Hindi", "Telugu"]}
    if SALES_PHONE: cp["telephone"] = SALES_PHONE
    return {"@type": "Organization", "@id": SITE + "/#org", "name": "Spanar Systems Private Limited", "alternateName": "Spanar Systems", "url": SITE + "/", "logo": SITE + "/assets/img/spanar-logo-official.png", "email": SALES_EMAIL, "address": {"@type": "PostalAddress", "addressLocality": "Hyderabad", "addressRegion": "Telangana", "addressCountry": "IN"}, "contactPoint": [cp], "sameAs": ["https://github.com/SpanarSystems"]}

def build_page(d):
    path = f"solutions/{d['slug']}.html"
    url = f"{SITE}/{path}"
    ld = {"@context": "https://schema.org", "@graph": [
        org_ld(),
        {"@type": "Service", "name": d["name"], "serviceType": d["name"], "description": d["desc"], "url": url, "provider": {"@id": SITE + "/#org"}, "areaServed": [{"@type": "Country", "name": "India"}], "availableChannel": {"@type": "ServiceChannel", "serviceUrl": url}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Solutions", "item": SITE + "/solutions/"}, {"@type": "ListItem", "position": 3, "name": d["name"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}]}
    feats = "".join(f'<article class="card feature reveal"><span class="tag">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></article>' for i, (t, p) in enumerate(d["feats"]))
    faq = "".join(f'<details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    others = "".join(f'<a class="chip" href="{o["slug"]}.html">{e(o["name"])}</a>' for o in DOMAINS if o is not d)
    body = f'''<body>{CSS_NAV}<main><header class="product-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="./">Solutions</a> / {e(d["name"])}</nav><div class="eyebrow">{e(d["name"])} · Hyderabad, India</div><h1>{e(d["h1"])}</h1><p class="lead">{e(d["lead"])}</p><div class="actions"><a class="pill primary" href="{mailto("Demo request: " + d["name"])}">Request a demo ↗</a><a class="pill" href="#preview">See sample screens ↓</a></div></div></header>
<section id="preview"><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">Sample screens</div><h2>A look at the software.</h2></div><p>These are illustrative screens with dummy data, showing the kind of interface we build. Every project is tailored to your workflow.</p></div><div class="shots reveal">{mock_desktop(d["mock"])}{mock_phone(d["mock"])}</div></div></section>
<section><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">What you get</div><h2>Built around your workflow.</h2></div><p>{e(d["name"])} from Spanar Systems is custom built or configured to your needs, with web and mobile access and ongoing support.</p></div><div class="feature-grid">{feats}</div></div></section>
<section><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">FAQ</div><h2>Common questions.</h2></div></div><div class="faq reveal">{faq}</div></div></section>
{contact_strip("Demo request: " + d["name"])}
<section><div class="wrap"><div class="eyebrow">More solutions</div><div class="chips">{others}</div></div></section></main>{foot()}<script src="../assets/js/spanar-next.js"></script></body></html>'''
    (ROOT / path).write_text(head(d["title"], d["desc"], d["kw"], path, ld) + body)

def build_hub():
    title = "Software Solutions for Clinics, Security, CA Firms, Retail & More | Spanar Systems"
    desc = "Custom software and mobile apps for clinics, security agencies, CA firms, schools, retail, real estate and logistics. Built in Hyderabad by Spanar Systems."
    kw = "software development company Hyderabad, custom software India, clinic software, security agency software, CA software, mobile app development, business software solutions"
    ld = {"@context": "https://schema.org", "@graph": [org_ld(), {"@type": "CollectionPage", "name": "Spanar Systems Solutions", "url": SITE + "/solutions/", "hasPart": [{"@type": "Service", "name": d["name"], "url": f"{SITE}/solutions/{d['slug']}.html"} for d in DOMAINS]}, {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Solutions", "item": SITE + "/solutions/"}]}]}
    cards = "".join(f'<a class="card sol-card reveal" href="{d["slug"]}.html"><span class="sol-icon">{d["icon"]}</span><h3>{e(d["name"])}</h3><p>{e(d["lead"])}</p><span class="more">View solution →</span></a>' for d in DOMAINS)
    body = f'''<body>{CSS_NAV}<main><header class="product-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Solutions</nav><div class="eyebrow">Solutions by industry</div><h1>Software for the way your industry works.</h1><p class="lead">Clinics, security agencies, CA firms, schools, retail, real estate, logistics and mobile apps. Pick your domain and see sample screens.</p></div></header><section><div class="wrap"><div class="sol-grid">{cards}</div></div></section>{contact_strip("Enquiry: Spanar solutions")}</main>{foot()}<script src="../assets/js/spanar-next.js"></script></body></html>'''
    (ROOT / "solutions/index.html").write_text(head(title, desc, kw, "solutions/", ld) + body)

def wa_link(text):
    if not SALES_PHONE: return ""
    return "https://wa.me/" + re.sub(r"\D", "", SALES_PHONE) + "?text=" + text.replace(" ", "%20")

def product_cards(prefix):
    return "".join(f'<a class="card sol-card reveal" href="{prefix}products/{p["slug"]}.html"><span class="sol-top"><span class="sol-icon">{p["icon"]}</span><span class="tag">{e(p["status"])}</span></span><h3>{e(p["name"])}</h3><small class="cat">{e(p["cat"])}</small><p>{e(p["tagline"])}</p><span class="more">See sample screens →</span></a>' for p in PRODUCTS)

def build_product(pr):
    path = f"products/{pr['slug']}.html"; url = f"{SITE}/{path}"
    ld = {"@context": "https://schema.org", "@graph": [org_ld(),
        {"@type": "SoftwareApplication", "name": pr["name"], "applicationCategory": "BusinessApplication", "description": pr["desc"], "url": url, "creator": {"@id": SITE + "/#org"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "AI products", "item": SITE + "/products/"}, {"@type": "ListItem", "position": 3, "name": pr["name"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pr["faq"]]}]}
    feats = "".join(f'<article class="card feature reveal"><span class="tag">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></article>' for i, (t, p) in enumerate(pr["feats"]))
    faq = "".join(f'<details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in pr["faq"])
    others = "".join(f'<a class="chip" href="{o["slug"]}.html">{e(o["name"])}</a>' for o in PRODUCTS if o is not pr)
    note = "we can build a tailored version for your business now." if pr["status"] == "Concept" else "talk to us for early access or a tailored build."
    body = f'''<body>{CSS_NAV}<main><header class="product-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="./">AI products</a> / {e(pr["name"])}</nav><div class="eyebrow">{e(pr["cat"])}</div><h1>{e(pr["name"])}<span class="gradient">.</span></h1><p class="status-line"><span class="pill">{e(pr["status"])}</span> <strong>{e(pr["tagline"])}</strong></p><p class="lead">{e(pr["lead"])}</p><div class="actions"><a class="pill primary" href="#talk">Get a demo or early access ↗</a><a class="pill" href="#preview">See sample screens ↓</a></div></div></header>
<section id="preview"><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">Sample screens</div><h2>See the interface.</h2></div><p>Illustrative screens with dummy data to show the direction. Final designs are tailored to your workflow.</p></div><div class="shots reveal">{mock_desktop(pr["mock"])}{mock_phone(pr["mock"])}</div></div></section>
<section><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">Capabilities</div><h2>What {e(pr["name"])} does.</h2></div><p>{e(pr["status"])}: {note}</p></div><div class="feature-grid">{feats}</div></div></section>
<section><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">FAQ</div><h2>Common questions.</h2></div></div><div class="faq reveal">{faq}</div></div></section>
<span id="talk"></span>{contact_strip("Demo request: " + pr["name"])}
<section><div class="wrap"><div class="eyebrow">More AI products</div><div class="chips">{others}</div></div></section></main>{foot()}<script src="../assets/js/spanar-next.js"></script></body></html>'''
    (ROOT / path).write_text(head(pr["title"], pr["desc"], pr["kw"], path, ld) + body)

def build_products_hub():
    title = "AI Products & Software by Spanar Systems | Velocity, AalayApp, Travai, Scribe & more"
    desc = "Explore Spanar Systems AI products: Velocity, AalayApp, Travai and concepts like Scribe, Sentinel, Ledger, Concierge, Tutor and Route. See sample screens and talk to sales."
    kw = "AI products India, AI software company Hyderabad, AI SaaS, AI assistant for business, AI clinic software, AI for CA firms, AI travel planner, temple app"
    ld = {"@context": "https://schema.org", "@graph": [org_ld(), {"@type": "CollectionPage", "name": "Spanar Systems AI products", "url": SITE + "/products/", "hasPart": [{"@type": "SoftwareApplication", "name": p["name"], "url": f"{SITE}/products/{p['slug']}.html"} for p in PRODUCTS]}]}
    body = f'<body>{CSS_NAV}<main><header class="product-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / AI products</nav><div class="eyebrow">AI products</div><h1>AI software for how business really works.</h1><p class="lead">Products in development and concepts we can build for you now. Each has sample screens and a clear next step.</p></div></header><section><div class="wrap"><div class="sol-grid">{product_cards("../")}</div></div></section>{contact_strip("Enquiry: AI products")}</main>{foot()}<script src="../assets/js/spanar-next.js"></script></body></html>'
    (ROOT / "products/index.html").write_text(head(title, desc, kw, "products/", ld) + body)

def build_temple_redirect():
    (ROOT / "products/temple.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Temple is now AalayApp | Spanar Systems</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/products/aalay.html"><meta http-equiv="refresh" content="0; url=aalay.html"></head><body><p>Temple is now <a href="aalay.html">AalayApp</a>.</p></body></html>')

LOADER = '<div id="ai-loader" class="ai-loader" aria-label="Spanar Systems launching"><div class="launch-terminal"><div class="launch-kicker">SPANAR / SYSTEM BOOT</div><div class="launch-type"><span id="launch-brand"></span><i></i></div><div class="launch-status" id="launch-status">initializing intelligence...</div><div class="launch-progress"><span></span></div></div></div>'
SPARK = '<button class="spark-fab" id="spark-fab" aria-label="Open SPARK AI companion"><span>✦</span></button><aside class="spark-panel" id="spark-panel" aria-hidden="true"><div class="spark-head"><div><small>SPANAR AI AMBASSADOR</small><strong>SPARK</strong></div><button id="close-spark" aria-label="Close">×</button></div><div class="spark-body"><div class="spark-message">Hi. I’m SPARK. Ask me about our AI products and software, or talk to our sales team.</div><button data-answer="Velocity is our AI-native multi-tenant SaaS platform, currently in development.">What is Velocity?</button><button data-answer="AalayApp is our bilingual English and Telugu spiritual hub with temple guides, maps and more, on Android and web.">What is AalayApp?</button><button data-answer="We have in-development products (Velocity, AalayApp, Travai) and AI concepts we can build for you now: Scribe, Sentinel, Ledger, Concierge, Tutor, Route, Relay and Prism.">Which AI products do you have?</button><button data-answer="Email SALES_EMAIL_X or call or WhatsApp SALES_PHONE_X. We reply within one business day.">Talk to sales</button><div class="spark-answer" id="spark-answer">Choose a question and I’ll guide you.</div></div></aside>'

def build_index():
    title = "Spanar Systems | AI Software, Mobile Apps & Custom Software in Hyderabad"
    desc = "Spanar Systems builds AI-native products and custom software for clinics, security agencies, CA firms, schools, retail, real estate and logistics. Mobile apps too. Get a free demo."
    kw = "AI software company Hyderabad, custom software development India, mobile app development Hyderabad, clinic management software, security agency software, CA practice software, AI chatbot for business, AI products"
    ph = phone_html(); tel = re.sub(r"[^\d+]", "", SALES_PHONE); digits = re.sub(r"\D", "", SALES_PHONE)
    ld = {"@context": "https://schema.org", "@graph": [org_ld(), {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Spanar Systems", "publisher": {"@id": SITE + "/#org"}},
        {"@type": "ItemList", "name": "Spanar AI products", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["name"], "url": f"{SITE}/products/{p['slug']}.html"} for i, p in enumerate(PRODUCTS)]},
        {"@type": "ItemList", "name": "Spanar solutions", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": d["name"], "url": f"{SITE}/solutions/{d['slug']}.html"} for i, d in enumerate(DOMAINS)]}]}
    opts = "".join(f"<option>{e(d['name'])}</option>" for d in DOMAINS) + "".join(f"<option>{e(p['name'])} (AI)</option>" for p in PRODUCTS) + "<option>Something else</option>"
    sol_cards = "".join(f'<a class="card sol-card reveal" href="solutions/{d["slug"]}.html"><span class="sol-icon">{d["icon"]}</span><h3>{e(d["name"])}</h3><p>{e(d["lead"])}</p><span class="more">See sample screens →</span></a>' for d in DOMAINS)
    steps = [("Talk","A free 30-minute call to understand your workflow and goals."),("Design","Clickable screens in days, so you see it before we build it."),("Build","Short sprints with a working demo every week."),("Launch & support","Go-live, training and ongoing improvements.")]
    steps_html = "".join(f'<div class="step reveal"><b>{i+1:02d}</b><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps))
    wa = wa_link("Hi Spanar Systems, I would like a demo.")
    hero_calls = (f'<a class="pill big" href="tel:{tel}">Call {e(SALES_PHONE)}</a><a class="pill big wa-pill" href="{wa}" rel="noopener">WhatsApp</a>') if SALES_PHONE else ""
    mobile_bar = f'<div class="mobile-bar"><a href="tel:{tel}">Call</a><a href="{wa}" rel="noopener">WhatsApp</a><a class="p" href="#contact">Free demo</a></div>' if SALES_PHONE else ""
    contact_ph = f'<li><span>Call or WhatsApp</span>{ph}</li>' if ph else ""
    foot_ph = (" · " + ph) if ph else ""
    spark = SPARK.replace("SALES_EMAIL_X", SALES_EMAIL).replace("SALES_PHONE_X", SALES_PHONE)
    body = f'''
<body>{LOADER}<nav class="nav"><a class="brand brand-logo" href="#top" aria-label="Spanar Systems home"><img src="assets/img/spanar-logo-official.png" alt="Spanar Systems"></a><div class="links"><a href="#products">AI products</a><a href="#solutions">Solutions</a><a href="#process">Process</a><a href="#contact">Contact</a><button class="theme-toggle" id="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false"><span class="theme-track"><span class="theme-icon sun">☀</span><span class="theme-icon moon">☾</span><span class="theme-thumb"></span></span></button><a class="pill call" href="tel:{tel}">Call</a><a class="pill primary" href="#contact">Get a free demo ↗</a></div></nav>
<main id="top"><header class="hero"><div class="wrap hero-grid"><div><div class="eyebrow">AI-native products · Hyderabad, India</div><h1>Software that runs<br>your business <span class="gradient">with AI.</span></h1><p class="lead">We design and build AI-powered software and mobile apps for clinics, security agencies, CA firms, schools, retail, real estate and logistics. See a working demo in days, not months.</p><div class="actions"><a class="pill primary big" href="#contact">Get a free demo ↗</a>{hero_calls}</div><ul class="trust"><li>Free demo and consultation</li><li>Reply within one business day</li><li>Built in Hyderabad</li></ul></div><div class="hero-visual">{mock_desktop(PRODUCTS[0]["mock"])}</div></div></header>
<div class="marquee"><div class="marquee-track">CLINICS <b>✦</b> SECURITY <b>✦</b> CA FIRMS <b>✦</b> SCHOOLS <b>✦</b> RETAIL <b>✦</b> REAL ESTATE <b>✦</b> LOGISTICS <b>✦</b> MOBILE APPS <b>✦</b> CLINICS <b>✦</b> SECURITY <b>✦</b> CA FIRMS <b>✦</b> SCHOOLS <b>✦</b> RETAIL <b>✦</b> REAL ESTATE <b>✦</b> LOGISTICS <b>✦</b> MOBILE APPS <b>✦</b></div></div>
<section id="products"><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">AI products</div><h2>AI software, ready to shape for you.</h2></div><p>Three products are in development and eight are concepts we can build for your business now. Every one has sample screens so you can picture it running in your company. <a href="products/">View all →</a></p></div><div class="sol-grid">{product_cards("")}</div></div></section>
<section id="solutions"><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">Software &amp; services</div><h2>Built for your industry.</h2></div><p>Custom software and mobile apps, designed around how your business works. Explore each solution and its sample screens.</p></div><div class="sol-grid">{sol_cards}</div></div></section>
<section id="intelligence"><div class="wrap"><div class="card ai-panel reveal"><div><div class="eyebrow">AI, without the theatre</div><h2 style="font-size:clamp(2.8rem,5vw,5.5rem);line-height:.95;letter-spacing:-.06em;margin:16px 0">Useful intelligence lives inside the workflow.</h2><p class="lead">We design AI around decisions: understand context, reduce repetitive work, suggest the next useful action and keep humans in control.</p></div><div class="console"><div class="console-top"><i class="dot"></i><i class="dot"></i><i class="dot"></i></div><div class="console-line"><strong>context</strong> → tenant + role + intent</div><div class="console-line"><strong>reason</strong> → retrieve + evaluate + explain</div><div class="console-line"><strong>assist</strong> → suggest next best action</div><div class="console-line"><strong>guardrail</strong> → permissions + audit + confirmation</div><div class="console-line"><strong>learn</strong> → feedback without losing control</div></div></div></div></section>
<section id="process"><div class="wrap"><div class="section-head reveal"><div><div class="eyebrow">How we work</div><h2>From first call to live software.</h2></div><p>A simple, transparent process with a working demo at every stage.</p></div><div class="steps">{steps_html}</div></div></section>
<section id="contact"><div class="wrap"><div class="card contact-card contact-big reveal"><div><div class="eyebrow">Talk to our sales team</div><h2>Tell us what you need. See a demo this week.</h2><p class="lead">Share your business and requirement. We reply within one business day, usually sooner.</p><ul class="contact-list"><li><span>Sales email</span><a href="{mailto("Enquiry: Spanar Systems")}">{e(SALES_EMAIL)}</a></li>{contact_ph}<li><span>Location</span>Hyderabad, Telangana, India</li></ul></div><form id="lead-form" class="lead-form" novalidate><label>Your name<input name="name" autocomplete="name" required></label><label>Phone or WhatsApp<input name="phone" type="tel" autocomplete="tel"></label><label>I am interested in<select name="interest">{opts}</select></label><label>Your requirement<textarea name="message" rows="3" placeholder="Tell us a little about your business"></textarea></label><div class="form-actions"><button class="pill primary" type="submit">Send by email ↗</button><button class="pill wa-pill" type="button" id="lead-wa">Send on WhatsApp</button></div><small>This opens your email or WhatsApp with your message ready to send. We do not store anything on this page.</small></form></div></div></section></main>
{mobile_bar}{spark}
<footer><div class="wrap foot"><span>© <span data-year></span> Spanar Systems Private Limited · Hyderabad, India</span><span><a href="products/">AI products</a> · <a href="solutions/">Solutions</a> · <a href="privacy.html">Privacy</a> · <a href="https://github.com/SpanarSystems" rel="noopener">GitHub</a> · <a href="mailto:{SALES_EMAIL}">{SALES_EMAIL}</a>{foot_ph}</span></div></footer><script>window.SPANAR={{email:"{SALES_EMAIL}",wa:"{digits}"}}</script><script src="assets/js/spanar-next.js"></script></body></html>'''
    (ROOT / "index.html").write_text(head(title, desc, kw, "", ld, depth="") + body)

def build_seo():
    urls = [("", "1.0"), ("products/", "0.9"), ("solutions/", "0.9")] + [(f"solutions/{d['slug']}.html", "0.8") for d in DOMAINS] + [(f"products/{p['slug']}.html", "0.7") for p in PRODUCTS] + [("privacy.html", "0.2")]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(x)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /forms/\n\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    (ROOT / "solutions").mkdir(exist_ok=True)
    for d in DOMAINS: build_page(d)
    build_hub()
    for pr in PRODUCTS: build_product(pr)
    build_products_hub(); build_temple_redirect(); build_index(); build_seo()
    print("built", len(DOMAINS), "solution pages")
