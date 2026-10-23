#!/bin/zsh
# v3 (Oct client changes): web encodes of the hero slide films.
#   zsh _tools/encode-oct-video.sh [grand-opening|service|ad-personam|lifestyle|urus|sv]
# Loops are muted H.264 (yuv420p, faststart), cut on a scene change so the jump back
# to the start lands on a cut. Desktop 1920x1080; phone = centre crop at the hero's
# portrait ratio (800 x 943), 720 wide. Posters = first frame (webp).
set -e
cd "${0:A:h}/.."
SRC="../___OCT changes/sources"
OUT=assets/video
mkdir -p $OUT

enc() {   # name src start dur [phone w/h, default 800/943 = the hero frame] [poster time in the loop, default 0]
  local name=$1 src=$2 ss=$3 t=$4 pr=${5:-800/943} pt=${6:-0} pre=${7:-null}   # pre: a crop applied first (e.g. a letterbox)
  ffmpeg -v error -y -ss $ss -t $t -i "$src" -an -vf "$pre,crop=min(iw\,ih*16/9):min(ih\,iw*9/16),scale=1920:1080:flags=lanczos,format=yuv420p" \
    -c:v libx264 -preset slow -crf 27 -profile:v high -movflags +faststart $OUT/$name-loop-d.mp4
  ffmpeg -v error -y -ss $ss -t $t -i "$src" -an -vf "$pre,crop=ih*$pr:ih,scale=720:-2:flags=lanczos,format=yuv420p" \
    -c:v libx264 -preset slow -crf 27 -profile:v high -movflags +faststart $OUT/$name-loop-m.mp4
  ffmpeg -v error -y -ss $pt -i $OUT/$name-loop-d.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/$name-poster-d.webp
  ffmpeg -v error -y -ss $pt -i $OUT/$name-loop-m.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/$name-poster-m.webp
  ls -la $OUT/$name-* | awk '{printf "%6.1f MB  %s\n", $5/1048576, $9}'
}

case ${1:-grand-opening} in
  # the 603 MB source was deleted locally (Alex, 21 Oct): re-download it from the client Dropbox link in index_v3.html to re-encode
  grand-opening) enc grand-opening "$SRC/01-grand-opening/2022-Lamborghini-Miami-Grand-Opening-4K-Landscape-With-Logo.mov" 0 8.30 ;;
  ad-personam)   enc ad-personam "$SRC/06-ad-personam/Andres-Ad-Personam-Revuelto-Horizontal-Reel.mp4" 1.335 10.635 4/5 ;;
  # the unveiling itself: the cover comes off, the yellow Revuelto, doors up (Alex: the subject is the car); poster = the car
  lifestyle)     enc revuelto-launch "$SRC/09-lifestyle/REVUELTO-LAUNCH.mp4" 23.524 8.883 800/943 5.0 ;;
  # the client's YouTube film (Alex downloaded it): dust road -> road -> front view, before the legal line that starts ~66.5 s
  urus)          enc urus-sep "$SRC/Urus SE Performante /YTDown.com_YouTube_Media_5ZtLH3s8Wvg_Lamborghini-Urus-SE-Performante-Urus-at-its-peak_001_1080p.mp4" 60.96 5.56 800/943 1.6 crop=1920:960:0:60 ;;   # 2:1 letterbox in a 16:9 file
  # the official Lamborghini film (youtu.be/1UE_RnIbt4c, Alex's file): track, head-on, light trail, head-on — no people, no legal line
  sv)            enc revuelto-sv "$SRC/Revuelto SV/YTDown.com_YouTube_Media_1UE_RnIbt4c_Lamborghini-Revuelto-SV-The-Quantum-of-Driving_001_1080p.mp4" 37.9 9.0 800/943 2.6 ;;
  service)       enc service       "$SRC/04-service/Andres-Service-Landing-Video.mov" 3.128 9.09 ;;
esac
# v4 (22 Oct, client round 2): slide 02, the End of Year 2021 film, 0:00-0:20 as the client asked, the 4K frame's
# top-left 84% so the bottom-right Prestige watermark stays out. Run with the same enc() body:
#   inventory)     enc inventory "$SRC/02-inventory/Lamborghini-Miami-End-of-Year-Video-2021-Landscape-4K-With-Logos.mov" 0 20 800/943 0 crop=3226:1814:0:0 ;;
# v4 sample pages (23 Oct): three loops cut from the service film with the concat filter, each starting
# on a different shot (seconds in the source): sched = 18.31-20.90 + 9.34-12.22 + 15.27-18.31 (wing, engine,
# body); parts = 12.22-15.27 + 9.34-12.22 (wheel, engine); collision = 15.27-20.90 (body, wing). Phone =
# 4:3 centre crop at 960x720. Posters = first frame. See the enc() in the shell history / DATA_SOURCES.md.
