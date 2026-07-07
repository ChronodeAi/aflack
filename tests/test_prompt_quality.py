from __future__ import annotations

import unittest
from pathlib import Path

from aflack.prompt_quality import check_short_asset_prompt


class PromptQualityTests(unittest.TestCase):
    def test_safe_but_generic_product_prompt_fails(self):
        prompt = (
            "Vertical 9:16 macro close-up of a generic matte-black game controller with no logos. "
            "A floating neutral analog-stick test grid overlays the right stick; the crosshair cursor "
            "drifts slowly on its own, then a signal-yellow tag snaps in reading FIX FIRST. Precise "
            "technical UI animation. Bright studio lighting with teal, white, and signal-yellow accents "
            "on a clean black gaming desk. Fast editorial camera moves. No real brand logos, no Rockstar "
            "or Take-Two logos, no GTA footage, no game UI, no trailer frames, no real-person likeness, "
            "no readable third-party marks. Mood: practical, honest, buyer-guide, launch prep."
        )

        result = check_short_asset_prompt(prompt)

        self.assertFalse(result.passed)
        self.assertIn("missing positive GTA6/day-one/Vice relevance anchor", result.blocks)
        self.assertIn("missing visible payoff or end-state reveal", result.blocks)

    def test_story_native_gta_prompt_passes(self):
        prompt = (
            "Vertical 9:16 GTA6 day-one setup audit scene. Opening frame: a controller sits under a "
            "neon countdown reading LAUNCH NIGHT, while the analog stick drifts by itself. Crash zoom "
            "to the stick test as the UI fails, then a yellow FIX FIRST label snaps on. The final frame "
            "reveals the whole boring-smart day-one setup checklist and loops back to the first frame. "
            "No real brand logos, no Rockstar or Take-Two logos, no GTA footage, no trailer frames, "
            "no real-person likeness."
        )

        result = check_short_asset_prompt(prompt)

        self.assertTrue(result.passed)
        self.assertEqual(result.blocks, [])

    def test_loadout_lab_v2_prompt_pack_passes_quality_gate(self):
        package = Path(".aiwg/marketing/loadout-lab/episode-001-affiliate-package.md")
        text = package.read_text()
        prompt_pack = text.split("### Rejected v1 Prompt Pattern", 1)[0]
        prompts = [line[2:].strip() for line in prompt_pack.splitlines() if line.startswith("> Vertical 9:16")]

        self.assertEqual(len(prompts), 6)
        for prompt in prompts:
            with self.subTest(prompt=prompt[:80]):
                result = check_short_asset_prompt(prompt)
                self.assertTrue(result.passed, result.blocks)
                self.assertEqual(result.blocks, [])


if __name__ == "__main__":
    unittest.main()
