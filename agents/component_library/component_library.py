import json
import shutil
from pathlib import Path
from typing import Dict, Any
import sys
import os

# Add the project root to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.agent_result import AgentResult


class ComponentLibrary:
    def __init__(self, config=None):
        if config is None:
            config_path = Path(__file__).parent / "component_library.json"
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = config
    
    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        """
        Enhance theme with modular UI components
        """
        try:
            input_path = Path(input_file)
            template_id = self.extract_template_id(input_path.name)

            # Safety check: Don't process if input contains component_enhanced_theme directories
            if input_path.is_dir() and any(p.name.startswith('component_enhanced_theme_') for p in input_path.iterdir() if p.is_dir()):
                print(f"⚠️ Skipping component library processing - input contains recursive component directories")
                return AgentResult(
                    agent_id="component_library",
                    success=True,
                    output_file=str(input_path),
                    metadata={"template_id": template_id, "skipped": True, "reason": "recursive_prevention"}
                )

            # Create component enhanced theme directory in template_generations
            component_theme_dir = Path(f"template_generations/component_enhanced_theme_{template_id}")
            
            # Copy SEO enhanced theme to component enhanced directory
            # Only copy if the target doesn't already exist to prevent recursive copying
            if not component_theme_dir.exists():
                if input_path.is_dir():
                    shutil.copytree(input_path, component_theme_dir, dirs_exist_ok=False)
                else:
                    shutil.copytree(input_path.parent, component_theme_dir, dirs_exist_ok=False)
            else:
                print(f"⚠️ Component enhanced theme directory already exists: {component_theme_dir}")
                print(f"✅ Using existing directory to prevent recursive copying")
            
            # Create components directory
            components_dir = component_theme_dir / "components"
            components_dir.mkdir(exist_ok=True)
            
            # Create assets directories
            (component_theme_dir / "js").mkdir(exist_ok=True)
            (component_theme_dir / "css").mkdir(exist_ok=True)
            
            # Generate components
            self.create_testimonial_slider(components_dir)
            self.create_sticky_navigation(components_dir)
            self.create_contact_form(components_dir)
            self.create_service_cards(components_dir)
            
            # Generate JavaScript and CSS
            self.create_components_js(component_theme_dir / "js")
            self.create_components_css(component_theme_dir / "css")
            
            # Enhance existing theme files
            self.enhance_functions_php(component_theme_dir)
            self.enhance_header_php(component_theme_dir)
            self.enhance_services_page(component_theme_dir)
            self.enhance_index_php(component_theme_dir)
            
            print(f"✅ Component enhanced theme generated in {component_theme_dir}")
            
            return AgentResult(
                agent_id="component_library",
                success=True,
                output_file=str(component_theme_dir),
                metadata={"template_id": template_id, "components": 4}
            )
            
        except Exception as e:
            return AgentResult(
                agent_id="component_library",
                success=False,
                error_message=str(e)
            )
    
    def extract_template_id(self, filename: str) -> str:
        """Extract template ID from filename or directory name"""
        import re
        match = re.search(r"(?:template_|seo_enhanced_theme_)([a-zA-Z0-9_]+)", filename)
        return match.group(1) if match else "000"
    
    def create_testimonial_slider(self, components_dir: Path):
        """Create testimonial slider component"""
        testimonial_content = '''<?php
/**
 * Testimonial Slider Component
 */
?>
<div class="testimonial-slider" id="testimonial-slider">
    <div class="testimonial-container">
        <div class="testimonial-slide active">
            <div class="testimonial-content">
                <blockquote>
                    "<?php echo get_option('business_name', 'This business'); ?> saved my business! Fast, reliable service and great communication throughout the process."
                </blockquote>
                <cite>
                    <strong>Sarah Johnson</strong>
                    <span>Small Business Owner</span>
                </cite>
            </div>
        </div>
        
        <div class="testimonial-slide">
            <div class="testimonial-content">
                <blockquote>
                    "Professional service at a fair price. They fixed my computer quickly and explained everything clearly."
                </blockquote>
                <cite>
                    <strong>Mike Thompson</strong>
                    <span><?php echo get_option('business_location', 'Local Area'); ?> Resident</span>
                </cite>
            </div>
        </div>
        
        <div class="testimonial-slide">
            <div class="testimonial-content">
                <blockquote>
                    "Excellent virus removal service. My computer runs like new again. Highly recommended!"
                </blockquote>
                <cite>
                    <strong>Lisa Chen</strong>
                    <span>Home User</span>
                </cite>
            </div>
        </div>
    </div>
    
    <div class="testimonial-navigation">
        <button class="testimonial-prev" aria-label="Previous testimonial">&larr;</button>
        <div class="testimonial-dots">
            <button class="dot active" data-slide="0" aria-label="Testimonial 1"></button>
            <button class="dot" data-slide="1" aria-label="Testimonial 2"></button>
            <button class="dot" data-slide="2" aria-label="Testimonial 3"></button>
        </div>
        <button class="testimonial-next" aria-label="Next testimonial">&rarr;</button>
    </div>
</div>
'''
        
        testimonial_file = components_dir / "testimonials.php"
        testimonial_file.write_text(testimonial_content, encoding='utf-8')
    
    def create_sticky_navigation(self, components_dir: Path):
        """Create sticky navigation component"""
        sticky_nav_content = '''<?php
/**
 * Sticky Navigation Component
 */
?>
<nav class="sticky-nav" id="sticky-nav">
    <div class="sticky-nav-container">
        <div class="sticky-nav-brand">
            <a href="<?php echo home_url('/'); ?>">
                <?php bloginfo('name'); ?>
            </a>
        </div>
        
        <button class="mobile-menu-toggle" id="mobile-menu-toggle" aria-label="Toggle mobile menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
        
        <div class="sticky-nav-menu" id="sticky-nav-menu">
            <a href="#home" class="nav-link">Home</a>
            <a href="#services" class="nav-link">Services</a>
            <a href="#about" class="nav-link">About</a>
            <a href="#testimonials" class="nav-link">Reviews</a>
            <a href="#contact" class="nav-link">Contact</a>
            <?php $phone = get_option('business_phone'); if ($phone): ?>
                <a href="tel:<?php echo esc_attr($phone); ?>" class="nav-cta">Call Now</a>
            <?php endif; ?>
        </div>
    </div>
</nav>
'''
        
        sticky_nav_file = components_dir / "sticky-nav.php"
        sticky_nav_file.write_text(sticky_nav_content, encoding='utf-8')
    
    def create_contact_form(self, components_dir: Path):
        """Create enhanced contact form component"""
        contact_form_content = '''<?php
/**
 * Enhanced Contact Form Component
 */
?>
<div class="contact-form-wrapper">
    <form class="contact-form" id="contact-form" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
        <?php wp_nonce_field('contact_form_nonce', 'contact_nonce'); ?>
        <input type="hidden" name="action" value="submit_contact_form">
        
        <div class="form-group">
            <label for="contact-name">Full Name *</label>
            <input type="text" id="contact-name" name="contact_name" required aria-describedby="name-error">
            <span class="error-message" id="name-error"></span>
        </div>
        
        <div class="form-group">
            <label for="contact-email">Email Address *</label>
            <input type="email" id="contact-email" name="contact_email" required aria-describedby="email-error">
            <span class="error-message" id="email-error"></span>
        </div>
        
        <div class="form-group">
            <label for="contact-phone">Phone Number</label>
            <input type="tel" id="contact-phone" name="contact_phone" aria-describedby="phone-error">
            <span class="error-message" id="phone-error"></span>
        </div>
        
        <div class="form-group">
            <label for="contact-service">Service Needed</label>
            <select id="contact-service" name="contact_service">
                <option value="">Select a service...</option>
                <?php
                $business_services = get_option('business_services', array());
                if (!empty($business_services)) {
                    foreach ($business_services as $service_name => $service_description) {
                        $service_value = strtolower(str_replace(array(' ', '&', '/'), array('-', '', '-'), $service_name));
                        echo '<option value="' . esc_attr($service_value) . '">' . esc_html($service_name) . '</option>';
                    }
                } else {
                    // Fallback options
                    echo '<option value="consultation">Consultation</option>';
                    echo '<option value="custom-service">Custom Service</option>';
                }
                ?>
                <option value="general-support">General Support</option>
                <option value="other">Other</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="contact-message">Message *</label>
            <textarea id="contact-message" name="contact_message" rows="5" required aria-describedby="message-error"></textarea>
            <span class="error-message" id="message-error"></span>
        </div>
        
        <div class="form-group">
            <button type="submit" class="submit-button">
                <span class="button-text">Send Message</span>
                <span class="button-loading" style="display: none;">Sending...</span>
            </button>
        </div>
        
        <div class="form-messages">
            <div class="success-message" id="success-message" style="display: none;">
                Thank you! Your message has been sent successfully.
            </div>
            <div class="error-message" id="form-error" style="display: none;">
                There was an error sending your message. Please try again.
            </div>
        </div>
    </form>
</div>
'''
        
        contact_form_file = components_dir / "contact-form.php"
        contact_form_file.write_text(contact_form_content, encoding='utf-8')
    
    def create_service_cards(self, components_dir: Path):
        """Create animated service cards component with dynamic services"""
        service_cards_content = '''<?php
/**
 * Service Cards Component - Dynamic Services
 */

// Load services from spec file or WordPress options
$services = array();

// Try to get services from WordPress options first
$wp_services = get_option('business_services', array());
if (!empty($wp_services)) {
    $services = $wp_services;
    if (WP_DEBUG) {
        error_log('🔧 Component Library: Using services from WordPress options');
    }
} else {
    // Fallback: try to load from spec file
    $spec_file = get_template_directory() . '/specs/template_spec.json';
    if (file_exists($spec_file)) {
        $spec_data = json_decode(file_get_contents($spec_file), true);
        if (isset($spec_data['business_info']['services']) && !empty($spec_data['business_info']['services'])) {
            $services_list = $spec_data['business_info']['services'];
            foreach ($services_list as $service_name) {
                $services[$service_name] = generate_service_description($service_name);
            }
            if (WP_DEBUG) {
                error_log('🔧 Component Library: Using services from spec file');
            }
        }
    } else {
        if (WP_DEBUG) {
            error_log('⚠️ Component Library: Spec file not found at ' . $spec_file);
        }
    }
}

// Final fallback: generate services based on business type
if (empty($services)) {
    $business_type = get_option('business_type', 'Service Business');
    $services = get_fallback_services($business_type);
    if (WP_DEBUG) {
        error_log('⚠️ Component Library: Using fallback services for business type: ' . $business_type);
    }
}

// Service icons mapping
$service_icons = array(
    'landscape' => '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
    'design' => '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>',
    'maintenance' => '<path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>',
    'repair' => '<path d="M20 6h-2.18c.11-.31.18-.65.18-1a2.996 2.996 0 0 0-5.5-1.65l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2z"/>',
    'default' => '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>'
);

function get_service_icon($service_name) {
    global $service_icons;
    $service_lower = strtolower($service_name);

    if (strpos($service_lower, 'landscape') !== false || strpos($service_lower, 'design') !== false) {
        return $service_icons['landscape'];
    } elseif (strpos($service_lower, 'maintenance') !== false || strpos($service_lower, 'care') !== false) {
        return $service_icons['maintenance'];
    } elseif (strpos($service_lower, 'repair') !== false || strpos($service_lower, 'hardware') !== false) {
        return $service_icons['repair'];
    } else {
        return $service_icons['default'];
    }
}

function generate_service_description($service_name) {
    $service_lower = strtolower($service_name);

    if (strpos($service_lower, 'landscape') !== false || strpos($service_lower, 'design') !== false) {
        return "Professional landscape design services to transform your outdoor space into a beautiful and functional environment.";
    } elseif (strpos($service_lower, 'hardscape') !== false || strpos($service_lower, 'patio') !== false) {
        return "Expert hardscaping and patio installation to create stunning outdoor living areas for your home.";
    } elseif (strpos($service_lower, 'lawn') !== false || strpos($service_lower, 'maintenance') !== false) {
        return "Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.";
    } elseif (strpos($service_lower, 'tree') !== false || strpos($service_lower, 'plant') !== false) {
        return "Professional tree and plant care services including pruning, planting, and health assessments.";
    } else {
        return "Professional service tailored to meet your specific needs with quality results and customer satisfaction.";
    }
}

function get_fallback_services($business_type) {
    $business_lower = strtolower($business_type);

    if (strpos($business_lower, 'landscaping') !== false) {
        return array(
            'Landscape Design' => 'Professional landscape design services to transform your outdoor space.',
            'Hardscaping & Patios' => 'Expert hardscaping and patio installation for outdoor living areas.',
            'Lawn Maintenance' => 'Comprehensive lawn care and maintenance services year-round.'
        );
    } elseif (strpos($business_lower, 'repair') !== false || strpos($business_lower, 'pc') !== false) {
        return array(
            'Computer Diagnostics' => 'Comprehensive computer diagnostics to identify and resolve issues.',
            'Hardware Repair' => 'Professional hardware repair services for all computer components.',
            'Software Solutions' => 'Expert software installation and troubleshooting services.'
        );
    } else {
        return array(
            'Professional Consultation' => 'Expert consultation services tailored to your specific needs.',
            'Custom Solutions' => 'Personalized solutions designed to address your unique challenges.',
            'Quality Support' => 'Reliable ongoing support to ensure continued success.'
        );
    }
}
?>
<div class="service-cards-grid">
    <?php foreach ($services as $service_name => $service_desc): ?>
        <?php
        // Generate service features based on service type
        $service_lower = strtolower($service_name);
        $features = array();
        if (strpos($service_lower, 'landscape') !== false || strpos($service_lower, 'design') !== false) {
            $features = array('Site analysis and planning', 'Custom design concepts', 'Plant selection guidance', 'Installation oversight', 'Seasonal maintenance tips');
        } elseif (strpos($service_lower, 'hardscaping') !== false || strpos($service_lower, 'patio') !== false) {
            $features = array('Material selection', 'Professional installation', 'Drainage solutions', 'Lighting integration', 'Warranty coverage');
        } elseif (strpos($service_lower, 'lawn') !== false || strpos($service_lower, 'maintenance') !== false) {
            $features = array('Regular mowing service', 'Fertilization program', 'Weed control', 'Seasonal cleanup', 'Equipment maintenance');
        } elseif (strpos($service_lower, 'virus') !== false || strpos($service_lower, 'malware') !== false) {
            $features = array('Full system scan', 'Malware removal', 'Security updates', 'Prevention education', 'Follow-up support');
        } elseif (strpos($service_lower, 'hardware') !== false || strpos($service_lower, 'repair') !== false) {
            $features = array('Hardware diagnosis', 'Component replacement', 'Performance upgrades', 'System testing', 'Warranty on parts');
        } elseif (strpos($service_lower, 'data') !== false || strpos($service_lower, 'recovery') !== false) {
            $features = array('Data recovery', 'Backup setup', 'Cloud solutions', 'Emergency response', 'Data protection');
        } else {
            $features = array('Professional consultation', 'Quality service delivery', 'Customer support', 'Satisfaction guarantee', 'Follow-up service');
        }

        // Generate pricing based on service type
        $pricing = 'Contact for pricing';
        if (strpos($service_lower, 'landscape') !== false || strpos($service_lower, 'design') !== false) {
            $pricing = 'Starting at $150';
        } elseif (strpos($service_lower, 'hardscaping') !== false || strpos($service_lower, 'patio') !== false) {
            $pricing = 'Starting at $200';
        } elseif (strpos($service_lower, 'lawn') !== false || strpos($service_lower, 'maintenance') !== false) {
            $pricing = 'Starting at $75';
        } elseif (strpos($service_lower, 'virus') !== false || strpos($service_lower, 'malware') !== false) {
            $pricing = 'Starting at $89';
        } elseif (strpos($service_lower, 'hardware') !== false || strpos($service_lower, 'repair') !== false) {
            $pricing = 'Starting at $75';
        } elseif (strpos($service_lower, 'data') !== false || strpos($service_lower, 'recovery') !== false) {
            $pricing = 'Starting at $125';
        }

        // Generate CTA text
        $cta_text = 'Get Started';
        if (strpos($service_lower, 'design') !== false) {
            $cta_text = 'Get Design Quote';
        } elseif (strpos($service_lower, 'maintenance') !== false) {
            $cta_text = 'Schedule Service';
        } elseif (strpos($service_lower, 'recovery') !== false) {
            $cta_text = 'Recover Data';
        } elseif (strpos($service_lower, 'virus') !== false || strpos($service_lower, 'malware') !== false) {
            $cta_text = 'Get Help Now';
        }
        ?>
    <div class="service-card">
        <div class="service-header">
            <div class="service-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                    <?php echo get_service_icon($service_name); ?>
                </svg>
            </div>
            <h3><?php echo esc_html($service_name); ?></h3>
        </div>
        <div class="service-body">
            <p class="service-description"><?php echo esc_html($service_desc); ?></p>
            <div class="service-features">
                <h4>What\\'s Included:</h4>
                <ul>
                    <?php foreach ($features as $feature): ?>
                        <li><?php echo esc_html($feature); ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>
        </div>
        <div class="service-footer">
            <div class="service-pricing">
                <span class="price-label">Starting at</span>
                <span class="price"><?php echo esc_html($pricing); ?></span>
            </div>
            <div class="service-actions">
                <?php $phone = get_option('business_phone'); if ($phone): ?>
                    <a href="tel:<?php echo esc_attr($phone); ?>" class="btn btn-primary"><?php echo esc_html($cta_text); ?></a>
                <?php else: ?>
                    <a href="<?php echo esc_url(home_url('/contact/')); ?>" class="btn btn-primary"><?php echo esc_html($cta_text); ?></a>
                <?php endif; ?>
                <button class="btn btn-secondary service-details-toggle">Learn More</button>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
'''

        service_cards_file = components_dir / "service-cards.php"
        service_cards_file.write_text(service_cards_content, encoding='utf-8')

    def create_components_js(self, js_dir: Path):
        """Create JavaScript for all components"""
        js_content = '''/**
 * Component Library JavaScript
 * Handles testimonial slider, sticky navigation, contact form, and service cards
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initTestimonialSlider();
    initStickyNavigation();
    initContactForm();
    initServiceCards();
});

/**
 * Testimonial Slider
 */
function initTestimonialSlider() {
    const slider = document.getElementById('testimonial-slider');
    if (!slider) return;

    const slides = slider.querySelectorAll('.testimonial-slide');
    const dots = slider.querySelectorAll('.dot');
    const prevBtn = slider.querySelector('.testimonial-prev');
    const nextBtn = slider.querySelector('.testimonial-next');

    let currentSlide = 0;
    let autoSlideInterval;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
        currentSlide = index;
    }

    function nextSlide() {
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }

    function prevSlide() {
        const prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }

    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 5000);
    }

    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }

    // Event listeners
    if (nextBtn) nextBtn.addEventListener('click', () => { stopAutoSlide(); nextSlide(); startAutoSlide(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { stopAutoSlide(); prevSlide(); startAutoSlide(); });

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopAutoSlide();
            showSlide(index);
            startAutoSlide();
        });
    });

    // Pause on hover
    slider.addEventListener('mouseenter', stopAutoSlide);
    slider.addEventListener('mouseleave', startAutoSlide);

    // Touch support
    let touchStartX = 0;
    let touchEndX = 0;

    slider.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    slider.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            stopAutoSlide();
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
            startAutoSlide();
        }
    }

    // Start auto-slide
    startAutoSlide();
}

/**
 * Sticky Navigation
 */
function initStickyNavigation() {
    const stickyNav = document.getElementById('sticky-nav');
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('sticky-nav-menu');

    if (!stickyNav) return;

    // Sticky behavior
    let lastScrollY = window.scrollY;

    function handleScroll() {
        const currentScrollY = window.scrollY;

        if (currentScrollY > 100) {
            stickyNav.classList.add('visible');

            // Hide on scroll down, show on scroll up
            if (currentScrollY > lastScrollY) {
                stickyNav.classList.add('hidden');
            } else {
                stickyNav.classList.remove('hidden');
            }
        } else {
            stickyNav.classList.remove('visible', 'hidden');
        }

        lastScrollY = currentScrollY;
    }

    // Throttled scroll handler
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }
        scrollTimeout = setTimeout(handleScroll, 10);
    });

    // Enhanced mobile menu toggle with error handling
    if (mobileToggle && mobileMenu) {
        console.log('🔧 Initializing sticky nav mobile menu...');

        function toggleStickyMobileMenu(event) {
            try {
                event.preventDefault();
                event.stopPropagation();

                console.log('🔄 Toggling sticky mobile menu...');

                const isActive = mobileMenu.classList.contains('active');

                if (isActive) {
                    mobileMenu.classList.remove('active');
                    mobileToggle.classList.remove('active');
                    mobileToggle.setAttribute('aria-expanded', 'false');
                    document.body.classList.remove('sticky-mobile-menu-open');
                    console.log('📴 Sticky mobile menu closed');
                } else {
                    mobileMenu.classList.add('active');
                    mobileToggle.classList.add('active');
                    mobileToggle.setAttribute('aria-expanded', 'true');
                    document.body.classList.add('sticky-mobile-menu-open');
                    console.log('📱 Sticky mobile menu opened');
                }
            } catch (error) {
                console.error('❌ Error toggling sticky mobile menu:', error);
            }
        }

        // Add click and touch event listeners
        mobileToggle.addEventListener('click', toggleStickyMobileMenu);
        mobileToggle.addEventListener('touchstart', toggleStickyMobileMenu);

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileToggle.contains(event.target) && !mobileMenu.contains(event.target)) {
                if (mobileMenu.classList.contains('active')) {
                    mobileMenu.classList.remove('active');
                    mobileToggle.classList.remove('active');
                    mobileToggle.setAttribute('aria-expanded', 'false');
                    document.body.classList.remove('sticky-mobile-menu-open');
                }
            }
        });

        // Close menu on escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && mobileMenu.classList.contains('active')) {
                mobileMenu.classList.remove('active');
                mobileToggle.classList.remove('active');
                mobileToggle.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('sticky-mobile-menu-open');
            }
        });

        console.log('✅ Sticky nav mobile menu initialized successfully');
    }

    // Smooth scroll for navigation links
    const navLinks = stickyNav.querySelectorAll('.nav-link[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Close mobile menu if open
                if (mobileMenu) {
                    mobileMenu.classList.remove('active');
                    mobileToggle.classList.remove('active');
                }
            }
        });
    });
}

/**
 * Contact Form
 */
function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const submitButton = form.querySelector('.submit-button');
    const buttonText = form.querySelector('.button-text');
    const buttonLoading = form.querySelector('.button-loading');
    const successMessage = document.getElementById('success-message');
    const errorMessage = document.getElementById('form-error');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous messages
        hideMessages();

        // Validate form
        if (!validateForm()) {
            return;
        }

        // Show loading state
        setLoadingState(true);

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                showSuccessMessage();
                form.reset();
            } else {
                showErrorMessage();
            }
        } catch (error) {
            showErrorMessage();
        } finally {
            setLoadingState(false);
        }
    });

    function validateForm() {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            const errorElement = document.getElementById(field.getAttribute('aria-describedby'));

            if (!field.value.trim()) {
                showFieldError(field, errorElement, 'This field is required');
                isValid = false;
            } else {
                clearFieldError(field, errorElement);
            }
        });

        // Email validation
        const emailField = form.querySelector('[type="email"]');
        if (emailField && emailField.value) {
            const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
            const errorElement = document.getElementById(emailField.getAttribute('aria-describedby'));

            if (!emailRegex.test(emailField.value)) {
                showFieldError(emailField, errorElement, 'Please enter a valid email address');
                isValid = false;
            }
        }

        return isValid;
    }

    function showFieldError(field, errorElement, message) {
        field.classList.add('error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }

    function clearFieldError(field, errorElement) {
        field.classList.remove('error');
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    }

    function setLoadingState(loading) {
        submitButton.disabled = loading;
        buttonText.style.display = loading ? 'none' : 'inline';
        buttonLoading.style.display = loading ? 'inline' : 'none';
    }

    function showSuccessMessage() {
        if (successMessage) {
            successMessage.style.display = 'block';
        }
    }

    function showErrorMessage() {
        if (errorMessage) {
            errorMessage.style.display = 'block';
        }
    }

    function hideMessages() {
        if (successMessage) successMessage.style.display = 'none';
        if (errorMessage) errorMessage.style.display = 'none';
    }
}

/**
 * Service Cards
 */
function initServiceCards() {
    const serviceCards = document.querySelectorAll('.service-card');

    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('hovered');
        });

        card.addEventListener('mouseleave', () => {
            card.classList.remove('hovered');
        });
    });
}
'''

        js_file = js_dir / "components.js"
        js_file.write_text(js_content, encoding='utf-8')

    def create_components_css(self, css_dir: Path):
        """Create CSS for all components"""
        css_content = '''/**
 * Component Library CSS
 * Styles for testimonial slider, sticky navigation, contact form, and service cards
 */

/* Testimonial Slider */
.testimonial-slider {
    max-width: 800px;
    margin: 3rem auto;
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 12px;
    position: relative;
}

.testimonial-container {
    position: relative;
    overflow: hidden;
    min-height: 200px;
}

.testimonial-slide {
    opacity: 0;
    transform: translateX(100%);
    transition: all 0.5s ease-in-out;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
}

.testimonial-slide.active {
    opacity: 1;
    transform: translateX(0);
    position: relative;
}

.testimonial-content {
    text-align: center;
    padding: 1rem;
}

.testimonial-content blockquote {
    font-size: 1.2rem;
    font-style: italic;
    margin: 0 0 1.5rem 0;
    color: #333;
    line-height: 1.6;
}

.testimonial-content cite {
    display: block;
    font-style: normal;
}

.testimonial-content cite strong {
    display: block;
    font-size: 1.1rem;
    color: #007cba;
    margin-bottom: 0.25rem;
}

.testimonial-content cite span {
    color: #666;
    font-size: 0.9rem;
}

.testimonial-navigation {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
}

.testimonial-prev,
.testimonial-next {
    background: #007cba;
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.2rem;
    transition: background-color 0.3s ease;
}

.testimonial-prev:hover,
.testimonial-next:hover {
    background: #005a87;
}

.testimonial-dots {
    display: flex;
    gap: 0.5rem;
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: none;
    background: #ccc;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.dot.active {
    background: #007cba;
}

/* Sticky Navigation */
.sticky-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    transform: translateY(-100%);
    transition: transform 0.3s ease;
}

.sticky-nav.visible {
    transform: translateY(0);
}

.sticky-nav.hidden {
    transform: translateY(-100%);
}

.sticky-nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
}

.sticky-nav-brand a {
    font-size: 1.5rem;
    font-weight: bold;
    color: #007cba;
    text-decoration: none;
}

.sticky-nav-menu {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-link {
    color: #333;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: #007cba;
}

.nav-cta {
    background: #007cba;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.nav-cta:hover {
    background: #005a87;
}

.mobile-menu-toggle {
    display: none;
    flex-direction: column;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
}

.mobile-menu-toggle span {
    width: 25px;
    height: 3px;
    background: #333;
    margin: 3px 0;
    transition: 0.3s;
}

.mobile-menu-toggle.active span:nth-child(1) {
    transform: rotate(-45deg) translate(-5px, 6px);
}

.mobile-menu-toggle.active span:nth-child(2) {
    opacity: 0;
}

.mobile-menu-toggle.active span:nth-child(3) {
    transform: rotate(45deg) translate(-5px, -6px);
}

/* Contact Form */
.contact-form-wrapper {
    max-width: 600px;
    margin: 3rem auto;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e1e5e9;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #007cba;
}

.form-group input.error,
.form-group select.error,
.form-group textarea.error {
    border-color: #dc3545;
}

.error-message {
    color: #dc3545;
    font-size: 0.875rem;
    margin-top: 0.25rem;
    display: none;
}

.submit-button {
    background: #007cba;
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 5px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
}

.submit-button:hover:not(:disabled) {
    background: #005a87;
}

.submit-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.success-message {
    background: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 5px;
    margin-top: 1rem;
}

.form-messages .error-message {
    background: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 5px;
    margin-top: 1rem;
    display: none;
}

/* Service Cards */
.service-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.service-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-card:hover,
.service-card.hovered {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.service-icon {
    color: #007cba;
    margin-bottom: 1rem;
}

.service-card h3 {
    color: #333;
    margin-bottom: 1rem;
    font-size: 1.25rem;
}

.service-card p {
    color: #666;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.service-features {
    list-style: none;
    padding: 0;
    margin: 1.5rem 0;
}

.service-features li {
    padding: 0.5rem 0;
    color: #555;
    position: relative;
    padding-left: 1.5rem;
}

.service-features li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #28a745;
    font-weight: bold;
}

.service-cta {
    display: inline-block;
    background: #007cba;
    color: white;
    padding: 0.75rem 1.5rem;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.service-cta:hover {
    background: #005a87;
}

/* Responsive Design */
@media (max-width: 768px) {
    .sticky-nav-menu {
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        background: white;
        flex-direction: column;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transform: translateY(-100%);
        transition: transform 0.3s ease;
    }

    .sticky-nav-menu.active {
        transform: translateY(0);
    }

    .mobile-menu-toggle {
        display: flex;
    }

    .testimonial-slider {
        padding: 1rem;
    }

    .contact-form-wrapper {
        margin: 2rem 1rem;
        padding: 1.5rem;
    }

    .service-cards-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
        margin: 2rem 1rem;
    }

    .service-card {
        padding: 1.5rem;
    }
}

@media (max-width: 480px) {
    .testimonial-content blockquote {
        font-size: 1rem;
    }

    .testimonial-navigation {
        gap: 0.5rem;
    }

    .testimonial-prev,
    .testimonial-next {
        width: 35px;
        height: 35px;
        font-size: 1rem;
    }
}
'''

        css_file = css_dir / "components.css"
        css_file.write_text(css_content, encoding='utf-8')

    def enhance_functions_php(self, theme_dir: Path):
        """Enhance functions.php to enqueue component assets"""
        functions_file = theme_dir / "functions.php"

        if not functions_file.exists():
            return

        content = functions_file.read_text(encoding='utf-8')

        # Add component enqueue function
        component_functions = '''
/**
 * Enqueue component assets - Enhanced for Bluehost compatibility
 */
function ai_theme_enqueue_components() {
    wp_enqueue_style('ai-theme-components', get_template_directory_uri() . '/css/components.css', array('ai-theme-style'), '1.0');

    // Remove jQuery dependency for better Bluehost compatibility
    wp_enqueue_script('ai-theme-components', get_template_directory_uri() . '/js/components.js', array(), '1.0', true);

    // Add inline script for debugging on live sites
    wp_add_inline_script('ai-theme-components', '
        console.log("🎯 Component script loaded successfully");
        console.log("📍 Current URL:", window.location.href);
        console.log("📱 Screen width:", window.innerWidth);
    ');
}
add_action('wp_enqueue_scripts', 'ai_theme_enqueue_components');

/**
 * Handle contact form submission
 */
function handle_contact_form_submission() {
    if (!isset($_POST['contact_nonce']) || !wp_verify_nonce($_POST['contact_nonce'], 'contact_form_nonce')) {
        wp_die('Security check failed');
    }

    $name = sanitize_text_field($_POST['contact_name']);
    $email = sanitize_email($_POST['contact_email']);
    $phone = sanitize_text_field($_POST['contact_phone']);
    $service = sanitize_text_field($_POST['contact_service']);
    $message = sanitize_textarea_field($_POST['contact_message']);

    // Send email (basic implementation)
    $to = get_option('admin_email');
    $subject = 'New Contact Form Submission';
    $body = "Name: $name\\nEmail: $email\\nPhone: $phone\\nService: $service\\nMessage: $message";
    $headers = array('Content-Type: text/plain; charset=UTF-8');

    if (wp_mail($to, $subject, $body, $headers)) {
        wp_redirect(add_query_arg('contact', 'success', wp_get_referer()));
    } else {
        wp_redirect(add_query_arg('contact', 'error', wp_get_referer()));
    }
    exit;
}
add_action('admin_post_submit_contact_form', 'handle_contact_form_submission');
add_action('admin_post_nopriv_submit_contact_form', 'handle_contact_form_submission');
'''

        # Insert before closing PHP tag if it exists, otherwise append
        if content.strip().endswith('?>'):
            content = content.rstrip('?>').rstrip() + "\\n\\n" + component_functions + "\\n?>"
        else:
            content += "\\n\\n" + component_functions

        functions_file.write_text(content, encoding='utf-8')

    def enhance_header_php(self, theme_dir: Path):
        """Enhance header.php to include sticky navigation"""
        header_file = theme_dir / "header.php"

        if not header_file.exists():
            return

        content = header_file.read_text(encoding='utf-8')

        # Add sticky navigation after the main header
        sticky_nav_include = '''
    <?php get_template_part('components/sticky-nav'); ?>
'''

        # Insert after the closing </header> tag
        header_pattern = r'(</header>)'
        content = re.sub(header_pattern, f'\\1{sticky_nav_include}', content)

        header_file.write_text(content, encoding='utf-8')

    def enhance_services_page(self, theme_dir: Path):
        """Enhance services page with interactive elements"""
        services_file = theme_dir / "page-services.php"

        if not services_file.exists():
            return

        content = services_file.read_text(encoding='utf-8')

        # Add JavaScript for service details toggle
        js_enhancement = """

        <!-- Enhanced Services Page JavaScript -->
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Service details toggle functionality
            const toggleButtons = document.querySelectorAll('.service-details-toggle');

            toggleButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const serviceCard = this.closest('.service-card');
                    const features = serviceCard.querySelector('.service-features');

                    if (features.style.display === 'none') {
                        features.style.display = 'block';
                        this.textContent = 'Show Less';
                        serviceCard.classList.add('expanded');
                    } else {
                        features.style.display = 'none';
                        this.textContent = 'Learn More';
                        serviceCard.classList.remove('expanded');
                    }
                });

                // Initially hide features on mobile
                if (window.innerWidth <= 768) {
                    const serviceCard = button.closest('.service-card');
                    const features = serviceCard.querySelector('.service-features');
                    features.style.display = 'none';
                }
            });

            // Smooth scroll to contact form when clicking CTA buttons
            const ctaButtons = document.querySelectorAll('.service-actions .btn-primary');
            ctaButtons.forEach(button => {
                if (button.getAttribute('href').includes('/contact/')) {
                    button.addEventListener('click', function(e) {
                        // Add smooth scroll behavior for better UX
                        if (window.location.pathname === '/contact/') {
                            e.preventDefault();
                            window.location.href = this.getAttribute('href') + '?service=' +
                                encodeURIComponent(this.closest('.service-card').querySelector('h3').textContent);
                        }
                    });
                }
            });

            // Add loading states for better perceived performance
            const serviceCards = document.querySelectorAll('.service-card');
            serviceCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';

                setTimeout(() => {
                    card.style.transition = 'all 0.6s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
        </script>

        <style>
        .service-card.expanded {
            background: rgba(var(--primary-rgb, 59, 106, 77), 0.08);
        }

        .service-features {
            transition: all 0.3s ease;
        }

        @media (max-width: 768px) {
            .service-features {
                margin-top: 1rem;
            }
        }
        </style>
        """

        # Insert before get_footer() call or at the end
        if '<?php get_footer(); ?>' in content:
            content = content.replace('<?php get_footer(); ?>', js_enhancement + '\n\n<?php get_footer(); ?>')
        elif '</body>' in content:
            content = content.replace('</body>', js_enhancement + '\n</body>')
        else:
            content += js_enhancement

        services_file.write_text(content, encoding='utf-8')

    def enhance_index_php(self, theme_dir: Path):
        """Enhance index.php to include components"""
        index_file = theme_dir / "index.php"

        if not index_file.exists():
            return

        content = index_file.read_text(encoding='utf-8')

        # Add components to the main content area
        components_include = '''
    <section id="services" class="services-section">
        <div class="container">
            <h2>Our Services</h2>
            <?php get_template_part('components/service-cards'); ?>
        </div>
    </section>

    <section id="testimonials" class="testimonials-section">
        <div class="container">
            <h2>What Our Customers Say</h2>
            <?php get_template_part('components/testimonials'); ?>
        </div>
    </section>

    <section id="contact" class="contact-section">
        <div class="container">
            <h2>Get In Touch</h2>
            <?php get_template_part('components/contact-form'); ?>
        </div>
    </section>
'''

        # Insert before the sidebar and footer
        sidebar_pattern = r'(<?php\\s*get_sidebar\\(\\);)'
        content = re.sub(sidebar_pattern, f'{components_include}\\n\\1', content)

        index_file.write_text(content, encoding='utf-8')
