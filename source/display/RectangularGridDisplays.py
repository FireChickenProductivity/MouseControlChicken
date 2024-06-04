from .Display import FrameDisplay, PositionDisplay, BoundariesTouching
from .Skipper import Skipper, HorizontalSkipper, VerticalSkipper, SkipperRunner, SingleNestedSkipperRunner, SkipperComposite, CheckerSkipper
from ..grid.Grid import Grid, RectangularGrid, Rectangle
from ..grid.GridCalculations import compute_primary_grid
from .Canvas import Text, Line, Canvas
from ..RectangleUtilities import compute_average, compute_rectangle_corners
from ..SettingsMediator import settings_mediator
from ..fire_chicken.mouse_position import MousePosition
from typing import Callable, Generator

class RectangularGridFrameDisplay(FrameDisplay):
    def __init__(self):
        super().__init__()
        self.grid: RectangularGrid = None

    def set_grid(self, grid: RectangularGrid): 
        primary_grid = compute_primary_grid(grid)
        super().set_grid(primary_grid)

    def draw_on_canvas_given_boundaries_touching(self, canvas: Canvas, boundaries_touching: BoundariesTouching):
        self.canvas = canvas
        self._add_main_frame(boundaries_touching)
        if self._should_show_crisscross():
            self._add_crisscross()
    
    def _add_main_frame(self, boundaries_touching: BoundariesTouching):
        frame_offset = settings_mediator.get_frame_grid_offset()
        self._add_horizontal_coordinates_to_frame(self.rectangle.top + frame_offset)
        if boundaries_touching.is_touching_bottom_boundary():
            self._add_horizontal_coordinates_to_frame(self.rectangle.bottom - frame_offset)
        self._add_vertical_coordinates_to_frame(self.rectangle.left + frame_offset)
        if boundaries_touching.is_touching_right_boundary():
            self._add_vertical_coordinates_to_frame(self.rectangle.right - frame_offset)

    def _add_horizontal_coordinates_to_frame(self, vertical: int):
        self._add_coordinates_to_frame(
            vertical, 
            self.grid.get_horizontal_coordinates(), 
            self.grid.compute_absolute_horizontal_from_horizontal_coordinates, 
            HorizontalSkipper(), 
            is_horizontal=True
        )

        
    def _add_vertical_coordinates_to_frame(self, horizontal: int):
        self._add_coordinates_to_frame(
            horizontal, 
            self.grid.get_vertical_coordinates(), 
            self.grid.compute_absolute_vertical_from_from_vertical_coordinates, 
            VerticalSkipper(),
            is_horizontal=False
        )
            
    def _add_coordinates_to_frame(
            self, 
            constant_coordinate: int, 
            coordinates: Generator, 
            compute_absolute_coordinate_from_coordinate: Callable[[str], int], 
            skipper: Skipper,
            *,
            is_horizontal: bool
        ):
        runner = SkipperRunner(skipper)
        runner.set_generator(coordinates)
        def create_position(coordinate, constant_coordinate, is_horizontal):
            absolute_coordinate = compute_absolute_coordinate_from_coordinate(coordinate)
            horizontal, vertical = self._compute_horizontal_and_vertical_from_absolute_and_constant_coordinates(absolute_coordinate, constant_coordinate, is_horizontal=is_horizontal)
            return MousePosition(horizontal, vertical)
        runner.set_position_creator(lambda coordinate: create_position(coordinate, constant_coordinate, is_horizontal))
        def on_inclusion(coordinate, position):
            self._draw_text_on_canvas(coordinate, position.get_horizontal(), position.get_vertical())
        runner.set_on_inclusion(on_inclusion)
        runner.run()

    @staticmethod
    def _compute_horizontal_and_vertical_from_absolute_and_constant_coordinates(absolute_coordinate: int, constant_coordinate: int, *, is_horizontal: bool):
        if is_horizontal:
            horizontal = absolute_coordinate
            vertical = constant_coordinate
        else:
            horizontal = constant_coordinate
            vertical = absolute_coordinate
        return horizontal, vertical

    def _draw_text_on_canvas(self, text: str, horizontal: int, vertical: int):
        text = Text(horizontal, vertical, text)
        self.canvas.insert_text(text)

    def _should_show_crisscross(self) -> bool:
        return settings_mediator.get_frame_grid_should_show_crisscross()

    def _add_crisscross(self):
        self._add_vertical_lines()
        self._add_horizontal_lines()

    def _add_vertical_lines(self):
        skipper = HorizontalSkipper()
        runner = SkipperRunner(skipper)
        runner.set_generator(self.grid.get_horizontal_coordinates())
        runner.set_on_inclusion(lambda item, position: self.canvas.insert_line(Line(position.get_horizontal(), self.rectangle.top, position.get_horizontal(), self.rectangle.bottom)))
        runner.set_position_creator(lambda coordinate: MousePosition(self.grid.compute_absolute_horizontal_from_horizontal_coordinates(coordinate), 0))
        runner.run()
        
    def _add_horizontal_lines(self):
        skipper = VerticalSkipper()
        runner = SkipperRunner(skipper)
        runner.set_generator(self.grid.get_vertical_coordinates())
        runner.set_on_inclusion(lambda item, position: self.canvas.insert_line(Line(self.rectangle.left, position.get_vertical(), self.rectangle.right, position.get_vertical())))
        runner.set_position_creator(lambda coordinate: MousePosition(0, self.grid.compute_absolute_vertical_from_from_vertical_coordinates(coordinate)))
        runner.run()
    
    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        return is_rectangular_grid(grid)

class DoubleFrameDisplay(RectangularGridFrameDisplay):
    def draw_on_canvas_given_boundaries_touching(self, canvas: Canvas, boundaries_touching: BoundariesTouching):
        super().draw_on_canvas_given_boundaries_touching(canvas, boundaries_touching)
        self._add_middle_frame(self.rectangle)

    def _add_middle_frame(self, rectangle: Rectangle):
        middle_vertical = round(compute_average(rectangle.bottom, rectangle.top))
        self._add_horizontal_coordinates_to_frame(middle_vertical)
        middle_horizontal = round(compute_average(rectangle.left, rectangle.right))
        self._add_vertical_coordinates_to_frame(middle_horizontal)
    
class QuadrupleFrameDisplay(DoubleFrameDisplay):
    def draw_on_canvas_given_boundaries_touching(self, canvas: Canvas, boundaries_touching: BoundariesTouching):
        super().draw_on_canvas_given_boundaries_touching(canvas, boundaries_touching)
        coroners = compute_rectangle_corners(self.rectangle)
        for corner in coroners: 
            self._add_middle_frame(corner)
        
class RectangularPositionDisplay(PositionDisplay):
    """For every horizontal and vertical coordinate combination, show the absolute position of the cursor."""
    def __init__(self):
        super().__init__()
        self.grid: RectangularGrid = None
    
    def set_grid(self, grid: RectangularGrid): 
        primary_grid = compute_primary_grid(grid)
        super().set_grid(primary_grid)
    
    def draw_on(self, canvas: Canvas):
        self.canvas = canvas
        self._add_positions()
    
    def _add_positions(self):
        runner = self._create_skipper_runner()
        runner.set_outer_generator(self.grid.get_vertical_coordinates())
        runner.set_inner_generator_creation_function(self.grid.get_horizontal_coordinates)
        runner.set_outer_value_creator(lambda coordinate: self.grid.compute_absolute_vertical_from_from_vertical_coordinates(coordinate))
        runner.set_outer_position_creator(lambda coordinate, vertical: MousePosition(0, vertical))
        runner.set_inner_position_creator(
            lambda horizontal_coordinate, vertical: MousePosition(self.grid.compute_absolute_horizontal_from_horizontal_coordinates(horizontal_coordinate), vertical)
            )
        runner.set_text_creator(lambda vertical_coordinate, horizontal_coordinate: self._compute_text_to_display(horizontal_coordinate, vertical_coordinate))
        runner.set_on_inclusion(lambda outer_item, inner_item, position: self._display_text_for_position(inner_item, outer_item, position))
        runner.run()
    
    def _display_text_for_position(self, horizontal_coordinate: str, vertical_coordinate: str, position: MousePosition):
        text = Text(position.get_horizontal(), position.get_vertical(), self._compute_text_to_display(horizontal_coordinate, vertical_coordinate))
        self.canvas.insert_text(text)

    def _compute_text_to_display(self, horizontal_coordinate: str, vertical_coordinate: str) -> str:
        return vertical_coordinate + self.grid.get_coordinate_system().get_separator() + horizontal_coordinate

    def _create_skipper_runner(self) -> SingleNestedSkipperRunner:
        runner = SingleNestedSkipperRunner(VerticalSkipper(), HorizontalSkipper())
        return runner

    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        return is_rectangular_grid(grid)
    
class RectangularCheckerDisplay(RectangularPositionDisplay):
    def _create_skipper_runner(self) -> SingleNestedSkipperRunner:
        checker_frequency = settings_mediator.get_checker_frequency()
        inner_skipper = SkipperComposite([CheckerSkipper(checker_frequency), HorizontalSkipper()])
        runner = SingleNestedSkipperRunner(VerticalSkipper(), inner_skipper)
        return runner

def is_rectangular_grid(grid: Grid) -> bool:
    primary_grid = compute_primary_grid(grid)
    return isinstance(primary_grid, RectangularGrid)