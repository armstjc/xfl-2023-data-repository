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
|       ├── parquet
|       └── raw
|           ├── csv
|           ├── json
|           └── parquet
├── team
|   ├── csv
|   ├── parquet
|   └── raw
|       ├── csv
|       ├── json
|       └── parquet
├── pbp
|   ├── season
|   |   ├── csv
|   |   └── parquet
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
|   └── weekly_standings
|       ├── csv
|       ├── json
|       └── parquet
|
├── teams
|   └── xfl_teams.csv
|
├── xfl_draft
    ├── csv
    ├── json
    └── parquet

```
