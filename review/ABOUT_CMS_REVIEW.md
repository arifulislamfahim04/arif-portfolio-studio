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

### HSC / SSC follow-up
Both completed qualifications now use the same full three-zone card and animated 88px GPA ring as the BSc, with Science group subtitle, editable Group fact, and a static Completed badge. No elapsed-period bar for these completed entries. The existing grades/dates/institutions are unchanged. The optional compact layout remains available by disabling Featured education card.

### Completed timeline bars and phone layout
HSC/SSC now keep full timeline bars using their existing year-only dates (no invented study months). BSc continues filling and stays visible at 100% after its end date; status stays manually editable. Date fields support years, months or days. The CMS timeline toggle applies to both completed and ongoing qualifications. On phones, logo and grade ring occupy the top row and the degree/institution block gets the full width below.

Phone QA for completed bars: Chromium iframe viewports 320, 375, 390, 430 and 768px in light and dark; no horizontal overflow on page/cards; phone rings 76px, tablet rings 88px. HSC and SSC report 100%; BSc 96% on 29 October. HSC detail opened successfully at 375px. Physical Android/iOS and touch hardware not available. Timeline caption is CMS-editable.

### Education hierarchy polish
Replaced repeated date line with CMS Programme duration (4-year/2-year programme), kept dates under the bar with Expected on BSc, cleared the optional timeline caption, moved CGPA/GPA inside the ring, centred logo/ring on the same axis (measured 0px delta on desktop/320/375/768), trimmed bottom padding, softened the existing filled arrow, and added CMS Softly pulse the status dot. Only BSc pending status pulses; reduced motion stops it. Browser light/dark overflow checks passed; physical phone testing remains unavailable.

## Step 2 — About navigation and timelines
Left section navigation now uses generated numbers, faint hover tint, a distinct 3px active bar, visible keyboard focus and a thin progress track scoped to About sections. Mobile uses sticky chips with active-item centring; manual pointer/wheel interaction suppresses automatic movement temporarily. Fixed duplicate global scroll-padding plus anchor-margin offset. Desktop target top measured 110px below an 88px header; 320px target cleared header plus chip row.
Education, Experience and Certificates/Workshops use a 2px neutral track with scroll-driven mint fill; 12px state dots align with each title’s first line. Per-card reveal replaces nested legacy reveals (12px fade-up, up to 60ms increments). Reduced motion disables entrance/pulse; progress remains informational. Awards and Skills are unchanged.
CMS → Education / Experience / Certificates / Workshops → entry → Timeline marker state: completed, in-progress, results-pending, upcoming. Marker state is independent of all dates, result and status text. Existing current class representative uses in-progress; BSc uses results-pending.
Checks: build/local references, existing education/optional/About tests, new timeline lifecycle checks, JS syntax; Chromium desktop plus 320/375/768px layouts in light/dark. Certificates active tracking and header clearance verified, 375px active chip centred. Physical Android/iOS swipes, screen reader and OS reduced-motion switching remain unverified.

## Two-zone Now, identity and contact panel
Mint-tinted Now zone (~40%) and facts/contact (~60%), stacked below 800px; phone identity is one column. Source wiring: Profile → Availability, name, location, email, phone; About → Information → Nationality and any custom facts; About → Languages → titles only (proficiency stays in Skills/Languages). Education → selected entry (Use this qualification in the About Now panel) → status, specialization, programme years/year reached. BSc is selected with four reached segments and Results pending; the old Final year glance text is not duplicated.
About design, motion & recommendations → Now panel labels, level suffix, optional WhatsApp URL/text, optional profile last reviewed date, and copy feedback strings. WhatsApp and reviewed date are blank/hidden by default. No fake fresh date; phone is not assumed to be a WhatsApp number. New institutions/photos are not needed. Icons reuse bundled SVG Repo paths and CMS overrides.
One divider separates identity from contact. Email/phone text are mailto/tel links; separate copy controls show a check and 1.5-second polite feedback after browser copy reports success. Controls stay visible on touch and on keyboard focus. Toast is moved to the body to avoid clipping by card transform/overflow. On copying failure the UI reports failure, not success.
Checks: CMS lifecycle tests update/clear status/specialization/years/WhatsApp/review date; existing About/timeline/optional tests and local-link check pass. Browser desktop and 320/375/768px light/dark overflow checks pass; small screen specialization font and email break point improved. Mouse/keyboard copy-success feedback checked. Browser virtual clipboard refused an independent paste verification, so actual clipboard contents and real-device touch remain unverified. OS reduced-motion/screen-reader checks not performed. Main remains unchanged; review remains a build snapshot.
