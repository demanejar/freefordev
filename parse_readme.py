#!/usr/bin/env python3
import re
import json

def parse_readme(file_path):
    """Parse README.md and extract all categories and services"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    categories = []
    current_category = None
    
    # Split by lines
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if it's a category header (## Title)
        if line.startswith('## ') and not line.startswith('###'):
            category_title = line[3:].strip()
            
            # Skip table of contents
            if category_title.lower() == 'table of contents':
                i += 1
                continue
            
            # Create new category
            current_category = {
                'title': category_title,
                'id': category_title.lower().replace(' ', '-').replace("'", ''),
                'services': []
            }
            categories.append(current_category)
        
        # Check if it's a service item (starts with * [)
        elif line.startswith('* [') and current_category:
            # Extract service name and URL
            match = re.match(r'\* \[([^\]]+)\]\(([^)]+)\)', line)
            if match:
                service_name = match.group(1)
                service_url = match.group(2)
                
                # Get description (rest of the line after URL)
                desc_start = line.find(')') + 1
                description = line[desc_start:].strip()
                
                # Remove leading dash or em-dash
                description = re.sub(r'^[—\-–]\s*', '', description)
                
                # If description is empty, try to get it from next lines
                if not description and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('*') and not next_line.startswith('#'):
                        description = next_line
                
                current_category['services'].append({
                    'name': service_name,
                    'url': service_url,
                    'description': description[:200] if description else 'Free tier available'
                })
        
        i += 1
    
    # Filter out categories with no services
    categories = [cat for cat in categories if cat['services']]
    
    # Add icons and descriptions for categories
    category_metadata = {
        'major-cloud-providers': {'icon': '☁️', 'description': 'Free tiers from major cloud providers including AWS, Google Cloud, Azure, and Oracle Cloud.'},
        'cloud-management-solutions': {'icon': '🛠️', 'description': 'Infrastructure as code and cloud management platforms.'},
        'source-code-repos': {'icon': '📦', 'description': 'Git repositories and version control hosting services.'},
        'apis-data-and-ml': {'icon': '🔌', 'description': 'Free APIs for data processing, machine learning, web scraping, and various integrations.'},
        'artifact-repos': {'icon': '📚', 'description': 'Package and artifact repository hosting services.'},
        'tools-for-teams-and-collaboration': {'icon': '👥', 'description': 'Communication, project management, and team productivity tools.'},
        'cms': {'icon': '📝', 'description': 'Headless CMS and content management platforms.'},
        'code-generation': {'icon': '⚡', 'description': 'AI-powered code generation and completion tools.'},
        'code-quality': {'icon': '✅', 'description': 'Code review, static analysis, and quality assurance tools.'},
        'code-search-and-browsing': {'icon': '🔍', 'description': 'Code search engines and browsing tools.'},
        'ci-and-cd': {'icon': '🔄', 'description': 'Continuous Integration and Deployment services.'},
        'testing': {'icon': '🧪', 'description': 'Testing tools for web, mobile, API testing, and QA.'},
        'security-and-pki': {'icon': '🛡️', 'description': 'Security scanning, SSL certificates, and vulnerability detection.'},
        'authentication-authorization-and-user-management': {'icon': '🔐', 'description': 'User management, SSO, OAuth, and identity services.'},
        'mobile-app-distribution-and-feedback': {'icon': '📱', 'description': 'Mobile app testing and distribution platforms.'},
        'management-system': {'icon': '⚙️', 'description': 'Server and device management platforms.'},
        'messaging-and-streaming': {'icon': '💬', 'description': 'Real-time messaging, pub/sub, and event streaming.'},
        'log-management': {'icon': '📜', 'description': 'Log aggregation, analysis, and monitoring.'},
        'translation-management': {'icon': '🌍', 'description': 'Localization and translation management platforms.'},
        'monitoring': {'icon': '📊', 'description': 'Application performance monitoring and uptime tracking.'},
        'crash-and-exception-handling': {'icon': '🐛', 'description': 'Error tracking and crash reporting services.'},
        'search': {'icon': '🔎', 'description': 'Search engines and search-as-a-service platforms.'},
        'email': {'icon': '📧', 'description': 'Transactional email and email marketing services.'},
        'cdn-and-protection': {'icon': '🌐', 'description': 'Content delivery networks and DDoS protection.'},
        'paas': {'icon': '🚀', 'description': 'Platform as a Service for application hosting.'},
        'baas': {'icon': '⚡', 'description': 'Backend as a Service platforms.'},
        'web-hosting': {'icon': '🌐', 'description': 'Free web hosting for static and dynamic sites.'},
        'iaas': {'icon': '💻', 'description': 'Infrastructure as a Service providers.'},
        'managed-data-services': {'icon': '🗄️', 'description': 'Managed database and data storage services.'},
        'tunneling-webrtc-web-socket-servers-and-other-routers': {'icon': '🔌', 'description': 'Tunneling, WebRTC, and networking services.'},
        'issue-tracking-and-project-management': {'icon': '📋', 'description': 'Project management and issue tracking tools.'},
        'storage-and-media-processing': {'icon': '💾', 'description': 'File storage, CDN, and media processing.'},
        'design-and-ui': {'icon': '🎨', 'description': 'Design tools, UI kits, and graphics resources.'},
        'design-inspiration': {'icon': '💡', 'description': 'Design inspiration and resource galleries.'},
        'data-visualization-on-maps': {'icon': '🗺️', 'description': 'Mapping and geospatial visualization tools.'},
        'package-build-system': {'icon': '📦', 'description': 'Package building and distribution systems.'},
        'ide-and-code-editing': {'icon': '💻', 'description': 'Online IDEs and code editors.'},
        'analytics-events-and-statistics': {'icon': '📈', 'description': 'Web analytics and event tracking platforms.'},
        'visitor-session-recording': {'icon': '🎥', 'description': 'Session recording and user behavior analytics.'},
        'international-mobile-number-verification-api-and-sdk': {'icon': '📞', 'description': 'Phone number verification APIs.'},
        'payment-and-billing-integration': {'icon': '💳', 'description': 'Payment processing and billing platforms.'},
        'docker-related': {'icon': '🐳', 'description': 'Docker registry and container services.'},
        'vagrant-related': {'icon': '📦', 'description': 'Vagrant and VM management tools.'},
        'dev-blogging-sites': {'icon': '✍️', 'description': 'Platforms for developer blogging.'},
        'commenting-platforms': {'icon': '💬', 'description': 'Comment systems for websites.'},
        'screenshot-apis': {'icon': '📸', 'description': 'Screenshot and image capture APIs.'},
        'flutter-related-and-building-ios-apps-without-mac': {'icon': '📱', 'description': 'Flutter development and iOS building tools.'},
        'education-and-career-development': {'icon': '🎓', 'description': 'Free learning resources and courses.'},
        'privacy-management': {'icon': '🔒', 'description': 'Privacy compliance and management tools.'},
        'miscellaneous': {'icon': '🔧', 'description': 'Various other free developer tools.'},
        'domain': {'icon': '🌐', 'description': 'Free domain names and DNS services.'},
        'dns': {'icon': '🌐', 'description': 'DNS hosting and management services.'},
        'font': {'icon': '🔤', 'description': 'Free fonts and typography resources.'},
        'forms': {'icon': '📋', 'description': 'Form builders and survey tools.'},
        'low-code-platform': {'icon': '⚡', 'description': 'No-code and low-code development platforms.'},
        'generative-ai': {'icon': '🤖', 'description': 'AI and machine learning services.'},
        'feature-toggles-management-platforms': {'icon': '🎚️', 'description': 'Feature flag management services.'},
        'browser-based-hardware-emulation-written-in-javascript': {'icon': '🖥️', 'description': 'Browser-based emulators.'},
        'remote-desktop-tools': {'icon': '🖥️', 'description': 'Remote desktop and screen sharing.'},
        'game-development': {'icon': '🎮', 'description': 'Game development tools and engines.'},
        'other-free-resources': {'icon': '🎁', 'description': 'Additional free resources for developers.'}
    }
    
    # Add metadata to categories
    for category in categories:
        cat_id = category['id']
        if cat_id in category_metadata:
            category['icon'] = category_metadata[cat_id]['icon']
            category['description'] = category_metadata[cat_id]['description']
        else:
            category['icon'] = '📦'
            category['description'] = f'Free services and tools for {category["title"].lower()}.'
    
    return categories

if __name__ == '__main__':
    readme_path = '/home/trannguyenhan/data/projects/freefordev/free-for-dev/README.md'
    categories = parse_readme(readme_path)
    
    # Save to JSON
    output_path = '/home/trannguyenhan/data/projects/freefordev/data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    total_services = sum(len(cat['services']) for cat in categories)
    print(f'✅ Parsed {len(categories)} categories with {total_services} services')
    print(f'📝 Data saved to {output_path}')
