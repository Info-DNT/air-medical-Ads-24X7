WA = "https://wa.me/16593005200?text=I%20need%20Assistance%20with%20Patient%20Air%20Transfer.%20Please%20Assist!"

def auto_desc(o, d):
    t = [
        f"ICU air ambulance and medical escort from {o} to {d}, with continuous patient monitoring, certified medical crew, and seamless end-to-end transfer coordination.",
        f"Emergency medical repatriation from {o} to {d}. Fully managed bed-to-bed transfer with specialised medical crew, rapid flight clearance, and receiving hospital liaison.",
        f"Critical care air ambulance and airline stretcher services from {o} to {d}, ensuring advanced ICU support and comprehensive patient care throughout the journey.",
    ]
    return t[hash(o + d) % 3]

def accordion_item(o, d):
    return (
        f'                    <div class="bg-white p-6 rounded-2xl border border-outline-variant/10 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col justify-between">\n'
        f'                        <div>\n'
        f'                            <div class="flex items-center justify-between font-headline font-black text-primary text-base mb-4">\n'
        f'                                <div class="flex flex-col text-left"><span class="leading-tight text-sm font-extrabold">{o}</span></div>\n'
        f'                                <span class="material-symbols-outlined text-secondary text-base flex-shrink-0 mx-2">trending_flat</span>\n'
        f'                                <div class="flex flex-col text-right"><span class="leading-tight text-sm font-extrabold text-right">{d}</span></div>\n'
        f'                            </div>\n'
        f'                            <p class="text-on-surface-variant font-body leading-relaxed text-xs mb-6">{auto_desc(o, d)}</p>\n'
        f'                        </div>\n'
        f'                        <div class="pt-4 border-t border-slate-100 flex justify-end">\n'
        f'                            <a href="{WA}" target="_blank" rel="noopener noreferrer nofollow"\n'
        f'                                class="px-5 py-2.5 bg-secondary text-white rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-primary transition-all shadow-md hover:shadow-lg flex items-center gap-1.5">\n'
        f'                                Get Quote on WhatsApp\n'
        f'                                <span class="material-symbols-outlined text-xs">open_in_new</span>\n'
        f'                            </a>\n'
        f'                        </div>\n'
        f'                    </div>'
    )

def build_accordion_section(rid, label, tid, routes):
    cards = "\n".join(accordion_item(o, d) for o, d in routes)
    return (
        f'            <!-- Region Accordion: {label} -->\n'
        f'            <div id="region-{rid}" class="mb-6 border border-slate-200/60 dark:border-slate-800/60 rounded-2xl overflow-hidden bg-white shadow-sm transition-all duration-300">\n'
        f'                <button class="w-full px-6 py-5 flex items-center justify-between bg-slate-50/50 hover:bg-slate-50 transition-colors" onclick="toggleRegion(\'{tid}\')">\n'
        f'                    <span class="font-headline text-base md:text-lg font-black text-primary uppercase tracking-wide">{label}</span>\n'
        f'                    <span class="material-symbols-outlined text-secondary text-2xl transform transition-transform duration-300 ease-in-out" id="icon-region-{rid}">keyboard_arrow_down</span>\n'
        f'                </button>\n'
        f'                <div class="hidden transition-all duration-300 ease-in-out border-t border-slate-100" id="content-region-{rid}">\n'
        f'                    <div class="p-6">\n'
        f'                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">\n'
        f'{cards}\n'
        f'                        </div>\n'
        f'                    </div>\n'
        f'                </div>\n'
        f'            </div>'
    )

def build_custom_accordion(acc):
    return "\n\n".join([
        build_accordion_section("asia",        "Asia & Subcontinent Routes",        "asia",        acc["asia"]),
        build_accordion_section("middle-east", "Middle East & Central Asia Routes", "middle-east", acc["middle_east"]),
        build_accordion_section("europe-usa",  "USA, Canada & Europe Routes",       "europe-usa",  acc["europe_usa"]),
        build_accordion_section("oceania",     "Oceania Routes",                    "oceania",     acc["oceania"]),
        build_accordion_section("africa",      "Africa Routes",                     "africa",      acc["africa"]),
    ])

def _li(dest, anchor, country="Vietnam"):
    return (
        f'                                        <li class="flex items-center gap-1">'
        f'<span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span>'
        f'<a href="#{anchor}" class="hover:text-secondary hover:underline transition-all">{country} to {dest}</a></li>'
    )

def build_custom_sidebar(groups, country="Vietnam"):
    divs = []
    for label, anchor, dests in groups:
        items = "\n".join(_li(d, anchor, country) for d in dests)
        divs.append(
            f'                                <!-- {label} -->\n'
            f'                                <div>\n'
            f'                                    <a href="#{anchor}" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">{label}</a>\n'
            f'                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">\n'
            f'{items}\n'
            f'                                    </ul>\n'
            f'                                </div>'
        )
    return (
        '                            <!-- Destinations Grid by Region \u2014 3 columns, no scroll -->\n'
        '                            <div class="space-y-2">\n\n'
        + "\n\n".join(divs)
        + '\n                            </div>'
    )

# ── Vietnam data ──────────────────────────────────────────────────────────────

VIETNAM_SIDEBAR = [
    ("Asia & Subcontinent", "region-asia", [
        "India", "Bangladesh", "Sri Lanka",
        "Thailand", "Malaysia", "Singapore",
        "Indonesia", "Philippines", "Cambodia",
        "China", "Japan", "Hong Kong",
        "South Korea", "Taiwan", "Brunei",
        "Laos", "Myanmar", "Macau",
    ]),
    ("Middle East & Central Asia", "region-middle-east", [
        "UAE", "Qatar", "Israel",
        "T\u00fcrkiye", "Saudi Arabia", "Oman",
        "Kuwait", "Bahrain",
    ]),
]

VIETNAM_ROUTE_CARDS = [
    ("Ho Chi Minh City", "Singapore",    auto_desc("Ho Chi Minh City", "Singapore")),
    ("Hanoi",            "Singapore",    auto_desc("Hanoi",            "Singapore")),
    ("Ho Chi Minh City", "Bangkok",      auto_desc("Ho Chi Minh City", "Bangkok")),
    ("Hanoi",            "Bangkok",      auto_desc("Hanoi",            "Bangkok")),
    ("Ho Chi Minh City", "Seoul",        auto_desc("Ho Chi Minh City", "Seoul")),
    ("Hanoi",            "Seoul",        auto_desc("Hanoi",            "Seoul")),
    ("Ho Chi Minh City", "Tokyo",        auto_desc("Ho Chi Minh City", "Tokyo")),
    ("Hanoi",            "Tokyo",        auto_desc("Hanoi",            "Tokyo")),
    ("Ho Chi Minh City", "Kuala Lumpur", auto_desc("Ho Chi Minh City", "Kuala Lumpur")),
    ("Hanoi",            "Kuala Lumpur", auto_desc("Hanoi",            "Kuala Lumpur")),
    ("Ho Chi Minh City", "Mumbai",       auto_desc("Ho Chi Minh City", "Mumbai")),
    ("Hanoi",            "Mumbai",       auto_desc("Hanoi",            "Mumbai")),
    ("Ho Chi Minh City", "Delhi",        auto_desc("Ho Chi Minh City", "Delhi")),
    ("Hanoi",            "Delhi",        auto_desc("Hanoi",            "Delhi")),
    ("Ho Chi Minh City", "Dubai",        auto_desc("Ho Chi Minh City", "Dubai")),
    ("Hanoi",            "Dubai",        auto_desc("Hanoi",            "Dubai")),
    ("Ho Chi Minh City", "Hong Kong",    auto_desc("Ho Chi Minh City", "Hong Kong")),
    ("Hanoi",            "Hong Kong",    auto_desc("Hanoi",            "Hong Kong")),
    ("Ho Chi Minh City", "Doha",         auto_desc("Ho Chi Minh City", "Doha")),
    ("Hanoi",            "Doha",         auto_desc("Hanoi",            "Doha")),
]

VIETNAM_ACCORDION = {
    "asia": [
        ("Hanoi",            "Delhi"),       ("Hanoi",            "Mumbai"),
        ("Hanoi",            "Chennai"),     ("Hanoi",            "Hyderabad"),
        ("Hanoi",            "Bengaluru"),   ("Ho Chi Minh City", "Delhi"),
        ("Ho Chi Minh City", "Mumbai"),      ("Ho Chi Minh City", "Chennai"),
        ("Ho Chi Minh City", "Hyderabad"),   ("Ho Chi Minh City", "Bengaluru"),
        ("Hanoi",            "Singapore"),   ("Ho Chi Minh City", "Singapore"),
        ("Da Nang",          "Singapore"),   ("Hanoi",            "Bangkok"),
        ("Ho Chi Minh City", "Bangkok"),     ("Da Nang",          "Bangkok"),
        ("Hanoi",            "Kuala Lumpur"),("Ho Chi Minh City", "Kuala Lumpur"),
        ("Da Nang",          "Kuala Lumpur"),("Hanoi",            "Hong Kong"),
        ("Ho Chi Minh City", "Hong Kong"),   ("Da Nang",          "Hong Kong"),
        ("Hanoi",            "Beijing"),     ("Hanoi",            "Shanghai"),
        ("Ho Chi Minh City", "Shanghai"),    ("Ho Chi Minh City", "Guangzhou"),
        ("Hanoi",            "Tokyo"),       ("Ho Chi Minh City", "Tokyo"),
        ("Hanoi",            "Osaka"),       ("Ho Chi Minh City", "Osaka"),
        ("Hanoi",            "Seoul"),       ("Ho Chi Minh City", "Seoul"),
        ("Da Nang",          "Seoul"),       ("Hanoi",            "Taipei"),
        ("Ho Chi Minh City", "Taipei"),
    ],
    "middle_east": [
        ("Hanoi",            "Dubai"),       ("Ho Chi Minh City", "Dubai"),
        ("Hanoi",            "Abu Dhabi"),   ("Ho Chi Minh City", "Abu Dhabi"),
        ("Hanoi",            "Doha"),        ("Ho Chi Minh City", "Doha"),
        ("Hanoi",            "Muscat"),      ("Ho Chi Minh City", "Muscat"),
        ("Hanoi",            "Riyadh"),      ("Ho Chi Minh City", "Riyadh"),
        ("Hanoi",            "Jeddah"),      ("Ho Chi Minh City", "Jeddah"),
        ("Hanoi",            "Istanbul"),    ("Ho Chi Minh City", "Istanbul"),
    ],
    "europe_usa": [
        ("Hanoi",            "New York"),    ("Ho Chi Minh City", "New York"),
        ("Hanoi",            "Los Angeles"), ("Ho Chi Minh City", "Los Angeles"),
        ("Hanoi",            "San Francisco"),("Ho Chi Minh City","San Francisco"),
        ("Hanoi",            "Chicago"),     ("Ho Chi Minh City", "Chicago"),
        ("Hanoi",            "Houston"),     ("Ho Chi Minh City", "Houston"),
        ("Hanoi",            "Miami"),       ("Ho Chi Minh City", "Miami"),
        ("Hanoi",            "Toronto"),     ("Ho Chi Minh City", "Toronto"),
        ("Hanoi",            "Vancouver"),   ("Ho Chi Minh City", "Vancouver"),
        ("Hanoi",            "London"),      ("Ho Chi Minh City", "London"),
        ("Hanoi",            "Manchester"),
        ("Hanoi",            "Frankfurt"),   ("Ho Chi Minh City", "Frankfurt"),
        ("Hanoi",            "Munich"),
        ("Hanoi",            "Paris"),       ("Ho Chi Minh City", "Paris"),
        ("Hanoi",            "Zurich"),      ("Ho Chi Minh City", "Zurich"),
        ("Hanoi",            "Amsterdam"),   ("Ho Chi Minh City", "Amsterdam"),
        ("Hanoi",            "Rome"),        ("Ho Chi Minh City", "Rome"),
    ],
    "oceania": [
        ("Hanoi",            "Sydney"),      ("Ho Chi Minh City", "Sydney"),
        ("Hanoi",            "Melbourne"),   ("Ho Chi Minh City", "Melbourne"),
        ("Hanoi",            "Brisbane"),    ("Ho Chi Minh City", "Brisbane"),
        ("Hanoi",            "Perth"),       ("Ho Chi Minh City", "Perth"),
        ("Ho Chi Minh City", "Auckland"),
    ],
    "africa": [
        ("Hanoi",            "Johannesburg"),("Ho Chi Minh City", "Johannesburg"),
        ("Hanoi",            "Nairobi"),     ("Ho Chi Minh City", "Nairobi"),
        ("Hanoi",            "Addis Ababa"), ("Ho Chi Minh City", "Addis Ababa"),
        ("Hanoi",            "Cairo"),       ("Ho Chi Minh City", "Cairo"),
        ("Hanoi",            "Casablanca"),  ("Ho Chi Minh City", "Casablanca"),
    ],
}
