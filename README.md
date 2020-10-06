# gif-to-ascii-gif
Takes a gif or webm and turns it into an gif rendered with ASCII characters.


You need the cour.ttf file in same directory as the script to run.

You can use these arguments:

* --file {filename}
* --cols {number of char columns widthwise, optional, default 64}
* --fps {output gif frames per sec, optional, default 12}

ie:
`gif2ascii.py --file "giphy.gif"`

increasing the cols exponentially increases the output file size.

increasing fps increases filesize linearly, but it adds up because output is a gif.

Also, I say JIFF but you guys keep saying gif so Im getting all messed up lol.
