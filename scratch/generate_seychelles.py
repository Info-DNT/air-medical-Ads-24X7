import re
import os

def generate_card(origin, destination):
    # Construct a clean custom description for each route card
    desc = f"Dedicated ICU air ambulance, commercial airline stretcher, and flight medical escort services from {origin} to {destination}, coordinating with major medical centers, specialists, and ground emergency teams."
    whatsapp_text = f"I need Assistance with Patient Air Transfer from {origin} to {destination}. Please Assist!"
    whatsapp_link = f"https://wa.me/16593005200?text={re.sub(r' ', '%20', whatsapp_text)}"
    
    return f"""                    <!-- Route Card: {origin} to {destination} -->
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
                                {desc}
                            </p>
                        </div>
                        <div class="pt-4 border-t border-slate-100 flex justify-end">
                            <a href="{whatsapp_link}"
                                target="_blank" rel="noopener noreferrer nofollow"
                                class="px-5 py-2.5 bg-secondary text-white rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-primary transition-all shadow-md hover:shadow-lg flex items-center gap-1.5">
                                Get Quote on WhatsApp
                                <span class="material-symbols-outlined text-xs">open_in_new</span>
                            </a>
                        </div>
                    </div>"""

def build_accordion(region_id, title, destinations, origin):
    """Build a complete accordion section exactly matching the UK page structure."""
    cards = '\n'.join([generate_card(origin, dest) for dest in destinations])
    return f"""            <!-- Region Accordion: {title} -->
            <div id="region-{region_id}"
                class="mb-6 border border-slate-200/60 dark:border-slate-800/60 rounded-2xl overflow-hidden bg-white shadow-sm transition-all duration-300">
                <!-- Accordion Header Button -->
                <button
                    class="w-full px-6 py-5 flex items-center justify-between bg-slate-50/50 hover:bg-slate-50 transition-colors text-left focus:outline-none group"
                    onclick="toggleRegion('{region_id}')">
                    <span
                        class="font-headline text-base md:text-lg font-black text-primary uppercase tracking-wide">{title}</span>
                    <span
                        class="material-symbols-outlined text-secondary text-2xl transform transition-transform duration-300 ease-in-out"
                        id="icon-region-{region_id}">keyboard_arrow_down</span>
                </button>
                <!-- Accordion Content (Collapsed by Default) -->
                <div class="hidden transition-all duration-300 ease-in-out border-t border-slate-100"
                    id="content-region-{region_id}">
                    <div class="p-6">
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
{cards}
                        </div>
                    </div>
                </div>
            </div>
"""



def main():
    template_path = 'air-ambulance-dummy.html'
    if not os.path.exists(template_path):
        print(f"Error: {template_path} does not exist.")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Base Placeholders Replacement
    replacements = {
        '[COUNTRY/REGION]': 'Seychelles',
        '[SLUG]': 'seychelles',
        '[PHONE_RAW]': '+2484632054',
        '[PHONE_DISPLAY]': '+248 4 632 054',
        '[PHONE_PREFIX]': '+248',
        '[CITY]': 'Victoria / Mahé',
        '[REGION]': 'Victoria',
        '[COUNTRY_CODE]': 'SC',
        '[CITIES]': 'Victoria, Mahé, Praslin, La Digue',
        '[CITY_1]': 'Victoria',
        '[CITY_2]': 'Mahé',
        '[DEST_1]': 'India',
        '[DEST_2]': 'UAE'
    }

    for placeholder, val in replacements.items():
        content = content.replace(placeholder, val)

    # 2. Update canonical links to be pointing to root page url (without /ads/ prefix)
    content = re.sub(
        r'<!-- TEMPLATE_PLACEHOLDER: CANONICAL_URL.*?-->\s*<link rel="canonical" href="[^"]+" />',
        '<link rel="canonical" href="https://airmedical24x7.com/air-ambulance-seychelles" />',
        content, flags=re.DOTALL
    )

    # 3. Replace LocalBusiness JSON-LD Schema
    local_business_schema = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["LocalBusiness", "MedicalOrganization"],
      "name": "Air Medical 24X7",
      "url": "https://airmedical24x7.com/air-ambulance-seychelles",
      "telephone": "+2484632054",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Victoria / Mahé",
        "addressRegion": "Victoria",
        "addressCountry": "SC"
      },
      "description": "24X7 Air Ambulance Services across Seychelles - Victoria, Mahé, Praslin, La Digue. ICU-equipped medical evacuation to India and worldwide.",
      "areaServed": "Seychelles - Victoria, Mahé, Praslin, La Digue",
      "medicalSpecialty": "Emergency Medicine",
      "availableService": "Air Ambulance",
      "openingHours": "Mo-Su 00:00-24:00"
    }
    </script>"""
    
    content = re.sub(
        r'<!-- TEMPLATE_PLACEHOLDER: LOCAL_BUSINESS_SCHEMA.*?-->\s*<script type="application/ld\+json">.*?</script>',
        local_business_schema,
        content, flags=re.DOTALL
    )

    # 4. Replace FAQ JSON-LD Schema
    faq_schema = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How much does an air ambulance from Seychelles to India cost?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The cost of a medical repatriation from Seychelles to India depends on the patient's condition, aircraft type, and distance (typically Victoria/Mahé to Mumbai or Delhi). We provide all-inclusive bedside-to-bedside quotes within 30 minutes."
          }
        },
        {
          "@type": "Question",
          "name": "Which regions in Seychelles do you cover?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We cover all regions of the Seychelles, including Victoria, Mahé, Praslin, La Digue, and outer islands, coordinating ground transport directly to Seychelles International Airport (SEZ)."
          }
        },
        {
          "@type": "Question",
          "name": "How quickly can an air ambulance be arranged from Seychelles?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Typically within 24 to 48 hours, depending on aircraft availability, patient medical clearance, and international flight permits. Our 24/7 operations desk coordinates all details."
          }
        },
        {
          "@type": "Question",
          "name": "Can I use insurance for air ambulance services from Seychelles?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Many international health insurance policies cover emergency medical evacuation. We coordinate directly with major global insurers to verify coverage and manage the billing process."
          }
        },
        {
          "@type": "Question",
          "name": "Is a flight medical escort sufficient or do I need a dedicated air ambulance from Seychelles?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "For stable patients, a commercial airline stretcher or medical escort is a cost-effective alternative. For critical care patients requiring continuous ICU support, a dedicated air ambulance is necessary."
          }
        },
        {
          "@type": "Question",
          "name": "How is ground ambulance in Seychelles coordinated?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Our bed-to-bed service includes full ground ambulance coordination in Seychelles, transferring the patient from their hospital bed to the aircraft, and from the destination airport to the receiving hospital."
          }
        }
      ]
    }
    </script>"""

    content = re.sub(
        r'<!-- TEMPLATE_PLACEHOLDER: FAQ_SCHEMA.*?-->\s*<script type="application/ld\+json">.*?</script>',
        faq_schema,
        content, flags=re.DOTALL
    )

    # 5. Populate Sidebar Destinations List (Hero Left Panel)
    asia_list = ['India', 'Sri Lanka', 'Bangladesh', 'Pakistan', 'Nepal', 'Maldives', 'Thailand', 'Malaysia', 'Singapore', 'Indonesia', 'Philippines', 'China', 'Japan', 'South Korea', 'Hong Kong']
    mideast_list = ['UAE', 'Qatar', 'Oman', 'Kuwait', 'Bahrain', 'Saudi Arabia', 'Israel']
    africa_list = ['South Africa', 'Ethiopia', 'Kenya', 'Tanzania', 'Mauritius', 'Madagascar', 'Réunion', 'Egypt', 'Morocco', 'Tunisia', 'Algeria', 'Nigeria', 'Ghana', 'Uganda', 'Rwanda', 'Mozambique', 'Zambia', 'Zimbabwe']
    europe_list = ['Türkiye', 'Germany', 'Switzerland', 'France', 'Russia', 'UK', 'Netherlands', 'Belgium', 'Italy', 'Spain', 'Austria', 'Greece', 'Portugal', 'Denmark', 'Sweden', 'Norway', 'Finland']
    na_list = ['USA', 'Canada']
    oceania_list = ['Australia', 'New Zealand']

    def make_sidebar_items(countries, region_hash):
        items = []
        for c in countries:
            items.append(f'<li class="flex items-center gap-1"><span class="w-1 h-1 rounded-full bg-secondary flex-shrink-0"></span><a href="{region_hash}" class="hover:text-secondary hover:underline transition-all">Seychelles to {c}</a></li>')
        return '\n                                        '.join(items)

    sidebar_html = f"""<!-- Asia & Subcontinent -->
                                <div>
                                    <a href="#region-asia" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Asia & Subcontinent</a>
                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        {make_sidebar_items(asia_list, '#region-asia')}
                                    </ul>
                                </div>

                                <!-- Middle East -->
                                <div>
                                    <a href="#region-middle-east" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Middle East</a>
                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        {make_sidebar_items(mideast_list, '#region-middle-east')}
                                    </ul>
                                </div>

                                <!-- Africa -->
                                <div>
                                    <a href="#region-africa" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Africa</a>
                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        {make_sidebar_items(africa_list, '#region-africa')}
                                    </ul>
                                </div>

                                <!-- Europe -->
                                <div>
                                    <a href="#region-europe-usa" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Europe</a>
                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        {make_sidebar_items(europe_list, '#region-europe-usa')}
                                    </ul>
                                </div>

                                <!-- North America -->
                                <div>
                                    <a href="#region-europe-usa" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">North America</a>
                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        {make_sidebar_items(na_list, '#region-europe-usa')}
                                    </ul>
                                </div>

                                <!-- Australia & Oceania -->
                                <div>
                                    <a href="#region-oceania" class="region-link text-[8px] font-black uppercase tracking-[0.18em] text-white underline mb-1 hover:text-secondary block">Australia & Oceania</a>
                                    <ul class="grid grid-cols-3 gap-x-2 gap-y-0.5 text-[9px] text-slate-200 font-semibold">
                                        {make_sidebar_items(oceania_list, '#region-oceania')}
                                    </ul>
                                </div>"""

    # Replace sidebar in content, ensuring correct nesting tags are preserved
    start_idx = content.find('<!-- Asia & Subcontinent -->')
    africa_idx = content.find('<!-- Africa -->')
    ul_end_idx = content.find('</ul>', africa_idx)
    div_end_idx = content.find('</div>', ul_end_idx)
    end_pos = div_end_idx + len('</div>')
    
    content = content[:start_idx] + sidebar_html + '\n                            ' + content[end_pos:]

    # 6. Update pricing section heading
    content = content.replace('Air Ambulance &amp; Airline Stretcher Costs from UK', 'Air Ambulance &amp; Airline Stretcher Costs from Seychelles')

    # 7. Localize "Why Families Rely on Us" Item "02"
    why_start = content.find('UK Operations &mdash; Rapid Local Response')
    if why_start != -1:
        why_idx = content.rfind('02</div>', 0, why_start)
        feature_item_start = content.rfind('class="feature-item', 0, why_idx)
        why_item_start = content.rfind('<div', 0, feature_item_start)
        why_p_close = content.find('</div>', why_start)
        why_wrap_close = content.find('</div>', why_p_close + 6)
        why_end_pos = why_wrap_close + len('</div>')

        why_families_seychelles = """<div class="feature-item flex gap-5 opacity-0 translate-x-8" data-index="1">
                            <div
                                class="flex-shrink-0 w-11 h-11 bg-secondary text-white flex items-center justify-center rounded font-headline font-bold text-sm shadow-lg shadow-secondary/30">
                                02</div>
                            <div>
                                <h4 class="text-lg font-bold mb-1">Seychelles Operations &mdash; Rapid Local Response</h4>
                                <p class="text-on-surface-variant text-sm leading-relaxed">Our Seychelles desk handles local hospital coordination (such as Seychelles Hospital in Victoria), Seychelles International Airport (SEZ) clearances, and ground ambulance dispatch &mdash; ensuring swift response across Victoria, Mah&eacute;, Praslin, La Digue, and other outer islands.</p>
                            </div>
                        </div>"""
        content = content[:why_item_start] + why_families_seychelles + content[why_end_pos:]

    # 8. Localize HTML FAQ Accordion items on the page
    faq_1_start = content.find('<!-- FAQ 1 -->')
    faq_6_start = content.find('<!-- FAQ 6 -->')
    if faq_1_start != -1 and faq_6_start != -1:
        faq_6_inner_close = content.find('</div>', faq_6_start)
        faq_6_close = content.find('</div>', faq_6_inner_close + 6)
        faq_end_pos = faq_6_close + len('</div>')

        faq_accordions_html = """<!-- FAQ 1 -->
                    <div
                        class="faq-item bg-white rounded-xl border border-outline-variant/10 overflow-hidden transition-all duration-300">
                        <button class="w-full flex justify-between items-center p-6 text-left group">
                            <span
                                class="font-headline font-bold text-primary group-hover:text-secondary transition-colors">How much does an air ambulance from Seychelles to India cost?</span>
                            <span
                                class="material-symbols-outlined transform transition-transform group-[.active]:rotate-180">expand_more</span>
                        </button>
                        <div
                            class="faq-answer hidden p-6 pt-0 text-on-surface-variant text-sm border-t border-slate-50 leading-relaxed">
                            The cost of a medical repatriation from Seychelles to India depends on the patient's condition, aircraft type, and distance (typically Victoria/Mah&eacute; to Mumbai or Delhi). We provide all-inclusive bedside-to-bedside quotes within 30 minutes.
                        </div>
                    </div>
                    <!-- FAQ 2 -->
                    <div
                        class="faq-item bg-white rounded-xl border border-outline-variant/10 overflow-hidden transition-all duration-300">
                        <button class="w-full flex justify-between items-center p-6 text-left group">
                            <span
                                class="font-headline font-bold text-primary group-hover:text-secondary transition-colors">Which regions in Seychelles do you cover?</span>
                            <span
                                class="material-symbols-outlined transform transition-transform group-[.active]:rotate-180">expand_more</span>
                        </button>
                        <div
                            class="faq-answer hidden p-6 pt-0 text-on-surface-variant text-sm border-t border-slate-50 leading-relaxed">
                            We cover all regions of the Seychelles, including Victoria, Mah&eacute;, Praslin, La Digue, and outer islands, coordinating ground transport directly to Seychelles International Airport (SEZ).
                        </div>
                    </div>
                    <!-- FAQ 3 -->
                    <div
                        class="faq-item bg-white rounded-xl border border-outline-variant/10 overflow-hidden transition-all duration-300">
                        <button class="w-full flex justify-between items-center p-6 text-left group">
                            <span
                                class="font-headline font-bold text-primary group-hover:text-secondary transition-colors">How quickly can an air ambulance be arranged from Seychelles?</span>
                            <span
                                class="material-symbols-outlined transform transition-transform group-[.active]:rotate-180">expand_more</span>
                        </button>
                        <div
                            class="faq-answer hidden p-6 pt-0 text-on-surface-variant text-sm border-t border-slate-50 leading-relaxed">
                            Typically within 24 to 48 hours, depending on aircraft availability, patient medical clearance, and international flight permits. Our 24/7 operations desk coordinates all details.
                        </div>
                    </div>
                    <!-- FAQ 4 -->
                    <div
                        class="faq-item bg-white rounded-xl border border-outline-variant/10 overflow-hidden transition-all duration-300">
                        <button class="w-full flex justify-between items-center p-6 text-left group">
                            <span
                                class="font-headline font-bold text-primary group-hover:text-secondary transition-colors">Can I use insurance for air ambulance services from Seychelles?</span>
                            <span
                                class="material-symbols-outlined transform transition-transform group-[.active]:rotate-180">expand_more</span>
                        </button>
                        <div
                            class="faq-answer hidden p-6 pt-0 text-on-surface-variant text-sm border-t border-slate-50 leading-relaxed">
                            Many international health insurance policies cover emergency medical evacuation. We coordinate directly with major global insurers to verify coverage and manage the billing process.
                        </div>
                    </div>
                    <!-- FAQ 5 -->
                    <div
                        class="faq-item bg-white rounded-xl border border-outline-variant/10 overflow-hidden transition-all duration-300">
                        <button class="w-full flex justify-between items-center p-6 text-left group">
                            <span
                                class="font-headline font-bold text-primary group-hover:text-secondary transition-colors">Is a flight medical escort sufficient or do I need a dedicated air ambulance from Seychelles?</span>
                            <span
                                class="material-symbols-outlined transform transition-transform group-[.active]:rotate-180">expand_more</span>
                        </button>
                        <div
                            class="faq-answer hidden p-6 pt-0 text-on-surface-variant text-sm border-t border-slate-50 leading-relaxed">
                            For stable patients, a commercial airline stretcher or medical escort is a cost-effective alternative. For critical care patients requiring continuous ICU support, a dedicated air ambulance is necessary.
                        </div>
                    </div>
                    <!-- FAQ 6 -->
                    <div
                        class="faq-item bg-white rounded-xl border border-outline-variant/10 overflow-hidden transition-all duration-300">
                        <button class="w-full flex justify-between items-center p-6 text-left group">
                            <span
                                class="font-headline font-bold text-primary group-hover:text-secondary transition-colors">How is ground ambulance in Seychelles coordinated?</span>
                            <span
                                class="material-symbols-outlined transform transition-transform group-[.active]:rotate-180">expand_more</span>
                        </button>
                        <div
                            class="faq-answer hidden p-6 pt-0 text-on-surface-variant text-sm border-t border-slate-50 leading-relaxed">
                            Our bed-to-bed service includes full ground ambulance coordination in Seychelles, transferring the patient from their hospital bed to the aircraft, and from the destination airport to the receiving hospital.
                        </div>
                    </div>"""
        content = content[:faq_1_start] + faq_accordions_html + content[faq_end_pos:]

    # 9. Build and inject the entire routes section (popular-routes grid + 5 accordions)
    origin = 'Victoria / Mahé'
    requested_dests = ['Mumbai', 'Dubai', 'Abu Dhabi', 'Doha', 'Colombo', 'Johannesburg', 'Nairobi', 'Addis Ababa', 'Istanbul', 'Frankfurt', 'Zurich', 'Paris', 'Moscow', 'Tel Aviv', 'Mauritius', 'Antananarivo', 'Saint-Denis', 'Dar es Salaam']
    popular_cards = '\n'.join([generate_card(origin, dest) for dest in requested_dests])

    asia_dests = ['Mumbai', 'Colombo', 'Chennai', 'New Delhi', 'Bengaluru', 'Hyderabad', 'Kochi', 'Singapore', 'Kuala Lumpur', 'Bangkok', 'Manila', 'Jakarta', 'Hong Kong', 'Beijing', 'Shanghai', 'Tokyo', 'Seoul', 'Dhaka', 'Kathmandu', 'Malé', 'Lahore', 'Karachi', 'Islamabad']
    mideast_dests = ['Dubai', 'Abu Dhabi', 'Doha', 'Istanbul', 'Tel Aviv', 'Muscat', 'Kuwait City', 'Manama', 'Riyadh', 'Jeddah', 'Cairo']
    europe_dests = ['Frankfurt', 'Zurich', 'Paris', 'Moscow', 'London', 'Manchester', 'Amsterdam', 'Brussels', 'Rome', 'Milan', 'Madrid', 'Barcelona', 'Vienna', 'Athens', 'Lisbon', 'Copenhagen', 'Stockholm', 'Oslo', 'Helsinki', 'Geneva', 'New York', 'Washington, D.C.', 'Toronto', 'Montreal']
    oceania_dests = ['Sydney', 'Melbourne', 'Auckland']
    africa_dests = ['Johannesburg', 'Nairobi', 'Addis Ababa', 'Mauritius', 'Antananarivo', 'Saint-Denis', 'Dar es Salaam', 'Casablanca', 'Tunis', 'Algiers', 'Lagos', 'Accra', 'Entebbe', 'Kigali', 'Maputo', 'Lusaka', 'Harare', 'Cape Town']

    routes_section_html = f"""<!-- SECTION START: Critical Global Transfer Routes -->
    <!-- Critical Global Transfer Routes from Seychelles Section -->
    <section id="routes-section"
        class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-12">
                <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
                    Critical Global Transfer Routes from Seychelles
                </h2>
                <p class="text-on-surface-variant font-body leading-relaxed text-sm">
                    Providing dedicated bed-to-bed ICU air ambulance and commercial airline stretcher services across all major international medical corridors, serving patients from Seychelles with seamless end-to-end medical transportation.
                </p>
            </div>

            <!-- Popular Routes Sub-Section -->
            <div id="popular-routes" class="mb-14">
                <h3 class="font-headline text-lg font-black text-primary mb-6 uppercase tracking-wider">Most Requested
                    Transfer Routes</h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
{popular_cards}
                </div>
            </div>

{build_accordion('asia', 'Asia & Subcontinent Routes', asia_dests, origin)}
{build_accordion('middle-east', 'Middle East & Central Asia Routes', mideast_dests, origin)}
{build_accordion('europe-usa', 'USA, Canada, Europe & UK Routes', europe_dests, origin)}
{build_accordion('oceania', 'Oceania Routes', oceania_dests, origin)}
{build_accordion('africa', 'Africa Routes', africa_dests, origin)}
        </div>
    </section>
<!-- SECTION END: Critical Global Transfer Routes -->"""

    # Find the old routes section and replace it entirely
    routes_start_marker = '<!-- SECTION START: Critical Global Transfer Routes'
    routes_end_marker = '<!-- SECTION END: Critical Global Transfer Routes -->'
    rs = content.find(routes_start_marker)
    re_end = content.find(routes_end_marker)
    if rs == -1 or re_end == -1:
        raise ValueError('Could not find routes section markers in template')
    re_end += len(routes_end_marker)
    content = content[:rs] + routes_section_html + content[re_end:]

    # 11. Create Root File (All relative asset paths)
    root_content = content
    root_content = root_content.replace('/ads/assets/', 'assets/')
    root_content = root_content.replace('/ads/script.js', 'script.js')
    root_content = root_content.replace('/ads/supabase-config.js', 'supabase-config.js')
    root_content = root_content.replace('/ads/styles.css', 'styles.css')

    with open('air-ambulance-seychelles.html', 'w', encoding='utf-8') as f:
        f.write(root_content)
    print("Generated: air-ambulance-seychelles.html")

    # 12. Create Deploy File (All /ads/ prefixed asset paths)
    deploy_content = content
    deploy_content = deploy_content.replace('href="styles.css"', 'href="/ads/styles.css"')
    deploy_content = deploy_content.replace('href="assets/', 'href="/ads/assets/')
    deploy_content = deploy_content.replace('src="assets/', 'src="/ads/assets/')
    deploy_content = deploy_content.replace('/ads//ads/', '/ads/')
    
    with open('uae-only-deploy/air-ambulance-seychelles.html', 'w', encoding='utf-8') as f:
        f.write(deploy_content)
    print("Generated: uae-only-deploy/air-ambulance-seychelles.html")

if __name__ == '__main__':
    main()
