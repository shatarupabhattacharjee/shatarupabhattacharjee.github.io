import os
import json
from pathlib import Path

def get_artwork_files():
    """Get all artwork files from the specified directories"""
    art_folders = {
        'paintings': r"C:\Shatarupa\Art\Paintings",
        'videos': r"C:\Shatarupa\Art\Short Painting Videos",
        'sold': r"C:\Shatarupa\Art\Sold Out"
    }
    
    artwork_data = {}
    
    for category, folder_path in art_folders.items():
        artwork_data[category] = []
        folder = Path(folder_path)
        
        if not folder.exists():
            print(f"Warning: Directory not found - {folder_path}")
            continue
            
        for file in folder.iterdir():
            if file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.webm', '.mov'}:
                is_video = file.suffix.lower() in {'.mp4', '.webm', '.mov'}
                artwork_data[category].append({
                    'filename': file.name,
                    'path': str(file).replace('\\', '/'),
                    'is_video': is_video,
                    'category': category
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
                                <source src="{item['path'].replace('\\', '/')}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="gallery-overlay">
                            <h3>{item_name}</h3>
                            <p>Video</p>
                            <a href="#" class="btn-details view-fullscreen" data-src="{item['path'].replace('\\', '/')}" data-type="video">View Fullscreen</a>
                        </div>
                    </div>
                </div>
                '''
            else:
                html += f'''
                <div class="gallery-item" data-category="{category}">
                    <div class="gallery-image">
                        <img src="{item['path'].replace('\\', '/')}" alt="{item_name}">
                        <div class="gallery-overlay">
                            <h3>{item_name}</h3>
                            <p>Painting</p>
                            <a href="#" class="btn-details view-fullscreen" data-src="{item['path'].replace('\\', '/')}" data-type="image">View Fullscreen</a>
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
    # Get the artwork data
    artwork_data = get_artwork_files()
    
    # Read the current index.html
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Generate the new gallery HTML
    gallery_html = generate_gallery_html(artwork_data)
    
    # Find and replace the gallery section
    start_marker = '<!-- Gallery Section -->'
    end_marker = '<!-- /Gallery Section -->'
    
    if start_marker in content and end_marker in content:
        # If markers exist, replace the content between them
        start = content.find(start_marker)
        end = content.find(end_marker) + len(end_marker)
        new_content = content[:start] + gallery_html + '<!-- /Gallery Section -->' + content[end:]
    else:
        # If markers don't exist, find the gallery section by ID
        start = content.find('<section id="gallery"')
        if start == -1:
            print("Error: Could not find gallery section in index.html")
            return
            
        # Find the end of the gallery section
        section_depth = 1
        end = start + 1
        while end < len(content) and section_depth > 0:
            if content[end] == '<':
                if content.startswith('</section>', end):
                    section_depth -= 1
                    if section_depth == 0:
                        end += len('</section>')
                        break
                elif content.startswith('<section', end):
                    section_depth += 1
            end += 1
            
        new_content = content[:start] + gallery_html + content[end:]
    
    # Write the updated content back to index.html
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print("Gallery updated successfully!")

if __name__ == "__main__":
    update_website()
