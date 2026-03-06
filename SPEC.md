# Nano Photoshop - Project Specification

## 1. Project Overview

**Project Name:** NanoShop
**Project Type:** AI-Powered Image Editing Web Application
**Core Functionality:** An intelligent image editing tool where users can chat with their images. The AI analyzes the image and conversation, then suggests and applies appropriate editing operations (saturation, masks, filters, brightness, contrast, etc.) to achieve the desired result.
**Target Users:**
- Casual users who want quick, professional-looking image edits without learning complex software
- Content creators who need transparent, controllable edits (not just AI generation)
- Small business owners who need quick image adjustments

---

## 2. UI/UX Specification

### Layout Structure

**Page Sections:**
1. **Header** - Logo, tagline, premium badge
2. **Main Workspace** - Split view with image canvas (left) and chat panel (right)
3. **Operation Panel** - Collapsible panel showing applied operations
4. **Footer** - Credits, pricing link

**Grid Layout:**
- Desktop: 60% image canvas | 40% chat panel
- Tablet: 50% | 50%
- Mobile: Stacked - image on top, chat below

**Responsive Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Visual Design

**Color Palette:**
- Primary: `#1A1A2E` (Deep navy background)
- Secondary: `#16213E` (Slightly lighter navy)
- Accent: `#E94560` (Vibrant coral red)
- Accent Secondary: `#0F3460` (Deep blue)
- Success: `#00D9A5` (Mint green)
- Text Primary: `#FFFFFF`
- Text Secondary: `#A0A0B0`
- Surface: `#252540` (Card backgrounds)
- Border: `#3A3A5C`

**Typography:**
- Headings: "Outfit" (Google Fonts) - Bold 700
  - H1: 48px
  - H2: 32px
  - H3: 24px
- Body: "DM Sans" (Google Fonts) - Regular 400
  - Body: 16px
  - Small: 14px
  - Caption: 12px

**Spacing System:**
- Base unit: 8px
- XS: 4px, S: 8px, M: 16px, L: 24px, XL: 32px, XXL: 48px

**Visual Effects:**
- Cards: `box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3)`
- Buttons hover: Scale 1.02 + glow effect
- Glassmorphism on panels: `backdrop-filter: blur(10px)`
- Gradient accents: `linear-gradient(135deg, #E94560, #0F3460)`
- Smooth transitions: 0.3s ease

### Components

**1. Upload Zone**
- Drag & drop area with dashed border
- States: default, hover (border solid + glow), file-loaded
- Icon: Cloud upload icon
- Supported formats badge

**2. Image Canvas**
- Zoomable/pannable image view
- Before/After toggle button
- Reset button
- Download button
- Fullscreen toggle

**3. Chat Panel**
- Message bubbles (user: right-aligned coral, AI: left-aligned surface)
- Typing indicator animation
- Input field with send button
- Quick suggestion chips below input

**4. Operation Cards**
- Icon + name + intensity slider
- Revert button per operation
- Drag to reorder

**5. Premium Banner**
- Floating banner for free tier limit
- CTA button to pricing

---

## 3. Functionality Specification

### Core Features

**Image Upload:**
- Drag & drop or click to upload
- Support: JPG, PNG, WEBP, BMP
- Max size: 10MB
- Auto-resize for large images (max 2048px)

**AI Chat Interface:**
- Natural language conversation about desired edits
- AI analyzes image and suggests operations
- Operations are applied in real-time preview
- Conversation history maintained

**Image Operations (AI-Suggested):**
- Brightness adjustment
- Contrast adjustment
- Saturation adjustment
- Hue rotation
- Blur/Sharpen
- Crop (with AI suggestion)
- Rotate
- Flip horizontal/vertical
- Auto-enhance (one-click)
- Remove background (premium)
- Add filters (vintage, noir, vivid, etc.)

**Operation Management:**
- View all applied operations as cards
- Adjust intensity slider per operation
- Revert individual operations
- Reset to original
- Export with applied operations

### User Interactions & Flows

1. **Upload Flow:** Land → Upload image → Image appears in canvas → Chat ready
2. **Edit Flow:** Type request → AI suggests operation → Preview shown → Confirm/Adjust → Apply
3. **Export Flow:** Click export → Choose format → Download

### Data Handling
- Images stored temporarily in session
- No persistent storage (privacy-focused)
- Operations stored as stack for undo/redo

### Edge Cases
- Invalid file type → Show error toast
- File too large → Show size limit message
- AI can't understand → Suggest rephrasing
- Network error → Retry with exponential backoff

---

## 4. Technical Architecture

### Backend (FastAPI)
- `/api/upload` - Image upload endpoint
- `/api/chat` - AI chat with image analysis
- `/api/apply` - Apply specific operation
- `/api/export` - Download edited image
- `/api/reset` - Reset to original

### Frontend (Flask + HTML/CSS/JS)
- Single page application
- AJAX for API calls
- Local state management for operations stack

### AI Integration
- Use Claude API for natural language understanding
- Image processing with Pillow (PIL)

---

## 5. Acceptance Criteria

1. ✅ User can upload an image via drag/drop or click
2. ✅ Image displays in canvas with zoom/pan
3. ✅ User can type natural language requests
4. ✅ AI responds with suggested operations
5. ✅ Operations can be previewed and applied
6. ✅ Operation stack is viewable and manageable
7. ✅ Before/After comparison works
8. ✅ Image can be exported in multiple formats
9. ✅ UI is beautiful and premium-looking
10. ✅ Responsive on mobile, tablet, desktop
11. ✅ Premium features show upgrade prompts

---

## 6. Pricing Model (Future)

**Free Tier:**
- 5 image edits per day
- Basic operations only
- Watermark on export

**Pro ($9.99/month):**
- Unlimited edits
- All operations
- No watermark
- Priority processing

**Enterprise:** Custom pricing
