# epidoc-headers
Create epidoc headers for Siddham metadata using python

Run `python encloseSnippets.py` first to add sanskrit edition div.

Next `createHeader.py` to create XML header from metadata csv.

Requires snippets, rootSnippets, metadata (object.csv, inscription.csv), headed and declared directories.

Snippets directory has epiDoc xml with filenames corresponding to IDs in inscriptions csv.
Remember: Metadata csv is formatted so that objects and inscriptions are columns not rows.
