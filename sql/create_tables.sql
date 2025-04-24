CREATE TABLE Player
(
    Username VARCHAR(50),
    Alias    VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Player_Username PRIMARY KEY (Username),
    CONSTRAINT UQ_Player_Alias UNIQUE (Username)
);

CREATE TABLE Score
(
    Username       VARCHAR(50),
    CompletionDate DATE        NOT NULL,
    TimeInSeconds  SMALLINT    NOT NULL,
    CONSTRAINT PK_Score_UsernameCompletionDate PRIMARY KEY (Username, CompletionDate),
    CONSTRAINT FK_Score_Username FOREIGN KEY (Username) REFERENCES Player(Username) ON UPDATE CASCADE
);