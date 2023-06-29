# A Sudoku Game!

This is a normal game of sudoku on a default 9x9 grid with a sudoku autosolver. You can create your own grids by going into the `` ./puzzle/grid.txt `` and adding your own data or let the script generate one for you.

## Usage
To start the application just run ``python app.py``.

## Controls
- Use the arrow keys or the mouse to navigate
- Hit a number between between ``[1..9]`` to fill the slot with that number.
- Press the ``backspace`` key to remove the number on the selected slot
- Press ``return`` to run the autosolver in fast mode or press the ``s`` key to run it in slow mode. You can modify the config in the ``app.py`` directory under the config section.
- Hit ``r`` to reset the board.
- Press ``t`` to save the current board. You may find the saved board under ``./puzzle/field.txt``.
- Press ``g``to auto genrate a new field.