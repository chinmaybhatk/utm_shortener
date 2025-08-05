/**
 * Cloudflare Worker for UTM Shortener Custom Domain
 * 
 * This worker enables you to use a custom short domain (like short.link)
 * that redirects to your Frappe Cloud UTM Shortener instance.
 * 
 * Setup:
 * 1. Create a Cloudflare account and add your short domain
 * 2. Go to Workers & Pages > Create Worker
 * 3. Copy this code into the worker
 * 4. Configure the FRAPPE_SITE_URL environment variable
 * 5. Add a route for your domain /* to this worker
 */

// Configuration - Update this with your Frappe Cloud site URL
const FRAPPE_SITE_URL = 'https://your-site.frappe.cloud';

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;
  
  // Handle different path patterns
  if (path === '/' || path === '') {
    // Root domain - show a landing page or redirect to main site
    return handleRootDomain();
  } else if (path.startsWith('/health')) {
    // Health check endpoint
    return handleHealthCheck();
  } else if (path.startsWith('/robots.txt')) {
    // Robots.txt for SEO
    return handleRobotsTxt();
  } else {
    // Assume everything else is a short code
    return handleShortCode(request, path);
  }
}

/**
 * Handle short code redirects
 */
async function handleShortCode(request, path) {
  // Remove leading slash
  const shortCode = path.substring(1);
  
  // Remove any trailing slashes
  const cleanCode = shortCode.replace(/\/$/, '');
  
  // Build the redirect URL
  const redirectUrl = `${FRAPPE_SITE_URL}/s/${cleanCode}`;
  
  // Preserve query parameters if any
  const url = new URL(request.url);
  if (url.search) {
    redirectUrl += url.search;
  }
  
  // Log the redirect (optional - remove in production for performance)
  console.log(`Redirecting ${cleanCode} to ${redirectUrl}`);
  
  // Perform the redirect
  return Response.redirect(redirectUrl, 301);
}

/**
 * Handle root domain requests
 */
function handleRootDomain() {
  const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Short URL Service</title>
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
          background: #f5f5f5;
        }
        .container {
          text-align: center;
          padding: 2rem;
          background: white;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
          color: #333;
          margin-bottom: 1rem;
        }
        p {
          color: #666;
          margin-bottom: 2rem;
        }
        a {
          color: #0066cc;
          text-decoration: none;
        }
        a:hover {
          text-decoration: underline;
        }
        .stats {
          margin-top: 2rem;
          padding-top: 2rem;
          border-top: 1px solid #eee;
          font-size: 0.9rem;
          color: #999;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🔗 Short URL Service</h1>
        <p>This is a private URL shortening service.</p>
        <p>
          <a href="${FRAPPE_SITE_URL}" target="_blank">Visit Main Site →</a>
        </p>
        <div class="stats">
          <p>Powered by UTM Shortener for Frappe</p>
        </div>
      </div>
    </body>
    </html>
  `;
  
  return new Response(html, {
    headers: {
      'Content-Type': 'text/html;charset=UTF-8',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}

/**
 * Handle health check requests
 */
function handleHealthCheck() {
  return new Response(JSON.stringify({
    status: 'healthy',
    service: 'utm-shortener-worker',
    frappe_site: FRAPPE_SITE_URL,
    timestamp: new Date().toISOString()
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-cache'
    }
  });
}

/**
 * Handle robots.txt requests
 */
function handleRobotsTxt() {
  const robotsTxt = `
User-agent: *
Disallow: /
Allow: /$

# Short URLs should not be indexed
User-agent: *
Disallow: /*

# Allow specific bots if needed
User-agent: Googlebot
Disallow: /*
  `.trim();
  
  return new Response(robotsTxt, {
    headers: {
      'Content-Type': 'text/plain',
      'Cache-Control': 'public, max-age=86400'
    }
  });
}

/**
 * Advanced Features (Optional)
 */

// Cache responses for better performance
const cache = caches.default;

async function handleShortCodeWithCache(request, path) {
  // Try to get from cache first
  const cacheKey = new Request(request.url, request);
  const cachedResponse = await cache.match(cacheKey);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // If not in cache, process normally
  const response = await handleShortCode(request, path);
  
  // Cache successful redirects for 5 minutes
  if (response.status === 301) {
    const cacheResponse = new Response(response.body, response);
    cacheResponse.headers.set('Cache-Control', 'public, max-age=300');
    event.waitUntil(cache.put(cacheKey, cacheResponse));
  }
  
  return response;
}

// Analytics Integration (Optional)
async function trackRedirect(shortCode, userAgent, referer) {
  // You can send analytics to your own service here
  // Example: Google Analytics Measurement Protocol
  const analyticsUrl = 'https://www.google-analytics.com/collect';
  const params = new URLSearchParams({
    v: '1',
    tid: 'YOUR-GA-TRACKING-ID',
    cid: generateClientId(),
    t: 'event',
    ec: 'redirect',
    ea: 'click',
    el: shortCode,
    dr: referer || '(direct)'
  });
  
  // Fire and forget
  fetch(analyticsUrl, {
    method: 'POST',
    body: params
  }).catch(() => {
    // Ignore errors
  });
}

function generateClientId() {
  return Math.random().toString(36).substring(2, 15);
}

// A/B Testing Support (Optional)
async function handleShortCodeWithABTest(request, path) {
  const shortCode = path.substring(1);
  
  // Example: 50/50 split test
  const variant = Math.random() < 0.5 ? 'A' : 'B';
  
  // You could redirect to different URLs based on variant
  // or pass variant as a parameter
  const redirectUrl = `${FRAPPE_SITE_URL}/s/${shortCode}?variant=${variant}`;
  
  return Response.redirect(redirectUrl, 301);
}

// Rate Limiting (Optional)
const rateLimiter = {
  requests: new Map(),
  
  isAllowed(ip) {
    const now = Date.now();
    const windowMs = 60 * 1000; // 1 minute
    const maxRequests = 100;
    
    if (!this.requests.has(ip)) {
      this.requests.set(ip, []);
    }
    
    const requests = this.requests.get(ip);
    const recentRequests = requests.filter(time => now - time < windowMs);
    
    if (recentRequests.length >= maxRequests) {
      return false;
    }
    
    recentRequests.push(now);
    this.requests.set(ip, recentRequests);
    
    // Cleanup old entries
    if (this.requests.size > 1000) {
      const oldestAllowed = now - windowMs;
      for (const [ip, times] of this.requests.entries()) {
        const recent = times.filter(time => time > oldestAllowed);
        if (recent.length === 0) {
          this.requests.delete(ip);
        } else {
          this.requests.set(ip, recent);
        }
      }
    }
    
    return true;
  }
};

// Use rate limiting
async function handleRequestWithRateLimit(request) {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  
  if (!rateLimiter.isAllowed(ip)) {
    return new Response('Too many requests', { status: 429 });
  }
  
  return handleRequest(request);
}
