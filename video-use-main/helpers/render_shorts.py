"""Render individual short-vertical clips from a highlights EDL.

Each clip in edl["clips"] → edit/clips_vertical/clip_NN_BEAT.mp4

Pipeline per clip:
  1. Extract with crop + scale to 1080×1920, 30ms audio fades
  2. Build per-clip SRT (UPPERCASE 2-word chunks, output-timeline offsets)
  3. Burn subtitles LAST with bold-overlay force_style
  4. Two-pass loudness normalize to -14 LUFS / -1 dBTP / LRA 11

Usage:
    python helpers/render_shorts.py edit/edl.json
    python helpers/render_shorts.py edit/edl.json --preview   # faster, CRF 22
    python helpers/render_shorts.py edit/edl.json --clips 1 3 6  # subset by id
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# Vertical bold-overlay subtitle style.
# Slightly larger than the horizontal preset (18→24, MarginV 35→50)
# to account for the taller, narrower frame.
SUB_FORCE_STYLE = (
    "FontName=Helvetica,FontSize=24,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,"
    "BorderStyle=1,Outline=2,Shadow=0,"
    "Alignment=2,MarginV=50"
)

LUFS_TARGET = -14.0
TP_TARGET   = -1.0
LRA_TARGET  = 11.0
PUNCT_BREAK = set(".,!?;:")


# ── SRT builder ──────────────────────────────────────────────────────────────


def srt_ts(s: float) -> str:
    ms = int(round(s * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    sec, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def build_clip_srt(transcript: dict, seg_start: float, seg_end: float) -> str:
    """2-word UPPERCASE chunks aligned to word-level timestamps.
    Output timestamps are relative to the clip (start = 0).
    """
    words = [
        w for w in transcript.get("words", [])
        if w.get("type") == "word"
        and w.get("start") is not None
        and w.get("end") is not None
        and w["end"] > seg_start
        and w["start"] < seg_end
    ]

    chunks: list[list[dict]] = []
    current: list[dict] = []
    for w in words:
        text = (w.get("text") or "").strip()
        if not text:
            continue
        current.append(w)
        ends_punct = text[-1] in PUNCT_BREAK
        if len(current) >= 2 or ends_punct:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)

    lines: list[str] = []
    for i, chunk in enumerate(chunks, 1):
        a = max(0.0, chunk[0]["start"] - seg_start)
        b = max(0.0, chunk[-1]["end"] - seg_start)
        if b <= a:
            b = a + 0.4
        text = " ".join((w.get("text") or "").strip() for w in chunk)
        text = re.sub(r"\s+", " ", text).strip().rstrip(",;:").upper()
        lines += [str(i), f"{srt_ts(a)} --> {srt_ts(b)}", text, ""]

    return "\n".join(lines)


# ── Loudnorm ──────────────────────────────────────────────────────────────────


def measure_loudness(path: Path) -> dict | None:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(path),
        "-af", f"loudnorm=I={LUFS_TARGET}:TP={TP_TARGET}:LRA={LRA_TARGET}:print_format=json",
        "-vn", "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    s, e = proc.stderr.rfind("{"), proc.stderr.rfind("}")
    if s == -1 or e <= s:
        return None
    try:
        return json.loads(proc.stderr[s : e + 1])
    except json.JSONDecodeError:
        return None


def apply_loudnorm(src: Path, dst: Path, preview: bool = False) -> None:
    if preview:
        filt = f"loudnorm=I={LUFS_TARGET}:TP={TP_TARGET}:LRA={LRA_TARGET}"
    else:
        m = measure_loudness(src)
        if m is None:
            print("        loudnorm measure failed — falling back to 1-pass")
            apply_loudnorm(src, dst, preview=True)
            return
        filt = (
            f"loudnorm=I={LUFS_TARGET}:TP={TP_TARGET}:LRA={LRA_TARGET}"
            f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
            f":offset={m['target_offset']}:linear=true"
        )

    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(src),
        "-c:v", "copy",
        "-af", filt,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(dst),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


# ── Per-clip render ───────────────────────────────────────────────────────────


def render_clip(
    clip: dict,
    source_path: Path,
    transcript: dict,
    crop_filter: str,   # just the crop= part — scale is added here
    out_dir: Path,
    preview: bool,
) -> Path:
    n      = clip["id"]
    beat   = clip["beat"]
    start  = float(clip["start"])
    end    = float(clip["end"])
    dur    = end - start
    fade_st = max(0.0, dur - 0.03)

    preset = "medium" if preview else "fast"
    crf    = "22"     if preview else "20"

    raw    = out_dir / f"clip_{n:02d}_{beat}_raw.mp4"
    subbed = out_dir / f"clip_{n:02d}_{beat}_subbed.mp4"
    final  = out_dir / f"clip_{n:02d}_{beat}.mp4"

    # 1. Extract: crop → scale to 1080×1920, audio fades, 30fps
    vf = f"{crop_filter},scale=1080:1920"
    af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={fade_st:.3f}:d=0.03"

    print(f"  [{n:02d}] {start:.1f}–{end:.1f}s ({dur:.1f}s)  {beat}")
    print(f"        extract + crop …")
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-ss", f"{start:.3f}", "-i", str(source_path),
        "-t", f"{dur:.3f}",
        "-vf", vf, "-af", af,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(raw),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    # 2. Build per-clip SRT
    srt_path = out_dir / f"clip_{n:02d}.srt"
    srt_path.write_text(build_clip_srt(transcript, start, end))

    # 3. Burn subtitles LAST (Hard Rule 1)
    srt_abs = str(srt_path.resolve()).replace(":", r"\:").replace("'", r"\'")
    print(f"        burn subtitles …")
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(raw),
        "-vf", f"subtitles='{srt_abs}':force_style='{SUB_FORCE_STYLE}'",
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(subbed),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    raw.unlink(missing_ok=True)
    srt_path.unlink(missing_ok=True)

    # 4. Loudness normalize → social-ready
    print(f"        loudnorm (-14 LUFS) …")
    apply_loudnorm(subbed, final, preview=preview)
    subbed.unlink(missing_ok=True)

    size_mb = final.stat().st_size / 1024 / 1024
    print(f"        ✓ {final.name}  ({size_mb:.1f} MB)")
    return final


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    ap = argparse.ArgumentParser(description="Render highlight shorts from an EDL")
    ap.add_argument("edl", type=Path, help="Path to edl.json")
    ap.add_argument("--preview", action="store_true", help="CRF 22, 1-pass loudnorm — faster")
    ap.add_argument("--clips", nargs="+", type=int, metavar="ID",
                    help="Render only these clip IDs (e.g. --clips 1 3 6)")
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"edl not found: {edl_path}")

    edl       = json.loads(edl_path.read_text())
    edit_dir  = edl_path.parent
    sources   = edl["sources"]
    profiles  = edl.get("crop_profiles", {})
    clips     = edl["clips"]

    if args.clips:
        clips = [c for c in clips if c["id"] in args.clips]
        if not clips:
            sys.exit(f"no clips matched IDs: {args.clips}")

    out_dir = edit_dir / "clips_vertical"
    out_dir.mkdir(parents=True, exist_ok=True)

    transcripts_dir = edit_dir / "transcripts"

    print(f"rendering {len(clips)} clip(s) → {out_dir}/")
    if args.preview:
        print("  (preview mode: CRF 22, 1-pass loudnorm)")

    rendered: list[Path] = []
    for clip in clips:
        src_name  = clip["source"]
        src_path  = Path(sources[src_name])
        if not src_path.is_absolute():
            src_path = (edit_dir / src_path).resolve()

        tr_path   = transcripts_dir / f"{src_name}.json"
        transcript = json.loads(tr_path.read_text()) if tr_path.exists() else {}

        # Crop profile: strip the trailing scale=… (render_clip appends its own)
        profile_str = profiles.get(clip.get("crop", "single_dominant"), "")
        crop_filter = profile_str.split(",scale=")[0] if profile_str else ""

        rendered.append(
            render_clip(clip, src_path, transcript, crop_filter, out_dir, args.preview)
        )

    print(f"\ndone — {len(rendered)} clip(s) in {out_dir}/")
    for p in rendered:
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
