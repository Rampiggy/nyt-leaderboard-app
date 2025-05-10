using System;
using System.Collections.Generic;

namespace NytStrawHatLeaderboard.Data.Entities;

public partial class Player
{
    public string Username { get; set; } = null!;

    public string Alias { get; set; } = null!;

    public virtual ICollection<Score> Scores { get; set; } = new List<Score>();
}
