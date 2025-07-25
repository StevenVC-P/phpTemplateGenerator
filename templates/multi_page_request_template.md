# Multi-Page Website Request Template

## Project Overview
**Business Name**: [Business Name]
**Industry**: [Industry/Service Type]
**Location**: [City, State]
**Website Type**: [Multi-page WordPress Site / E-commerce / Portfolio / etc.]

## Site Architecture

### Navigation Structure
```
[Primary Nav Item 1] | [Primary Nav Item 2] | [Primary Nav Item 3] | [Primary Nav Item 4] | [Primary Nav Item 5]
```

### Page Hierarchy
```
├── [Page 1] ([template-file.php])
│   ├── [Subpage 1.1] ([URL slug])
│   └── [Subpage 1.2] ([URL slug])
├── [Page 2] ([template-file.php])
├── [Page 3] ([template-file.php])
└── [Page 4] ([template-file.php])
```

## Page Specifications

### 📄 **[Page Name]** ([template-file.php])
**Purpose**: [Primary goal of this page]
**Target Keywords**: [SEO keywords for this page]

**Content Sections**:
- [Section 1]: [Description]
- [Section 2]: [Description]
- [Section 3]: [Description]

**Call-to-Actions**:
- Primary: "[CTA Text]" → [Action/Link]
- Secondary: "[CTA Text]" → [Action/Link]

**Schema Markup**: [LocalBusiness / Service / Article / etc.]

---

### 📄 **[Page Name 2]** ([template-file.php])
**Purpose**: [Primary goal of this page]
**Target Keywords**: [SEO keywords for this page]

**Content Sections**:
- [Section 1]: [Description]
- [Section 2]: [Description]

**Call-to-Actions**:
- Primary: "[CTA Text]" → [Action/Link]

**Schema Markup**: [Schema type]

---

## Navigation & User Flow

### Primary Navigation
- **Desktop Behavior**: [Horizontal / Dropdown / Mega Menu]
- **Mobile Behavior**: [Hamburger / Slide-out / Accordion]
- **Sticky Navigation**: [Yes/No]
- **Active States**: [How to indicate current page]

### Internal Linking Strategy
- [Page A] links to [Page B] via [specific CTAs]
- [Cross-linking strategy between related pages]
- [Footer navigation structure]

### Breadcrumb Navigation
- **Pages to Include**: [All except home / Specific pages only]
- **Format**: [Home > Category > Page]
- **Schema Markup**: [Yes/No]

## Technical Requirements

### WordPress Template Files
```
Required Files:
├── index.php
├── [custom-page-template.php]
├── [another-template.php]
├── header.php
├── footer.php
└── functions.php

Optional Files:
├── sidebar.php
├── 404.php
├── archive.php
└── single.php
```

### Custom Post Types
- **[Post Type Name]**: [Description and purpose]
- **[Post Type Name 2]**: [Description and purpose]

### Menu Locations
```php
register_nav_menus(array(
    'primary' => '[Menu Description]',
    'footer' => '[Menu Description]',
    'utility' => '[Menu Description]'
));
```

## SEO Strategy

### Page-Specific SEO
| Page | Primary Keyword | Schema Type | Meta Description |
|------|----------------|-------------|------------------|
| [Page 1] | [keyword] | [schema] | [description] |
| [Page 2] | [keyword] | [schema] | [description] |

### Local SEO (if applicable)
- **Service Area**: [Geographic coverage]
- **Local Keywords**: [Location + service combinations]
- **Google My Business**: [Integration requirements]

## Design Requirements

### Global Elements
- **Header**: [Logo, navigation, contact info, etc.]
- **Footer**: [Contact, sitemap, social links, etc.]
- **Sidebar**: [Widgets, CTAs, related content]

### Page-Specific Design
- **[Page Name]**: [Unique design elements]
- **[Page Name 2]**: [Unique design elements]

### Responsive Design
- **Breakpoints**: [Mobile, tablet, desktop specifications]
- **Mobile-First**: [Yes/No and specific requirements]
- **Touch Targets**: [Minimum size requirements]

## Content Strategy

### Content Types
- **Static Pages**: [List of pages with static content]
- **Dynamic Content**: [Blog, news, case studies, etc.]
- **User-Generated**: [Reviews, testimonials, comments]

### Content Management
- **Editable Areas**: [What content should be easily editable]
- **WordPress Customizer**: [What options to include]
- **Custom Fields**: [Any special content fields needed]

## Conversion Goals

### Primary Conversions
- [Goal 1]: [Description and measurement]
- [Goal 2]: [Description and measurement]

### Secondary Conversions
- [Goal 1]: [Description and measurement]
- [Goal 2]: [Description and measurement]

### Tracking Requirements
- **Analytics**: [Google Analytics, custom events, etc.]
- **Conversion Tracking**: [Forms, phone calls, etc.]
- **A/B Testing**: [Elements to test]

## Performance Requirements

### Speed Goals
- **Page Load Time**: [Target in seconds]
- **Mobile Performance**: [Specific requirements]
- **Core Web Vitals**: [LCP, FID, CLS targets]

### Optimization
- **Image Optimization**: [Format, compression, lazy loading]
- **CSS/JS**: [Minification, critical CSS, etc.]
- **Caching**: [Requirements and strategy]

## Future Considerations

### Phase 2 Features
- [Feature 1]: [Description and timeline]
- [Feature 2]: [Description and timeline]

### Scalability
- [How the site should handle growth]
- [Additional pages or features to consider]

### Maintenance
- [Content update frequency]
- [Technical maintenance requirements]

---

## Example Usage

To use this template:

1. **Copy this template** for each new multi-page project
2. **Fill in all bracketed placeholders** with specific requirements
3. **Customize sections** based on project needs
4. **Add or remove pages** as needed for the specific project
5. **Include wireframes or mockups** if available

This template ensures that all agents in the pipeline understand:
- The complete site structure
- Page-specific requirements
- Navigation and user flow
- Technical implementation needs
- SEO and conversion goals
