import urllib.parse

categories = {
    "india": {
        "title": "India",
        "description_template": "Specialized intercontinental ICU air ambulance transfers and medical escorts from {origin} to {dest}. Fully equipped for long-haul critical care, ventilator support, and bed-to-bed coordination.",
        "routes": [
            ("Toronto (Pearson)", "Delhi NCR"),
            ("Toronto (Pearson)", "Amritsar"),
            ("Toronto (Pearson)", "Chandigarh"),
            ("Toronto (Pearson)", "Mumbai"),
            ("Vancouver / Surrey", "Amritsar"),
            ("Vancouver / Surrey", "Chandigarh"),
            ("Calgary", "Delhi NCR"),
            ("Calgary", "Amritsar"),
            ("Edmonton", "Ludhiana"),
            ("Montréal", "Hyderabad"),
            ("Toronto (Pearson)", "Bengaluru"),
            ("Toronto (Pearson)", "Chennai"),
            ("Toronto (Pearson)", "Kolkata"),
            ("Vancouver / Surrey", "Bengaluru"),
            ("Ottawa", "Ahmedabad"),
            ("Winnipeg", "Jaipur")
        ]
    },
    "middle-east": {
        "title": "Middle East",
        "description_template": "Rapid-response air medical flights and critical patient transfer from {origin} to {dest}. Fully coordinated medical crews, Arabic/English bilingual coordination, and smooth customs clearance.",
        "routes": [
            ("Toronto (Pearson)", "Dubai / Abu Dhabi"),
            ("Vancouver / Surrey", "Riyadh"),
            ("Toronto (Pearson)", "Jeddah"),
            ("Calgary", "Doha"),
            ("Toronto (Pearson)", "Muscat")
        ]
    },
    "south-asia-non-india": {
        "title": "South Asia (Non-India)",
        "description_template": "Dedicated regional ICU air ambulance and commercial medical escort from {origin} to {dest}. Coordinated transit clearance, double-licensed medical crew, and bedside handover.",
        "routes": [
            ("Toronto (Pearson)", "Dhaka"),
            ("Vancouver / Surrey", "Karachi"),
            ("Toronto (Pearson)", "Lahore"),
            ("Toronto (Pearson)", "Islamabad"),
            ("Toronto (Pearson)", "Colombo"),
            ("Vancouver / Surrey", "Kathmandu")
        ]
    },
    "usa-uk": {
        "title": "USA & UK",
        "description_template": "Dedicated trans-border ICU air ambulance evacuation and commercial stretcher services from {origin} to {dest}. Coordinated airport logistics and ground ambulance transfers.",
        "routes": [
            ("Toronto (Pearson)", "New York"),
            ("Vancouver / Surrey", "Los Angeles"),
            ("Toronto (Pearson)", "Chicago"),
            ("Toronto (Pearson)", "London")
        ]
    },
    "europe": {
        "title": "Europe",
        "description_template": "Transatlantic medical flight services and commercial medical escort repatriation from {origin} to {dest}. Coordinated with leading healthcare facilities and specialists.",
        "routes": [
            ("Montréal", "Paris"),
            ("Toronto (Pearson)", "Frankfurt"),
            ("Toronto (Pearson)", "Amsterdam")
        ]
    },
    "africa": {
        "title": "Africa",
        "description_template": "Premium medical evacuation and long-haul intercontinental ICU transfers from {origin} to {dest}. Features advanced flight planning, refueling stops, and specialized critical-care crews.",
        "routes": [
            ("Toronto (Pearson)", "Lagos"),
            ("Toronto (Pearson)", "Nairobi")
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

for idx, (cat_id, cat_data) in enumerate(categories.items()):
    desc_tmpl = cat_data["description_template"]
    routes = cat_data["routes"]
    
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

section_html = f"""<!-- Critical Transfer Routes from Canada Section -->
    <section class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-12">
                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
                    Critical Transfer Routes from Canada
                </h2>
                <p class="text-on-surface-variant font-body leading-relaxed text-sm">
                    Providing dedicated bed-to-bed ICU air evacuations and commercial airline stretcher services on all
                    major international medical corridors from Canada &mdash; India, Middle East, Europe, Asia, Africa &amp; Worldwide.
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
file_path = "air-ambulance-canada.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!-- Critical Transfer Routes from Canada Section -->"
end_marker = "<!-- Why Families in Canada Rely on Air Medical 24X7 -->"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Markers not found in the file.")
else:
    new_content = content[:start_idx] + section_html + content[end_idx:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully replaced critical route section with flat grid layout in air-ambulance-canada.html!")
