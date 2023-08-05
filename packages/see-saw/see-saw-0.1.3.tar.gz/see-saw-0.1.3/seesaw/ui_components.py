import urwid

HELPTEXT = """
Welcome to See-Saw!

Navigation:
- Arrow keys to move left/right between sections
- Up/Down arrow and Page Up/Page Down to scroll around the logs
- Space bar to select/de-select regions and log groups

Other keybinds:
r - refresh the logs displayed based on the current log groups selected
v - turn on verbose timestamps (full date/time)
h - show this help menu
q - quit the program
""".strip()


class HelpPopUp(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """

    signals = ["close"]

    def __init__(self):
        close_button = urwid.Button("that's pretty cool")
        urwid.connect_signal(close_button, "click", lambda button: self._emit("close"))
        pile = urwid.Pile(
            [
                urwid.Text(
                    "^^  I'm attached to the widget that opened me. "
                    "Try resizing the window!\n"
                ),
                close_button,
            ]
        )
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, "popbg"))
