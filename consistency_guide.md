# Regional Landing Page Design Consistency Guide

This guide establishes the visual, structural, and behavioral standards for all regional landing pages. All new regional landing pages generated from `air-ambulance-dummy.html` must follow these rules to ensure absolute design consistency.

---

## 1. Core Typography & Design System

*   **Primary Font Family (Headline)**: `Manrope`
*   **Secondary Font Family (Body/Label)**: `Public Sans`
*   **Standard Colors**:
    *   **Primary (Navy)**: `#00355f` (`text-primary`, `bg-primary`)
    *   **Secondary (Red)**: `#b7102a` (`text-secondary`, `bg-secondary`)
    *   **Background (Light Gray/White)**: `#f8f9fa` (`bg-background`) / `#ffffff` (`bg-white`)
    *   **Surface Container Low**: `#f3f4f5` (`bg-surface-container-low`)
    *   **Outline-Variant**: `#c2c7d1` (`border-outline-variant`)

---

## 2. Key Sections & Structural Standards

### A. Critical Global Transfer Routes Section
This section is crucial for SEO and user routing. It must strictly maintain the grid layout, font size hierarchies, responsive behavior, and active state transitions.

*   **Outer Container**:
    ```html
    <section id="routes-section" class="py-16 bg-surface-container-low/40 border-b border-outline-variant/10 relative overflow-hidden">
    ```
*   **Heading Structure**:
    ```html
    <h2 class="font-headline text-3xl md:text-4xl font-extrabold text-primary mb-4 tracking-tighter">
        Critical Global Transfer Routes from [COUNTRY/REGION]
    </h2>
    <p class="text-on-surface-variant font-body leading-relaxed text-sm">
        [Standardized description paragraph detailing services and regions served]
    </p>
    ```
*   **Grid Layout**:
    *   Popular/Featured routes must use: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6`.
    *   Route cards must use white backgrounds, rounded borders (`rounded-2xl`), shadow-sm, and hover translations (`hover:-translate-y-1 hover:shadow-md transition-all duration-300`).
*   **Accordion Component Standards**:
    *   Accordion headers must use flexbox layouts with items-center, justify-between, and bold typography.
    *   The dropdown chevron icon must transition smoothly (`transition-transform duration-300`) and rotate 180 degrees when open (`.rotate-180`).
    *   Collapsed panels must utilize Tailwind transitions to animate max-height and opacity, avoiding sudden layout shifts.

### B. Hero 2-Panel Card
The conversion form and localized info grid must remain side-by-side on desktop, stacking seamlessly on mobile.

*   **Grid Container**:
    ```html
    <div class="max-w-4xl mx-auto bg-surface-container-lowest rounded-2xl shadow-[0_40px_80px_rgba(0,53,95,0.40)] overflow-hidden border border-white/10">
        <div class="grid grid-cols-1 lg:grid-cols-2">
    ```
*   **Left Panel (Navy/Info Grid)**:
    *   Use `.bg-primary .p-8 .md:p-10 .text-white` with `.hidden .lg:flex` to hide on smaller screens.
    *   Contains the regional title, brief info paragraph, and structured lists of destinations mapped into neat sub-grids.
*   **Right Panel (Lead Capture Form)**:
    *   Use `.p-5 .md:p-10 .bg-white`.
    *   Inputs must use light grey background (`bg-gray-100`), subtle border (`border-gray-200`), large rounded corners (`rounded-xl`), and smooth transitioning borders on focus (`focus:ring-2 focus:ring-secondary/30 focus:border-secondary/40`).
    *   The submit button must feature the pulse animation:
        ```html
        <button class="w-full bg-secondary text-white py-4 rounded-lg font-headline font-black uppercase tracking-[0.2em] text-xs hover:bg-primary transition-all duration-300 shadow-xl shadow-secondary/20 pulse-motif relative overflow-hidden group" type="submit">
        ```

### C. FAQ Accordion
*   **Container**:
    ```html
    <section class="py-16 bg-surface-dim relative overflow-hidden">
    ```
*   **Layout**: Left column (`md:w-1/3`) for section title; right column (`md:w-2/3`) for collapsible accordion questions.
*   **Interactive Behavior**:
    *   Questions should highlight in the secondary color (`text-secondary`) when active.
    *   Chevron icons must rotate using standard CSS transition.

---

## 3. Interactivity & Micro-Animations

All buttons and call-to-actions (CTAs) must maintain the same feedback states:
1.  **Phone & WhatsApp Links**:
    *   Standard color transitions (`transition-colors duration-300`).
    *   Subtle hover scales (`hover:scale-105 active:scale-95 transition-transform`).
2.  **Submit Buttons**:
    *   Pulse micro-animations using custom utility classes (`pulse-motif`).
3.  **Scroll Animations**:
    *   Use intersection observers to fade in cards with class `scroll-reveal-up` or `scroll-reveal-right` as the user scrolls.

---

## 4. Verification Checklists for New Pages

When developing a new page from `air-ambulance-dummy.html`:
1.  [ ] Verify GTM, Google Ads tracking, and conversion script values.
2.  [ ] Verify canonical link points to the exact absolute URL of the new regional page.
3.  [ ] Ensure JSON-LD schema (both LocalBusiness and FAQPage) has been correctly generated and validated using schema.org markup validator.
4.  [ ] Ensure all instances of the placeholder `[COUNTRY/REGION]`, `[SLUG]`, `[PHONE_RAW]`, `[PHONE_DISPLAY]`, `[PHONE_PREFIX]`, and `[CITIES]` are replaced.
5.  [ ] Verify all links and CTAs point to the correct regional telephone lines.
