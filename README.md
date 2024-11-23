# Video Game Sales Analysis

This project analyzes video game sales data and creates various visualizations to understand trends and patterns in the gaming industry.

## Visualizations

The project generates the following visualizations:

1. **Global Sales by Game**: Bar plot showing sales figures for different games
2. **Genre Distribution**: Pie chart showing the distribution of games across different genres
3. **Rating vs Sales**: Scatter plot with trend line showing the relationship between game ratings and sales
4. **Sales by Genre**: Box plot showing the distribution of sales across different genres
5. **Correlation Matrix**: Heatmap showing correlations between numeric variables (Year, Sales, Rating)

## Setup and Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the analysis:
```bash
python video_games_analysis.py
```

## Output

The script will generate:
- Multiple PNG files containing the visualizations
- Summary statistics in the console output
- Genre-wise average sales analysis

## Dependencies

- pandas (2.0.3)
- matplotlib (3.7.1)
- seaborn (0.12.2)
- numpy (1.24.3)
