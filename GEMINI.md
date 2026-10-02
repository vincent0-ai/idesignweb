# Idesignweb Design System & Frontend Invariants

This project follows strict minimalist, modern digital studio and engineering agency standards. Adhere strictly to these principles whenever creating, updating, or reviewing templates, stylesheets, and components.

---

## 1. Zero Decorative Clutter (Strict Prohibition)
- **No Unsolicited Third-Party Buttons**: **NEVER add WhatsApp buttons**, chat bubbles, or third-party contact pills unless explicitly requested in the prompt.
- **No Kicker Tags & Pill Clutter**: Do NOT add uppercase meta tags (`OUR PICKS`, `CAPABILITIES`, `OUR THESIS`, `DIRECT LEADERSHIP`, `PRACTICE 01`) above headings.
- **No Author Avatar Circles**: Do NOT display avatar chips (e.g. `TO`, `VO`) on card fronts.
- **No Bullet Lists Inside Cards**: Cards are teasers and hooks. Deliverable bullet lists belong strictly on detail pages (`.detail-deliverables-list`), NEVER on card fronts. Do not use global hide rules (`display: none`) that bleed into detail templates.
- **No Trailing Arrow Decorations**: Avoid appending `&rarr;`, `&larr;`, or chevron symbols to every link and button.
- **No Shouting All-Caps Headings**: Avoid `text-transform: uppercase` on headings. Use clean Title Case or Sentence Case with tight editorial line-height (`1.15` to `1.25`).

---

## 1.1 Page Headers & Alignment
- **Centered Hierarchy**: All primary page headers (`.page-header`) and section headers (`.section-header-center`) must be centered horizontally.
- **Subtitle Constraints**: Subtitles must use `text-align: center; max-width: 640px; margin: 0 auto; line-height: 1.6; color: var(--text-muted);` to prevent overly wide line-wrapping.

---

## 2. Card Architecture: "No Card Houses"
- **Avoid Heavy Boxed Containers**: Never wrap items in bulky multi-layer bunkers with thick borders, heavy dark backgrounds, or pastel sky-blue fills.
- **Flat & Clean Structure**:
  - Base: Clean flat surface (`#FFFFFF`) with a hairline border (`1px solid #E2E8F0`).
  - Radius: Smooth `8px` to `10px`.
  - Padding: Compact (`16px` to `20px` desktop, `12px` to `14px` mobile).
  - Hover: Subtle lift (`translateY(-2px)`) with soft shadow (`0 4px 16px rgba(0, 0, 0, 0.05)`).
- **Edge-to-Edge Media**:
  - Card images use `aspect-ratio: 16 / 10` (or `4 / 3`) with `width: 100%`, `height: auto`, and `object-fit: cover`.
  - Border-radius applied to top corners with zero side voids or letterboxing.

---

## 3. 2-Column Mobile Grid Layout
- **Mobile Cards**: Always use a **2-column layout on mobile** (`grid-template-columns: repeat(2, 1fr)`) with compact gutters (`8px` to `12px`).
- **Zero Side Voids**: In a 2-column mobile layout, card width is ~165px, allowing standard landscape and editorial photography to fill edge-to-edge naturally.

---

## 4. Color Palette & Typography
- **Palette**:
  - Obsidian Slate: `#0F172A` (primary text, headers, primary buttons).
  - Muted Text: `#64748B` (body text, descriptions).
  - Backgrounds: `#FFFFFF` (clean surface) and `#F8FAFC` (subtle contrast sections).
  - Hairline Border: `#E2E8F0`.
  - Restrained Accent: `#2563EB` (clean modern blue, used sparingly).
  - Strictly avoid jarring electric blues (`#2D00FB`), neon greens (`#00D084`), or pastel sky blues (`#EBF6FC`).
- **Typography**:
  - Primary Stack: Google Font **Inter** (`'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`), matching `vinkj.com`.
  - Hierarchy & Weights: 400 (body), 500 (meta, labels, buttons), 600 (subheadings, accents), 700 (primary headings & brand wordmark), 800 (heavy display).
  - No Monospace / Typewriter Clutter: All editorial content, numerals, and badges use clean sans-serif typography.

---

## 5. Buttons & Interactivity
- **Primary Buttons (`btn-primary`)**: Obsidian slate background (`#0F172A`), white text (`#FFFFFF`), smooth radius (`6px` to `8px`), padding `10px 20px`.
- **Secondary Buttons (`btn-outline`)**: Hairline border (`1px solid #E2E8F0`), background `transparent` or `#FFFFFF`, text `#0F172A`.
- **No Neon Buttons**: Never use bright neon green (`btn-green`) or electric cobalt buttons.
