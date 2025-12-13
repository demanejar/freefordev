# Free for Developers - Website

A beautiful, modern website showcasing **1,603 free services** across **61 categories** for developers.

## ✨ Features

### 🎨 Modern Design
- **Dark theme** with gradient effects and glassmorphism
- **Smooth animations** and micro-interactions
- **Responsive design** for all devices
- **Custom scrollbars** and hover effects

### 🔍 Search & Filter
- **Real-time search** across all services and categories
- **Category filters** for quick navigation
- **Keyboard shortcuts** (Ctrl/Cmd + K to search, Esc to clear)

### 📱 Modal Service Viewer
- Click "View all X services" to open a beautiful modal
- **Grid layout** for easy browsing
- **Search within modal** to find specific services
- **Backdrop blur** effect
- Click outside or press Esc to close

### 📊 Statistics
- Live count of total services and categories
- Service count per category
- Auto-updated when filtering

## 🚀 Quick Start

### Option 1: Python Server (Recommended)
```bash
cd /home/trannguyenhan/data/projects/freefordev
python3 -m http.server 8000
```

Then open: http://localhost:8000

### Option 2: PHP Server
```bash
cd /home/trannguyenhan/data/projects/freefordev
php -S localhost:8000
```

### Option 3: Node.js Server
```bash
cd /home/trannguyenhan/data/projects/freefordev
npx serve
```

## 📁 Project Structure

```
freefordev/
├── index.html          # Main HTML file
├── styles.css          # All CSS styles
├── script.js           # JavaScript functionality
├── data.json           # Parsed services data (1,603 services)
├── parse_readme.py     # Python script to parse README.md
└── free-for-dev/
    └── README.md       # Original data source
```

## 🔄 Update Data

To refresh the services data from the latest README.md:

```bash
python3 parse_readme.py
```

This will:
- Parse `free-for-dev/README.md`
- Extract all categories and services
- Generate `data.json` with structured data
- Show statistics (categories and services count)

## 🎯 Key Technologies

- **Pure HTML/CSS/JavaScript** - No frameworks needed
- **CSS Grid & Flexbox** - Modern responsive layouts
- **Fetch API** - Load data dynamically
- **Intersection Observer** - Scroll animations
- **CSS Custom Properties** - Easy theming

## 🎨 Design Highlights

### Color Palette
- Primary Gradient: `#667eea → #764ba2`
- Background: `#0a0e27` (Dark blue)
- Cards: `rgba(30, 33, 57, 0.6)` (Glassmorphism)

### Typography
- Primary Font: Inter
- Monospace: JetBrains Mono

### Animations
- Fade in up on scroll
- Hover lift effects
- Modal scale & fade transitions
- Smooth color transitions

## 📱 Responsive Breakpoints

- Desktop: > 1024px
- Tablet: 768px - 1024px
- Mobile: < 768px
- Small Mobile: < 480px

## ⌨️ Keyboard Shortcuts

- `Ctrl/Cmd + K` - Focus search
- `Esc` - Clear search or close modal
- `Tab` - Navigate through elements

## 🌟 Categories

The website includes 61 categories:
- Major Cloud Providers
- APIs, Data & ML
- CI/CD
- Testing
- Monitoring
- Databases
- Web Hosting
- Email Services
- Authentication & Authorization
- And 52 more...

## 📊 Statistics

- **1,603 Services** across all categories
- **61 Categories** covering all developer needs
- **100% Free** tiers available
- **Regular updates** from community

## 🤝 Contributing

This website is built from the [free-for-dev](https://github.com/ripienaar/free-for-dev) repository.

To contribute:
1. Add services to `free-for-dev/README.md`
2. Run `python3 parse_readme.py`
3. Test the website
4. Submit changes

## 📝 License

This project follows the same license as the original free-for-dev repository.

## 🙏 Credits

- Data source: [free-for-dev](https://github.com/ripienaar/free-for-dev)
- Built with ❤️ by the developer community
- 1600+ contributors to the original repository

---

**Enjoy discovering free services for developers! 🚀**
