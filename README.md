# trafficanalytics
This directory contains IPython scripts for analyzing real-world speed observations from sensors.

**Traffic Event Extraction From Tweets**

This project has two major components: (1) Annotator and (2) Extractor

**Annotator**

Sequence labeling model trained with declarative knowledge from location and event knowledge base is utilized for annotation of raw tweets. Open Street Maps [1] is used as a location based knowledge specific to a city and 511.org [2] schema of events is used as a knowledge of traffic related events. Each word in a tweet is assigned a tag (one of: B-LOCATION, I-LOCATION, B-EVENT, I-EVENT, OTHER).

Download all the data files from [3] and place it in a directory called "data". Download all the models (from files tab) and place it in a directory called "models". You can invoke the annotator using the command: 

*java -cp eventannotation.jar org.ccsr.tagging.CreateAnnotatedData models/model-twitter*

This code will take a while to run and the output is a file containing all the event terms and locations (this file is named final-training-data.txt). This file is the input for the extraction phase that follows.

**Extractor**

Extraction algorithms use space, time and theme characteristic of city events to aggregate all the tags for emitting events.

Download *extractevents.py* and place the output of the annotation phase (final-training-data.txt) in a directory called "data". Invoke the python script for aggregating annotations to emit events using the command:

*/usr/bin/python extractevents.py* 

***Visualization***
We have created a prototype to visualize all the city events both from city department (511.org) and the events we have extracted from tweets -- http://bit.ly/1gcSvLz

**References**

[1] Open Street Maps: http://www.openstreetmap.org/

[2] 511.org knowledge of traffic events: http://511.org/docs/TOMSSchema.zip

[3] Dataset used for experiments: https://app.box.com/s/uvws6ztf5jzbc8cxmb9b4r6a1zuei0pt


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
