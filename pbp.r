## Ensure that nflfastR exists in this context.
#install.packages("nflfastR")

## Load required libraries
library(nflfastR)
library(dplyr)

## Apply EP caclulations
pbp_data <- read.csv("pbp/season/csv/2023_xfl_pbp.csv")
df <- calculate_expected_points(pbp_data)
#df <- calculate_win_probability(df)


#df <- transform(df, epa = c(ep[-1], NA))
df <-
    df %>%
    group_by(game_id) %>%
    dplyr::mutate(ep_f = lead(ep, n = 1, default = NA))
df["epa"] <- df["ep_f"] - df["ep"]

## Save off the data.
write.csv(df, "pbp/season/csv/2023_xfl_pbp_EP.csv",
    na = "",
    row.names = FALSE
)
