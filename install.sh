#!/bin/bash

echo "Installing Pulsar..."

if ! command -v pip3 &> /dev/null; then
    sudo dnf install python3-pip -y
fi

pip3 install psutil rich --break-system-packages

curl -sSL https://raw.githubusercontent.com/2aadd/pulsar/main/pulsar.py -o /tmp/pulsar.py

sudo bash -c 'echo "#!/usr/bin/env python3" > /usr/local/bin/pulsar && cat /tmp/pulsar.py >> /usr/local/bin/pulsar'
sudo chmod +x /usr/local/bin/pulsar

echo "Done! Run with: pulsar"
