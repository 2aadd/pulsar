#!/bin/bash

echo "Installing Pulsar..."

if ! command -v pip3 &> /dev/null; then
    sudo dnf install python3-pip -y
fi

pip3 install psutil rich --break-system-packages

sudo curl -sSL https://raw.githubusercontent.com/2aadd/pulsar/main/pulsar.py -o /usr/local/bin/pulsar
sudo chmod +x /usr/local/bin/pulsar

echo "Done! Run with: pulsar"
