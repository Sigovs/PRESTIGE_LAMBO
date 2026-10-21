#!/bin/zsh
# v3 hero slide 05 (Alex, 21 Oct 2026): one history film — the historical shots of the Prestige portal's
# our-story film (Irv on the phone, the first building, the Countach, Ferruccio signing) joined with Alex's
# three animated photos (video2/3/4), roughly in date order. Alex: "why so short and fast?" — the portal
# shots are only 0.6-1 s in the source, so each is slowed to ~2.5 s (motion-compensated in-betweens, forward
# only); Alex's clips run 4.5 s; dissolves 0.5 s.
#   zsh _tools/make-prestige-history.sh
set -e
cd "${0:A:h}/.."
P="../../_______PRESTIGE TO PREVIEW/prestige-final/assets/videos/our_story_video_hero.mp4"
A="../___OCT changes/sources/05-prestige-2017"
OUT=assets/video
TMP=$(mktemp -d)
XF=0.5
slow() {   # out start dur factor
  ffmpeg -v error -y -ss $2 -t $3 -i "$P" -an -vf "setpts=$4*PTS,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1,format=yuv420p" -c:v libx264 -crf 14 $TMP/$1.mp4
}
slow phone    3.00 0.80 3.0
slow building 3.88 1.00 2.5
slow countach 5.02 0.98 2.5
slow ferruccio 6.12 0.62 3.0
dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
build() {   # name W H
  local name=$1 W=$2 H=$3
  local norm="scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=24,format=yuv420p,settb=AVTB"
  local inputs=( $TMP/phone.mp4 $TMP/building.mp4 $TMP/countach.mp4 "$A/video3.mp4" "$A/video2.mp4" $TMP/ferruccio.mp4 "$A/video4.mp4" )
  local args=() lens=() g="" i=0 off=0 prev="v0"
  for f in $inputs; do
    if [[ $f == $A/* ]]; then args+=(-ss 0.3 -t 4.5 -i "$f"); lens+=(4.5); else args+=(-i "$f"); lens+=($(dur "$f")); fi
  done
  for i in {0..6}; do g+="[$i:v]${norm}[v$i];"; done
  for i in {1..6}; do
    off=$(( off + lens[i] - (i>1 ? XF : 0) ))
    g+="[${prev}][v$i]xfade=transition=fade:duration=$XF:offset=$(( off - XF ))[x$i];"; prev="x$i"
  done
  ffmpeg -v error -y $args -filter_complex "${g%;}" -map "[x6]" -an -c:v libx264 -preset slow -crf 23 -movflags +faststart $OUT/prestige-history-$name.mp4
}
build d 1920 1080
build m 720 848
ffmpeg -v error -y -ss 7.5 -i $OUT/prestige-history-d.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/prestige-history-poster-d.webp
ffmpeg -v error -y -ss 7.5 -i $OUT/prestige-history-m.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/prestige-history-poster-m.webp
rm -rf $TMP
for f in $OUT/prestige-history-*; do printf "%6.1f MB  %s\n" $(( $(stat -f%z $f) / 1048576.0 )) $f; done
dur $OUT/prestige-history-d.mp4
