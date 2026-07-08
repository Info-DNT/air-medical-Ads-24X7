import urllib.parse

tiers = {
    "tier-1": {
        "title": "India & Subcontinent",
        "description_template": "Specialized intercontinental ICU air ambulance transfers and medical escorts from {origin} to {dest}. Fully equipped for long-haul critical care, ventilator support, and bed-to-bed coordination.",
        "routes": [
            ("New York (JFK)", "Delhi NCR"),
            ("New York (JFK)", "Mumbai"),
            ("New York (JFK)", "Kolkata"),
            ("Chicago", "Delhi NCR"),
            ("Chicago", "Chandigarh"),
            ("San Francisco", "Bengaluru"),
            ("San Francisco", "Chennai"),
            ("Dallas / Fort Worth", "Hyderabad"),
            ("Washington, D.C.", "Hyderabad"),
            ("Houston", "Hyderabad"),
            ("Houston", "Ahmedabad"),
            ("Newark", "Ahmedabad"),
            ("Los Angeles", "Delhi NCR"),
            ("Los Angeles", "Mumbai"),
            ("Boston", "Ahmedabad"),
            ("Atlanta", "Ahmedabad"),
            ("Seattle", "Kochi")
        ]
    },
    "tier-2": {
        "title": "Middle East",
        "description_template": "Rapid-response air medical flights and critical patient transfer from {origin} to {dest}. Fully coordinated medical crews, Arabic/English bilingual coordination, and smooth customs clearance.",
        "routes": [
            ("New York (JFK)", "Dubai / Abu Dhabi"),
            ("Chicago", "Riyadh"),
            ("Houston", "Jeddah"),
            ("Los Angeles", "Doha"),
            ("Newark", "Kuwait City"),
            ("Dallas / Fort Worth", "Muscat")
        ]
    },
    "tier-3": {
        "title": "UK & Europe",
        "description_template": "High-standard intercontinental ICU transfers and commercial medical escorts from {origin} to {dest}. Coordinating with major European hospitals, specialists, and ground emergency services.",
        "routes": [
            ("New York (JFK)", "London"),
            ("Boston", "Manchester"),
            ("Chicago", "Frankfurt"),
            ("Los Angeles", "Paris"),
            ("Miami", "Madrid"),
            ("San Francisco", "Amsterdam"),
            ("Newark", "Zurich"),
            ("Washington, D.C.", "Rome")
        ]
    },
    "tier-4": {
        "title": "Canada",
        "description_template": "Dedicated border-crossing air medical evacuation and bed-to-bed patient transfer from {origin} to {dest}. Full coordination of US-Canada transit permits and ground ambulance logistics.",
        "routes": [
            ("New York (JFK)", "Toronto"),
            ("Seattle", "Vancouver"),
            ("Boston", "Montréal"),
            ("Chicago", "Calgary")
        ]
    },
    "tier-5": {
        "title": "Asia Pacific",
        "description_template": "Advanced long-distance medical repatriation and ICU flight services from {origin} to {dest}. Specialized critical care medical team, advanced life support equipment, and flight coordination.",
        "routes": [
            ("Los Angeles", "Manila"),
            ("San Francisco", "Hong Kong"),
            ("Seattle", "Tokyo"),
            ("Los Angeles", "Seoul"),
            ("San Francisco", "Singapore"),
            ("New York (JFK)", "Beijing")
        ]
    },
    "tier-6": {
        "title": "Latin America",
        "description_template": "Reliable private medical flight services and commercial stretcher repatriation from {origin} to {dest}. Multilingual medical staff, bedside handovers, and smooth international flight logistics.",
        "routes": [
            ("Miami", "Mexico City"),
            ("Miami", "São Paulo"),
            ("Houston", "Bogotá"),
            ("Miami", "Buenos Aires")
        ]
    },
    "tier-7": {
        "title": "Africa",
        "description_template": "Premium medical evacuation and long-haul intercontinental ICU transfers from {origin} to {dest}. Features advanced flight planning, refueling stops, and specialized critical-care crews.",
        "routes": [
            ("New York (JFK)", "Lagos"),
            ("Washington, D.C.", "Addis Ababa"),
            ("Atlanta", "Accra"),
            ("New York (JFK)", "Johannesburg")
        ]
    }
}

card_template = """                <!-- Route Card: {origin} → {dest} -->
                <div
                    class="bg-white p-6 rounded-2xl border border-outline-variant/10 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col justify-between">
                    <div>
                        <div
                            class="flex items-center justify-between font-headline font-black text-primary text-base mb-4">
                            <div class="flex flex-col text-left">
                                <span class="leading-tight text-sm font-extrabold">{origin}</span>
                            </div>
                            <span
                                class="material-symbols-outlined text-secondary text-base flex-shrink-0 mx-2">trending_flat</span>
                            <div class="flex flex-col text-right">
                                <span class="leading-tight text-sm font-extrabold text-right">{dest}</span>
                            </div>
                        </div>
                        <p class="text-on-surface-variant text-[11px] leading-relaxed mb-6">
                            {description}
                        </p>
                    </div>
                    <div class="pt-4 border-t border-slate-100 flex justify-end">
                        <a href="https://wa.me/971565542001?text={whatsapp_text}"
                            target="_blank" rel="noopener noreferrer"
                            class="px-5 py-2.5 bg-secondary text-white rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-primary transition-all shadow-md hover:shadow-lg flex items-center gap-1.5">
                            Get Quote on WhatsApp
                            <span class="material-symbols-outlined text-xs">open_in_new</span>
                        </a>
                    </div>
                </div>"""

# Generate all cards in a flat list
cards_html = []

for idx, (tier_id, tier_data) in enumerate(tiers.items()):
    desc_tmpl = tier_data["description_template"]
    routes = tier_data["routes"]
    
    for origin, dest in routes:
        desc = desc_tmpl.format(origin=origin, dest=dest)
        raw_msg = f"I need urgent air ambulance assistance for a patient from {origin} to {dest}. Please provide a quote."
        whatsapp_text = urllib.parse.quote(raw_msg)
        card = card_template.format(
            origin=origin,
            dest=dest,
            description=desc,
            whatsapp_text=whatsapp_text
        )
        cards_html.append(card)
        
cards_joined = "\n".join(cards_html)

section_html = f"""<!-- Critical Transfer Routes from USA Section -->
    <section class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-12">
                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
                    Critical Transfer Routes from USA
                </h2>
                <p class="text-on-surface-variant font-body leading-relaxed text-sm">
                    Providing dedicated bed-to-bed ICU air evacuations and commercial airline stretcher services on all
                    major international medical corridors from USA &mdash; India, Middle East, Europe, Asia, Africa &amp; Worldwide.
                </p>
            </div>

            <!-- Flat Grid of Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
{cards_joined}
            </div>
        </div>
    </section>

    """

# Now write this to the file replacing the section
file_path = "air-ambulance-usa.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!-- Critical Transfer Routes from USA Section -->"

# In the current file, the script element might follow, so we'll look for "<!-- Why Families in USA Rely on Air Medical 24X7 -->"
end_marker = "<!-- Why Families in USA Rely on Air Medical 24X7 -->"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Markers not found in the file.")
else:
    new_content = content[:start_idx] + section_html + content[end_idx:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully replaced critical route section with flat grid layout in air-ambulance-usa.html!")
