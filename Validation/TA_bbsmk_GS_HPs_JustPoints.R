# ==== Required Packages ====
library(modifiedmk)
library(readr)
library(dplyr)
library(ggplot2)
library(ggtext)
library(cowplot)
library(gridtext)
library(grid)

# ==== Load and Label Data ====
load_data <- function(path, label) {
  df <- read_csv(path)
  df$opt_type <- label
  return(df)
}

data_GS1 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/1/optimization_log.csv", "GS1")
data_GS2 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/2/optimization_log.csv", "GS2")
data_GS3 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/3/optimization_log.csv", "GS3")
data_GS4 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/4/optimization_log.csv", "GS4")
data_GS5 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/5/optimization_log.csv", "GS5")
data_GS6 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/6/optimization_log.csv", "GS6")
data_GS7 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/7/optimization_log.csv", "GS7")
data_GS8 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/8/optimization_log.csv", "GS8")
data_GS9 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/9/optimization_log.csv", "GS9")
data_GS10 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/10/optimization_log.csv", "GS10")
data_GS11 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/11/optimization_log.csv", "GS11")
data_GS12 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/12/optimization_log.csv", "GS12")
data_GS13 <- load_data("C:/Users/mamad_js/Desktop/MOGWO_Res/_GridSearch/Opt_Log/13/optimization_log.csv", "GS13")

# Combine all
full_data <- bind_rows(data_GS1,data_GS2,data_GS3,data_GS4,data_GS5,data_GS6,data_GS7,data_GS8,data_GS9,data_GS10,data_GS11,data_GS12,data_GS13)
# Set opt_type as a factor with correct order
ordered_labels <- paste0("GS", 1:13)
full_data$opt_type <- factor(full_data$opt_type, levels = ordered_labels)

# ==== Summarize ====
summary_data <- full_data %>%
  group_by(iteration, opt_type) %>%
  summarise(
    NC = mean(num_clusters, na.rm = TRUE),
    MNP = mean(min_n_pxls, na.rm = TRUE),
    DT = mean(dist_thres, na.rm = TRUE),
    MNPF = mean(min_clump_size_factor, na.rm = TRUE),
    DTF = mean(pxl_val_thres_factor, na.rm = TRUE)
  ) %>% ungroup()

# ==== Define Colors & Metric Names ====
line_colors <- c(
  "GS1" = "#001219",   # Rich black (original)
  "GS2" = "#005f73",   # Deep teal (original)
  "GS3" = "#4788c7",   # Viridian green (original)
  "GS4" = "#94d2bd",   # Middle blue green (original)
  "GS5" = "#e9d8a6",   # Straw (original)
  "GS6" = "#ee9b00",   # Gamboge orange (original)
  "GS7" = "#f6bd60",   # Alloy orange (original)
  "GS8" = "#83c5be",   # Rust (original)
  "GS9" = "#e36414",   # Rufous (original)
  "GS10" = "#9b2226",  # Ruby red (original)
  "GS11" = "#415a77",  # Dark cerulean (deep blue)
  "GS12" = "#1a936f",  # Green Munsell (vibrant green)
  "GS13" = "#4cc9f0"   # Vivid sky blue (light blue)
)
metrics <- c("NC", "MNP", "DT", "MNPF", "DTF")
titles <- c("Number of Clusters", "Minimum Number of Pixels", "Distance Thresohld",
            "Minimum Number of Pixels Factor", "Distance Thresohld Factor")

# ==== Label values (below the legend) ====
metric_labels <- list(
  NC = c(
    "GS1" = "-0.551", "GS2" = "-0.487", "GS3" = "-0.712", "GS4" = "-0.554", "GS5" = "-0.613",
    "GS6" = "-0.656", "GS7" = "-0.539", "GS8" = "-0.578", "GS9" = "-0.448", "GS10" = "-0.690",
    "GS11" = "-0.459", "GS12" = "-0.092", "GS13" = "0.766"
  ),
  MNP = c(
    "GS1" = "0.618", "GS2" = "0.486", "GS3" = "0.621", "GS4" = "0.340", "GS5" = "0.473",
    "GS6" = "0.575", "GS7" = "-0.152", "GS8" = "0.434", "GS9" = "0.344", "GS10" = "-0.581",
    "GS11" = "0.041", "GS12" = "0.373", "GS13" = "-0.184"
  ),
  DT = c(
    "GS1" = "0.505", "GS2" = "0.309", "GS3" = "-0.419", "GS4" = "-0.131", "GS5" = "-0.504",
    "GS6" = "0.466", "GS7" = "-0.573", "GS8" = "0.233", "GS9" = "-0.705", "GS10" = "-0.497",
    "GS11" = "-0.620", "GS12" = "-0.005", "GS13" = "-0.267"
  ),
  MNPF = c(
    "GS1" = "0.102", "GS2" = "0.280", "GS3" = "0.166", "GS4" = "0.202", "GS5" = "-0.220",
    "GS6" = "0.215", "GS7" = "0.344", "GS8" = "-0.019", "GS9" = "-0.076", "GS10" = "0.190",
    "GS11" = "-0.122", "GS12" = "-0.019", "GS13" = "-0.123"
  ),
  DTF = c(
    "GS1" = "0.053", "GS2" = "-0.053", "GS3" = "0.138", "GS4" = "0.143", "GS5" = "-0.096",
    "GS6" = "-0.233", "GS7" = "0.122", "GS8" = "0.115", "GS9" = "0.154", "GS10" = "-0.342",
    "GS11" = "0.238", "GS12" = "0.326", "GS13" = "-0.398"
  )
)

# ==== Line Types (All Dashed) ====
linetypes_map <- c(
  "GS1" = "solid",     "GS2" = "dashed",   "GS3" = "solid",  
  "GS4" = "dashed",   "GS5" = "solid", 
  "GS6" = "dashed",     "GS7" = "solid",   "GS8" = "dashed",  
  "GS9" = "solid",   "GS10" = "dashed",
  "GS11" = "solid",    "GS12" = "dashed",  "GS13" = "solid"
)
# ==== Output Directory ====
output_dir <- "C:/Users/mamad_js/Desktop/MOGWO_Res/TrendCompare_HP"
dir.create(output_dir, showWarnings = FALSE)

# ==== Helper Function: Colored Slope Text for Left-aligned Annotation ====
generate_legend_text <- function(label_data, colors) {
  paste0(
    sapply(names(label_data), function(opt) {
      sprintf("<span style='color:%s;'><b>%s</b></span>", colors[opt], label_data[opt])
    }),
    collapse = "<br>"
  )
}
# ==== Modified Main Plotting Loop ====
for (i in seq_along(metrics)) {
  metric <- metrics[i]
  metric_title <- titles[i]
  slope_labels <- metric_labels[[metric]]
  
  # Prepare Data
  plot_data <- summary_data %>%
    select(iteration, opt_type, !!sym(metric)) %>%
    rename(value = !!sym(metric))
  
  # Create custom legend labels with values
  legend_labels <- paste0(names(line_colors), " (", slope_labels[names(line_colors)], ")")
  
  # Create Base Plot
  p <- ggplot(plot_data, aes(x = iteration, y = value, color = opt_type, linetype = opt_type)) +
    geom_line(size = 0.8) +
    geom_point(size = 2) +
    scale_color_manual(
      values = line_colors,
      labels = legend_labels  # Use custom labels with values
    ) +
    scale_linetype_manual(
      values = linetypes_map,
      labels = legend_labels  # Consistent labels for both color and linetype
    ) +
    labs(
      title = metric_title,
      x = "Iteration",
      y = metric_title,
      color = "Optimization ",  # Updated legend title
      linetype = "Optimization " # Keep both legends synchronized
    ) +
    theme_minimal(base_family = "Arial") +
    theme(
      plot.title = element_text(size = 18, face = "bold", hjust = 0.5),
      axis.title = element_text(size = 16),
      axis.text = element_text(size = 14),
      legend.position = "bottom",
      legend.box = "horizontal",
      legend.title = element_text(size = 18),
      legend.text = element_markdown(size = 14), # Allows for HTML formatting
      legend.spacing.x = unit(0.5, 'cm'), # Add space between legend items
      panel.grid.major = element_line(color = "grey90", linetype = "dotted")
    ) +
    guides(
      color = guide_legend(nrow = 3), # Adjust rows as needed
      linetype = guide_legend(nrow = 3)
    )
  
  # Save plot without additional slope annotation (since values are in legend now)
  ggsave(
    filename = file.path(output_dir, paste0(metric, "_TrendPlot.png")),
    plot = p,
    width = 10,  # Wider to accommodate legend
    height = 7,
    dpi = 1000
  )
}

