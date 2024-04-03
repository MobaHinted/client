// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models.Data.Matches;

using CamilleMatch = Camille.RiotGames.MatchV5.Match;

public class PlayerData { }

public class TeamData { }

public class MatchData
{
    private readonly CamilleMatch _match;

    public MatchData(CamilleMatch match)
    {
        this._match = match;

        Program.log(
                source: nameof(MatchData),
                method: "MatchData()",
                doing: "Parsing Match Data",
                message: "Loaded match data"
                + match.Metadata.MatchId
                + " in "
                + match.Info.GameVersion,
                debugSymbols:
                [
                    match.Metadata.MatchId,
                ],
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose
            );
    }

    public string MatchId
    {
        get => this._match.Metadata.MatchId;
    }

    #region Version

    private float? _gameVersion;

    public float GameVersion
    {
        get
        {
            if (this._gameVersion is not null)
            {
                return (float)this._gameVersion;
            }

            string gameVersion = this._match.Info.GameVersion;
            string[] parts = gameVersion.Split('.');
            float version = float.Parse(parts[0] + "." + parts[1]);

            this._gameVersion = version;
            return version;
        }
    }

    private string FullGameVersion
    {
        get => this._match.Info.GameVersion;
    }

    #endregion

    #region Time

    public int Duration
    {
        // ReSharper disable once PossibleLossOfFraction
        get => (int)Math.Round((double)(this._match.Info.GameDuration / 60));
    }

    private DateTime GameStart
    {
        get =>
            DateTimeOffset
                .FromUnixTimeMilliseconds(this._match.Info.GameStartTimestamp)
                .DateTime;
    }

    private DateTime? _gameEnd;

    private DateTime GameEnd
    {
        get
        {
            if (this._gameEnd is not null)
            {
                return (DateTime)this._gameEnd;
            }

            // Handle games without an end timestamp
            if (this._match.Info.GameEndTimestamp is null)
            {
                DateTime endTime = this.GameStart.AddMinutes(this.Duration);
                this._gameEnd = endTime;
                return endTime;
            }

            // Return the precise end time
            DateTime preciseEndTime = DateTimeOffset
                .FromUnixTimeMilliseconds((long)this._match.Info.GameEndTimestamp!)
                .DateTime;
            this._gameEnd = preciseEndTime;
            return preciseEndTime;
        }
    }

    #endregion
}
