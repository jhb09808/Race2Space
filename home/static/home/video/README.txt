Drop your two background videos in this folder:

  hero.mp4      -> plays behind the RACE2SPACE hero at the top of the homepage
  feature.mp4   -> plays in the full-viewport "REACHING BEYOND EARTH" section lower down

Requirements:
  - MP4 (H.264 / AAC), looping-friendly, no audio needed (they play muted).
  - Keep them reasonably small (ideally < 10-15 MB each) so the page loads fast.

After adding them on PythonAnywhere:
  git pull origin master
  python manage.py collectstatic --noinput
  then Reload the web app.
