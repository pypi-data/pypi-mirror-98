# TkinterWeb 
**A fast and simple cross-platform webbrowser for Tkinter.**

&nbsp;
&nbsp;
## Overview
**TkinterWeb offers bindings for the Tkhtml3 widget from http://tkhtml.tcl.tk/tkhtml.html, which enables loading HTML and CSS code into Tkinter applications.**

Both Python 2 and Python 3, as well as MacOS, Windows, and Linux are supported. 

&nbsp;
&nbsp;
## Usage

**TkinterWeb can be used in any Tkinter application. Here is an example:**
```
from tkinterweb import HtmlFrame #import the HTML browser
try:
  import tkinter as tk #python3
except ImportError:
  import Tkinter as tk #python2

root = tk.Tk() #create the tkinter window
frame = HtmlFrame(root) #create HTML browser
frame.load_website("http://tkhtml.tcl.tk/tkhtml.html") #load a website
frame.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window
root.mainloop()
```

Some other tricks can be found in the [HtmlFrame documentation](https://github.com/Andereoo/TkinterWeb/blob/main/tkinterweb/docs/HTMLFRAME.md#tips-and-tricks)

**Refer to the [GitHub home page](https://github.com/Andereoo/TkinterWeb)  for more information.**
