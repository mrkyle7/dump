# 112cam daily highlight reel

Builds a short video from the 112cam "Person Detected" snapshot emails received in the last 24 hours.

> **Never commit or upload the snapshots or videos.** This repo is public and the images show the
> house, people and number plates. Media lives only in the session scratchpad and is delivered to
> the user with `SendUserFile`. `.gitignore` already excludes `*.mp4`, `*.jpg` and `112cam_images/`.

## Steps

1. **Find the emails** with the Gmail connector:
   `search_threads` query `label:112cam newer_than:2d`, `pageSize: 50` (paginate if needed).
   Keep only messages whose `date` (UTC) is within 24h of `date -u` now. Each alert is a one-message
   thread with subject `Person Detected from 112cam at YYYY/MM/DD hh:mm:ss` and one JPEG attachment
   (2560x1920).
2. **Download the images.** There is no attachment-download tool, so call `get_message` with
   `messageFormat: RAW` for each message. The result is too big for context and gets saved to a file
   under `~/.claude/projects/.../tool-results/`; the error text gives the path. Extract the JPEG:
   ```bash
   python3 -I 112cam/extract.py <saved-result.txt> $SCRATCH/imgs
   ```
3. **Caption the frames** (sorted by filename = chronological, camera local time). This writes each
   snapshot plus a separate caption-bar PNG, which render.sh overlays after the zoom so it isn't cropped:
   ```bash
   python3 -I 112cam/caption.py $SCRATCH/imgs $SCRATCH/frames
   ```
4. **Render**:
   ```bash
   112cam/render.sh $SCRATCH/frames $SCRATCH/112cam_highlights_$(date +%F).mp4
   ```
   Each snapshot gets 3s with a slow zoom and 0.5s crossfades, so 8 images ≈ 20.5s.
   Note: inputs must be single images (no `-loop`), or zoompan multiplies the length.
5. **Check** one frame (`ffmpeg -ss 5 -i out.mp4 -frames:v 1 check.jpg`) and look at it.
6. **Deliver** the video with `SendUserFile` (`display: render`) and a one-line caption listing
   how many alerts and their times. If there were no alerts in the window, just say so.

Requirements: `ffmpeg`, Python 3 with Pillow (if missing: `python3 -m pip install pillow`, using the same
interpreter that runs the scripts).

The scheduled task ("112cam daily highlight reel", 18:53 UK daily) carries its own copy of these
scripts in its prompt, because cloud sessions refuse to run scripts cloned from GitHub. When you change
a script here, update the task's prompt too.
