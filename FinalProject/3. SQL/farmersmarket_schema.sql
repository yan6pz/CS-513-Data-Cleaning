/* Represent a Dimention tables*/ 
CREATE TABLE counties 
  ( 
     countyid INT PRIMARY KEY NOT NULL, 
     NAME      CHAR(50)  
  ); 

CREATE TABLE cities 
  ( 
     cityid INT PRIMARY KEY NOT NULL, 
     NAME   CHAR(50)  
  ); 

CREATE TABLE states 
  ( 
     stateid INT PRIMARY KEY NOT NULL, 
     NAME    CHAR(50)  
  ); 

/* Represents a Fact table.*/ 
CREATE TABLE markets 
  ( 
     fmid       INT PRIMARY KEY NOT NULL, 
     marketname TEXT NOT NULL, 
     street     TEXT, 
     state      INT, 
     city       INT, 
     county    INT, 
     zip        CHAR(20), 
     latitude   REAL NOT NULL, 
     longitude  REAL NOT NULL, 
     credit     CHAR(1), 
     wic        CHAR(1), 
     wiccash    CHAR(1), 
     organic    CHAR(1), 
     cheese     CHAR(1), 
     eggs       CHAR(1), 
     seafood    CHAR(1), 
     herbs      CHAR(1), 
     vegetables CHAR(1), 
     honey      CHAR(1), 
     jams       CHAR(1), 
     meat       CHAR(1), 
     nuts       CHAR(1), 
     plants     CHAR(1), 
     soap       CHAR(1), 
     wine       CHAR(1), 
     trees      CHAR(1), 
     coffee     CHAR(1), 
     beans      CHAR(1), 
     fruits     CHAR(1), 
     mushrooms  CHAR(1), 
     tofu       CHAR(1), 
     updatetime DATETIME NOT NULL, 
     FOREIGN KEY(state) REFERENCES states(stateid), 
     FOREIGN KEY(city) REFERENCES cities(cityid) ,
     FOREIGN KEY(county) REFERENCES counties(countyid) 
  ); 
  
/* Fixing data redundancy. This table has a record only if there is a record in the excel sheet having non-blank value for this column. 
Id represents FMID from the Markets table and it is both primary key and points as foreign key to markets table*/
CREATE TABLE website 
  ( 
     id  INT PRIMARY KEY NOT NULL, 
     url TEXT , 
     FOREIGN KEY(id) REFERENCES markets(fmid) 
  ); 

CREATE TABLE facebook 
  ( 
     id  INT PRIMARY KEY NOT NULL, 
     url TEXT , 
     FOREIGN KEY(id) REFERENCES markets(fmid) 
  ); 

CREATE TABLE twitter 
  ( 
     id  INT PRIMARY KEY NOT NULL, 
     url TEXT , 
     FOREIGN KEY(id) REFERENCES markets(fmid) 
  ); 

CREATE TABLE youtube 
  ( 
     id  INT PRIMARY KEY NOT NULL, 
     url TEXT , 
     FOREIGN KEY(id) REFERENCES markets(fmid) 
  ); 

CREATE TABLE othermedia 
  ( 
     id  INT PRIMARY KEY NOT NULL, 
     url TEXT , 
     FOREIGN KEY(id) REFERENCES markets(fmid) 
  ); 

/* Contains all the dates per market in the form of intervals(foreign key to markets table). Each record has season number which shows the season the dates are at.*/
CREATE TABLE seasondates 
  ( 
     id           INT PRIMARY KEY NOT NULL, 
     datefrom     DATE , 
     dateto       DATE , 
     seasonnumber SMALLINT NOT NULL, 
     marketid     INT NOT NULL, 
     FOREIGN KEY(marketid) REFERENCES markets(fmid) 
  ); 

/*Contains all the times per date in the form of intervals(foreign key to season dates table). 
 Dayoftheweek column will preserve the information for the day of the week the time is at. */ 
CREATE TABLE seasontimes 
  ( 
     id           INT PRIMARY KEY NOT NULL, 
     timefrom     DATETIME NOT NULL, 
     timeto       DATETIME NOT NULL, 
     dayoftheweek INT NOT NULL, 
     FOREIGN KEY(id) REFERENCES seasondates(id) 
  ); 

