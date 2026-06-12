# NexStudio UI Migration Plan

## Scope
- Redesign only the visual layer in the existing frontend pages.
- Preserve all current API calls, form submissions, authentication flow, and business logic.
- Do not modify backend code, Flask APIs, PostgreSQL models, authentication, routes, or database behavior.

## Current Frontend Inventory
The current project already has the right structure for a UI-only redesign:
- Pages: [frontend/index.html](frontend/index.html), [frontend/about.html](frontend/about.html), [frontend/projects.html](frontend/projects.html), [frontend/blog.html](frontend/blog.html), [frontend/contact.html](frontend/contact.html)
- Styling: [frontend/css/style.css](frontend/css/style.css), [frontend/css/responsive.css](frontend/css/responsive.css), [frontend/css/animations.css](frontend/css/animations.css)
- Interactivity: [frontend/js/app.js](frontend/js/app.js), [frontend/js/api.js](frontend/js/api.js), [frontend/js/gsap.js](frontend/js/gsap.js), [frontend/js/swiper.js](frontend/js/swiper.js)

The current design system already uses:
- a premium monochrome palette
- rounded cards and soft borders
- GSAP scroll animations
- hover lift / zoom utilities
- responsive breakpoints for desktop, tablet, and mobile

## Migration Strategy
1. Keep the existing HTML page skeleton and current IDs/classes for the working JS.
2. Refactor only the visual presentation in CSS and select HTML sections to match the NexStudio aesthetic.
3. Reuse existing content blocks and assets before introducing new visual components.
4. Preserve existing JS hooks for filters, forms, calendar, newsletter, and API interactions.

## Page-by-Page UI Work Plan

### 1. Home Page
- Refine the hero section with stronger hierarchy, spacing, and a premium editorial layout.
- Upgrade the partner logos strip into a clean monochrome marquee.
- Rework the about, services, and projects preview sections into a luxury agency visual system.
- Refresh testimonials and blog preview cards with consistent rounded cards, border treatment, and hover motion.
- Keep existing CTA buttons and footer structure intact while improving the visual styling.

### 2. Projects Page
- Rebuild project cards into a darker, more cinematic grid with subtle borders and hover lift.
- Keep the existing filter pills and data-driven project loading behavior unchanged.
- Improve image framing, spacing, and hover zoom while maintaining the current project data flow.

### 3. Blog Page
- Rework blog card layout with stronger image framing, category chips, and refined spacing.
- Keep the existing search input, category filters, and pagination logic untouched.
- Update only the look-and-feel of the cards and page hero to match the premium agency style.

### 4. About Page
- Re-design the story, stats, and team sections into a more editorial and premium composition.
- Keep the current team content, counters, and GSAP animation triggers.
- Upgrade the cards and spacing while preserving all existing text and data.

### 5. Contact Page
- Re-style the two-column layout with a modern form card and a polished scheduling panel.
- Keep the existing service selection pills, form fields, and calendar interactivity untouched.
- Update only the container styling, spacing, border treatment, and button presentation.

## Design Direction
Apply the NexStudio reference feel using the current design language:
- Black / white / warm gray palette
- Large whitespace and strong section rhythm
- 24px rounded corners
- Thin borders and elevated card surfaces
- Smooth GSAP fade-up, stagger, hover lift, and zoom transitions

## Implementation Guardrails
- Do not touch [backend/](backend/) or any Flask route logic.
- Do not change [backend/models.py](backend/models.py) or authentication behavior.
- Do not alter [frontend/js/api.js](frontend/js/api.js) unless purely cosmetic and non-functional.
- Keep current page links, forms, and JS selectors stable so the UI remains fully functional.

## Verification Checklist
After the visual redesign:
1. Open each page and confirm sections render correctly.
2. Confirm project/blog filters still work.
3. Confirm contact form and newsletter form still submit through the existing API path.
4. Confirm mobile/tablet navigation still opens and closes properly.
5. Confirm no backend or API routes were changed.

## Recommended Execution Order
1. Update the shared design system in [frontend/css/style.css](frontend/css/style.css).
2. Tune responsive behavior in [frontend/css/responsive.css](frontend/css/responsive.css).
3. Refine animation polish in [frontend/css/animations.css](frontend/css/animations.css).
4. Adjust page-specific section structure in the HTML files only where needed for visual hierarchy.
5. Verify with the existing JS and API behavior before final review.
