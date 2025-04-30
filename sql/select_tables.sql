/*
    Below are some useful SELECT statements to check the score data in the database.
*/

-- Get all the scores
SELECT
    RANK() OVER (PARTITION BY CompletionDate ORDER BY TimeInSeconds ASC) AS Rank,
    Username,
    CompletionDate AS [Completion Date],
    TimeInSeconds AS [Time in Seconds]
FROM
    Score
ORDER BY CompletionDate DESC, TimeInSeconds ASC

-- Get the score count for each day
SELECT
    CompletionDate AS [Completion Date],
    COUNT(CompletionDate) AS [Score Count]
FROM
    Score
GROUP BY CompletionDate
ORDER BY CompletionDate DESC