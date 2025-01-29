import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pandas.plotting import parallel_coordinates

def bar_plot(data, label=None):

    fig = plt.figure(figsize=(15, 8))
    bars = plt.bar(data['Year'], data['Temperature'])

    for i, bar in enumerate(bars):
        if i == 0:  # First year has no change to compare to
            bar.set_color('gray')
        elif data['Temperature_Change'].iloc[i] > 0:
            bar.set_color('red')
        else:
            bar.set_color('blue')
    
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Degrees F +/- From Average', fontsize=12)
    plt.title(label, fontsize=14)
    plt.grid(True, alpha=0.3)

    legend_elements = [
        Patch(facecolor='red', label='Temperature Increase from Previous Year'),
        Patch(facecolor='blue', label='Temperature Decrease from Previous Year'),
        Patch(facecolor='gray', label='First Year (No Change Data)')
    ]
    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.savefig('Temparature-change-bar-plot.png')
    plt.close()
    # plt.show()

def get_user_cereal_choices(data):
    """
    Allow user to select three cereals from the available options
    
    Parameters:
    data (DataFrame): The cereal dataset
    
    Returns:
    list: Three chosen cereal names
    """
    all_cereals = data['Cereal'].tolist()
    chosen_cereals = []
    
    print("\nAvailable cereals:")
    for i, cereal in enumerate(all_cereals, 1):
        print(f"{i}. {cereal}")
    
    for i in range(3):
        while True:
            try:
                choice = int(input(f"\nSelect cereal #{i+1} (enter the number): "))
                if 1 <= choice <= len(all_cereals):
                    cereal = all_cereals[choice-1]
                    if cereal in chosen_cereals:
                        print("You've already selected this cereal. Please choose a different one.")
                    else:
                        chosen_cereals.append(cereal)
                        break
                else:
                    print(f"Please enter a number between 1 and {len(all_cereals)}")
            except ValueError:
                print("Please enter a valid number")
    
    return chosen_cereals

def radar_chart_cereals(data, cereals, stats):

    num_vars = len(stats)
    
    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
    angles += angles[:1]  # Complete the circle
    

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Plot data for each cereal
    colors = ['#FF9999', '#66B2FF', '#99FF99']
    for idx, cereal in enumerate(cereals):
        values = data[data['Cereal'] == cereal][stats].values.flatten().tolist()
        values += values[:1]  # Complete the circle
        
        ax.plot(angles, values, 'o-', linewidth=2, label=cereal, color=colors[idx])
        ax.fill(angles, values, alpha=0.25, color=colors[idx])
    
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats)
    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title("Cereal Nutrition Comparison", pad=20)
    plt.tight_layout()
    plt.savefig('cereal-comparison-radar-chart.png')
    plt.close()
    # plt.show()

def parallel_coordinates_plot(data):
    # Select columns for visualization
    cols_to_plot = ['avail_seat_km_per_week', 'incidents_85_99', 'fatalities_85_99', 
                    'incidents_00_14', 'fatalities_00_14']
    
    # Normalize the data for better visualization
    normalized_data = data.copy()
    for col in cols_to_plot:
        normalized_data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())

    normalized_data['Airline'] = data['airline']
    
    plt.figure(figsize=(15, 8))
    parallel_coordinates(normalized_data, 'Airline', cols=cols_to_plot, colormap=plt.cm.RdYlBu)
    
    plt.title('Airline Safety Metrics Comparison', pad=20)
    plt.xticks(rotation=30)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('Airline-safety-parrallel-cordinates.png')
    plt.close()
    # plt.show()

def scatter_plot_countries(data):

    sorted_data = data.sort_values('Percent', ascending=False)
    
    plt.figure(figsize=(15, 8))
    plt.scatter(range(len(sorted_data)), sorted_data['Percent'], 
                alpha=0.6, c=sorted_data['Percent'], cmap='viridis')
    
    plt.colorbar(label='Percentage')
    plt.xlabel('Country Rank', fontsize=12)
    plt.ylabel('Percentage', fontsize=12)
    plt.title('Country Percentage Distribution', pad=20)
    plt.grid(True, alpha=0.3)
    
    # Annotate some interesting points
    for i, (country, percent) in enumerate(zip(sorted_data['Country'], sorted_data['Percent'])):
        if i < 3 or i > len(sorted_data) - 3:  # Annotate top 3 and bottom 3
            plt.annotate(f'{country}\n{percent:.1f}%', 
                        (i, percent),
                        xytext=(5, 5), 
                        textcoords='offset points')
    
    plt.tight_layout()
    plt.savefig('cousin-marriage.png')
    plt.close()
    # plt.show()

def main():

    data = pd.read_csv('data1.csv', skiprows=4)
    data.columns = ['Year', 'Value']
    data['Temperature'] = data['Value'].astype(float) * 9/5 + 32 # Convert to Fahrenheit 
    data['Temperature_Change'] = data['Temperature'].diff() 

    # Display the summary statistics of the data
    print(data.describe())

    # Calculate and print some trend analysis
    print("\nTrend Analysis:")
    print(f"Average year-over-year change: {data['Temperature_Change'].mean():.2f}°F")
    print(f"Largest single-year increase: {data['Temperature_Change'].max():.2f}°F (Year: {data['Year'][data['Temperature_Change'].idxmax()]})")
    print(f"Largest single-year decrease: {data['Temperature_Change'].min():.2f}°F (Year: {data['Year'][data['Temperature_Change'].idxmin()]})")

    # Calculate the percentage of years with increases vs decreases
    increases = (data['Temperature_Change'] > 0).sum()
    decreases = (data['Temperature_Change'] < 0).sum()
    print(f"\nPercentage of years with temperature increases: {(increases/(increases+decreases)*100):.1f}%")
    print(f"Percentage of years with temperature decreases: {(decreases/(increases+decreases)*100):.1f}%")

    bar_plot(data, 'NOAA Global Land and Ocean Temperature Anomalies (June)')

    cereal_data = pd.read_excel('data2.xls')
    
    # Select nutritional stats to compare
    nutritional_stats = ['Calories', 'Protein', 'Fat', 'Sodium', 'Fiber', 
                        'Carbohydrates', 'Sugars', 'Potassium']
    
    print("Welcome to the Cereal Nutrition Comparison Tool!")
    
    while True:
        user_cereals = get_user_cereal_choices(cereal_data)
        
        radar_chart_cereals(cereal_data, user_cereals, nutritional_stats)
        
        again = input("\nWould you like to compare different cereals? (yes/no): ").lower()
        if again != 'yes':
            break
    
    print("Thank you for using the Cereal Nutrition Comparison Tool!")

    print("\nAnalyzing Airline Safety Data:")
    airline_data = pd.read_csv('data3.csv')
    print(airline_data.describe())
    parallel_coordinates_plot(airline_data)

    print("\nAnalyzing Cousin Marriage Percentage Data:")
    country_data = pd.read_csv('data4.csv')
    print(country_data.describe())
    scatter_plot_countries(country_data)

if __name__ == "__main__":
    main()



    



    

    



   

  