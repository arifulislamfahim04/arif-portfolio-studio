# Edit your portfolio without code

Open **https://app.pagescms.org/** and sign in with your GitHub account.
Install Pages CMS for **only `arif-portfolio-studio`**, then select that repository and its `main` branch.
Your editor reads the `.pages.yml` configuration automatically.

## Daily editing

- **Profile, résumé & homepage**: choose your portrait, replace your résumé PDF, edit your introduction, contact details and statistics. A portrait replaces the decorative monogram. Leave it empty to retain the original textile design.
- **Biography, skills & references**: update your biography, repeating information fields, languages, skills and recommendations. Upload a transcript when available.
- **Blogs & articles / Projects**: click New, enter a title and summary, then write in the visual editor. Use headings, lists and image uploads between paragraphs. Add captions through Extra pictures. You can paste common formatting from Word; complex Word page layouts may need adjustment.
- **Education / Experience / Certificates / Achievements / Workshops**: click New for every new entry. There is no fixed number of entries. Upload a certificate PDF or picture to let visitors view it.
- **Show on website**: turn OFF to save an unpublished entry; ON to publish. Lower display-order numbers appear first.
- **Pictures, résumé & certificates**: organize media in folders if useful. Upload a file, then select it in the appropriate content field. You do not need fixed filenames. Uploading an image alone does not select it as your profile photo.

Save the entry. GitHub Actions builds and publishes the website automatically, usually within a few minutes. Check **Actions → Publish portfolio content** if an update has not appeared. A failed build keeps the last successful deployment live.

Each published blog/project has a shareable page URL as well as a reading dialog. Changing its filename changes its URL. Updating only its title does not require renaming it.

## Important practical details

The public site and repository are public. Unpublished entries are omitted from the website, but their text and uploaded files remain visible in the public GitHub repository. Do not use this as private storage for confidential drafts or documents. Keep certificate files suitable for public viewing.

Use YouTube links for large videos to keep repository storage manageable. Small MP4/WebM uploads also work. There is no paid domain, database, hosting subscription, or API key required by this setup.

GitHub history keeps previous versions of saved files. The content is stored in standard JSON and media files, so it can be moved if the editor changes in the future. A deletion remains in repository history; deleting a file does not erase all historical copies.

## For future maintainers

`editor/` is the content source. `templates/` retains the existing design. `docs/assets/` contains media. `.pages.yml` configures Pages CMS. `scripts/build_editor.py` builds the website and `.github/workflows/publish.yml` publishes it.

Run `python -m pip install -r requirements.txt`, `python scripts/build_editor.py`, then `python scripts/check_site.py`. The older `build_portfolio.py`, `content/` and `dist/` are retained for historical reference; do not use them for routine publication because they predate the editor.

GitHub Settings → Pages must use **GitHub Actions** as the source. Never put a GitHub token in frontend HTML or JavaScript. Pages CMS performs authenticated edits through its GitHub App.
