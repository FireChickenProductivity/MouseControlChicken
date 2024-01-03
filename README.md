# MouseControlChicken
Offers talon voice customization for controlling the mouse. The project currently offers mouse grid systems.

## Mouse Grids
Mouse Control Chicken currently offers a few mouse grids and limited support for creating custom grids. Every grid can be represented graphically with multiple displays.

### Global Commands

chicken choose grid (grid name): Changes the active grid to the specified one.

chicken hide: Closes the active grid.

chicken show: Shows the active grid.

chicken choose grid: Opens a dialogue showing options for the grid. An option can be chosen by dictating "choose (option number)".

chicken choose display: Opens a dialogue showing options for the display for the active grid. An option can be chosen by dictating "choose (option number)".

chicken choose default display: Opens a dialogue showing options for the default display for the active grid. An option can be chosen by dictating "choose (option number)".

chicken screen next: Makes the active mouse grid around the next screen. The words screen is optional.

chicken screen last: Makes the active mouse grid around the previous screen. The words screen is optional.

chicken screen (number): Makes the active mouse grid around the specified screen.

chicken (window|dough|when): Makes the active mouse grid around the active window.

chicken refresh: Refreshes the mouse grid and reloads the active settings from their defaults.

### Grid Showing Commands

meet (mouse_control_chicken_coordinates): Moves the cursor to the specified position on the grid.

tap (mouse_control_chicken_coordinates): Left clicks specified position on the grid.

pierce (mouse_control_chicken_coordinates): Double left clicks the specified position on the grid.

brush (mouse_control_chicken_coordinates): Right clicks the specified position on the grid.

(mouse_control_chicken_coordinates) slide (mouse_control_chicken_coordinates): Moves the cursor to the first specified position on the grid, starts dragging, moves to the second specified position on the grid, and stops dragging.

hold (mouse_control_chicken_coordinates): Starts dragging at the specified position on the grid.

drop (mouse_control_chicken_coordinates): Stops dragging at the specified position on the grid.

chicken crisscross: Toggles showing cross crossing lines on the display for rectangular grids.

chicken checker frequency (number_small): This determines how frequently to show a position on a checker display. Every nth position will be shown where n is the frequency.

### Narrowing Grid Showing Commands

If the active grid showing operates by narrowing around dictated coordinates, the following becomes available (The standard grid showing commands are still available and work the way they usually do but do not narrow the grid):

trace (mouse_control_chicken_coordinates): Moves the cursor to the specified position on the grid and shows the grid narrowed around that position.

