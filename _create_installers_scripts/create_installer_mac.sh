# need to install create-dmg to use this script!!
# You can do this by BREW:
#
#	  brew install create-dmg
#
# Run this script only after 'build_nuitka_mac.sh' is done
create-dmg \
  --volname "Apexsetup" \
  --window-pos 400 400 \
  --window-size 510 410 \
  --icon-size 60 \
  --icon "./dist/Apexsymm.app" 60 190 \
  --app-drop-link 350 190 \
  "Apexsetup.dmg" \
  "./dist"