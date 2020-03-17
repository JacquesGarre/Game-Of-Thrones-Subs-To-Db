CREATE DATABASE IF NOT EXISTS got;
CREATE TABLE IF NOT EXISTS got.season ( 
	id      int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	number  varchar(2) NOT NULL    
);
CREATE TABLE IF NOT EXISTS got.episode ( 
	id          int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	number      varchar(2) NOT NULL,
	title       varchar(255) NOT NULL,
	season_id   int NOT NULL,
	CONSTRAINT fk_episode_season FOREIGN KEY (season_id) REFERENCES season(id)
);
CREATE TABLE IF NOT EXISTS got.subtitle ( 
	id          int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	number      varchar(4) NOT NULL,
	content     varchar(255) NOT NULL,
	episode_id  int NOT NULL,
	CONSTRAINT fk_subtitle_episode FOREIGN KEY (episode_id) REFERENCES episode(id)
);