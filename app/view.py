from typing import List, Optional

class TerminalView:
    def __init__(self, window, debug: bool):
        self.window = window
        self.debug: bool = debug

    def render_screen(self, steps_count: int, env_state: Optional[List[List[Optional[int]]]], action: Optional[int], finished: bool):
        self.window.clear()

        self.__render_metrics(steps_count)

        if self.debug:
            self.window.addstr("\n")
            self.__render_action(action)

        self.window.addstr("\n")
        self.__render_controls()


        self.window.addstr("\n")
        self.window.addstr("\n")
        self.__render_game_state(env_state)

        if finished:
            self.window.addstr("\n")
            self.window.addstr("\n")
            self.__render_finished(steps_count)

        self.window.refresh()

    def __render_metrics(self, steps_count: int):
        self.window.addstr(f"Steps: {steps_count}\n")

    def __render_action(self, action: int):
        self.window.addstr(f"Action: {action}\n")

    def __render_controls(self):
        self.window.addstr("Controls:\n")
        self.window.addstr("  Restart: R\n")
        self.window.addstr("  Quit: Q or Esc\n")
        self.window.addstr("  Move Up: Key Up or W\n")
        self.window.addstr("  Move Right: Key Right or D\n")
        self.window.addstr("  Move Down: Key Down or S\n")
        self.window.addstr("  Move Left: Key Left or A\n")

    def __render_game_state(self, env_state: Optional[List[List[Optional[int]]]]):
        str_state = "\n".join([
            "\t".join(
                map(
                    lambda x: str(x) if x is not None else "", 
                    row
                )
            ) 
            for row in env_state
        ])
        self.window.addstr(str_state)

    def __render_finished(self, steps_count: int):
        self.window.addstr(f"Game successfully finished in {steps_count} steps!\n")
        self.window.addstr(f"You can now restart (R) the game or quit (Q or Esc).")
