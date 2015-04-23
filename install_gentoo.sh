#!/bin/bash

mkdir -p /usr/lib/duck_launcher
cp duck_launcher/* /usr/lib/duck_launcher/
mkdir -p /usr/lib/duck_settings
cp -r duck_settings/* /usr/lib/duck_settings/
cp -r bin/* /usr/bin/
mkdir -p /usr/share/duck-launcher/default-theme
cp -r default-theme/* /usr/share/duck-launcher/default-theme/
mkdir -p /usr/share/duck-launcher/plugins
cp -r plugins/* /usr/share/duck-launcher/plugins
cp -r icons/* /usr/share/icons/hicolor/scalable/apps

