#!/bin/zsh
# v3 hero slide 05 (Alex, 21 Oct 2026): one history film — the historical shots of the Prestige portal's
# our-story film (Irv on the phone, the first building, the Countach, Ferruccio signing) joined with Alex's
# three animated photos (video2/3/4: the child in the Countach, Irv at the white Countach, Irv with the
# Diablo), roughly in date order, short dissolves as in the portal film. Alex's clips: 3 s from the middle.
#   zsh _tools/make-prestige-history.sh
set -e
cd "${0:A:h}/.."
P="../../_______PRESTIGE TO PREVIEW/prestige-final/assets/videos/our_story_video_hero.mp4"
A="../___OCT changes/sources/05-prestige-2017"
OUT=assets/video
XF=0.25
build() {   # name W H
  local name=$1 W=$2 H=$3
  local norm="scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=24,format=yuv420p,settb=AVTB"
  ffmpeg -v error -y \
    -ss 3.00 -t 0.80 -i "$P" -ss 3.88 -t 1.00 -i "$P" -ss 5.02 -t 0.98 -i "$P" \
    -ss 1.0 -t 3.0 -i "$A/video3.mp4" -ss 1.0 -t 3.0 -i "$A/video2.mp4" \
    -ss 6.12 -t 0.62 -i "$P" -ss 1.0 -t 3.0 -i "$A/video4.mp4" \
    -filter_complex "[0:v]${norm}[v0];[1:v]${norm}[v1];[2:v]${norm}[v2];[3:v]${norm}[v3];[4:v]${norm}[v4];[5:v]${norm}[v5];[6:v]${norm}[v6];[v0][v1]xfade=transition=fade:duration=$XF:offset=0.55[x1];[x1][v2]xfade=transition=fade:duration=$XF:offset=1.3[x2];[x2][v3]xfade=transition=fade:duration=$XF:offset=2.03[x3];[x3][v4]xfade=transition=fade:duration=$XF:offset=4.78[x4];[x4][v5]xfade=transition=fade:duration=$XF:offset=7.53[x5];[x5][v6]xfade=transition=fade:duration=$XF:offset=7.9[x6]" \
    -map "[x6]" -an -c:v libx264 -preset slow -crf 23 -movflags +faststart $OUT/prestige-history-$name.mp4
}
build d 1920 1080
build m 720 848
ffmpeg -v error -y -ss 3.4 -i $OUT/prestige-history-d.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/prestige-history-poster-d.webp
ffmpeg -v error -y -ss 3.4 -i $OUT/prestige-history-m.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/prestige-history-poster-m.webp
for f in $OUT/prestige-history-*; do printf "%6.1f MB  %s\n" $(( $(stat -f%z $f) / 1048576.0 )) $f; done
ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/prestige-history-d.mp4
