my bookshelf
============

Simple book reading manager. Use case: you have many ebooks on your computer, situated in diferent folders. You can list all reading books by command ``bs -l`` and open specified book in one touch by ``bs -r book_id``. 

Tested on *Arch Linux* + *XFCE 4.10* with *python 3* and *evince* as reader.

Install
-------

Clone to convenient directory and symlink to */usr/bin/bs*.

Set constants *FILE_SCHEMA* and *FILE_DB* to valid path.

Example of use
--------------

Adding new book:
    
    bs -a "Book 1" "/path/to/book1"

List all reading books

    bs

Set page *10* for book with ID *1*

    bs -p 1 123
    
Set book with ID *1* as readed

    bs -c 1

Delay book with ID *1* 

    bs -l 1

List all delaed books

    bs -l

