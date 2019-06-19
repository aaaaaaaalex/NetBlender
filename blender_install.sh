#!/bin/sh

rm -rf ./netblend/__pycache__
rm -rf ~/.config/blender/2.79/scripts/modules/netblend
rm -rf ~/.config/blender/2.79/scripts/modules/__pychache__

mkdir ~/.config/blender/2.79/scripts/modules/netblend
cp -r ./netblend/* ~/.config/blender/2.79/scripts/modules/netblend
