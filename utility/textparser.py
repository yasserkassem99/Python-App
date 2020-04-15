import arabic_reshaper
from bidi.algorithm import get_display
import tkinter as tk


def arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text


class ArabicText(tk.StringVar):
    def __init__(self, master=None, value=None, name=None):
        tk.StringVar.__init__(self, master=master, value=value, name=name)

    def get(self):
        """Return value of variable as string."""
        value = self._tk.globalgetvar(self._name)
        if isinstance(value, str):
            return arabic(value)
        return arabic(str(value))

    def set(self, value):
        """Set the variable to VALUE."""
        print('hi')
        return self._tk.globalsetvar(self._name, arabic(value))


class TextInput(tk.Entry):

    def delete(self, first, last=None):
        print('delete')
        """Delete text from FIRST to LAST (not included)."""
        self.tk.call(self._w, 'delete', first, last)

    def get(self):
        print('g')
        """Return the text."""
        return self.tk.call(self._w, 'get')

    def icursor(self, index):
        print('ic')
        """Insert cursor at INDEX."""
        self.tk.call(self._w, 'icursor', index)

    def index(self, index):
        print('ind')
        """Return position of cursor."""
        return self.tk.getint(self.tk.call(
            self._w, 'index', index))

    def insert(self, index, string):
        print('insert')
        """Insert STRING at INDEX."""
        self.tk.call(self._w, 'insert', index, string)

    def scan_mark(self, x):
        print('sc')
        """Remember the current X, Y coordinates."""
        self.tk.call(self._w, 'scan', 'mark', x)

    def scan_dragto(self, x):
        print('dr')
        """Adjust the view of the canvas to 10 times the
        difference between X and Y and the coordinates given in
        scan_mark."""
        self.tk.call(self._w, 'scan', 'dragto', x)

    def selection_adjust(self, index):
        print('ad')
        """Adjust the end of the selection near the cursor to INDEX."""
        self.tk.call(self._w, 'selection', 'adjust', index)

    select_adjust = selection_adjust

    def selection_clear(self):
        print('cl')
        """Clear the selection if it is in this widget."""
        self.tk.call(self._w, 'selection', 'clear')

    select_clear = selection_clear

    def selection_from(self, index):
        print('fr')
        """Set the fixed end of a selection to INDEX."""
        self.tk.call(self._w, 'selection', 'from', index)

    select_from = selection_from

    def selection_present(self):
        print('pr')
        """Return True if there are characters selected in the entry, False
        otherwise."""
        return self.tk.getboolean(
            self.tk.call(self._w, 'selection', 'present'))

    select_present = selection_present

    def selection_range(self, start, end):
        print('ra')
        """Set the selection from START to END (not included)."""
        self.tk.call(self._w, 'selection', 'range', start, end)

    select_range = selection_range

    def selection_to(self, index):
        print('to')
        """Set the variable end of a selection to INDEX."""
        self.tk.call(self._w, 'selection', 'to', index)

    select_to = selection_to
