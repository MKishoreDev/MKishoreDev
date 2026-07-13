# update-commits.py — fetch latest commits, rewrite assets/commits.svg, write commits.txt
# runs in GitHub Actions every hour. no dependencies. python 3.

import json
import urllib.request
import os
import sys
from datetime import datetime, timezone, timedelta

FALLBACK_COMMITS = [
    {"repo": "MKishoreDev", "sha": "3295847", "message": "chore(quote): refresh profile quote card", "time": "recent", "url": "https://github.com/MKishoreDev/MKishoreDev/commit/3295847"},
    {"repo": "MKishoreDev", "sha": "81c103c", "message": "refactor: optimize asset styling and path layouts", "time": "1d ago", "url": "https://github.com/MKishoreDev/MKishoreDev/commit/81c103c"},
    {"repo": "SerenaRobot", "sha": "a4f912c", "message": "feat: add rate limiting support for telegram groups", "time": "2d ago", "url": "https://github.com/MKishoreDev/SerenaRobot/commit/a4f912c"},
    {"repo": "MKishoreDev", "sha": "fa20d1e", "message": "feat: add recent activity and blog post SVGs", "time": "3d ago", "url": "https://github.com/MKishoreDev/MKishoreDev/commit/fa20d1e"},
    {"repo": "MKishoreDev", "sha": "6f15b1f", "message": "style(commits): optimize layout coordinates", "time": "4d ago", "url": "https://github.com/MKishoreDev/MKishoreDev/commit/6f15b1f"}
]

def esc(s):
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))

def truncate(text, max_chars):
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 3] + "..."

def time_ago(date_str):
    try:
        # Standard GitHub ISO: e.g. 2026-07-12T09:33:04.000Z
        if date_str.endswith("Z"):
            date_str = date_str[:-1] + "+00:00"
        past = datetime.fromisoformat(date_str)
        now = datetime.now(past.tzinfo)
        diff = now - past
        seconds = diff.total_seconds()
        
        mins = int(seconds // 60)
        hours = int(mins // 60)
        days = int(hours // 24)
        
        if mins < 1:
            return "just now"
        if mins < 60:
            return f"{mins}m ago"
        if hours < 24:
            return f"{hours}h ago"
        return f"{days}d ago"
    except Exception as e:
        print(f"Time parsing failed: {e}", file=sys.stderr)
        return "recent"

def fetch_commits():
    url = "https://api.github.com/search/commits?q=author:MKishoreDev&sort=author-date&order=desc"
    headers = {
        "User-Agent": "MKishoreDev-README/1.0 (+github actions)",
        "Accept": "application/vnd.github.cloak-preview+json"
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get("items", [])
            if not isinstance(items, list):
                raise ValueError("invalid api response")
            
            commits = []
            for item in items:
                msg = item.get("commit", {}).get("message", "")
                is_bot = (msg.startswith("chore(quote):") or 
                          msg.startswith("chore(snake):") or 
                          msg.startswith("chore(blogs):") or 
                          msg.startswith("chore(commits):") or 
                          msg.startswith("chore(profile):") or 
                          msg.startswith("chore: automated") or 
                          "automated profile update" in msg or
                          "github-actions" in msg)
                if is_bot:
                    continue
                
                commits.append({
                    "repo": item.get("repository", {}).get("name", ""),
                    "sha": item.get("sha", "")[:7],
                    "message": msg.split("\n")[0][:76],
                    "time": time_ago(item.get("commit", {}).get("author", {}).get("date", "")),
                    "url": item.get("html_url", "")
                })
            
            if len(commits) == 0:
                return FALLBACK_COMMITS
            return commits[:5]
    except Exception as e:
        print(f"commits fetch failed: {e}", file=sys.stderr)
        return FALLBACK_COMMITS

def main():
    commits = fetch_commits()
    line_h = 26
    start_y = 80

    commit_lines = []
    for i, c in enumerate(commits):
        y = start_y + i * line_h
        opacity = 0 if i == len(commits) - 1 else 0.5
        repo_display = truncate(f"[{c['repo']}]", 18)
        
        commit_lines.append(f"""
    <g transform="translate(60, {y})">
      <!-- bullet point branch dot -->
      <circle cx="10" cy="-5" r="3" fill="#a78bfa" opacity="0.8"/>
      <line x1="10" y1="5" x2="10" y2="18" stroke="#432874" stroke-width="1.2" opacity="{opacity}"/>
      
      <!-- sha -->
      <text x="30" y="0" font-family="ui-monospace,monospace" font-size="12" fill="#a78bfa">#{esc(c["sha"])}</text>
      
      <!-- repo chip -->
      <text x="95" y="0" font-family="ui-monospace,monospace" font-size="12" fill="#8a7a9d">{esc(repo_display)}</text>
      
      <!-- message -->
      <text x="230" y="0" font-family="ui-monospace,monospace" font-size="12.5" fill="#f5e6d3">{esc(c["message"])}</text>
      
      <!-- time -->
      <text x="1080" y="0" font-family="ui-monospace,monospace" font-size="11.5" fill="#8a7a9d" text-anchor="end">{esc(c["time"])}</text>
    </g>""")

    commit_lines_str = "\n".join(commit_lines)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 230" width="1200" height="230" role="img" aria-label="recent git commits">
  <title>Recent Git Commits</title>
  <desc>Latest {len(commits)} public commits by Kishore M, updated hourly.</desc>
  <style>@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}</style>
  <!-- commits.svg · generated by .github/workflows/update-profile.yml -->
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0c0717"/>
      <stop offset="100%" stop-color="#140b24"/>
    </linearGradient>
    <linearGradient id="cBorder" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#432874" stop-opacity="0"/>
      <stop offset="50%"  stop-color="#a78bfa" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#432874" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="shimmer" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#a78bfa" stop-opacity="0"/>
      <stop offset="50%" stop-color="#a78bfa" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="#a78bfa" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="230" fill="url(#cbg)"/>
  <rect width="1200" height="230" fill="url(#shimmer)" pointer-events="none">
    <animate attributeName="x" values="-1200;1200" dur="4s" repeatCount="indefinite" begin="0.9s"/>
  </rect>
  <rect x="30" y="20" width="1140" height="190" rx="8"
        fill="#0a0612" stroke="#2c1a4d" stroke-width="1.2"/>
  <line x1="30" y1="20"  x2="1170" y2="20"  stroke="url(#cBorder)" stroke-width="1"/>
  <line x1="30" y1="210" x2="1170" y2="210" stroke="url(#cBorder)" stroke-width="1"/>

  <!-- header HUD -->
  <text x="60" y="44" font-family="ui-monospace,monospace" font-size="11" letter-spacing="3" fill="#8a7a9d">
    03 · RECENT ACTIVITY ── quiet commits, one at a time
  </text>

  <!-- commit list -->
  {commit_lines_str}

  <!-- mini terminal command display -->
  <g transform="translate(1140, 44)">
    <text font-family="ui-monospace,monospace" font-size="10.5" fill="#6d5da8" letter-spacing="1" text-anchor="end">
      <tspan fill="#a78bfa">$</tspan> git log -n 5 --oneline
    </text>
  </g>
</svg>
"""
    with open("assets/commits.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    ist = timezone(timedelta(hours=5, minutes=30))
    with open("commits.txt", "w", encoding="utf-8") as f:
        f.write("Recent Commits\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
        f.write("=" * 80 + "\n\n")
        for i, c in enumerate(commits, 1):
            f.write(f"Commit {i}\n")
            f.write(f"  SHA:      {c['sha']}\n")
            f.write(f"  Repo:     {c['repo']}\n")
            f.write(f"  Message:  {c['message']}\n")
            f.write(f"  Time:     {c['time']}\n")
            f.write(f"  URL:      {c['url']}\n")
            f.write("\n")
    print(f"wrote assets/commits.svg and commits.txt -> {len(commits)} commits")

if __name__ == "__main__":
    main()
