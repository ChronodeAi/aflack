# Vice Signal EP001 — Final Render Candidate

**Date**: 2026-07-07  
**Package**: VS-EP001-PREGEN  
**Render**: candidate v2  
**Local file**: `media/vice-signal/ep001/final/final-render-candidate-v2.mp4`  
**SHA-256**: `9a889802444d168dafb45c6d1eb8e7ec9d8da41272ec424d33c4da100a33b0a3`  
**Size bytes**: 25313662  
**Duration**: 40.300000 seconds  
**Resolution**: 1080x1920  
**Frame rate**: 24 fps  
**Status**: assembled candidate; pending operator review; not approved for publishing

## What was executed

1. Downloaded the seven already-generated Seedance clips from the result URLs
   recorded in `.aiwg/marketing/vice-signal/episode-001-generation-2026-07-04.md`.
2. Concatenated S1-S7 into a 40.30 second vertical render.
3. Added burned-in caption overlays for each storyboard beat.
4. Added mandatory disclosure from 0:32 to end:
   `AI-generated visuals. Not affiliated with Rockstar Games. Links may be affiliate links.`
5. Added a simple original generated tone bed using local ffmpeg sine sources.
6. Generated QC frames under:
   `media/vice-signal/ep001/final/qc-frames-v2/`.

## Known limitations / uncertainties

- Local macOS `say` produced a zero-duration AIFF in this execution
  environment, so the candidate render does **not** include spoken VO.
- The audio bed is locally generated and rights-safe, but it is not yet a
  polished licensed/original synthwave music bed.
- This candidate is suitable for operator visual review and iteration, but it is
  **not final-publish approved** until the operator explicitly approves the
  render and separately approves public publish/scheduling.

## Output files

- Candidate render: `media/vice-signal/ep001/final/final-render-candidate-v2.mp4`
- Failed first candidate with clipped captions: `media/vice-signal/ep001/final/final-render-candidate-v1.mp4`
- Caption overlays: `media/vice-signal/ep001/final/overlays-v2/`
- QC frames: `media/vice-signal/ep001/final/qc-frames-v2/`
