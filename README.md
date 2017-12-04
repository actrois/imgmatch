# imgmatch
A duplicate image file finder tool  
This program will look for duplicate images in the specified folder

## Usage
### Requirements
 - Python 2.7
 - OpenCV 3.3

### Simple usage
1. Install requirements with `pip install -r requirements.txt`  
2. Run the program with `python imgmatch.py <image_folder_path>`

Alternatively, using setup.sh:
1. Run `./setup.sh` (might need `sudo`)
2. Run the program with `imgmatch <image_folder_path>`

#### Sample output:
```
   meme_resize.jpg is a duplicate of meme_format.bmp
   meme.jpg is a duplicate of meme_format.bmp
   meme_filter.jpg is a duplicate of meme_format.bmp
   meme_crop.jpg is a duplicate of meme_format.bmp
   meme_rotate.jpg is a duplicate of meme_format.bmp
   selfie.jpg is a duplicate of just_donwloaded_file.jpg
```

## Development
### Requirements
 - Python 2.7
 - OpenCV 3.3
 - Vagrant
 - VirtualBox
 - Ansible

### Development setup
1. Install VirtualBox, Vagrant, and Ansible. Just because.
2. Run `vagrant up`
