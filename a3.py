import tkinter as tk
from tkinter import filedialog # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *
import os


class InfoBar(AbstractGrid):    
    """ A view class representing the InfoBar showing the day,
        player's money and player's inventory """
    
    def __init__(self, master: tk.Tk|tk.Frame) -> None:
        """ Constructor for Infobar.

        Parameters: 
            master: Tkinter frame, the class FarmGame.
        """
        self._master = master
        super().__init__(master,
                         (2,3),
                         (FARM_WIDTH+INVENTORY_WIDTH,INFO_BAR_HEIGHT))
                 
    def redraw(self, day: int, money: int, energy: int) -> None:
        """ Clears the info bar and redraws it to display the 
            day, and the player's money and energy.

        Parameters:
            day: Current day in game
            money: Player's money
            energy: Player's energy
        """
        self.clear()
        text = ('Day:', 'Money:', 'Energy:')
        info = (day, str('$'+ str(money)), energy)

        text_positions = [(i,j) for i in range (1) for j in range (3)]     
        for position in text_positions:
            self.annotate_position((position),
                                   text[position[1]],
                                   HEADING_FONT)
        
        info_positions = [(i,j) for i in range (1,2) for j in range (3)]
        for position in info_positions:
            self.annotate_position(position,
                                   info[position[1]])
    
class FarmView(AbstractGrid):    
    """  A view class representing the farmView in the game,
        a grid displaying the farm map, player, and plants.
    """
    
    def __init__(self, master: tk.Tk|tk.Frame,
                 dimensions: tuple[int,int], 
                 size: tuple[int,int], 
                 images_dir: str = 'images',
                 **kwargs) -> None:
        """ Constructor for FarmView

        Parameters:
            master: Tkinter frame, the class FarmGame.
            dimensions: Number of rows, numer of columns.
            size: Width in pixels, height in pixels.
            images_dir: Directory containg the images file
        """
        self._master = master
        self._images_dir = images_dir
        super().__init__(master, dimensions, size, **kwargs)
        self._images = {}

    def _put_image(self, image_filename, position):
        """ Takes the image from the filename and places it
            on the farm view. 

        Parameters:
            image_filename: filename of the image.
            positon: position to place image (row, col).
        """
        image_path = os.path.join(self._images_dir, image_filename)
        image = get_image(image_path,
                          self.get_cell_size(),
                          self._images)
        mid_point = self.get_midpoint(position)
        self.create_image(mid_point[0],
                          mid_point[1],
                          image=image)

    def redraw(self, ground: list[str],
                plants: dict[tuple[int, int], 'Plant'],
                player_position: tuple[int, int],
                player_direction: str) -> None:
        """ Clears the farm view, then places the images
            for the ground, the plants and the player on the farm view.

        Parameters:
            ground: List of letters representing the state of the ground.
            plants: Plant positon in (row, col) (key)
                    and the plant instance (value).
            player_positon: Positon of player (row, col).
            player_direction: Direction player is facing ('w' up,
                            'a' left, 's' down, 'd' right).
        """
        self.clear()
        
        # Place images for ground
        positions = [(row,col) for row in range (len(ground))
                     for col in range (len(ground[0]))]
        for position in positions:
            row, col = position
            state_ground = ground[row][col] 
            ground_image_filename = IMAGES[state_ground]
            self._put_image(ground_image_filename, position)
            
        # Place plant images
        for position, plant in plants.items():
            plant_image_filename = get_plant_image_name(plant)
            self._put_image(plant_image_filename, position)

        # Place player image
        player_image_filename = IMAGES[player_direction]
        self._put_image(player_image_filename, player_position)

    def clear_cache(self):
        """ Clears the farm view images cache """
        self._images={}                              

class ItemView(tk.Frame):
    """ A class representing a single item view showing the item name,
        the amount in the player's inventory, the buy price and sell price.
    """
    
    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """ Constructer for ItemView.

        Parameters:
            master: Tkinter frame, the class FarmGame.
            item_name: The item represented on the item view instance.
            select_command: Callback for selecting the item.
            sell_command: Callback for selling the item.
            buy_command: Callback for buying the item.
        """
        self._master = master
        self._item_name = item_name
        self._amount = amount
        super().__init__(master)

        # Functions for buy and sell button callbacks
        if item_name in ITEMS:
            buy_cmd = lambda item_name = item_name: buy_command(item_name)
            sell_cmd = lambda item_name = item_name: sell_command(item_name)

        # Create a single itemview
        self.config(relief=tk.RAISED,
                    borderwidth=2,
                    bg=INVENTORY_COLOUR)     
        label_text = self._get_label_text(item_name, amount) 
        self._label = tk.Label(self,
                               pady = 15.45,
                               text = label_text,
                               bg = INVENTORY_COLOUR)      
        self._label.pack(side = tk.LEFT)
        buy_price = BUY_PRICES.get(item_name,'N/A')
        
        if buy_price != 'N/A':     
            self._buy_button = self._create_button('Buy', buy_cmd)
        self._sell_button = self._create_button('Sell', sell_cmd)
        
        self.bind("<Button-1>", lambda event: select_command(item_name))
        self._label.bind("<Button-1>", lambda event: select_command(item_name)) 

    def _create_button(self, text, command):
        """ Returns a button for item view.

        Parameters:
            text: The text on the button.
            command: The callback command.

        Returns:
            The button with appropriate attributes, packed to left.
        """
        return tk.Button(self,
                         width = 6,
                         text = text,
                         bd = 0,
                         command = command).pack(side=tk.LEFT, padx=7)
     
    def _get_label_text(self, item_name:str, amount:int) -> str:
        """" Returns a string for the text on each item label

        Parameters:
            item_name: Item from ITEMS.
            amount: Amount of the item in the players inventory.

        Returns:
            Formatted string for itemview label.
        """
        buy_price = BUY_PRICES.get(item_name, 'N/A')
        sell_price = SELL_PRICES.get(item_name)
        return (f'{item_name}: {amount} \n' +
                f'Sell price: ${sell_price} \n' +
                f'Buy price: ${buy_price}')

    def update(self, amount:int, selected: bool=False)-> None:
        """ Updates the text on the label, and the colour of this ItemView
            appropriately.

        Parameters:
            amount: Amount of item in player's inventory.
            selected: Whether the item has been selected by player.
        """
        item_name = self._label['text'].split(':',1)[0]
        self._label.config(text = self._get_label_text(item_name,
                                                       amount))

        item_view_state =({(False, True): INVENTORY_EMPTY_COLOUR,
                          (False, False): INVENTORY_EMPTY_COLOUR,
                          (True, True): INVENTORY_SELECTED_COLOUR,
                          (True, False): INVENTORY_COLOUR})
        has_inventory = lambda amount: True if amount > 0 else False
        
        self._label.config(bg = item_view_state.get((has_inventory(amount),
                                                     selected)))
        self.config(bg = item_view_state.get((has_inventory(amount),
                                              selected)))

class FarmGame:
    """ The controller class for the overall game """
    def __init__(self, master: tk.Tk, map_file: str, images_dir: str) -> None:
        """ Constructor for FarmGame

        Parameters:
            master: Tk root object.
            map_file: Map of the ground for this game.
            images_dir: Directory containing the image files
        """
        self._master = master
        self._master.title('Farm Game')
        self._map_file = map_file
        self._images_dir = images_dir
        self._farm_model = FarmModel(map_file)      
        self._item_views = []
        self._player = self._farm_model.get_player()
        self._player_inventory = self._player.get_inventory()

        # File menu           
        menu = tk.Menu()
        self._master.config(menu=menu)  
        # File > 
        file_menu = tk.Menu(menu)
        menu.add_cascade (
                label = 'File',
                menu=file_menu)
        # File > Quit    
        quit_menu = tk.Menu(file_menu)        
        file_menu.add_command(
            label = "Quit",
            command = self._master.destroy)
        # File > Map Selection
        map_menu = tk.Menu(file_menu)
        file_menu.add_command(
            label = "Map selection",
            command=self._select_map_file)

        # Title banner with 'Farm Game' image
        title_banner = (get_image(os.path.join(images_dir, 'header.png'),
                                (FARM_WIDTH+INVENTORY_WIDTH,BANNER_HEIGHT),
                                ))
        title_banner_label = tk.Label(image=title_banner)
        title_banner_label.image = title_banner
        title_banner_label.place(x=3,y=3)
        
        # Next day button below the Info Bar to increase the day by one
        button_frame = tk.Frame(master, height=20)
        button_frame.pack(side=tk.BOTTOM)
        next_day_button=tk.Button(button_frame,
                                  bd=0,
                                  text='Next day',
                                  bg='white',
                                  command=self._next_day)
        next_day_button.pack()
        
        # Instances of view classes
        # Info bar
        self._info_bar = InfoBar(master)
        self._info_bar.pack(side = tk.BOTTOM) 

        # Farm view
        rows, cols = self._farm_model.get_dimensions()
        self._farm_view = FarmView(master, (rows, cols), 
                                   (FARM_WIDTH, FARM_WIDTH),
                                   images_dir=images_dir)
        self._farm_view.pack(side = tk.LEFT, anchor='sw')
  
        # Item view      
        for item_name in reversed(ITEMS):          
            amount = self._player_inventory.get(item_name, 0)
            self._item_view =ItemView(self._master, item_name, amount,
                                     self.select_item, self.sell_item,
                                     self.buy_item)           
            if amount == 0:
                self._item_view._label.config(bg = INVENTORY_EMPTY_COLOUR)
                self._item_view.config(bg = INVENTORY_EMPTY_COLOUR)
            self._item_view.pack(side = tk.BOTTOM, fill = tk.BOTH)
            self._item_views.append(self._item_view)
                      
        # Bind handle_keypress method to the '<KeyPress>' event
        master.bind('<KeyPress>', self.handle_keypress)
    
        # Call the redraw method to ensure the view draws
        # according to the current model state
        self.redraw()

    def _select_map_file(self):
        """ Command for File menu to open a new map file. """
        map_file = filedialog.askopenfilename()
        self._farm_model = FarmModel(map_file)
        self._player = self._farm_model.get_player()
        self._player_inventory = self._player.get_inventory()
        self._farm_view.set_dimensions(self._farm_model.get_dimensions())
        self._farm_view.clear_cache()
        self.redraw() 

    def _next_day(self) -> None: 
        """ Callback method for Next Day button on the info bar,
            increments the day in the game by one day.
        """
        self._farm_model.new_day()
        self.redraw()
  
    def redraw(self) -> None:
        """ Redraws the entire game based on the current model state. """

        # InfoBar
        money = self._player.get_money()
        days_elapsed = self._farm_model.get_days_elapsed()
        energy = self._player.get_energy()       
        self._info_bar.redraw(days_elapsed, money, energy)
        
        # FarmView                      
        ground = self._farm_model.get_map()
        position = self._player.get_position()
        direction = self._player.get_direction()
        plants = self._farm_model.get_plants()
        self._farm_view.redraw(ground, plants, position, direction)

        # ItemView
        selected_item = self._player.get_selected_item()
        for item_view in self._item_views:
            item_name = item_view._item_name       
            amount = self._player_inventory.get((item_name),0)
            if item_name == selected_item:
                item_view.update(amount, True)
            else:
                item_view.update(amount, False) 
            
    def handle_keypress(self, event: tk.Event) -> None:
        """ An event handler to be called when a keypress event occurs
            If a key is pressed that does not correspond to an event,
            it is ignored. """
        
        player_position = self._player.get_position()
        row, col = player_position 

        # Options to move player, up='w', down ='s',left ='a', right='d'
        if event.char in ('s','w','a','d'):
            self._farm_model.move_player(event.char)

        # Options to till ('t') and untill ('u') the soil    
        if event.char in ('t','u'):
            if event.char == 't': 
                self._farm_model.till_soil((row, col))
            if event.char == 'u': 
                self._farm_model.untill_soil((row, col))
                
        # Options to plant seeds ('p'), harvet ('h') and remove ('r') plants
        if event.char in ('p', 'h', 'r'):
            plant_classes = ({'Potato Seed': PotatoPlant,
                            'Kale Seed': KalePlant,
                            'Berry Seed': BerryPlant})
            selected_plant = self._player.get_selected_item() 
            plant_to_add = plant_classes.get(selected_plant) 
            qty_seed = self._player_inventory.\
                       get(selected_plant)
            ground = self._farm_model.get_map()[row][col]
            plant_at_position = self._farm_model.get_plants().get((row,col))
               
            if event.char == 'p': # Plant seed at players position.              
                # Plant seed if no plant already exists at player's position,
                # the player's position contains soil,
                # a seed is the selected item,
                # and player has a non-zero qty of the selected seed
                if (plant_at_position == None and
                    qty_seed !=0 and
                    qty_seed != None and
                    ground == 'S' and
                    selected_plant in SEEDS):
                        self._farm_model.add_plant(player_position, 
                                                   plant_to_add())
                        self._player.remove_item((selected_plant, 1))
   
            if event.char == 'h': # Harvest plant from players position and
                # add to inventory.

                # Do nothing if no plant exists at players position,
                # or plant not ready for harvet          
                if not plant_at_position:
                    return
                
                harvestable = plant_at_position.can_harvest()
                item_name = plant_at_position.get_name().title() 
                if harvestable:
                    self._farm_model.harvest_plant(player_position)
                    self._player.add_item((item_name,1))
                
            if event.char == 'r': # Remove palnt from player's position
                self._farm_model.remove_plant(player_position)
            
        self.redraw()
    
    def select_item(self, item_name: str) -> None:
        """ The callback for each ItemView instance for item selection."""
        self._player.select_item(item_name)
        self.redraw()
                  
    def buy_item(self, item_name: str) -> None:
        """ Callback for each ItemView instance button for buying items."""
        self._player.buy(item_name, BUY_PRICES.get(item_name))
        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """ Callback for each ItemView instance button for selling items."""
        self._player.sell(item_name, SELL_PRICES.get(item_name))
        self.redraw()    

def play_game(root: tk.Tk, map_file: str, images_dir: str) -> None:
    """ Sets up and runs the game with selected mapfile """
    FarmGame(root, map_file, images_dir) 
    root.mainloop() 

def main() -> None:
    """ Main function for the Farm Game. """
    root=tk.Tk()
    root.geometry('710x760')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(script_dir, 'maps', 'map1.txt')
    images_dir = os.path.join(script_dir, 'images')

    #map_file='./maps/map1.txt'
    play_game(root, map_file, images_dir)
    
if __name__ == '__main__':
    main()
