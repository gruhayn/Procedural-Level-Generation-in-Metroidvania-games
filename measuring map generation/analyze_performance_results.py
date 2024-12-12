import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
from matplotlib.backends.backend_pdf import PdfPages
import json

# Load performance data
with open("comprehensive_performance_results.json") as file:
    data = json.load(file)

# Flatten `input_params` and convert to DataFrame
df = pd.json_normalize(data)
df.rename(columns=lambda x: x.replace("input_params.", ""), inplace=True)

# Define metrics and parameters
metrics = ['elapsed_time', 'memory_used', 'peak_memory']
parameters = ['Seed', 'Minimum Winning Path Count', 'Room Count', 'Skill Count', 'Sliding Count', 'Neighbor Distance', 'Backward Step Count']

# --- 1. Variance and Standard Deviation Analysis ---
print("Variance and Standard Deviation Analysis:")
for metric in metrics:
    for param in parameters:
        if param in df.columns:
            variance = df.groupby(param)[metric].var()
            std_dev = df.groupby(param)[metric].std()
            print(f"{param} - {metric} Variance:\n", variance)
            print(f"{param} - {metric} Standard Deviation:\n", std_dev)

# --- 2. Correlation Analysis ---
print("\nCorrelation Analysis:")
for metric in metrics:
    for param in parameters:
        if param in df.columns:
            pearson_corr = df[param].corr(df[metric], method='pearson')
            spearman_corr = df[param].corr(df[metric], method='spearman')
            print(f"{param} - {metric} Pearson Correlation: {pearson_corr}")
            print(f"{param} - {metric} Spearman Correlation: {spearman_corr}")

# --- 3. Regression Analysis ---
print("\nRegression Analysis:")
X = df[parameters].drop(columns=['Seed'], errors='ignore')
X = sm.add_constant(X)
for metric in metrics:
    y = df[metric]
    model = sm.OLS(y, X).fit()
    print(f"Regression summary for {metric}:\n", model.summary())

# --- 4. Distribution Analysis with Summary Tables ---
print("\nDistribution Analysis:")
with PdfPages('distribution_analysis_plots.pdf') as pdf:
    for metric in metrics:
        for param in parameters:
            if param in df.columns:
                unique_values = df[param].unique()
                if len(unique_values) > 10:
                    unique_values = np.random.choice(unique_values, size=10, replace=False)
                sampled_df = df[df[param].isin(unique_values)]

                # Histogram and KDE plot
                plt.figure()
                sns.histplot(sampled_df, x=metric, hue=param, kde=True)
                plt.title(f"Distribution of {metric} by {param}")
                pdf.savefig()  # Save to PDF
                plt.close()

                # Box plot
                plt.figure()
                sns.boxplot(x=param, y=metric, data=sampled_df)
                plt.title(f"{metric} by {param}")
                pdf.savefig()  # Save to PDF
                plt.close()

                # Summary statistics table
                summary_stats = sampled_df.groupby(param)[metric].describe()
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.axis("off")
                ax.axis("tight")
                ax.table(cellText=summary_stats.values, colLabels=summary_stats.columns, rowLabels=summary_stats.index, loc='center')
                plt.title(f"Summary Statistics for {metric} by {param}")
                pdf.savefig(fig)
                plt.close()

# --- 5. Outlier Detection ---
print("\nOutlier Detection:")
for metric in metrics:
    q1 = df[metric].quantile(0.25)
    q3 = df[metric].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df[metric] < lower_bound) | (df[metric] > upper_bound)]
    print(f"Outliers in {metric}:\n", outliers)

# --- 6. Scaling Efficiency Analysis ---
print("\nScaling Efficiency Analysis:")
with PdfPages('scaling_efficiency_plots.pdf') as pdf:
    for metric in metrics:
        for param in parameters:
            if param in df.columns:
                plt.figure()
                sns.lineplot(data=df, x=param, y=metric)
                plt.title(f"Scaling of {metric} with {param}")
                pdf.savefig()  # Save to PDF
                plt.close()

# --- 7. Statistical Significance Testing ---
print("\nStatistical Significance Testing:")
for param in parameters:
    if param in df.columns:
        unique_values = df[param].unique()
        if len(unique_values) >= 2:
            for metric in metrics:
                groups = [df[df[param] == value][metric] for value in unique_values if len(df[df[param] == value]) > 1]

                # Check if we have at least two groups with sufficient data for ANOVA
                if len(groups) > 1:
                    f_stat, p_val = f_oneway(*groups)
                    print(f"ANOVA for {param} levels on {metric}: F={f_stat}, p={p_val}")
                else:
                    print(f"Skipping ANOVA for {param} on {metric} due to insufficient data.")
