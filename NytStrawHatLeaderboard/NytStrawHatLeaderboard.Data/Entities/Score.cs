using System;
using System.Collections.Generic;

namespace NytStrawHatLeaderboard.Data.Entities;

public partial class Score
{
    public string Username { get; set; } = null!;

    public DateOnly CompletionDate { get; set; }

    public short TimeInSeconds { get; set; }

    public virtual Player UsernameNavigation { get; set; } = null!;
}
