/* Tables for Basic Data Types: users, stories, words, etc. */

create table user(
  userid int unsigned not null primary key,
  username char(50) not null
);

create table story(
  storyid int unsigned not null primary key,
  title char(100) not null
);

create table word(
  wordid int unsigned not null auto_increment primary key,
  string char(100) not null,
  stem char(100),
  lemma char(100)
);

create table profile(
  userid int unsigned not null,
  content text,
  stamp timestamp(12),

  foreign key(userid) references user(userid)
);

create table review(
  userid int unsigned not null,
  reviewid int unsigned not null auto_increment,
  polarity float,
  subjectivity float,
  stamp timestamp(12),
  content text,

  foreign key(userid) references user(userid),
  primary key(userid, reviewid)
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
