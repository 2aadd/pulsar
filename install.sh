
#!/bin/bash

echo "Installing Pulsar..."


if ! command -v pip3 &> /dev/null; then

    echo "pip3 not found, installing..."

    sudo dnf install python3-pip -y

fi


pip3 install psutil rich --break-system-packages

# pulsar'ı indir

curl -sSL https://raw.githubusercontent.com/2aadd/pulsar/main/pulsar.py -o ~/pulsar.py


sudo cp ~/pulsar.py /usr/local/bin/pulsar

sudo chmod +x /usr/local/bin/pulsar

echo "Done! Run with: pulsar"

