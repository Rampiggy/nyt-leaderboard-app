using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace NytStrawHatLeaderboard.Data.Entities;

public partial class NytContext : DbContext
{
    public NytContext(DbContextOptions<NytContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Player> Players { get; set; }

    public virtual DbSet<Score> Scores { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Player>(entity =>
        {
            entity.HasKey(e => e.Username).HasName("PK_Player_Username");

            entity.ToTable("Player");

            entity.HasIndex(e => e.Username, "UQ_Player_Alias").IsUnique();

            entity.Property(e => e.Username)
                .HasMaxLength(50)
                .IsUnicode(false);
            entity.Property(e => e.Alias)
                .HasMaxLength(50)
                .IsUnicode(false);
        });

        modelBuilder.Entity<Score>(entity =>
        {
            entity.HasKey(e => new { e.Username, e.CompletionDate }).HasName("PK_Score_UsernameCompletionDate");

            entity.ToTable("Score");

            entity.Property(e => e.Username)
                .HasMaxLength(50)
                .IsUnicode(false);

            entity.HasOne(d => d.UsernameNavigation).WithMany(p => p.Scores)
                .HasForeignKey(d => d.Username)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_Score_Username");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
