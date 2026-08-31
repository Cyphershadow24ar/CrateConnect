# FRONTEND_GUIDELINES — Milestone 1

## 1. Product Style
Style direction:
- Clean
- Professional
- Food/sustainability oriented
- Modern SaaS dashboard
- Not overly decorative
- Strong hierarchy and readable data

Use the supplied project PDF sample dashboard only as visual inspiration. Do not copy its branding, text, or exact layout.

## 2. Design Principles
1. Clarity first — operational information should be immediately understandable.
2. Consistency — same controls behave the same across pages.
3. Efficiency — adding/updating inventory should require minimal steps.
4. Accessibility — keyboard-friendly and readable contrast.

## 3. Design Tokens
Create tokens in Tailwind-compatible form.

Color categories:
- Primary: deep green family
- Neutral: slate/gray family
- Success: green
- Warning: amber
- Error: red
- Info: blue

Do not hardcode arbitrary colors in individual components. Centralize tokens.

Typography:
- Use a clean sans-serif system/UI font stack.
- Establish consistent heading/body/caption hierarchy.

Spacing:
- Use a small consistent spacing scale.
- Avoid arbitrary pixel values where a token exists.

Radius:
- Small to medium rounded corners; cards should remain professional, not playful.

## 4. Required Components
Each component should have loading/error/disabled states where meaningful:
- Button
- Input
- Select
- Date picker/input
- Number input
- Search box
- Card
- Table
- Badge
- Modal/Dialog
- Alert
- Toast
- Empty State
- Loading Skeleton
- File Dropzone
- Scanner modal/panel
- Confirm Delete dialog

## 5. Dashboard
Show:
- Total inventory items
- Total quantity
- Expiring soon
- Expired
- Recent inventory activity

Keep the dashboard useful but avoid implementing future AI or NGO widgets.

## 6. Inventory Table
Columns:
- Product
- Category
- Quantity
- Unit
- Purchase Date
- Expiry Date
- Days to Expiry
- Status
- Barcode
- Actions

Status examples:
Expired / Critical / Warning / Safe

## 7. Forms
Inventory form fields:
- Product name
- Category
- Quantity
- Unit
- Purchase date
- Expiry date
- Barcode/QR value
- Optional storage type if present in the category model

Rules:
- Client-side validation for fast feedback.
- Server remains source of truth.
- Show field-level errors.
- Preserve entered values when a request fails.

## 8. Accessibility
Target WCAG 2.1 AA where practical:
- Keyboard navigation
- Visible focus
- Labels for inputs
- Semantic buttons/links
- Accessible dialog behavior
- Sufficient contrast
- Do not rely on color alone for expiry status

## 9. Responsive
Mobile-first:
- Inventory controls stack vertically.
- Forms become one column.
- Buttons remain touch-friendly.
- Scanner is usable on phone widths.
- Dashboard cards wrap cleanly.

Desktop:
- Use wider tables and multi-column dashboard regions.

## 10. Animation
Minimal:
- Fast hover/focus transitions
- Subtle modal/alert transitions
- Respect prefers-reduced-motion
- No decorative animation that delays workflows

## 11. Frontend Data Layer
- One HTTP client pattern.
- Central API base URL from environment.
- Consistent error mapping.
- Avoid duplicated fetch logic.
- Keep business/tenant context centralized.

## 12. UI State Coverage
Every page must define:
- Loading
- Success
- Empty
- Error
- Disabled/action-in-progress

No blank screens.
