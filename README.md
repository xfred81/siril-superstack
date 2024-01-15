# siril-superstack

```siril-superstack``` generates a Siril script to render superstacks, as described on Siril's site https://siril.org/tutorials/comet/#animations-with-superstacking. A superstack refers to a stacking applied only to a part of a sequence; applied to planetary, the main goal is to generate animations through mutiple TIF files stacked at different moment in time (superstacks), and with a specific subfiltering of frames within each superstack.

## Installation

There's no particular dependencies here; directly running ```./superplanetary.py``` should work.

## Usage

My routine:

* Open Siril (1.2.0 or above),
* Open your sequence or SER file,
* Exclude frame that you absolutely want to reject in animation,
* *Align the sequence!* this is important :)
* Run ```siril-superstack``` and specific your parameters,
* The script should have been generated; run ```reloadscripts``` in Siril to refresh and load the new script,
* Use Superstack-planetary script in the Scripts menu of Siril.
* Images should be generated in a new img/ subdirectory within the path you indicated in parameters

Notice that if script fails and if you want to regenerate it, you'll have to
select all of your images again.

After image's creation, you can combine them as a animation with ffmpeg tool for example.

