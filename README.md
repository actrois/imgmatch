# imgmatch
A duplicate image file finder tool  
This program will look for duplicate images in a specified folder

## Usage
### Requirements
 - Python 2.7
 - [OpenCV 3.3](https://opencv.org/)
 - [python-daemon](https://pypi.python.org/pypi/python-daemon/)
 - [Libnotify](https://developer.gnome.org/libnotify)

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
  -b <start or stop>  :  Start or stop background mode
                          When run with -b option, imgmatch will run in 
                          background watching a specified directory by 
                          -d option. When duplicate image will found, 
                          it will make a desktop notification.
```
#### Sample usages:
`imgmatch -d /home/user/pictures -r`
   Search recursively in `/home/user/pictures` for duplicate images

`imgmatch -d /home/user/pictures/memes -r -b start`
   Watch `/home/user/pictures/meme` in background and gives desktop notification when duplicate images found.
   
 `imgmatch -b stop`
   Stop any imgmatch background service run earlier.
   
Note: for now, only one background service can be run, new one will replace the older one.

#### Sample output:
```
   meme_resize.jpg is a duplicate of meme_format.bmp
   meme.jpg is a duplicate of meme_format.bmp
   meme_filter.jpg is a duplicate of meme_format.bmp
   meme_crop.jpg is a duplicate of meme_format.bmp
   meme_rotate.jpg is a duplicate of meme_format.bmp
   selfie.jpg is a duplicate of just_donwloaded_file.jpg
```

---

## Development
### Requirements
 - Python 2.7
 - [OpenCV 3.3](https://opencv.org/)
 - [python-daemon](https://pypi.python.org/pypi/python-daemon/)
 - [Libnotify](https://developer.gnome.org/libnotify)
 - Vagrant
 - VirtualBox
 - Ansible

### Development setup
1. Install VirtualBox, Vagrant, and Ansible. Just because.
2. Run `vagrant up`
