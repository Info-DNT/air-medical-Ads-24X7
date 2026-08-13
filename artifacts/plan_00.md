# Implementation Plan: Dynamic Page/Country Tracking for Leads

## Goal
Automatically identify which landing page a user filled the form on (e.g., UAE, UK, USA, Canada, India, Philippines, Seychelles, Vietnam) and send this page name to Supabase ("super") in a separate column when the form is submitted.

---

## Proposed Changes

### [MODIFY] script.js and uae-only-deploy/script.js

1. **Page Identification Logic**:
   We will add a helper function inside the DOMContentLoaded listener to determine the country/page name based on the current URL path:
   ```javascript
   const getPageIdentifier = () => {
       const path = window.location.pathname.toLowerCase();
       if (path.includes('uae')) return 'UAE';
       if (path.includes('uk')) return 'UK';
       if (path.includes('usa')) return 'USA';
       if (path.includes('canada')) return 'Canada';
       if (path.includes('india')) return 'India';
       if (path.includes('philippines')) return 'Philippines';
       if (path.includes('seychelles')) return 'Seychelles';
       if (path.includes('vietnam')) return 'Vietnam';
       return 'Main'; // Fallback for index.html
   };
   ```

2. **Payload Update**:
   Update the form submission payload in both `script.js` files to pass the page identifier. To ensure it matches whichever column name exists in your Supabase table, we will send it under the three most common field names:
   ```javascript
   const pageId = getPageIdentifier();
   
   const payload = {
       name: formData.get('name'),
       phone: formData.get('phone'),
       email: formData.get('email'),
       from_location: formData.get('from_location'),
       to_location: formData.get('to_location'),
       service: formData.get('service'),
       token: turnstileToken,
       
       // Page tracking columns
       page: pageId,
       page_name: pageId,
       country: pageId
   };
   ```

---

## Verification Plan

- Run a local server and intercept the form submission payload to verify that when submitting from a page (e.g. `air-ambulance-uk.html`), the payload sent to the Supabase endpoint contains the correct country identifier (e.g., `page: "UK"`, `page_name: "UK"`, `country: "UK"`).
