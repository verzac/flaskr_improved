drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null,
  username text foreign key references authentication(username)
);

drop table if exists authentication;
create table authentication (
  username text primary key,
  password text not null
);

insert into authentication
values ('root', 'root');