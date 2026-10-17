#!/usr/bin/env bash
# Usage: render.sh <frames_dir> <output.mp4>
# Output is H.264 High/yuv420p so it plays on phones (4:4:4 does not play on Android).
# Turns 00.png, 01.png, ... into a reel: 3s per frame, slow zoom, 0.5s crossfades.
set -euo pipefail
FRAMES=$1; OUT=$(realpath -m "$2")
cd "$FRAMES"
N=$(ls [0-9][0-9].png | wc -l); D=3; X=0.5; FPS=30; inputs=(); fc=""
for i in $(seq 0 $((N-1))); do
  inputs+=(-i "$(printf '%02d' $i).png")
  fc+="[$i:v]scale=2880:2160,zoompan=z='1+0.08*on/($D*$FPS)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$((D*FPS)):s=1440x1080:fps=$FPS,setsar=1,format=yuv420p[v$i];"
done
prev=v0
for i in $(seq 1 $((N-1))); do
  fc+="[$prev][v$i]xfade=transition=fade:duration=$X:offset=$(python3 -c "print($i*($D-$X))")[x$i];"; prev=x$i
done
fc+="[$prev]fade=t=in:st=0:d=0.5,fade=t=out:st=$(python3 -c "print(max(0,$N*$D-($N-1)*$X-0.7))"):d=0.7,format=yuv420p[out]"
ffmpeg -y -v error "${inputs[@]}" -filter_complex "$fc" -map "[out]" -c:v libx264 -pix_fmt yuv420p -profile:v high -level 4.0 -crf 23 -preset medium -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$OUT"
