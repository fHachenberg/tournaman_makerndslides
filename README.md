Mission
=======

This tools is meant as a replacement of the Tournaman feature "Create sound slides" which requires Powerpoint to work correctly. 

Requirements
============

Software
--------

 *Python 2.7
 *python-pptx (tested with 0.3.0) (https://pypi.python.org/pypi/python-pptx)
 *Tournaman 2 (tested with Version 2.0.8) (http://tournaman.wikidot.com)

Data
----

 *A presentation template in pptx format is required, see chapter "Template"

Installation
============
The most simple approach is to simply copy the py files into the folder containing the trm file. 

Usage
=====

Template
--------
Like Tournaman itself, the tool creates the round slides (containing the debate settings as well as the motion) by substituting values in a presentation template. The template contains a lot of placeholder strings like "#m" (motion), "#j1" (adjudicator board for debate #1 in the current round).

In contrast to Tournaman, though, this tools requires the presentation template in the '''pptx''' format! Tournaman provides a sample template in ppt format. If you intend to use this sample template, you will have to find a way to convert it to pptx format

Converting sample template using Libreoffice
--------------------------------------------
You can use Libreoffice (http://www.libreoffice.org/) to convert the original template to pptx. But beware of conversion errors. To actually see the errors the conversion to pptx format created, you will have to close the presentation in Libreoffice and reopen the pptx file. 

Running the tool
----------------
Change to the directory where the trm file resides. This will be the working directory of the python tool. There should be a subdirectory present called "Data". To get more information about the tool, simply run (assuming you copied the py files to this very directory)

    python create_round_slides.py --help

