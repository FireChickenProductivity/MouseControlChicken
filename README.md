# Mouse Control Chicken
Offers talon voice customization for controlling the mouse. The project currently offers mouse grid systems. 

The system is intended to be useful now but is still early in development. There are plans to add more grid and display options as well as commands for dealing with scrolling by voice.

The project has only been tested on windows.

The data directory mentioned below should be created in the talon user directory and called "Mouse Control Chicken Data". 

## Mouse Grids
Mouse Control Chicken currently offers a few mouse grids and limited support for creating custom grids. Every grid can be represented graphically with multiple displays.

### Global Commands

chicken choose grid (grid name): Changes the active grid to the specified one.

chicken hide: Closes the active grid.

chicken show: Shows the active grid.

chicken choose grid: Opens a dialogue showing options for the grid. An option can be chosen by dictating "choose (option number)".

chicken choose display: Opens a dialogue showing options for the display for the active grid. An option can be chosen by dictating "choose (option number)".

chicken choose default display: Opens a dialogue showing options for the default display for the active grid. An option can be chosen by dictating "choose (option number)".

chicken screen next: Makes the active mouse grid around the next screen. The word screen is optional.

chicken screen last: Makes the active mouse grid around the previous screen. The word screen is optional.

chicken screen (number): Makes the active mouse grid around the specified screen.

chicken (window|dough|when): Makes the active mouse grid around the active window.

chicken refresh: Refreshes the mouse grid and reloads the active settings from their defaults.

### Grid Showing Commands

meet (mouse_control_chicken_coordinates): Moves the cursor to the specified position on the grid.

tap (mouse_control_chicken_coordinates): Left clicks s1pecified position on the grid.

pierce (mouse_control_chicken_coordinates): Double left clicks the specified position on the grid.

brush (mouse_control_chicken_coordinates): Right clicks the specified position on the grid.

(mouse_control_chicken_coordinates) slide (mouse_control_chicken_coordinates): Moves the cursor to the first specified position on the grid, starts dragging, moves to the second specified position on the grid, and stops dragging.

hold (mouse_control_chicken_coordinates): Starts dragging at the specified position on the grid.

drop (mouse_control_chicken_coordinates): Stops dragging at the specified position on the grid.

chicken crisscross: Toggles showing cross crossing lines on the display for rectangular frame grids.

chicken checker frequency (number_small): This determines how frequently to show a position on a checker display. Every nth position will be shown where n is the frequency.

### Narrowing Grid Showing Commands

If the active grid showing operates by narrowing around dictated coordinates, the following becomes available (The standard grid showing commands are still available and work the way they usually do but do not narrow the grid):

trace (mouse_control_chicken_coordinates): Narrows the grid and display around the specified position. Dictating mouse control chicken coordinates after dictating trace will narrow the grid and display around the specified position until the grid is re-expanded.

(mouse_control_chicken_coordinates) (mouse control chicken grid action, such as tap, brush, etc): Narrows the grid and display around the specified position, performs the specified action, and then re-expands the grid and display.

(mouse control chicken grid action) here: Performs the specified action using the middle of the grid as the position and then re-expands the grid and display.

### Dialogue Options Commands

options (hide or close or off): Hides the options dialogue.

page next: Displays the next page if options if one is available.

page last: Displays the previous page.

choose (option number): Chooses the option with the specified number.

### Dictation Input Commands
Dictation input is available for some dialogues.

choose (option): Sets the dictation input to the dictated option. Depending upon the specific dialogue, the option could be arbitrary dictation or limited.

accept: Accepts the dictation input and closes the dialogue.

reject: Cancels the dialogue.

### Default Grid Options

#### double alphabet numbers
Offers a primary 52 by 52 grid with a secondary recursively narrowable 1-9 grid around each position. The primary grid coordinates are based on uppercase and lowercase letters in the english alphabet. Lowercase letters are referred to with the user.letter capture's phonetic alphabet. Uppercase letters are referred to with the user.mouse_control_chicken_uppercase_letter talon list generated within the data directory in the uppercase_letters.talon-list file. A position on the primary grid is dictated with the letter corresponding to the vertical followed by the letter corresponding to the horizontal. Positions on the primary grid may be utilized without referencing the secondary. Numbers between 1 and 9 can optionally be used at the end of the position for more fine grained mouse control equivalent to utilizing a one to nine grid around the position on the primary grid.

#### one to nine
Divides the screen into 9 squares. 1 is the top left square. 2 is the top middle square. 3 is the top right square. 4 is the middle left square. 5 is the middle square. 6 is the middle right square. 7 is the bottom left square. 8 is the bottom middle square. 9 is the bottom right square. Positions can be referred to with a sequence of numbers between 1 and 9. The resulting position is determined by taking the square given by the first number, dividing it into 9 squares like before, and then picking the square specified by the second number. The process repeats until all the numbers are used. The final position is the middle of the last square chosen.

#### alphabet numbers
Works the same as the double alphabet numbers grid but only offers the lower case letters on the primary grid.

#### alphabet
A single alphabet grid offering the primary grid system of the alphabet numbers grid but without the secondary grid. 

#### double alphabet
A double alphabet grid offering the primary grid system of the double alphabet numbers grid but without the secondary grid.

### Display Options
The display options available depend on the active grid.

#### Universal Display Options

UniversalPosition: Displays every position on the grid's primary coordinate system. This takes into account little information about the specifics of the grid and is generally a bad option.

#### Rectangular Grid Display Options
Rectangular displays take into account the size of the rectangle the grid is created around and consequently only draws coordinates not too close to already drawn coordinates during the drawing process.

RectangularGridFrame: Displays a frame around the grid. This shows the horizontal coordinates on the left and right of the frame and the vertical coordinates on the top and bottom of the frame.

DoubleFrame: A RectangularGridFrame that also shows the horizontal and vertical coordinates in the middle of the grid.

QuadrupleFrame: A RectangularGridFrame that essentially creates a DoubleFrame for each quadrant of the grid. It shows the vertical coordinates in the middle of the left and right halves of the grid and the horizontal coordinates in the middle of the top and bottom halves of the grid in addition to showing the coordinates in the middle of the grid.

RectangularPosition: Displays every position on the grid's primary coordinate system if the grid is big enough. The advantage of this over the UniversalPosition display is that it only shows positions that are far enough apart.

RectangularChecker: Displays every nth position on the grid's primary coordinate system that is far enough apart to display where n is the checker frequency. 

#### Narrow Grid Display Options

Narrow: Draws every region on the grid's primary coordinate system and shows the corresponding coordinate in the middle of the region.

DoubleNarrow: Behaves like the Narrow option but also shows the regions of the secondary coordinates using half lines.

### Creating Custom Grids

The grid creation process can be initiated with the "chicken create grid" command. The process initially asks for a name for the grid. You should provide a unique name. The process next asks you to choose the type of grid. 

Square Recursive Division Grid is what the one to nine grid uses. You can pick a number between 2 and 9 for the division factor. The resulting grid will divide the base rectangle into the square of the division factor. 

Alphabet is a clone of the alphabet grid.

Double Alphabet is a clone of the double alphabet grid.

Recursively Divisible Combination let you put one grid inside another such as how the alphabet numbers grid has the alphabet grid as the primary and the one to nine as the secondary. Having a square recursive division grid as the primary is currently not supported.

Cloning an existing grid can be useful if you want multiple options for the same grid that have different default displays.

After you pick the grid type, the process will ask you to provide any needed grid arguments.

Next, the process will ask you to choose the default display.

The grid creation process does not currently make sure that your input makes sense. Providing input that this document explains is not a valid option may have unexpected results.

During the process, choose an enumerated option with the corresponding number.

## Settings
Mouse Control Chicken generates a settings file in the data directory called settings.talon. If you want to read the description for any setting, you can find it in the settings definitions in SettingsMediator.py. Changes to some settings may require using the "chicken refresh" command to take effect in the current talon session.

## Dependencies
The project depends upon the following from the community repository:

user.letter capture

user.mouse_drag action

user.mouse_drag_end action

## Known Issues

Grids might not work properly if you try to make them around a very very tiny rectangle that has fewer pixels than the grid has coordinates in a dimension.

Updating any of the python files in this project might require restarting talon for mouse control chicken to work properly.

After updating a python file in this project, sometimes an old display would still be visible but could not be hidden. In the unlikely event that an old display gets stuck like that during normal use, please report the issue and explain as much as you can about what you did before that happened. 

## Inspiration
The project was inspired by the following repositories:

https://github.com/tararoys/modified_full_mouse_grid

https://github.com/tararoys/dense-mouse-grid/tree/dense_mouse_grid_2

In particular, I was inspired by the idea of an alphabet based grid.