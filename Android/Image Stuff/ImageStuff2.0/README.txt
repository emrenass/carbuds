TO be added at the desired packages

///////////////////////////////////////////////////////////////////////////////////////////

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

///////////////////////////////////////////////////////////////////////////////////////////
HOW TO USE: 
///////////////////////////////////////////////////////////////////////////////////////////

ProfilePicture:

Must pass an ImageView object.



ProfilePictureNOGUI:
  
Using class must pass an object implementing required interfaces  



PFPSetActivity:

Using class must pass an objecy implementing required interfaces on .execute()


///////////////////////////////////////////////////////////////////////////////////////////
INTERFACES 
///////////////////////////////////////////////////////////////////////////////////////////

To enforce the callback functions.


///////////////////////////////////////////////////////////////////////////////////////////
WHAT IT DOES:
///////////////////////////////////////////////////////////////////////////////////////////

ProfilePicture:

Asynchronously updates the ImageView on construction.

.synch() on the ProfilePicture object will trigger another update chain.



ProfilePictureNOGUI:

Asynchronously updates the Object implementing required interface on construction.

.synch() on the rofilePictureNOGUI object will trigger another update chain.



PFPSetActivity:

Asynchronously updates the database on .execute(), when finished updates the 
Object implementing required interface on construction for signaling.

Can be disposed off or reused.(.execute())


/////////////////////////////////////////////////////////////////////////////////////////////
NOTE: 
/////////////////////////////////////////////////////////////////////////////////////////////

Threads with objects waiting response should NEVER sleep on mid execution, 
BECAUSE they update when the thread is idle, sleep prevents that. 

 
Initiating them on UI threads( on component code) is recomended since UI component design 
shouldn't have too long procedures on them
