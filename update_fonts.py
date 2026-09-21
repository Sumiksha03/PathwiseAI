import os
import re

def bump_font_size(match):
    size = float(match.group(1))
    # Bump by 15% and round to 2 decimals
    new_size = round(size * 1.15, 2)
    return f"font-size:{new_size}rem"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace specific hardcoded fonts with our tokens
    replacements = [
        (r"font-family:\s*['\"]Syne['\"],\s*sans-serif", "font-family:var(--font-serif)"),
        (r"font-family:\s*['\"]DM Sans['\"],\s*sans-serif", "font-family:var(--font)"),
        (r"font-family:\s*['\"]Georgia['\"],\s*serif", "font-family:var(--font-serif)"),
        (r"font-family:\s*['\"]Playfair Display['\"],\s*serif", "font-family:var(--font-serif)"),
        (r"font-family:\s*['\"]Inter['\"],\s*sans-serif", "font-family:var(--font)"),
        (r"font-family:\s*['\"]JetBrains Mono['\"],\s*monospace", "font-family:var(--font-mono)"),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)

    # We also want to match spacing variations: "font-size: 1.2rem", "font-size:1.2rem"
    content = re.sub(r"font-size:\s*([0-9.]+)rem", bump_font_size, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

# Update all pages
pages_dir = r"c:\Users\Sumiksha\OneDrive\Desktop\AI Rgh\pages"
for filename in os.listdir(pages_dir):
    if filename.endswith(".py"):
        process_file(os.path.join(pages_dir, filename))

# We already updated app.py, but just in case there are still hardcoded ones
process_file(r"c:\Users\Sumiksha\OneDrive\Desktop\AI Rgh\app.py")
