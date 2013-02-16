#!/usr/bin/env python

"""
my bookshelf

Simple book reading manager. Use case: you have many ebooks on your computer, situated in diferent folders.
You can list all reading books by command ``bs -l`` and open specified book in one touch by ``bs -r book_id``.

by proft // http://proft.me
"""

import os
import sqlite3
import argparse
from datetime import datetime
from subprocess import call
from termcolor import cprint

FILE_DB = '/home/proft/Dropbox/scripts/bookshelf/bs.db'
FILE_SCHEMA = '/home/proft/Dropbox/scripts/bookshelf/bs_schema.sql'

db_is_new = not os.path.exists(FILE_DB)


def print_table(cursor):
    format_string = "%5s %50s %6s %25s"
    print(format_string % ('ID', 'TITLE', 'PAGE', 'START DATE'))
    for index, row in enumerate(cursor.fetchall()):
        cprint(format_string % (row[0], row[1], row[2], row[3]), 'yellow' if index % 2 == 0 else 'cyan')


if db_is_new:
    with sqlite3.connect(FILE_DB) as conn:
        print('Creating schema ...')
        with open(FILE_SCHEMA, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

parser = argparse.ArgumentParser(description='My bookshelf')
parser.add_argument('-a', action="store", type=str, nargs=2, help="add new book")
parser.add_argument('-p', action="store", type=str, nargs=2, help="set page for book ID with PAGE")
parser.add_argument('-r', action="store", type=int, help="read book with ID")
parser.add_argument('-l', action="store", type=int, nargs='*', help="list delayed books or delay book with ID")
parser.add_argument('-c', action="store", type=int, help="complete book with ID")
parser.add_argument('-i', action="store", type=int, help="show info for book with ID")

args = parser.parse_args()

with sqlite3.connect(FILE_DB) as conn:
    cursor = conn.cursor()

    ######
    # add
    ######

    if args.a is not None:
        title, path = args.a
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('insert into books(title, fpath, cdate, readed, later) values(?, ?, ?, 0, 0)', (title, path, now))
        bid = cursor.lastrowid

    ######
    # read
    ######

    elif args.r is not None:
        bid = int(args.r)

        cursor.execute('select fpath, cpage from books where id=?', (bid,))
        book = cursor.fetchone()
        fpath, page = book[0], book[1]
        cmd = "evince '%s' -i %s 2>/dev/null &" % (fpath, page)

        call(cmd, shell=True)

    ###############
    # complete read
    ###############

    elif args.c is not None:
        bid = int(args.c)
        cursor.execute('update books set readed=1 where id = ?', (bid,))
        conn.commit()

    ###############
    # set current page
    ###############

    elif args.p is not None:
        bid, page = args.p
        cursor.execute('update books set cpage=? where id = ?', (page, bid))
        conn.commit()

    ##########
    # show info
    ##########

    elif args.i is not None:
        bid = args.i
        cursor.execute('select id, title, fpath, readed, later from books where id=?', (bid,))
        book = cursor.fetchone()

        print("ID: %s\nTitle: %s\nFile path: %s\nReaded: %s\nLater: %s" % (book[0], book[1], book[2], book[3], book[4]))

    ##########
    # show/switch later
    ##########

    elif args.l is not None:
        if args.l:
            bid = args.l[0]
            cursor.execute('select later from books where id=?', (bid,))
            later = int(not bool(cursor.fetchone()[0]))

            cursor.execute('update books set later = ? where id = ?', (later, bid))
            conn.commit()
        else:
            cursor.execute('select id, title, cpage, cdate from books where later = 1')
            print_table(cursor)

    ##########
    # default: show all
    ##########

    else:
        cursor.execute('select id, title, cpage, cdate from books where readed = 0 and later = 0')
        print_table(cursor)
