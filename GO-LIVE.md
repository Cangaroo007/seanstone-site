# Go live — seanstone.com

**Status, 28 Aug 2026: the plumbing is done and one step remains.**

| | |
|---|---|
| Repo | `github.com/Cangaroo007/seanstone-site`, public ✓ |
| Pages | Deploy from `main` / root ✓ |
| DNS | Cloudflare, apex + `www` resolving ✓ |
| Certificate | Issued, Enforce HTTPS on ✓ |
| **Content** | **Still the old placeholder page — see step 2 below** |

`https://seanstone.com` and `https://www.seanstone.com` both load, over HTTPS, from the
right repo. What they serve is a three-file placeholder: `CNAME`, `README.md` and an
`index.html` that predates this project. Push the real files and the site changes within
about a minute. Nothing else needs touching.

Everything deployable sits at the repo root, so GitHub Pages serves it with no build step
of its own. `python3 build.py` regenerates `index.html` before you push; GitHub just serves
what it's given.

---

## 1 · ~~Create the repository~~ — done

`github.com/Cangaroo007/seanstone-site`, public, Pages building from `main` / root.

## 2 · Get the real files in — **the one step left**

The repo currently holds an older `index.html`. Uploading ours replaces it; the old one
stays in the commit history if you ever want it back.

**In the browser** (no Terminal needed):

1. Unzip `seanstone-site.zip`. You get a folder called `personal-site`.
2. Repo → **Add file → Upload files**.
3. **Open** the `personal-site` folder, select everything inside it (⌘A), and drag that
   into the upload box — the contents, not the folder itself, or the site ends up one
   level deep and serves nothing.
4. Commit to `main`.
5. The uploader silently skips dotfiles, and `.nojekyll` matters — without it GitHub runs
   Jekyll over the files. So afterwards: **Add file → Create new file**, name it exactly
   `.nojekyll`, leave the body empty, commit.

**Or with git**, which handles the dotfiles for you:

```bash
cd ~/Downloads
unzip -o seanstone-site.zip
git clone https://github.com/Cangaroo007/seanstone-site.git repo
cd repo
rm -f index.html README.md
cp -R ../personal-site/. .
git add -A
git commit -m "Instrumented site v0.4"
git push
```

If git asks for a password, it wants a personal access token, not your GitHub password —
GitHub removed password auth. GitHub Desktop or the browser route above both avoid that.

## 3 · ~~Turn Pages on~~ — done

Deploy from `main` / root, building on every push.

## 4 · ~~DNS in Cloudflare~~ — done

Recorded here for reference, and for the day this ever needs rebuilding.

Cloudflare → seanstone.com → **DNS → Records**. Add five records, **all grey cloud
(DNS only — click the orange cloud to turn it grey)**:

| Type | Name | Content | Proxy |
|---|---|---|---|
| A | `@` | `185.199.108.153` | DNS only |
| A | `@` | `185.199.109.153` | DNS only |
| A | `@` | `185.199.110.153` | DNS only |
| A | `@` | `185.199.111.153` | DNS only |
| CNAME | `www` | `cangaroo007.github.io` | DNS only |

The CNAME points at the *account*, not the repo — no `/seanstone-site` on the end.

**Grey cloud is not optional at this stage.** Proxied, Cloudflare terminates TLS itself and
GitHub never sees the validation request, so the certificate never issues. Same trap as the
Framer records on cangaroo.ai.

Leave the Google MX, SPF and DMARC records alone — none of this touches mail.

## 5 · ~~Point Pages at the domain~~ — done

Custom domain `seanstone.com`, DNS check successful, certificate issued, Enforce HTTPS on.
Kept below for reference.

- The `CNAME` file in the repo already says `seanstone.com`; GitHub may rewrite it with an
  identical commit. Harmless.
- **"Enforce HTTPS" stays greyed out until the certificate issues.** Usually 10–15 minutes,
  occasionally an hour. Tick it the moment it's available.
- If it's still pending after an hour: remove the custom domain, save, re-add it. This
  re-queues the certificate and fixes it most of the time.

## 6 · Verify — after the push

- [x] `https://seanstone.com` loads with the padlock
- [x] `https://www.seanstone.com` resolves
- [x] `http://seanstone.com` upgrades to HTTPS
- [ ] The headline reads "I don't advise on the revenue system. I build it."
      (if it still says "Revenue Operations · GTM · HubSpot + AI", the old page is cached —
      hard-reload with ⇧⌘R, and give Pages a minute)
- [ ] Fonts render as Instrument Serif and Archivo, not fallback Georgia/Helvetica
- [ ] The router, enquiry engine, diagnostic and scope builder all work
- [ ] `https://seanstone.com/case/roadrunner/` opens the case study directly
- [ ] `https://seanstone.com/robots.txt` and `/sitemap.xml` both load
- [ ] Paste the URL into LinkedIn's [Post Inspector](https://www.linkedin.com/post-inspector/)
      and confirm the share card renders
- [ ] Open it on a phone — the telemetry rail should become a bottom drawer

## 7 · Optional, once it's stable

- **Turn the orange cloud on**, if you want Cloudflare's caching and analytics in front of
  it. Only after the certificate has issued, and set **SSL/TLS → Overview → Full (strict)**
  first. Flexible causes a redirect loop with Pages.
- **Verify the domain** in GitHub → Settings → Pages → "Verified domains", which stops
  anyone else claiming seanstone.com on their own Pages account.
- **DKIM for seanstone.com** — still outstanding from the DNS cutover, unrelated to this
  but on the same TXT screen while you're there.
- **Submit the sitemap** in Google Search Console (`https://seanstone.com/sitemap.xml`) and
  verify ownership with a TXT record while you're in Cloudflare anyway. Indexing happens
  without it, but this makes it days rather than weeks — and it's the only way to see what
  people search before they land on you.

---

## Updating the site afterwards

1. Edit `src/site.json` (content) or `src/template.html` (code)
2. `python3 build.py`
3. Commit and push — Pages redeploys in about a minute

Or ask me: I edit the source, rebuild, and hand you the changed files.

## If it goes wrong

Nothing here is destructive. To back it out: delete the five DNS records in Cloudflare and
remove the custom domain in Pages. The domain returns to where it was this morning —
resolving nowhere, mail untouched. The repo can sit there indefinitely.
