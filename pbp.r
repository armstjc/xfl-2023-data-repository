#install.packages("nflfastR")
library(nflfastR)

pbp_data <- read.csv("pbp/season/csv/2023_xfl_pbp.csv")
df <- calculate_expected_points(pbp_data)


write.csv(df, "pbp/season/csv/2023_xfl_pbp.csv", row.names = FALSE)