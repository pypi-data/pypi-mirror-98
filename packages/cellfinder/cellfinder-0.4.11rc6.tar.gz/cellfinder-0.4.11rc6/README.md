[![Python Version](https://img.shields.io/pypi/pyversions/cellfinder.svg)](https://pypi.org/project/cellfinder)
[![PyPI](https://img.shields.io/pypi/v/cellfinder.svg)](https://pypi.org/project/cellfinder)
[![Downloads](https://pepy.tech/badge/cellfinder)](https://pepy.tech/project/cellfinder)
[![Wheel](https://img.shields.io/pypi/wheel/cellfinder.svg)](https://pypi.org/project/cellfinder)
[![Development Status](https://img.shields.io/pypi/status/cellfinder.svg)](https://github.com/brainglobe/cellfinder)
[![Tests](https://img.shields.io/github/workflow/status/brainglobe/cellfinder/tests)](
    https://github.com/brainglobe/cellfinder/actions)
[![Coverage Status](https://coveralls.io/repos/github/brainglobe/cellfinder/badge.svg?branch=master)](https://coveralls.io/github/brainglobe/cellfinder?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Gitter](https://badges.gitter.im/brainglobe.svg)](https://gitter.im/BrainGlobe/cellfinder/?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3891338.svg)](https://doi.org/10.5281/zenodo.3891338)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://docs.brainglobe.info/cellfinder/contributing)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fcellfinder.info)](https://cellfinder.info)
[![Twitter](https://img.shields.io/twitter/follow/findingcells?style=social)](https://twitter.com/findingcells)
# Cellfinder
Whole-brain cell detection, registration and analysis.

---


Cellfinder is a collection of tools from the 
[Margrie Lab](https://www.sainsburywellcome.org/web/groups/margrie-lab) and
 others at the [Sainsbury Wellcome Centre](https://www.sainsburywellcome.org/web/), [UCL](https://www.ucl.ac.uk/)
 for the analysis of whole-brain imaging data such as 
 [serial-section imaging](https://sainsburywellcomecentre.github.io/OpenSerialSection/)
 and lightsheet imaging in cleared tissue.
 
 The aim is to provide a single solution for:
 
 * Cell detection (initial cell candidate detection and refinement using 
 deep learning).
 * Atlas registration (using [brainreg](https://github.com/brainglobe/brainreg))
 * Analysis of cell positions in a common space
 
Installation is with 
`pip install cellfinder`.

Basic usage:
```bash
cellfinder -s signal_images -b background_images -o output_dir --metadata metadata
```
Full documentation can be 
found [here](https://docs.brainglobe.info/cellfinder).
 
This software is at a very early stage, and was written with our data in mind. 
Over time we hope to support other data types/formats. If you have any 
questions or issues, please get in touch by 
[email](mailto:adam.tyson@ucl.ac.uk?subject=cellfinder), 
[gitter](https://gitter.im/BrainGlobe/cellfinder) or by 
[raising an issue](https://github.com/brainglobe/cellfinder/issues/new/choose).


---
## Illustration

### Introduction
cellfinder takes a stitched, but otherwise raw whole-brain dataset with at least 
two channels:
 * Background channel (i.e. autofluorescence)
 * Signal channel, the one with the cells to be detected:
 
![raw](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/raw.png)
**Raw coronal serial two-photon mouse brain image showing labelled cells**


### Cell candidate detection
Classical image analysis (e.g. filters, thresholding) is used to find 
cell-like objects (with false positives):

![raw](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/detect.png)
**Candidate cells (including many artefacts)**


### Cell candidate classification
A deep-learning network (ResNet) is used to classify cell candidates as true 
cells or artefacts:

![raw](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/classify.png)
**Cassified cell candidates. Yellow - cells, Blue - artefacts**

### Registration and segmentation (brainreg)
Using [brainreg](https://github.com/brainglobe/brainreg), 
cellfinder aligns a template brain and atlas annotations (e.g. 
the Allen Reference Atlas, ARA) to the sample allowing detected cells to be assigned 
a brain region.

This transformation can be inverted, allowing detected cells to be
transformed to a standard anatomical space.

![raw](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/register.png)
**ARA overlaid on sample image**

### Analysis of cell positions in a common anatomical space
Registration to a template allows for powerful group-level analysis of cellular
disributions. *(Example to come)*

## Examples
*(more to come)*

### Tracing of inputs to retrosplenial cortex (RSP)
Input cell somas detected by cellfinder, aligned to the Allen Reference Atlas, 
and visualised in [brainrender](https://github.com/brancolab/brainrender) along 
with RSP.

![brainrender](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/brainrender.png)

Data courtesy of Sepiedeh Keshavarzi and Chryssanthi Tsitoura. [Details here](https://www.youtube.com/watch?v=pMHP0o-KsoQ)


## Citing cellfinder

If you find cellfinder useful, and use it in your research, please cite the preprint outlining the cell detection algorithm:
> Tyson, A. L., Rousseau, C. V., Niedworok, C. J., Keshavarzi, S., Tsitoura, C., Cossell, L., Strom, M. and Margrie, T. W. (2021) “A deep learning algorithm for 3D cell detection in whole mouse brain image datasets’ bioRxiv, [doi.org/10.1101/2020.10.21.348771](https://doi.org/10.1101/2020.10.21.348771)

If you use any of the image registration functions in cellfinder, please also cite [brainreg](https://github.com/brainglobe/brainreg#citing-brainreg).

**If you use this, or any other tools in the brainglobe suite, please
 [let us know](mailto:adam.tyson@ucl.ac.uk?subject=cellfinder), and 
 we'd be happy to promote your paper/talk etc.**
