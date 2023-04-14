# xfl-2023-data-repository
[![Update XFL Stats](https://github.com/armstjc/xfl-2023-data-repository/actions/workflows/update_xfl_stats.yml/badge.svg)](https://github.com/armstjc/xfl-2023-data-repository/actions/workflows/update_xfl_stats.yml)
[![update_xfl_epa](https://github.com/armstjc/xfl-2023-data-repository/actions/workflows/update_xfl_pbp.yml/badge.svg)](https://github.com/armstjc/xfl-2023-data-repository/actions/workflows/update_xfl_pbp.yml)

Houses data related to the 2023 relaunch of the XFL Football League.

## Repostiory Structure

```
xfl-2023-data-repository

├── game_stats
|   └── player
|       ├── csv
|       |   ├── 2023_xfl_player_game_stats.csv
|       |   └── 2023_xfl_player_game_stats.csv
|       ├── parquet
|       |   ├── 2023_xfl_player_game_stats.parquet
|       |   └── 2023_xfl_player_game_stats.parquet
|       └── raw
|           ├── csv
|           ├── json
|           └── parquet
├── team
|   ├── csv
|   |   └── 2023_xfl_team_game_stats.csv
|   ├── parquet
|   └── raw
|       ├── csv
|       ├── json
|       └── parquet
├── pbp
|   ├── season
|   |   ├── csv
|   |   |   └── 2023_xfl_pbp.csv
|   |   └── parquet
|   |       └── 2023_xfl_pbp.parquet
|   └── single_game
|       ├── csv
|       ├── json
|       └── parquet
|
├── player_info
|   ├── participation_data
|   |   ├── csv
|   |   ├── json
|   |   └── parquet
|   └── photos
|
├── rosters
|   ├── weekly_rosters
|   |   ├── csv
|   |   ├── json
|   |   ├── parquet
|   |   ├── 2023_weekly_xfl_roster.csv
|   |   └── 2023_weekly_xfl_roster.parquet
|   ├── 2023_xfl_roster.csv
|   └── 2023_xfl_roster.parquet
|
├── schedule
|   ├── csv
|   ├── json
|   ├── parquet
|   ├── 2023_xfl_schedule.csv
|   └── 2023_xfl_schedule.parquet
|
├── standings
|   ├── weekly_standings
|   |   ├── csv
|   |   ├── json
|   |   └── parquet
|   ├── 2023_xfl_standings.csv
|   └── 2023_xfl_standings.parquet
├── teams
|   └── xfl_teams.csv
├── xfl_draft
|   ├── csv
|   |   └── 2023_xfl_draft.csv
|   ├── json
|   |   └── 2023_xfl_draft.json
|   └── parquet
|       └── 2023_xfl_draft.parquet
|
```
