#!/bin/zsh
# v3 (Oct client changes): web encodes of the hero slide films.
#   zsh _tools/encode-oct-video.sh [grand-opening|service|ad-personam]
# Loops are muted H.264 (yuv420p, faststart), cut on a scene change so the jump back
# to the start lands on a cut. Desktop 1920x1080; phone = centre crop at the hero's
# portrait ratio (800 x 943), 720 wide. Posters = first frame (webp).
set -e
cd "${0:A:h}/.."
SRC="../___OCT changes/sources"
OUT=assets/video
mkdir -p $OUT

enc() {   # name src start dur [phone w/h, default 800/943 = the hero frame]
  local name=$1 src=$2 ss=$3 t=$4 pr=${5:-800/943}
  ffmpeg -v error -y -ss $ss -t $t -i "$src" -an -vf "scale=1920:1080:flags=lanczos,format=yuv420p" \
    -c:v libx264 -preset slow -crf 27 -profile:v high -movflags +faststart $OUT/$name-loop-d.mp4
  ffmpeg -v error -y -ss $ss -t $t -i "$src" -an -vf "crop=ih*$pr:ih,scale=720:-2:flags=lanczos,format=yuv420p" \
    -c:v libx264 -preset slow -crf 27 -profile:v high -movflags +faststart $OUT/$name-loop-m.mp4
  ffmpeg -v error -y -i $OUT/$name-loop-d.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/$name-poster-d.webp
  ffmpeg -v error -y -i $OUT/$name-loop-m.mp4 -frames:v 1 -c:v libwebp -quality 80 $OUT/$name-poster-m.webp
  ls -la $OUT/$name-* | awk '{printf "%6.1f MB  %s\n", $5/1048576, $9}'
}

case ${1:-grand-opening} in
  # the 603 MB source was deleted locally (Alex, 21 Oct): re-download it from the client Dropbox link in index_v3.html to re-encode
  grand-opening) enc grand-opening "$SRC/01-grand-opening/2022-Lamborghini-Miami-Grand-Opening-4K-Landscape-With-Logo.mov" 0 8.30 ;;
  ad-personam)   enc ad-personam "$SRC/06-ad-personam/Andres-Ad-Personam-Revuelto-Horizontal-Reel.mp4" 1.335 10.635 4/5 ;;
  service)       enc service       "$SRC/04-service/Andres-Service-Landing-Video.mov" 3.128 9.09 ;;
esac
