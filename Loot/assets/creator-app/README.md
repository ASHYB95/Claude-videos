# LOOT Creator App: screens

66 screenshots of the creator app, in the order a creator meets them.

- **Size:** 1179 × 2556 px (iPhone 15 Pro, @3x), PNG, with an iOS status bar (9:41).
- **`-full` files:** the whole scrolling page in one tall image, good for scroll animations inside a phone mockup.
- **`__greenscreen` files:** the same shot with the feed videos replaced by pure green (#00FF00), so you can key in real creator footage in your editor.
- **Data:** everything shown is fictional demo data: creator "Riya Kapoor" and brands Brewbox, Glowlab, Paisa+, Nova Audio, FitFuel and Sneakr.

| Folder | What's in it |
| --- | --- |
| 01 Onboarding | Welcome, 4 tutorial slides, sign in, sign up (empty and filled) |
| 02 Profile Setup | All 13 questions of the profile form, answered |
| 03 Home | Notification prompt, pending-approval banner, home, feed, video player, analytics |
| 04 Loot | Mission marketplace, contracts list, brand page |
| 05 Mission Brief | Mission detail, script tabs (hooks, body, CTAs), specs, assets, the 3 other brief formats, applied state |
| 06 Studio | My missions, then the mission console in every state: start, video selected, under review, reshoot requested with feedback, approved and paid |
| 07 Profile & Stash | Profile, wallet balance and transactions |
| 08 Account States | Banned account, disapproved profile |

## Before publishing

The feed videos in the non-greenscreen shots are the sample clips in `LootApp/assets/sample_videos`.
They show real people and another company's branding, so for published videos use the
`__greenscreen` versions and key in footage from LOOT creators who have agreed to it.

## Regenerating

See `LootApp/demo-mode/README.md`. Edit `LootApp/demo-mode/demoData.js` to change names, brands or amounts, then re-run the capture script.
