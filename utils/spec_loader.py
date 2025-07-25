"""
Shared Helper Module for Dynamic Spec Loading
Provides centralized functions for loading services, colors, CTA text, phone numbers, and other business data
from template_spec.json files or WordPress options.

This module can be reused across all agents and WordPress components to ensure consistency.
"""

import json
import glob
from pathlib import Path
from typing import Dict, List, Optional, Any


class SpecLoader:
    """Central helper class for loading business specifications from various sources"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize SpecLoader
        
        Args:
            template_dir: Optional path to template directory containing specs folder
        """
        self.template_dir = template_dir
        self._cached_spec = None
    
    def load_spec_data(self, spec_file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load spec data from template_spec.json
        
        Args:
            spec_file_path: Optional direct path to spec file
            
        Returns:
            Dict containing spec data or empty dict if not found
        """
        if self._cached_spec:
            return self._cached_spec
            
        spec_data = {}
        
        try:
            # Try direct path first
            if spec_file_path and Path(spec_file_path).exists():
                with open(spec_file_path, 'r', encoding='utf-8') as f:
                    spec_data = json.load(f)
                    print(f"📋 Loaded spec from direct path: {spec_file_path}")
            
            # Try template directory
            elif self.template_dir:
                spec_file = Path(self.template_dir) / "specs" / "template_spec.json"
                if spec_file.exists():
                    with open(spec_file, 'r', encoding='utf-8') as f:
                        spec_data = json.load(f)
                        print(f"📋 Loaded spec from template dir: {spec_file}")
            
            # Try to find latest spec file in template_generations
            else:
                spec_files = glob.glob("template_generations/*/specs/template_spec.json")
                if spec_files:
                    latest_spec = max(spec_files, key=lambda x: Path(x).stat().st_mtime)
                    with open(latest_spec, 'r', encoding='utf-8') as f:
                        spec_data = json.load(f)
                        print(f"📋 Loaded latest spec: {latest_spec}")
                        
        except Exception as e:
            print(f"⚠️ Could not load spec data: {e}")
            
        self._cached_spec = spec_data
        return spec_data
    
    def get_business_info(self, spec_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Get business information from spec data"""
        if not spec_data:
            spec_data = self.load_spec_data()
            
        return spec_data.get("business_info", {})
    
    def get_services(self, spec_data: Optional[Dict] = None) -> Dict[str, str]:
        """
        Get services with descriptions from spec data
        
        Returns:
            Dict mapping service names to descriptions
        """
        if not spec_data:
            spec_data = self.load_spec_data()
            
        business_info = self.get_business_info(spec_data)
        services = {}
        
        if "services" in business_info:
            services_list = business_info["services"]
            for service_name in services_list:
                if service_name.lower() != 'services':  # Skip generic "Services" entry
                    services[service_name] = self.generate_service_description(service_name, business_info)
        
        # Fallback to business type-based services
        if not services:
            business_type = business_info.get("business_type", "Service Business")
            services = self.get_fallback_services(business_type)
            print(f"⚠️ Using fallback services for business type: {business_type}")
        
        return services
    
    def get_colors(self, spec_data: Optional[Dict] = None) -> Dict[str, str]:
        """
        Get color palette from spec data
        
        Returns:
            Dict mapping color roles to hex codes
        """
        if not spec_data:
            spec_data = self.load_spec_data()
            
        color_palette = spec_data.get("color_palette", {})
        
        # Try mapped colors first
        if "mapped_colors" in color_palette:
            print("🎨 Using mapped colors from spec")
            return color_palette["mapped_colors"]
        
        # Try specified colors
        elif "specified_colors" in color_palette:
            colors = {}
            for color_spec in color_palette["specified_colors"]:
                if "usage" in color_spec and "hex_code" in color_spec:
                    usage = color_spec["usage"].lower()
                    if "button" in usage or "accent" in usage:
                        colors["primary"] = color_spec["hex_code"]
                    elif "highlight" in usage or "icon" in usage:
                        colors["secondary"] = color_spec["hex_code"]
                    elif "background" in usage:
                        colors["background"] = color_spec["hex_code"]
                    elif "text" in usage or "header" in usage:
                        colors["text"] = color_spec["hex_code"]
                    elif "footer" in usage or "secondary" in usage:
                        colors["accent"] = color_spec["hex_code"]
            
            if colors:
                print("🎨 Using specified colors from spec")
                return colors
        
        # Fallback to business type colors
        business_info = self.get_business_info(spec_data)
        business_type = business_info.get("business_type", "Service Business")
        colors = self.get_fallback_colors(business_type)
        print(f"⚠️ Using fallback colors for business type: {business_type}")
        
        return colors
    
    def get_contact_info(self, spec_data: Optional[Dict] = None) -> Dict[str, str]:
        """Get contact information from spec data"""
        if not spec_data:
            spec_data = self.load_spec_data()
            
        business_info = self.get_business_info(spec_data)
        
        return {
            "phone": business_info.get("phone", ""),
            "email": business_info.get("email", ""),
            "address": business_info.get("address", ""),
            "business_name": business_info.get("business_name", ""),
            "business_type": business_info.get("business_type", "Service Business")
        }
    
    def get_cta_text(self, service_name: str, context: str = "default") -> str:
        """
        Generate appropriate CTA text based on service name and context
        
        Args:
            service_name: Name of the service
            context: Context like 'button', 'link', 'phone'
            
        Returns:
            Appropriate CTA text
        """
        service_lower = service_name.lower()
        
        if context == "phone":
            if "emergency" in service_lower or "urgent" in service_lower:
                return "Call Now"
            elif "consultation" in service_lower:
                return "Schedule Call"
            else:
                return "Call Today"
        
        # Default button/link context
        if "design" in service_lower:
            return "Get Design Quote"
        elif "maintenance" in service_lower:
            return "Schedule Service"
        elif "recovery" in service_lower or "repair" in service_lower:
            return "Get Help Now"
        elif "consultation" in service_lower:
            return "Book Consultation"
        elif "installation" in service_lower:
            return "Get Installed"
        
        return "Get Started"
    
    def generate_service_description(self, service_name: str, business_info: Dict = None) -> str:
        """Generate appropriate description for a service based on its name and business context"""
        service_lower = service_name.lower()
        business_type = business_info.get("business_type", "") if business_info else ""
        business_type_lower = business_type.lower()
        
        # Landscaping services
        if "landscape" in service_lower or "design" in service_lower:
            return "Professional landscape design services to transform your outdoor space into a beautiful and functional environment."
        elif "hardscaping" in service_lower or "patio" in service_lower:
            return "Expert hardscaping and patio installation to create stunning outdoor living areas for your home."
        elif "lawn" in service_lower or "maintenance" in service_lower:
            return "Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round."
        
        # PC repair services
        elif "virus" in service_lower or "malware" in service_lower:
            return "Complete virus and malware removal to keep your computer safe and running smoothly."
        elif "hardware" in service_lower and "repair" in service_lower:
            return "Professional hardware diagnosis, repair, and upgrade services for optimal performance."
        elif "data" in service_lower and "recovery" in service_lower:
            return "Recover lost data and set up reliable backup solutions to protect your important files."
        
        # Generic descriptions based on business type
        elif "landscaping" in business_type_lower:
            return f"Professional {service_name.lower()} services to enhance and maintain your outdoor spaces."
        elif "repair" in business_type_lower or "pc" in business_type_lower:
            return f"Expert {service_name.lower()} services to keep your technology running smoothly."
        
        # Generic fallback
        return f"Professional {service_name.lower()} services delivered with expertise, attention to detail, and a commitment to customer satisfaction."
    
    def get_fallback_services(self, business_type: str) -> Dict[str, str]:
        """Get fallback services based on business type"""
        business_lower = business_type.lower()
        
        if "landscaping" in business_lower or "landscape" in business_lower:
            return {
                "Landscape Design": "Professional landscape design services to transform your outdoor space.",
                "Hardscaping & Patios": "Expert hardscaping and patio installation for outdoor living areas.",
                "Lawn Maintenance": "Comprehensive lawn care and maintenance services year-round."
            }
        elif "repair" in business_lower or "pc" in business_lower:
            return {
                "Computer Diagnostics": "Comprehensive computer diagnostics to identify and resolve issues.",
                "Hardware Repair": "Professional hardware repair services for all computer components.",
                "Software Solutions": "Expert software installation and troubleshooting services."
            }
        
        return {
            "Professional Consultation": "Expert consultation services tailored to your specific needs.",
            "Custom Solutions": "Personalized solutions designed to address your unique challenges.",
            "Professional Support": "Reliable ongoing support to ensure continued success."
        }
    
    def get_fallback_colors(self, business_type: str) -> Dict[str, str]:
        """Get fallback colors based on business type"""
        business_lower = business_type.lower()
        
        # Business-specific color palettes
        color_palettes = {
            "landscaping": {"primary": "#22c55e", "secondary": "#16a34a", "accent": "#84cc16", "background": "#ffffff", "text": "#1f2937"},
            "pc repair": {"primary": "#3b82f6", "secondary": "#1d4ed8", "accent": "#06b6d4", "background": "#ffffff", "text": "#1f2937"},
            "restaurant": {"primary": "#dc2626", "secondary": "#b91c1c", "accent": "#f59e0b", "background": "#ffffff", "text": "#1f2937"},
            "construction": {"primary": "#ea580c", "secondary": "#c2410c", "accent": "#eab308", "background": "#ffffff", "text": "#1f2937"},
            "automotive": {"primary": "#dc2626", "secondary": "#991b1b", "accent": "#6b7280", "background": "#ffffff", "text": "#1f2937"},
        }
        
        # Find matching palette
        for key, palette in color_palettes.items():
            if key in business_lower:
                return palette
        
        # Default palette
        return {
            "primary": "#2563eb", "secondary": "#1d4ed8", "accent": "#f59e0b",
            "background": "#ffffff", "text": "#1f2937"
        }


# Convenience functions for backward compatibility
def load_business_info(template_dir: Optional[str] = None) -> Dict[str, Any]:
    """Load business info from spec file"""
    loader = SpecLoader(template_dir)
    return loader.get_business_info()

def load_services(template_dir: Optional[str] = None) -> Dict[str, str]:
    """Load services from spec file"""
    loader = SpecLoader(template_dir)
    return loader.get_services()

def load_colors(template_dir: Optional[str] = None) -> Dict[str, str]:
    """Load colors from spec file"""
    loader = SpecLoader(template_dir)
    return loader.get_colors()

def load_contact_info(template_dir: Optional[str] = None) -> Dict[str, str]:
    """Load contact info from spec file"""
    loader = SpecLoader(template_dir)
    return loader.get_contact_info()
