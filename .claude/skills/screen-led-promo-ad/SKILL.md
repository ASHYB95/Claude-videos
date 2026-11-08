---
name: screen-led-promo-ad
description: Make a fast-paced vertical (9:16) brand/product promo ad that cuts AI-generated B-roll (Higgsfield) with on-brand recreations of the product's real app/website screens in a 3D phone, with ElevenLabs voiceover, synthesised music and SFX, rendered with HyperFrames. Use when the user wants a SaaS/app/website ad, "show how easy it is", a product walkthrough ad, or a professional social ad with B-roll + screens (reference: collection-pot/).
---

# Screen-led promo ad (B-roll + real screens)

Reference build: `collection-pot/` (32 s ad). Read its `index.html`, `TREATMENT.md` and `audio/` before starting — copy patterns, don't reinvent.

## The format
- 9:16, 1080×1920, 30 fps, ~30–35 s. **Fast**: B-roll shots on screen 1.0–2.8 s, cut on VO beats.
- Structure: hook B-roll with kinetic type (the pain) → B-roll of phone pickup **with the real site tracked onto its screen** → match-cut *through* the screen into a 3D phone on a brand stage → 3 numbered setup steps with a running timer → B-roll with notification toasts → product payoff (money/spend) → emotional B-roll payoff → end card that mirrors the brand's own homepage hero.
- Camera: push-ins that follow each tap, tilt to the button, pull-backs for 3D pop-outs (link, QR, avatars, cards). Motion blur on (`data-motion-blur="on"`, shutter 180).
- Transitions: whip pans, brand-colour wipes (single and double), match cut through the phone screen.

## Workflow (get approval at each ★)
1. **Research the brand**: fetch the site (add hosts to the cloud environment if blocked: site, app subdomain, image CDN). Extract real copy/claims, hex colours (CSS), fonts, logo + mascot SVGs. Only use claims the site makes.
2. ★ **Script** as a table: time · visual (🎬 B-roll / 📱 screen) · VO. Keep VO ~70–80 words for 30 s.
3. **Capture real screens** with Playwright through the proxy (`chromium.launch({proxy:{server:process.env.HTTPS_PROXY}})`, mobile 430×932 @2x). Stub trackers; if Next.js chunks 404 in Chrome, fulfil `/_next/static/chunks/` via `curl` (see `collection-pot/reference/capture-flow.js`). Click through the real flow and stop before sign-up.
4. ★ **Quote Higgsfield credits** (`generate_video` with `get_cost:true`) and get approval. B-roll: `seedance_2_5`, 9:16, 5 s, 1080p, `generate_audio:false` (~80 credits each). Prompts: "commercial", camera move, light, "no readable text, no logos". For the pickup shot ask for "the phone's softly glowing **blank** screen fills the frame" → screen replacement.
5. Download clips (add the Higgsfield CDN host if blocked), **transcode HEVC → H.264** (`-c:v libx264 -crf 15 -pix_fmt yuv420p -r 30`) — headless Chrome can't decode HEVC.
6. **Screen replacement**: retime the pickup clip, then `scripts/screen_replace.py <screenshot.png>` tracks the white screen per frame and composites the real homepage (thumb/notch stay on top). Freeze its last frame and start the UI scene with the phone screen at the exact same rect (clip-path iris out) for an invisible match cut.
7. **VO**: `scripts/tts.py` with `voices/lines.json` (`[id, voice_id, text]`), `eleven_multilingual_v2`, `/with-timestamps` → word timings for sync. `speed` ~1.08 for a punchy ad. Join run-on lines (e.g. the 3 steps) into one take.
8. **Build `index.html`** (HyperFrames + vendored GSAP — `vendor/gsap.min.js`, CDN is blocked in render). Rebuild app screens in HTML at the site's logical width (430) scaled ×1.293 into a 556×1196 screen; brand fonts (OFL look-alike if the brand font is commercial — compare side by side). **Measure tap targets lazily** with function-based GSAP values (`ctr(sel)`), never guessed pixels.
9. Snapshot (`npx hyperframes snapshot --at …`) every few seconds, read the contact sheets, fix overlaps/clipping. ★ Show the user frames before the full render if direction is uncertain.
10. **Audio**: `scripts/score_upbeat.py` (120 BPM major, bar-aligned drops), `scripts/sfx.py` (ElevenLabs SFX; music API needs a paid plan), `scripts/mix.py` (VO on top, music ducked, per-SFX trims from measured mean volume, loudnorm −14 LUFS). Check VO vs music RMS numerically — you can't listen.
11. Render: `npx hyperframes render -q delivery -o renders/<name>.mp4` (background; ~8–10 min). Verify frames + loudness, copy to project root, write `.srt` from alignment, `CREDITS`, commit.

## Gotchas
- Lint errors to pre-empt: CSS `transform` on GSAP-animated elements, `letterSpacing` tweens, template-literal `querySelector`, fonts without `@font-face` (bundle emoji font if used).
- Repeated `fromTo` on one element: `immediateRender:false` on later ones (else ripples/rings show at t=0).
- Headlines meant to span a match cut must live in an overlay layer above the clipped scene.
- Never invent stats; keep characters/companies fictional; no third-party logos.
