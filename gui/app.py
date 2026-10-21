#!/usr/bin/env python3
"""Tic-Tac-Toe GUI for the STM32 serial game server (docs/protocol.md v1.0).

    python gui/app.py                       # pick the port in the window
    python gui/app.py --port COM9           # preselect the port
    python gui/app.py --port socket://127.0.0.1:5555   # the PC mock server

The window draws ONLY what the device confirms. A click sends a command; nothing on the
board changes until a valid reply arrives. Serial I/O runs in a worker thread so the
window never freezes.
"""
import argparse
import os
import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client import Connection, GameView, ReplyError  # noqa: E402

try:
    from serial.tools import list_ports
except Exception:                                    # pragma: no cover
    list_ports = None

COLORS = {"X": "#c0392b", "O": "#1f6fb2", ".": "#222222"}


class App:
    def __init__(self, root, port=""):
        self.root = root
        root.title("Serial Game Server - Tic-Tac-Toe")
        root.minsize(520, 560)
        self.view = GameView()
        self.conn = None
        self.busy = False
        self.results = queue.Queue()

        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="Port:").pack(side="left")
        self.port_var = tk.StringVar(value=port)
        self.port_box = ttk.Combobox(top, textvariable=self.port_var, width=34, values=self.ports())
        self.port_box.pack(side="left", padx=6)
        self.connect_btn = ttk.Button(top, text="Connect", command=self.on_connect)
        self.connect_btn.pack(side="left")
        self.disconnect_btn = ttk.Button(top, text="Disconnect", command=self.on_disconnect)
        self.disconnect_btn.pack(side="left", padx=6)

        self.status = tk.StringVar()
        ttk.Label(root, textvariable=self.status, font=("Segoe UI", 14, "bold"),
                  wraplength=480, anchor="center", justify="center").pack(fill="x", padx=8, pady=(6, 2))
        self.result = tk.StringVar()
        self.result_label = tk.Label(root, textvariable=self.result, font=("Segoe UI", 20, "bold"), fg="#1e8449")
        self.result_label.pack()

        grid = ttk.Frame(root, padding=8)
        grid.pack()
        self.cells = []
        for i in range(9):
            b = tk.Button(grid, text="", width=4, height=1, font=("Helvetica", 40, "bold"),
                          command=lambda i=i: self.on_cell(i))
            b.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.cells.append(b)

        bar = ttk.Frame(root, padding=4)
        bar.pack()
        self.new_btn = ttk.Button(bar, text="New Game", command=lambda: self.send(["NEW"]))
        self.new_btn.pack(side="left", padx=4)
        self.resign_btn = ttk.Button(bar, text="Resign", command=lambda: self.send(["RESIGN"]))
        self.resign_btn.pack(side="left", padx=4)
        self.refresh_btn = ttk.Button(bar, text="Refresh (STATE)", command=lambda: self.send(["STATE"]))
        self.refresh_btn.pack(side="left", padx=4)

        ttk.Label(root, text="Messages on the wire (TX = sent, RX = checksum-verified reply):").pack(anchor="w", padx=8)
        self.log = tk.Text(root, height=8, state="disabled", font=("Consolas", 9))
        self.log.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.log.tag_config("tx", foreground="#555555")
        self.log.tag_config("rx", foreground="#1e8449")
        self.log.tag_config("err", foreground="#c0392b")

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.refresh()
        self.root.after(30, self.poll)

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def ports():
        found = [p.device for p in list_ports.comports()] if list_ports else []
        return found + ["socket://127.0.0.1:5555"]

    def write_log(self, kind, text):
        self.log.config(state="normal")
        label = {"tx": "TX  ", "rx": "RX  ", "err": "ERR "}[kind]
        self.log.insert("end", label + text + "\n", kind)
        self.log.see("end")
        self.log.config(state="disabled")

    def refresh(self):
        """Redraw from the GameView (which only changes on a valid server reply)."""
        v = self.view
        connected = self.conn is not None
        for i, b in enumerate(self.cells):
            ch = v.board[i]
            b.config(text="" if ch == "." else ch, fg=COLORS[ch], disabledforeground=COLORS[ch],
                     state="normal" if (connected and not self.busy and v.can_move(i)) else "disabled")
        self.status.set(v.message)
        self.result.set(v.result)
        idle_ok = connected and not self.busy
        self.connect_btn.config(state="normal" if (not connected and not self.busy) else "disabled")
        self.disconnect_btn.config(state="normal" if idle_ok else "disabled")
        self.new_btn.config(state="normal" if idle_ok and v.state in ("IDLE", "GAME_OVER") else "disabled")
        self.resign_btn.config(state="normal" if idle_ok and v.state == "IN_PROGRESS" else "disabled")
        self.refresh_btn.config(state="normal" if idle_ok else "disabled")
        self.port_box.config(state="normal" if not connected and not self.busy else "disabled")

    # ---------------------------------------------------------------- worker thread
    def run_in_thread(self, work):
        """work() runs off the UI thread and returns a list of (request, reply) or raises."""
        self.busy = True
        self.refresh()

        def target():
            try:
                self.results.put(("ok", work()))
            except ReplyError as exc:
                self.results.put(("err", str(exc)))
            except Exception as exc:                      # port missing, busy, unplugged ...
                self.results.put(("fatal", str(exc)))
        threading.Thread(target=target, daemon=True).start()

    def exchange(self, body):
        """One request; if the reply is lost, ask STATE once (protocol.md section 10)."""
        try:
            return [(body, self.conn.request(body))]
        except ReplyError as exc:
            if "no reply" not in str(exc):
                raise
            return [("STATE", self.conn.request("STATE"))]

    def poll(self):
        try:
            while True:
                kind, payload = self.results.get_nowait()
                self.finish(kind, payload)
        except queue.Empty:
            pass
        if self.conn is not None:
            while self.conn.log:
                self.write_log(*self.conn.log.pop(0))
        self.root.after(30, self.poll)

    def finish(self, kind, payload):
        self.busy = False
        if kind == "ok":
            for request, reply in payload:
                self.view.apply(request, reply)
        elif kind == "err":
            self.view.message = "Problem: " + payload                 # board is NOT touched
        else:
            self.view.message = "Port error: " + payload
            self.drop_connection()
        self.refresh()

    def drop_connection(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
        self.conn = None

    # ---------------------------------------------------------------- actions
    def on_connect(self):
        port = self.port_var.get().strip()
        if not port:
            self.view.message = "Choose a port first."
            self.refresh()
            return

        def work():
            self.conn = Connection(port)
            pairs = self.exchange("CONNECT")
            if pairs[0][1] == "NACK:STATE":                  # device is not idle: find out why
                d = self.conn.request("DISCONNECT")
                pairs.append(("DISCONNECT", d))
                if d == "OK":                                # it was a finished game: now idle
                    pairs.append(("CONNECT", self.conn.request("CONNECT")))
                else:                                        # a game is running: resync the board
                    pairs.append(("STATE", self.conn.request("STATE")))
            return pairs
        self.view.reset()
        self.run_in_thread(work)

    def send(self, bodies):
        if self.conn is None or self.busy:
            return
        self.run_in_thread(lambda: [p for b in bodies for p in self.exchange(b)])

    def on_cell(self, i):
        if self.view.can_move(i):                              # click only SENDS; no drawing here
            self.send([self.view.command_for_move(i)])

    def on_disconnect(self):
        def work():
            pairs = []
            if self.view.state == "IN_PROGRESS":
                pairs += self.exchange("RESIGN")
            pairs += self.exchange("DISCONNECT")
            return pairs
        self.run_in_thread(work)
        self.root.after(100, self.close_when_done)

    def close_when_done(self):
        if self.busy:
            self.root.after(100, self.close_when_done)
            return
        self.drop_connection()
        self.refresh()

    def on_close(self):
        if self.conn is not None and not self.busy:
            try:
                if self.view.state == "IN_PROGRESS":
                    self.conn.request("RESIGN")
                self.conn.request("DISCONNECT")
            except Exception:
                pass
        self.drop_connection()
        self.root.destroy()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", default=os.environ.get("GAME_PORT", ""))
    args = ap.parse_args()
    root = tk.Tk()
    App(root, args.port)
    root.mainloop()


if __name__ == "__main__":
    main()
