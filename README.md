Final assignment for CSSE7030 Introduction to Software Engineering

The script runs a Farm Game.

The code structure is organized with separate classes for different views.
The code relies on helper python scripts and png images and text maps. 
These are the intellectual property of the University of Queensland so 
are not included here.  

The screen is divided into four views, the header, farm, information bar and item view.
The Header shows the title of the game. The information bar shows the number of days elapsed, 
money and energy the player has. The item view lists the plants and seeds available 
to buy and sell. The player can click on the items to select them (the item changes colour when
selected or when it becomes unavailable). The player moves around the farm using s (down), w (up), a (left) 
and d (right). The player can plant seeds by standing on tilled soiled, clicking on an seed item and 
clicking p (plant). The player can also till or untill soil (click 't' or 'u')any.
Clicking the next day button forwards the game one day, the player energy will 
increase and the images on any plants will update until they are ready to harvest. The player can 
harvest plants by standing next to a plant and clicking h (harvest). The farm, item views and information bar
will update accordingly. 

A File Menu is implemented that will allow the player to quit the game or load one of two map files.
