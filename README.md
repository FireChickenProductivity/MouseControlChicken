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

chicken choose default display: Opens a dialogue showing options for the default display for the active grid. An option can be chosen by dictating "choose (option number)". For a grid combination, you choose the default display for every sub grid that can be displayed.

chicken screen next: Makes the active mouse grid around the next screen. The word screen is optional.

chicken screen last: Makes the active mouse grid around the previous screen. The word screen is optional.

chicken screen (number): Makes the active mouse grid around the specified screen.

chicken (window|dough|when): Makes the active mouse grid around the active window.

chicken follow (window|dough|when): Makes the active mouse grid around the active window and remakes it around the window as it moves.

chicken follow screen: Makes the active mouse grid around the screen containing the active window and remix it around the screen if the active window moves to a different screen.

chicken refresh: Refreshes the mouse grid and reloads the active settings from their defaults.

chicken (down or up) (optional number_small): Starts continuously scrolling down or up respectively. The optional number sets the scrolling speed.

### Grid Showing Commands

meet (mouse_control_chicken_coordinates): Moves the cursor to the specified position on the grid.

tap (mouse_control_chicken_coordinates): Left clicks the specified position on the grid.

pierce (mouse_control_chicken_coordinates): Double left clicks the specified position on the grid.

brush (mouse_control_chicken_coordinates): Right clicks the specified position on the grid.

(mouse_control_chicken_coordinates) slide (mouse_control_chicken_coordinates): Moves the cursor to the first specified position on the grid, starts dragging, moves to the second specified position on the grid, and stops dragging.

hold (mouse_control_chicken_coordinates): Starts dragging at the specified position on the grid.

drop (mouse_control_chicken_coordinates): Stops dragging at the specified position on the grid.

twist (mouse_control_chicken_coordinates): Moves the cursor to the specified position on the grid and then scrolls up.

roll (mouse_control_chicken_coordinates): Moves the cursor to the specified position on the grid and then scrolls down.

(down or up) (mouse_control_chicken_coordinates): Starts continuously scrolling down or up respectively at the specified position on the grid. You may optionally dictate "speed" (number_small) at the end to set the scrolling speed.

chicken crisscross: Toggles showing cross crossing lines on the display for rectangular frame grids.

chicken flicker: Toggles having the display flicker if the setting user.mouse_control_chicken_flickering_enabled is true. This causes the display to alternate between showing and not showing. user.mouse_control_chicken_flickering_show_time determines how long the display shows in milliseconds and user.mouse_control_chicken_flickering_hide_time determines how long the display hides in milliseconds. 

chicken flicker transparency: If the setting user.mouse_control_chicken_flickering_enabled is true, toggles having the display alternate between the primary and alternate transparency settings. This can be useful for switching between having high and low transparency to balance between making it easy to see what is behind the grid and making it easy to see the grid itself.

chicken checker frequency (number_small): This determines how frequently to show a position on a checker display. Every nth position will be shown where n is the frequency.

chicken zigzag (number_small): If 0, frame grids will not zigzag. Otherwise, the frames will be drawn in a zigzagging pattern instead of with straight lines where the number determines how many coordinates will be drawn before changing directions. This can make the grid obscure less of what is behind it but make reading the coordinates for a position somewhat harder.

chicken text size (number_small): temporarily changes the text size.

chicken main (transparency or transparent) (number_small): temporarily changes the main transparency.

chicken back (transparency or transparent) (number_small): temporarily changes the background transparency.

chicken line width (number_small): temporarily changes the line width.

chicken horizontal (procs or proximity) (number): temporarily changes the horizontal frame proximity distance for proximity frame displays.

chicken vertical (procs or proximity) (number): temporarily changes the vertical frame proximity distance for proximity frame displays.

chicken text color (color): temporarily changes the text color. Color options include black, white, red, green, blue, yellow, bright green, and bright blue.

chicken back color (color): temporarily changes the background color.

chicken line color (color): temporarily changes the line color.

chicken line (transparency or transparent) (number_small): temporarily changes the line transparency.

chicken quick (act or action) on:  This enables the quick action, so dictating the main coordinates on the grid (As opposed to secondary or tertiary coordinates) will activate the action specified by the user.mouse_control_chicken_quick_action setting (which is to click the position by default). The words act, action, and on are all optional.

chicken quick (act or action) off: Disables the quick action. The words act and action are optional.

### Narrowing Grid Showing Commands

If the active grid showing operates by narrowing around dictated coordinates, the following becomes available (The standard grid showing commands are still available and work the way they usually do but do not narrow the grid):

trace (mouse_control_chicken_coordinates): Narrows the grid and display around the specified position. Dictating mouse control chicken coordinates after dictating trace will narrow the grid and display around the specified position until the grid is re-expanded.

(mouse_control_chicken_coordinates) (mouse control chicken grid action, such as tap, brush, etc): Narrows the grid and display around the specified position, performs the specified action, and then re-expands the grid and display.

(mouse control chicken grid action) here: Performs the specified action using the middle of the grid as the position and then re-expands the grid and display.

### Continuous Scrolling Commands

Continuous scrolling activates a specialized mode where only the following scrolling commands are available.

(reverse or rev or verse): reverse the scrolling direction.

stop: exit scrolling mode and stop continuously scrolling.

(number_small): set the scrolling speed to the number. You may optionally proceed this with the word speed.

half: halve the scrolling speed.

double: double the scrolling speed.

slow: set the scrolling speed to 1.

skip (number_small): scroll an amount in the current scrolling direction based on the number dictated. 

back (number_small): scroll an amount in the opposite direction of the current scrolling direction based on the number dictated.

### Dialogue Options Commands

options (hide or close or off): Hides the options dialogue.

page next: Displays the next page if options if one is available.

page last: Displays the previous page.

choose (option number): Chooses the option with the specified number.

### Dictation Input Commands
Dictation input is available for some dialogues.

chicken choose (option): Sets the dictation input to the dictated option. Depending upon the specific dialogue, the option could be arbitrary dictation or limited.

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

![Frame Display](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/eb10f598-93df-4156-af0f-4637b2c5b4e9)

DoubleFrame: A RectangularGridFrame that also shows the horizontal and vertical coordinates in the middle of the grid.

![Double Frame](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/33f9f86e-c153-48a9-b9c6-fe57f7905ef4)

QuadrupleFrame: A RectangularGridFrame that essentially creates a DoubleFrame for each quadrant of the grid. It shows the vertical coordinates in the middle of the left and right halves of the grid and the horizontal coordinates in the middle of the top and bottom halves of the grid in addition to showing the coordinates in the middle of the grid.

![Quadruple Frame](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/4ebc56e8-c776-4925-8b30-5db002cdacd7)

RectangularPosition: Displays every position on the grid's primary coordinate system if the grid is big enough. The advantage of this over the UniversalPosition display is that it only shows positions that are far enough apart.

![Rectangular Position Display](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/fc1bde11-801b-4435-943c-aeca4afe1912)

RectangularChecker: Displays every nth position on the grid's primary coordinate system that is far enough apart to display where n is the checker frequency. 

![Rectangular Checker Display](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/f6d291ea-e559-4f3d-a83b-a07389f25e87)

Rectangular Diagonal Display: Shows the main diagonal coordinates.

![Rectangular Diagonal Display](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/5b2b112e-61dc-4d72-a767-5ea6f88c6f83)

Double Rectangular Diagonal Display: Shows the main diagonal coordinates for each quadrant.

![Double Rectangular Diagonal Display](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/569e5eda-14b5-4344-a6d8-20faab5e17ec)

Quadruple Rectangular Diagonal Display: Shows the main diagonal coordinates for each quadrant of each quadrant.

![image](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/39b5943e-ddb4-4a6e-a388-a0cda2ef035c)

Proximity Frame: Shows a frame display with vertical coordinate frame lines at every pixel distance given by the horizontal frame proximity distance and horizontal coordinate frame lines at every pixel distance given by the vertical frame proximity distance. The default values for this can be set with the user.mouse_control_chicken_default_horizontal_frame_proximity_distance and user.mouse_control_chicken_default_vertical_frame_proximity_distance settings. The main advantage this has over the double and quadruple frames is that it will cover less of the screen with smaller windows while still making it easier to see the coordinates with bigger areas.

#### Narrow Grid Display Options

Narrow: Draws every region on the grid's primary coordinate system and shows the corresponding coordinate in the middle of the region.

![Narrow Display](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/53959b6f-3f30-4bc4-a3ce-fdb5d4a8c6e7)

DoubleNarrow: Behaves like the Narrow option but also shows the regions of the secondary coordinates using half lines.

![Double Narrow Display](https://github.com/FireChickenProductivity/MouseControlChicken/assets/107892169/ce99a1b5-2327-4102-88dd-40ba5e47fc8d)

### Creating Custom Grids

The grid creation process can be initiated with the "chicken create grid" command. The process initially asks for a name for the grid. You should provide a unique name. The process next asks you to choose the type of grid. 

Square Recursive Division Grid is what the one to nine grid uses. You can pick a number between 2 and 9 for the division factor. The resulting grid will divide the base rectangle into the square of the division factor. 

Rectangular Recursive Division Grid is like the square recursive division grid but allows you to pick a division factor for the horizontal and vertical directions separately. You can pick division factors of less 1 to 99, but dividing the screen into more than 99 squares will divide the screen further than the current coordinate dictation capture currently supports and is not recommended.

Alphabet is a clone of the alphabet grid.

Double Alphabet is a clone of the double alphabet grid.

Recursively Divisible Combination let you put one grid inside another such as how the alphabet numbers grid has the alphabet grid as the primary and the one to nine as the secondary. Having a square or rectangular recursive division grid as the primary will have the recursive aspect removed so that it only provides the top level of the grid. Currently, only one combination can be put inside a combination.

Horizontal Doubling: creates a doubled version of a grid such that a copy of the grid is on the left and another copy is on the right. Performing actions by dictating an action followed by a position will perform the operation on the position on the grid copy on the left. Performing actions by dictating a position followed by an action will perform the operation on the position on the grid copy on the right.

Vertical Doubling: creates a doubled version of a grid such that a copy of the grid is on the top and another copy is on the bottom. Performing actions by dictating an action followed by a position will perform the operation on the position on the grid copy on the top. Performing actions by dictating a position followed by an action will perform the operation on the position on the grid copy on the bottom.

Doubling currently does not work properly with narrowable grids and will never work with having multiple doubled grids inside a single combination.

Cloning an existing grid can be useful if you want multiple options for the same grid that have different default displays.

After you pick the grid type, the process will ask you to provide any needed grid arguments.

Next, the process will ask you to choose the default display.

The grid creation process does not currently make sure that your input makes sense. Providing input that this document explains is not a valid option may have unexpected results.

During the process, choose an enumerated option with the corresponding number.

## Settings
Mouse Control Chicken generates a settings file in the data directory called settings.talon. If you want to read the description for any setting, you can find it in the settings definitions in SettingsMediator.py. Changes to some settings may require using the "chicken refresh" command to take effect in the current talon session.

user.mouse_control_chicken_default_rectangle_manager is a string setting that determines the default strategy for deciding what to draw the grid around. The options correspond to the commands for setting the rectangle manager and are "window", "screen", "follow window", and "follow screen". "screen" will be used if you provide an invalid value.

## Dependencies
The project depends upon the following from the community repository:

user.letter capture

user.mouse_drag action

user.mouse_drag_end action

## Known Issues

Grids might not work properly if you try to make them around a very very tiny rectangle that has fewer pixels than the grid has coordinates in a dimension. Fixing this is planned but not a high priority right now.

Updating any of the python files in this project might require restarting talon for mouse control chicken to work properly.

A few features may not work on a fresh installation until after talon is restarted, but I should be able to fix this.

## Inspiration
The project was inspired by the following repositories:

https://github.com/tararoys/modified_full_mouse_grid

https://github.com/tararoys/dense-mouse-grid

In particular, I was inspired by the idea of an alphabet based grid as well as the idea of a checker display. 

The community repository (https://github.com/talonhub/community) mouse grid influenced my default color scheme.

My default font and recommended alternative came from 2 of the fonts recommended by the [Flex Grid](https://github.com/brollin/flex-mouse-grid). 

## Credit
I used GitHub Copilot on this project. It did an astonishingly good job of offering useful code completions that mimicked my coding style. Without Copilot, I would not have been able to develop Mouse Control Chicken so quickly without wearing out my voice. If you have to program a lot of Talon Voice customization in python, I highly recommend using Copilot to make your life easier.
