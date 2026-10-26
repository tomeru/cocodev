# CoCoDev lab website

Plain HTML + one stylesheet, hosted on GitHub Pages. No build step.

```
index.html              Home / About
people/index.html       People + alumni
publications/index.html Publications (with a live filter box)
join-us/index.html      Open positions + past projects
lab-photos/index.html   Photo gallery
style.css               All styling (colors and fonts are at the top)
images/                 logo.png, people/<slug>.jpg, join/*.jpg, photos/*.jpg
about-us/, people/<slug>/   Redirects so old Google Sites links keep working
```

## Common edits (all doable on github.com: open file → pencil icon → Commit)

**Add a publication:** in `publications/index.html`, copy an existing `<li>…</li>` line under the right year and edit it.

**Add a person:** in `people/index.html`, copy an existing `<article class="person" …>…</article>` block, change the `id`, name, role, bio and links, and upload their photo as `images/people/<id>.jpg` (square-ish, ~600px).

**Move someone to alumni:** cut their block and add a short `<article class="alum">` entry in the Lab Alumni section.

**Change colors or fonts:** edit the variables at the top of `style.css`.

## Images

Run `python3 fetch_images.py` once, while the old Google Site is still published. It reads fresh image links from the live pages (Google's links expire) and downloads the logo, headshots, Join Us images and Lab Photos.

Lab Photos are saved under these filenames in `images/photos/` (if the script can't match them, it puts them in `images/_unsorted/` for you to rename):

| File | Caption |
|---|---|
| 2023-11-escape-room.jpg | Nov 2023: Successful heist at Red Fox Escape! |
| 2023-tomer-throne.jpg | We put Tomer on the throne! |
| 2023-06-lab-photo.jpg | June 2023: lab photo in front of the Northwest Lab Building |
| 2023-05-retreat.jpg | May 2023: Lab retreat in nature! |
| 2023-05-cco-summit.jpg | May 2023: CCO Summit during the lab retreat |
| 2023-02-bowling.jpg | February 2023: Bowling at Sacco |

Missing images degrade gracefully: people show initials, gallery shows a blank tile.
