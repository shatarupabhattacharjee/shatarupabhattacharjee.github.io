import os
import json
import shutil
from pathlib import Path

# Configuration
WEBSITE_DIR = Path(__file__).parent
ARTWORK_DIR = WEBSITE_DIR / 'artwork'

def copy_artwork_to_website():
    """Copy artwork from source to website directory"""
    art_folders = {
        'paintings': r"C:\Shatarupa\Art\Paintings",
        'videos': r"C:\Shatarupa\Art\Short Painting Videos",
        'sold': r"C:\Shatarupa\Art\Sold Out"
    }
    
    # Create artwork directory if it doesn't exist
    ARTWORK_DIR.mkdir(exist_ok=True)
    
    # Clear existing artwork to avoid duplicates
    for item in ARTWORK_DIR.glob('*'):
        if item.is_file():
            item.unlink()
    
    # Copy files
    for category, src_folder in art_folders.items():
        src_path = Path(src_folder)
        if not src_path.exists():
            print(f"Warning: Source directory not found - {src_folder}")
            continue
            
        for ext in ('*.jpg', '*.jpeg', '*.png', '*.mp4', '*.webm'):
            for src_file in src_path.glob(ext):
                dest_file = ARTWORK_DIR / f"{category}_{src_file.name}"
                shutil.copy2(src_file, dest_file)

def get_artwork_files():
    """Get all artwork files from the website's artwork directory"""
    artwork_data = {}
    categories = ['paintings', 'videos', 'sold']
    
    for category in categories:
        artwork_data[category] = []
        for ext in ('.jpg', '.jpeg', '.png', '.mp4', '.webm'):
            for file_path in ARTWORK_DIR.glob(f"{category}_*{ext}"):
                is_video = file_path.suffix.lower() in ['.mp4', '.webm']
                artwork_data[category].append({
                    'path': f"artwork/{file_path.name}",
                    'filename': file_path.name.replace(f"{category}_", "", 1),
                    'is_video': is_video
                })
    
    return artwork_data

def generate_gallery_html(artwork_data):
    """Generate HTML for the gallery section"""
    html = '''
    <!-- Gallery Section -->
    <section id="gallery" class="gallery">
        <div class="container">
            <h2 class="section-title">My Painting Gallery</h2>
            <p class="section-subtitle">Explore my collection of handmade paintings</p>
            
            <div class="gallery-filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="paintings">Paintings</button>
                <button class="filter-btn" data-filter="videos">Painting Videos</button>
                <button class="filter-btn" data-filter="sold">Sold Out</button>
            </div>

            <div class="gallery-grid">
    '''
    
    # Add paintings
    for category, items in artwork_data.items():
        for item in items:
            item_name = ' '.join(word.capitalize() for word in item['filename'].split('.')[0].replace('_', ' ').split())
            
            if item['is_video']:
                html += f'''
                <div class="gallery-item" data-category="{category}">
                    <div class="gallery-image">
                        <div class="video-container">
                            <video class="art-video" controls>
                                <source src="{item['path']}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="gallery-overlay">
                            <h3>{item_name}</h3>
                            <p>Video</p>
                            <a href="#" class="btn-details view-fullscreen" data-src="{item['path']}" data-type="video">View Fullscreen</a>
                        </div>
                    </div>
                </div>
                '''
            else:
                html += f'''
                <div class="gallery-item" data-category="{category}">
                    <div class="gallery-image">
                        <img src="{item['path']}" alt="{item_name}">
                        <div class="gallery-overlay">
                            <h3>{item_name}</h3>
                            <p>Painting</p>
                            <a href="#" class="btn-details view-fullscreen" data-src="{item['path']}" data-type="image">View Fullscreen</a>
                        </div>
                    </div>
                </div>
                '''
    
    # Add lightbox HTML
    html += '''
            </div>
        </div>
        
        <!-- Lightbox -->
        <div id="lightbox" class="lightbox">
            <span class="close-lightbox">&times;</span>
            <div class="lightbox-content">
                <!-- Content will be inserted here by JavaScript -->
            </div>
        </div>
    </section>
    
    <!-- Add JavaScript for lightbox and filtering -->
    <script>
    // Gallery filtering
    document.addEventListener('DOMContentLoaded', function() {
        // Filter functionality
        const filterBtns = document.querySelectorAll('.filter-btn');
        const galleryItems = document.querySelectorAll('.gallery-item');
        
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all buttons
                filterBtns.forEach(b => b.classList.remove('active'));
                // Add active class to clicked button
                btn.classList.add('active');
                
                const filter = btn.getAttribute('data-filter');
                
                galleryItems.forEach(item => {
                    if (filter === 'all' || item.getAttribute('data-category') === filter) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
        
        // Lightbox functionality
        const lightbox = document.getElementById('lightbox');
        const lightboxContent = document.querySelector('.lightbox-content');
        const closeLightbox = document.querySelector('.close-lightbox');
        
        document.querySelectorAll('.view-fullscreen').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const src = this.getAttribute('data-src');
                const type = this.getAttribute('data-type');
                
                if (type === 'video') {
                    lightboxContent.innerHTML = `
                        <video controls autoplay style="width: 100%; max-height: 80vh;">
                            <source src="${src}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                    `;
                } else {
                    lightboxContent.innerHTML = `<img src="${src}" style="max-width: 100%; max-height: 80vh; display: block; margin: 0 auto;">`;
                }
                
                lightbox.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        });
        
        // Close lightbox
        closeLightbox.addEventListener('click', () => {
            lightbox.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
        
        // Close when clicking outside the content
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                lightbox.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
        
        // Close with ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.style.display === 'flex') {
                lightbox.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    });
    </script>
    '''
    return html

def update_website():
    """Update the website with the latest gallery content"""
    # First, copy all artwork to the website directory
    print("Copying artwork files...")
    copy_artwork_to_website()
    
    # Get artwork data
    print("Scanning artwork...")
    artwork_data = get_artwork_files()
    
    # Generate gallery HTML
    print("Generating gallery HTML...")
    gallery_html = generate_gallery_html(artwork_data)
    
    # Read the current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the gallery section
    start_marker = '<!-- GALLERY_SECTION_START -->'
    end_marker = '<!-- GALLERY_SECTION_END -->'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find gallery section markers in index.html")
        return
    
    # Update the content
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
