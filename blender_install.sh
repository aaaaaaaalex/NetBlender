#!/bin/sh

rm -rf ~/.config/blender/2.79/scripts/modules/netblend
rm -rf ~/.config/blender/2.79/scripts/modules/__pychache__

mkdir ~/.config/blender/2.79/scripts/modules/netblend
cp ./netblend/* ~/.config/blender/2.79/scripts/modules/netblend
