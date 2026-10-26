#!/usr/bin/env python3
"""
Download the CoCoDev images from the LIVE Google Site into ./images.

Google Sites image links are temporary (they expire after a while), so this
script re-reads each page to get fresh links, then downloads them right away.
Run it from inside the site folder, while the Google Site is still published:

    python3 fetch_images.py

Uses only the Python standard library plus the `curl` command (both built into macOS).
"""
import html, os, re, subprocess, sys

SITE = "https://www.cocodev.org"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
ICON_ALTS = {"email", "link", "github", "twitter", "youtube", "linkedin", "bluesky", "x", "instagram", "facebook"}

# What each page should contain, in page order.
PEOPLE = ["tomer", "lonnie", "peng", "junyi", "jenn", "felix", "eric", "yichen", "yingqiao", "sonia",
          "whitney", "yuki", "zihan", "sophie", "mariel", "john", "chloe", "jiayi", "kiera"]
JOIN = ["object-representation", "play", "creative-problem-solving"]
PHOTOS = ["2023-11-escape-room", "2023-tomer-throne", "2023-06-lab-photo",
          "2023-05-retreat", "2023-05-cco-summit", "2023-02-bowling"]

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def curl(url, out=None, referer=SITE + "/"):
    cmd = ["curl", "-fsSL", "--retry", "2", "-A", UA, "-e", referer, url]
    if out:
        cmd[1:1] = ["-o", out]
    r = subprocess.run(cmd, capture_output=True, text=out is None)
    if r.returncode != 0:
        return None
    return r.stdout if out is None else True


IMG_URL = r"https://lh\d+-\w+\.googleusercontent\.com/sitesv-images-rt/[A-Za-z0-9_\-]+"


def page_images(path):
    """Return content-image base URLs on a page, in page order (icons and logo removed)."""
    src = curl(SITE + path)
    if src is None:
        sys.exit(f"Could not load {SITE + path}. Is the Google Site still published?")
    logo = set(re.findall(r'og:image"\s+content="(' + IMG_URL + ")", src))
    found, seen = [], set()
    # Walk <img> tags and inline background-image URLs in document order.
    for m in re.finditer(r"<img\b[^>]*>|url\(['\"]?(" + IMG_URL + ")", src):
        tag = m.group(0)
        if tag.startswith("<img"):
            alt = html.unescape((re.search(r'\balt="([^"]*)"', tag) or [None, ""])[1]).strip().lower()
            u = re.search(IMG_URL, html.unescape(tag))
            if not u or alt in ICON_ALTS:
                continue
            url = u.group(0)
        else:
            url = m.group(1)
        if url in logo or url in seen:
            continue
        seen.add(url)
        found.append(url)
    return found, logo


def save(url, dest, width):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    ok = curl(f"{url}=w{width}", dest)
    print(("  ok   " if ok else "  FAIL ") + dest)
    return bool(ok)


def grab(path, names, folder, width):
    print(f"\n{SITE}{path}")
    urls, logo = page_images(path)
    if len(urls) != len(names):
        # Layout didn't match expectations: keep everything, numbered, for manual renaming.
        print(f"  Expected {len(names)} images, found {len(urls)}. Saving them numbered in "
              f"images/_unsorted{path}/ so you can rename them by eye.")
        for i, u in enumerate(urls, 1):
            save(u, f"images/_unsorted{path}/{i:02d}.jpg", width)
        return logo
    for name, u in zip(names, urls):
        save(u, f"{folder}/{name}.jpg", width)
    return logo


logo = grab("/people", PEOPLE, "images/people", 600)
grab("/join-us", JOIN, "images/join", 1200)
grab("/lab-photos", PHOTOS, "images/photos", 1600)
if logo:
    print("\nLogo")
    save(sorted(logo)[0], "images/logo.png", 256)

print("\nDone. Open index.html (or the GitHub Pages preview) to check the photos.")
