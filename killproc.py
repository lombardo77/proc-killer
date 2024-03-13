#!/usr/bin/env python3

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListItem, ListView, Input
import psutil
import os 


class ProcBrowser(ListView):
    pids_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.populate()

    def populate(self):
        for i in psutil.pids():
            s = "/".join(psutil.Process(i).cmdline())
            self.append(ListItem(
                Label(str(i), id="pid"),
                Label(psutil.Process(i).status(), id="status"),
                Label(s),
                id="p" + str(i),
            ))
            self.pids_list.append((str(i), str(i) + " " + s))

    def on_list_view_selected(self, event: ListView.Selected):
        pid = int(event.item.id[1:])
        p = psutil.Process(pid)
        p.kill()


class Myapp(App):

    CSS = """
        ListItem {
            layout: horizontal;
            margin: 1;
        }
        Label {
            padding: 0 1;
        }
        Screen {
            align: center middle;
        }
        Input {
            align: center middle;
        }

    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="submit", id="submit")
        yield ProcBrowser(id="list")
        yield Footer()

    def on_input_changed(self, event: Input.Submitted):
        # TODO: figure out search
        list_items = self.query_one("#list", ProcBrowser)
        list_items.clear()
        for pid, cmd in ProcBrowser.pids_list:
            s = "/".join(psutil.Process(int(pid)).cmdline())
            if event.value in cmd:
                # pass
                list_items.append(ListItem(
                    Label(str(pid), id="pid"),
                    Label(psutil.Process(int(pid)).status(), id="status"),
                    Label(s),
                    id="p" + str(pid),
                ))


if __name__ == "__main__":
    app = Myapp()
    app.run()


if __name__ == "__main__":
    Myapp().run()
 
