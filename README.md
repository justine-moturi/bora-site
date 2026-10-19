# Bora website

Marketing site for Bora, microlending for Kenya's women's groups. Plain static HTML: `index.html` plus `assets/`.

## Deploying

There is one environment. Every commit pushed to `main` deploys to the live site.

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
