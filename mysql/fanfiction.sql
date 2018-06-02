/* Tables for Basic Data Types: users, stories, words, etc. */

create table user(
  userid int unsigned not null primary key,
  username char(50) not null
);

create table story(
  storyid int unsigned not null primary key,
  title char(100) not null
);

/* Tables for relations derived from the basic types */
create table author(

  userid int unsigned not null,
  storyid int unsigned not null,

  foreign key(userid) references user(userid),
  foreign key(storyid) references story(storyid)
);

create table likes(

  userid int unsigned not null,
  storyid int unsigned not null,

  foreign key(userid) references user(userid),
  foreign key(storyid) references story(storyid)
);
