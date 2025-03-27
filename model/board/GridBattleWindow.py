import pygame
import sys
from pygame.locals import *
from model.board.BattleshipMatrix import BattleshipMatrix


class GridBattleWindow:
    """
    A window that displays a 10x10 grid for a Battleship game,
    with visual customization for different cell states:
    * 0 = water (no ship, no bomb)
    * 1 = ship (ship, no bomb)
    * -1 = water bombed (no ship, bomb landed)
    * 2 = ship bombed (ship, bomb landed)
    """

    # Constants for grid
    GRID_SIZE = 10
    CELL_SIZE = 40
    GRID_PADDING = 50

    # Colors
    BACKGROUND_COLOR = (50, 50, 50)  # Dark gray
    GRID_LINE_COLOR = (200, 200, 200)  # Light gray

    # State colors and patterns
    STATE_STYLES = {
        0: {"color": (0, 105, 148),  # Deep blue for water
            "pattern": None},
        1: {"color": (100, 100, 100),  # Gray for ship
            "pattern": "grid"},
        -1: {"color": (0, 70, 120),  # Darker blue for bombed water
             "pattern": "circle"},
        2: {"color": (180, 30, 30),  # Red for bombed ship
            "pattern": "cross"}
    }

    def __init__(self, width=600, height=600):
        """Initialize the grid battle window with given dimensions."""
        self.width = width
        self.height = height
        self.surface = None
        self.grid_origin_x = self.GRID_PADDING
        self.grid_origin_y = self.GRID_PADDING

        # Initialize the battle matrix (10x10 grid)
        self.battle_matrix = BattleshipMatrix()

        # Track selected cell (for user interaction)
        self.selected_cell = None

        # Initialize pygame and create surface
        self._init_pygame()

    def _init_pygame(self):
        """Initialize pygame and create the display surface."""
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battleship Grid")
        self.font = pygame.font.SysFont('Arial', 16)

    def draw(self):
        """Draw the grid and all cell states to the surface."""
        # Fill background
        self.surface.fill(self.BACKGROUND_COLOR)

        # Draw grid labels (A-J for columns, 1-10 for rows)
        self._draw_grid_labels()

        # Draw grid lines
        self._draw_grid_lines()

        # Draw cells based on their states
        self._draw_cells()

        # Draw selection highlight if a cell is selected
        if self.selected_cell:
            self._draw_selection()

        # Update the display
        pygame.display.flip()

    def _draw_grid_labels(self):
        """Draw row and column labels."""
        # Column labels (A through J)
        for col in range(self.GRID_SIZE):
            label = chr(65 + col)  # ASCII 'A' starts at 65
            text = self.font.render(label, True, self.GRID_LINE_COLOR)
            x = self.grid_origin_x + col * self.CELL_SIZE + self.CELL_SIZE // 2 - text.get_width() // 2
            y = self.grid_origin_y - 30
            self.surface.blit(text, (x, y))

        # Row labels (1 through 10)
        for row in range(self.GRID_SIZE):
            label = str(row + 1)
            text = self.font.render(label, True, self.GRID_LINE_COLOR)
            x = self.grid_origin_x - 30
            y = self.grid_origin_y + row * self.CELL_SIZE + self.CELL_SIZE // 2 - text.get_height() // 2
            self.surface.blit(text, (x, y))

    def _draw_grid_lines(self):
        """Draw the grid lines."""
        grid_width = self.GRID_SIZE * self.CELL_SIZE
        grid_height = self.GRID_SIZE * self.CELL_SIZE

        # Draw horizontal lines
        for i in range(self.GRID_SIZE + 1):
            y = self.grid_origin_y + i * self.CELL_SIZE
            pygame.draw.line(
                self.surface,
                self.GRID_LINE_COLOR,
                (self.grid_origin_x, y),
                (self.grid_origin_x + grid_width, y),
                2
            )

        # Draw vertical lines
        for i in range(self.GRID_SIZE + 1):
            x = self.grid_origin_x + i * self.CELL_SIZE
            pygame.draw.line(
                self.surface,
                self.GRID_LINE_COLOR,
                (x, self.grid_origin_y),
                (x, self.grid_origin_y + grid_height),
                2
            )

    def _draw_cells(self):
        """Draw each cell based on its state."""
        matrix = self.battle_matrix.get_matrix()
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                # Get cell state from the battle matrix
                # NOTE: Your matrix is indexed as [row][col]
                state = matrix[row][col]

                # Draw the cell with appropriate style
                self._draw_cell(row, col, state)

    def _draw_cell(self, row, col, state):
        """Draw a single cell with the style for its state."""
        # Calculate cell rect
        x = self.grid_origin_x + col * self.CELL_SIZE
        y = self.grid_origin_y + row * self.CELL_SIZE
        cell_rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)

        # Fill with base color for state
        style = self.STATE_STYLES.get(state, self.STATE_STYLES[0])  # Default to water if invalid state
        pygame.draw.rect(self.surface, style["color"], cell_rect)

        # Add pattern based on state
        pattern = style.get("pattern")
        if pattern == "grid":
            # Draw grid pattern (for ships)
            line_spacing = 8
            for i in range(1, self.CELL_SIZE // line_spacing):
                # Horizontal lines
                pygame.draw.line(
                    self.surface,
                    (50, 50, 50),  # Darker gray
                    (x, y + i * line_spacing),
                    (x + self.CELL_SIZE, y + i * line_spacing),
                    1
                )
                # Vertical lines
                pygame.draw.line(
                    self.surface,
                    (50, 50, 50),  # Darker gray
                    (x + i * line_spacing, y),
                    (x + i * line_spacing, y + self.CELL_SIZE),
                    1
                )
        elif pattern == "circle":
            # Draw circle pattern (for bombed water)
            circle_radius = self.CELL_SIZE // 4
            center_x = x + self.CELL_SIZE // 2
            center_y = y + self.CELL_SIZE // 2
            pygame.draw.circle(
                self.surface,
                (200, 200, 200),  # Light gray
                (center_x, center_y),
                circle_radius,
                3  # Width of the circle outline
            )
        elif pattern == "cross":
            # Draw X pattern (for bombed ship)
            padding = 8
            pygame.draw.line(
                self.surface,
                (0, 0, 0),  # Black
                (x + padding, y + padding),
                (x + self.CELL_SIZE - padding, y + self.CELL_SIZE - padding),
                3
            )
            pygame.draw.line(
                self.surface,
                (0, 0, 0),  # Black
                (x + self.CELL_SIZE - padding, y + padding),
                (x + padding, y + self.CELL_SIZE - padding),
                3
            )

    def _draw_selection(self):
        """Draw a highlight around the selected cell."""
        if not self.selected_cell:
            return

        row, col = self.selected_cell
        x = self.grid_origin_x + col * self.CELL_SIZE
        y = self.grid_origin_y + row * self.CELL_SIZE

        # Draw a highlighted border
        highlight_rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(self.surface, (255, 255, 0), highlight_rect, 3)  # Yellow highlight, 3px width

    def handle_event(self, event):
        """Handle user input events."""
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # Handle mouse clicks on the grid
            if event.button == 1:  # Left mouse button
                self._handle_click(event.pos)

    def _handle_click(self, pos):
        """Handle mouse click at the given position."""
        # Check if click is within grid bounds
        x, y = pos
        grid_x = x - self.grid_origin_x
        grid_y = y - self.grid_origin_y

        # Check if click is outside the grid
        if grid_x < 0 or grid_y < 0:
            self.selected_cell = None
            return

        # Convert to grid coordinates
        col = grid_x // self.CELL_SIZE
        row = grid_y // self.CELL_SIZE

        # Check if click is within valid grid range
        if row < self.GRID_SIZE and col < self.GRID_SIZE:
            self.selected_cell = (row, col)
            print(f"Selected cell: ({row}, {col})")
            # You can add code here to place a bomb when a cell is clicked
            # e.g., self.place_bomb(row, col)
        else:
            self.selected_cell = None

    def place_bomb(self, row, col):
        """Place a bomb at the given coordinates."""
        if 0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE:
            # Check if bomb has already been placed
            if not self.battle_matrix.has_bomb_been_placed(row, col):
                # Set bomb in matrix and get result (hit or miss)
                hit = self.battle_matrix.set_bomb_in_matrix(row, col)
                return hit
        return None

    def create_random_ships(self):
        """Create random ships on the grid."""
        self.battle_matrix.create_battleships()

    def run(self):
        """Run the main window loop."""
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                self.handle_event(event)

            # Draw everything
            self.draw()

            # Cap the frame rate
            clock.tick(60)


# Demo code to test the window independently
if __name__ == "__main__":
    window = GridBattleWindow()

    # Create random ships
    window.create_random_ships()

    # Add some bombs
    window.place_bomb(1, 1)  # Try to bomb at row 1, col 1
    window.place_bomb(2, 2)  # Try to bomb at row 2, col 2
    window.place_bomb(7, 7)  # Try to bomb at row 7, col 7

    # Print the matrix for debugging
    print("Matrix state:")
    window.battle_matrix.print_matrix()

    # Run the window
    window.run()