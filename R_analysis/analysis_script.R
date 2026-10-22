# read all csv files from data
folder = "/home/simon/code/school/efficientalgorithms_step1/data"
files = list.files(
  path = folder,
  pattern = "*.csv",
  ignore.case = T,
  full.names = T
)

data = lapply(files, read.csv)
names(data) <- sub(pattern = "(.*)\\..*$",replacement = "\\1",basename(files))

data[["BU:arithmetic"]]=head(data[["BU:arithmetic"]],51)
data[["BU:palindrome"]]=head(data[["BU:palindrome"]],50)
naive_cases = data[grep("Naive",names(data))]

data = Filter(function(df){
  (is.data.frame(df) && nrow(df) >= 50)
},data)

bad_cases = data[grep("higher_resolution_timer",names(naive_cases))]
naive_cases = naive_cases[!(names(naive_cases) %in% names(bad_cases))]
data = c(data,naive_cases)


library(ggplot2)
library(purrr)
plot_all_trends <- function(plot) {
  return(  
    plot +
    geom_point() +
    stat_smooth(method = 'lm', aes(colour = 'linear'), se = FALSE) +
    stat_smooth(method = 'lm', formula = y ~ poly(x,2), aes(colour = 'polynomial'), se= FALSE) +
    stat_smooth(method = 'nls', formula = y ~ a * log(x) + b, aes(colour = 'logarithmic'), se = FALSE, method.args = list(start = list(a = 1, b = 1))) +
    stat_smooth(method = 'nls', formula = y ~ a * exp(b * x), aes(colour = 'Exponential'), se = FALSE, method.args = list(start = list(a = 1, b = 1))) +
    theme_bw() +
    scale_colour_brewer(name = 'Trendline', palette = 'Set2')
  )
}
#plots <- map(data ~ ggplot(.x,aes(x=length,y=avg_time)) + geom_point())
#for(frame in data){
#  print(ggplot(frame,aes(x=length,y=avg_time))+geom_point()+labs(title = ))
  #View(data.frame(frame))
#}

# Create a list of ggplot objects, each titled by its list name
#plots <- imap(data, ~ plot_all_trends(ggplot(.x, aes(x=length, y=avg_time))+geom_point()) +
 #               labs(title = .y))

# Print all plots
#walk(plots, print)



library(dplyr)      # data‑wrangling  
library(tidyr)      # nest, unnest, crossing  
library(purrr)      # map, safely  
library(broom)      # augment  
library(ggplot2)    # plotting  
library(stringr)
filter_by_pattern_tt2 <- function(mylist, pattern) {
  # split the pattern string into tokens, "_" means wildcard
  pats <- str_split(pattern, ":", simplify = TRUE)   # :contentReference[oaicite:3]{index=3}
  np   <- length(pats)
  
  # imap: .x = data-frame, .y = element name
  imap(mylist, ~ {
    pr <- str_split(.y, ":", simplify = TRUE)        # :contentReference[oaicite:4]{index=4}
    # test only first np positions:
    ok <- all(
      map_lgl(seq_len(np), function(i) {
        pat <- pats[i]
        if (pat == "_") return(TRUE)
        if (ncol(pr) < i)  return(FALSE)
        pr[1, i] == pat
      })
    )                                                 # :contentReference[oaicite:5]{index=5}
    if (ok) .x else NULL
  }) %>% compact()                                    # drop NULLs :contentReference[oaicite:6]{index=6}
}
sublist <- filter_by_pattern_tt2(data,"Naive")

# .id = "group" creates a column called “group” from the list names
big_df <- bind_rows(sublist, .id = "group")

model_funs <- list(
  linear = possibly(
    function(d) lm(avg_time ~ length, data = d),
    otherwise = NULL
  ),
  quadratic = possibly(
    function(d) lm(avg_time ~ poly(length,2), data = d),
    otherwise = NULL
  ),
  cubic = possibly(
    function(d) lm(avg_time ~ poly(length,3), data = d),
    otherwise = NULL
  ),
  exponential = possibly(
    function(d) nls(avg_time ~ a * exp(b * length), data = d, start = list(a=2.5,b=0.7)),
    otherwise = NULL
  )
)                                                             # :contentReference[oaicite:4]{index=4}

# 2. nest by group, cross with model names
nested <- big_df %>% nest(data = -group)                    # :contentReference[oaicite:5]{index=5}
models <- nested %>% 
  crossing(model_name = names(model_funs)) %>%              # one row per group × model :contentReference[oaicite:6]{index=6}
  mutate(
    fit = map2(data, model_name, ~ model_funs[[.y]](.x))    # fit each safely; returns NULL on failure :contentReference[oaicite:7]{index=7}
  ) %>% 
  filter(!map_lgl(fit, is.null))                            # drop failed fits

# 3. augment to get .fitted
preds <- models %>% 
  mutate(aug = map2(fit, data, ~ augment(.x, data = .y)))  # add .fitted, .resid :contentReference[oaicite:8]{index=8}
preds_long <- preds %>% unnest(aug)                        # flatten

# 4. plot all candidate trendlines?
ggplot(preds_long, aes(x = length, y = avg_time)) +
  #xlim(0,500) +
  #ylim(0,.01)+
  geom_point(alpha = 0.3) +
  geom_line(aes(y = .fitted, color = model_name, linetype = model_name), size = 1) +
  facet_wrap(~ group,) +
  labs(
    title = "All candidate trendlines by group",
    color = "Model", linetype = "Model"
  ) +
  theme_minimal() 
