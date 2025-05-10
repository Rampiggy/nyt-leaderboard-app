using NytStrawHatLeaderboard.Data.Entities;

namespace NytStrawHatLeaderboard.Data;

public class NytRepository
{
    private readonly NytContext _nytContext;
    private readonly Dictionary<string, string> _usernameToAlias;

    public NytRepository(NytContext nytContext)
    {
        _nytContext = nytContext;
        _usernameToAlias = nytContext.Players.ToDictionary(p => p.Username, p => p.Alias);
    }

    public List<Score> GetAllScores()
    {
        var scores = _nytContext.Scores.ToList();
        ReplaceUsernamesWithAliases(scores);
        return scores;
    }

    public List<Score> GetScoresByDay(DateOnly date)
    {
        var scores = _nytContext.Scores
            .Where(score => score.CompletionDate == date)
            .ToList();
        ReplaceUsernamesWithAliases(scores);
        return scores;
    }

    public List<Score> GetScoresByMonth(DateOnly date)
    {
        var scores = _nytContext.Scores
            .Where(score => score.CompletionDate.Year == date.Year && score.CompletionDate.Month == date.Month)
            .ToList();
        ReplaceUsernamesWithAliases(scores);
        return scores;
    }
    
    public List<Score> GetScoresByYear(DateOnly date)
    {
        var scores = _nytContext.Scores
            .Where(score => score.CompletionDate.Year == date.Year)
            .ToList();
        ReplaceUsernamesWithAliases(scores);
        return scores;
    }

    private void ReplaceUsernamesWithAliases(List<Score> scores)
    {
        foreach (var score in scores)
            score.Username = _usernameToAlias[score.Username];
    }
}