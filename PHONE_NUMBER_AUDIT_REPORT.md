# Global Landing Pages Phone Number Audit Report

## Executive Summary
This document provides a comprehensive audit of the 14-helpline network across all landing pages in this deployment directory. Every page features:
- **Column 3 (Right)**: Primary regional emergency helpline.
- **Column 2 (Center)**: The remaining 13 global helplines in **strict canonical sequence** (`USA` -> `UAE` -> `UK` -> `India` -> `Canada` -> `Vietnam` -> `Philippines` -> `Seychelles` -> `South Africa` -> `Tanzania` -> `Turkey` -> `Japan` -> `Kenya` -> `Saudi Arabia`) with zero duplicates or missing entries.

## Helpline Network Verification Matrix

| Landing Page File | Column 3 Primary Helpline | Col 2 Count | Canonical Sequence | Compliance Status |
| :--- | :--- | :--- | :--- | :--- |
| `air-ambulance-bangladesh.html` | `+18335186535` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-canada.html` | `+18337257598` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-dummy.html` | `[PHONE_RAW]` | 14 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-india-to-international.html` | `0008000504740` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-ksa.html` | `+9668001010817` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-philippines.html` | `+63180015500181` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-seychelles.html` | `+2484632054` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-spain.html` | `+18335186535` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-tanzania.html` | `+255800120158` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-uae.html` | `+9718000160098` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-uk.html` | `+448002294751` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-usa.html` | `+18335186535` | 13 | **Strict Match** | **100% CLEAN** |
| `air-ambulance-vietnam.html` | `+8412032123` | 13 | **Strict Match** | **100% CLEAN** |

## Standard HTML Format Reference
```html
<a href="tel:[TEL_NUMBER]" onclick="return gtag_report_phone_conversion(this.href);"
    class="text-white hover:text-secondary transition-colors flex items-center gap-4">
    <span class="w-24 inline-block text-white font-normal text-left">[COUNTRY]</span>
    <span class="font-mono text-[13px] tracking-wide">[PHONE_DISPLAY]</span>
</a>
```