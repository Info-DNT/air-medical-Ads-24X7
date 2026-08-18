import re
import os

# ── Load template ─────────────────────────────────────────────────────────────
with open("air-ambulance-dummy.html", "r", encoding="utf-8") as f:
    template = f.read()

# ── Extract accordion block from template (5 region dropdowns) ──────────────
_routes_sec = re.search(r'<section id="routes-section".*?</section>', template, re.DOTALL)
_acc_match  = re.search(
    r'(<!-- Region Accordion:.*?)(\s*\n\s*</div>\s*\n\s*</section>)',
    _routes_sec.group(0), re.DOTALL) if _routes_sec else None
ACCORDION_HTML = _acc_match.group(1).strip() if _acc_match else ""
if ACCORDION_HTML:
    print(f"[INFO] Accordion extracted: {len(ACCORDION_HTML):,} chars, 5 regions")
else:
    print("[WARN] Accordion block not found in template!")

# ── LocalBusiness schema placeholder (must match dummy exactly) ───────────────
old_schema = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "MedicalOrganization"],
      "name": "Air Medical 24X7",
      "url": "https://airmedical24x7.com/air-ambulance-[SLUG]",
      "telephone": "[PHONE_RAW]",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "[CITY]",
        "addressRegion": "[REGION]",
        "addressCountry": "[COUNTRY_CODE]"
      },
      "description": "24X7 Air Ambulance Services across [COUNTRY/REGION] — [CITIES]. ICU-equipped medical evacuation to India and worldwide.",
      "areaServed": "[COUNTRY/REGION] — [CITIES]",
      "medicalSpecialty": "Emergency Medicine",
      "availableService": "Air Ambulance",
      "openingHours": "Mo-Su 00:00-24:00"
    }
    </script>"""

routes_re = r'<section id="routes-section".*?(?=<section id="services"|<!-- Services Grid -->)'

# ── Route card generator ──────────────────────────────────────────────────────
def route_card(origin, destination, description, wa="https://wa.me/16593005200?text=I%20need%20Assistance%20with%20Patient%20Air%20Transfer.%20Please%20Assist!"):
    return f"""                    <!-- Route Card: {origin} -> {destination} -->
                    <div class="bg-white p-6 rounded-2xl border border-outline-variant/10 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between font-headline font-black text-primary text-base mb-4">
                                <div class="flex flex-col text-left">
                                    <span class="leading-tight text-sm font-extrabold">{origin}</span>
                                </div>
                                <span class="material-symbols-outlined text-secondary text-base flex-shrink-0 mx-2">trending_flat</span>
                                <div class="flex flex-col text-right">
                                    <span class="leading-tight text-sm font-extrabold text-right">{destination}</span>
                                </div>
                            </div>
                            <p class="text-on-surface-variant font-body leading-relaxed text-xs mb-6">
                                {description}
                            </p>
                        </div>
                        <div class="pt-4 border-t border-slate-100 flex justify-end">
                            <a href="{wa}" target="_blank" rel="noopener noreferrer"
                                class="px-5 py-2.5 bg-secondary text-white rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-primary transition-all shadow-md hover:shadow-lg flex items-center gap-1.5">
                                Get Quote on WhatsApp
                                <span class="material-symbols-outlined text-xs">open_in_new</span>
                            </a>
                        </div>
                    </div>"""


# ── Root-relative path normaliser ───────────────────────────────────────────
def make_paths_relative_root(h):
    """Convert all /ads/... absolute paths to relative paths for root deployment."""
    # CSS stylesheet
    h = h.replace('href="/ads/styles.css"', 'href="styles.css"')
    # JS scripts
    h = h.replace('src="/ads/script.js"',          'src="script.js"')
    h = h.replace('src="/ads/supabase-config.js"', 'src="supabase-config.js"')
    # Standard img src and href assets
    h = h.replace('src="/ads/assets/',  'src="assets/')
    h = h.replace('href="/ads/assets/', 'href="assets/')
    # Tailwind inline bg-[url()] — hero background image
    h = h.replace("bg-[url('/ads/assets/", "bg-[url('assets/")
    # Any remaining /ads/ prefix (catch-all)
    h = h.replace('"/ads/', '"')
    return h


# ── Core page builder ─────────────────────────────────────────────────────────
def build_page(cfg):
    c   = cfg["country"]
    s   = cfg["slug"]
    pr  = cfg["phone_raw"]
    pd  = cfg["phone_display"]
    pp  = cfg["phone_prefix"]
    cap = cfg["capital"]
    cit = cfg["cities"]
    cc  = cfg["country_code"]
    reg = cfg.get("schema_region", cap)
    c1  = cfg["city_1"];  c2 = cfg["city_2"]
    d1  = cfg["dest_1"];  d2 = cfg["dest_2"]
    ci  = cfg["cost_image"]
    ca  = cfg["cost_image_alt"]

    h = template

    # Head
    h = h.replace(
        "<title>Air Ambulance Services [COUNTRY/REGION] | ICU Medical Evacuation 24X7</title>",
        f"<title>Air Ambulance Services {c} | ICU Medical Evacuation 24X7</title>")
    h = h.replace(
        '<meta name="description"\n        content="24\u00d77 Emergency Air Ambulance Services across [COUNTRY/REGION]. ICU medical evacuation, Repatriation, patient transfer, stretcher, and medical escort services. Quote in 30 minutes." />',
        f'<meta name="description" content="24\u00d77 Emergency Air Ambulance Services across {c}. ICU medical evacuation, Medical Repatriation, patient transfer, stretcher services, and flight medical escort. Quote within 30 minutes." />')
    h = h.replace(
        '<meta name="keywords"\n        content="Air Ambulance [COUNTRY/REGION], air ambulance cost [COUNTRY/REGION], Air Ambulance [CITY/CAPITAL], private air ambulance [COUNTRY/REGION], Medical Evacuation [COUNTRY/REGION], Emergency Air Ambulance [COUNTRY/REGION], ICU Air Ambulance [COUNTRY/REGION], Air Ambulance [COUNTRY/REGION] to India, Flight Medical Escort [COUNTRY/REGION], Airline Stretcher [COUNTRY/REGION], ECMO Transfer [COUNTRY/REGION], Medical Repatriation [COUNTRY/REGION], Patient Transfer [COUNTRY/REGION], Critical Care Transport [COUNTRY/REGION]">',
        f'<meta name="keywords" content="Air Ambulance {c}, air ambulance cost {c}, Air Ambulance {cap}, private air ambulance {c}, Medical Evacuation {c}, Emergency Air Ambulance {c}, ICU Air Ambulance {c}, Air Ambulance {c} to India, Flight Medical Escort {c}, Airline Stretcher {c}, ECMO Transfer {c}, Medical Repatriation {c}, Patient Transfer {c}, Critical Care Transport {c}">')
    h = h.replace(
        '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-[SLUG]" />',
        f'<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-{s}" />')

    # LocalBusiness schema
    new_schema = f"""    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "MedicalOrganization"],
      "name": "Air Medical 24X7",
      "url": "https://airmedical24x7.com/air-ambulance-{s}",
      "telephone": "{pr}",
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "{cap}",
        "addressRegion": "{reg}",
        "addressCountry": "{cc}"
      }},
      "description": "24X7 Air Ambulance Services across {c} \u2014 {cit}. ICU-equipped medical evacuation to India and worldwide.",
      "areaServed": "{c} \u2014 {cit}",
      "medicalSpecialty": "Emergency Medicine",
      "availableService": "Air Ambulance",
      "openingHours": "Mo-Su 00:00-24:00"
    }}
    </script>"""
    h = h.replace(old_schema, new_schema)

    # Phone
    h = h.replace("[PHONE_RAW]",     pr)
    h = h.replace("[PHONE_DISPLAY]", pd)

    # Hero
    h = h.replace(
        "24/7 ICU Air Ambulance & Medical Evacuation from [COUNTRY/REGION]",
        f"24/7 ICU Air Ambulance &amp; Medical Evacuation from {c}")
    h = h.replace(
        "Global bed-to-bed medical repatriation from anywhere in [COUNTRY/REGION], including [CITIES], to destinations worldwide. Rapid dispatch with a fully equipped medical crew, providing safe and reliable transfers from [COUNTRY/REGION] to anywhere in the world.",
        f"Global bed-to-bed medical repatriation from anywhere in {c}, including {cit}, to destinations worldwide. Rapid dispatch with a fully equipped medical crew, providing safe and reliable transfers from {c} to anywhere in the world.")

    # Form
    h = h.replace('placeholder="[PHONE_PREFIX] Enter your number"', f'placeholder="{pp} Enter your number"')
    h = h.replace('placeholder="e.g. [CITY_1], [CITY_2]"',         f'placeholder="e.g. {c1}, {c2}"')
    h = h.replace('placeholder="e.g. [DEST_1], [DEST_2]"',         f'placeholder="e.g. {d1}, {d2}"')

    # Stats / Cost section
    h = h.replace("[COUNTRY/REGION] Command Center",                 f"{c} Command Center")
    h = h.replace("Air Ambulance &amp; Airline Stretcher Costs from [COUNTRY/REGION]", f"Air Ambulance &amp; Airline Stretcher Costs from {c}")
    h = h.replace("repatriation from [COUNTRY/REGION]",              f"repatriation from {c}")
    h = h.replace("evacuations from [COUNTRY/REGION]",               f"evacuations from {c}")
    h = h.replace("Call [COUNTRY/REGION] Emergency Desk",            f"Call {c} Emergency Desk")
    h = h.replace(
        "We provide medical transfers from major cities in [COUNTRY/REGION], including <strong>[CITIES]</strong>, to destinations across Europe, Asia, the Middle East, North America, and worldwide, ensuring seamless bedside-to-bedside patient transportation.",
        f"We provide medical transfers from major cities in {c}, including <strong>{cit}</strong>, to destinations across Europe, Asia, the Middle East, North America, and worldwide, ensuring seamless bedside-to-bedside patient transportation.")
    h = h.replace(
        'src="/ads/assets/air-ambulance-[SLUG].jfif" alt="Air Ambulance [COUNTRY/REGION] Cost"',
        f'src="assets/{ci}" alt="{ca}"')

    # Routes section
    cards_html = "\n".join([route_card(o, d, desc) for o, d, desc in cfg["route_cards"]])
    new_routes = f"""    <section id="routes-section"
        class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-12">
                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
                    Critical Global Transfer Routes from {c}
                </h2>
                <p class="text-on-surface-variant font-body leading-relaxed text-sm">
                    Providing dedicated bed-to-bed ICU air ambulance and commercial airline stretcher services across all major international medical corridors from {c} with seamless end-to-end medical transportation.
                </p>
            </div>
            <div id="popular-routes">
                <h3 class="font-headline text-lg font-black text-primary mb-6 uppercase tracking-wider">Most Requested Transfer Routes</h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
{cards_html}
                </div>
            </div>

            {ACCORDION_HTML}

        </div>
    </section>"""
    h = re.sub(routes_re, new_routes + "\n\n", h, flags=re.DOTALL)

    # FAQs
    h = h.replace("insurance coordination for [COUNTRY/REGION]",   f"insurance coordination for {c}")
    h = h.replace("How much does an air ambulance from [COUNTRY/REGION] to India cost?", f"How much does an air ambulance from {c} to India cost?")
    h = h.replace(
        "The cost of an air ambulance from [COUNTRY/REGION] to India depends on the departure city, destination in India, aircraft type, and the level of medical care required onboard. For stable patients, a commercial airline stretcher or flight medical escort is a more affordable option. Contact our team for a precise quote within 30 minutes.",
        f"The cost of an air ambulance from {c} to India depends on the departure city, aircraft type, and the level of medical care required onboard. For stable patients, a commercial airline stretcher or flight medical escort is a more affordable option. Contact our team for a precise quote within 30 minutes.")
    h = h.replace("cities in [COUNTRY/REGION] do you cover for air ambulance services?", f"cities in {c} do you cover for air ambulance services?")
    h = h.replace(
        "We cover all major cities in [COUNTRY/REGION] and regions including London, Manchester, Birmingham, Glasgow, Edinburgh, Leeds, Sheffield, Leicester, Bristol, and nationwide. Ground ambulance is coordinated from the patient's location to the nearest departure airport, with the full transfer managed by our operations team.",
        f"We cover all major cities in {c}, including {cit}. Ground ambulance is coordinated from the patient's location to the nearest departure airport, with the full transfer managed by our operations team.")
    h = h.replace("quickly can an air ambulance be arranged from [COUNTRY/REGION]?",     f"quickly can an air ambulance be arranged from {c}?")
    h = h.replace("I use insurance for air ambulance services from [COUNTRY/REGION]?",   f"I use insurance for air ambulance services from {c}?")
    h = h.replace("Is a flight medical escort sufficient or do I need a dedicated air ambulance from [COUNTRY/REGION]?", f"Is a flight medical escort sufficient or do I need a dedicated air ambulance from {c}?")
    h = h.replace("is ground ambulance in [COUNTRY/REGION] coordinated for air ambulance transfers?", f"is ground ambulance in {c} coordinated for air ambulance transfers?")

    # Footer / Why Families / Operations
    h = h.replace("24X7 [COUNTRY/REGION] Emergency Helpline",                           f"24X7 {c} Emergency Helpline")
    h = h.replace("<!-- Why Families in [COUNTRY/REGION] Rely on Air Medical 24X7 -->", f"<!-- Why Families in {c} Rely on Air Medical 24X7 -->")
    h = h.replace("Why Families in [COUNTRY/REGION] Rely on Air Medical 24X7",          f"Why Families in {c} Rely on Air Medical 24X7")
    h = h.replace("thousands of families in [COUNTRY/REGION]",                          f"thousands of families across {c}")
    h = h.replace("[COUNTRY/REGION] Operations &mdash; Rapid Local Response",           f"{c} Operations &mdash; Rapid Local Response")
    h = h.replace(
        "Our [COUNTRY/REGION] desk handles\n                                    NHS hospital liaisons, London airport clearances (Heathrow, Gatwick, Stansted), and ground ambulance dispatch &mdash; ensuring swift response across England, Scotland, Wales, and Northern Ireland.",
        f"Our {c} operations desk coordinates international flight clearances, ground ambulance dispatch, and hospital liaisons &mdash; ensuring swift medical response across {cit}.")
    h = h.replace(
        "across all\n                                    [COUNTRY/REGION] departures.",
        f"across all\n                                    {c} departures.")

    # Global fallback
    h = h.replace("[COUNTRY/REGION]", c)
    h = h.replace("[SLUG]",           s)
    h = h.replace("[CITY/CAPITAL]",   cap)
    h = h.replace("[CITIES]",         cit)
    h = h.replace("[CITY]",           cap)
    h = h.replace("[REGION]",         reg)
    h = h.replace("[COUNTRY_CODE]",   cc)
    h = h.replace("[PHONE_PREFIX]",   pp)
    h = h.replace("[CITY_1]",         c1)
    h = h.replace("[CITY_2]",         c2)
    h = h.replace("[DEST_1]",         d1)
    h = h.replace("[DEST_2]",         d2)

    # Fix 1: Remove uppercase class from 'How We Transfer' heading
    h = h.replace(
        'class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-3 tracking-tighter uppercase"',
        'class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-3 tracking-tighter"'
    )

    # ── Normalise all /ads/ absolute paths to root-relative ──────────────────
    h = make_paths_relative_root(h)
    return h


# ── Country configs ───────────────────────────────────────────────────────────
COUNTRIES = [
    {
        "country": "Tanzania", "slug": "tanzania",
        "phone_raw": "+255800120158", "phone_display": "+255 800 12 0158", "phone_prefix": "+255",
        "capital": "Dar es Salaam", "cities": "Dar es Salaam, Zanzibar, Arusha, Mwanza, Dodoma",
        "country_code": "TZ", "schema_region": "Dar es Salaam Region",
        "cost_image": "tanzania-country.jpeg", "cost_image_alt": "Air Ambulance Tanzania Cost",
        "city_1": "Dar es Salaam", "city_2": "Zanzibar",
        "dest_1": "Mumbai, India",  "dest_2": "Dubai, UAE",
        "route_cards": [
            ("Dar es Salaam", "Mumbai",    "Dedicated ICU air ambulance and flight medical escort from Dar es Salaam to Mumbai, coordinating with leading Indian super-specialty hospitals for seamless bed-to-bed transfer."),
            ("Dar es Salaam", "New Delhi", "Critical care air ambulance transfers from Dar es Salaam to New Delhi, managing all international clearances, medical crew deployment, and ground ambulance logistics."),
            ("Dar es Salaam", "Dubai",     "ICU-equipped air ambulance and commercial airline stretcher services from Dar es Salaam to Dubai, providing continuous patient monitoring and hospital coordination."),
            ("Zanzibar",      "Chennai",   "Emergency medical repatriation from Zanzibar to Chennai, India. Fully managed bed-to-bed transfer with specialised medical crew and rapid flight clearance."),
            ("Arusha",        "Singapore", "Long-haul ICU air ambulance from Arusha to Singapore, coordinating with world-class specialist centres for complex medical cases requiring advanced treatment."),
            ("Dar es Salaam", "London",    "International medical repatriation from Dar es Salaam to London, UK. Commercial airline stretcher and dedicated air ambulance options with full escort services."),
        ]
    },
    {
        "country": "Vietnam", "slug": "vietnam",
        "phone_raw": "+8412032123", "phone_display": "+84 1203 2123", "phone_prefix": "+84",
        "capital": "Hanoi", "cities": "Ho Chi Minh City, Hanoi, Da Nang, Nha Trang, Hoi An",
        "country_code": "VN", "schema_region": "Ho Chi Minh City",
        "cost_image": "vietnam-country.jfif", "cost_image_alt": "Air Ambulance Vietnam Cost",
        "city_1": "Ho Chi Minh City", "city_2": "Hanoi",
        "dest_1": "Mumbai, India",    "dest_2": "Singapore",
        "route_cards": [
            ("Ho Chi Minh City", "Mumbai",    "ICU air ambulance and medical escort from Ho Chi Minh City to Mumbai, India. Fully managed bed-to-bed transfer with specialised crew and continuous patient monitoring."),
            ("Hanoi",            "New Delhi", "Critical care air ambulance from Hanoi to New Delhi, coordinating international clearances, specialised medical crew deployment, and ground ambulance logistics."),
            ("Da Nang",          "Dubai",     "Emergency air ambulance from Da Nang to Dubai, UAE. ICU-equipped aircraft, flight medical escort, and full hospital coordination for seamless international transfer."),
            ("Ho Chi Minh City", "Singapore", "Short-haul ICU air ambulance from Ho Chi Minh City to Singapore, connecting patients to world-class medical facilities with rapid dispatch and flight clearance."),
            ("Hanoi",            "Bangkok",   "Medical repatriation from Hanoi to Bangkok, Thailand. Commercial airline stretcher or dedicated air ambulance options with certified medical escort personnel."),
            ("Ho Chi Minh City", "Sydney",    "Long-haul international medical evacuation from Ho Chi Minh City to Sydney, Australia, with continuous ICU monitoring and full end-to-end care coordination."),
        ]
    },
    {
        "country": "Spain", "slug": "spain",
        "phone_raw": "+34900123456", "phone_display": "+34 900 123 456", "phone_prefix": "+34",
        "capital": "Madrid", "cities": "Madrid, Barcelona, Valencia, Seville, Malaga, Bilbao",
        "country_code": "ES", "schema_region": "Comunidad de Madrid",
        "cost_image": "madrid-spain-country.jpeg", "cost_image_alt": "Air Ambulance Spain Madrid Cost",
        "city_1": "Madrid", "city_2": "Barcelona",
        "dest_1": "Mumbai, India", "dest_2": "Dubai, UAE",
        "route_cards": [
            ("Madrid",    "Mumbai",    "Dedicated ICU air ambulance and medical escort services from Madrid to Mumbai, India, coordinating with leading super-specialty hospitals for seamless bed-to-bed patient transfer."),
            ("Barcelona", "New Delhi", "Critical care air ambulance transfers from Barcelona to New Delhi, managing all international clearances, specialised medical crew, and ground ambulance logistics."),
            ("Madrid",    "Dubai",     "ICU-equipped air ambulance and commercial airline stretcher services from Madrid to Dubai, UAE, with continuous patient monitoring and hospital coordination."),
            ("Seville",   "London",    "Medical repatriation from Seville to London, UK. Commercial airline stretcher and dedicated air ambulance options with certified medical escort personnel."),
            ("Madrid",    "New York",  "Transatlantic ICU air ambulance from Madrid to New York, USA, managing all flight clearances, medical crew deployment, and receiving hospital coordination."),
            ("Barcelona", "Toronto",   "International medical evacuation from Barcelona to Toronto, Canada, with fully equipped ICU aircraft and seamless end-to-end patient care management."),
        ]
    },
    {
        "country": "Bangladesh", "slug": "bangladesh",
        "phone_raw": "+8801700123456", "phone_display": "+880 1700 123456", "phone_prefix": "+880",
        "capital": "Dhaka", "cities": "Dhaka, Chittagong, Sylhet, Khulna, Rajshahi",
        "country_code": "BD", "schema_region": "Dhaka Division",
        "cost_image": "dhaka-bangladesh-country.jpeg", "cost_image_alt": "Air Ambulance Bangladesh Dhaka Cost",
        "city_1": "Dhaka", "city_2": "Chittagong",
        "dest_1": "Kolkata, India", "dest_2": "Mumbai, India",
        "route_cards": [
            ("Dhaka",      "Kolkata",    "Rapid ICU air ambulance and medical escort from Dhaka to Kolkata, India. Nearest super-specialty corridor with fast clearance and bed-to-bed transfer management."),
            ("Dhaka",      "New Delhi",  "Critical care air ambulance from Dhaka to New Delhi, coordinating international clearances, specialised medical crew deployment, and ground ambulance logistics."),
            ("Chittagong", "Chennai",    "Emergency medical repatriation from Chittagong to Chennai, India. Dedicated air ambulance or commercial airline stretcher with certified medical escort."),
            ("Dhaka",      "Dubai",      "ICU-equipped air ambulance and commercial airline stretcher services from Dhaka to Dubai, UAE, with continuous patient monitoring and hospital coordination."),
            ("Dhaka",      "London",     "International medical evacuation from Dhaka to London, UK. Fully managed bed-to-bed transfer with specialised crew and all flight clearance handling."),
            ("Sylhet",     "Singapore",  "Long-haul ICU air ambulance from Sylhet to Singapore, connecting patients to world-class medical facilities with rapid dispatch and seamless coordination."),
        ]
    },
]

# ── Generate pages ────────────────────────────────────────────────────────────
for cfg in COUNTRIES:
    html = build_page(cfg)
    out  = f"air-ambulance-{cfg['slug']}.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved {out}  ({len(html):,} bytes)")
