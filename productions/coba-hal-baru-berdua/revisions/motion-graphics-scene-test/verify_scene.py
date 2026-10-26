"""Verify the isolated scene in the assembled HyperFrames preview."""
import asyncio
import hashlib
import json
import re
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright

TRIAL = Path(__file__).resolve().parent
PROOF = TRIAL / "video/verification/seek"


async def main():
    preview = json.loads((TRIAL / "PREVIEW.json").read_text(encoding="utf-8"))
    assert urllib.request.urlopen(preview["serverUrl"], timeout=10).status == 200
    PROOF.mkdir(parents=True, exist_ok=True)
    errors = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True, args=["--autoplay-policy=no-user-gesture-required"]
        )
        try:
            page = await browser.new_page(viewport={"width": 1600, "height": 1000})
            page.on("pageerror", lambda error: errors.append(str(error)))
            await page.goto(preview["studioUrl"])
            # The player iframe lives in Studio's shadow DOM; Playwright locators pierce it.
            await page.locator("iframe").first.wait_for(state="attached")
            iframe = await page.locator("iframe").first.element_handle()
            frame = await iframe.content_frame()
            await frame.wait_for_function("window.__playerReady === true")
            await frame.evaluate("document.fonts.ready.then(() => true)")
            canvas = frame.locator('[data-composition-id="main"]').first
            hashes = {}
            seeks = []
            times = [3.72125, 4.08125, 4.90125, 5.811, 7.74125, 8.14125,
                     3.72125, 4.90125, 7.74125, 4.08125, 5.811]
            for index, time in enumerate(times):
                await frame.evaluate("time => window.__player.seek(time)", time)
                await page.wait_for_timeout(160)
                state = await frame.evaluate("""() => ({
                  time: window.__player.getTime(),
                  words: ['f12-word-coba', 'f12-word-bareng'].map(id => {
                    const element = document.getElementById(id);
                    if (!element) return {id, missing:true};
                    const style = getComputedStyle(element);
                    const box = element.getBoundingClientRect();
                    return {id, opacity:Number(style.opacity), transform:style.transform,
                            x:box.x, y:box.y, width:box.width, height:box.height};
                  })
                })""")
                png = await canvas.screenshot(path=str(PROOF / f"seek-{index:02d}.png"))
                digest = hashlib.sha256(png).hexdigest()
                state.update(requested_time=time, screenshot_sha256=digest)
                if time in hashes:
                    state["matches_earlier_seek"] = digest == hashes[time]
                    assert state["matches_earlier_seek"], f"Reverse seek differs at {time}s"
                hashes[time] = digest
                # The 30 fps host quantizes seeks to its frame grid.
                assert abs(state["time"] - time) <= 1 / 30 + 1e-6, state
                seeks.append(state)

            await frame.evaluate("window.__player.seek(0)")
            await page.get_by_role("button", name=re.compile(r"^Play", re.I)).first.click()
            playback = []
            for _ in range(7):
                await page.wait_for_timeout(2000)
                sample = await frame.evaluate("""() => ({
                  time:window.__player.getTime(), playing:window.__player.isPlaying(),
                  audio:[...document.querySelectorAll('audio')].map(audio => ({
                    id:audio.id, time:audio.currentTime, paused:audio.paused,
                    ready:audio.readyState, error:audio.error?.message || null
                  }))
                })""")
                playback.append(sample)
            await frame.evaluate("window.__player.pause()")
            assert playback[0]["time"] > 1
            assert playback[-1]["time"] >= 12.2
            for sample in playback:
                assert all(audio["error"] is None for audio in sample["audio"])
                voice = next(audio for audio in sample["audio"] if audio["id"] == "test-narration")
                assert voice["ready"] >= 2
                if sample["playing"]:
                    assert abs(voice["time"] - (62.1695 + sample["time"])) < 0.3
            assert not errors, errors
            await page.screenshot(path=str(PROOF.parent / "studio-preview.png"))
            report = {
                "ok": True, "http_status": 200, "seeks": seeks,
                "repeated_seek_pixel_matches": sum("matches_earlier_seek" in seek for seek in seeks),
                "playback": playback, "page_errors": errors,
                "listening_limit": "Playback, media readiness, timing and error state verified programmatically; no direct perceptual listening claimed.",
            }
            (TRIAL / "runtime-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"ok": True, "seeks": len(seeks),
                              "repeated_seek_pixel_matches": report["repeated_seek_pixel_matches"],
                              "last_playback_time": playback[-1]["time"], "page_errors": errors}))
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
