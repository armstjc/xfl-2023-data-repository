## Ensure that nflfastR exists in this context.
#install.packages("nflfastR")

## Load nflfastR in this context
library(nflfastR)

## Apply EP caclulations
pbp_data <- read.csv("pbp/season/csv/2023_xfl_pbp.csv")
df <- calculate_expected_points(pbp_data)

## Save off the data.
write.csv(df, "pbp/season/csv/2023_xfl_pbp_EP.csv", row.names = FALSE)
