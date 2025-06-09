# bbsmk --> Nonparametric Block Bootstrapped Mann-Kendall Trend Test

# ✅ Handles autocorrelation via block bootstrap — critical in optimization logs.
 
# ✅ Non-parametric — robust to non-normality.

# ✅ Retains the memory structure of the data — good fit for iteration-based optimization.

# ✅ Gives an empirical p-value from bootstrapping — more reliable in small samples (like your 50 iterations).

# ==== Load Required Packages ====
library(modifiedmk)
library(readr)
library(dplyr)
library(ggplot2)

# ==== Step 1: Load and Prepare Data ====
data <- read_csv("C:/Users/mamad_js/Desktop/MOGWO_Res/_JustF1/Opt_Log/optimization_log.csv")

# Summarize metrics by iteration
summary_data <- data %>%
  group_by(iteration) %>%
  summarise(
    avg_f1 = mean(average_f1_score, na.rm = TRUE),
    num_elim = mean(num_eliminated_polygons, na.rm = TRUE),
    over_seg = mean(over_segmentation_factor, na.rm = TRUE),
    weighted_iou = mean(weighted_mean_iou, na.rm = TRUE),
    mean_iou = mean(mean_iou, na.rm = TRUE),
    obj_score = mean(objective_score, na.rm = TRUE)
  )

# ==== Step 2: Create Output Directory ====
output_dir <- "C:/Users/mamad_js/Desktop/MOGWO_Res/_JustF1/Them_Ev"
dir.create(output_dir, showWarnings = FALSE)

# ==== Step 3: Define Metrics and Labels ====
metrics <- c("avg_f1", "num_elim", "over_seg", "weighted_iou", "mean_iou", "obj_score")
titles <- c("Average F1 Score", "Eliminated Polygons", "Over-Segmentation Factor",
            "Weighted Mean IoU", "Mean IoU", "Objective Score")

# ==== Step 4: Initialize MK Results Data Frame ====
mk_results <- data.frame(
  Metric = character(),
  Tau = numeric(),
  Z = numeric(),
  P_Value = numeric(),
  stringsAsFactors = FALSE
)

# ==== Step 5: Loop Through Metrics ====
for (i in seq_along(metrics)) {
  metric <- metrics[i]
  title <- titles[i]
  y_data <- summary_data[[metric]]
  
  # Perform Block Bootstrap Mann-Kendall Test
  mk <- bbsmk(y_data)  # default: ci = 0.95, nsim = 2000, eta = 1
  
  # Store results (convert to numeric because bbsmk returns a named vector)
  mk_results <- rbind(mk_results, data.frame(
    Metric = title,
    Tau = as.numeric(mk[["Kendall's Tau"]]),
    Z = as.numeric(mk[["Z-Value"]]),
    S = as.numeric(mk[["S"]]),
    Sen_Slope = as.numeric(mk[["Sen's Slope"]]),
    CI_Tau_Lower = as.numeric(mk[["Kendall's Tau Empirical Bootstrapped CI Lower Bound"]]),
    CI_Tau_Upper = as.numeric(mk[["Kendall's Tau Empirical Bootstrapped CI Upper Bound"]]),
    CI_Z_Lower = as.numeric(mk[["Z-value Empirical Bootstrapped CI Lower Bound"]]),
    CI_Z_Upper = as.numeric(mk[["Z-value Empirical Bootstrapped CI Upper Bound"]])
  ))
  
  
  # Create Plot
  p <- ggplot(summary_data, aes_string(x = "iteration", y = metric)) +
    geom_line(color = "#2A9D8F", size = 1) +  # Trend line color
    geom_point(color = "#2A9D8F", size = 2, alpha = 0.6) +
    geom_smooth(method = "lm", linetype = "dashed", color = "#E76F51", size = 0.8) +  # Fit line color
    labs(title = paste(title),
         x = "Iteration",
         y = title) +
    theme_minimal(base_size = 13, base_family = "Arial") +
    theme(
      plot.title = element_text(family = "Arial", face = "bold", size = 28, hjust = 0.5),
      axis.title.x = element_text(family = "Arial", face = "plain", size = 22),
      axis.title.y = element_text(family = "Arial", face = "plain", size = 22),
      axis.text.x = element_text(family = "Arial", size = 18),
      axis.text.y = element_text(family = "Arial", size = 18)
    )
  
  # Save Plot
  ggsave(
    filename = paste0(output_dir, "/", metric, "_bbsmk_plot.png"),
    plot = p, width = 8, height = 5.5, dpi = 1000
  )
}

# ==== Step 6: Save MK Results to CSV ====
write.csv(mk_results, file = paste0(output_dir, "/bbsmk_results.csv"), row.names = FALSE)

cat("✅ Trend analysis complete! Results saved in:", output_dir, "\n")

