library(ggplot2)
library(dplyr)
library(lubridate)

traffic_data <- read.csv("./data/road/processed_road_data.csv")

traffic_data <- traffic_data %>%
  mutate(
    datetime_str = paste(date_time),
    timestamp = as.POSIXct(datetime_str, format = "%Y-%m-%d %H:%M:%S"),
    hour = hour(timestamp),
    day_of_week = wday(timestamp, label = TRUE, week_start = 1, abbr = FALSE)
  )
head(traffic_data)

heatmap_data <- traffic_data %>%
  group_by(day_of_week, hour) %>%
  summarize(
    avg_traffic = mean(traffic, na.rm = TRUE)
  ) %>%
  ungroup()

ggplot(heatmap_data, aes(x = hour, y = day_of_week, fill = avg_traffic)) +
  geom_tile(color = "white") +
  scale_fill_gradient2(low = "green", mid = "yellow", high = "red", midpoint = 2) +
  scale_x_continuous(breaks = seq(0, 23, by = 2)) +
  labs(
    title = "요일 및 시간대별 평균 교통량 (HeatMap)",
    x = "시간 (0~23시)",
    y = "요일",
    fill = "평균 교통량"
  ) +
  theme_minimal()

stacked_bar_data <- traffic_data %>%
  mutate(
    traffic_level = factor(traffic,
                           levels = c(1, 2, 3),
                           labels = c("원활(1)", "서행(2)", "정체(3)"))
  )

ggplot(stacked_bar_data, aes(x = hour, fill = traffic_level)) +
  geom_bar(position = "fill") +
  facet_wrap(~ day_of_week, ncol = 1) +
  scale_fill_manual(values = c("원활(1)" = "green", "서행(2)" = "orange", "정체(3)" = "red")) +
  scale_x_continuous(breaks = seq(0, 23, by = 2)) +
  scale_y_continuous(labels = scales::percent_format()) +
  labs(
    title = "요일별 시간대별 교통량 비율 변화",
    x = "시간 (0~23시)",
    y = "비율",
    fill = "교통량 수준"
  ) +
  theme_minimal()