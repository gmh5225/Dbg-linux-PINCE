#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2016-2017 Korcan Karaokçu <korcankaraokcu@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import unittest, argparse, psutil
from libpince import GDB_Engine, SysUtils

desc = 'Runs all unit tests by creating or attaching to a process'
ex = 'Example of Usage:' \
     + '\n\tsudo python3 run_tests.py -a kmines' \
     + '\n\tsudo python3 run_tests.py -c /usr/games/kmines -o="-v"'

parser = argparse.ArgumentParser(description=desc, epilog=ex, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-a", metavar="process_name", type=str, help="Attaches to the process with given name")
parser.add_argument("-c", metavar="file_path", type=str, help="Creates a new process with given path")
parser.add_argument("-o", metavar="options", type=str, default="",
                    help="Arguments that'll be passed to the inferior, only can be used with -c, optional")
parser.add_argument("-l", metavar="ld_preload_path", type=str, default="",
                    help="Path of the preloaded .so file, only can be used with -c, optional")

args = parser.parse_args()
if args.a:
    process_list = SysUtils.search_in_processes_by_name(args.a)
    if not process_list:
        parser.error("There's no process with the name " + args.a)
    if len(process_list) > 1:
        for p in process_list:
            try:
                name = p.name()
            except psutil.NoSuchProcess:
                print("Process with pid", p.pid, "does not exist anymore")
                continue
            print(name)
        print("There are more than one process with the name " + args.a)
        exit()
    pid = process_list[0].pid
    if not GDB_Engine.can_attach(pid):
        parser.error("Failed to attach to the process with pid " + str(pid))
    GDB_Engine.attach(pid)
elif args.c:
    if not GDB_Engine.create_process(args.c, args.o, args.l):
        parser.error("Couldn't create the process with current args")
else:
    parser.error("Provide at least one of these arguments: -a or -c")
unittest.main(module="tests.GDB_Engine_tests", exit=False, argv=[""])
unittest.main(module="tests.SysUtils_tests", exit=False, argv=[""])
unittest.main(module="tests.GuiUtils_tests", exit=False, argv=[""])
GDB_Engine.detach()
