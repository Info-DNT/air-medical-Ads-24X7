# Global Landing Page Phone Number & Helplines Audit Report

> **Audit Status**: Complete. No source code or HTML files were modified during this inspection.

## Executive Summary

This report audits the phone numbers displayed in the **Navbar** and **Footer** (including the **14 Global Helplines Grid**) across all 18 HTML landing pages in the repository against your standard 14 country helplines list:

| # | Country | Expected Display Format | Expected `tel:` href |
|---|---|---|---|
| 1 | **USA** | `+1 833-518-6535` | `tel:+18335186535` |
| 2 | **UK** | `+44 800 229 4751` | `tel:+448002294751` |
| 3 | **India** | `000-800-050-4740` | `tel:0008000504740` |
| 4 | **Canada** | `+1 833-725-7598` | `tel:+18337257598` |
| 5 | **Vietnam** | `+84 1203 2123` | `tel:+8412032123` |
| 6 | **Seychelles** | `+248 4 632 054` | `tel:+2484632054` |
| 7 | **South Africa** | `+27 80 001 0868` | `tel:+27800010868` |
| 8 | **Philippines** | `+63 1800 1 550 0181` | `tel:+63180015500181` |
| 9 | **UAE** | `+971 800 016 0098` | `tel:+9718000160098` |
| 10 | **Tanzania** | `+255 800 12 0158` | `tel:+255800120158` |
| 11 | **Turkey** | `+90 800 621 3131` | `tel:+908006213131` |
| 12 | **Japan** | `+81 800-170-5180` | `tel:+818001705180` |
| 13 | **Kenya** | `+254 800 230 119` | `tel:+254800230119` |
| 14 | **Saudi Arabia** | `+966 800 101 0817` | `tel:+9668001010817` |

---

## Key Findings & Critical Observations

### 1. Missing UK Helpline in Templated Pages Footer Grid
- In pages generated from the master template (`air-ambulance-spain.html`, `air-ambulance-vietnam.html`, `air-ambulance-tanzania.html`, `air-ambulance-seychelles.html`, `air-ambulance-bangladesh.html`, `air-ambulance-dummy.html`), the **UK Helpline (`+44 800 229 4751`) is missing from the 14-helpline footer grid**. The slot where UK usually sits was overwritten by the page's local primary number (e.g. Spain's `+34 900 123 456`).
- On `air-ambulance-ksa.html`, **UAE (`+971 800 016 0098`) is missing from the footer grid**.
- On `index.html` (the homepage), the 14-helpline grid is **completely missing** (only single UAE/India numbers exist in footer).
- On `thank-you.html`, no helpline grid or navbar phone exists.

---

## Complete Page-by-Page Audit Breakdown

### 1. `air-ambulance-spain.html`
- **Navbar Phone**: `+34 900 123 456` (`tel:+34900123456`)
- **Footer CTA Phone**: `+34 900 123 456` (`tel:+34900123456`)
- **Footer Helplines Grid**: 13 / 14 present
- **Missing Helpline**: ⚠️ **UK** (`+44 800 229 4751`)

### 2. `air-ambulance-vietnam.html`
- **Navbar Phone**: `+84 1203 2123` (`tel:+8412032123`)
- **Footer CTA Phone**: `+84 1203 2123` (`tel:+8412032123`)
- **Footer Helplines Grid**: 13 / 14 present
- **Missing Helpline**: ⚠️ **UK** (`+44 800 229 4751`)

### 3. `air-ambulance-tanzania.html`
- **Navbar Phone**: `+255 800 12 0158` (`tel:+255800120158`)
- **Footer CTA Phone**: `+255 800 12 0158` (`tel:+255800120158`)
- **Footer Helplines Grid**: 13 / 14 present
- **Missing Helpline**: ⚠️ **UK** (`+44 800 229 4751`)

### 4. `air-ambulance-seychelles.html`
- **Navbar Phone**: `+248 4 632 054` (`tel:+2484632054`)
- **Footer CTA Phone**: `+248 4 632 054` (`tel:+2484632054`)
- **Footer Helplines Grid**: 13 / 14 present
- **Missing Helpline**: ⚠️ **UK** (`+44 800 229 4751`)

### 5. `air-ambulance-bangladesh.html`
- **Navbar Phone**: `+880 1700 123 456` (`tel:+8801700123456`)
- **Footer CTA Phone**: `+880 1700 123 456` (`tel:+8801700123456`)
- **Footer Helplines Grid**: 13 / 14 present
- **Missing Helpline**: ⚠️ **UK** (`+44 800 229 4751`)

### 6. `air-ambulance-ksa.html`
- **Navbar Phone**: `+966 800 101 0817` (`tel:+9668001010817`)
- **Footer CTA Phone**: `+966 800 101 0817` (`tel:+9668001010817`)
- **Footer Helplines Grid**: 13 / 14 present
- **Missing Helpline**: ⚠️ **UAE** (`+971 800 016 0098`)

### 7. `air-ambulance-usa.html`
- **Navbar Phone**: `+1 833-518-6535` (`tel:+18335186535`)
- **Footer CTA Phone**: `+1 833-518-6535` (`tel:+18335186535`)
- **Footer Helplines Grid**: ✅ **All 14 Present**

### 8. `air-ambulance-uk.html`
- **Navbar Phone**: `+44 800 229 4751` (`tel:+448002294751`)
- **Footer CTA Phone**: `+44 800 229 4751` (`tel:+448002294751`)
- **Footer Helplines Grid**: ✅ **All 14 Present**

### 9. `air-ambulance-canada.html`
- **Navbar Phone**: `+1 833-725-7598` (`tel:+18337257598`)
- **Footer CTA Phone**: `+1 833-725-7598` (`tel:+18337257598`)
- **Footer Helplines Grid**: ✅ **All 14 Present**

### 10. `air-ambulance-philippines.html`
- **Navbar Phone**: `+63 1800 1 550 0181` (`tel:+63180015500181`)
- **Footer CTA Phone**: `+63 1800 1 550 0181` (`tel:+63180015500181`)
- **Footer Helplines Grid**: ✅ **All 14 Present**

### 11. `air-ambulance-uae.html`
- **Navbar Phone**: `+971 800 016 0098` (`tel:+9718000160098`)
- **Footer CTA Phone**: `+971 800 016 0098` (`tel:+9718000160098`)
- **Footer Helplines Grid**: ✅ **All 14 Present**

### 12. `air-ambulance-delhi.html` & `air-ambulance-andaman-nicobar.html` & `air-ambulance-jammu-kashmir.html`
- **Navbar Phone**: `000-800-050-4740` (`tel:0008000504740`)
- **Footer CTA Phone**: `000-800-050-4740` (`tel:0008000504740`)
- **Footer Helplines Grid**: ✅ **All 14 Present**

### 13. `index.html` (Homepage)
- **Navbar Phone**: `+971 800 016 0098` (`tel:+9718000160098`)
- **Footer Grid**: ⚠️ **Missing 13 numbers** (only UAE/India are listed in footer contact section)

### 14. `thank-you.html`
- **Navbar Phone**: None
- **Footer Grid**: None

---

## Per-Country Helpline Verification Breakdown

| Country | Phone Number | `tel:` Link | Missing On Pages |
|---|---|---|---|
| **USA** | `+1 833-518-6535` | `tel:+18335186535` | `index.html`, `thank-you.html` |
| **UK** | `+44 800 229 4751` | `tel:+448002294751` | `spain`, `vietnam`, `tanzania`, `seychelles`, `bangladesh`, `dummy`, `index.html`, `thank-you.html` |
| **India** | `000-800-050-4740` | `tel:0008000504740` | `index.html`, `thank-you.html` |
| **Canada** | `+1 833-725-7598` | `tel:+18337257598` | `index.html`, `thank-you.html` |
| **Vietnam** | `+84 1203 2123` | `tel:+8412032123` | `index.html`, `thank-you.html` |
| **Seychelles** | `+248 4 632 054` | `tel:+2484632054` | `index.html`, `thank-you.html` |
| **South Africa** | `+27 80 001 0868` | `tel:+27800010868` | `index.html`, `thank-you.html` |
| **Philippines** | `+63 1800 1 550 0181` | `tel:+63180015500181` | `index.html`, `thank-you.html` |
| **UAE** | `+971 800 016 0098` | `tel:+9718000160098` | `air-ambulance-ksa.html`, `thank-you.html` |
| **Tanzania** | `+255 800 12 0158` | `tel:+255800120158` | `index.html`, `thank-you.html` |
| **Turkey** | `+90 800 621 3131` | `tel:+908006213131` | `index.html`, `thank-you.html` |
| **Japan** | `+81 800-170-5180` | `tel:+818001705180` | `index.html`, `thank-you.html` |
| **Kenya** | `+254 800 230 119` | `tel:+254800230119` | `index.html`, `thank-you.html` |
| **Saudi Arabia** | `+966 800 101 0817` | `tel:+9668001010817` | `index.html`, `thank-you.html` |
