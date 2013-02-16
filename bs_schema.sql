create table books (
    id		integer primary key autoincrement not null,
    title	text,
    fpath   text,
    cpage   integer default 0,
    readed  boolean default 0,
    later   boolean default 0,
    cdate	datetime
);
