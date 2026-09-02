# New MENA Country Landing Pages — Build Report

## Executive Summary

Sixteen new country landing pages were generated from `air-ambulance-dummy.html` and placed in the repository root. They cover the Middle East, North Africa and the wider Arab League markets requested by the client.

Of the eighteen countries on the client list, **sixteen required new pages**. The remaining two were already live with substantially richer content and were deliberately left untouched:

| Country | Existing page | Size | Route cards | FAQs | Decision |
| :--- | :--- | ---: | ---: | ---: | :--- |
| UAE | `air-ambulance-uae.html` | 1,297 KB | 538 | 7 | **Skipped** — rebuilding would overwrite live UAE content |
| Saudi Arabia | `air-ambulance-ksa.html` | 873 KB | 344 | 8 | **Skipped** — a second Saudi page would duplicate it |

## Build Parameters

| Parameter | Value | Rationale |
| :--- | :--- | :--- |
| Source template | `air-ambulance-dummy.html` | Client-nominated reference page |
| Helpline | `+971 800 016 0098` (UAE) | Regional line for all 16 markets; matches the precedent of Spain reusing the UK line |
| Route cards | Template defaults retained | Client instruction — see *Known Follow-ups* |
| Hero image | `assets/air_ambulance_aircraft_hero_image.png` | Template default |
| Section photo | `assets/Air ambulance 24X7.jpeg` | Country-neutral; per-country images do not exist for these markets |
| Asset paths | Converted `/ads/...` → relative | Every other root page uses relative paths |

## Page Matrix

| # | File | Country | Capital | Region (schema) | ISO | Form prefix | Size |
| ---: | :--- | :--- | :--- | :--- | :--- | :--- | ---: |
| 1 | `air-ambulance-algeria.html` | Algeria | Algiers | Algiers Province | `DZ` | `+213` | 611 KB |
| 2 | `air-ambulance-bahrain.html` | Bahrain | Manama | Capital Governorate | `BH` | `+973` | 611 KB |
| 3 | `air-ambulance-egypt.html` | Egypt | Cairo | Cairo Governorate | `EG` | `+20` | 611 KB |
| 4 | `air-ambulance-iraq.html` | Iraq | Baghdad | Baghdad Governorate | `IQ` | `+964` | 611 KB |
| 5 | `air-ambulance-jordan.html` | Jordan | Amman | Amman Governorate | `JO` | `+962` | 611 KB |
| 6 | `air-ambulance-kuwait.html` | Kuwait | Kuwait City | Al Asimah Governorate | `KW` | `+965` | 611 KB |
| 7 | `air-ambulance-lebanon.html` | Lebanon | Beirut | Beirut Governorate | `LB` | `+961` | 611 KB |
| 8 | `air-ambulance-libya.html` | Libya | Tripoli | Tripoli District | `LY` | `+218` | 611 KB |
| 9 | `air-ambulance-mauritania.html` | Mauritania | Nouakchott | Nouakchott Region | `MR` | `+222` | 612 KB |
| 10 | `air-ambulance-morocco.html` | Morocco | Rabat | Rabat-Sale-Kenitra | `MA` | `+212` | 611 KB |
| 11 | `air-ambulance-oman.html` | Oman | Muscat | Muscat Governorate | `OM` | `+968` | 611 KB |
| 12 | `air-ambulance-qatar.html` | Qatar | Doha | Doha Municipality | `QA` | `+974` | 611 KB |
| 13 | `air-ambulance-sudan.html` | Sudan | Khartoum | Khartoum State | `SD` | `+249` | 611 KB |
| 14 | `air-ambulance-syria.html` | Syria | Damascus | Damascus Governorate | `SY` | `+963` | 611 KB |
| 15 | `air-ambulance-tunisia.html` | Tunisia | Tunis | Tunis Governorate | `TN` | `+216` | 611 KB |
| 16 | `air-ambulance-yemen.html` | Yemen | Sanaa | Sanaa Governorate | `YE` | `+967` | 611 KB |

## Canonical URLs

| Country | Canonical |
| :--- | :--- |
| Algeria | https://airmedical24x7.com/air-ambulance-algeria |
| Bahrain | https://airmedical24x7.com/air-ambulance-bahrain |
| Egypt | https://airmedical24x7.com/air-ambulance-egypt |
| Iraq | https://airmedical24x7.com/air-ambulance-iraq |
| Jordan | https://airmedical24x7.com/air-ambulance-jordan |
| Kuwait | https://airmedical24x7.com/air-ambulance-kuwait |
| Lebanon | https://airmedical24x7.com/air-ambulance-lebanon |
| Libya | https://airmedical24x7.com/air-ambulance-libya |
| Mauritania | https://airmedical24x7.com/air-ambulance-mauritania |
| Morocco | https://airmedical24x7.com/air-ambulance-morocco |
| Oman | https://airmedical24x7.com/air-ambulance-oman |
| Qatar | https://airmedical24x7.com/air-ambulance-qatar |
| Sudan | https://airmedical24x7.com/air-ambulance-sudan |
| Syria | https://airmedical24x7.com/air-ambulance-syria |
| Tunisia | https://airmedical24x7.com/air-ambulance-tunisia |
| Yemen | https://airmedical24x7.com/air-ambulance-yemen |

## Shared Page Composition

Every generated page is structurally identical to the template:

| Element | Value |
| :--- | :--- |
| Route cards | 206 |
| FAQ accordion items | 6 |
| Helpline (all pages) | `+9718000160098` |
| Analytics | Microsoft Clarity `y8ut5a17d8`, GTM `GTM-KG4BQ6SM`, Google Ads `AW-16644189187` |
| Conversion events | Website Visit + Phone Number Clicks |
| Lead capture | Supabase `submit-lead` edge function, Cloudflare Turnstile |
| Structured data | `LocalBusiness` + `MedicalOrganization`, `FAQPage` |

### Title pattern

```
Air Ambulance Services <COUNTRY> | ICU Medical Evacuation 24X7
```

### H1 pattern

```
24X7 ICU Air Ambulance & Medical Evacuation from <COUNTRY>
```

## Verification

All sixteen pages were audited after generation. **No defects found.**

| Check | Result |
| :--- | :--- |
| Unresolved `[PLACEHOLDER]` tokens | 0 |
| Stale `/ads/` absolute paths | 0 |
| `24/7` branding residue | 0 |
| Local asset references resolving on disk | 19 / 19 |
| JSON-LD blocks parsing | all valid |
| HTML tag balance vs template | identical |
| Line endings / encoding | CRLF, no BOM |

## Known Follow-ups

1. **Route cards carry the template's UK routes.** All 206 cards on every page read `London (Heathrow) → …`, `Manchester → …`, `Birmingham → …` and similar. The template was derived from the UK page and its route grid was never parameterised — zero of its 206 cards contain a country placeholder. Retaining them was a client decision; replacing them with per-country corridors remains open.
2. **No `sitemap.xml` exists in the repository**, although `robots.txt` advertises `https://airmedical24x7.com/sitemap.xml`. The sixteen new URLs are not discoverable through it.
3. **Per-country helplines are not provisioned.** All sixteen pages route to the UAE line. If dedicated numbers are issued per market, update `telephone` in the JSON-LD, the three `tel:` links, and the two display spans on each page.

## Regeneration

Pages are deterministic output of the template plus a per-country data table (country, slug, capital, schema region, ISO code, dial prefix, city list). Regenerating after a template change means re-running that substitution rather than hand-editing sixteen files.
