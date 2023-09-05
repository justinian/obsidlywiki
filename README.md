# ObsidlyWiki

This is a simple script I use to output [TiddlyWiki][]-friendly markdown files
from my [Obsidian][] vaults.

[TiddlyWiki]: https://www.tiddlywiki.com
[Obsidian]: https://www.obsidian.md

## Basic Usage

Install requirements (your OS may differ in how to set up Python virtual
environments):

```
python3 -m venv ./venv      # You can put the venv wherever, i like it in the repo dir.
source ./venv/bin/activate  # for bash. see other scripts for other shells.
pip install -r requirements.txt
```

Convert a directory of Obsidian notes into a directory of TiddlyWiki-formatted
markdown notes:

```
./convert.py "/path/to/obsidian/notes" "/path/to/output"
```

*NOTE*: ONLY files with the `#public` tag in the obsidian notebook will be
converted. This is to avoid accidentally sharing private notes - notes must be
explicitly tagged as `#public` in order to show up.

## Advanced Usage

I use this for my tabletop roleplaying setting's wiki, [Gradia][], so that I
can share lore and campaign information with my players without revealing my GM
secrets. (Not that players ever _read_ lore, but hey that's fine, I worldbuild
for me.) It's a little bit bubble gum and duct tape, but it works. Here's the
setup:

1. I use [SyncThing][] to sync my notes from my desktop to my web server.
2. On the server, I use `incron` to monitor the incoming notes directory for
   changes, and call a script to regenerate the wiki file. See the script in
   `examples/obsidlywiki_update.sh` to see how I have that set up.
3. I've installed [Node][] and the [Node version of TiddlyWiki][ntw], and have
   a basic skeleton of a TiddlyWiki for my site set up (with the Markdown
   plugin enabled) in that installation - created as e.g. `wiki_name`
4. In that installation, under `wiki_name/tiddlers` I created a directory
   specifically for the import called `wiki_name/obsidian`. There is _also_ a
   directory to tell TiddlyWiki about these files in
   `wiki_name/tiddlers/obsidian` - that directory should contain only the file
   `tiddlywiki.files` from this repo's `examples` directory, to tell TiddlyWiki
   how to add and convert the exported files.

With all of that set up, changes to the wiki should trigger the
`obsidlywiki_update.sh` script, converting the notes into TiddlyWiki-flavored
Markdown, building the TiddlyWiki HTML file with Node, and copying the result
out to your webserver root.


[Gradia]: https://gradia.org
[SyncThing]: https://syncthing.net
[node]: https://nodejs.org
[ntw]: https://tiddlywiki.com/static/TiddlyWiki%2520on%2520Node.js.html
