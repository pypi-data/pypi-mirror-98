# -*- coding: utf-8 -*-
#
# frontends/basefrontend.py
#
# This file is part of py2048.
#
# py2048 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# py2048 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with py2048.  If not, see <https://www.gnu.org/licenses/>.

from typing import Any, final, List, Optional
from abc import ABC
import sys
from pathlib import Path
import random

from py2048 import Base2048Error, Directions, type_check
from py2048.grid import Grid


class Base2048Frontend(ABC):
    """This abstract class implements the `play2048` method. A concrete
    frontend should inherit from this class, but shouldn't override this
    method.
    Many other methods are 'hooks' that either can, should, or must be
    overriden.
    """

    # 2^11 == 2048
    # sys.maxsize == (2^63) - 1 on 64bits machines
    valid_numbers: List[int] = [2 ** power for power in range(1, 12)]
    DIRECTIONS = tuple(Directions)
    SLEEP_S = 1  # how many seconds to sleep when in auto mode
    # converting seconds to mseconds
    SLEEP_MS = int(SLEEP_S * 1_000)

    @classmethod
    def is2048like(cls, n: int) -> bool:
        cache = cls.valid_numbers
        while cache[-1] < sys.maxsize and n > cache[-1]:
            cache.append(cache[-1] * 2)
        return n in cache

    def restart(self) -> None:
        self.victory = False
        self.grid.reset()
        self.grid.seed()

    def __init__(
        self,
        grid: Grid,
        is_random: bool,
        *,  # makes the remaining arguments keyword-only
        goal: Optional[int] = None,
    ) -> None:
        # first, perform some checks
        type_check(grid, Grid)
        # `goal = goal or 2048` would allow "goal = 0" to pass silently
        if goal is None:
            goal = 2048
        elif not self.is2048like(goal):
            raise ValueError(
                "goal must be a positive power of 2 "
                f"smaller than {sys.maxsize}"
            )
        # checks passed
        self.grid = grid
        self.goal = goal
        if is_random:
            self.choice_function = self.guess_direction
        else:
            self.choice_function = self.choose_direction
        self.is_random = is_random
        self.victory = False

    # play hooks: don't need to be overriden, but probably should
    def on_play(self) -> Any:
        pass

    def on_attempt(self) -> Any:
        pass

    def after_choice(self, choice: str) -> Any:
        pass

    def after_change(self, choice: str) -> Any:
        pass

    def after_nochange(self, choice: str) -> Any:
        pass

    def after_attempt(self, choice: str) -> Any:
        pass

    def after_play(self) -> Any:
        pass

    def guess_direction(self) -> Directions:
        return random.choice(self.DIRECTIONS)

    # MAIN LOOP: shouldn't be overriden
    @final
    def play2048(self) -> None:
        """The main loop repeatedly calls self.choice_function. If that raises
        `KeyboardInterrupt`, it returns immediately, without even calling
        `self.after_play()`. If that raises `EOFError`, it breaks the loop and
        calls `self.after_play()`.
        This loops until either a) the grid is jammed; or b) the player exited;
        or c) the goal has been reached for the first time.
        """

        player_quit = False
        grid = self.grid
        self.on_play()
        # can't play with an empty board
        if grid.is_empty:
            raise Base2048Error(
                f"Asked to play 2048 with an empty grid:\n{grid}"
            )
        # the actual loop
        jammed = grid.jammed
        if jammed:
            raise Base2048Error(
                f"Asked to play 2048 with a jammed grid:\n{grid}"
            )
        while not jammed:
            self.on_attempt()
            try:
                choice = self.choice_function()
            except KeyboardInterrupt:
                # quickly exit due to Ctrl-C
                print()  # makes terminal looks nicer
                return
            except EOFError:
                # Ctrl-D/Z or some quit-command
                player_quit = True
                break
            assert choice in self.DIRECTIONS
            self.after_choice(choice)
            dragged = grid.drag(choice)
            if dragged:
                self.after_change(choice)
                jammed = grid.jammed
            else:
                self.after_nochange(choice)
            self.after_attempt(choice)
            if not self.victory and grid.largest_number >= self.goal:
                self.victory = True
                break
        # after loop stuff
        self.after_play()
        if player_quit:
            self.on_player_quit()
        elif self.victory:
            if jammed:
                # the game has jammed, but the player had already won, so it's
                # an "overvictory"
                self.on_player_overvictory()
            else:
                # player's winning for the first time
                self.on_player_victory()
        else:
            assert jammed
            self.on_player_loss()

    # the following methods MUST be overriden
    def choose_direction(self) -> Directions:
        raise NotImplementedError(
            "'choose_direction' must be overriden by subclass"
        )

    def on_player_quit(self) -> Any:
        raise NotImplementedError(
            "'on_player_quit' must be overriden by subclass"
        )

    def on_player_victory(self) -> Any:
        raise NotImplementedError(
            "'on_player_victory' must be overriden by subclass"
        )

    def on_player_overvictory(self) -> Any:
        raise NotImplementedError(
            "'on_player_overvictory' must be overriden by subclass"
        )

    def on_player_loss(self) -> Any:
        raise NotImplementedError(
            "'on_player_loss' must be overriden by subclass"
        )
