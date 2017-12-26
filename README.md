# imgmatch
A duplicate image file finder tool  
This program will look for duplicate images in a specified folder

## Usage
### Requirements
 - Python 2.7
 - OpenCV 3.3

### Simple usage
1. Install requirements with `pip install -r requirements.txt`  
2. Run the program with `python imgmatch.py -d <image_folder_path>`

Alternatively, using `setup.sh`:
1. Run `./setup.sh` (might need `sudo`)
2. Run the program with `imgmatch -d <image_folder_path>`

#### Argument Options: 
```
  -h, --help          :  Show help and exit
  -l, --log           :  Show log
  -d, --dir=<DIR>     :  The directory to search for duplicate images,
                          default is current working directory
  -r, --recursive     :  Search image recursively in subdirectories
  -s <VALUE>          :  Similarity treshold to recognize duplicate images
                          default value is 1.8, lower treshold means the
                          check will be more strict (i.e. only images
                          that are very similar will be marked) and vice versa
```

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
