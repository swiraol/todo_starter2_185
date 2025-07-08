CREATE TABLE lists (
  id serial PRIMARY KEY,
  title text NOT NULL 
);

ALTER TABLE lists ADD CONSTRAINT unique_title UNIQUE (title);

CREATE TABLE todos (
  id serial PRIMARY KEY,
  title text NOT NULL,
  completed boolean NOT NULL DEFAULT false,
  list_id int NOT NULL 
);

ALTER TABLE todos ADD FOREIGN KEY (list_id)
                  REFERENCES lists (id) 
                  ON DELETE CASCADE;