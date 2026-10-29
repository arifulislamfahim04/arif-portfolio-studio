# About and CMS review

About now uses the approved mint/Poppins presentation, right-hand navigation, light/dark switch, social footer and filled SVG Repo icons. Biography, personal facts, education, experience, skills, awards, certificates, recommendations and CV remain connected to existing CMS data.

## CMS editing

- **About**: biography (rich text), personal information, at-a-glance facts, skills and languages. Formatting in biography and detail bodies supports bold, italic and underline.
- **Page headings & SEO → About**: page title, heading, introduction and metadata.
- **Education / Experience / Achievements / Certificates / Workshops**: add, edit, remove and reorder individual records; optional detail fields, images and supporting documents remain optional.
- **Homepage · hero, previews & highlights → Card and footer contact buttons (up to 4)**: order up to four buttons; choose Email/LinkedIn/Facebook to reuse Profile, or Custom URL for another platform. Blank destinations hide their buttons. This applies to the reviewed Home and About pages.
- **Profile, résumé & homepage → Email / LinkedIn / Facebook**: edit the real contact destinations. Empty Facebook stays hidden.
- **Homepage · hero, previews & highlights → Replace icons (Home and About)**: select the icon key, then upload a transparent SVG from SVG Repo in the SVG icons media area. Empty upload restores the filled default. Uploaded SVGs render as colour-inheriting masks, not executable markup.
- **Profile, résumé & homepage → Homepage statistics → Filled statistic icon**: select a default filled icon per counter.

Other pages retain their existing presentation until their individual reviews. Icon overrides will be connected to those pages when they are updated.

## Fixed and verified

- Repeated award titles previously acquired each other's detail panels. Cards now match their unique CMS entry IDs; each of the five current awards has one panel.
- Safe defaults for references and transcript visibility are preserved. The source About JSON was not modified. Visibility controls affect rendering; they cannot make records in a public Git repository confidential.
- Tests cover social addition/removal, empty Facebook, custom URL, uploaded icon/reset, awards, active About navigation and isolated page styling. General content lifecycle and optional-field tests pass.
- Chromium checks: 375px (light and dark), 768px and 1280px; no horizontal overflow in sampled states. Education disclosure opens; theme and active About navigation work.
- Not verified: actual Android/iOS hardware, screen reader audit, complete contrast/Lighthouse audit, live Pages CMS upload clicks and real certificate/PDF transfer.

No new photography or icon pack. Existing images, icon sources and licences are retained. Main and the original GitHub Pages deployment remain unchanged.

## Education card v2 — 29 October 2026

- BSc: featured three-zone layout, 88px CGPA ring, date-based elapsed-period bar, Results pending, expected December 2026. Start retained October 2022; existing 3.90/4.00 unchanged.
- HSC and SSC: compact GPA chips, existing 4.92/5.00 and 4.67/5.00 retained.
- CMS → Education → choose entry: featured switch, subtitle, result label/value/scale, dates, expected date switch, current status, institution website/logo, major, focus, location, courses, thesis, transcript link, optional public student ID and additional details. Add/reorder/remove via the collection.
- Logos: SVG/PNG/JPG/WebP media folder `assets/institutions`; initials until an official logo is supplied. No new third-party asset.
- Empty optional facts disappear. All existing extra facts, supporting documents, media and safe rich text remain supported. Transcript only comes from the entry’s explicit public link; no private profile transcript is automatically exposed.
- Institution arrow reuses the bundled SVG Repo filled-arrow asset and respects the existing Arrow icon override. Institution links open independently from the full-width disclosure row.
- Animation: ring stroke reveal, status-dot opacity, date bar transform, 300ms disclosure height and plus rotation; reduced motion bypasses these. Logo grayscale and card spotlight are limited decorative effects.
- Checked: content lifecycle/schema/optional field tests, safe rich text, local references, JS syntax. Chromium desktop light/dark and 375/768px iframe layouts; no page horizontal overflow. Mouse and keyboard disclosure checked. Actual phone hardware, OS reduced-motion switch and live CMS upload UI remain unverified.
- The review Site remains a built snapshot; CMS edits to the review GitHub branch need a rebuild to appear there. Main is unchanged.
