# Jiahao Xie Academic Homepage

Standalone static academic homepage prepared outside `/home/axie/web` for GitHub Pages deployment.

## Structure

- `index.html` — single-page academic homepage
- `style.css` — standalone styling, no build step
- `assets/avatar.jpg` — profile portrait copied from the current personal site
- `assets/favicon.svg` — favicon copied from the current personal site
- `.nojekyll` — disables Jekyll processing on GitHub Pages
- `tests/validate_site.py` — static sanity checks

## Local verification

```bash
python tests/validate_site.py
python -m http.server 8766
```

Then open <http://127.0.0.1:8766/>.

## GitHub Pages deployment

Create a repository such as `AxiEj.github.io` or another Pages-enabled repository, copy/push this directory, then enable Pages from the repository settings if needed.
