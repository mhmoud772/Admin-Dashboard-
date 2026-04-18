# Design System Specification: The Technical Command Paradigm

## 1. Overview & Creative North Star
### The Creative North Star: "The Tactical Observer"
This design system moves away from the chaotic "wall of widgets" common in legacy DevOps tools. Instead, it adopts the persona of a **Tactical Observer**—a high-end, editorialized command center that prioritizes clarity, depth, and intentionality. 

To break the "template" look, we utilize **Intentional Asymmetry**. Dashboards should not be rigid grids; instead, use varying card widths and "broken" layouts where key metrics overlap background containers. This system isn't just about showing data; it’s about providing a curated, premium experience for the engineers who keep the world running.

---

## 2. Colors & Surface Philosophy
The palette is rooted in a deep, atmospheric slate, punctuated by high-energy accents.

### The "No-Line" Rule
**Prohibit 1px solid borders for sectioning.** Boundaries are defined strictly through background color shifts. For example, a `surface-container-low` section sitting on a `surface` background provides all the separation a professional eye needs.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of "Synthetic Glass."
- **Nesting:** Place a `surface-container-high` element inside a `surface-container` to denote active status or focus.
- **The Glass & Gradient Rule:** Use Glassmorphism for floating panels. Apply `surface` colors at 70-80% opacity with a `20px` backdrop-blur. 
- **Signature Textures:** Main CTAs and "System Healthy" states should utilize a subtle linear gradient from `primary` (#adc6ff) to `primary_container` (#4d8eff) at a 135-degree angle to provide a sense of "active energy."

| Token | Value | Role |
| :--- | :--- | :--- |
| `surface` | #0b1326 | Base background layer. |
| `surface_container_low` | #131b2e | Primary dashboard workspace. |
| `surface_container_high` | #222a3d | Elevated cards and interactive nodes. |
| `primary` | #adc6ff | Actionable elements and highlights. |
| `tertiary` | #ffb786 | Warning/Amber (System Latency). |
| `error` | #ffb4ab | Critical alerts (Service Down). |

---

## 3. Typography: Technical Authority
We pair the geometric precision of **Space Grotesk** with the utilitarian clarity of **Inter**. 

*   **Display & Headlines (Space Grotesk):** Used for high-level system status and dashboard titles. The wide apertures and technical feel convey a "Mission Control" aesthetic.
*   **Body & Labels (Inter):** Reserved for data density. Inter's tall x-height ensures readability in high-density logs.
*   **The Monospace Exception:** All API paths, log entries, and CLI snippets must use a monospaced font (e.g., JetBrains Mono) at `label-md` scale to differentiate "Machine Language" from "Human Language."

| Level | Font | Size | Intent |
| :--- | :--- | :--- | :--- |
| `display-lg` | Space Grotesk | 3.5rem | Hero metrics (e.g., 99.9% Uptime). |
| `headline-sm` | Space Grotesk | 1.5rem | Card headers and section titles. |
| `body-md` | Inter | 0.875rem | Standard UI text and descriptions. |
| `label-sm` | Inter | 0.6875rem | Metadata, timestamps, and tags. |

---

## 4. Elevation & Depth
In this system, elevation is a product of **Tonal Layering**, not shadows.

*   **The Layering Principle:** Depth is achieved by "stacking" container tiers. Place a `surface_container_lowest` card on a `surface_container_low` section to create a "recessed" look, ideal for log streams.
*   **Ambient Shadows:** For floating modals only. Use a 32px blur at 6% opacity, tinted with `#001a42` (on_primary_fixed) to mimic light refracting through dark glass.
*   **The Ghost Border:** If high-density data requires extra containment, use the `outline_variant` (#424754) at **15% opacity**. Never use a 100% opaque border.

---

## 5. Components

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary_container`) with `on_primary` text. No border.
*   **Secondary:** `surface_container_highest` background with a `Ghost Border`.
*   **States:** On hover, primary buttons should "glow" using a subtle outer drop-shadow of the `primary` color (15% opacity).

### Cards & Lists
*   **Strict Rule:** No divider lines. Use `0.75rem` of vertical whitespace or a background shift to `surface_container_low` to separate list items.
*   **High Density:** Cards should use `0.25rem` (sm) rounded corners for a sharp, "instrument-panel" look.

### Input Fields & Terminal Emulators
*   **Inputs:** Use `surface_container_lowest` for the field background. The active state is indicated by a 2px `primary` underline rather than a full border glow.
*   **Terminal:** Background must be `surface_container_lowest`. Use `on_surface_variant` for timestamps and `primary` for executable commands.

### Status Chips
*   **Success:** `secondary_container` background with `on_secondary_container` text.
*   **Error:** `error_container` background with `on_error_container` text.
*   **Shape:** Use `full` (9999px) roundedness to contrast against the sharp-edged cards.

---

## 6. Do’s and Don’ts

### Do
*   **Do** use asymmetrical layouts. A 70/30 split for "Main Metric / Side Logs" feels more premium than a 50/50 split.
*   **Do** lean into high-density. Developers prefer seeing more data at once if the typography is clear.
*   **Do** use `backdrop-blur` on navigation sidebars to allow the "soul" of the dashboard colors to peek through.

### Don’t
*   **Don't** use pure black (#000). It kills the depth of the slate tones.
*   **Don't** use standard "drop shadows" on cards. Rely on color shifts between `surface_container` levels.
*   **Don't** use bright white for body text. Use `on_surface_variant` (#c2c6d6) to reduce eye strain during long on-call shifts.