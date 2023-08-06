# ALS.Liam (version 0.9)

Overview
---
_**Liam**_ is a Python module used to visualize CCD data that was collected 
on the **Scattering Chamber** located at **Beamline 4.0.2** 
(_a.k.a. **BL402**_) of the **Advanced Light Source** (Berkeley, CA USA). 
This module utilizes the _**ALS.Milo**_ package for processing the data.

It is distributed under the _namespace package_, _**ALS**_. 

Installation
---
### Install from PyPI
**_ALS.Liam_** can be installed from PyPI using `pip`.
The following example shows how.

```bash
>> sudo python -m pip install ALS.Liam -vv
```

### Install from local repository (download)
**_ALS.Liam_** can be installed from a local copy of the project repository 
using `pip`. The following example shows how.

```bash
>> cd ALS.Liam-0.9.0/  # Local directory of project repository
>> sudo python -m pip install . -vv
```

Background information
---
Data from the BL402 Scattering Chamber is stored in two types of files:

* **FITS files**: Each image captured by the CCD (_a.k.a._ the camera) is 
stored in a separate file using the _FITS_ format. _More details below._
https://fits.gsfc.nasa.gov/fits_documentation.html
* **Scan summary files**: When a scan sequence is run to collect data, a text 
file is created to summarize the parameters of the scan and the data collected. 
These files typically end with the extension "*-AI.txt".

Every _scan summary file_ contains a header that describes the scan and the 
types of data recorded, followed by data rows -- one row per data point. An 
_Instrument Scan_ provides an _image filename_ in each data row that can be 
used to access the CCD images recorded during the scan.

Using the FITS Viewer to visualize your data
---
To start the viewer, run the following command in your terminal or prompt:

```bash
python fitsViewer.py
```

### Load data files
* Click `Load data file` button to open a file selection dialog.
* Select file for display. This can be a `.FITS` file, a `*-AI.txt` file, or 
many image file types (`.png`, `.jpg`, etc.)
* If the file type you are looking for is not displayer or not selectable, it 
might be necessary to change the file filter to the appropriate file extension.
    * Mac: For OS X, the file filter might be hidden. If so, click the 
    `Options` button in the file selection dialog.
    * Selecting a `*-AI.txt` file will allow you to browse all FITS files that 
    were collected as part of this data scan

### Viewing the data
Image data is displayed in the central region. File name and location are 
displayed near the top of the window. To the right of the image is a color 
scale bar and histogram of the data intensity values. The color scale of the 
image can be adjusted with these controls (see _Adjusting the color scale_). 
To the left and also to the bottom of the plot are 1D representations of the 
image intensity, collapsed along the orthogonal dimension. The rows and columns 
can be restricted for these 1D plots using control bars in the image plot 
(see _Setting ROI horizontal and vertical limits_). The cursor displays the 
row, column, and intensity value for the pixel under the cross-hair.

### Zoom or pan 2D data
The image magnification (zoom) can be changed by using the middle mouse button 
(or scroll wheel). Clicking-and-dragging the mouse on the image will recenter 
(pan) the image by the amount that you drag it.

### Adjusting the color scale
Drag the yellow bars (between the intensity labels and the color bar) to adjust 
the upper or lower limit of color scaling. There are options for autoscaling 
the intensity (covers full range) or toggling between linear and log intensity 
scale; these are activated by the corresponding checkboxes. The colored arrows 
to the right of the color bar allow the color scale to be manipulated. These 
arrows can be relocated, added (by double-clicking in an empty space), removed 
(right-click for context menu), or be changed to other colors (click on arrow).

### Setting ROI horizontal and vertical limits
A Region of Interest (ROI) can be selected from the image by setting horizontal 
and/or vertical limits. This is done by dragging the yellow or blue bars that 
are initially located at the left and bottom edges of the image. The 
highlighted blue (yellow) regions are averaged to generate the blue (yellow) 
1D plots. Initially the 1D plots average data across the entire image before 
the selection bars are first moved. Returning the selection bars to their 
initial position recovers this initial state. Intensity values for the 1D 
plots are displayed in the average counts per pixel.

### Navigate FITS files within a scan set
Click `Prev` or `Next` buttons to display the previous or next image in the 
scan data set. `First` and `Last` buttons will display the first or last image 
in the scan data set. The image number can be typed directly into the entry 
field to the left of these buttons. If an out-of-range value is entered, it 
will automatically select the nearest available image.

Navigation is only possible for `*-AI.txt` files. The image number persists 
between data sets; i.e., it does not change when you load a new data set 
(unless it is out-of-bounds for the new data set).

### Reloading (incomplete) data sets
Click `Reload` to reload the data file with the most recent information. This 
is most useful for datasets (`*-AI.txt` files) that were incomplete when 
initially loaded (because data was still being captured or transfered).

### Export plots
Right-click on image or plot, then select `Export`. Select region, format, and 
other options. Data can be exported to file or copied to clipboard.

Notes for Developers
---

### Additional test data
Additional CCD data files and scan sets can be downloaded from these links.
Unzip and place the contents into the `test_data` folder.

* CCD Scan 8032: [https://zenodo.org/record/3923169#.Xvs-hi2ZPxg
](https://zenodo.org/record/3923169#.Xvs-hi2ZPxg)
* CCD Scan 8044: [https://zenodo.org/record/3923175#.XvqZcS2ZPxg
](https://zenodo.org/record/3923175#.XvqZcS2ZPxg)


Copyright Notice
---
ALS.Liam: BL402 CCD image viewer for RSXD data, Copyright (c) 2017-2019, 2021, 
The Regents of the University of California, through Lawrence Berkeley 
National Laboratory (subject to receipt of any required approvals from the 
U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software, 
please contact Berkeley Lab's Intellectual Property Office at IPO@lbl.gov.

NOTICE. This Software was developed under funding from the U.S. Department of 
Energy and the U.S. Government consequently retains certain rights. As such, 
the U.S. Government has been granted for itself and others acting on its 
behalf a paid-up, nonexclusive, irrevocable, worldwide license in the 
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit other to do 
so. 