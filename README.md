# notepad--
### A text editor so bad it can't even edit.  Made for viewing huge files quickly.

Many text editors won't allow you to view large files.  This text editor will at least make an effort, and as long as you have enough RAM (or page+RAM), it will actually work.  This has been tested with multi-gigabyte files.

The "editor" (currently) does not support editing; only viewing.  Hence, it's `notepad--` (a nod to the otherwise excellent [Notepad++](https://notepad-plus-plus.org/)).

## Options and Features

| Command                              | Effect              |
|:-------------------------------------|:--------------------|
| Escape                               | Close `notepad--`   |
| ALT + G                              | Go to line          |
| CTRL + W                             | Toggle line wrap    |
| PG UP/DOWN, Mouse Scroll, Scroll Bar | Scroll file         |
| MINUS/PLUS                           | Shrink/enlarge font |

Configurable:

- Color scheme
- Font (name, size, line padding)
- Tab width
- Default screen size
- Default line wrapping
- Key and mouse event repeat delays
- Slider size

## Installation

`notepad--` requires the language [`Python`](https://www.python.org/) (2 or 3), and the package [`PyGame`](http://www.pygame.org/download.shtml).  Installing `PyGame` is usually as simple as `pip install pygame` (UNIX), or `pip.exe install pygame` (Windows; if it's not on your path, `pip.exe` is usually in `Python##/Scripts/`, where `##` is the version you installed).

## Contributing

Pull requests are welcome.  The most obvious missing feature is that `notepad--` cannot edit files.  It might also be nice to have some kind of paging scheme to more easily load enormous files that don't fit in memory.