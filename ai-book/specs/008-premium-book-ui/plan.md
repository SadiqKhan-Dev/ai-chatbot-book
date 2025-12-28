# Architectural Plan: Premium Book UI - Modern Docusaurus Theme

**Feature Branch**: `[008-premium-book-ui]`
**Created**: 2025-12-28
**Status**: Draft
**Parent Spec**: `ai-book/specs/008-premium-book-ui/spec.md`

## Executive Summary

This plan outlines the implementation of a premium Docusaurus UI for the AI & Robotics book, following a 4-phase approach. The implementation prioritizes localhost development performance, accessibility, and future extensibility for animated content.

---

## Scope and Dependencies

### In Scope
- Complete design token system (colors, typography, spacing, animations)
- Animated hero banner with gradient effects
- Module and chapter card components with micro-interactions
- Dark/light mode with system preference detection
- Custom navbar and footer
- Sidebar improvements for readability
- MDX-compatible banner system for future animations
- Local placeholder assets
- Performance optimization and accessibility compliance

### Out of Scope
- User authentication and backend integration
- Search functionality (use Docusaurus default)
- Multi-language support (English only)
- PWA/offline capabilities
- Print-optimized styles
- Analytics integration

### External Dependencies
| Dependency | Purpose | Ownership |
|------------|---------|-----------|
| Docusaurus 3.9.2 | Core framework | Facebook/Meta |
| React 19 | UI component library | Meta |
| TypeScript 5.6 | Type safety | Microsoft |
| clsx | Conditional class names | - |

---

## Phase 1: Foundation & Theme

### Tasks

#### 1.1 Initialize Docusaurus Custom Theme Configuration
- **File**: `docusaurus.config.ts`
- **Changes**:
  - Update site title and tagline
  - Configure navbar with theme toggle and navigation
  - Set up footer with custom content
  - Configure color mode defaults
  - Add prism theme for code blocks

#### 1.2 Define Global Design Tokens
- **File**: `src/css/tokens.css`
- **Contents**:
  - Light mode color palette (11 steps)
  - Dark mode color palette (11 steps)
  - Semantic colors (success, warning, error, info)
  - Background and text color tokens
  - Border color tokens

#### 1.3 Define Typography Scale
- **File**: `src/css/tokens.css`
- **Contents**:
  - Font size scale (Major Third 1.250)
  - Font family definitions
  - Font weight definitions
  - Line height definitions

#### 1.4 Define Spacing & Radius System
- **File**: `src/css/tokens.css`
- **Contents**:
  - Spacing scale (8px base)
  - Border radius tokens
  - Shadow tokens

#### 1.5 Configure Navbar
- **File**: `docusaurus.config.ts` → `themeConfig.navbar`
- **Items**:
  - Logo with proper sizing
  - Module dropdown navigation
  - Theme toggle button
  - GitHub link

#### 1.6 Configure Footer
- **File**: `docusaurus.config.ts` → `themeConfig.footer`
- **Items**:
  - Module links
  - Community links
  - Legal/copyright
  - Social icons

#### 1.7 Configure Sidebar
- **File**: `docusaurus.config.ts` + `sidebars.ts`
- **Items**:
  - Collapsible section headers
  - Active state styling
  - Readable typography

### Acceptance Criteria
- [ ] `tokens.css` defines all design tokens
- [ ] Light/dark mode works via system preference
- [ ] Navbar displays all navigation items correctly
- [ ] Footer renders with proper links
- [ ] Sidebar shows active section with clear styling

### Files Modified
```
docusaurus.config.ts
src/css/tokens.css (new)
sidebars.ts
```

---

## Phase 2: Homepage & Navigation

### Tasks

#### 2.1 Build Animated Hero Section
- **File**: `src/components/HeroBanner/index.tsx`
- **Features**:
  - Gradient mesh background animation (CSS keyframes)
  - Text reveal animation (staggered fade-in)
  - Mouse-follow glow effect (CSS `mousemove`)
  - Reduced motion fallback

#### 2.2 Create Module Card Component
- **File**: `src/components/ModuleCard/index.tsx`
- **Features**:
  - Title, description, chapter count, duration
  - Optional thumbnail with gradient placeholder
  - Hover: lift 4px + shadow increase + icon scale
  - Progress ring animation (optional)
  - Link wrapper

#### 2.3 Create Chapter Card Component
- **File**: `src/components/ChapterCard/index.tsx`
- **Features**:
  - Title, description, duration, difficulty badge
  - Hover: scale 1.02x + shadow
  - Completion checkmark animation
  - Difficulty color coding (green/orange/red)

#### 2.4 Build Premium Homepage Layout
- **File**: `src/pages/index.tsx`
- **Sections**:
  - Hero banner
  - Module grid (7 modules)
  - Learning path visualization
  - Chapter preview cards
  - Footer

#### 2.5 Improve Sidebar Styling
- **File**: `src/css/custom.css`
- **Changes**:
  - Active menu item highlighting
  - Collapsible category headers
  - Hover state for links
  - Better spacing for readability

### Acceptance Criteria
- [ ] Hero banner animates on load
- [ ] Module cards show hover micro-interactions
- [ ] Chapter cards display correctly with difficulty badges
- [ ] Homepage renders all 7 modules in grid
- [ ] Sidebar shows clear active state
- [ ] All animations respect `prefers-reduced-motion`

### Files Created/Modified
```
src/components/HeroBanner/
  ├── index.tsx
  ├── styles.module.css
  └── GradientMesh.tsx
src/components/ModuleCard/
  ├── index.tsx
  └── styles.module.css
src/components/ChapterCard/
  ├── index.tsx
  └── styles.module.css
src/pages/index.tsx
src/css/custom.css
```

---

## Phase 3: Motion & Book Content Enhancements

### Tasks

#### 3.1 Create Animation Utilities
- **File**: `src/css/animations.css`
- **Contents**:
  - Fade-in animations (multiple durations)
  - Slide-up animations
  - Scale animations
  - Focus transition utilities

#### 3.2 Implement Scroll-Based Animations
- **Target**: Content sections, cards, banners
- **Method**: Intersection Observer API
- **Behavior**: Elements fade/slide in when scrolled into view

#### 3.3 Add Page Transition Effects
- **File**: `src/css/layout.css`
- **Changes**:
  - Smooth scrolling behavior
  - Link click transition hints
  - Loading state indicators

#### 3.4 Build MDX Banner Component (Static)
- **File**: `src/theme/Banner/index.tsx`
- **Features**:
  - Gradient banner type (CSS)
  - Geometric banner type (SVG)
  - Interactive prop for hover effects
  - Lazy loading wrapper

#### 3.5 Add Hover Micro-interactions
- **Implementation**: Throughout components
- **Interactions**:
  - Button press state (0.98x scale)
  - Link underline expansion
  - Icon rotation on expand
  - Card glow on focus

#### 3.6 Prepare for Future Animations
- **Structure**: Code organization for:
  - Lottie animation integration
  - CSS keyframe enhancements
  - Motion One library usage
  - Canvas/WebGL placeholders

### Acceptance Criteria
- [ ] Scroll animations trigger smoothly
- [ ] Page transitions feel cohesive
- [ ] Banner MDX component works in markdown
- [ ] All interactive elements have hover states
- [ ] Motion preferences are respected

### Files Created/Modified
```
src/css/animations.css (new)
src/css/layout.css (new)
src/theme/Banner/
  ├── index.tsx
  └── styles.module.css
```

---

## Phase 4: Assets & Performance

### Tasks

#### 4.1 Create Placeholder Assets
- **Directory**: `static/img/placeholders/`
- **Files**:
  - `module-default.svg` - Gradient placeholder for modules
  - `chapter-default.svg` - Geometric placeholder for chapters
  - `hero-pattern.svg` - Subtle pattern for hero background
  - `diagram-coming-soon.svg` - "Coming Soon" illustration

#### 4.2 Optimize Images
- **Actions**:
  - Add WebP alternatives where applicable
  - Set explicit dimensions to prevent CLS
  - Use lazy loading for below-fold images

#### 4.3 Performance Testing
- **Metrics**:
  - Lighthouse Performance ≥ 90
  - First Contentful Paint (FCP) < 1.5s
  - Largest Contentful Paint (LCP) < 2.5s
  - Cumulative Layout Shift (CLS) = 0
  - First Input Delay (FID) < 100ms

#### 4.4 Accessibility Testing
- **Metrics**:
  - Lighthouse Accessibility ≥ 95
  - Color contrast WCAG AA compliant
  - Keyboard navigation works
  - Screen reader compatibility
  - Focus indicators visible

#### 4.5 Localhost Validation
- **Actions**:
  - Hot reload < 1 second
  - No console errors
  - No layout shifts on navigation
  - Theme toggle works instantly

#### 4.6 Cross-Browser Testing
- **Browsers**:
  - Chrome (latest 3 versions)
  - Firefox (latest 3 versions)
  - Safari (latest 2 versions)
  - Edge (latest 2 versions)

### Acceptance Criteria
- [ ] All placeholder images render correctly
- [ ] Lighthouse scores meet targets
- [ ] Theme toggle is instant
- [ ] Hot reload is fast
- [ ] Accessibility audit passes
- [ ] No console errors on localhost

### Files Created
```
static/img/placeholders/
  ├── module-default.svg
  ├── chapter-default.svg
  ├── hero-pattern.svg
  ├── diagram-coming-soon.svg
  └── icons/
      ├── module-icon.svg
      └── chapter-icon.svg
```

---

## Key Decisions and Rationale

### Decision 1: CSS Modules for Component Styling
**Options Considered**: CSS Modules vs Tailwind vs Styled Components
**Choice**: CSS Modules
**Rationale**:
- Already used in existing codebase
- Scoped styles prevent conflicts
- No additional dependencies
- Easy to migrate from existing patterns
- Best for Docusaurus ecosystem

### Decision 2: CSS Custom Properties for Theming
**Options Considered**: CSS Variables vs JavaScript theme object
**Choice**: CSS Variables
**Rationale**:
- Native browser support
- Instant theme switching
- No FOUC (Flash of Unstyled Content)
- Easy to debug in DevTools
- Lower JavaScript overhead

### Decision 3: CSS Keyframes Over JavaScript Animations
**Options Considered**: CSS animations vs requestAnimationFrame vs Framer Motion
**Choice**: CSS Keyframes (primary), Canvas (future banners)
**Rationale**:
- Best performance (GPU accelerated)
- Respects `prefers-reduced-motion`
- No external dependencies for MVP
- Easier maintenance
- Future-proof for canvas/WebGL

### Decision 4: 8px Base Spacing System
**Options Considered**: 4px vs 8px vs 10px base
**Choice**: 8px base
**Rationale**:
- Industry standard (used by Material Design, Tailwind)
- Balances granularity with simplicity
- Easy mental math (4=0.5rem, 8=1rem)
- Works well with typical component sizes

---

## Non-Functional Requirements

### Performance Budgets
| Metric | Target | Measurement Tool |
|--------|--------|------------------|
| FCP | < 1.5s | Lighthouse |
| LCP | < 2.5s | Lighthouse |
| CLS | 0 | Lighthouse |
| FID | < 100ms | Lighthouse |
| Bundle size | < 500KB gzipped | Bundle analyzer |
| Hot reload | < 1s | Manual timing |

### Accessibility Requirements
- WCAG 2.1 AA compliance
- Color contrast 4.5:1 minimum
- Focus indicators visible (2px minimum)
- Keyboard navigation complete
- ARIA labels where needed
- `prefers-reduced-motion` respected
- Screen reader tested

### Browser Support
- Chrome 120+
- Firefox 120+
- Safari 17+
- Edge 120+

---

## Operational Readiness

### Observability
- No external analytics in MVP
- Console errors visible in dev
- Performance via Lighthouse CI

### Alerting (Not in MVP)
- Lighthouse score regression
- Bundle size increase
- Accessibility violations

### Deployment
- GitHub Pages (via Docusaurus)
- Vercel (alternative)
- Netlify (alternative)

### Rollback
- Git revert to previous commit
- No database migrations

---

## Risk Analysis

### Risk 1: Animation Performance on Low-End Devices
**Impact**: Medium
**Blast Radius**: Users with older devices may experience jank
**Mitigation**:
- Use CSS transforms (GPU accelerated)
- Respect `prefers-reduced-motion`
- Test on representative devices
- Implement motion reduction automatically

### Risk 2: Design Token Conflicts with Docusaurus Defaults
**Impact**: Low
**Blast Radius**: Some Docusaurus styles may override tokens
**Mitigation**:
- Use specific CSS selectors
- Override Infima variables first
- Test in isolation before integration
- Document override strategy

### Risk 3: Scope Creep During Implementation
**Impact**: Medium
**Blast Radius**: Timeline delays, feature bloat
**Mitigation**:
- Strict acceptance criteria
- Phase gates with review
- Feature flags for non-essential items
- Clear MVP definition

### Risk 4: Placeholder Assets May Delay Progress
**Impact**: Low
**Blast Radius**: Visual gaps in demo
**Mitigation**:
- SVG placeholders can be created quickly
- CSS-only gradients as fallback
- Clear "Coming Soon" styling

---

## File Inventory

### New Files Created
```
src/css/tokens.css          # Design tokens
src/css/animations.css      # Animation keyframes
src/css/layout.css          # Layout utilities
src/components/HeroBanner/index.tsx
src/components/HeroBanner/styles.module.css
src/components/HeroBanner/GradientMesh.tsx
src/components/ModuleCard/index.tsx
src/components/ModuleCard/styles.module.css
src/components/ChapterCard/index.tsx
src/components/ChapterCard/styles.module.css
src/theme/Banner/index.tsx
src/theme/Banner/styles.module.css
static/img/placeholders/*.svg
```

### Files Modified
```
docusaurus.config.ts
src/pages/index.tsx
src/css/custom.css
sidebars.ts
```

### Files Deleted (if any)
```
None
```

---

## Success Criteria Validation

### Phase 1 Validation
- [ ] Tokens CSS compiles without errors
- [ ] Theme toggle appears in navbar
- [ ] Navbar links navigate correctly
- [ ] Footer displays all sections
- [ ] Sidebar collapsible works

### Phase 2 Validation
- [ ] Hero banner animates smoothly
- [ ] Module cards respond to hover
- [ ] Chapter cards display properly
- [ ] Homepage loads all content
- [ ] Navigation works correctly

### Phase 3 Validation
- [ ] Scroll animations trigger
- [ ] Page transitions feel smooth
- [ ] Banner MDX works in docs
- [ ] All hover states present
- [ ] Motion preferences respected

### Phase 4 Validation
- [ ] All placeholder images load
- [ ] Lighthouse scores meet targets
- [ ] No console errors
- [ ] Hot reload < 1 second
- [ ] Accessibility audit passes

---

## Estimated Timeline

| Phase | Effort | Dependencies |
|-------|--------|--------------|
| Phase 1: Foundation & Theme | 4-6 hours | None |
| Phase 2: Homepage & Navigation | 8-12 hours | Phase 1 |
| Phase 3: Motion & Content | 6-8 hours | Phase 2 |
| Phase 4: Assets & Performance | 4-6 hours | Phase 3 |
| **Total** | **22-32 hours** | - |

---

## References

- Docusaurus Theming: https://docusaurus.io/docs/styling/layout
- MDX Components: https://docusaurus.io/docs/markdown/react
- CSS Custom Properties: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- Motion Safety: https://web.dev/prefers-reduced-motion/
