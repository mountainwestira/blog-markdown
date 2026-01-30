#!/usr/bin/env python3
"""
Auto-generate sitemap.xml and update README.md for Mountain West IRA markdown blog archive.
This script scans all .md files, creates a sitemap, and updates the README with the blog list.
"""

import os
import re
from datetime import datetime
from pathlib import Path

# Configuration
BASE_URL = "https://mountainwestira.github.io/blog-markdown"
EXCLUDED_FILES = ["README.md", "LICENSE.md"]

def get_file_modified_date(filepath):
    """Get the last modified date of a file."""
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def extract_title_from_markdown(filepath):
    """Extract the title from the first H1 heading in markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Look for markdown H1 heading
                match = re.match(r'^#\s+(.+)$', line.strip())
                if match:
                    return match.group(1)
    except:
        pass
    
    # Fallback to filename if no H1 found
    return filepath.stem.replace('-', ' ').title()

def extract_date_from_markdown(filepath):
    """Extract the published date from markdown metadata."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(500)  # Only read first 500 chars
            # Look for **Published:** pattern
            match = re.search(r'\*\*Published:\*\*\s+(.+)', content)
            if match:
                return match.group(1).strip()
    except:
        pass
    
    # Fallback to file modification date
    return get_file_modified_date(filepath)

def generate_sitemap(md_files):
    """Generate sitemap.xml from all markdown files."""
    
    # Start building sitemap
    sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Add main index page
    sitemap_content.append('  <!-- Main Index Page -->')
    sitemap_content.append('  <url>')
    sitemap_content.append(f'    <loc>{BASE_URL}/</loc>')
    sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap_content.append('    <changefreq>weekly</changefreq>')
    sitemap_content.append('    <priority>1.0</priority>')
    sitemap_content.append('  </url>')
    sitemap_content.append('')
    
    # Add all markdown blog posts
    sitemap_content.append('  <!-- Blog Posts in Markdown Format -->')
    for md_file in md_files:
        # Convert file path to URL path
        url_path = str(md_file).replace('\\', '/')
        last_mod = get_file_modified_date(md_file)
        
        sitemap_content.append('  <url>')
        sitemap_content.append(f'    <loc>{BASE_URL}/{url_path}</loc>')
        sitemap_content.append(f'    <lastmod>{last_mod}</lastmod>')
        sitemap_content.append('    <changefreq>monthly</changefreq>')
        sitemap_content.append('    <priority>0.8</priority>')
        sitemap_content.append('  </url>')
    
    sitemap_content.append('</urlset>')
    
    # Write sitemap to file
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap_content))
    
    print(f"✅ Sitemap generated successfully with {len(md_files)} blog posts!")

def update_readme(md_files):
    """Update README.md with list of all blog posts."""
    
    # Create blog post entries
    blog_entries = []
    for md_file in md_files:
        title = extract_title_from_markdown(md_file)
        date = extract_date_from_markdown(md_file)
        url = f"{BASE_URL}/{str(md_file).replace(os.sep, '/')}"
        
        blog_entries.append(f"- [{title}]({url}) - {date}")
    
    # Build README content
    readme_content = [
        "# Mountain West IRA Blog - Markdown Archive",
        "",
        "AI-friendly markdown versions of our blog posts for enhanced discoverability.",
        "",
        "## Available Posts",
        ""
    ]
    
    # Add all blog post links
    readme_content.extend(blog_entries)
    
    # Add footer
    readme_content.extend([
        "",
        "---",
        "",
        "**About Mountain West IRA**",
        "",
        "We specialize in Self-Directed IRAs that give you the power to invest beyond the stock market, into real estate, private loans, precious metals, cryptocurrency and more.",
        "",
        "📞 Call us at **866-377-3311**  ",
        "📅 Schedule a [free consultation](https://outlook.office365.com/owa/calendar/MountainWestIRA@mwira.com/bookings/)  ",
        "🌐 Visit our website: [mountainwestira.com](https://www.mountainwestira.com)",
        "",
        "*This archive is maintained for AI search engines and research tools. For the full blog experience with images and formatting, visit [mountainwestira.com/blog](https://www.mountainwestira.com/blog)*"
    ])
    
    # Write README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_content))
    
    print(f"✅ README.md updated with {len(md_files)} blog posts!")

def main():
    """Main function to generate sitemap and update README."""
    
    # Find all .md files (excluding README and LICENSE)
    md_files = []
    for path in Path('.').rglob('*.md'):
        if path.name not in EXCLUDED_FILES:
            md_files.append(path)
    
    # Sort files by modification date (newest first)
    md_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    print(f"📂 Found {len(md_files)} blog post(s)")
    
    # Generate sitemap
    generate_sitemap(md_files)
    
    # Update README
    update_readme(md_files)
    
    print("🎉 All done! Sitemap and README updated successfully!")

if __name__ == "__main__":
    main()
