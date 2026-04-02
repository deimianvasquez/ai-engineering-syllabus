# Wanderlust Explorer - Reference solution

This README documents the reference solution for **"Wanderlust Explorer with React and Next.js"**.

## Recommended solution structure

A reference implementation should include:

- `src/app/page.tsx` (Home)
- `src/app/experiences/page.tsx` (Explorer)
- `src/app/experiences/[id]/page.tsx` (Experience detail)
- `src/app/favorites/page.tsx` (Favorites)
- `src/app/profile/page.tsx` (Profile)
- `src/components/` for reusable UI components
- `src/data/experiences.ts` with the 100-item dataset
- `src/hooks/useExperiences.ts` (or similar custom hook)

## What this reference solution demonstrates

- URL-driven filtering with search, category, and destination query params.
- Correct query param prefill using `useSearchParams` and router updates.
- Case-insensitive regex search over experience titles.
- Favorites managed in shared React `useState` without external state libraries.
- Reusable component architecture (`Navbar`, `SearchBar`, `FilterBar`, `ExperienceCard`).

## URL filters and regex implementation guide

### 1) Read and prefill values from the URL

On `/experiences`, read current query params with `useSearchParams` and initialize controlled inputs from those values:

- `search`: free-text query
- `category`: one of the allowed categories
- `destination`: city/country filter

Recommended defaults:

- `searchParams.get("search") ?? ""`
- `searchParams.get("category") ?? ""`
- `searchParams.get("destination") ?? ""`

This guarantees that opening a shared URL such as `/experiences?search=sailing&category=Adventure` preloads the same filtered state in the UI.

### 2) Update query params with `usePathname` + router navigation

Use `usePathname` to keep the current route base (`/experiences`) and update only the query string when filters change:

1. Create `new URLSearchParams(searchParams.toString())`
2. Set or delete each key depending on whether input is empty
3. Push the updated URL with the current pathname

Expected result pattern:

- `router.push(\`\${pathname}?\${params.toString()}\`)`

This keeps filters shareable and avoids hardcoding route strings in multiple places.

### 3) Apply the regex safely for title search

The filter must use a case-insensitive regex against `experience.title`.
To avoid runtime errors with special characters (`(`, `[`, `*`, etc.), escape user input before building the regex.

Suggested flow:

1. `const term = search.trim()`
2. If empty, skip title filter
3. Escape term (for example: `term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")`)
4. Build regex with `i` flag and test each title

Reference matcher:

- `new RegExp(escapedTerm, "i").test(experience.title)`

This satisfies the rubric requirement and keeps behavior stable for edge-case inputs.

## Expected behavior checklist

Use this checklist to validate student submissions:

- [ ] Routes `/`, `/experiences`, `/experiences/[id]`, `/favorites`, and `/profile` are implemented and navigable.
- [ ] Explorer renders the full dataset and updates results when search or filters change.
- [ ] Search uses regex matching against title with case-insensitive behavior.
- [ ] Category and destination filters can be combined with search.
- [ ] Query params are reflected in the URL and inputs are prefilled on reload.
- [ ] Favorite toggle updates card state and favorites page content.
- [ ] "No results found" appears when filters return zero experiences.
- [ ] App is responsive and navbar active links reflect the current route.

## Reviewer notes

- Persistence with `localStorage` is optional and not required for passing criteria.
- Primary assessment criteria are routing, URL-state synchronization, and component composition.
