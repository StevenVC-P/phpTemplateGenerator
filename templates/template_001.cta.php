<?php
/**
 * SaaS Landing Page Template - CTA Optimized Version
 * Template ID: template_001.cta
 * Created: 2025-06-23
 * Description: Call-to-action optimized version with enhanced conversion elements
 */

// Enhanced form handling with better validation and tracking
$form_submitted = false;
$form_errors = [];
$success_message = '';
$conversion_tracking = false;

if ($_POST) {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $company = trim($_POST['company'] ?? '');
    $plan_interest = $_POST['plan_interest'] ?? '';
    
    // Enhanced validation
    if (empty($name) || strlen($name) < 2) {
        $form_errors[] = 'Name must be at least 2 characters';
    }
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $form_errors[] = 'Valid email address is required';
    }
    if (empty($company)) {
        $form_errors[] = 'Company name is required';
    }
    
    if (empty($form_errors)) {
        // Process lead capture
        $success_message = 'Welcome aboard! Check your email for next steps.';
        $form_submitted = true;
        $conversion_tracking = true;
        
        // Here you would typically:
        // - Save to CRM/database
        // - Send welcome email
        // - Trigger marketing automation
        // - Track conversion event
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaaS Landing Page - Start Your Free Trial Today</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Enhanced CTA-focused styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #1f2937;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Enhanced Hero with stronger CTA */
        .hero {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            padding: 120px 0 80px;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .hero .subtitle {
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .cta-primary {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 1.25rem 2.5rem;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.1rem;
            margin: 0 1rem 1rem 0;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }
        
        .cta-primary:hover {
            background: #059669;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        }
        
        .cta-secondary {
            display: inline-block;
            background: transparent;
            color: white;
            padding: 1.25rem 2.5rem;
            text-decoration: none;
            border: 2px solid white;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s;
        }
        
        .cta-secondary:hover {
            background: white;
            color: #2563eb;
        }
        
        .trust-indicators {
            margin-top: 3rem;
            opacity: 0.8;
        }
        
        .trust-indicators p {
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        /* Enhanced pricing section */
        .pricing {
            padding: 80px 0;
            background: #f9fafb;
        }
        
        .pricing h2 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #1f2937;
        }
        
        .pricing-subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #6b7280;
            margin-bottom: 3rem;
        }
        
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .pricing-card {
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            transition: transform 0.3s;
        }
        
        .pricing-card:hover {
            transform: translateY(-5px);
        }
        
        .pricing-card.featured {
            border: 3px solid #10b981;
            transform: scale(1.05);
        }
        
        .pricing-card.featured::before {
            content: "Most Popular";
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: #10b981;
            color: white;
            padding: 0.5rem 1.5rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .price {
            font-size: 3rem;
            font-weight: 700;
            color: #2563eb;
            margin: 1rem 0;
        }
        
        .price-period {
            font-size: 1rem;
            color: #6b7280;
            font-weight: 400;
        }
        
        /* Lead capture form */
        .lead-capture {
            padding: 80px 0;
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white;
        }
        
        .lead-form {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .lead-form h3 {
            color: #1f2937;
            text-align: center;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #374151;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 1rem;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #2563eb;
        }
        
        .submit-btn {
            width: 100%;
            background: #2563eb;
            color: white;
            padding: 1.25rem;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .submit-btn:hover {
            background: #1d4ed8;
        }
        
        .success-message {
            background: #10b981;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .error-messages {
            background: #ef4444;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .cta-primary,
            .cta-secondary {
                display: block;
                margin: 0.5rem 0;
            }
            
            .pricing-card.featured {
                transform: none;
            }
        }
    </style>
</head>
<body>
    <!-- Hero Section with Enhanced CTAs -->
    <section class="hero" id="home">
        <div class="container">
            <h1>Transform Your Business in 30 Days</h1>
            <p class="subtitle">Join 10,000+ companies using SaaSPro to streamline operations and boost productivity by 40%</p>
            <div class="cta-buttons">
                <a href="#signup" class="cta-primary">Start Free Trial</a>
                <a href="#demo" class="cta-secondary">Watch Demo</a>
            </div>
            <div class="trust-indicators">
                <p>✓ No credit card required ✓ 14-day free trial ✓ Cancel anytime</p>
                <p>Trusted by Fortune 500 companies</p>
            </div>
        </div>
    </section>

    <!-- Enhanced Pricing Section -->
    <section class="pricing" id="pricing">
        <div class="container">
            <h2>Choose Your Plan</h2>
            <p class="pricing-subtitle">Start free, upgrade as you grow. All plans include our core features.</p>
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h3>Starter</h3>
                    <div class="price">$0<span class="price-period">/month</span></div>
                    <p>Perfect for small teams</p>
                    <a href="#signup" class="cta-primary">Start Free</a>
                </div>
                <div class="pricing-card featured">
                    <h3>Professional</h3>
                    <div class="price">$29<span class="price-period">/month</span></div>
                    <p>For growing businesses</p>
                    <a href="#signup" class="cta-primary">Start Trial</a>
                </div>
                <div class="pricing-card">
                    <h3>Enterprise</h3>
                    <div class="price">$99<span class="price-period">/month</span></div>
                    <p>For large organizations</p>
                    <a href="#signup" class="cta-primary">Contact Sales</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Lead Capture Section -->
    <section class="lead-capture" id="signup">
        <div class="container">
            <div class="lead-form">
                <h3>Start Your Free Trial Today</h3>
                
                <?php if ($success_message): ?>
                    <div class="success-message"><?php echo htmlspecialchars($success_message); ?></div>
                <?php endif; ?>
                
                <?php if (!empty($form_errors)): ?>
                    <div class="error-messages">
                        <?php foreach ($form_errors as $error): ?>
                            <p><?php echo htmlspecialchars($error); ?></p>
                        <?php endforeach; ?>
                    </div>
                <?php endif; ?>
                
                <?php if (!$form_submitted): ?>
                <form method="POST" action="">
                    <div class="form-group">
                        <label for="name">Full Name</label>
                        <input type="text" id="name" name="name" value="<?php echo htmlspecialchars($_POST['name'] ?? ''); ?>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Work Email</label>
                        <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="company">Company Name</label>
                        <input type="text" id="company" name="company" value="<?php echo htmlspecialchars($_POST['company'] ?? ''); ?>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="plan_interest">Plan Interest</label>
                        <select id="plan_interest" name="plan_interest">
                            <option value="">Select a plan</option>
                            <option value="starter" <?php echo ($_POST['plan_interest'] ?? '') === 'starter' ? 'selected' : ''; ?>>Starter (Free)</option>
                            <option value="professional" <?php echo ($_POST['plan_interest'] ?? '') === 'professional' ? 'selected' : ''; ?>>Professional ($29/mo)</option>
                            <option value="enterprise" <?php echo ($_POST['plan_interest'] ?? '') === 'enterprise' ? 'selected' : ''; ?>>Enterprise ($99/mo)</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="submit-btn">Start Free Trial</button>
                </form>
                <?php endif; ?>
            </div>
        </div>
    </section>

    <?php if ($conversion_tracking): ?>
    <script>
        // Conversion tracking code would go here
        console.log('Conversion tracked: Lead captured');
    </script>
    <?php endif; ?>
</body>
</html>
