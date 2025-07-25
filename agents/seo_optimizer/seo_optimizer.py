import json
import re
import shutil
from pathlib import Path
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import sys
import os

# Add the project root to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.agent_result import AgentResult


class SeoOptimizer:
    def __init__(self, config=None):
        if config is None:
            config_path = Path(__file__).parent / "seo_optimizer.json"
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = config
    
    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        """
        Enhance WordPress theme with local SEO optimization and schema markup
        """
        try:
            input_path = Path(input_file)
            template_id = self.extract_template_id(input_path.name)
            
            # Create SEO enhanced theme directory
            template_dir = input_path.parent  # Go up from wordpress_theme_xxx/ to template_xxx/
            seo_theme_dir = template_dir.parent / f"seo_enhanced_theme_{template_id}"

            # The template_dir IS the template_xxx directory that contains the spec file
            self.current_theme_dir = template_dir  # Store for use in helper methods
            
            # Copy WordPress theme to SEO enhanced directory
            if input_path.is_dir():
                shutil.copytree(input_path, seo_theme_dir, dirs_exist_ok=True)
            else:
                # If input is a file, copy the parent directory
                shutil.copytree(input_path.parent, seo_theme_dir, dirs_exist_ok=True)
            
            # Extract business information from template spec
            business_info = self.extract_business_info(template_dir)
            
            # Enhance theme files with SEO
            self.enhance_header_php(seo_theme_dir, business_info)
            self.enhance_functions_php(seo_theme_dir, business_info)
            self.enhance_index_php(seo_theme_dir, business_info)
            self.enhance_style_css(seo_theme_dir, business_info)
            self.create_schema_markup(seo_theme_dir, business_info)
            
            print(f"✅ SEO enhanced theme generated in {seo_theme_dir}")
            
            return AgentResult(
                agent_id="seo_optimizer",
                success=True,
                output_file=str(seo_theme_dir),
                metadata={"template_id": template_id, "seo_features": 5}
            )
            
        except Exception as e:
            return AgentResult(
                agent_id="seo_optimizer",
                success=False,
                error_message=str(e)
            )
    
    def extract_template_id(self, filename: str) -> str:
        """Extract template ID from filename or directory name"""
        match = re.search(r"(?:template_|wordpress_theme_)([a-zA-Z0-9_]+)", filename)
        return match.group(1) if match else "000"
    
    def extract_business_info(self, template_dir: Path) -> Dict[str, Any]:
        """Extract business information from template spec"""
        spec_file = template_dir / "specs" / "template_spec.json"
        
        default_info = {
            "business_name": "Local Service Business",
            "city": "Your City",
            "state": "Your State",
            "service": "Professional Services",
            "business_type": "Professional Services",
            "phone": "",
            "services_list": "Professional Services",
            "area": "Local Area",
            "year": "2020"
        }
        
        if spec_file.exists():
            try:
                with open(spec_file, 'r') as f:
                    spec = json.load(f)
                
                # Extract location info
                location = spec.get("location", {})
                default_info.update({
                    "city": location.get("city", "Your City"),
                    "state": location.get("state", "Your State"),
                    "area": location.get("region", "Local Area")
                })
                
                # Extract business info from business_info section
                if "business_info" in spec:
                    business_info = spec["business_info"]
                    default_info.update({
                        "business_name": business_info.get("business_name", default_info["business_name"]),
                        "service": business_info.get("business_type", default_info["service"]),
                        "business_type": business_info.get("business_type", default_info["service"]),
                        "phone": business_info.get("phone", default_info["phone"])
                    })
                
            except Exception as e:
                print(f"Warning: Could not parse spec file: {e}")
        
        return default_info
    
    def enhance_header_php(self, theme_dir: Path, business_info: Dict[str, Any]):
        """Enhance header.php with SEO meta tags and schema markup"""
        header_file = theme_dir / "header.php"
        
        if not header_file.exists():
            return
        
        content = header_file.read_text(encoding='utf-8')
        
        # Generate SEO meta tags
        seo_meta = self.generate_seo_meta_tags(business_info)
        
        # Insert SEO meta tags before wp_head()
        wp_head_pattern = r'(\s*<?php wp_head\(\); \?>)'
        seo_enhanced = f"{seo_meta}\\1"
        content = re.sub(wp_head_pattern, seo_enhanced, content)
        
        header_file.write_text(content, encoding='utf-8')
    
    def generate_seo_meta_tags(self, business_info: Dict[str, Any]) -> str:
        """Generate comprehensive SEO meta tags"""
        service = business_info["service"]
        city = business_info["city"]
        state = business_info["state"]
        business_name = business_info["business_name"]
        phone = business_info["phone"]
        services_list = business_info["services_list"]
        
        # Generate optimized title and description
        title = f"{service} in {city}, {state} | {business_name}"
        description = f"Professional {service} in {city}, {state}. {business_name} provides {services_list}. Call {phone} for a free quote!"
        
        return f"""
    <!-- SEO Meta Tags -->
    <meta name="description" content="{description}">
    <meta name="keywords" content="{service}, {city} {service}, {state} {service}, local {service}, {service} near me">
    <meta name="author" content="{business_name}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="<?php echo esc_url(home_url('/')); ?>">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="<?php echo esc_url(home_url('/')); ?>">
    <meta property="og:site_name" content="{business_name}">
    <meta property="og:locale" content="en_US">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    
    <!-- Local Business Meta Tags -->
    <meta name="geo.region" content="US-{state[:2].upper()}">
    <meta name="geo.placename" content="{city}">
    <meta name="geo.position" content="45.1611;-93.4758">
    <meta name="ICBM" content="45.1611, -93.4758">
    
    <!-- Google Site Verification (placeholder) -->
    <meta name="google-site-verification" content="your-verification-code-here">
"""
    
    def enhance_functions_php(self, theme_dir: Path, business_info: Dict[str, Any]):
        """Enhance functions.php with SEO-related functionality"""
        functions_file = theme_dir / "functions.php"
        
        if not functions_file.exists():
            return
        
        content = functions_file.read_text(encoding='utf-8')
        
        # Add SEO functions before the closing PHP tag or at the end
        seo_functions = self.generate_seo_functions(business_info)
        
        # Insert before closing PHP tag if it exists, otherwise append
        if content.strip().endswith('?>'):
            content = content.rstrip('?>').rstrip() + "\n\n" + seo_functions + "\n?>"
        else:
            content += "\n\n" + seo_functions
        
        functions_file.write_text(content, encoding='utf-8')
    
    def generate_seo_functions(self, business_info: Dict[str, Any]) -> str:
        """Generate SEO-related WordPress functions"""
        template_id = "seo"  # Simplified for this function
        
        return f"""
/**
 * SEO Enhancements
 */

// Custom title tag for better SEO
function ai_theme_seo_title($title) {{
    if (is_home() || is_front_page()) {{
        return '{business_info["service"]} in {business_info["city"]}, {business_info["state"]} | {business_info["business_name"]}';
    }}
    return $title;
}}
add_filter('wp_title', 'ai_theme_seo_title');

// Add structured data to footer
function ai_theme_add_schema_markup() {{
    if (is_home() || is_front_page()) {{
        echo ai_theme_get_local_business_schema();
    }}
}}
add_action('wp_footer', 'ai_theme_add_schema_markup');

// Generate local business schema
function ai_theme_get_local_business_schema() {{
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'LocalBusiness',
        'name' => '{business_info["business_name"]}',
        'description' => 'Professional {business_info["service"]} services in {business_info["city"]}, {business_info["state"]}',
        'url' => home_url('/'),
        'telephone' => '{business_info["phone"]}',
        'address' => array(
            '@type' => 'PostalAddress',
            'addressLocality' => '{business_info["city"]}',
            'addressRegion' => '{business_info["state"]}',
            'addressCountry' => 'US'
        ),
        'geo' => array(
            '@type' => 'GeoCoordinates',
            'latitude' => '45.1611',
            'longitude' => '-93.4758'
        ),
        'openingHours' => 'Mo-Fr 08:00-18:00',
        'priceRange' => '$$',
        'serviceArea' => array(
            '@type' => 'GeoCircle',
            'geoMidpoint' => array(
                '@type' => 'GeoCoordinates',
                'latitude' => '45.1611',
                'longitude' => '-93.4758'
            ),
            'geoRadius' => '25000'
        )
    );
    
    return '<script type="application/ld+json">' . json_encode($schema, JSON_UNESCAPED_SLASHES) . '</script>';
}}

// Optimize meta descriptions
function ai_theme_meta_description() {{
    if (is_home() || is_front_page()) {{
        echo '<meta name="description" content="Professional {business_info["service"]} in {business_info["city"]}, {business_info["state"]}. {business_info["business_name"]} provides {business_info["services_list"]}. Call {business_info["phone"]} for a free quote!">';
    }}
}}
add_action('wp_head', 'ai_theme_meta_description');
"""

    def enhance_index_php(self, theme_dir: Path, business_info: Dict[str, Any]):
        """Enhance index.php with SEO-optimized content structure"""
        index_file = theme_dir / "index.php"

        if not index_file.exists():
            return

        content = index_file.read_text(encoding='utf-8')

        # Add SEO-optimized heading structure
        service = business_info["service"]
        city = business_info["city"]
        state = business_info["state"]
        business_name = business_info["business_name"]

        # Replace generic title with SEO-optimized version
        title_pattern = r'(<h1[^>]*>)([^<]+)(</h1>)'
        seo_title = f"\\1{service} in {city}, {state} - {business_name}\\3"
        content = re.sub(title_pattern, seo_title, content)

        # Add local business content if it's a basic template
        if "Sorry, no posts matched" in content:
            seo_content = self.generate_seo_content(business_info)
            content = content.replace(
                '<?php _e(\'Sorry, no posts matched your criteria.\', \'ai-theme-{template_id}\'); ?>',
                seo_content
            )

        index_file.write_text(content, encoding='utf-8')

    def generate_seo_content(self, business_info: Dict[str, Any]) -> str:
        """Generate SEO-optimized content for local business"""
        return f"""
        <div class="local-business-content">
            <h1>{business_info["service"]} in {business_info["city"]}, {business_info["state"]}</h1>

            <div class="hero-section">
                <h2>Professional {business_info["service"]} Services</h2>
                <p>Welcome to {business_info["business_name"]}, your trusted {business_info["service"]} provider in {business_info["city"]}, {business_info["state"]}. We offer comprehensive {business_info["services_list"]} to keep your technology running smoothly.</p>
                <a href="tel:{business_info["phone"]}" class="cta-button">Call {business_info["phone"]} Now</a>
            </div>

            <div class="services-section">
                <h2>Our {business_info["service"]} Services in {business_info["area"]}</h2>
                <ul>
                    {self.generate_services_list_html(business_info)}
                </ul>
            </div>

            <div class="local-area">
                <h3>Serving {business_info["city"]} and Surrounding Areas</h3>
                <p>We proudly serve {business_info["city"]}, {business_info["state"]} and the entire {business_info["area"]} area. Our local {business_info["service"]} experts are ready to help with all your technology needs.</p>
            </div>
        </div>
        """

    def get_dynamic_services(self, business_info: Dict[str, Any]) -> Dict[str, str]:
        """Get services dynamically from spec file or generate based on business type"""
        # Try to read from spec file first
        spec_file = Path(self.current_theme_dir) / "specs" / "template_spec.json"
        if spec_file.exists():
            try:
                with open(spec_file, 'r', encoding='utf-8') as f:
                    spec_data = json.load(f)
                    if 'business_info' in spec_data and 'services' in spec_data['business_info']:
                        services_list = spec_data['business_info']['services']
                        services = {}
                        for service_name in services_list:
                            if service_name.lower() != 'services':  # Skip generic "Services" entry
                                services[service_name] = self.generate_service_description(service_name, business_info)
                        if services:
                            return services
            except (json.JSONDecodeError, KeyError):
                pass

        # Fallback: generate based on business type
        business_type = business_info.get('business_type', 'Service Business').lower()

        if 'landscaping' in business_type or 'landscape' in business_type:
            return {
                'Landscape Design': 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.',
                'Hardscaping & Patios': 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.',
                'Lawn Maintenance': 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'
            }
        elif 'repair' in business_type or 'pc' in business_type:
            return {
                'Computer Diagnostics': 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                'Hardware Repair': 'Professional hardware repair services for all types of computer components and peripherals.',
                'Software Solutions': 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
            }
        else:
            return {
                'Professional Consultation': 'Expert consultation services tailored to your specific needs and requirements.',
                'Custom Solutions': 'Personalized solutions designed to address your unique challenges and goals.',
                'Professional Support': 'Reliable ongoing support to ensure continued success and satisfaction.'
            }

    def generate_service_description(self, service_name: str, business_info: Dict[str, Any]) -> str:
        """Generate appropriate description for a service"""
        service_lower = service_name.lower()
        business_type = business_info.get('business_type', 'Service Business').lower()

        # Landscaping services
        if 'landscape' in service_lower or 'design' in service_lower:
            return 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.'
        elif 'hardscaping' in service_lower or 'patio' in service_lower:
            return 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.'
        elif 'lawn' in service_lower or 'maintenance' in service_lower:
            return 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'

        # PC repair services
        elif 'diagnostic' in service_lower or 'computer' in service_lower:
            return 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.'
        elif 'hardware' in service_lower or 'repair' in service_lower:
            return 'Professional hardware repair services for all types of computer components and peripherals.'
        elif 'software' in service_lower or 'solution' in service_lower:
            return 'Expert software installation, configuration, and troubleshooting for optimal system performance.'

        # Generic fallback
        else:
            return f'Professional {service_name.lower()} services tailored to your specific needs and requirements.'

    def generate_services_list_html(self, business_info: Dict[str, Any]) -> str:
        """Generate HTML list items for services"""
        services = self.get_dynamic_services(business_info)
        html_items = []
        for service_name in services.keys():
            html_items.append(f'<li>{service_name}</li>')
        return '\n                    '.join(html_items)

    def generate_services_schema(self, business_info: Dict[str, Any]) -> list:
        """Generate schema.org service offers"""
        services = self.get_dynamic_services(business_info)
        schema_items = []
        for service_name, service_desc in services.items():
            schema_items.append({
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": service_name,
                    "description": service_desc
                }
            })
        return schema_items

    def enhance_style_css(self, theme_dir: Path, business_info: Dict[str, Any]):
        """Add SEO-friendly CSS enhancements"""
        style_file = theme_dir / "style.css"

        if not style_file.exists():
            return

        content = style_file.read_text(encoding='utf-8')

        # Add SEO-friendly CSS
        seo_css = """
/* SEO-Friendly Styles */
.local-business-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.hero-section {
    text-align: center;
    padding: 3rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    margin-bottom: 2rem;
}

.services-section {
    margin: 2rem 0;
}

.services-section ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    list-style: none;
    padding: 0;
}

.services-section li {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #007cba;
}

.cta-button {
    display: inline-block;
    background: #007cba;
    color: white;
    padding: 1rem 2rem;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    margin-top: 1rem;
}

.cta-button:hover {
    background: #005a87;
}

.local-area {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    margin-top: 2rem;
}

/* Mobile-first responsive design */
@media (max-width: 768px) {
    .local-business-content {
        padding: 1rem;
    }

    .hero-section {
        padding: 2rem 1rem;
    }

    .services-section ul {
        grid-template-columns: 1fr;
    }
}
"""

        content += seo_css
        style_file.write_text(content, encoding='utf-8')

    def create_schema_markup(self, theme_dir: Path, business_info: Dict[str, Any]):
        """Create a separate schema markup file for advanced SEO"""
        schema_file = theme_dir / "schema.json"

        schema_data = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": business_info["business_name"],
            "description": f"Professional {business_info['service']} services in {business_info['city']}, {business_info['state']}",
            "url": "<?php echo home_url('/'); ?>",
            "telephone": business_info["phone"],
            "address": {
                "@type": "PostalAddress",
                "addressLocality": business_info["city"],
                "addressRegion": business_info["state"],
                "addressCountry": "US"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": "45.1611",
                "longitude": "-93.4758"
            },
            "openingHours": [
                "Mo-Fr 08:00-18:00",
                "Sa 09:00-15:00"
            ],
            "priceRange": "$$",
            "serviceArea": {
                "@type": "GeoCircle",
                "geoMidpoint": {
                    "@type": "GeoCoordinates",
                    "latitude": "45.1611",
                    "longitude": "-93.4758"
                },
                "geoRadius": "25000"
            },
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": f"{business_info['service']} Services",
                "itemListElement": self.generate_services_schema(business_info)
            }
        }

        schema_file.write_text(json.dumps(schema_data, indent=2), encoding='utf-8')
