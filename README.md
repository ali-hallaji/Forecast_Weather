# Project Description
It is weather forecast application for Ubuntu desktop.

# Running and Installation

Before install you should install these packages on your ubuntu desktop:
```
sudo apt-get install libwebkit-dev -y
sudo apt-get install python-gtk2 -y
```

If you have trouble with installing `WebKit` on your ubuntu, please follow this link [install webkit](https://help.ubuntu.com/community/WebKit) or use deb package in the source packages directory.
```
sudo dpkg -i source_packages/python-webkit_1.1.8-3ubuntu2_amd64.deb
```

Then install python packages:
```
pip install -r requirments.txt
```

For using pygtk into virtualenv make these link to your virtualenv library:
```
ln -s /usr/lib/python2.7/dist-packages/gtk-2.0/ lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/gi lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/pygtk* lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/glib/ lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/gobject/ lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/cairo/ lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/webkit/ lib/python2.7/site-packages/
```

# Execute and Try
