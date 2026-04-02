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
