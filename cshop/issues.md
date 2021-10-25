I ran into some issues while trying to run weasyprint on mac. I had to install the following:

Glib, Pango
`brew install glib pango `

Then link them:
`ln -s /usr/local/lib/libgobject-2.0.dylib /usr/local/lib/gobject-2.0`
`ln -s /usr/local/lib/libpango-1.0.dylib /usr/local/lib/pango-1.0`


Also, the following script allow the seeking of library paths
```python
from ctypes.util import find_library

find_library('gobject-2.0')
```
