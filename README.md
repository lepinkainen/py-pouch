py-pouch
========

Add links from CLI to your <a href="http://getpocket.com/developer/">Pocket</a> account.

Usage: 

    py-pouch.py [url]

If you have not authorized yet, the program will give you the URL to authorize at getpocket.com. After authorization links given as arguments are saved directly to Pocket


newsbeuter integration
======================

Just add

    bookmark-cmd "~/bin/py-pouch.py"
  
to your configuration file. The error messages are already optimized for newsbeuter.

Remember to authorize by manually running py-pouch once.
