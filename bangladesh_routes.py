"""
bangladesh_routes.py
====================
Route data and HTML injector for air-ambulance-bangladesh.html.

Pattern mirrors vietnam_routes.py / spain_routes.py.
Only air-ambulance-bangladesh.html is modified (root + uae-only-deploy).

Run:
    python bangladesh_routes.py
"""

import re
import os
from vietnam_routes import auto_desc, accordion_item, build_custom_sidebar

# ── Inbound sidebar helper (reverses direction: dest → country) ───────────────
def _li_inbound(dest, anchor, country="Bangladesh"):
    """Renders 'UAE to Bangladesh' instead of 'Bangladesh to UAE' with crisp styling."""
    return (
        f'                                        <li class="flex items-center gap-1 min-w-0">'
        f'<span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span>'
        f'<a href="#{anchor}" title="Air Ambulance from {dest} to {country}" class="hover:text-secondary hover:underline transition-all leading-tight text-[9px] font-semibold text-slate-200">{dest} to {country}</a></li>'
    )


def build_inbound_sidebar(groups, country="Bangladesh"):
    """Same structure as build_custom_sidebar but uses _li_inbound for direction."""
    divs = []
    for label, anchor, dests in groups:
        items = "\n".join(_li_inbound(d, anchor, country) for d in dests)
        divs.append(
            f'                                <!-- {label} -->\n'
            f'                                <div>\n'
            f'                                    <a href="#{anchor}" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">{label}</a>\n'
            f'                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-1 text-[9px] text-slate-200 font-semibold">\n'
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

# ── WhatsApp CTA ───────────────────────────────────────────────────────────────
WA = "https://wa.me/16593005200?text=I%20need%20Assistance%20with%20Patient%20Air%20Transfer.%20Please%20Assist!"

# ═══════════════════════════════════════════════════════════════════════════════
# 1.  SIDEBAR  (Hero left-panel — "X → Bangladesh" inbound routes)
# ═══════════════════════════════════════════════════════════════════════════════

BANGLADESH_SIDEBAR = [
    ("Middle East & GCC", "region-asia", [
        "UAE",          "Oman",          "Qatar",
        "Kuwait",       "Bahrain",       "Saudi Arabia",
    ]),
    ("India & South Asia", "region-asia", [
        "India",        "Maldives",      "Nepal",
        "Myanmar",
    ]),
    ("Southeast & East Asia", "region-asia", [
        "Malaysia",     "Japan",         "Thailand",
        "China",        "Singapore",     "South Korea",
    ]),
    ("Europe & UK", "region-europe-usa", [
        "UK",           "Germany",       "Italy",
        "France",       "Türkiye",
    ]),
    ("North America", "region-europe-usa", [
        "USA",          "Canada",
    ]),
    ("Oceania", "region-oceania", [
        "Australia",
    ]),
    ("Africa", "region-africa", [
        "Kenya",        "South Africa",
    ]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 2.  MOST REQUESTED ROUTE CARDS  (28 individual cards)
# ═══════════════════════════════════════════════════════════════════════════════

BANGLADESH_ROUTE_CARDS = [
    # GCC / Middle East (11 cards)
    ("Dubai",        "Dhaka",      auto_desc("Dubai",        "Dhaka")),
    ("Dubai",        "Chattogram", auto_desc("Dubai",        "Chattogram")),
    ("Abu Dhabi",    "Dhaka",      auto_desc("Abu Dhabi",    "Dhaka")),
    ("Abu Dhabi",    "Chattogram", auto_desc("Abu Dhabi",    "Chattogram")),
    ("Riyadh",       "Dhaka",      auto_desc("Riyadh",       "Dhaka")),
    ("Jeddah",       "Dhaka",      auto_desc("Jeddah",       "Dhaka")),
    ("Dammam",       "Dhaka",      auto_desc("Dammam",       "Dhaka")),
    ("Doha",         "Dhaka",      auto_desc("Doha",         "Dhaka")),
    ("Muscat",       "Dhaka",      auto_desc("Muscat",       "Dhaka")),
    ("Muscat",       "Chattogram", auto_desc("Muscat",       "Chattogram")),
    ("Kuwait City",  "Dhaka",      auto_desc("Kuwait City",  "Dhaka")),
    # India (7 cards)
    ("Kolkata",      "Dhaka",      auto_desc("Kolkata",      "Dhaka")),
    ("Kolkata",      "Chattogram", auto_desc("Kolkata",      "Chattogram")),
    ("Delhi",        "Dhaka",      auto_desc("Delhi",        "Dhaka")),
    ("Chennai",      "Dhaka",      auto_desc("Chennai",      "Dhaka")),
    ("Chennai",      "Chattogram", auto_desc("Chennai",      "Chattogram")),
    ("Vellore",      "Dhaka",      auto_desc("Vellore",      "Dhaka")),
    ("Bengaluru",    "Dhaka",      auto_desc("Bengaluru",    "Dhaka")),
    # SE / East Asia (3 cards)
    ("Kuala Lumpur", "Dhaka",      auto_desc("Kuala Lumpur", "Dhaka")),
    ("Singapore",    "Dhaka",      auto_desc("Singapore",    "Dhaka")),
    ("Bangkok",      "Dhaka",      auto_desc("Bangkok",      "Dhaka")),
    # Europe (1 card)
    ("London",       "Dhaka",      auto_desc("London",       "Dhaka")),
    # Maldives (2 cards)
    ("Malé",         "Dhaka",      auto_desc("Malé",         "Dhaka")),
    ("Malé",         "Chattogram", auto_desc("Malé",         "Chattogram")),
    # Americas (2 cards)
    ("New York",     "Dhaka",      auto_desc("New York",     "Dhaka")),
    ("Toronto",      "Dhaka",      auto_desc("Toronto",      "Dhaka")),
    # Oceania (2 cards)
    ("Sydney",       "Dhaka",      auto_desc("Sydney",       "Dhaka")),
    ("Melbourne",    "Dhaka",      auto_desc("Melbourne",    "Dhaka")),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 3.  ACCORDION DATA  (80 individual cards across 4 sections)
# ═══════════════════════════════════════════════════════════════════════════════

BANGLADESH_ACCORDION = {
    # ── Asia & Subcontinent (66 cards) ────────────────────────────────────────
    "asia": [
        # India (30 cards)
        ("Kolkata",            "Dhaka"),   ("Kolkata",            "Chattogram"),
        ("Delhi",              "Dhaka"),   ("Delhi",              "Chattogram"),
        ("Gurugram",           "Dhaka"),   ("Noida",              "Dhaka"),
        ("Chennai",            "Dhaka"),   ("Chennai",            "Chattogram"),
        ("Vellore",            "Dhaka"),   ("Bengaluru",          "Dhaka"),
        ("Hyderabad",          "Dhaka"),   ("Mumbai",             "Dhaka"),
        ("Pune",               "Dhaka"),   ("Kochi",              "Dhaka"),
        ("Thiruvananthapuram", "Dhaka"),   ("Coimbatore",         "Dhaka"),
        ("Ahmedabad",          "Dhaka"),   ("Surat",              "Dhaka"),
        ("Jaipur",             "Dhaka"),   ("Lucknow",            "Dhaka"),
        ("Chandigarh",         "Dhaka"),   ("Patna",              "Dhaka"),
        ("Bhubaneswar",        "Dhaka"),   ("Guwahati",           "Dhaka"),
        ("Ranchi",             "Dhaka"),   ("Visakhapatnam",      "Dhaka"),
        ("Nagpur",             "Dhaka"),   ("Indore",             "Dhaka"),
        ("Bhopal",             "Dhaka"),   ("Rajkot",             "Dhaka"),
        # GCC & Middle East (19 cards)
        ("Dubai",              "Dhaka"),   ("Dubai",              "Chattogram"),
        ("Abu Dhabi",          "Dhaka"),   ("Abu Dhabi",          "Chattogram"),
        ("Sharjah",            "Dhaka"),   ("Sharjah",            "Chattogram"),
        ("Riyadh",             "Dhaka"),   ("Riyadh",             "Chattogram"),
        ("Jeddah",             "Dhaka"),   ("Jeddah",             "Chattogram"),
        ("Dammam",             "Dhaka"),   ("Dammam",             "Chattogram"),
        ("Doha",               "Dhaka"),
        ("Muscat",             "Dhaka"),   ("Muscat",             "Chattogram"),
        ("Salalah",            "Dhaka"),   ("Salalah",            "Chattogram"),
        ("Kuwait City",        "Dhaka"),   ("Manama",             "Dhaka"),
        # Southeast & East Asia (17 cards)
        ("Kuala Lumpur",       "Dhaka"),   ("Singapore",          "Dhaka"),
        ("Bangkok",            "Dhaka"),
        ("Malé",               "Dhaka"),   ("Malé",               "Chattogram"),
        ("Kathmandu",          "Dhaka"),
        ("Yangon",             "Dhaka"),   ("Yangon",             "Chattogram"),
        ("Beijing",            "Dhaka"),   ("Beijing",            "Chattogram"),
        ("Guangzhou",          "Dhaka"),   ("Guangzhou",          "Chattogram"),
        ("Seoul",              "Dhaka"),
        ("Tokyo",              "Dhaka"),   ("Tokyo",              "Chattogram"),
        ("Osaka",              "Dhaka"),   ("Osaka",              "Chattogram"),
    ],

    # ── USA, Canada & Europe (10 cards) ───────────────────────────────────────
    "europe_usa": [
        ("London",      "Dhaka"),   ("Manchester",  "Dhaka"),
        ("Birmingham",  "Dhaka"),
        ("Rome",        "Dhaka"),   ("Milan",       "Dhaka"),
        ("Frankfurt",   "Dhaka"),   ("Paris",       "Dhaka"),
        ("Istanbul",    "Dhaka"),
        ("New York",    "Dhaka"),   ("Toronto",     "Dhaka"),
    ],

    # ── Africa (2 cards) ──────────────────────────────────────────────────────
    "africa": [
        ("Nairobi",       "Dhaka"),
        ("Johannesburg",  "Dhaka"),
    ],

    # ── Oceania (2 cards) ─────────────────────────────────────────────────────
    "oceania": [
        ("Sydney",     "Dhaka"),
        ("Melbourne",  "Dhaka"),
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════
# HTML builders
# ═══════════════════════════════════════════════════════════════════════════════

def build_route_card(origin, dest, desc):
    """Single Most-Requested card (matches existing Bangladesh card HTML)."""
    return (
        f'                    <!-- Route Card: {origin} → {dest} -->\n'
        f'                    <div class="bg-white p-6 rounded-2xl border border-outline-variant/10 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col justify-between">\n'
        f'                        <div>\n'
        f'                            <div class="flex items-center justify-between font-headline font-black text-primary text-base mb-4">\n'
        f'                                <div class="flex flex-col text-left">\n'
        f'                                    <span class="leading-tight text-sm font-extrabold">{origin}</span>\n'
        f'                                </div>\n'
        f'                                <span class="material-symbols-outlined text-secondary text-base flex-shrink-0 mx-2">trending_flat</span>\n'
        f'                                <div class="flex flex-col text-right">\n'
        f'                                    <span class="leading-tight text-sm font-extrabold text-right">{dest}</span>\n'
        f'                                </div>\n'
        f'                            </div>\n'
        f'                            <p class="text-on-surface-variant font-body leading-relaxed text-xs mb-6">{desc}</p>\n'
        f'                        </div>\n'
        f'                        <div class="pt-4 border-t border-slate-100 flex justify-end">\n'
        f'                            <a href="{WA}" target="_blank" rel="noopener noreferrer"\n'
        f'                                class="px-5 py-2.5 bg-secondary text-white rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-primary transition-all shadow-md hover:shadow-lg flex items-center gap-1.5">\n'
        f'                                Get Quote on WhatsApp\n'
        f'                                <span class="material-symbols-outlined text-xs">open_in_new</span>\n'
        f'                            </a>\n'
        f'                        </div>\n'
        f'                    </div>'
    )


def build_accordion_section(rid, label, tid, routes):
    """Full accordion block for one geographic region."""
    cards = "\n".join(accordion_item(o, d) for o, d in routes)
    return (
        f'            <!-- Region Accordion: {label} -->\n'
        f'            <div id="region-{rid}" class="mb-6 border border-slate-200/60 dark:border-slate-800/60 rounded-2xl overflow-hidden bg-white shadow-sm transition-all duration-300">\n'
        f'                <button class="w-full px-6 py-5 flex items-center justify-between bg-slate-50/50 hover:bg-slate-50 transition-colors text-left focus:outline-none group"\n'
        f'                    onclick="toggleRegion(\'{tid}\')">\n'
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


def build_all_accordions():
    return "\n\n".join([
        build_accordion_section("asia",       "Asia & Subcontinent Routes", "asia",       BANGLADESH_ACCORDION["asia"]),
        build_accordion_section("europe-usa", "USA, Canada & Europe Routes","europe-usa", BANGLADESH_ACCORDION["europe_usa"]),
        build_accordion_section("africa",     "Africa Routes",              "africa",     BANGLADESH_ACCORDION["africa"]),
        build_accordion_section("oceania",    "Oceania Routes",             "oceania",    BANGLADESH_ACCORDION["oceania"]),
    ])


def build_all_route_cards():
    return "\n".join(build_route_card(o, d, desc) for o, d, desc in BANGLADESH_ROUTE_CARDS)


# ═══════════════════════════════════════════════════════════════════════════════
# Injection helpers
# ═══════════════════════════════════════════════════════════════════════════════

def inject_sidebar(html, country="Bangladesh"):
    """Replace the sidebar destinations grid (inbound: 'UAE to Bangladesh')."""
    sidebar_html = build_inbound_sidebar(BANGLADESH_SIDEBAR, country)

    # Matches the wrapping div that contains the grid — bounded by the sentinel comments
    pattern = re.compile(
        r'(<!-- Destinations Grid by Region.*?— 3 columns, no scroll -->)\s*'
        r'<div class="space-y-2">.*?</div>'
        r'(\s*</div>\s*<!-- end destinations grid -->)',
        re.DOTALL,
    )
    # Try sentinel-based replacement first
    if re.search(pattern, html):
        return re.sub(pattern, lambda m: sidebar_html + m.group(2), html)

    # Fallback: replace by the opening marker of the destinations grid
    fallback = re.compile(
        r'<!-- Destinations Grid by Region.*?</div>\s*</div>',
        re.DOTALL,
    )
    result, n = re.subn(fallback, sidebar_html, html, count=1)
    if n:
        return result

    print("  WARNING: sidebar injection marker not found — sidebar unchanged.")
    return html


def inject_routes_section(html):
    """Replace the entire <section id="routes-section" ...> </section> block with clean route cards and accordions."""
    cards_html = build_all_route_cards()
    acc_html = build_all_accordions()

    new_section = (
        '<!-- SECTION START: Critical Global Transfer Routes (MUST maintain 100% design and class parity) -->\n'
        '    <!-- Critical Global Transfer Routes from Bangladesh Section -->\n'
        '    <section id="routes-section"\n'
        '        class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">\n'
        '        <div class="container mx-auto px-6 md:px-8 relative z-10">\n'
        '            <div class="text-center max-w-3xl mx-auto mb-12">\n'
        '                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">\n'
        '                    Critical Global Transfer Routes from Bangladesh\n'
        '                </h2>\n'
        '                <p class="text-on-surface-variant font-body leading-relaxed text-sm">\n'
        '                    Providing dedicated bed-to-bed ICU air ambulance and commercial airline stretcher services across all major international medical corridors from Bangladesh with seamless end-to-end medical transportation.\n'
        '                </p>\n'
        '            </div>\n'
        '            <div id="popular-routes" class="mb-14">\n'
        '                <h3 class="font-headline text-lg font-black text-primary mb-6 uppercase tracking-wider">Most Requested Transfer Routes</h3>\n'
        '                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">\n'
        + cards_html + '\n'
        '                </div>\n'
        '            </div>\n\n'
        + acc_html + '\n\n'
        '        </div>\n'
        '    </section>'
    )

    pattern = re.compile(
        r'(?:<!-- SECTION START: Critical Global Transfer Routes.*?\n\s*)?'
        r'<section id="routes-section"[^>]*>.*?</section>',
        re.DOTALL
    )

    result, n = re.subn(pattern, new_section, html, count=1)
    if n:
        return result

    print("  WARNING: routes-section tag not found — routes section unchanged.")
    return html


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

BASE = os.path.dirname(os.path.abspath(__file__))
TARGETS = [
    os.path.join(BASE, "air-ambulance-bangladesh.html"),
    os.path.join(BASE, "uae-only-deploy", "air-ambulance-bangladesh.html"),
]


def process(path):
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original_len = len(html)

    html = inject_sidebar(html)
    html = inject_routes_section(html)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    delta = len(html) - original_len
    print(f"  OK  {os.path.relpath(path, BASE)}  (delta {delta:+,} bytes)")


if __name__ == "__main__":
    print("Bangladesh Routes Injector")
    print("=" * 50)
    print(f"  Route cards : {len(BANGLADESH_ROUTE_CARDS)}")
    print(f"  Accordion   : {sum(len(v) for v in BANGLADESH_ACCORDION.values())} cards across {len(BANGLADESH_ACCORDION)} sections")
    print()
    for t in TARGETS:
        process(t)
    print()
    print("Done. Only air-ambulance-bangladesh.html was modified.")

