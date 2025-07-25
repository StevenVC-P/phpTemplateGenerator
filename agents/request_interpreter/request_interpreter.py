# agents/request_interpreter/request_interpreter.py
import json
import re
from pathlib import Path

class RequestInterpreter:
    def __init__(self, config=None):
        if isinstance(config, dict):
            # Config passed as dict (from orchestrator)
            self.config = config
        elif isinstance(config, (str, Path)):
            # Config passed as file path
            self.config_path = Path(config)
            self.config = json.loads(self.config_path.read_text())
        else:
            # Default: load from file
            self.config_path = Path(__file__).parent / "request_interpreter.json"
            self.config = json.loads(self.config_path.read_text())

    def extract_section(self, markdown, header):
        pattern = rf"## {re.escape(header)}\n(.+?)(?=\n## |\Z)"
        match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def detect_site_type(self, markdown_text):
        """Detect if this is a single-page or multi-page request"""
        multi_page_indicators = [
            "multi-page", "multiple pages", "site architecture", "page hierarchy",
            "navigation structure", "primary navigation", "page specifications"
        ]

        for indicator in multi_page_indicators:
            if indicator.lower() in markdown_text.lower():
                return "multi_page"

        return "single_page"

    def parse_navigation_structure(self, markdown_text):
        """Extract navigation structure from multi-page requests"""
        nav_pattern = r"### Primary Navigation Structure\n```\n(.+?)\n```"
        match = re.search(nav_pattern, markdown_text, re.DOTALL)

        if match:
            nav_text = match.group(1).strip()
            # Parse navigation items (assuming format: "Home | Services | About | Contact")
            nav_items = [item.strip() for item in nav_text.split('|')]
            return nav_items

        return ["Home", "Services", "About", "Contact"]  # Default navigation

    def extract_business_info(self, markdown_text):
        """Extract structured business information from the markdown"""
        business_info = {
            "business_name": "",
            "business_type": "",
            "location": "",
            "phone": "",
            "email": "",
            "tagline": "",
            "services": [],
            "owner_name": "",
            "founding_year": "",
            "description": ""
        }

        # Extract business name (enhanced patterns for any business type)
        name_patterns = [
            # Pattern 1: **Business Name** with common business keywords
            r'\*\*([^*]+(?:Landscaping|PC Repair|Repair|Service|Company|Business|LLC|Inc|Restaurant|Cafe|Shop|Store|Clinic|Dental|Medical|Law|Legal|Consulting|Design|Construction|Plumbing|Electric|HVAC|Roofing|Cleaning|Catering|Photography|Marketing|Real Estate|Insurance|Financial|Accounting|Fitness|Gym|Salon|Spa|Veterinary|Pet|Auto|Automotive|Mechanic|Garage|Hardware|Garden|Nursery|Florist|Bakery|Deli|Bar|Grill|Pizza|Coffee|Hotel|Motel|Inn|Lodge|Resort|Travel|Tour|Transportation|Delivery|Moving|Storage|Contractor|Builder|Architect|Engineer|Realtor|Agent|Broker|Manager|Property|Rental|Bank|Investment|Tax|Bookkeeping|HR|Staffing|Training|Education|School|Academy|Tutor|Coach|Instructor|Counselor|Therapist|Dentist|Orthodontist|Optometrist|Chiropractor|Massage|Wellness|Health|Hospital|Care|Security|Guard|Alarm|Jewelry|Watch|Electronics|Computer|IT|Tech|Software|Hardware|Network|Internet|Web|Digital|Online|Marketing|Advertising|Media|Entertainment|Event|Party|Wedding|Floral|Equipment|Tool|Supply|Material|Lumber|Steel|Metal|Glass|Plastic|Paint|Roofing|Siding|Window|Door|Floor|Carpet|Tile|Stone|Brick|Concrete|Paving|Fence|Deck|Patio|Pool|Spa|Landscape|Lawn|Tree|Plant|Irrigation|Plumbing|Electrical|Energy|Solar|Utility|Gas|Oil|Green|Eco|Organic|Natural|Professional|Expert|Master|Certified|Licensed|Commercial|Residential|Local|Regional|National|Community|Family)[^*]*)\*\*',
            # Pattern 2: **Any Business Name** (flexible - captures any bold text that looks like a business name)
            r'\*\*([A-Z][A-Za-z\s&\'-]{2,50})\*\*',
            # Pattern 3: "for **Business Name**"
            r'for\s+\*\*([^*]+)\*\*',
            # Pattern 4: "website for Business Name"
            r'website\s+for\s+([A-Z][A-Za-z\s&\'-]{2,50})(?:,|\.|$)',
            # Pattern 5: "Create a ... for Business Name"
            r'Create\s+a[^.]*?for\s+([A-Z][A-Za-z\s&\'-]{2,50})(?:,|\.|$)',
            # Pattern 6: Business name after "for" in description
            r'(?:Create|Build|Design|Develop)[^.]*?for\s+([A-Z][A-Za-z\s&\'-]{2,50})(?:,|\.|$)',
            # Pattern 7: Business name in title/heading
            r'#[^#\n]*?([A-Z][A-Za-z\s&\'-]{2,50})(?:\s*#|\s*$)',
        ]

        for pattern in name_patterns:
            match = re.search(pattern, markdown_text, re.IGNORECASE)
            if match:
                business_info["business_name"] = match.group(1).strip()
                break

        # Extract location (city, state patterns)
        location_patterns = [
            r'in\s+\*\*([A-Za-z\s]+,\s*[A-Za-z\s]+)\*\*',  # **Ramsey, Minnesota**
            r'in\s+([A-Za-z\s]+,\s*[A-Za-z\s]+)',
            r'located\s+in\s+([A-Za-z\s]+,\s*[A-Za-z\s]+)',
            r'serving\s+([A-Za-z\s]+,\s*[A-Za-z\s]+)',
            r'business\s+in\s+([A-Za-z\s]+,\s*[A-Za-z\s]+)',
            r'([A-Za-z\s]+,\s*[A-Za-z\s]+)\s+community'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, markdown_text, re.IGNORECASE)
            if match:
                business_info["location"] = match.group(1).strip()
                break

        # Extract business type from context (enhanced for multiple business types)
        business_type_patterns = [
            (r'Landscaping|Landscape|Lawn|Garden|Yard|Tree|Plant|Irrigation|Hardscape|Patio|Outdoor', "Landscaping"),
            (r'PC\s+Repair|Computer\s+Repair|Tech\s+Support|IT\s+Service', "PC Repair"),
            (r'Restaurant|Food|Dining|Cafe|Bar|Grill|Pizza|Coffee|Bakery|Catering', "Restaurant"),
            (r'Law|Legal|Attorney|Lawyer|Paralegal', "Legal Services"),
            (r'Medical|Health|Doctor|Dental|Clinic|Healthcare|Therapy|Wellness', "Healthcare"),
            (r'Real\s+Estate|Realtor|Property|Rental|Mortgage|Investment', "Real Estate"),
            (r'Construction|Contractor|Builder|Roofing|Plumbing|Electric|HVAC', "Construction"),
            (r'Auto|Automotive|Mechanic|Garage|Car\s+Repair|Vehicle', "Automotive"),
            (r'Cleaning|Janitorial|Maid|Housekeeping|Carpet\s+Cleaning', "Cleaning Services"),
            (r'Photography|Photo|Wedding|Event|Portrait|Commercial', "Photography"),
            (r'Marketing|Advertising|Digital|SEO|Social\s+Media|Branding', "Marketing"),
            (r'Insurance|Financial|Accounting|Tax|Bookkeeping|CPA', "Financial Services"),
            (r'Fitness|Gym|Personal\s+Training|Yoga|Pilates|Wellness', "Fitness"),
            (r'Salon|Spa|Beauty|Hair|Nail|Massage|Skincare', "Beauty & Wellness"),
            (r'Pet|Veterinary|Animal|Dog|Cat|Grooming|Boarding', "Pet Services"),
            (r'Education|School|Tutoring|Training|Academy|Learning', "Education"),
            (r'Travel|Tour|Hotel|Resort|Transportation|Vacation', "Travel & Hospitality"),
            (r'Consulting|Business\s+Services|Professional\s+Services', "Consulting"),
        ]

        business_info["business_type"] = "Service Business"  # Default

        for pattern, business_type in business_type_patterns:
            if re.search(pattern, markdown_text, re.IGNORECASE):
                business_info["business_type"] = business_type
                break

        # Extract phone number (multiple formats)
        phone_patterns = [
            r'(\(\d{3}\)\s*\d{3}-\d{4})',  # (555) 123-4567
            r'(\d{3}-\d{3}-\d{4})',        # 555-123-4567
            r'(\d{3}\.\d{3}\.\d{4})',      # 555.123.4567
            r'(\d{3}\s+\d{3}\s+\d{4})',    # 555 123 4567
            r'(\+1\s*\d{3}\s*\d{3}\s*\d{4})'  # +1 555 123 4567
        ]

        for pattern in phone_patterns:
            phone_match = re.search(pattern, markdown_text)
            if phone_match:
                business_info["phone"] = phone_match.group(1)
                break

        # Extract email
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', markdown_text)
        if email_match:
            business_info["email"] = email_match.group(1)

        # Extract business description from project description
        desc_match = re.search(r'Create\s+a\s+[^.]*?\s+for\s+[^.]*?\.\s+([^.]+\.)', markdown_text, re.IGNORECASE)
        if desc_match:
            business_info["description"] = desc_match.group(1).strip()

        # Generate tagline based on business type and location
        if business_info["business_type"] and business_info["location"]:
            business_info["tagline"] = f"{business_info['business_type']} in {business_info['location']}"

        # Extract services from multiple sources
        business_info["services"] = self.extract_services_from_content(markdown_text, business_info["business_type"])

        return business_info

    def extract_services_from_content(self, markdown_text: str, business_type: str) -> list:
        """Extract services from various sections of the markdown content"""
        services = []

        # Method 1: Extract from page hierarchy (like Northern Roots)
        hierarchy_match = re.search(r'### Page Hierarchy.*?```(.*?)```', markdown_text, re.DOTALL | re.IGNORECASE)
        if hierarchy_match:
            hierarchy_content = hierarchy_match.group(1)
            # Look for service-related entries in hierarchy
            service_lines = re.findall(r'├──\s*([^(]+)\s*\(', hierarchy_content)
            service_lines.extend(re.findall(r'│\s*├──\s*([^(]+)\s*\(', hierarchy_content))
            service_lines.extend(re.findall(r'│\s*└──\s*([^(]+)\s*\(', hierarchy_content))

            for service in service_lines:
                service_name = service.strip()
                if len(service_name) > 3 and service_name not in ['Home', 'About', 'Contact', 'Blog', 'Portfolio']:
                    services.append(service_name)

        # Method 2: Extract from Services page content sections
        services_page_match = re.search(r'### 🌿 \*\*Services Page\*\*.*?### 👤', markdown_text, re.DOTALL | re.IGNORECASE)
        if not services_page_match:
            services_page_match = re.search(r'### \*\*Services.*?Page\*\*.*?(?=### \*\*[^S]|$)', markdown_text, re.DOTALL | re.IGNORECASE)

        if services_page_match:
            services_content = services_page_match.group(0)
            # Look for service descriptions or mentions
            service_mentions = re.findall(r'[-•]\s*([^:\n]+(?:service|care|design|maintenance|repair|installation)[^:\n]*)', services_content, re.IGNORECASE)
            for service in service_mentions:
                service_name = service.strip()
                if len(service_name) > 5:
                    services.append(service_name)

        # Method 3: Extract from explicit services sections
        services_section = self.extract_section(markdown_text, "Services")
        if services_section:
            service_matches = re.findall(r'[-*•]\s*([^\n]+)', services_section)
            for service in service_matches:
                service_name = service.strip()
                if len(service_name) > 3:
                    services.append(service_name)

        # Method 4: Generate default services based on business type if none found
        if not services and business_type:
            services = self.generate_default_services(business_type)

        # Clean up and deduplicate services
        cleaned_services = []
        for service in services[:6]:  # Limit to 6 services
            service = service.strip()
            if service and service not in cleaned_services:
                cleaned_services.append(service)

        return cleaned_services

    def generate_default_services(self, business_type: str) -> list:
        """Generate appropriate default services based on business type"""
        business_type_lower = business_type.lower()

        if 'landscaping' in business_type_lower or 'landscape' in business_type_lower:
            return [
                "Landscape Design",
                "Hardscaping & Patios",
                "Lawn Maintenance",
                "Tree & Plant Care",
                "Irrigation Systems",
                "Seasonal Cleanup"
            ]
        elif 'pc' in business_type_lower or 'computer' in business_type_lower or 'repair' in business_type_lower:
            return [
                "Computer Diagnostics",
                "Hardware Repair",
                "Software Solutions",
                "Virus Removal",
                "Data Recovery",
                "System Optimization"
            ]
        elif 'restaurant' in business_type_lower or 'food' in business_type_lower:
            return [
                "Dine-In Service",
                "Takeout Orders",
                "Catering Services",
                "Private Events",
                "Delivery Service",
                "Special Occasions"
            ]
        else:
            return [
                "Professional Consultation",
                "Custom Solutions",
                "Expert Support",
                "Quality Service",
                "Reliable Results",
                "Customer Satisfaction"
            ]

    def extract_color_palette(self, markdown_text: str) -> dict:
        """Extract specific color palette from markdown text"""
        color_palette = {}

        # Look for color palette section
        color_section_match = re.search(r'###?\s*Color\s*Palette.*?(?=###|$)', markdown_text, re.IGNORECASE | re.DOTALL)

        if color_section_match:
            color_section = color_section_match.group(0)
            print(f"🎨 Found color palette section: {color_section[:100]}...")

            # Extract hex colors with their descriptions
            hex_color_patterns = [
                # Pattern: **Color Name (#HEXCODE)** – description
                r'\*\*([^*]+)\s*\(#([0-9A-Fa-f]{6})\)\*\*[^\n]*?–\s*([^\n]+)',
                # Pattern: **Color Name (#HEXCODE)** - description
                r'\*\*([^*]+)\s*\(#([0-9A-Fa-f]{6})\)\*\*[^\n]*?-\s*([^\n]+)',
                # Pattern: - **Color Name (#HEXCODE)** – description
                r'-\s*\*\*([^*]+)\s*\(#([0-9A-Fa-f]{6})\)\*\*[^\n]*?–\s*([^\n]+)',
                # Pattern: - **Color Name (#HEXCODE)** - description
                r'-\s*\*\*([^*]+)\s*\(#([0-9A-Fa-f]{6})\)\*\*[^\n]*?-\s*([^\n]+)',
                # Pattern: Color Name (#HEXCODE) – description
                r'([A-Z][^(#\n]+)\s*\(#([0-9A-Fa-f]{6})\)[^\n]*?–\s*([^\n]+)',
                # Pattern: Color Name (#HEXCODE) - description
                r'([A-Z][^(#\n]+)\s*\(#([0-9A-Fa-f]{6})\)[^\n]*?-\s*([^\n]+)'
            ]

            colors_found = []
            for pattern in hex_color_patterns:
                matches = re.findall(pattern, color_section)
                for match in matches:
                    color_name = match[0].strip()
                    hex_code = f"#{match[1].upper()}"
                    description = match[2].strip()

                    colors_found.append({
                        "name": color_name,
                        "hex": hex_code,
                        "description": description
                    })
                    print(f"   🎨 Extracted: {color_name} = {hex_code} ({description})")

            if colors_found:
                color_palette["specified_colors"] = colors_found
                color_palette["has_custom_palette"] = True

                # Map colors to common roles based on descriptions
                color_palette["mapped_colors"] = self.map_colors_to_roles(colors_found)
            else:
                print("⚠️ Color palette section found but no hex colors extracted")
        else:
            print("ℹ️ No color palette section found in markdown")

        return color_palette

    def map_colors_to_roles(self, colors_found: list) -> dict:
        """Map extracted colors to common design roles"""
        mapped = {}

        for color in colors_found:
            name_lower = color["name"].lower()
            desc_lower = color["description"].lower()

            print(f"   🔍 Mapping {color['name']} ({color['hex']}): {color['description']}")

            # Map to primary color (buttons, accents, callouts)
            if any(keyword in desc_lower for keyword in ["button", "accent", "callout"]):
                mapped["primary"] = color["hex"]
                print(f"      → Mapped to PRIMARY (buttons/accents)")

            # Map to secondary color (highlights, icons, hover effects)
            elif any(keyword in desc_lower for keyword in ["highlight", "icon", "hover"]):
                mapped["secondary"] = color["hex"]
                print(f"      → Mapped to SECONDARY (highlights/icons)")

            # Map to background color (main background)
            elif any(keyword in desc_lower for keyword in ["background", "main background"]):
                mapped["background"] = color["hex"]
                print(f"      → Mapped to BACKGROUND")

            # Map to text color (headers, important text)
            elif any(keyword in desc_lower for keyword in ["text", "header", "important text"]):
                mapped["text"] = color["hex"]
                print(f"      → Mapped to TEXT")

            # Map to accent color (footer, secondary elements)
            elif any(keyword in desc_lower for keyword in ["footer", "secondary element"]):
                mapped["accent"] = color["hex"]
                print(f"      → Mapped to ACCENT (footer/secondary)")
            else:
                print(f"      → No specific mapping found")

        print(f"   🎨 Final color mapping: {mapped}")
        return mapped

    def extract_color_palette_with_fallback(self, markdown_text: str, business_info: dict) -> dict:
        """Extract color palette with intelligent fallback based on business type and theme preference"""

        # First try to extract explicit colors from markdown
        explicit_colors = self.extract_color_palette(markdown_text)

        # If we found explicit colors, use them
        if explicit_colors and any(color for color in explicit_colors.values() if color):
            print("🎨 Using EXPLICIT colors from markdown")
            return explicit_colors

        # No explicit colors found - use intelligent fallback
        print("🎨 No explicit colors found - using INTELLIGENT FALLBACK")

        # Analyze the request for theme preferences
        theme_preference = self.detect_theme_preference(markdown_text)
        business_type = business_info.get("business_type", "").lower()
        business_name = business_info.get("business_name", "").lower()

        print(f"   🎨 Theme preference: {theme_preference}")
        print(f"   🎨 Business type: {business_type}")
        print(f"   🎨 Business name: {business_name}")

        # Smart color selection based on business type and theme
        fallback_colors = self.get_smart_color_palette(business_type, business_name, theme_preference)

        print(f"   🎨 Selected fallback palette: {fallback_colors}")
        return fallback_colors

    def detect_theme_preference(self, markdown_text: str) -> str:
        """Detect if the user wants a light, dark, or neutral theme"""
        text_lower = markdown_text.lower()

        # Dark theme indicators
        dark_indicators = [
            'dark-themed', 'dark theme', 'dark design', 'dark color',
            'modern dark', 'sleek dark', 'professional dark',
            'black', 'charcoal', 'midnight', 'slate'
        ]

        # Light theme indicators
        light_indicators = [
            'light-themed', 'light theme', 'light design', 'light color',
            'bright', 'clean light', 'fresh', 'airy',
            'white', 'cream', 'beige', 'soft'
        ]

        # Count indicators
        dark_score = sum(1 for indicator in dark_indicators if indicator in text_lower)
        light_score = sum(1 for indicator in light_indicators if indicator in text_lower)

        if dark_score > light_score:
            return "dark"
        elif light_score > dark_score:
            return "light"
        else:
            return "neutral"

    def get_smart_color_palette(self, business_type: str, business_name: str, theme_preference: str) -> dict:
        """Generate intelligent color palette based on business context"""

        # Business type color associations
        business_color_map = {
            # Tech/Computer businesses
            'pc repair': {'primary': '#2563EB', 'secondary': '#60A5FA', 'accent': '#1E40AF'},
            'computer': {'primary': '#2563EB', 'secondary': '#60A5FA', 'accent': '#1E40AF'},
            'tech': {'primary': '#2563EB', 'secondary': '#60A5FA', 'accent': '#1E40AF'},
            'it': {'primary': '#2563EB', 'secondary': '#60A5FA', 'accent': '#1E40AF'},

            # Landscaping/Nature businesses
            'landscaping': {'primary': '#3B6A4D', 'secondary': '#9CAF88', 'accent': '#A68C6D'},
            'lawn': {'primary': '#22C55E', 'secondary': '#86EFAC', 'accent': '#15803D'},
            'garden': {'primary': '#22C55E', 'secondary': '#86EFAC', 'accent': '#15803D'},

            # Medical/Health businesses
            'medical': {'primary': '#0EA5E9', 'secondary': '#7DD3FC', 'accent': '#0284C7'},
            'dental': {'primary': '#0EA5E9', 'secondary': '#7DD3FC', 'accent': '#0284C7'},
            'health': {'primary': '#0EA5E9', 'secondary': '#7DD3FC', 'accent': '#0284C7'},

            # Legal/Professional services
            'legal': {'primary': '#1F2937', 'secondary': '#6B7280', 'accent': '#374151'},
            'law': {'primary': '#1F2937', 'secondary': '#6B7280', 'accent': '#374151'},
            'consulting': {'primary': '#1F2937', 'secondary': '#6B7280', 'accent': '#374151'},

            # Food/Restaurant businesses
            'restaurant': {'primary': '#DC2626', 'secondary': '#FCA5A5', 'accent': '#B91C1C'},
            'cafe': {'primary': '#92400E', 'secondary': '#FCD34D', 'accent': '#78350F'},
            'food': {'primary': '#DC2626', 'secondary': '#FCA5A5', 'accent': '#B91C1C'},
        }

        # Find matching business type
        matched_colors = None
        for biz_type, colors in business_color_map.items():
            if biz_type in business_type or biz_type in business_name:
                matched_colors = colors
                break

        # Default colors if no match
        if not matched_colors:
            if theme_preference == "dark":
                matched_colors = {'primary': '#3B82F6', 'secondary': '#60A5FA', 'accent': '#1E40AF'}
            else:
                matched_colors = {'primary': '#059669', 'secondary': '#34D399', 'accent': '#047857'}

        # Theme-specific adjustments
        if theme_preference == "dark":
            return {
                'primary': matched_colors['primary'],
                'secondary': matched_colors['secondary'],
                'background': '#0F172A',  # Dark background
                'text': '#F8FAFC',        # Light text
                'accent': matched_colors['accent']
            }
        elif theme_preference == "light":
            return {
                'primary': matched_colors['primary'],
                'secondary': matched_colors['secondary'],
                'background': '#F8FAFC',  # Light background
                'text': '#1F2937',       # Dark text
                'accent': matched_colors['accent']
            }
        else:  # neutral
            return {
                'primary': matched_colors['primary'],
                'secondary': matched_colors['secondary'],
                'background': '#FFFFFF',  # White background
                'text': '#374151',       # Medium gray text
                'accent': matched_colors['accent']
            }

    def parse_page_hierarchy(self, markdown_text):
        """Extract page hierarchy from multi-page requests"""
        hierarchy_pattern = r"### Page Hierarchy\n```\n(.+?)\n```"
        match = re.search(hierarchy_pattern, markdown_text, re.DOTALL)

        if match:
            hierarchy_text = match.group(1).strip()
            # Parse the tree structure
            pages = []
            for line in hierarchy_text.split('\n'):
                if '├──' in line or '└──' in line:
                    # Extract page name and template file
                    page_match = re.search(r'[├└]── (.+?) \((.+?)\)', line)
                    if page_match:
                        page_name = page_match.group(1).strip()
                        template_file = page_match.group(2).strip()
                        pages.append({
                            "name": page_name,
                            "template": template_file,
                            "level": 0 if '├──' in line else 1
                        })
            return pages

        return []

    def parse_page_specifications(self, markdown_text):
        """Extract individual page specifications from multi-page requests"""
        page_specs = []

        # Pattern to match page specification sections
        page_pattern = r"### 📄 \*\*(.+?)\*\* \((.+?)\)\n\*\*Purpose\*\*: (.+?)\n(.+?)(?=### 📄|\n## |$)"
        matches = re.finditer(page_pattern, markdown_text, re.DOTALL)

        for match in matches:
            page_name = match.group(1).strip()
            template_file = match.group(2).strip()
            purpose = match.group(3).strip()
            content = match.group(4).strip()

            # Extract CTAs from the content
            cta_pattern = r"\*\*Call-to-Actions\*\*:\n(.+?)(?=\n\*\*|$)"
            cta_match = re.search(cta_pattern, content, re.DOTALL)
            ctas = []
            if cta_match:
                cta_text = cta_match.group(1).strip()
                for line in cta_text.split('\n'):
                    if line.strip().startswith('- Primary:') or line.strip().startswith('- Secondary:'):
                        cta_info = line.strip().split(':', 1)
                        if len(cta_info) == 2:
                            cta_type = cta_info[0].replace('- ', '').strip()
                            cta_content = cta_info[1].strip()
                            ctas.append({"type": cta_type, "content": cta_content})

            # Extract content sections
            sections_pattern = r"\*\*Content Sections\*\*:\n(.+?)(?=\n\*\*|$)"
            sections_match = re.search(sections_pattern, content, re.DOTALL)
            sections = []
            if sections_match:
                sections_text = sections_match.group(1).strip()
                for line in sections_text.split('\n'):
                    if line.strip().startswith('- '):
                        sections.append(line.strip()[2:])

            page_specs.append({
                "name": page_name,
                "template": template_file,
                "purpose": purpose,
                "sections": sections,
                "ctas": ctas
            })

        return page_specs

    def parse_request_markdown(self, markdown_text):
        # Debug: check what we received
        print(f"🔍 parse_request_markdown called with:")
        print(f"   markdown_text: {type(markdown_text)} - {str(markdown_text)[:100]}...")

        # Detect site type
        site_type = self.detect_site_type(markdown_text)
        print(f"🔍 Detected site type: {site_type}")

        # Extract business information
        business_info = self.extract_business_info(markdown_text)

        required_sections = self.config.get("input_format", {}).get("required_sections", [])
        optional_sections = self.config.get("input_format", {}).get("optional_sections", [])

        # Parse location from business info
        location_parts = business_info["location"].split(",") if business_info["location"] else ["", ""]
        city = location_parts[0].strip() if len(location_parts) > 0 else "Your City"
        state = location_parts[1].strip() if len(location_parts) > 1 else "Your State"

        # Extract color palette with intelligent fallback
        color_palette = self.extract_color_palette_with_fallback(markdown_text, business_info)

        # Base spec structure with dynamic business information
        spec = {
            "template_id": "template_001",
            "project_type": "local_service_page" if site_type == "single_page" else "multi_page_website",
            "site_type": site_type,
            "status": "parsed_from_request",
            "business_info": business_info,
            "color_palette": color_palette,
            "location": {
                "city": city,
                "state": state,
                "region": f"{city} Metro" if city != "Your City" else "Local Area"
            },
            "responsive": True,
            "framework": "none",
            "audience": ["local_customers"],
            "layout_style": site_type,
            "primary_cta": "Get Quote" if business_info["business_type"] == "Service Business" else "Call Now",
            "technical_notes": {
                "language": "PHP",
                "css": "manual_or_flexbox",
                "js": "minimal"
            }
        }

        if site_type == "multi_page":
            # Parse multi-page specific elements
            spec["navigation"] = {
                "primary": self.parse_navigation_structure(markdown_text),
                "structure": "horizontal_with_dropdowns",
                "mobile_behavior": "hamburger_menu",
                "sticky": True
            }
            spec["page_hierarchy"] = self.parse_page_hierarchy(markdown_text)
            spec["page_specifications"] = self.parse_page_specifications(markdown_text)
            spec["sections"] = []  # Will be populated per page

            # Extract required WordPress template files
            template_files = []
            for page_spec in spec["page_specifications"]:
                if page_spec["template"] not in template_files:
                    template_files.append(page_spec["template"])
            spec["required_templates"] = template_files

        else:
            # Single page structure (existing logic)
            spec["sections"] = ["hero", "services", "about", "testimonials", "contact"]

        # Extract common sections regardless of site type
        for section in required_sections + optional_sections:
            content = self.extract_section(markdown_text, section.replace("_", " ").title())
            if content:
                spec[section] = content

        return spec

    def validate_spec(self, spec):
        required_fields = self.config.get("validation_rules", {}).get("required_fields", [])
        missing = [field for field in required_fields if field not in spec]
        if missing:
            print(f"⚠️  Warning: Missing required fields in spec: {', '.join(missing)}")

    async def run(self, input_file: str, pipeline_id: str):
        """Standard agent interface for orchestrator"""
        from dataclasses import dataclass
        from typing import Dict
        from datetime import datetime

        @dataclass
        class AgentResult:
            agent_id: str
            success: bool
            output_file: str = ""
            error_message: str = ""
            execution_time: float = 0.0
            metadata: Dict = None

        try:
            # Debug: print what we received
            print(f"🔍 request_interpreter.run called with:")
            print(f"   input_file: {input_file} (type: {type(input_file)})")
            print(f"   pipeline_id: {pipeline_id} (type: {type(pipeline_id)})")

            # Convert input_file to Path object
            input_path = Path(input_file)

            # Generate output path using pipeline_id for consistency
            template_id = pipeline_id.replace('pipeline_', '')
            output_path = Path(f"template_generations/template_{template_id}/specs/template_spec.json")

            # Check if input file exists
            if not input_path.exists():
                return AgentResult(
                    agent_id="request_interpreter",
                    success=False,
                    error_message=f"Input file not found: {input_path}"
                )

            # Read and process the markdown file
            markdown = input_path.read_text(encoding='utf-8')
            structured = self.parse_request_markdown(markdown)
            self.validate_spec(structured)

            # Create output directory and write spec file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(structured, indent=2), encoding='utf-8')

            print(f"✅ Spec written to {output_path}")

            return AgentResult(
                agent_id="request_interpreter",
                success=True,
                output_file=str(output_path),
                metadata={"template_id": structured.get("template_id")}
            )

        except Exception as e:
            return AgentResult(
                agent_id="request_interpreter",
                success=False,
                error_message=str(e)
            )

    def run_old(self, input_path: str, output_path: str) -> bool:
        """Legacy method for backward compatibility"""
        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.exists():
            print(f"❌ Input file not found: {input_path}")
            return False

        markdown = input_path.read_text()
        structured = self.parse_request_markdown(markdown)
        self.validate_spec(structured)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(structured, indent=2))

        print(f"✅ Spec written to {output_path}")
        return True
