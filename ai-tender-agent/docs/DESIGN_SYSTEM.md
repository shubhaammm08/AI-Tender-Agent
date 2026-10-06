# Design System

Minimal, white and green. Calm, plain, easy for a shop owner to read.

## Colors

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | #FFFFFF | #0E1511 | Page background |
| `--soft` | #F3FAF5 | #141E18 | Hover, selected rows |
| `--ink` | #14231A | #E7EFE9 | Main text |
| `--mute` | #66756B | #93A399 | Secondary text |
| `--line` | #E4EBE6 | #25322A | Borders |
| `--g` | #15803D | #4ADE80 | Primary green |
| `--gd` | #116B33 | #86EFAC | Primary hover |
| `--gl` | #DCF3E3 | #16301F | Soft green fills |
| `--red` / `--redbg` | #B42318 / #FDE8E6 | #F4887F / #3A1B18 | Problems |
| `--amb` / `--ambbg` | #9A6200 / #FDF1D6 | #F2BB55 / #392B10 | Warnings |

Green means good or primary action. Amber means check. Red means a problem. Never use color alone to carry meaning. Pair it with a label.

## Typography

DM Sans. Sizes: 21px page title, 16px card title, 14.5px body, 13px secondary. Weights 400, 500, 600, 700. Sentence case everywhere. Line length under 80 characters.

## Layout

- Left sidebar (200px): Tenders, Document vault, My bids. Becomes a top scroll bar on mobile.
- Main area: three summary stats, then a two-column split (list and detail). Single column on mobile.
- Radius 6 to 8px. 1px borders. No heavy shadows or gradients.

## Components

| Component | Rule |
|---|---|
| Primary button | Green fill, white text, one per view |
| Pill badge | Soft background, 12px, 600 weight, for status |
| List item | Bordered row, green border when selected |
| Card | 1px border, 16px padding |
| Table | Muted header, 1px row dividers |
| Progress bar | 6px, soft green track, green fill |

## Copy

- Use plain words: "Prepare bid", "Upload document", "Renew by 31 Mar 2027".
- A button keeps the same name in the toast that follows it.
- Errors say what happened and how to fix it. They do not apologize.
- Empty states tell the user what to do next.

## Accessibility

- Contrast at least 4.5:1 for text.
- Visible keyboard focus (2px green outline).
- Support light and dark mode and reduced motion.
- Touch targets at least 40px high on mobile.

## Reference

A working prototype of these rules is the file `tender-agent-ui.html`.
