#!/bin/bash


echo "Installing Pulsar..."


pip install psutil rich --break-system-packages # Ya da kullanıcı dizinine: --user


sudo cp pulsar.py /usr/local/bin/pulsar


sudo chmod +x /usr/local/bin/pulsar


echo "Done! Run with: pulsar"
