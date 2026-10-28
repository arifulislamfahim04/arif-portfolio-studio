# Manage your portfolio without code

See [EDITING.md](EDITING.md) for the visual editor and content management instructions. The new publishing workflow builds from `editor/` and retains the existing design in `templates/`. GitHub Pages should use **GitHub Actions** after this integration is activated.

The following original export notes are retained for reference; use the new editing guide for updates.

# Arif — Personal Portfolio

The original five-page portfolio for Ariful Islam Fahim, exported from the latest portfolio studio source. Includes Home, About, Blogs, Projects, Contact, styles, JavaScript, fonts, images, and the résumé PDF.

## GitHub Pages

In **Settings → Pages**, choose **Deploy from a branch**, then **main** and **/docs**, and save. The published website is served entirely as static files by GitHub Pages.

## Edit and preview

`dist/` holds the original website files. `docs/` is the matching GitHub Pages publication copy. No Node.js, server, API key, or paid hosting is required.

```sh
python -m http.server 8000 --directory docs
```

Open http://localhost:8000. Edit the HTML, CSS, and JavaScript directly. Keep `dist/` and `docs/` synchronized when making changes.

## Optional page generator

The original generator and content inputs are included. To regenerate pages, use Python 3:

```sh
python -m pip install -r requirements.txt
python build_portfolio.py
python publish_pages.py
```

The generator uses the bundled Bootstrap icon sprite. It generates HTML and content data; CSS and interaction scripts are maintained directly. Existing unfinished portfolio content is preserved.

## Contact form

The form opens the visitor’s email application with a prepared draft. The visitor must send it there. GitHub Pages does not provide a message backend.

## Assets

Asset credits and third-party license notices are retained in `ICON-SOURCES.md` and `dist/assets/`. The résumé PDF is included as linked by the original portfolio. No ChatGPT sign-in is required on GitHub Pages.
