import os
from pathlib import Path

def update_website():
    print("Updating gallery with existing artwork...")
    artwork_dir = Path("artwork")
    if not artwork_dir.exists():
        print("Error: 'artwork' folder not found. Please create it and add your artwork files.")
        return
    
    # Continue with the rest of the update process
    from update_gallery import get_artwork_files, generate_gallery_html
    
    print("Scanning artwork...")
    artwork_data = get_artwork_files()
    
    print("Generating gallery HTML...")
    gallery_html = generate_gallery_html(artwork_data)
    
    # Read the current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the content
    start_marker = '<!-- GALLERY_SECTION_START -->'
    end_marker = '<!-- GALLERY_SECTION_END -->'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find gallery section markers in index.html")
        return
    
    new_content = (
        content[:start_idx + len(start_marker)] + 
        '\n' + gallery_html + '\n' +
        content[end_idx:]
    )
    
    # Write the updated content back to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Gallery updated successfully!")
    print("\nNext steps:")
    print("1. Commit and push your changes to GitHub")
    print("2. Your changes will be live at: https://shatarupabhattacharjee.github.io")

if __name__ == "__main__":
    update_website()