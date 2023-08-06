=========
Changelog
=========

Version 0.4.8
=============

* now reads DCML labels with cadence annotations
* unified command-line interface file options and included ``-f file.json``
* Parse got more options for creating DataFrame index levels
* Parse.measures property for convenience
* bug fixes for better GitHub workflows

Version 0.4.7
=============

* Labels can be attached to MuseScore's Roman Numeral Analysis (RNA) layer
  * parameter `label_type=1` in both `Score.attach_labels()` and `Parse.attach_labels()`
  * `Annotations.remove_initial_dots()` before inserting into the RNA layer
  * `Annotations.add_initial_dots()` before inserting into the absolute chord layer
* interpret all `#vii` in major contexts as `vii` when computing chord tones
* code cosmetics and bug fixes

Version 0.4.6
=============

* ms3 extract and Parse.store_lists() now have the option unfold to account for repeats
* minor bug fixes

Version 0.4.5
=============

* added 'ms3 compare' command
* support for parsing cap, capx, midi, musicxml, mxl, and xml files through temporary conversion
* support for parsing MuseScore 2 files through temporary conversion

Version 0.4.3
=============

* added 'ms3 check' command
* support of coloured labels
* write coloured labels to score comparing attached and detached labels to each other
* better interface for defining log file paths (more options, now conforming to the Parse.store_lists() interface)
* fixed erroneous separation of alternative labels


Version 0.4.2
=============

* small bug fixes
* correct computation of chord tones for new DCML syntax elements ``+M``, ``-``, ``^``, and ``v``

Version 0.4.1
=============

* ms3 0.4.1 supports parsing (but not storing) compressed MuseScore files (.mscz)
* Installs "ms3 convert" command to your system for batch conversion using your local MuseScore installation
* "ms3 extract" command now supports creation of log files
* take ``labels_cfg`` into account when creating expanded chord tables

Version 0.4.0
=============

* The standard column 'onset' has been renamed to 'mc_onset' and 'mn_onset' has been added as an additional standard column.
* Parse TSV files as Annotations objects
* Parse.attach_labels() for inserting annotations into MuseScore files
* Prepare detached labels so that they can actually be attached
* Install "ms3 extract" command to the system
* Including da capo, dal segno, fine, and coda for calculating 'next' column in measures tables (for correct unfolding of repeats)
* Simulate parsing and table extraction
* Passing labels_cfg to Score/Parse to control the format of annotation lists
* Easy access to individual parsed files through Parse[ID] or Parse[ix]
* parse annotation files with diverging column names

Version 0.3.0
=============

* Parse.detach_levels() for emptying all parsed scores from annotations
* Parse.store_mscx() for storing altered (e.g. emptied) score objects as MuseScore files
* Parse.metadata() to return a DataFrame with all parsed pieces' metadata
* Parse.get_labels() to retrieve labels of a particular kind
* Parse.info() has improved the information that objects return about themselves
* Parse.key for a quick overview of the files of a given key
* Parse can be used with a custom index instead of IDs [an ID is an (key, i) tuple]
* Score.store_list() for easily storing TSVs
* renamed Score.output_mscx() to store_mscx() for consistency.
* improved expansion of DCML harmony labels

Version 0.2.0
=============

Beta stage:

* attaching and detaching labels
* parsing multiple pieces at once
* extraction of metadata from scores
* inclusion of staff text, dynamics and articulation in chord lists, added 'auto' mode
* conversion of MuseScore's encoding of absolute chords
* first version of docs

Version 0.1.3
=============

At this stage, the library can parse MuseScore 3 files to different types of lists:

* measures
* chords (= groups of notes)
  * including slurs and spanners such as pedal, 8va or hairpin markings
  * including lyrics
* notes
* harmonies

and also some basic metadata.

Version 0.1.0
=============

- Basic parser implemented
- Logging
- Measure lists
