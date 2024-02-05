create table if not EXISTS categories1st(
	cat1_id INTEGER PRIMARY KEY AUTOINCREMENT,
	cat1_name TEXT NOT NULL
);

create table if not EXISTS categories2nd(
	cat2_id INTEGER PRIMARY KEY AUTOINCREMENT,
	cat2_name TEXT NOT NULL,
	cat1_id INTEGER,
	FOREIGN KEY(cat1_id) REFERENCES categories1st(cat1_id)
);

create table if not EXISTS categories3rd(
	cat3_id INTEGER PRIMARY KEY AUTOINCREMENT,
	cat3_name TEXT NOT NULL,
	cat2_id INTEGER,
	FOREIGN KEY(cat2_id) REFERENCES categories2nd(cat2_id)
);

create table if not EXISTS tags(
	tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
	tag_name TEXT NOT NULL
);

create table if not EXISTS books(
	book_id INTEGER PRIMARY KEY AUTOINCREMENT,
	url TEXT,
	name TEXT,
	author TEXT,
	rating INTEGER DEFAULT 0,
	status TEXT DEFAULT '未完结',
	read_status TEXT DEFAULT '未读', --"未读","已读","在读","想读"
	updated_chapter TEXT,
	last_update_date TEXT DEFAULT CURRENT_DATE,
	website TEXT,
	comment TEXT,
	UNIQUE(url,name)
);

create table if not EXISTS book_tag(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	book_id INTEGER,
	tag_id INTEGER,
	FOREIGN KEY(book_id) REFERENCES books(book_id),
	FOREIGN KEY(tag_id) REFERENCES tags(tag_id),
	UNIQUE(book_id,tag_id)
);

create TRIGGER trigger_delTagAfterDelBooks AFTER DELETE
on books for each ROW
BEGIN
	delete from book_tag where book_id=old.book_id;
END;
