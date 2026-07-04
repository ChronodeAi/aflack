# Backlog Lane — "Vice Fly-Through" B2B Product (Miami Local Businesses)

**Created**: 2026-07-04 · **Status**: BACKLOG — activate after FIFA content sprint (operator directive: FIFA first)
**One-liner**: Turn any physical Miami business into a cinematic game-world fly-through — GTA6-style neon Miami aesthetic — delivered free as the cold-outreach hook, converting to paid promo content + ongoing services.

## The product

1. **Input**: public imagery of the business — Google Maps/Street View, their own Instagram photo library, website photos.
2. **Build**: Higgsfield image-reference pipeline recreates the venue in our neon-Miami "Vice" world style (same aesthetic engine as the Vice-final series). Reference chain: their photos → stylized stills → Seedance fly-through.
3. **The video** (barbershop reference example the operator liked): POV glide through the front door → orbit a client mid-service (haircut in chair) → holographic floating UI showing services/styles/prices → transition to second service vignette (shave/facial) → exit shot with CTA. Template adapts per business type (restaurant: kitchen→plate→table; gym: floor→equipment→classes).
4. **Why it converts**: massive free value upfront; ties their real venue to the biggest cultural moment in Miami's history (GTA6, Nov 19); reputation flywheel ("this place is so Miami it's in the game-world").

## Outreach motion (AI agent + CRM)

- Prospect list: Miami businesses with active IG presence (scrape public directory + IG).
- **Video-first cold outreach**: the finished fly-through IS the first message — IG DM (if on IG), email fallback, cold call last. "We made this for you" > any pitch text.
- AI agent handles: prospect research → video brief → generation → personalized DM/email → follow-up sequencing → CRM capture (wire into event store, ADR-0002; agentmail/agentphone infra already in browser tabs).
- Human gate before send (at least in v1): outreach is outward-facing + platform-ToS-sensitive.

## Compliance rails (BLOCKING — same discipline as content lanes)

- **Never market as "inside GTA6" / "in the game."** That sells a commercial service on Rockstar's trademark and implies affiliation → C&D magnet. Frame: "Vice-style," "neon-Miami game-world," "Miami 2026 aesthetic." Sales conversation can reference the GTA6 moment; the artifact and copy stay original-style.
- Zero Rockstar assets/footage/frames in the pipeline (existing gate applies).
- Business's own photos as references: fine for a private demo delivered TO the rights holder; do NOT publish publicly before they consent (their likeness/venue, their call). Public posting = after signed engagement.
- Outreach: personalized 1:1, human-approved sends in v1; respect IG automation ToS + CAN-SPAM on email.
- People in generated scenes: synthetic, non-identifiable — never recreate real staff/customers from their photos without consent.

## Why this slots into the factory (not a distraction)

- Reuses: Higgsfield world engine, the Vice aesthetic (already canon), reference-chain workflow (proven today), Postiz publishing, event-store CRM.
- Diversifies revenue: B2B service income decoupled from view-RPM — the factory's first non-virality revenue line, sold USING virality craft.
- Natural sequencing: FIFA sprint (now, ends ~Jul 19) → GTA6 wave content (Jul-Nov) → fly-through product rides the same wave with local businesses as GTA6 launch approaches (peak "Miami = Vice" cultural salience).

## Activation checklist (when pulled from backlog)

- [ ] Pick 3 pilot businesses (barbershop, restaurant, gym) with strong IG photo libraries
- [ ] Build 1 spec-quality demo end-to-end; measure production cost/time per video
- [ ] Draft outreach scripts + CRM schema in event store
- [ ] Price the ladder (free demo → paid package → monthly content retainer)
- [ ] Legal once-over on style framing + outreach compliance
