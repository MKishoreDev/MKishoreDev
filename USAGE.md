# Profile README Workspace Template Guide

This repository is configured as a public template. You are welcome to fork, copy, or adapt this lo-fi coding workspace theme for your own GitHub profile README!

---

## ⚠️ Important Template Notice

> [!WARNING]
> **Do not use this repository's personal details as-is!**
> This repository contains personal information, links, and API configurations belonging to the original developer. When copying or forking this template, **you must replace all personal details with your own information.**

### Checklist of items to replace:

1. **GitHub Username:**
   * In [README.md](file:///c:/Users/kishore/Downloads/MKishoreDev-main/MKishoreDev-main/README.md), replace all instances of `MKishoreDev` with your own GitHub username (including in Shields.io badges, visitor counters, and statistics URLs).
   * In `.github/scripts/update-commits.py`, replace `MKishoreDev` in the GitHub Search API query (`q=author:MKishoreDev`) with your own username to fetch your own commits.

2. **Personal Portfolio & Social Links:**
   * In `README.md`, update the `ELSEWHERE` table and website links with your own links and usernames.
   * Replace the domain `mkishore.is-a.dev` with your own website or portfolio URL.

3. **Blogs Index Integration:**
   * In `.github/scripts/update-blogs.py`, replace the URL `https://mkishore.is-a.dev/blogs/index.json` with the JSON index feed of your own blog posts. The JSON file should follow this structure:
     ```json
     [
       {
         "slug": "article-slug",
         "title": "Article Title",
         "date": "YYYY-MM-DD",
         "tags": ["tag1", "tag2"],
         "readTime": 5
       }
     ]
     ```

4. **Dynamic Quote API:**
   * The quote card pulls programming quotes from a public repository. If you have your own quote database or API, update the fetch URL inside `.github/scripts/update-quote.py`.

---

## 🎨 Visual Features

This template includes several visual enhancements that are fully compatible with GitHub README rendering:

### Loading Animations
* All 9 SVG assets (`banner.svg`, `commits.svg`, `quote.svg`, `journey.svg`, `divider.svg`, `footer.svg`, `blog-1.svg`, `blog-2.svg`, `blog-3.svg`) feature a subtle **shimmer loading animation** using SMIL `<animate>` elements.
* Shimmers are **staggered** across SVGs (0s → 2.4s) so they pulse organically instead of in unison.
* All animations respect `prefers-reduced-motion` for accessibility.

### Interactive Elements
* **Commits Card** — The `commits.svg` is wrapped in a clickable link that opens `commits.txt`, a plain-text file generated hourly with full commit details (SHA, repo, message, time, direct URL).

### Accessibility
* Every generated SVG includes `<title>` and `<desc>` elements for screen readers.
* All animations are designed to be subtle and non-distracting.

### Live Timestamp
* The banner's top-right HUD corner displays a live IST timestamp (`DD Mon YYYY · HH:MM IST`) injected by `.github/scripts/update-banner.py` on every workflow run.

---

## 🚀 How to Set Up the Automated Actions

To enable the hourly profile updates:

1. **Enable Workflow Permissions:**
   * In your repository settings on GitHub, go to **Settings** > **Actions** > **General**.
   * Scroll down to **Workflow permissions** and select **Read and write permissions**.
   * Click **Save**.

2. **Run the Workflow:**
   * The workflow [update-profile.yml](file:///c:/Users/kishore/Downloads/MKishoreDev-main/MKishoreDev-main/.github/workflows/update-profile.yml) runs automatically every hour.
   * You can also trigger it manually by going to the **Actions** tab, selecting **Update Profile README**, and clicking **Run workflow**.

3. **Rate Limits & Secret Token:**
   * The action uses the default repository `GITHUB_TOKEN` to fetch commits and update the profile without hitting GitHub API rate limits. No extra setup is required!

---

## 🛠️ Customization Ideas

Want to make this template your own? Here are some ideas:

* **Social Preview Image** — Upload a custom banner in your repo settings so link previews on Twitter/Discord/Slack look branded.
* **Typing SVG Pause-on-Hover** — Add `&pause=10000` to the typing SVG URL so the text freezes when hovered, making it easier to read.
* **Custom Color Palette** — Edit the gradient stops in each SVG's `<defs>` section to match your personal brand colors.
