import json
import re
from pathlib import Path
from typing import Dict, List, Any

class MobileUxEnhancer:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agent_id = self.config.get("agent_id", "mobile_ux_enhancer")

    async def run(self, input_path: str, pipeline_id: str):
        """
        Enhance WordPress theme with mobile-first UX improvements
        """
        try:
            theme_dir = Path(input_path)
            if not theme_dir.exists():
                raise FileNotFoundError(f"Theme directory not found: {input_path}")
            
            print(f"🎨 Enhancing mobile UX for theme in {theme_dir}")
            
            # Create enhanced theme directory
            enhanced_dir = theme_dir.parent / f"mobile_enhanced_theme_{pipeline_id}"
            enhanced_dir.mkdir(exist_ok=True)
            
            # Copy all files from input theme
            self.copy_theme_files(theme_dir, enhanced_dir)
            
            # Apply mobile UX enhancements
            self.enhance_style_css(enhanced_dir)
            self.enhance_template_files(enhanced_dir)
            self.add_mobile_javascript(enhanced_dir)
            self.optimize_for_mobile(enhanced_dir)
            
            print(f"✅ Mobile UX enhanced theme generated in {enhanced_dir}")

            # Return result in the format expected by orchestrator
            return type('Result', (), {
                'success': True,
                'output_file': str(enhanced_dir),
                'message': "Mobile UX enhancements applied successfully"
            })()

        except Exception as e:
            print(f"❌ Mobile UX enhancement failed: {str(e)}")
            return type('Result', (), {
                'success': False,
                'error_message': str(e),
                'message': f"Mobile UX enhancement failed: {str(e)}"
            })()
    
    def copy_theme_files(self, source_dir: Path, target_dir: Path):
        """Copy all theme files to the enhanced directory"""
        import shutil
        
        for item in source_dir.rglob('*'):
            if item.is_file():
                relative_path = item.relative_to(source_dir)
                target_path = target_dir / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
    
    def enhance_style_css(self, theme_dir: Path):
        """Apply mobile-first CSS enhancements"""
        style_file = theme_dir / "style.css"
        if not style_file.exists():
            return
        
        current_css = style_file.read_text(encoding='utf-8')
        
        # Add mobile UX enhancements
        mobile_enhancements = self.generate_mobile_ux_css()
        
        # Insert enhancements before the last closing brace or at the end
        enhanced_css = current_css + "\n\n" + mobile_enhancements
        
        style_file.write_text(enhanced_css, encoding='utf-8')
        print("🎨 Applied mobile UX CSS enhancements")
    
    def generate_mobile_ux_css(self) -> str:
        """Generate comprehensive mobile UX CSS enhancements"""
        return """
/* ========================================
   MOBILE UX ENHANCEMENTS
   ======================================== */

/* CSS Custom Properties for Mobile UX */
:root {
    --mobile-spacing-xs: 0.5rem;
    --mobile-spacing-sm: 1rem;
    --mobile-spacing-md: 1.5rem;
    --mobile-spacing-lg: 2rem;
    --mobile-spacing-xl: 3rem;
    
    --shadow-subtle: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-medium: 0 4px 12px rgba(0,0,0,0.15);
    --shadow-strong: 0 8px 24px rgba(0,0,0,0.2);
    
    --border-radius-sm: 8px;
    --border-radius-md: 12px;
    --border-radius-lg: 16px;
    
    --transition-fast: 0.2s ease;
    --transition-medium: 0.3s ease;
    --transition-slow: 0.5s ease;
}

/* Mobile-First Base Improvements */
body {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

/* Enhanced Visual Hierarchy */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, var(--background-color) 0%, rgba(var(--primary-rgb), 0.1) 100%);
    padding: var(--mobile-spacing-xl) var(--mobile-spacing-md);
    min-height: 70vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 80%, rgba(var(--primary-rgb), 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(var(--secondary-rgb), 0.1) 0%, transparent 50%);
    z-index: 1;
}

.hero .container {
    position: relative;
    z-index: 2;
}

.hero h1 {
    font-size: clamp(2rem, 8vw, 3.5rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: var(--mobile-spacing-md);
    background: linear-gradient(135deg, var(--text-color) 0%, var(--primary-color) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero p {
    font-size: clamp(1.125rem, 4vw, 1.25rem);
    line-height: 1.6;
    margin-bottom: var(--mobile-spacing-lg);
    opacity: 0.9;
}

/* Enhanced Service Cards with Depth */
.services-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--mobile-spacing-md);
    padding: var(--mobile-spacing-lg) var(--mobile-spacing-md);
}

.service-card {
    background: white;
    border-radius: var(--border-radius-md);
    padding: var(--mobile-spacing-lg);
    box-shadow: var(--shadow-subtle);
    border: 1px solid rgba(var(--primary-rgb), 0.1);
    transition: all var(--transition-medium);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.service-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    transform: scaleX(0);
    transition: transform var(--transition-medium);
}

.service-card:hover,
.service-card:focus {
    transform: translateY(-4px);
    box-shadow: var(--shadow-strong);
    border-color: var(--primary-color);
}

.service-card:hover::before,
.service-card:focus::before {
    transform: scaleX(1);
}

.service-card h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: var(--mobile-spacing-sm);
    color: var(--text-color);
}

.service-card p {
    color: rgba(var(--text-rgb), 0.8);
    line-height: 1.6;
    margin-bottom: var(--mobile-spacing-md);
}

/* Enhanced Buttons with Touch Optimization */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 44px;
    min-width: 44px;
    padding: var(--mobile-spacing-sm) var(--mobile-spacing-lg);
    border-radius: var(--border-radius-sm);
    font-weight: 600;
    font-size: 1rem;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: all var(--transition-fast);
    position: relative;
    overflow: hidden;
}

.btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left var(--transition-medium);
}

.btn:hover::before,
.btn:focus::before {
    left: 100%;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: white;
    box-shadow: var(--shadow-medium);
}

.btn-primary:hover,
.btn-primary:focus {
    transform: translateY(-2px);
    box-shadow: var(--shadow-strong);
}

.btn-primary:active {
    transform: translateY(0);
    box-shadow: var(--shadow-subtle);
}

/* Mobile Navigation Enhancements */
.mobile-menu-toggle {
    display: block;
    background: none;
    border: none;
    padding: var(--mobile-spacing-sm);
    cursor: pointer;
    border-radius: var(--border-radius-sm);
    transition: background-color var(--transition-fast);
}

.mobile-menu-toggle:hover,
.mobile-menu-toggle:focus {
    background-color: rgba(var(--primary-rgb), 0.1);
}

/* Floating Contact Button */
.floating-contact {
    position: fixed;
    bottom: var(--mobile-spacing-md);
    right: var(--mobile-spacing-md);
    z-index: 1000;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-strong);
    text-decoration: none;
    transition: all var(--transition-medium);
}

.floating-contact:hover,
.floating-contact:focus {
    transform: scale(1.1);
    box-shadow: 0 12px 32px rgba(var(--primary-rgb), 0.4);
}

/* Responsive Improvements */
@media (min-width: 768px) {
    .services-grid {
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: var(--mobile-spacing-lg);
    }
    
    .hero {
        padding: var(--mobile-spacing-xl) var(--mobile-spacing-lg);
    }
}

/* Animation Classes */
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: all var(--transition-slow);
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}

.slide-up {
    transform: translateY(40px);
    opacity: 0;
    transition: all var(--transition-medium);
}

.slide-up.visible {
    transform: translateY(0);
    opacity: 1;
}

/* Loading States */
.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
"""

    def enhance_template_files(self, theme_dir: Path):
        """Enhance template files with mobile UX improvements"""
        # Enhance front-page.php
        front_page = theme_dir / "front-page.php"
        if front_page.exists():
            self.enhance_front_page(front_page)

        # Enhance header.php
        header_file = theme_dir / "header.php"
        if header_file.exists():
            self.enhance_header(header_file)

        # Enhance footer.php
        footer_file = theme_dir / "footer.php"
        if footer_file.exists():
            self.enhance_footer(footer_file)

    def enhance_front_page(self, front_page_file: Path):
        """Enhance front page with mobile UX improvements"""
        content = front_page_file.read_text(encoding='utf-8')

        # Add mobile-optimized service cards structure
        if 'services-grid' in content:
            # Enhance existing services grid - capture the entire PHP block from services-grid to endforeach
            enhanced_content = re.sub(
                r'<div class="services-grid">\s*<\?php.*?endforeach; \?>\s*</div>',
                self.generate_enhanced_services_section(),
                content,
                flags=re.DOTALL
            )
            front_page_file.write_text(enhanced_content, encoding='utf-8')
            print("🎨 Enhanced front page with mobile UX improvements")

    def generate_enhanced_services_section(self) -> str:
        """Generate mobile-optimized services section"""
        return '''<div class="services-grid">
                <?php
                $services = get_option('business_services', array());
                if (empty($services)) {
                    // Generate dynamic services based on business context
                    $business_type = get_option('business_type', 'Service Business');

                    if (stripos($business_type, 'landscaping') !== false) {
                        $services = array(
                            'Landscape Design' => 'Transform your outdoor space with custom landscape design that reflects your style and enhances your property value.',
                            'Lawn Maintenance' => 'Keep your lawn healthy and beautiful year-round with our comprehensive maintenance services.',
                            'Garden Installation' => 'Professional garden installation with carefully selected plants that thrive in your local climate.'
                        );
                    } else {
                        $services = array(
                            'Professional Service 1' => 'High-quality service delivered with expertise and attention to detail.',
                            'Professional Service 2' => 'Reliable solutions tailored to meet your specific needs and requirements.',
                            'Professional Service 3' => 'Expert consultation and implementation for optimal results.'
                        );
                    }
                }

                foreach ($services as $service_name => $service_description): ?>
                    <div class="service-card fade-in" onclick="location.href='<?php echo home_url('/services/'); ?>'" role="button" tabindex="0"
                         onkeypress="if(event.key==='Enter') location.href='<?php echo home_url('/services/'); ?>'">
                        <div class="service-icon">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="12" cy="12" r="10" stroke="var(--primary-color)" stroke-width="2"/>
                                <path d="M8 12l2 2 4-4" stroke="var(--primary-color)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <h3><?php echo esc_html($service_name); ?></h3>
                        <p><?php echo esc_html($service_description); ?></p>
                        <div class="service-cta">
                            <span class="learn-more">Learn More →</span>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>'''

    def enhance_header(self, header_file: Path):
        """Enhance header with mobile navigation"""
        content = header_file.read_text(encoding='utf-8')

        # Add mobile menu toggle if not present
        if 'mobile-menu-toggle' not in content:
            # Insert mobile menu toggle before closing header tag
            mobile_nav = '''
    <!-- Mobile Navigation Enhancement -->
    <button class="mobile-menu-toggle" aria-label="Toggle mobile menu" onclick="toggleMobileMenu()">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
    </button>
</header>'''

            enhanced_content = content.replace('</header>', mobile_nav)
            header_file.write_text(enhanced_content, encoding='utf-8')
            print("🎨 Enhanced header with mobile navigation")

    def enhance_footer(self, footer_file: Path):
        """Enhance footer with floating contact button"""
        content = footer_file.read_text(encoding='utf-8')

        # Add floating contact button before closing body tag
        if 'floating-contact' not in content:
            floating_contact = '''
    <!-- Floating Contact Button -->
    <a href="tel:<?php echo get_option('business_phone', '#'); ?>" class="floating-contact" aria-label="Call us">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" fill="currentColor"/>
        </svg>
    </a>

<?php wp_footer(); ?>
</body>
</html>'''

            enhanced_content = content.replace('<?php wp_footer(); ?>\n</body>\n</html>', floating_contact)
            footer_file.write_text(enhanced_content, encoding='utf-8')
            print("🎨 Enhanced footer with floating contact button")

    def add_mobile_javascript(self, theme_dir: Path):
        """Add mobile-specific JavaScript enhancements"""
        js_dir = theme_dir / "js"
        js_dir.mkdir(exist_ok=True)

        mobile_js = js_dir / "mobile-ux.js"
        mobile_js.write_text(self.generate_mobile_javascript(), encoding='utf-8')
        print("🎨 Added mobile UX JavaScript")

    def generate_mobile_javascript(self) -> str:
        """Generate mobile UX JavaScript"""
        return '''/**
 * Mobile UX Enhancement JavaScript
 */

// Intersection Observer for animations
const observeElements = () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe fade-in elements
    document.querySelectorAll('.fade-in, .slide-up').forEach(el => {
        observer.observe(el);
    });
};

// Mobile menu toggle
const toggleMobileMenu = () => {
    const menu = document.querySelector('.mobile-menu');
    const toggle = document.querySelector('.mobile-menu-toggle');

    if (menu) {
        menu.classList.toggle('active');
        toggle.setAttribute('aria-expanded', menu.classList.contains('active'));
    }
};

// Touch feedback for service cards
const addTouchFeedback = () => {
    document.querySelectorAll('.service-card').forEach(card => {
        card.addEventListener('touchstart', () => {
            card.style.transform = 'scale(0.98)';
        });

        card.addEventListener('touchend', () => {
            card.style.transform = '';
        });
    });
};

// Smooth scrolling for anchor links
const enableSmoothScrolling = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    observeElements();
    addTouchFeedback();
    enableSmoothScrolling();
});

// Initialize on window load for better performance
window.addEventListener('load', () => {
    // Add loaded class for any load-dependent animations
    document.body.classList.add('loaded');
});'''

    def optimize_for_mobile(self, theme_dir: Path):
        """Apply mobile performance optimizations"""
        # Update functions.php to enqueue mobile JS
        functions_file = theme_dir / "functions.php"
        if functions_file.exists():
            content = functions_file.read_text(encoding='utf-8')

            # Add mobile JS enqueue if not present
            if 'mobile-ux.js' not in content:
                mobile_enqueue = '''
// Enqueue mobile UX JavaScript
wp_enqueue_script('mobile-ux', get_template_directory_uri() . '/js/mobile-ux.js', array(), '1.0', true);
'''
                # Insert before the closing PHP tag or at the end
                if '?>' in content:
                    enhanced_content = content.replace('?>', mobile_enqueue + '\n?>')
                else:
                    enhanced_content = content + '\n' + mobile_enqueue

                functions_file.write_text(enhanced_content, encoding='utf-8')
                print("🎨 Added mobile JavaScript enqueue to functions.php")
