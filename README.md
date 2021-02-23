# gif-to-ascii-gif
Takes a gif or webm and turns it into an gif rendered with ASCII characters.


You need the cour.ttf file in same directory as the script to run.

The Tkinter UI asks you to select a file,
then optionally an ASCII char resolution, num of char per width,
then an output FPS

increasing the num of char per width exponentially increases the output file size.
increasing output FPS increases filesize linearly, but it adds up because output is a gif.
