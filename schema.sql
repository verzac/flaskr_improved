drop table if exists authentication;
create table authentication (
  username text primary key,
  password text not null
);

drop table if exists blog_entries;
create table blog_entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null,
  username text not null,
  foreign key(username) references authentication(username)
);

drop table if exists keytags;
create table keytags (
  keytag text primary key,
  when_generated date not null,
  who_used_it_last text,
  foreign key(who_used_it_last) references authentication(username)
);

drop table if exists page_entries;

insert into authentication
values ('root', 'root');