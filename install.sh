#!/bin/bash

echo "Installing Pulsar..."

if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found, installing..."
    sudo dnf install python3-pip -y
fi

pip3 install psutil rich --break-system-packages

curl -sSL https://raw.githubusercontent.com/2aadd/pulsar/main/pulsar.py -o /tmp/pulsar.py

echo '#!/usr/bin/env python3' | sudo tee /usr/local/bin/pulsar > /dev/null
sudo cat /tmp/pulsar.py | sudo tee -a /usr/local/bin/pulsar > /dev/null
sudo chmod +x /usr/local/bin/pulsar

echo "Done! Run with: pulsar"
