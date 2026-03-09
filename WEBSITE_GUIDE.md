# Shatarupa's Artree - Website Management Guide

## How to Update Your Artwork

### Adding New Artwork
1. **For Paintings**:
   - Save your new painting images to: `C:\Shatarupa\Art\Paintings\`
   - Supported formats: `.jpg`, `.jpeg`, `.png`
   - Naming: Use descriptive names with underscores (e.g., `sunset_landscape.jpg`)

2. **For Videos**:
   - Save your new videos to: `C:\Shatarupa\Art\Short Painting Videos\`
   - Supported formats: `.mp4` (recommended), `.webm`
   - Keep videos under 2 minutes for best performance

3. **For Sold Artwork**:
   - Move sold artwork to: `C:\Shatarupa\Art\Sold Out\`
   - They will automatically appear in the "Sold Out" section

### Updating the Website
1. After adding new files, simply double-click on `update_gallery.bat`
2. The script will automatically:
   - Scan your art folders
   - Update the gallery section
   - Preserve all your existing content
   - Show a success message when done

3. Refresh your website to see the changes

## Website Structure
```
website/
├── index.html          # Main website file
├── styles.css          # Website styling
├── update_gallery.py   # Script that updates the gallery
├── update_gallery.bat  # Easy one-click updater
└── WEBSITE_GUIDE.md    # This guide
```

## Hosting Your Website
1. **Free Options**:
   - GitHub Pages
   - Netlify
   - Vercel

2. **Paid Options**:
   - Hostinger
   - Bluehost
   - SiteGround

## Troubleshooting
- If the update fails:
  1. Check that Python is installed
  2. Make sure all files are in the correct folders
  3. Ensure no files are open in another program

## Need Help?
Contact your developer if you need assistance with:
- Adding new features
- Changing the website design
- Setting up a custom domain
- Any other technical questions

## Backup Your Website
Always keep a backup of your website folder before making major changes.

---
Last Updated: November 2024
