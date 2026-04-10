# ffmpeg Clip Pipeline Pattern

**Date**: 2026-03-05
**Source**: Paji-Affiliate-Gen + Paji-editz reference

## Pattern: Video-Only Intermediate Clips

When building a multi-clip video pipeline (trim → concat → merge audio):

**DO**: Trim clips as video-only (`-an`)
**DO**: Normalize fps and pixel format during trim
**DO**: Add audio only at the final merge step
**DON'T**: Try to preserve source audio through intermediate clips

```python
# Trim — video only, normalized
ffmpeg -y -i src -t {trim_t} \
  -vf "scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p" \
  -c:v libx264 -preset ultrafast -crf 23 \
  -an -avoid_negative_ts make_zero \
  clip_N.mp4

# Concat — safe because all clips are identical codec/fps/format
ffmpeg -f concat -safe 0 -i clips.txt -c copy concat.mp4

# Final merge — audio added here only
ffmpeg -i concat.mp4 -i audio.wav -map 0:v -map 1:a \
  -c:v libx264 -preset fast -crf 23 -c:a aac -shortest output.mp4
```

## Why

- Source clips may have no audio stream → ffmpeg fails or produces corrupt output
- Mixed audio streams across clips cause concat demuxer issues
- fps/format normalization is REQUIRED for `-c copy` concat to work cleanly

## Reference

- Paji-editz `core/video.py` `create_slideshow_video()` — uses `-an` for all intermediate clips
- Paji-Affiliate-Gen `video/editor.py` — applied this pattern after 3 failed attempts with audio preservation
