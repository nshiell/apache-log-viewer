#! /usr/bin/python3
"""
    Blue Log Viewer - Log files in a GUI
    This program is not related to Apache or the Apache Software Foundation in any way
    Copyright (C) 2019  Nicholas Shiell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import sys
from PyQt5.QtWidgets import QApplication
from argparse import ArgumentParser
from blueLogViewer.windows import QMainWindowBlueLogViewer, get_valid_path
from blueLogViewer import Events
from blueLogViewer import LineCollection, LineCollectionBroker

import signal

if __name__ == '__main__':
    # Kill the app on ctrl-c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    parser = ArgumentParser(
        description='Show an autoupdating grid from Apache\'s Error Log'
    )

    parser.add_argument(
        'file',
        help=
        'The Path of the log file to tail',
        nargs='?'
    )

    app = QApplication(sys.argv)
    args = parser.parse_args()

    # We need a main window before we show anything
    # even if we are not ready to show it yet!
    main_window = QMainWindowBlueLogViewer()
    Events(main_window)
    path = get_valid_path(main_window, args.file)

    broker = LineCollectionBroker(path, main_window)
    broker.read_file_current_lines()
    broker.start_tailling()

    main_window.setup(broker.table_model)
    main_window.show()

    app.exec_()