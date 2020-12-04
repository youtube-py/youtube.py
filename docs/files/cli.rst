.. _cli:

Command Line Input 
==================

.. _clihelp:

Help
----

.. code-block:: bash

   usage: youtube [-h] [-o OUTPUT] [-l] [-ff [FFMPEG] | -v [VIDEO] | -i ITAG | -s
                  | -a [AUDIO] | -r [RESOLUTION] | --version]
                  url

   Definitions:
     Quality Types: ('HIGH','MID', 'LOW')
     Video resolution examples. ('144', '240', '360', '480', '720', '1080') more/less depend on your video

   Note:
     Default values for '--ffmpeg', '--video', '--audio' is 'HIGH'
     Default values for '--resolution' is 720

   positional arguments:
     url                   Enter video or playlist url

   optional arguments:
     -h, --help            show this help message and exit
     -o OUTPUT, --output OUTPUT
                           Output location for downloading streams.
     -l, --logs            To enable extra logs.
     -ff [FFMPEG], --ffmpeg [FFMPEG]
                           FFMPEG downloads audio/video both then copy in one file, Pass the quality type.
     -v [VIDEO], --video [VIDEO]
                           Downlaod video (only progressive), Pass quality.
     -i ITAG, --itag ITAG  Download stream with itag, Pass itag id.
     -s, --streams         This argument will list the all available streams.
     -a [AUDIO], --audio [AUDIO]
                           Download audio, Pass quality.
     -r [RESOLUTION], --resolution [RESOLUTION]
                           Download stream with quality type, Pass video resolution.
     --version             Check the current version of youtube.py



Example
-------

``-r`` and ``--resolution`` have default resolution 720

.. code-block:: bash

   >>> youtube https://www.youtube.com/watch?v=3AtDnEC4zak -r
   Downloading : video : mp4: 720
   Process: [██████████████████████████████████████████████████] 100.0% Complete 0.0 Kb/s  /s
   Downloading : audio : webm: 76035
   Process: [██████████████████████████████████████████████████] 100.0% Complete 0.0 Kb/s  /s
   Charlie_Puth_-_We_Don't_Talk_Anymore_(feat.mp4 Downloaded


``-r`` and ``--resolution`` value can be overwritten

.. code-block:: bash

   >>> youtube https://www.youtube.com/watch?v=3AtDnEC4zak -r 1080
   Downloading : video : mp4: 1080
   Process: [██████████████████████████████████████████████████] 100.0% Complete 0.0 Kb/s  /s
   Downloading : audio : webm: 76035
   Process: [██████████████████████████████████████████████████] 100.0% Complete 0.0 Kb/s  /s
   Charlie_Puth_-_We_Don't_Talk_Anymore_(feat.mp4 Downloaded

.. note::
	Downloading with ``--resolution`` , ``--ffmpeg`` or with ``--video`` is different, 
	resolution and ffmpeg uses ``FFMPEG`` to download files and copy them in one but
	``--video`` download a single file made/generate by youtube which has audio/video both. but
	``--video`` cant always download files in better quality so preffer ``--resolution`` or ``--ffmpeg``
	use ``--video`` only when your system do not support :ref:`FFMPEG <installffmpeg>`

Example with ``--video``

.. code-block:: bash

   >>> youtube https://www.youtube.com/watch?v=3AtDnEC4zak --video high
   Process: [██████████████████████████████████████████████████] 100.0% Complete 0.0 Kb/s  s
   44Charlie_Puth_-_We_Don't_Talk_Anymore_(feat._Selena_Gomez)_[Official_Video].mp4 Downloaded

Example with ``--audio``

.. code-block:: bash

   >>> youtube https://www.youtube.com/watch?v=3AtDnEC4zak --audio high
   Process: [██████████████████████████████████████████████████] 100.0% Complete 0.0 Kb/s  /s
   71Charlie_Puth_-_We_Don't_Talk_Anymore_(feat._Selena_Gomez)_[Official_Video].webm Downloaded