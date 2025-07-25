<?php
/**
 * Shared Helper Module for Dynamic Spec Loading (PHP Version)
 * Provides centralized functions for loading services, colors, CTA text, phone numbers, and other business data
 * from template_spec.json files or WordPress options.
 * 
 * This module can be reused across all WordPress components to ensure consistency.
 */

class SpecLoader {
    private $template_dir;
    private $cached_spec = null;
    
    public function __construct($template_dir = null) {
        $this->template_dir = $template_dir ?: get_template_directory();
    }
    
    /**
     * Load spec data from template_spec.json
     */
    public function load_spec_data($spec_file_path = null) {
        if ($this->cached_spec !== null) {
            return $this->cached_spec;
        }
        
        $spec_data = array();
        
        try {
            // Try direct path first
            if ($spec_file_path && file_exists($spec_file_path)) {
                $spec_data = json_decode(file_get_contents($spec_file_path), true);
                if (WP_DEBUG) {
                    error_log("📋 Loaded spec from direct path: " . $spec_file_path);
                }
            }
            // Try template directory
            elseif ($this->template_dir) {
                $spec_file = $this->template_dir . '/specs/template_spec.json';
                if (file_exists($spec_file)) {
                    $spec_data = json_decode(file_get_contents($spec_file), true);
                    if (WP_DEBUG) {
                        error_log("📋 Loaded spec from template dir: " . $spec_file);
                    }
                }
            }
        } catch (Exception $e) {
            if (WP_DEBUG) {
                error_log("⚠️ Could not load spec data: " . $e->getMessage());
            }
        }
        
        $this->cached_spec = $spec_data ?: array();
        return $this->cached_spec;
    }
    
    /**
     * Get business information from spec data
     */
    public function get_business_info($spec_data = null) {
        if (!$spec_data) {
            $spec_data = $this->load_spec_data();
        }
        
        return isset($spec_data['business_info']) ? $spec_data['business_info'] : array();
    }
    
    /**
     * Get services with descriptions from spec data
     */
    public function get_services($spec_data = null) {
        if (!$spec_data) {
            $spec_data = $this->load_spec_data();
        }
        
        // Try WordPress options first
        $wp_services = get_option('business_services', array());
        if (!empty($wp_services)) {
            if (WP_DEBUG) {
                error_log("🔧 Using services from WordPress options");
            }
            return $wp_services;
        }
        
        // Try spec data
        $business_info = $this->get_business_info($spec_data);
        $services = array();
        
        if (isset($business_info['services']) && !empty($business_info['services'])) {
            foreach ($business_info['services'] as $service_name) {
                if (strtolower($service_name) !== 'services') {
                    $services[$service_name] = $this->generate_service_description($service_name, $business_info);
                }
            }
            if (WP_DEBUG) {
                error_log("🔧 Using services from spec data");
            }
        }
        
        // Fallback to business type-based services
        if (empty($services)) {
            $business_type = isset($business_info['business_type']) ? $business_info['business_type'] : 'Service Business';
            $services = $this->get_fallback_services($business_type);
            if (WP_DEBUG) {
                error_log("⚠️ Using fallback services for business type: " . $business_type);
            }
        }
        
        return $services;
    }
    
    /**
     * Get color palette from spec data
     */
    public function get_colors($spec_data = null) {
        if (!$spec_data) {
            $spec_data = $this->load_spec_data();
        }
        
        $color_palette = isset($spec_data['color_palette']) ? $spec_data['color_palette'] : array();
        
        // Try mapped colors first
        if (isset($color_palette['mapped_colors']) && !empty($color_palette['mapped_colors'])) {
            if (WP_DEBUG) {
                error_log("🎨 Using mapped colors from spec");
            }
            return $color_palette['mapped_colors'];
        }
        
        // Try specified colors
        if (isset($color_palette['specified_colors']) && !empty($color_palette['specified_colors'])) {
            $colors = array();
            foreach ($color_palette['specified_colors'] as $color_spec) {
                if (isset($color_spec['usage']) && isset($color_spec['hex_code'])) {
                    $usage = strtolower($color_spec['usage']);
                    if (strpos($usage, 'button') !== false || strpos($usage, 'accent') !== false) {
                        $colors['primary'] = $color_spec['hex_code'];
                    } elseif (strpos($usage, 'highlight') !== false || strpos($usage, 'icon') !== false) {
                        $colors['secondary'] = $color_spec['hex_code'];
                    } elseif (strpos($usage, 'background') !== false) {
                        $colors['background'] = $color_spec['hex_code'];
                    } elseif (strpos($usage, 'text') !== false || strpos($usage, 'header') !== false) {
                        $colors['text'] = $color_spec['hex_code'];
                    } elseif (strpos($usage, 'footer') !== false || strpos($usage, 'secondary') !== false) {
                        $colors['accent'] = $color_spec['hex_code'];
                    }
                }
            }
            
            if (!empty($colors)) {
                if (WP_DEBUG) {
                    error_log("🎨 Using specified colors from spec");
                }
                return $colors;
            }
        }
        
        // Fallback to business type colors
        $business_info = $this->get_business_info($spec_data);
        $business_type = isset($business_info['business_type']) ? $business_info['business_type'] : 'Service Business';
        $colors = $this->get_fallback_colors($business_type);
        if (WP_DEBUG) {
            error_log("⚠️ Using fallback colors for business type: " . $business_type);
        }
        
        return $colors;
    }
    
    /**
     * Get contact information from spec data
     */
    public function get_contact_info($spec_data = null) {
        if (!$spec_data) {
            $spec_data = $this->load_spec_data();
        }
        
        $business_info = $this->get_business_info($spec_data);
        
        return array(
            'phone' => isset($business_info['phone']) ? $business_info['phone'] : '',
            'email' => isset($business_info['email']) ? $business_info['email'] : '',
            'address' => isset($business_info['address']) ? $business_info['address'] : '',
            'business_name' => isset($business_info['business_name']) ? $business_info['business_name'] : '',
            'business_type' => isset($business_info['business_type']) ? $business_info['business_type'] : 'Service Business'
        );
    }
    
    /**
     * Generate appropriate CTA text based on service name and context
     */
    public function get_cta_text($service_name, $context = 'default') {
        $service_lower = strtolower($service_name);
        
        if ($context === 'phone') {
            if (strpos($service_lower, 'emergency') !== false || strpos($service_lower, 'urgent') !== false) {
                return 'Call Now';
            } elseif (strpos($service_lower, 'consultation') !== false) {
                return 'Schedule Call';
            } else {
                return 'Call Today';
            }
        }
        
        // Default button/link context
        if (strpos($service_lower, 'design') !== false) {
            return 'Get Design Quote';
        } elseif (strpos($service_lower, 'maintenance') !== false) {
            return 'Schedule Service';
        } elseif (strpos($service_lower, 'recovery') !== false || strpos($service_lower, 'repair') !== false) {
            return 'Get Help Now';
        } elseif (strpos($service_lower, 'consultation') !== false) {
            return 'Book Consultation';
        } elseif (strpos($service_lower, 'installation') !== false) {
            return 'Get Installed';
        }
        
        return 'Get Started';
    }
    
    /**
     * Generate appropriate description for a service based on its name and business context
     */
    public function generate_service_description($service_name, $business_info = array()) {
        $service_lower = strtolower($service_name);
        $business_type = isset($business_info['business_type']) ? $business_info['business_type'] : '';
        $business_type_lower = strtolower($business_type);
        
        // Landscaping services
        if (strpos($service_lower, 'landscape') !== false || strpos($service_lower, 'design') !== false) {
            return 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.';
        } elseif (strpos($service_lower, 'hardscaping') !== false || strpos($service_lower, 'patio') !== false) {
            return 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.';
        } elseif (strpos($service_lower, 'lawn') !== false || strpos($service_lower, 'maintenance') !== false) {
            return 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.';
        }
        
        // PC repair services
        elseif (strpos($service_lower, 'virus') !== false || strpos($service_lower, 'malware') !== false) {
            return 'Complete virus and malware removal to keep your computer safe and running smoothly.';
        } elseif (strpos($service_lower, 'hardware') !== false && strpos($service_lower, 'repair') !== false) {
            return 'Professional hardware diagnosis, repair, and upgrade services for optimal performance.';
        } elseif (strpos($service_lower, 'data') !== false && strpos($service_lower, 'recovery') !== false) {
            return 'Recover lost data and set up reliable backup solutions to protect your important files.';
        }
        
        // Generic descriptions based on business type
        elseif (strpos($business_type_lower, 'landscaping') !== false) {
            return 'Professional ' . strtolower($service_name) . ' services to enhance and maintain your outdoor spaces.';
        } elseif (strpos($business_type_lower, 'repair') !== false || strpos($business_type_lower, 'pc') !== false) {
            return 'Expert ' . strtolower($service_name) . ' services to keep your technology running smoothly.';
        }
        
        // Generic fallback
        return 'Professional ' . strtolower($service_name) . ' services delivered with expertise, attention to detail, and a commitment to customer satisfaction.';
    }
    
    /**
     * Get fallback services based on business type
     */
    public function get_fallback_services($business_type) {
        $business_lower = strtolower($business_type);
        
        if (strpos($business_lower, 'landscaping') !== false || strpos($business_lower, 'landscape') !== false) {
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
        }
        
        return array(
            'Professional Consultation' => 'Expert consultation services tailored to your specific needs.',
            'Custom Solutions' => 'Personalized solutions designed to address your unique challenges.',
            'Professional Support' => 'Reliable ongoing support to ensure continued success.'
        );
    }
    
    /**
     * Get fallback colors based on business type
     */
    public function get_fallback_colors($business_type) {
        $business_lower = strtolower($business_type);
        
        // Business-specific color palettes
        $color_palettes = array(
            'landscaping' => array('primary' => '#22c55e', 'secondary' => '#16a34a', 'accent' => '#84cc16', 'background' => '#ffffff', 'text' => '#1f2937'),
            'pc repair' => array('primary' => '#3b82f6', 'secondary' => '#1d4ed8', 'accent' => '#06b6d4', 'background' => '#ffffff', 'text' => '#1f2937'),
            'restaurant' => array('primary' => '#dc2626', 'secondary' => '#b91c1c', 'accent' => '#f59e0b', 'background' => '#ffffff', 'text' => '#1f2937'),
            'construction' => array('primary' => '#ea580c', 'secondary' => '#c2410c', 'accent' => '#eab308', 'background' => '#ffffff', 'text' => '#1f2937'),
            'automotive' => array('primary' => '#dc2626', 'secondary' => '#991b1b', 'accent' => '#6b7280', 'background' => '#ffffff', 'text' => '#1f2937'),
        );
        
        // Find matching palette
        foreach ($color_palettes as $key => $palette) {
            if (strpos($business_lower, $key) !== false) {
                return $palette;
            }
        }
        
        // Default palette
        return array(
            'primary' => '#2563eb', 'secondary' => '#1d4ed8', 'accent' => '#f59e0b',
            'background' => '#ffffff', 'text' => '#1f2937'
        );
    }
}

// Convenience functions for backward compatibility
function load_business_info($template_dir = null) {
    $loader = new SpecLoader($template_dir);
    return $loader->get_business_info();
}

function load_services($template_dir = null) {
    $loader = new SpecLoader($template_dir);
    return $loader->get_services();
}

function load_colors($template_dir = null) {
    $loader = new SpecLoader($template_dir);
    return $loader->get_colors();
}

function load_contact_info($template_dir = null) {
    $loader = new SpecLoader($template_dir);
    return $loader->get_contact_info();
}
?>
