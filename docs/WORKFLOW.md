# UTM Shortener Workflow

## How It Works

```mermaid
graph TB
    A[User Creates Campaign] --> B[Define UTM Parameters]
    B --> C[Create Short URLs]
    C --> D[Share URLs in Marketing]
    
    D --> E[Visitor Clicks Link]
    E --> F[System Tracks Click]
    F --> G[Log Analytics Data]
    G --> H[Redirect to Target URL]
    
    F --> I[Capture Data]
    I --> J[IP/Location]
    I --> K[Device/Browser]
    I --> L[Referrer Source]
    
    J --> M[Analytics Dashboard]
    K --> M
    L --> M
    
    M --> N[Campaign Reports]
    M --> O[URL Performance]
    M --> P[Source Analysis]
```

## Key Components

### 1. Campaign Creation Flow
```mermaid
sequenceDiagram
    participant User
    participant System
    participant Database
    
    User->>System: Create UTM Campaign
    System->>System: Validate Parameters
    System->>Database: Save Campaign
    Database-->>System: Campaign ID
    System-->>User: Campaign Created
    
    User->>System: Create Short URL
    System->>System: Generate Short Code
    System->>System: Build Short URL with Domain
    System->>Database: Save Short URL
    Database-->>System: Short URL Data
    System-->>User: Short URL Ready
```

### 2. Click Tracking Flow
```mermaid
sequenceDiagram
    participant Visitor
    participant ShortURL
    participant Analytics
    participant Target
    
    Visitor->>ShortURL: Click short.link/s/abc123
    ShortURL->>Analytics: Log Click Event
    Analytics->>Analytics: Parse User Agent
    Analytics->>Analytics: Get Referrer
    Analytics->>Analytics: Get IP/Location
    ShortURL->>Target: Redirect with UTM
    Target-->>Visitor: Show Content
```

## Data Flow

### Campaign Structure
```
UTM Campaign
├── Campaign Name
├── UTM Parameters
│   ├── utm_source
│   ├── utm_medium
│   ├── utm_campaign
│   ├── utm_term (optional)
│   └── utm_content (optional)
└── Short URLs
    ├── URL 1
    ├── URL 2
    └── URL N
```

### Analytics Collection
```
Click Event
├── Timestamp
├── Short URL Reference
├── Visitor Data
│   ├── IP Address
│   ├── User Agent
│   └── Referrer
└── Parsed Data
    ├── Country
    ├── Device Type
    ├── Browser
    └── Traffic Source
```

## Configuration Options

### Domain Setup Options

#### Option 1: Same Domain
```
Your Site: https://erp.company.com
Short URLs: https://erp.company.com/s/xxxxx
```

#### Option 2: Subdomain
```
Your Site: https://erp.company.com
Short URLs: https://link.company.com/s/xxxxx
```

#### Option 3: Custom Domain
```
Your Site: https://erp.company.com
Short URLs: https://short.link/s/xxxxx
```

## Analytics Dashboard Views

### Campaign Overview
- Total Clicks
- Unique Visitors
- Click-through Rate
- Top Performing URLs
- Geographic Distribution

### Source Analysis
- Traffic Sources Breakdown
- Social Media Performance
- Email Campaign Results
- Direct Traffic Analysis

### Device Analytics
- Desktop vs Mobile
- Browser Distribution
- Operating System Stats

### Time-based Analytics
- Hourly Click Patterns
- Daily Trends
- Campaign Duration Performance
