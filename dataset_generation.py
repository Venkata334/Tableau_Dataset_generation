"""
I have developed a code that generates synthetic data specifically designed for Tableau, 
enabling the creation of a dashboard intended for publication on Tableau Public.

The motivation behind crafting this data was twofold. Firstly, it offers flexibility in selecting the columns to utilize, 
and secondly, it addresses the challenge of locating similar data readily available on the internet.

This code is adept at simulating fictitious data that closely resembles real-life scenarios, 
thanks to its integration of random variables based on mathematical principles. The code's key steps can be summarized as follows:

1. **Initialization:** This phase involves creating lists for salespeople, managers, stores, regions, and other essential variables.

2. **Assignment:** Salespeople are assigned to managers, stores, and regions as part of this step.

3. **Account Association:** Accounts are linked to salespeople, facilitating a comprehensive data representation.

4. **Determination and Adjustment of Opportunities:** Leveraging a Poisson distribution and 
fine-tuning to approach the target of around 1000 opportunities.

5. **Opportunity Generation:** Opportunities are generated for each account, taking into account predefined weights.

6. **Calculation of Actual Prices:** This step involves applying a variability factor and considering the likelihood of success.

7. **DataFrame Creation and Verification:** The generated data is integrated into a DataFrame while ensuring data consistency 
and coherence.

8. **Incorporating Growth Factors and Seasonality:** The code defines and applies annual growth factors and seasonality patterns.

9. **Monthly Goals:** It generates monthly targets for each salesperson, facilitating performance tracking.

10. **DataFrame for Goals:** This phase involves the integration of monthly goals into a separate DataFrame.

11. **Export and Download of DataFrames:** Finally, the code writes the "opportunities" and "goals" DataFrames 
to an Excel file and retrieves the resulting file.

This comprehensive code streamlines the process of generating synthetic data tailored for Tableau, ensuring that the subsequent dashboard creation and publication on Tableau Public are efficient and effective."""

import random
import pandas as pd
import numpy as np
import xlsxwriter
from datetime import datetime, timedelta
from datetime import date as dt_date, timedelta

# Define the lists of salespeople, managers, stores, and regions
salespeople = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
managers = ['Manager1', 'Manager2', 'Manager3']
stores = ['Store1', 'Store2', 'Store3', 'Store4', 'Store5']
regions = ['Region1', 'Region2', 'Region3']

# Create a list of 50 account names, and a dictionary of account price factors
accounts = [f'Account{i}' for i in range(1, 51)]
account_price_factors = {account: np.random.lognormal(mean=np.log(1), sigma=0.5) for account in accounts}

# Define opportunity types, their weights, product categories, acquisition sources, and acquisition source weights
opportunity_types = ['New customer', 'Upsell', 'Renewal', 'Expansion', 'Cross-sell']
opportunity_types_weights = [0.2, 0.25, 0.3, 0.15, 0.1]
product_categories = ['Electronics', 'Software', 'Home Appliances', 'Furniture', 'Office Supplies']
acquisition_sources = ['Website', 'Referral', 'Direct mail', 'Trade show', 'Cold call']
acquisition_sources_weights = [0.2, 0.25, 0.3, 0.15, 0.1]

# Define result types and their weights, and opportunity stages and their weights
results = ['Won', 'Open', 'Lost']
results_weights = [0.5, 0.3, 0.2]
stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Signature']
stages_weights = [0.4, 0.25, 0.2, 0.1, 0.05]

# Define the start and end dates for the data, and calculate the number of days between them
start_date = dt_date(2021, 5, 1)
end_date = dt_date(2023, 6, 30)
days_range = (end_date - start_date).days

# Assign salespeople to managers, stores, and regions
assignments = []
for salesperson in salespeople:
    manager = random.choice(managers)
    store = random.choice(stores)
    region = random.choice(regions)
    assignments.append((salesperson, manager, store, region))

# Assign accounts to salespeople
num_accounts_per_salesperson = len(accounts) // len(salespeople)
accounts_chunked = [accounts[i:i + num_accounts_per_salesperson] for i in range(0, len(accounts), num_accounts_per_salesperson)]

account_assignments = {}
for salesperson, account_list in zip(salespeople, accounts_chunked):
    for account in account_list:
        account_assignments[account] = salesperson

# Find the appropriate Poisson lambda value to generate approximately 1000 opportunities
lmbda = 1000 / len(accounts)

# Generate the number of opportunities for each account using a Poisson distribution
opportunities_per_account = np.random.poisson(lmbda, len(accounts))
account_opportunities = dict(zip(accounts, opportunities_per_account))

# Calculate the actual number of opportunities that will be generated
total_opportunities = sum(opportunities_per_account)

# Adjust the number of opportunities to be close to 1000
while total_opportunities < 990 or total_opportunities > 1010:
    opportunities_per_account = np.random.poisson(lmbda, len(accounts))
    account_opportunities = dict(zip(accounts, opportunities_per_account))
    total_opportunities = sum(opportunities_per_account)

# Generate data
data = []
opportunity_id = 1

# Iterate through accounts and generate opportunities for each account
for account, num_opportunities in account_opportunities.items():
    for _ in range(num_opportunities):

        # Affect the values
        opportunity_type = random.choices(opportunity_types, weights=opportunity_types_weights)[0]
        salesperson = account_assignments[account]
        manager, store, region = [assignment[1:] for assignment in assignments if assignment[0] == salesperson][0]
        price_factor = account_price_factors[account]
        price = int(np.random.lognormal(mean=np.log(500), sigma=1.5) * price_factor)
        date = start_date + timedelta(days=random.randint(0, days_range))
        product_category = random.choice(product_categories)
        opportunity_description = f"{opportunity_type} opportunity for {store} in {product_category}"
        acquisition_source = random.choices(acquisition_sources, weights=acquisition_sources_weights)[0]
        result = random.choices(results, weights=results_weights)[0]
        stage = 'Signature' if result == 'Won' else random.choices(stages, weights=stages_weights)[0]
        potential_revenue = price * random.randint(1, 10)
        realization_delay = random.choices([30, 60, 90, 180, 365], weights=[0.3, 0.25, 0.2, 0.15, 0.1])[0]
        success_probability = random.randint(20, 100)

        if result == "Open":
            conversion_date = None
        else:
            remaining_days = (end_date - date).days
            max_days = min(realization_delay, remaining_days)
            conversion_date = date + timedelta(days=random.randint(0, max_days))


        # Apply a variation factor to modify the total amount of revenue
        variation_factor = random.uniform(0.5, 1.3)
        price = potential_revenue * success_probability * variation_factor

        # Add generated data to the list
        data.append([opportunity_id, opportunity_type, salesperson, price, region, store, date, manager,
                     opportunity_description, acquisition_source, product_category, success_probability, result,
                     stage, potential_revenue, realization_delay, conversion_date, account])
        
        opportunity_id += 1

# Create a DataFrame with the generated data
df = pd.DataFrame(data, columns=['ID', 'Type', 'Salesperson', 'Price', 'Region', 'Store', 'Date', 'Manager',
                                 'Description', 'Source', 'Category', 'Probability', 'Result', 'Stage', 'Potential_revenue',
                                 'Delay', 'Conversion_date', 'Account'])

# Check consistency between result and stage, and update stage if needed
for index, row in df.iterrows():
    result = row['Result']
    stage = row['Stage']
    
    if result == 'Won' and stage != 'Signature':
        df.at[index, 'Stage'] = 'Signature'
    elif result == 'Lost' and stage == 'Signature':
        df.at[index, 'Stage'] = 'Negotiation'

# Define annual growth factor for each salesperson
annual_growth = {salesperson: random.uniform(0.8, 1.3) for salesperson in salespeople}

# Apply annual growth and seasonality for each salesperson
for index, row in df.iterrows():
    salesperson = row['Salesperson']
    date = row['Date']
    price = row['Price']
    
    year = date.year
    month = date.month
    
    # Apply annual growth
    price *= annual_growth[salesperson] ** (year - 2021)

    # Apply seasonality
    seasonality = 1 + (0.1 * random.uniform(-1, 1))
    if 3 <= month <= 5 or 9 <= month <= 11:
        price *= seasonality
    
    df.at[index, 'Price'] = int(price)

# Generate monthly targets for each salesperson
monthly_targets = []
for year in range(2021, 2024):
    for month in range(1, 13):
        for salesperson in salespeople:
            # Calculate the sum of sales made by the salesperson on this month and year
            df['Date'] = pd.to_datetime(df['Date'])
            monthly_sales = df[(df['Salesperson'] == salesperson) & (df['Result'] == 'Won') & (df['Date'].dt.year == year) & (df['Date'].dt.month == month)]['Price'].sum()
            # Calculate the monthly target
            average_target = monthly_sales * annual_growth[salesperson] * random.uniform(0.9, 1.1)
            # Use a binomial distribution to determine whether the salesperson reaches their target or not. 
            #When low, they achieve more. 
            success_probability = np.random.binomial(1, 0.32)
            target = average_target if success_probability else average_target * random.uniform(0.5, 0.9)
            monthly_targets.append([year, month, salesperson, target])

# Create the DataFrame of monthly targets
df_targets = pd.DataFrame(monthly_targets, columns=['Year', 'Month', 'Salesperson', 'Target'])

# Create a Pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter('opportunities_and_targets.xlsx', engine='xlsxwriter')

# Write the opportunities DataFrame to a sheet named 'opportunities'
df.to_excel(writer, sheet_name='opportunities', index=False)

# Write the targets DataFrame to a sheet named 'targets'
df_targets.to_excel(writer, sheet_name='targets', index=False)

# Close the Pandas Excel writer and output the Excel file
writer.save()

# Indicate the location of the saved Excel file
output_file = 'opportunities_and_targets.xlsx'
print(f"Le fichier Excel a été enregistré sous : {output_file}")
