# Multi-Page Website Request

## Project Description

Create a clean, light-themed WordPress website for **Northern Roots Landscaping**, a residential and commercial landscaping company based in **Andover, Minnesota**. This multi-page site will be optimized for mobile and SEO, highlighting the company's design/build services and driving local leads.

## Target Audience

- Homeowners looking to upgrade their yards, patios, or outdoor features
- Property managers and HOAs needing ongoing landscape maintenance
- Minnesotans who value curb appeal, sustainability, and seasonal outdoor enhancements

## Site Architecture & Navigation

### Primary Navigation Structure

```
Home | Services | Portfolio | About | Contact | Blog
```

### Page Hierarchy

```
├── Home (index.php)
├── Services (page-services.php)
│   ├── Landscape Design (/services/design/)
│   ├── Hardscaping & Patios (/services/hardscaping/)
│   └── Lawn Maintenance (/services/lawn-care/)
├── Portfolio (page-portfolio.php)
├── About (page-about.php)
├── Contact (page-contact.php)
└── Blog (index.php with posts)
    ├── Category: Seasonal Tips
    ├── Category: Project Spotlights
    └── Category: Outdoor Living Ideas
```

### Secondary Navigation

- **Footer Menu**: Privacy Policy | Terms of Service | Service Areas
- **Utility Navigation**: Call Now | Request Consultation | Get Estimate

## Page-Specific Requirements

### 🏠 **Home Page** (index.php)

**Purpose**: Showcase professionalism and outdoor transformation expertise  
**Content Sections**:

- Hero with seasonal landscape image and CTA
- Service highlights (3 cards linking to individual services)
- Portfolio preview (carousel or grid)
- "Why Choose Us" credibility section
- Google review highlights
- Local service area mention

**CTAs**:

- Primary: "Get Your Free Estimate"
- Secondary: "See Our Work"
- Tertiary: "Explore Services"

### 🌿 **Services Page** (page-services.php)

**Purpose**: Provide clarity on offerings and encourage action  
**Content Sections**:

- Overview of service philosophy
- Detailed service cards with photos
- Lawn care packages & seasonal options
- Commercial vs. Residential differences
- FAQs and seasonal tips
- Estimate request form

**CTAs**:

- Primary: "Schedule Consultation"
- Secondary: "Request Service Plan"

### 👤 **About Page** (page-about.php)

**Purpose**: Build connection and convey trust  
**Content Sections**:

- Founder/owner story with outdoor background
- Team photos and bios
- Experience, licenses, and affiliations
- Commitment to eco-friendly practices
- Community projects or events
- Awards or recognition

**CTAs**:

- Primary: "Start Your Project"
- Secondary: "View Our Portfolio"

### 🌟 **Portfolio Page** (page-portfolio.php)

**Purpose**: Demonstrate quality and inspire visitors  
**Content Sections**:

- Project showcase (categorized or filterable)
- Before/after image sliders
- Project descriptions (goals, challenges, outcomes)
- Client quotes per project
- Seasonal project examples (snow to summer)

**CTAs**:

- Primary: "Book Your Free Estimate"
- Secondary: "View All Services"

### 📞 **Contact Page** (page-contact.php)

**Purpose**: Encourage connection and service inquiries  
**Content Sections**:

- Customizable contact form
- Phone, email, and social links
- Office location map
- Service hours and seasonal availability
- Service area map with cities listed
- Emergency/after-storm service info

**CTAs**:

- Primary: "Call Us Today"
- Secondary: "Send a Message"

### 📝 **Blog/News** (blog template)

**Purpose**: Build topical authority and provide seasonal advice  
**Content Types**:

- Seasonal preparation guides (e.g. fall cleanup, spring prep)
- Hardscape care and maintenance
- Behind-the-scenes project posts
- Trends in outdoor living design
- Native plants and sustainable landscaping

## Navigation & User Experience

### Primary Navigation Behavior

- **Desktop**: Horizontal menu with dropdown under Services
- **Mobile**: Hamburger menu with nested dropdowns
- **Sticky Nav**: Condensed scroll state with CTA
- **Current Page Highlighting**: Clear active page indicators

### Breadcrumb Navigation

- Display on all content pages (except Home)
- Format: Home > Services > Lawn Maintenance
- Use structured data for breadcrumbs

### Internal Linking Strategy

- Link related services (e.g. design ↔ install)
- Blog ↔ service pages (e.g. “5 Best Patio Ideas” → Hardscaping)
- Footer sitemap for crawlability
- Cross-promotion in CTAs and related cards

## Technical Requirements

### WordPress Template Files Needed

```
├── index.php (blog/home)
├── front-page.php (static home page)
├── page.php (default page template)
├── page-services.php (services page template)
├── page-about.php (about page template)
├── page-portfolio.php (portfolio showcase template)
├── page-contact.php (contact page template)
├── single.php (blog post template)
├── archive.php (blog archive)
├── 404.php (error page)
├── header.php
├── footer.php
├── sidebar.php
└── functions.php
```

### Menu Registration

```php
register_nav_menus(array(
    'primary' => 'Primary Navigation',
    'footer' => 'Footer Navigation',
    'utility' => 'Utility Navigation',
    'services' => 'Services Submenu'
));
```

### Custom Post Types (Optional)

- **Projects**: Custom portfolio entries
- **Testimonials**: For structured social proof
- **Seasonal Tips**: Grouped under blog or stand-alone

## SEO & Schema Strategy

### Page-Specific SEO

- **Home**: Local business schema + landscaping service
- **Services**: Service schema for each landscape offering
- **About**: Organization + person schema
- **Portfolio**: ImageObject schema for visuals
- **Contact**: Local business schema
- **Blog**: Article schema

### Local SEO Focus

- Rich snippets for services and testimonials
- Consistent NAP (Name, Address, Phone)
- Integrate with Google Business Profile
- Location keywords: Andover, Anoka, Ham Lake, Coon Rapids

## Design & Layout Requirements

### Consistent Elements Across Pages

- **Header**: Logo, clean nav, phone number, sticky CTA
- **Footer**: Contact info, location links, newsletter opt-in
- **Sidebar** (where needed): Seasonal offer, service links

### Page-Specific Design Elements

- **Home**: Hero with changing seasonal image, icon blocks for services
- **Services**: Collapsible service details, comparison charts
- **About**: Nature-styled timeline or milestones
- **Portfolio**: Image grid with modal popups or sliders
- **Contact**: Clean form layout, map embed, contact icons

### Responsive Considerations

- Responsive grid layouts
- Flexible image ratios
- Tap targets and hover feedback
- Performance optimization for mobile users

## Visual Style & Branding Guidelines

### Color Palette

The website should use a nature-inspired, light color palette that reflects Minnesota’s outdoors across all seasons. Recommended colors include:

- **Evergreen (#3B6A4D)** – for buttons, accents, and callouts
- **Sage Green (#9CAF88)** – for highlights, icons, and hover effects
- **Soft Cream (#F0EDE5)** – as the main background color (easier on eyes)
- **Charcoal Gray (#333333)** – for headers and important text
- **Soft Earth Brown (#A68C6D)** – for footer or secondary elements

Avoid heavy contrast or neon tones. The design should feel **organic**, **professional**, and **friendly**.

### Typography

- **Headings**: Use a strong but modern serif like Merriweather or a rustic sans-serif like Cabin.
- **Body Text**: Clean, readable sans-serif like Lato or Open Sans.

### Imagery & Icons

- Use **high-quality outdoor images** from Minnesota seasons (snowy yards, green lawns, stone patios).
- Emphasize **before/after visuals** in service and portfolio sections.
- Icons should be **outlined and natural-themed** (leaves, tools, water drops).

### General Style Description

The site should feel:

- **Fresh and open**, not cluttered
- **Grounded in nature**, not overly corporate
- **Trustworthy and family-run**, with warm tones and personal photos
- **Mobile-friendly** with large tap targets and generous spacing

This design guidance should be followed across all templates and adapted for responsiveness and accessibility.

## Content Management

### Editable Content Areas

- Service descriptions and availability
- Seasonal promotions
- Blog posts and images
- Testimonials and case studies
- Contact details and hours

### WordPress Customizer Options

- Logo and branding colors
- Header CTA text
- Homepage hero image
- Custom quote form toggle
- Social profile links

## Success Metrics & Goals

### Conversion Goals

- Quote form submissions
- Consultation bookings
- Call-to-action clicks
- Portfolio engagement

### SEO Goals

- Rank for "landscaping Andover MN"
- Rank for "patio design MN" and related terms
- Increase seasonal organic traffic
- Improve local map pack visibility

### User Experience Goals

- Clean mobile navigation
- Easy access to services
- Fast performance across devices
- Cohesive design with natural elements

## Future Expansion Considerations

### Phase 2 Features

- Client login for project tracking
- Online estimate calculator
- Newsletter integration
- Referral/rewards program

### Content Growth

- Monthly blog articles
- Seasonal video tips
- Project walkthroughs
- Sustainability education
