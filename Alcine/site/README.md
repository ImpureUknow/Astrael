# ASTRAEL WIKI site

This folder is a static website and can be uploaded directly to:

* GitHub Pages
* Netlify
* Cloudflare Pages
* Any static web host

## Main files

* `index.html` - page shell
* `content.md` - wiki content shown on the site
* `styles.css` - visual design
* `app.js` - search, table of contents, theme, and section links
* `assets/hero.webp` - hero image
* `standalone.html` - single-file version inside the site bundle
* `../astrael-wiki-standalone.html` - duplicate single-file version placed at the project root for easy sharing

## Update content

Edit `content.md`, then upload the folder again.

If you need a fresh single-file copy after editing the wiki, rebuild `../astrael-wiki-standalone.html` from the updated site files.

## Local preview

Run the included local server from inside this folder:

```powershell
node dev-server.mjs 4173
```

Then open:

```text
http://127.0.0.1:4173
```
