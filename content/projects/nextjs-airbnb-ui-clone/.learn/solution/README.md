# Airbnb UI Clone - Reference solution

This README documents the reference solution for **"Building an Airbnb UI Clone with Next.js and React"**.

## Recommended solution structure

A reference implementation should include:

- `app/page.tsx` (Home)
- `app/catalog/page.tsx` (Catalog)
- `app/rooms/[id]/page.tsx` (Room detail)
- `components/` for reusable UI components
- `types/` for TypeScript interfaces
- `context.md` at project root with the vision-to-spec notes

## What this reference solution demonstrates

- Mobile-first implementation at 375px with desktop adaptations from 768px and up.
- Reusable listing card component shared between Home and Catalog.
- Correct use of `useState` for search, category filtering, sorting, gallery index, and guest counter.
- Correct use of `useEffect` to simulate async loading in Home and Room Detail.
- Internal navigation with Next.js `Link` (no full page reloads).

## Correct `useState` and `useEffect` usage in this project

Use this quick guide while reviewing or implementing the three pages:

- Keep `useState` for UI state only: search text, selected category, sort option, active photo index, guest count, and loading flags.
- Derive visible lists from state instead of storing duplicated state when possible (for example, derive filtered cards from `search` and `selectedCategory`).
- Update state with functional setters when next value depends on previous value, such as guest counters:
  - `setGuests((prev) => Math.min(MAX_GUESTS, prev + 1))`
  - `setGuests((prev) => Math.max(MIN_GUESTS, prev - 1))`
- Group related state by feature so each component owns one responsibility (search logic in search/list area, gallery state in gallery component, etc.).

For `useEffect`, follow these rules:

- Use it for side effects only (simulated fetch with `setTimeout`, subscriptions, timers), not for pure calculations.
- Home and Room Detail should trigger loading effects on mount, then clean up timers to avoid updates after unmount:
  - Create timeout inside `useEffect`.
  - Return cleanup with `clearTimeout(timeoutId)`.
- Include all external dependencies in the dependency array.
  - Mount-only simulated load: `[]`
  - Load by route param (room detail): `[id]`
- Avoid using `useEffect` to sync values that can be computed directly in render.

Practical patterns for this project:

- Home (`/`): `useState` for `search`, `activeCategory`, `isLoading`; `useEffect` for initial simulated data loading.
- Catalog (`/catalog`): `useState` for sort order; derive sorted cards from base data and selected order.
- Room Detail (`/rooms/[id]`): `useState` for `photoIndex`, `guests`, `isLoading`; `useEffect` to load room data when `id` changes.

Common mistakes to avoid:

- Duplicating the same list in multiple states (`allListings` and `visibleListings`) without a reason.
- Forgetting effect cleanup for timeouts.
- Missing dependencies in `useEffect`, causing stale values.
- Using `useEffect` for every state change when plain render logic is enough.

## Expected behavior checklist

Use this checklist to validate student submissions:

- [ ] `context.md` exists and documents pages, components, and user intent.
- [ ] Routes `/`, `/catalog`, and `/rooms/[id]` are implemented and navigable.
- [ ] Search filtering updates listing cards in real time.
- [ ] Category filter highlights the active selection.
- [ ] Catalog sorting control changes order by price (asc/desc).
- [ ] Room detail includes gallery, header, host info, amenities, and booking card.
- [ ] Guest counter enforces min/max boundaries.
- [ ] Loading states are visible while simulated fetch is pending.

## Reviewer notes

- Optional map integration and date picker are stretch goals and should not block passing the base rubric.
- The primary assessment criteria are component architecture, state management, and navigation behavior.
