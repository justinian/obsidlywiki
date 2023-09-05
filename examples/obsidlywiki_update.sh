#!/bin/bash

set -o errexit -o errtrace

obs="/path/to/obsidlywiki"
notes="/path/to/note/files"
wikibase="/path/to/tiddlywiki"
out="/path/to/wwwroot"

# Create a virtual env for obsidlywiki if you don't want to install
# its requirements globally. Here, I've made a virtual env in $obs/venv
# with:
#     python3 -m venv ./venv
#     source ./venv/bin/activate
#     pip install -r requirements.txt
source "${obs}/venv/bin/activate"

(
	trap 'logger "  ERROR: exited with $? at $LINENO"' ERR

	flock -n 9 || exit 1
	logger "Wiki update:" $1
	sleep 3

	trap 'logger "  Finished wiki update"' EXIT

	logger "Running:" "${obs}/convert.py"
	"${obs}/convert.py" "${notes}" "${wikibase}/wiki_name/obsidian"

	logger "Building"
	node "${wikibase}/node_modules/tiddlywiki/tiddlywiki.js" "${wikibase}/wiki_name" --build index
	cp "${wikibase}/wiki_name/output/index.html" "${out}/index.html"

) 9<"${notes}" # use the notebook dir as the fd 9 for flock
