# PyQIF-Parser

A(nother) Python-based Parser for Quicken / Lexware Finance Manager QIF files.

## Why

There are already some Python-based parsers for QIF files, however they had issues with the file my (German) Lexware Financial Manager 2019 is spitting out. 

What I basically need is a tool to convert a QIF file into a pandas dataframe, so this is my main motivation. 

As I do not use split bookings I probably will not spend some effort to implement them. Feel free to send a pull request.

## Resources

* https://github.com/jemmyw/Qif/blob/master/QIF_references for a QIF reference

* Quicken may differ with respect to their content, as Quicken allows to include or exclude categories, classes, etc.

In the file I used to build the parser there were:

* an option to indicate the date format (here: "MDY")
* The classes
* The categories
* The accounts
* The bookings 




## Proof of Concept

I hacked together a proof of concept, see it here: https://gist.github.com/UweZiegenhagen/08885a0c08a6f23bd2c3855106a1522c

This code is quite ugly but parses my QIF file w/o errors, so it will be the basis for this project.

It works by checking each line and triggering a mode change when certain keywords are found. 

Let's see an example. Imagine, we find !Type:Class in the QIF file. This indicates that the next lines (up to the next !Type:XXXX) contain the classes, which are formed by an N-Tag, followed by D-tag, followed by the circumflex. 

!Type:Class
NHouse
DSpendings for the house
^