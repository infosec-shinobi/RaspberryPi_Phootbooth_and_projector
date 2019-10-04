# RaspberryPi_Phootbooth_and_projector
Python code leveraging pygames to turn two raspberry pi's into a photobooth and projector.

PyBooth: runs the wedding photobooth app
PyProjector: runs the projector app

PyBooth needs a samba share which hosts the "GridPics" folder

Need to make sure the two pi's are networked togehter (I simply assigned each with x.x.x.1 and x.x.x.2). 

The "Launcer.sh" file in each app folder needs to be set up as a cron job to run at boot. 

Note, PyProjector has a built in 5 minute delay to launching (hardcoded in the code) to allow time for the samba share on PyBooth to get set up. 

Will flush this out more when I get some time and add some pics...
