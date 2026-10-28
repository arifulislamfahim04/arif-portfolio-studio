# Major revision audit — 28 October 2026

The baseline was inspected before implementation. `major-revision-audit.json` retains the measured baseline and 60 revised viewport/theme cases.

Viewports: 1920×1080, 1440×800, 1366×700, 1024×768, 768×1024, 375×812. Each of the five revised pages was checked in dark and light themes.

| Known issue | Resolution |
|---|---|
| 1. Oversized laptop hero | A viewport-constrained desktop stage and height-aware type/spacing. At 1366×700, actions end at 490px; full stats end at 692px. |
| 2. Wrapped/clipped name | Single-line name, responsive card width and font size. Measured without overflow at all six sizes. |
| 3. Doubled outline contours | Static contour-merged Bricolage font; tested A–Z. Positive tracking on outlined text. |
| 4. Jumping/fading typewriter | Reserved grid cell measures all phrases. Absolutely overlaid live text keeps constant fill/stroke and one caret. Same dimensions verified mid-deletion and full phrase. |
| 5. Gradient hover floods | Removed gradient text. Single-colour fill with a short fade and stable outline/tracking. |
| 6. Dock hover blob | Per-button backgrounds, contained active marker, no separate blob. |
| 7. Tall/clipped navigation | Height-aware control sizes; five items; bottom bar below 1200px or below 700px height. |
| 8. Narrow content behind side dock | The bottom-bar breakpoint replaces the side dock; desktop shell reserves right space. |
| 9. Contact icons after labels | Label-only rows; four distinct solid badges outside the input and to its left. |
| 10. Filled cursor disc | 8px translucent dot, 28px transparent ring, 32px hover ring, no filled ring background. |
| 11. Old bird and placeholder blocks | X available in the shared solid set; only supplied LinkedIn profile is displayed. Unprovided social profiles hidden. AF monogram replaces portrait instructions. One recommendation empty state replaces fake reviews. |
| 12. Marquee | 16–17px Inter, spaced items, edge masks, complete duplicate track. |
| 13. Inconsistent headings | One centered selectable ghost/label/title component on every page and section. |
| 14. Large empty gaps | Shared 64–120px section spacing; no allocated empty ghost region. |
| 15. Duplicate About numbers | Home retains stats; About has focus, supported study stage, languages, and availability. |

Additional changes: five real document routes; single education timeline; independent experience timeline; grouped skill stages and language dots; five award cards with drag/inertia/snap/arrows/dots/lightboxes; separate certificates and transcript viewer; blog search/categories/reader; textile-first project ordering/filtering; map styling/mobile opt-in; contact validation/mail-draft confirmation; scroll-progress back-to-top; stitch page transition.

Runtime checks: project/category filters, blog search, opaque reader and custom scrollbar, native modal focus restoration/Escape, document zoom and next/previous, contact required-field errors and clipboard confirmation, menu routes, theme switch, carousel scroll and chosen-card state. Carousel QA uncovered a programmatic-scroll selection reset; manual and programmatic scroll tracking are now separate.

All 60 layout cases had no horizontal page overflow, no checked heading/value clipping, no text under 14px, no navigation-control size mismatch, and no navigation controls outside the viewport. Reduced-motion branches are provided in CSS and JS; OS emulation was not available in the browser API.

## Asset/content limits

- User portrait not provided: a quiet AF identity panel uses a real textile photo, not a fabricated portrait.
- Certificate, award, transcript scans were not in the source assets. Their viewers show retained CV records, with explicit original-document availability states and email actions. No certificate or transcript image was fabricated.
- Current semester number is not supplied; the supported final-year study stage is used.
- No Facebook, YouTube or X profile URL was supplied, so no guessed or dead profile links are displayed.
- Solid Bootstrap Icons 1.13.1, MIT, official inline SVG fallback. The license and icon inventory are stored alongside assets.
- Two Unsplash textile photographs, indigo duotone treatment. Alt text and attribution records are included.
