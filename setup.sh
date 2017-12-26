echo "Updating repository..."
apt-get update -y > /dev/null 2>&1
echo "Installing dependencies..."
apt-get install -y python python-pip libsm6 libxext6 libxrender1 > /dev/null 2>&1
pip install opencv-python > /dev/null 2>&1
echo "Copying imgmatch to /usr/bin/"
cp imgmatch.py /usr/bin/imgmatch
chmod +x /usr/bin/imgmatch
echo "Finished"
