# Bora website

Marketing site for Bora, microlending for Kenya's women's groups. Plain static HTML: `index.html` plus `assets/`.

## Deploying

Hosted on GitHub Pages at https://justine-moturi.github.io/bora-site/. There is one environment: every commit pushed to `main` deploys to the live site within a minute or two.

```sh
git add -A
git commit -m "Describe the change"
git push
```

## Preview locally

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Rebuilding from the working copy

The page is edited in the working copy (`Bora — Microlending for Kenya's women's groups.html` in its `_files` folder), then rebuilt into this repo:

```sh
python3 tools/build_site.py "<path to the _files folder>" .
```

The script strips the Lovable scripts and badge, swaps the contact form for an "Email us" button, rewrites asset paths to `assets/`, and copies only the assets the page uses.
