import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec

# Set the style for better-looking graphs
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Load and clean the dataset
df = pd.read_csv('vgsales.csv')
df = df.dropna()

# Convert Year to integer and create a decade column
df['Year'] = df['Year'].astype(int)
df['Decade'] = (df['Year'] // 10) * 10

# 1. Top 10 Games Analysis
plt.figure(figsize=(15, 8))
top_10_games = df.nlargest(10, 'Global_Sales')
ax = sns.barplot(data=top_10_games, x='Name', y='Global_Sales', palette='viridis')
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Best-Selling Video Games of All Time', pad=20, fontsize=14)
plt.xlabel('Game Title', fontsize=12)
plt.ylabel('Global Sales (millions)', fontsize=12)

# Add publisher labels and sales numbers
for i, v in enumerate(top_10_games['Global_Sales']):
    ax.text(i, v, f"{top_10_games['Publisher'].iloc[i]}\n({v:.1f}M)", 
            rotation=0, ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('top_10_sales.png', bbox_inches='tight')
plt.close()

# 2. Sales Distribution Over Time
plt.figure(figsize=(20, 10))
gs = GridSpec(2, 2)

# 2.1 Total sales by decade
plt.subplot(gs[0, 0])
decade_sales = df.groupby('Decade')['Global_Sales'].sum()
sns.barplot(x=decade_sales.index, y=decade_sales.values, palette='viridis')
plt.title('Total Game Sales by Decade', fontsize=12)
plt.xlabel('Decade')
plt.ylabel('Total Sales (millions)')

# Add value labels
for i, v in enumerate(decade_sales.values):
    plt.text(i, v, f'{v:.0f}M', ha='center', va='bottom')

# 2.2 Number of games by decade
plt.subplot(gs[0, 1])
decade_counts = df['Decade'].value_counts().sort_index()
sns.barplot(x=decade_counts.index, y=decade_counts.values, palette='viridis')
plt.title('Number of Games Released by Decade', fontsize=12)
plt.xlabel('Decade')
plt.ylabel('Number of Games')

# Add value labels
for i, v in enumerate(decade_counts.values):
    plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom')

# 2.3 Genre evolution
plt.subplot(gs[1, :])
genre_decade = pd.crosstab(df['Decade'], df['Genre'])
genre_decade_pct = genre_decade.div(genre_decade.sum(axis=1), axis=0) * 100
genre_decade_pct.plot(kind='bar', stacked=True, colormap='viridis')
plt.title('Evolution of Genre Popularity by Decade', fontsize=12)
plt.xlabel('Decade')
plt.ylabel('Percentage of Games')
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('decade_analysis.png', bbox_inches='tight')
plt.close()

# 3. Regional Sales Analysis
plt.figure(figsize=(12, 8))
sales_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
correlation_matrix = df[sales_cols].corr()
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
            vmin=-1, vmax=1, center=0, square=True)
plt.title('Correlation between Regional Sales', pad=20, fontsize=14)
plt.tight_layout()
plt.savefig('sales_correlation.png', bbox_inches='tight')
plt.close()

# 4. Publisher Analysis
plt.figure(figsize=(15, 8))
success_threshold = 1
top_publishers = df['Publisher'].value_counts().nlargest(15).index
publisher_stats = df[df['Publisher'].isin(top_publishers)].groupby('Publisher').agg({
    'Global_Sales': ['count', 'mean', lambda x: (x > success_threshold).mean() * 100]
}).round(2)
publisher_stats.columns = ['Total Games', 'Avg Sales', 'Success Rate %']
publisher_stats = publisher_stats.sort_values('Success Rate %', ascending=False)

fig, ax1 = plt.subplots(figsize=(15, 8))
ax2 = ax1.twinx()

# Plot success rate
bars = sns.barplot(x=publisher_stats.index, y=publisher_stats['Success Rate %'], 
                  color='lightblue', alpha=0.5, ax=ax1)
ax1.set_xticklabels(publisher_stats.index, rotation=45, ha='right')
ax1.set_ylabel('Success Rate %', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Add value labels to bars
for i, v in enumerate(publisher_stats['Success Rate %']):
    ax1.text(i, v, f'{v:.1f}%', ha='center', va='bottom', color='blue')

# Plot average sales
line = ax2.plot(range(len(publisher_stats)), publisher_stats['Avg Sales'], 
                color='red', marker='o')
ax2.set_ylabel('Average Sales (millions)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add value labels to points
for i, v in enumerate(publisher_stats['Avg Sales']):
    ax2.text(i, v, f'{v:.2f}M', ha='center', va='bottom', color='red')

plt.title('Publisher Performance Analysis: Success Rate vs Average Sales', pad=20, fontsize=14)
plt.tight_layout()
plt.savefig('publisher_analysis.png', bbox_inches='tight')
plt.close()

# 5. Platform Market Share
plt.figure(figsize=(15, 8))
platform_sales = df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=True)
total_sales = platform_sales.sum()
platform_share = platform_sales / total_sales * 100

# Create horizontal bar chart
ax = platform_share.plot(kind='barh', color=plt.cm.viridis(np.linspace(0, 1, len(platform_share))))
plt.title('Platform Market Share (% of Global Sales)', pad=20, fontsize=14)
plt.xlabel('Market Share (%)')
plt.ylabel('Platform')

# Add percentage labels
for i, v in enumerate(platform_share):
    ax.text(v, i, f'{v:.1f}%', va='center')

plt.tight_layout()
plt.savefig('platform_share.png', bbox_inches='tight')
plt.close()

# 6. Year-over-Year Analysis
plt.figure(figsize=(15, 8))
yearly_data = df.groupby('Year').agg({
    'Global_Sales': 'sum',
    'Name': 'count'
}).reset_index()
yearly_data['Avg_Sales'] = yearly_data['Global_Sales'] / yearly_data['Name']

fig, ax1 = plt.subplots(figsize=(15, 8))
ax2 = ax1.twinx()

# Plot total sales
ax1.plot(yearly_data['Year'], yearly_data['Global_Sales'], 
         color='blue', linewidth=2, label='Total Sales')
ax1.set_xlabel('Year')
ax1.set_ylabel('Total Sales (millions)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Plot average sales
ax2.plot(yearly_data['Year'], yearly_data['Avg_Sales'], 
         color='red', linewidth=2, label='Average Sales')
ax2.set_ylabel('Average Sales per Game (millions)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('Video Game Sales Trends Over Time', pad=20, fontsize=14)
plt.tight_layout()
plt.savefig('sales_trends.png', bbox_inches='tight')
plt.close()

# Print detailed statistics
print("\nEnhanced Dataset Analysis:")
print(f"Analysis Period: {df['Year'].min()} - {df['Year'].max()} ({df['Year'].max() - df['Year'].min()} years)")
print(f"Total Games Analyzed: {len(df):,}")
print(f"Total Global Sales: {df['Global_Sales'].sum():,.2f} million units")
print(f"Average Sales per Game: {df['Global_Sales'].mean():.2f} million units")

print("\nSuccess Metrics:")
print(f"Games selling over 1M units: {(df['Global_Sales'] > 1).sum():,} ({(df['Global_Sales'] > 1).mean()*100:.1f}%)")
print(f"Games selling over 10M units: {(df['Global_Sales'] > 10).sum():,} ({(df['Global_Sales'] > 10).mean()*100:.1f}%)")

print("\nTop 5 Most Successful Years:")
yearly_sales = df.groupby('Year').agg({
    'Global_Sales': 'sum',
    'Name': 'count'
}).round(2)
yearly_sales['Avg_Sales'] = (yearly_sales['Global_Sales'] / yearly_sales['Name']).round(2)
print(yearly_sales.sort_values('Global_Sales', ascending=False).head().to_string())

print("\nGenre Evolution:")
for decade in sorted(df['Decade'].unique()):
    decade_data = df[df['Decade'] == decade]
    top_genre = decade_data.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    print(f"\n{decade}s Top Genres:")
    print(top_genre.head(3).to_string())

print("\nPlatform Lifecycle Analysis:")
platform_lifecycle = df.groupby('Platform').agg({
    'Year': ['min', 'max'],
    'Global_Sales': 'sum'
}).round(2)
platform_lifecycle.columns = ['Start Year', 'End Year', 'Total Sales']
platform_lifecycle['Lifespan (Years)'] = platform_lifecycle['End Year'] - platform_lifecycle['Start Year']
print("\nTop 5 Platforms by Total Sales:")
print(platform_lifecycle.sort_values('Total Sales', ascending=False).head().to_string())
