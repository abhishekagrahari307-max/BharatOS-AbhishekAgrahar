#!/bin/bash
# ====================== BHARATOS INSTALLER ======================
set -eo pipefail

# Install dependencies
sudo apt update && sudo apt install -y \
    git python3-pip tpm2-tools sbctl ffmpeg \
    libopencv-dev libx11-dev jq zenity

# Install Python modules
pip install mediapipe opencv-python vosk indic-nlp-library

# Setup Hindi NLP
mkdir -p core/hindi_nlp
wget -q https://alphacephei.com/vosk/models/vosk-model-hi-0.22.zip
unzip -o vosk-model-hi-0.22.zip -d core/hindi_nlp/

# Setup security
sudo systemctl enable tpm2-abrmd
sudo sbctl enroll-keys --yes-this-might-brick-my-machine
sudo tailscale up --advertise-exit-node --accept-routes

# Setup autostart
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/bharatos.desktop <<EOL
[Desktop Entry]
Type=Application
Name=BharatOS Launcher
Exec=$PWD/scripts/launch_ui.sh
Icon=$PWD/assets/om-symbol.png
EOL

echo "BharatOS installed successfully! Reboot to start."
