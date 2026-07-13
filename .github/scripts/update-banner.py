# update-banner.py — inject last-updated IST timestamp into assets/banner.svg
# runs in GitHub Actions every hour. no dependencies. python 3.

import datetime
import sys
import re

BANNER_PATH = "assets/banner.svg"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

def esc(s):
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))

def main():
    now = datetime.datetime.now(IST)
    timestamp = now.strftime("%d %b %Y · %H:%M IST")
    
    with open(BANNER_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = r'(MMXXVI · )\d{2} [A-Za-z]{3} \d{4} · \d{2}:\d{2} (UTC|IST)'
    replacement = r'\g<1>' + esc(timestamp)
    
    new_content, count = re.subn(pattern, replacement, content)
    
    if count == 0:
        print("Could not find timestamp placeholder in banner.svg", file=sys.stderr)
        return
    
    with open(BANNER_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated banner.svg with timestamp: {timestamp}")

if __name__ == "__main__":
    main()
