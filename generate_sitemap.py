#!/usr/bin/env python3
"""
Auto-generate sitemap.xml for Mountain West IRA markdown blog archive.
This script scans all .md files and creates a sitemap for AI crawlers.
"""

import os
from datetime import datetime
from pathlib import Path

# Configuration
BASE_URL = "https://mountainwestira.github.io/blog-markdown"
EXCLUDED_FILES = ["README.md", "LICENSE.md"]

def get_file_modified_date(filepath):
    """Get the last modified date of a file."""
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def generate_sitemap():
    """Generate sitemap.xml from all markdown files."""
    
    # Find all .md files
    md_files = []
    for path in Path('.').rglob('*.md'):
        if path.name not in EXCLUDED_FILES:
            md_files.append(path)
    
    # Sort files alphabetically
    md_files.sort()
    
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
    print(f"📍 Location: sitemap.xml")

if __name__ == "__main__":
    generate_sitemap()
