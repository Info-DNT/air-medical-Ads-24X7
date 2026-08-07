import re
import os

# Delete temporary files if they exist
for temp_file in ["air-ambulance-new-delhi.html", "air-ambulance-new-andaman-nicobar.html"]:
    if os.path.exists(temp_file):
        try:
            os.remove(temp_file)
            print(f"Deleted temporary file: {temp_file}")
        except Exception as e:
            print(f"Error deleting {temp_file}: {e}")

# Load template (UK page)
with open("air-ambulance-uk.html", "r", encoding="utf-8") as f:
    template = f.read()

# Helper to make all resource/script/style paths relative for national subfolder
def make_paths_relative(html_content):
    # Convert absolute ads paths to relative paths
    html_content = html_content.replace('href="/ads/styles.css"', 'href="../styles.css"')
    html_content = html_content.replace('href="styles.css"', 'href="../styles.css"')
    html_content = html_content.replace('href="/ads/assets/', 'href="../assets/')
    html_content = html_content.replace('src="/ads/assets/', 'src="../assets/')
    html_content = html_content.replace('href="assets/', 'href="../assets/')
    html_content = html_content.replace('src="assets/', 'src="../assets/')
    html_content = html_content.replace('src="/ads/supabase-config.js"', 'src="../supabase-config.js"')
    html_content = html_content.replace('src="/ads/script.js"', 'src="../script.js"')
    html_content = html_content.replace('src="supabase-config.js"', 'src="../supabase-config.js"')
    html_content = html_content.replace('src="script.js"', 'src="../script.js"')
    return html_content

# Helper to parse routes from a source file
def parse_route_cards(html_content):
    segments = html_content.split('<!-- Route Card:')
    cards = []
    
    for segment in segments[1:]:
        title_match = re.match(r'^(.*?) -->', segment)
        if not title_match:
            continue
        title = title_match.group(1).strip()
        
        arrow_idx = segment.find('trending_flat')
        if arrow_idx == -1:
            continue
            
        before_arrow = segment[:arrow_idx]
        after_arrow = segment[arrow_idx:]
        
        origin_block_match = re.search(r'<div class="flex flex-col text-left">(.*?)</div>', before_arrow, re.DOTALL)
        if origin_block_match:
            origin_html = origin_block_match.group(1).strip()
            origin = re.sub(r'<[^>]+>', ' ', origin_html)
            origin = ' '.join(origin.split())
        else:
            span_matches = re.findall(r'<span[^>]*>(.*?)</span>', before_arrow, re.DOTALL)
            origin = span_matches[-1].strip() if span_matches else "Delhi NCR"
            
        dest_match = re.search(r'</span>\s*(?:<span[^>]*>)?\s*([^<]+?)\s*(?:</span>)?\s*</div>', after_arrow, re.DOTALL)
        if dest_match:
            dest = dest_match.group(1).strip()
        else:
            dest = title.split('to')[-1].strip()
            
        desc_match = re.search(r'<p class="text-on-surface-variant[^>]*>(.*?)</p>', segment, re.DOTALL)
        desc = desc_match.group(1).strip() if desc_match else ""
        desc = desc.replace("specialized", "specialised").replace("Specialized", "Specialised")
        desc = desc.replace("customized", "customised").replace("Customized", "Customised")
        
        wa_match = re.search(r'href="(https://wa\.me/[^"]+)"', segment)
        wa_link = wa_match.group(1).strip() if wa_match else "https://wa.me/16593005200"
        
        cards.append({
            'title': title,
            'origin': origin,
            'destination': dest,
            'description': desc,
            'wa_link': wa_link
        })
        
    return cards

def generate_uk_style_route_card(card):
    origin_html = ""
    if "Port Blair" in card['origin']:
        origin_html = """<span class="leading-tight text-sm font-extrabold">Port Blair</span>
                                    <span class="text-xs text-primary font-bold mt-0.5">(Andaman & Nicobar)</span>"""
    elif card['origin'] in ["Srinagar", "Jammu"]:
        origin_html = f"""<span class="leading-tight text-sm font-extrabold">{card['origin']}</span>
                                    <span class="text-xs text-primary font-bold mt-0.5">(Jammu & Kashmir)</span>"""
    else:
        origin_html = f"""<span class="leading-tight text-sm font-extrabold">{card['origin']}</span>"""
        
    return f"""                    <!-- Route Card: {card['origin']} -> {card['destination']} -->
                    <div
                        class="bg-white p-6 rounded-2xl border border-outline-variant/10 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col justify-between">
                        <div>
                            <div
                                class="flex items-center justify-between font-headline font-black text-primary text-base mb-4">
                                <div class="flex flex-col text-left">
                                    {origin_html}
                                </div>
                                <span
                                    class="material-symbols-outlined text-secondary text-base flex-shrink-0 mx-2">trending_flat</span>
                                <div class="flex flex-col text-right">
                                    <span class="leading-tight text-sm font-extrabold text-right">{card['destination']}</span>
                                </div>
                            </div>
                            <p class="text-on-surface-variant font-body leading-relaxed text-xs mb-6">
                                {card['description']}
                            </p>
                        </div>
                        <div class="pt-4 border-t border-slate-100 flex justify-end">
                            <a href="{card['wa_link']}"
                                target="_blank" rel="noopener noreferrer"
                                class="px-5 py-2.5 bg-secondary text-white rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-primary transition-all shadow-md hover:shadow-lg flex items-center gap-1.5">
                                Get Quote on WhatsApp
                                <span class="material-symbols-outlined text-xs">open_in_new</span>
                            </a>
                        </div>
                    </div>"""

# ----------------- 1. Process Delhi Page (air-ambulance-delhi.html) -----------------
with open("national/air-ambulance-delhi.html", "r", encoding="utf-8") as f:
    delhi_src_html = f.read()
delhi_cards = parse_route_cards(delhi_src_html)

html_delhi = template

# Replace Title, Meta Description, Keywords, Canonical Link
html_delhi = html_delhi.replace(
    '<title>Air Ambulance Service UK &ndash; 24X7 ICU Patient Repatriation</title>',
    '<title>Air Ambulance Service in Delhi NCR – 24X7 ICU Transport</title>'
)
html_delhi = html_delhi.replace(
    '<meta name="description"\n        content="Emergency Air Ambulance &amp; Medical Repatriation UK. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from UK to anywhere globally." />',
    '<meta name="description" content="Emergency Air Ambulance in Delhi NCR. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from Delhi NCR to destinations worldwide." />'
)
html_delhi = html_delhi.replace(
    '<meta name="keywords"\n        content="Air Ambulance Services UK, Air Ambulance UK, Emergency Air Ambulance UK, Medical Evacuation UK, Air Ambulance UK to India, Air Ambulance UK to USA, Airline Stretcher UK, Flight Medical Escort UK" />',
    '<meta name="keywords" content="Air Ambulance Services in Delhi, Air Ambulance Delhi, Emergency Air Ambulance Delhi NCR, Medical Evacuation Delhi, Air Ambulance Delhi to Patna, Air Ambulance Delhi to Mumbai, Airline Stretcher Delhi, Flight Medical Escort Delhi" />'
)
html_delhi = html_delhi.replace(
    '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-uk" />',
    '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-delhi" />'
)

# Localize Schema
old_schema = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "MedicalOrganization"],
      "name": "Air Medical 24X7",
      "url": "https://airmedical24x7.com/air-ambulance-uk",
      "telephone": "+448002294751",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "London",
        "addressRegion": "England",
        "addressCountry": "GB"
      },
      "description": "Emergency Air Ambulance & Medical Repatriation UK. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from UK to anywhere globally.",
      "areaServed": "United Kingdom",
      "medicalSpecialty": "Emergency Medicine",
      "availableService": "Air Ambulance",
      "openingHours": "Mo-Su 00:00-24:00"
    }
    </script>"""

delhi_schema = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "MedicalOrganization"],
      "name": "Air Medical 24X7",
      "url": "https://airmedical24x7.com/air-ambulance-delhi",
      "telephone": "+919217710155",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Delhi NCR",
        "addressRegion": "Delhi",
        "addressCountry": "IN"
      },
      "description": "Emergency Air Ambulance in Delhi NCR. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from Delhi NCR to destinations worldwide.",
      "areaServed": "Delhi NCR, India",
      "medicalSpecialty": "Emergency Medicine",
      "availableService": "Air Ambulance",
      "openingHours": "Mo-Su 00:00-24:00"
    }
    </script>"""

html_delhi = html_delhi.replace(old_schema, delhi_schema)

# Localize Header persistent phone link
html_delhi = html_delhi.replace('href="tel:+448002294751"', 'href="tel:+919217710155"')
html_delhi = html_delhi.replace('+44 800 229 4751', '+91 92177 10155')

# Localize Hero Left Panel Header & Description
hero_title_uk = '24/7 ICU Air Ambulance &amp; Medical Evacuation from the UK'
hero_title_delhi = '24/7 ICU Air Ambulance &amp; Medical Evacuation from Delhi NCR'
html_delhi = html_delhi.replace(hero_title_uk, hero_title_delhi)

hero_desc_uk = 'Global bed-to-bed medical repatriation from anywhere in the UK, including London, Edinburgh, Manchester, Birmingham, and Glasgow, to destinations worldwide. Rapid dispatch with a fully equipped medical crew, providing safe and reliable transfers from the UK to anywhere in the world.'
hero_desc_delhi = 'Global bed-to-bed medical repatriation from anywhere in Delhi NCR, including Central Delhi, South Delhi, Gurugram, Noida, and Ghaziabad, to destinations worldwide. Rapid dispatch with a fully equipped medical crew, providing safe and reliable transfers from Delhi to anywhere in the world.'
html_delhi = html_delhi.replace(hero_desc_uk, hero_desc_delhi)

# Replace Form placeholders in Delhi
html_delhi = html_delhi.replace('placeholder="e.g. London, Birmingham"', 'placeholder="e.g. Delhi NCR, Noida, Gurugram"')
html_delhi = html_delhi.replace('placeholder="e.g. Delhi, Mumbai, Dubai"', 'placeholder="e.g. Patna, Mumbai, Kolkata"')

# Replace Left Panel Sidebar content
delhi_sidebar_html = """<!-- Destinations Grid by Region — 3 columns, no scroll -->
                            <div class="space-y-2">

                                <!-- Northern Region -->
                                <div>
                                    <a href="#region-north" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Northern Region</a>
                                    <ul
                                        class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-north" class="hover:text-secondary hover:underline transition-all">Srinagar</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-north" class="hover:text-secondary hover:underline transition-all">Lucknow</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-north" class="hover:text-secondary hover:underline transition-all">Jaipur</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-north" class="hover:text-secondary hover:underline transition-all">Jammu</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-north" class="hover:text-secondary hover:underline transition-all">Leh</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-north" class="hover:text-secondary hover:underline transition-all">Varanasi</a></li>
                                    </ul>
                                </div>

                                <!-- Southern Region -->
                                <div>
                                    <a href="#region-south" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Southern Region</a>
                                    <ul
                                        class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-south" class="hover:text-secondary hover:underline transition-all">Hyderabad</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-south" class="hover:text-secondary hover:underline transition-all">Bengaluru</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-south" class="hover:text-secondary hover:underline transition-all">Chennai</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-south" class="hover:text-secondary hover:underline transition-all">Kochi</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-south" class="hover:text-secondary hover:underline transition-all">Kozhikode</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-south" class="hover:text-secondary hover:underline transition-all">Vizag</a></li>
                                    </ul>
                                </div>

                                <!-- Eastern Region -->
                                <div>
                                    <a href="#region-east" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Eastern Region</a>
                                    <ul
                                        class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-east" class="hover:text-secondary hover:underline transition-all">Patna</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-east" class="hover:text-secondary hover:underline transition-all">Kolkata</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-east" class="hover:text-secondary hover:underline transition-all">Ranchi</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-east" class="hover:text-secondary hover:underline transition-all">Jamshedpur</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-east" class="hover:text-secondary hover:underline transition-all">Bhubaneswar</a></li>
                                        <li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="#region-east" class="hover:text-secondary hover:underline transition-all">Raipur</a></li>
                                    </ul>
                                </div>
                            </div>"""

# Replace Left Panel
left_panel_regex = r'<!-- Left Panel: Navy / Info -->.*?<!-- Right Panel: White / Quote Form -->'
new_left_panel_delhi = f"""<!-- Left Panel: Navy / Info -->
                    <div
                        class="bg-primary p-8 md:p-10 text-white hidden lg:flex flex-col justify-center relative overflow-hidden group">
                        <div
                            class="absolute inset-0 bg-gradient-to-br from-primary to-primary-container opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                        </div>
                        <div class="relative z-10">
                            <h1 class="font-headline text-xl font-extrabold leading-tight mb-3">
                                {hero_title_delhi}
                            </h1>
                            <p class="text-xs text-slate-300 mb-4 leading-relaxed">
                                {hero_desc_delhi}
                            </p>
                            {delhi_sidebar_html}
                        </div>
                        <!-- Decorative icon -->
                        <div
                            class="absolute -bottom-10 -right-10 opacity-10 group-hover:opacity-20 transition-opacity duration-500 group-hover:scale-110 transform">
                            <span class="material-symbols-outlined text-[200px]">support_agent</span>
                        </div>
                    </div>

                    <!-- Right Panel: White / Quote Form -->"""

html_delhi = re.sub(left_panel_regex, new_left_panel_delhi, html_delhi, flags=re.DOTALL)

# Stats section
html_delhi = html_delhi.replace('UK Command Center', 'Delhi NCR Command Center')

# Cost section
html_delhi = html_delhi.replace('Air Ambulance &amp; Airline Stretcher Costs from UK', 'Air Ambulance &amp; Airline Stretcher Costs from Delhi NCR')
html_delhi = html_delhi.replace('repatriation from the UK', 'repatriation from Delhi NCR')
html_delhi = html_delhi.replace('evacuations from the UK', 'evacuations from Delhi NCR')
html_delhi = html_delhi.replace('Call UK Emergency Desk', 'Call India Emergency Desk')
html_delhi = html_delhi.replace(
    'We provide medical transfers from major UK cities, including <strong>London, Edinburgh, Manchester, Birmingham, and Glasgow</strong>, to destinations across Europe, Asia, the Middle East, North America, and worldwide, ensuring seamless bedside-to-bedside patient transportation.',
    'We provide medical transfers from all major areas of Delhi NCR, including Noida, Gurugram, Ghaziabad, and Faridabad, to destinations across India and worldwide, ensuring seamless bedside-to-bedside patient transportation.'
)
html_delhi = html_delhi.replace('src="assets/air-ambulance-uk.jfif" alt="Air Ambulance UK London Pricing"', 'src="assets/Delhi_airport.jfif" alt="Air Ambulance Delhi Airport Pricing"')

# Group Delhi routes into 5 regions
regions = {
    'north': {
        'title': 'Northern India Routes',
        'destinations': ['Srinagar', 'Jammu', 'Leh', 'Lucknow', 'Varanasi', 'Gorakhpur', 'Prayagraj', 'Jaipur', 'Jodhpur', 'Bikaner', 'Dehradun', 'Amritsar'],
        'cards': []
    },
    'south': {
        'title': 'Southern India Routes',
        'destinations': ['Hyderabad', 'Bengaluru', 'Chennai', 'Kochi', 'Kozhikode', 'Visakhapatnam'],
        'cards': []
    },
    'east': {
        'title': 'Eastern India Routes',
        'destinations': ['Patna', 'Darbhanga', 'Ranchi', 'Jamshedpur', 'Kolkata', 'Bhubaneswar', 'Raipur'],
        'cards': []
    },
    'west': {
        'title': 'Western & Central India Routes',
        'destinations': ['Pune', 'Mumbai', 'Ahmedabad', 'Indore', 'Bhopal'],
        'cards': []
    },
    'northeast': {
        'title': 'North-East India & Islands',
        'destinations': ['Guwahati', 'Dibrugarh', 'Silchar', 'Imphal', 'Agartala', 'Shillong', 'Aizawl', 'Itanagar', 'Dimapur', 'Port Blair'],
        'cards': []
    }
}

for card in delhi_cards:
    dest = card['destination']
    matched = False
    for r_key, r_info in regions.items():
        if dest in r_info['destinations']:
            r_info['cards'].append(card)
            matched = True
            break
    if not matched:
        regions['north']['cards'].append(card)

# Build accordions HTML
accordions_html = ""
for r_key, r_info in regions.items():
    region_cards_html = "\n".join([generate_uk_style_route_card(c) for c in r_info['cards']])
    
    accordions_html += f"""
            <!-- Region Accordion: {r_info['title']} -->
            <div id="region-{r_key}"
                class="mb-6 border border-slate-200/60 dark:border-slate-800/60 rounded-2xl overflow-hidden bg-white shadow-sm transition-all duration-300">
                <!-- Accordion Header Button -->
                <button
                    class="w-full px-6 py-5 flex items-center justify-between bg-slate-50/50 hover:bg-slate-50 transition-colors text-left focus:outline-none group"
                    onclick="toggleRegion('{r_key}')">
                    <span
                        class="font-headline text-base md:text-lg font-black text-primary uppercase tracking-wide">{r_info['title']}</span>
                    <span
                        class="material-symbols-outlined text-secondary text-2xl transform transition-transform duration-300 ease-in-out"
                        id="icon-region-{r_key}">keyboard_arrow_down</span>
                </button>
                <!-- Accordion Content (Collapsed by Default) -->
                <div class="hidden transition-all duration-300 ease-in-out border-t border-slate-100"
                    id="content-region-{r_key}">
                    <div class="p-6">
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
{region_cards_html}
                        </div>
                    </div>
                </div>
            </div>"""

new_routes_section = f"""    <section id="routes-section"
        class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-12">
                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
                    Critical Evacuation Routes from Delhi NCR
                </h2>
                <p class="text-on-surface-variant font-body leading-relaxed text-sm">
                    Providing dedicated bed-to-bed ICU air evacuations with fully configured medical teams on standby on all major corridors from Delhi NCR.
                </p>
            </div>

            <div class="max-w-6xl mx-auto">
{accordions_html}
            </div>
        </div>
    </section>"""

# Replace the routes section
routes_section_regex_template = r'<section id="routes-section".*?(?=<section id="services"|<!-- Services Grid -->)'
html_delhi = re.sub(routes_section_regex_template, new_routes_section + "\n\n", html_delhi, flags=re.DOTALL)

# Localize FAQs
html_delhi = html_delhi.replace('insurance coordination for UK', 'insurance coordination for India')
html_delhi = html_delhi.replace('How much does an Air Ambulance Cost from the UK?', 'How much does an Air Ambulance Cost from Delhi NCR?')
html_delhi = html_delhi.replace('air ambulance cost from the UK', 'air ambulance cost from Delhi NCR')
html_delhi = html_delhi.replace('regions in the UK do you cover', 'regions in Delhi NCR do you cover')
html_delhi = html_delhi.replace('managed by our UK operations team', 'managed by our operations team')
html_delhi = html_delhi.replace('air ambulance be arranged from UK?', 'air ambulance be arranged from Delhi NCR?')
html_delhi = html_delhi.replace('Our UK team responds to', 'Our operations team responds to')
html_delhi = html_delhi.replace('services from UK?', 'services from Delhi NCR?')
html_delhi = html_delhi.replace('Many UK health insurance', 'Many Indian health insurance')
html_delhi = html_delhi.replace('ground ambulance in UK coordinated', 'ground ambulance in Delhi NCR coordinated')
html_delhi = html_delhi.replace('Our UK operations team coordinates', 'Our operations team coordinates')

# Localize Footer UK helpline
html_delhi = html_delhi.replace('24X7 UK Emergency Helpline', '24X7 India Emergency Helpline')

# Localize Why Families Section
html_delhi = html_delhi.replace('<!-- Why Families in UK Rely on Air Medical 24X7 -->', '<!-- Why Families in India Rely on Air Medical 24X7 -->')
html_delhi = html_delhi.replace('Why Families in the UK Rely on Air Medical 24X7', 'Why Families in India Rely on Air Medical 24X7')
html_delhi = html_delhi.replace('thousands of UK families', 'thousands of families in India')
html_delhi = html_delhi.replace('UK Operations &mdash; Rapid Local Response', 'India Operations &mdash; Rapid Response')
html_delhi = html_delhi.replace('Our UK desk handles\n                                    NHS hospital liaisons, London airport clearances (Heathrow, Gatwick, Stansted), and ground ambulance dispatch &mdash; ensuring swift response across England, Scotland, Wales, and Northern Ireland.',
                                'Our local operations coordinate ground ambulance dispatch, airport coordination, and flight logistics &mdash; ensuring the fastest possible response across all major cities and regions in India.')
html_delhi = html_delhi.replace('across all\n                                    UK departures.', 'across all\n                                    departures from India.')

# Save Delhi page (overwriting air-ambulance-delhi.html)
html_delhi = make_paths_relative(html_delhi)
with open("national/air-ambulance-delhi.html", "w", encoding="utf-8") as f:
    f.write(html_delhi)
print("Saved national/air-ambulance-delhi.html")


# ----------------- 2. Process Andaman Page (air-ambulance-portblair.html) -----------------
with open("national/air-ambulance-portblair.html", "r", encoding="utf-8") as f:
    andaman_src_html = f.read()
andaman_cards = parse_route_cards(andaman_src_html)

html_andaman = template

# Replace Title, Meta Description, Keywords, Canonical Link
html_andaman = html_andaman.replace(
    '<title>Air Ambulance Service UK &ndash; 24X7 ICU Patient Repatriation</title>',
    '<title>Air Ambulance Service in Port Blair, Andaman & Nicobar – 24X7 ICU Transport</title>'
)
html_andaman = html_andaman.replace(
    '<meta name="description"\n        content="Emergency Air Ambulance &amp; Medical Repatriation UK. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from UK to anywhere globally." />',
    '<meta name="description" content="Emergency Air Ambulance in Andaman & Nicobar. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from Port Blair to destinations worldwide." />'
)
html_andaman = html_andaman.replace(
    '<meta name="keywords"\n        content="Air Ambulance Services UK, Air Ambulance UK, Emergency Air Ambulance UK, Medical Evacuation UK, Air Ambulance UK to India, Air Ambulance UK to USA, Airline Stretcher UK, Flight Medical Escort UK" />',
    '<meta name="keywords" content="Air Ambulance Services in Andaman, Air Ambulance Port Blair, Emergency Air Ambulance Andaman & Nicobar, Medical Evacuation Andaman, Air Ambulance Port Blair to Chennai, Air Ambulance Port Blair to Kolkata, Airline Stretcher Port Blair, Flight Medical Escort Port Blair" />'
)
html_andaman = html_andaman.replace(
    '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-uk" />',
    '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-portblair" />'
)

# Localize Schema
andaman_schema = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "MedicalOrganization"],
      "name": "Air Medical 24X7",
      "url": "https://airmedical24x7.com/air-ambulance-portblair",
      "telephone": "+919217710155",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Port Blair",
        "addressRegion": "Andaman & Nicobar Islands",
        "addressCountry": "IN"
      },
      "description": "Emergency Air Ambulance in Andaman & Nicobar. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from Port Blair to destinations worldwide.",
      "areaServed": "Andaman & Nicobar Islands",
      "medicalSpecialty": "Emergency Medicine",
      "availableService": "Air Ambulance",
      "openingHours": "Mo-Su 00:00-24:00"
    }
    </script>"""

html_andaman = html_andaman.replace(old_schema, andaman_schema)

# Localize Header persistent phone link
html_andaman = html_andaman.replace('href="tel:+448002294751"', 'href="tel:+919217710155"')
html_andaman = html_andaman.replace('+44 800 229 4751', '+91 92177 10155')

# Localize Hero Left Panel Header & Description
hero_title_andaman = '24/7 ICU Air Ambulance &amp; Medical Evacuation from Andaman &amp; Nicobar'
html_andaman = html_andaman.replace(hero_title_uk, hero_title_andaman)

hero_desc_andaman = 'Global bed-to-bed medical repatriation from anywhere in Andaman & Nicobar, including Port Blair, Havelock Island, Neil Island, and Mayabunder, to destinations worldwide. Rapid dispatch with a fully equipped medical crew, providing safe and reliable transfers from Port Blair to anywhere in the world.'
html_andaman = html_andaman.replace(hero_desc_uk, hero_desc_andaman)

# Replace Form placeholders in Andaman
html_andaman = html_andaman.replace('placeholder="e.g. London, Birmingham"', 'placeholder="e.g. Port Blair, Havelock, Neil Island"')
html_andaman = html_andaman.replace('placeholder="e.g. Delhi, Mumbai, Dubai"', 'placeholder="e.g. Chennai, Kolkata, Delhi"')

# Replace sidebar destinations grid
andaman_sidebar_html = """<!-- Destinations Grid — 1 column list -->
                            <div class="space-y-2 mb-5">
                                <div>
                                    <h2 class="text-[8px] font-black uppercase tracking-[0.18em] text-white mb-2">Mainland Evacuation Corridors</h2>
                                    <ul class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10px] text-slate-200 font-bold">
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Port Blair to Chennai</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Port Blair to Delhi NCR</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Port Blair to Kolkata</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Port Blair to Bengaluru</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Port Blair to Hyderabad</li>
                                    </ul>
                                </div>
                            </div>"""

new_left_panel_andaman = f"""<!-- Left Panel: Navy / Info -->
                    <div
                        class="bg-primary p-8 md:p-10 text-white hidden lg:flex flex-col justify-center relative overflow-hidden group">
                        <div
                            class="absolute inset-0 bg-gradient-to-br from-primary to-primary-container opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                        </div>
                        <div class="relative z-10">
                            <h1 class="font-headline text-xl font-extrabold leading-tight mb-3">
                                {hero_title_andaman}
                            </h1>
                            <p class="text-xs text-slate-300 mb-4 leading-relaxed">
                                {hero_desc_andaman}
                            </p>
                            {andaman_sidebar_html}
                        </div>
                        <!-- Decorative icon -->
                        <div
                            class="absolute -bottom-10 -right-10 opacity-10 group-hover:opacity-20 transition-opacity duration-500 group-hover:scale-110 transform">
                            <span class="material-symbols-outlined text-[200px]">support_agent</span>
                        </div>
                    </div>

                    <!-- Right Panel: White / Quote Form -->"""

html_andaman = re.sub(left_panel_regex, new_left_panel_andaman, html_andaman, flags=re.DOTALL)

# Stats section
html_andaman = html_andaman.replace('UK Command Center', 'Andaman Operations Command Center')

# Cost section
html_andaman = html_andaman.replace('Air Ambulance &amp; Airline Stretcher Costs from UK', 'Air Ambulance &amp; Airline Stretcher Costs from Andaman & Nicobar')
html_andaman = html_andaman.replace('repatriation from the UK', 'repatriation from Andaman & Nicobar')
html_andaman = html_andaman.replace('evacuations from the UK', 'evacuations from Andaman & Nicobar')
html_andaman = html_andaman.replace('Call UK Emergency Desk', 'Call India Emergency Desk')
html_andaman = html_andaman.replace(
    'We provide medical transfers from major UK cities, including <strong>London, Edinburgh, Manchester, Birmingham, and Glasgow</strong>, to destinations across Europe, Asia, the Middle East, North America, and worldwide, ensuring seamless bedside-to-bedside patient transportation.',
    'We provide medical transfers from all major locations in Andaman & Nicobar, including Port Blair, Havelock Island, Neil Island, and Mayabunder, to mainland Indian cities (Chennai, Delhi, Kolkata, Bengaluru, Hyderabad) and worldwide, ensuring seamless bedside-to-bedside patient transportation.'
)
html_andaman = html_andaman.replace('src="assets/air-ambulance-uk.jfif" alt="Air Ambulance UK London Pricing"', 'src="assets/airport_port_blair_andaman.jpg.jpg" alt="Air Ambulance Port Blair Airport Pricing"')

# Build Andaman routes section (clean grid list)
andaman_cards_html = "\n".join([generate_uk_style_route_card(c) for c in andaman_cards])

new_andaman_routes_section = f"""    <section id="routes-section"
        class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-12">
                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
                    Critical Evacuation Routes from Andaman & Nicobar
                </h2>
                <p class="text-on-surface-variant font-body leading-relaxed text-sm">
                    Providing dedicated bed-to-bed ICU air evacuations with fully configured medical teams on standby on all major corridors from Andaman & Nicobar.
                </p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
{andaman_cards_html}
            </div>
        </div>
    </section>"""

html_andaman = re.sub(routes_section_regex_template, new_andaman_routes_section + "\n\n", html_andaman, flags=re.DOTALL)

# Localize FAQs
html_andaman = html_andaman.replace('insurance coordination for UK', 'insurance coordination for India')
html_andaman = html_andaman.replace('How much does an Air Ambulance Cost from the UK?', 'How much does an Air Ambulance Cost from Andaman & Nicobar?')
html_andaman = html_andaman.replace('air ambulance cost from the UK', 'air ambulance cost from Andaman & Nicobar')
html_andaman = html_andaman.replace('regions in the UK do you cover', 'regions in Andaman & Nicobar do you cover')
html_andaman = html_andaman.replace('managed by our UK operations team', 'managed by our operations team')
html_andaman = html_andaman.replace('air ambulance be arranged from UK?', 'air ambulance be arranged from Andaman & Nicobar?')
html_andaman = html_andaman.replace('Our UK team responds to', 'Our operations team responds to')
html_andaman = html_andaman.replace('services from UK?', 'services from Andaman & Nicobar?')
html_andaman = html_andaman.replace('Many UK health insurance', 'Many Indian health insurance')
html_andaman = html_andaman.replace('ground ambulance in UK coordinated', 'ground ambulance in Andaman & Nicobar coordinated')
html_andaman = html_andaman.replace('Our UK operations team coordinates', 'Our operations team coordinates')

# Localize Footer UK helpline
html_andaman = html_andaman.replace('24X7 UK Emergency Helpline', '24X7 India Emergency Helpline')

# Localize Why Families Section
html_andaman = html_andaman.replace('<!-- Why Families in UK Rely on Air Medical 24X7 -->', '<!-- Why Families in Andaman and Nicobar Rely on Air Medical 24X7 -->')
html_andaman = html_andaman.replace('Why Families in the UK Rely on Air Medical 24X7', 'Why Families in Andaman and Nicobar Rely on Air Medical 24X7')
html_andaman = html_andaman.replace('thousands of UK families', 'thousands of families in India')
html_andaman = html_andaman.replace('UK Operations &mdash; Rapid Local Response', 'India Operations &mdash; Rapid Response')
html_andaman = html_andaman.replace('Our UK desk handles\n                                    NHS hospital liaisons, London airport clearances (Heathrow, Gatwick, Stansted), and ground ambulance dispatch &mdash; ensuring swift response across England, Scotland, Wales, and Northern Ireland.',
                                     'Our local operations coordinate ground ambulance dispatch, airport coordination, and flight logistics &mdash; ensuring the fastest possible response across all major cities and regions in India.')
html_andaman = html_andaman.replace('across all\n                                    UK departures.', 'across all\n                                    departures from India.')

# Save Andaman page (overwriting air-ambulance-portblair.html)
html_andaman = make_paths_relative(html_andaman)
with open("national/air-ambulance-portblair.html", "w", encoding="utf-8") as f:
    f.write(html_andaman)
print("Saved national/air-ambulance-portblair.html")


# ----------------- 3. Process Jammu & Kashmir Page (air-ambulance-jammu-kashmir.html) -----------------
with open("national/air-ambulance-jammu-kashmir.html", "r", encoding="utf-8") as f:
    jk_src_html = f.read()

jk_all_cards = parse_route_cards(jk_src_html)

# Get unique cards
seen = set()
jk_cards = []
for c in jk_all_cards:
    key = (c['origin'].strip(), c['destination'].strip())
    if key not in seen:
        seen.add(key)
        jk_cards.append(c)

def find_card(cards, origin, dest):
    for c in cards:
        if c['origin'].strip() == origin and c['destination'].strip() == dest:
            return c
    # Fallback if card is missing
    return {
        'title': f"{origin} to {dest}",
        'origin': origin,
        'destination': dest,
        'description': f"Emergency ICU medical flights and patient transfer from {origin} to {dest}, connecting you to top hospitals for specialized treatments.",
        'wa_link': f"https://wa.me/16593005200?text=I%20need%20Assistance%20with%20Patient%20Air%20Transfer%20from%20{origin}%20to%20{dest}.%20Please%20Assist!"
    }

html_jk = template

# Replace Title, Meta Description, Keywords, Canonical Link
html_jk = html_jk.replace(
    '<title>Air Ambulance Service UK &ndash; 24X7 ICU Patient Repatriation</title>',
    '<title>Air Ambulance Services in Jammu & Kashmir | Srinagar & Jammu ICU Medical Evacuation 24X7</title>'
)
html_jk = html_jk.replace(
    '<meta name="description"\n        content="Emergency Air Ambulance &amp; Medical Repatriation UK. Rapid response medical flights, commercial airline stretcher, and bed-to-bed patient transfer from UK to anywhere globally." />',
    '<meta name="description" content="24/7 Air Ambulance Services and ICU medical flights from Srinagar, Jammu and Jammu & Kashmir to Delhi, Mumbai, and worldwide. Patient transfers, commercial airline stretchers, and medical escorts. Get a quote within 30 minutes." />'
)
html_jk = html_jk.replace(
    '<meta name="keywords"\n        content="Air Ambulance Services UK, Air Ambulance UK, Emergency Air Ambulance UK, Medical Evacuation UK, Air Ambulance UK to India, Air Ambulance UK to USA, Airline Stretcher UK, Flight Medical Escort UK" />',
    '<meta name="keywords" content="Air Ambulance Jammu Kashmir, Air Ambulance Srinagar, Air Ambulance Jammu, Medical Evacuation Srinagar, Emergency Flight Srinagar, ICU Air Ambulance Jammu, Airline Stretcher Jammu, Flight Medical Escort Srinagar, Patient Transfer Jammu Kashmir" />'
)
html_jk = html_jk.replace(
    '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-uk" />',
    '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-jammu-kashmir" />'
)

# Localize Schema
jk_schema = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "MedicalOrganization"],
      "name": "Air Medical 24X7 Jammu & Kashmir",
      "url": "https://airmedical24x7.com/air-ambulance-jammu-kashmir",
      "telephone": "+919217710155",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Srinagar & Jammu",
        "addressRegion": "Jammu & Kashmir",
        "addressCountry": "IN"
      },
      "description": "24X7 Air Ambulance and Medical Evacuation Services from Srinagar, Jammu and Jammu & Kashmir to major hospitals (Delhi, Mumbai, Chandigarh) and worldwide.",
      "areaServed": "Srinagar, Jammu, Leh, Anantnag, Baramulla, Kathua, Samba, Udhampur, Poonch, Kupwara, Pulwama, Sopore",
      "medicalSpecialty": "Emergency Medicine",
      "availableService": "Air Ambulance",
      "openingHours": "Mo-Su 00:00-24:00"
    }
    </script>"""

html_jk = html_jk.replace(old_schema, jk_schema)

# Localize Header persistent phone link
html_jk = html_jk.replace('href="tel:+448002294751"', 'href="tel:+919217710155"')
html_jk = html_jk.replace('+44 800 229 4751', '+91 92177 10155')

# Localize Hero Left Panel Header & Description
hero_title_jk = '24/7 ICU Air Ambulance &amp; Medical Evacuation from Jammu &amp; Kashmir'
hero_desc_jk = 'Emergency medical repatriation from anywhere in Jammu & Kashmir, including Srinagar, Jammu, Leh, Anantnag, Baramulla, Kathua, Samba, Udhampur, Poonch, Kupwara, Pulwama, and Sopore, to destinations worldwide. Rapid dispatch with a fully equipped medical crew, providing safe and reliable transfers from Srinagar or Jammu to anywhere in the world.'
html_jk = html_jk.replace(hero_title_uk, hero_title_jk)
html_jk = html_jk.replace(hero_desc_uk, hero_desc_jk)

# Replace Form placeholders in J&K
html_jk = html_jk.replace('placeholder="e.g. London, Birmingham"', 'placeholder="e.g. Srinagar, Jammu, Leh"')
html_jk = html_jk.replace('placeholder="e.g. Delhi, Mumbai, Dubai"', 'placeholder="e.g. New Delhi, Mumbai, Chandigarh"')

# Replace sidebar destinations grid
jk_sidebar_html = """<!-- Destinations Grid — 3 columns -->
                            <div class="space-y-2 mb-5">
                                <div>
                                    <h2 class="text-[8px] font-black uppercase tracking-[0.18em] text-white mb-2">Mainland Evacuation Corridors</h2>
                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-1 text-[10px] text-slate-200 font-bold">
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to New Delhi</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Chandigarh</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Amritsar</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Mumbai</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Hyderabad</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Bengaluru</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Chennai</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Kolkata</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Ahmedabad</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Lucknow</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Jaipur</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Pune</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Kochi</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Dehradun</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Gurugram</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Noida</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Ludhiana</li>
                                        <li class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0"></span>Jammu & Kashmir to Jalandhar</li>
                                    </ul>
                                </div>
                            </div>"""

new_left_panel_jk = f"""<!-- Left Panel: Navy / Info -->
                    <div
                        class="bg-primary p-8 md:p-10 text-white hidden lg:flex flex-col justify-center relative overflow-hidden group">
                        <div
                            class="absolute inset-0 bg-gradient-to-br from-primary to-primary-container opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                        </div>
                        <div class="relative z-10">
                            <h1 class="font-headline text-xl font-extrabold leading-tight mb-3">
                                {hero_title_jk}
                            </h1>
                            <p class="text-xs text-slate-300 mb-4 leading-relaxed">
                                {hero_desc_jk}
                            </p>
                            {jk_sidebar_html}
                        </div>
                        <!-- Decorative icon -->
                        <div
                            class="absolute -bottom-10 -right-10 opacity-10 group-hover:opacity-20 transition-opacity duration-500 group-hover:scale-110 transform">
                            <span class="material-symbols-outlined text-[200px]">support_agent</span>
                        </div>
                    </div>

                    <!-- Right Panel: White / Quote Form -->"""

html_jk = re.sub(left_panel_regex, new_left_panel_jk, html_jk, flags=re.DOTALL)

# Stats section
html_jk = html_jk.replace('UK Command Center', 'Jammu & Kashmir Operations Command Center')

# Cost section
html_jk = html_jk.replace('Air Ambulance &amp; Airline Stretcher Costs from UK', 'Air Ambulance &amp; Airline Stretcher Costs from Jammu & Kashmir')
html_jk = html_jk.replace('repatriation from the UK', 'repatriation from Jammu & Kashmir')
html_jk = html_jk.replace('evacuations from the UK', 'evacuations from Jammu & Kashmir')
html_jk = html_jk.replace('Call UK Emergency Desk', 'Call India Emergency Desk')
html_jk = html_jk.replace(
    'We provide medical transfers from major UK cities, including <strong>London, Edinburgh, Manchester, Birmingham, and Glasgow</strong>, to destinations across Europe, Asia, the Middle East, North America, and worldwide, ensuring seamless bedside-to-bedside patient transportation.',
    'We provide medical transfers from all major locations in Jammu & Kashmir, including Srinagar, Jammu, and Leh, to leading super-specialty hospitals in Delhi NCR, Mumbai, and worldwide, ensuring seamless bedside-to-bedside patient transportation.'
)
html_jk = html_jk.replace('src="assets/air-ambulance-uk.jfif" alt="Air Ambulance UK London Pricing"', 'src="../assets/airport_jammu_jk.jpg.jpg" alt="Air Ambulance Cost from Jammu & Kashmir"')

# Build 24 Most Requested routes cards
req_dests = ['New Delhi', 'Mumbai', 'Hyderabad', 'Bengaluru', 'Chennai', 'Kolkata', 'Ahmedabad', 'Lucknow', 'Jaipur', 'Chandigarh', 'Amritsar']
most_requested_cards = []

for d in req_dests + ['Jammu']:
    card = find_card(jk_cards, "Srinagar", d)
    most_requested_cards.append(generate_uk_style_route_card(card))
    
for d in req_dests + ['Srinagar']:
    card = find_card(jk_cards, "Jammu", d)
    most_requested_cards.append(generate_uk_style_route_card(card))
    
most_requested_grid_html = "\n".join(most_requested_cards)

# Build collapsible regions (accordions)
regions_data = {
    'north-india': {
        'title': 'North India',
        'routes': [
            ("Srinagar", "New Delhi"), ("Srinagar", "Noida"), ("Srinagar", "Gurugram"), ("Srinagar", "Ghaziabad"), ("Srinagar", "Faridabad"), 
            ("Srinagar", "Chandigarh"), ("Srinagar", "Amritsar"), ("Srinagar", "Ludhiana"), ("Srinagar", "Jalandhar"), ("Srinagar", "Jaipur"), 
            ("Srinagar", "Lucknow"), ("Srinagar", "Kanpur"), ("Srinagar", "Dehradun"), ("Srinagar", "Varanasi"), ("Srinagar", "Jammu"), ("Srinagar", "Leh"),
            ("Jammu", "New Delhi"), ("Jammu", "Noida"), ("Jammu", "Gurugram"), ("Jammu", "Ghaziabad"), ("Jammu", "Faridabad"), 
            ("Jammu", "Chandigarh"), ("Jammu", "Amritsar"), ("Jammu", "Ludhiana"), ("Jammu", "Jalandhar"), ("Jammu", "Jaipur"), 
            ("Jammu", "Lucknow"), ("Jammu", "Kanpur"), ("Jammu", "Dehradun"), ("Jammu", "Varanasi"), ("Jammu", "Srinagar"), ("Jammu", "Leh")
        ]
    },
    'south-india': {
        'title': 'South India',
        'routes': [
            ("Srinagar", "Chennai"), ("Srinagar", "Bengaluru"), ("Srinagar", "Hyderabad"), ("Srinagar", "Kochi"), ("Srinagar", "Coimbatore"), 
            ("Srinagar", "Thiruvananthapuram"), ("Srinagar", "Visakhapatnam"),
            ("Jammu", "Chennai"), ("Jammu", "Bengaluru"), ("Jammu", "Hyderabad"), ("Jammu", "Kochi")
        ]
    },
    'west-india': {
        'title': 'West India',
        'routes': [
            ("Srinagar", "Mumbai"), ("Srinagar", "Pune"), ("Srinagar", "Ahmedabad"), ("Srinagar", "Goa"),
            ("Jammu", "Mumbai"), ("Jammu", "Pune"), ("Jammu", "Ahmedabad"), ("Jammu", "Goa")
        ]
    },
    'central-india': {
        'title': 'Central India',
        'routes': [
            ("Srinagar", "Nagpur"), ("Srinagar", "Indore"), ("Srinagar", "Bhopal"), ("Srinagar", "Raipur"),
            ("Jammu", "Nagpur"), ("Jammu", "Indore"), ("Jammu", "Bhopal")
        ]
    },
    'east-india': {
        'title': 'East India',
        'routes': [
            ("Srinagar", "Kolkata"), ("Srinagar", "Bhubaneswar"), ("Srinagar", "Ranchi"), ("Srinagar", "Patna"),
            ("Jammu", "Kolkata"), ("Jammu", "Bhubaneswar"), ("Jammu", "Ranchi"), ("Jammu", "Patna")
        ]
    },
    'northeast-india': {
        'title': 'North-East India',
        'routes': [
            ("Srinagar", "Guwahati"),
            ("Jammu", "Guwahati")
        ]
    }
}

accordions = []
for r_key, r_info in regions_data.items():
    r_cards = []
    for origin, dest in r_info['routes']:
        card = find_card(jk_cards, origin, dest)
        r_cards.append(generate_uk_style_route_card(card))
        
    r_cards_html = "\n".join(r_cards)
    
    accordion = f"""            <!-- Region: {r_info['title']} -->
            <div class="border border-outline-variant/10 rounded-2xl overflow-hidden bg-white shadow-sm transition-all duration-300">
                <button class="w-full flex justify-between items-center p-6 text-left font-headline font-bold text-primary hover:text-secondary transition-colors" onclick="toggleRegion('{r_key}')">
                    <span>{r_info['title']}</span>
                    <span class="material-symbols-outlined text-secondary text-2xl transform transition-transform duration-300 ease-in-out" id="icon-region-{r_key}">keyboard_arrow_down</span>
                </button>
                <div class="hidden transition-all duration-300 ease-in-out border-t border-slate-100" id="content-region-{r_key}">
                    <div class="p-6">
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
{r_cards_html}
                        </div>
                    </div>
                </div>
            </div>"""
    accordions.append(accordion)
    
accordions_html = "\n".join(accordions)

new_jk_routes_section = f"""    <section id="routes-section" class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-12">
                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
                    Critical Evacuation Routes from Jammu & Kashmir
                </h2>
                <p class="text-on-surface-variant font-body leading-relaxed text-sm">
                    Providing dedicated bed-to-bed ICU air ambulance and commercial airline stretcher services, serving patients from Srinagar, Jammu, Leh and the surrounding Jammu & Kashmir regions with seamless end-to-end medical transportation.
                </p>
            </div>

            <!-- Most Requested Transfer Routes -->
            <div id="popular-routes" class="mb-14">
                <h3 class="font-headline text-lg font-extrabold uppercase tracking-widest text-primary mb-6 border-l-4 border-secondary pl-3">
                    Most Requested Transfer Routes
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{most_requested_grid_html}
                </div>
            </div>

            <!-- Collapsible Region Groups -->
            <div class="space-y-4 max-w-6xl mx-auto mt-12">
{accordions_html}
            </div>
        </div>
    </section>"""

html_jk = re.sub(routes_section_regex_template, new_jk_routes_section + "\n\n", html_jk, flags=re.DOTALL)

# Localize Why Families Section
html_jk = html_jk.replace('<!-- Why Families in UK Rely on Air Medical 24X7 -->', '<!-- Why Families in Jammu Kashmir Rely on Air Medical 24X7 -->')
html_jk = html_jk.replace('Why Families in the UK Rely on Air Medical 24X7', 'Why Families in Jammu Kashmir Rely on Air Medical 24X7')
html_jk = html_jk.replace('thousands of UK families', 'thousands of families in India')
html_jk = html_jk.replace('UK Operations &mdash; Rapid Local Response', 'India Operations &mdash; Rapid Response')
html_jk = html_jk.replace('Our UK desk handles\n                                    NHS hospital liaisons, London airport clearances (Heathrow, Gatwick, Stansted), and ground ambulance dispatch &mdash; ensuring swift response across England, Scotland, Wales, and Northern Ireland.',
                          'Our local operations coordinate ground ambulance dispatch, airport coordination, and flight logistics &mdash; ensuring the fastest possible response across all major cities and regions in India.')
html_jk = html_jk.replace('across all\n                                    UK departures.', 'across all\n                                    departures from India.')

# Localize FAQs
html_jk = html_jk.replace('insurance coordination for UK', 'insurance coordination for India')
html_jk = html_jk.replace('How much does an Air Ambulance Cost from the UK?', 'How much does an Air Ambulance Cost from Jammu & Kashmir?')
html_jk = html_jk.replace('air ambulance cost from the UK', 'air ambulance cost from Jammu & Kashmir')
html_jk = html_jk.replace('regions in the UK do you cover', 'regions in Jammu & Kashmir do you cover')
html_jk = html_jk.replace('managed by our UK operations team', 'managed by our operations team')
html_jk = html_jk.replace('air ambulance be arranged from UK?', 'air ambulance be arranged from Jammu & Kashmir?')
html_jk = html_jk.replace('Our UK team responds to', 'Our operations team responds to')
html_jk = html_jk.replace('services from UK?', 'services from Jammu & Kashmir?')
html_jk = html_jk.replace('Many UK health insurance', 'Many Indian health insurance')
html_jk = html_jk.replace('ground ambulance in UK coordinated', 'ground ambulance in Jammu & Kashmir coordinated')
html_jk = html_jk.replace('Our UK operations team coordinates', 'Our operations team coordinates')

# Localize Footer UK helpline
html_jk = html_jk.replace('24X7 UK Emergency Helpline', '24X7 India Emergency Helpline')

# Save Jammu & Kashmir page
html_jk = make_paths_relative(html_jk)
with open("national/air-ambulance-jammu-kashmir.html", "w", encoding="utf-8") as f:
    f.write(html_jk)
print("Saved national/air-ambulance-jammu-kashmir.html")
