# OctoMars

# NOTICE

OctoMars is no longer supported and has reached its end of life. 
If another maintainer is interested contact me to take over.

## About

Use [MarsEdit](http://www.red-sweater.com/marsedit/) to publish to the 
[Octopress](http://octopress.org) static blogging system.

This script is fairly simple and was written to scratch an itch. Any and
all contributions will be considered.

## Requirements

Octomars requires the gitpython module. Install it with:

    sudo easy_install gitpython

## Installing OctoMars

To install octomars on your system run the following from the repository root
that you've cloned:

    python ./setup.py install

If you get an error with the above command try installing with `sudo`:

    sudo python ./setup.py install

## Configuring MarsEdit

This is a sample configuration of MarsEdit to use octomars to post to an
Octopress static blog:

1. Make a directory in your local Octopress directory to hold MarsEdit posts.

        mkdir ~/Blog/source/_marsedit

    Add source/_marsedit to the .gitignore file if you don't want to worry about
    the _marsedit directory in your git repository.

2. Create a new blog in MarsEdit with the **File > New Blog…** menu item.

    Enter the blog name and url. MarsEdit will fail to detect the blog settings
    and present you with a dialog, click on the **Edit Settings** button to continue.
    
    !["MarsEdit blog settings detection fail dialog."](https://github.com/danimal/octomars/raw/master/resources/Edit_Settings.png "Press the Edit Settings button")
    
3. You will be presented with a blog settings dialog.

    !["MarsEdit blog settings dialog."](https://github.com/danimal/octomars/raw/master/resources/Blog_Settings.png "MarsEdit blog settings dialog sample")

    To setup your Octopress static blog set the:
    * _System Name_ pulldown to _Other_
    * _System API_ pulldown to _Blosxom API_
    * Choose your source/_marsedit directory as the Blosxom folder
    * In the last text entry box enter a command like this to call octomars:
        
            /usr/local/bin/octomars --commit --push %@
    
    Be sure to set the path to your octomars install location and to adjust the
    parameters to suit your needs (remove git commands, don't deploy the
    static files, etc.).

