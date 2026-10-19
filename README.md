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
