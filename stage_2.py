import numpy as np
import csv

# Initialize parameters
r1 = 0.0535    # Interest rate of the foreign currency (USD)
r2 = -0.0031   # Interest rate of the domestic currency (JPY)
sigma = 0.108  # Volatility of the underlying spot rate
strike_price = 140  # Strike price for the option
num_simulations = 1000  # Number of simulations
dt = 1 / 365   # Time period (1 day)

# Define scenarios
maturity_days_scenarios = [1, 7, 30, 90, 180, 360, 720]  # Different maturity periods
initial_spot_rates = [115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165]  # Different initial spot rates

np.random.seed(66)

# Open a CSV file to write the results
with open('simulation_results_stage2.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header to the CSV file
    csv_writer.writerow(['Maturity Days', 'Initial Spot Rate', 'Average Payoff'])

    # Loop through each scenario
    for maturity_days in maturity_days_scenarios:
        num_steps = maturity_days  # Number of steps corresponds to the number of days in maturity

        for S in initial_spot_rates:

            option_payoffs = np.zeros(num_simulations)  # Initialize payoff array

            # Simulate each path
            for sim in range(num_simulations):
                S_t = S  # Start with the initial spot rate for this simulation
                
                # Simulate over the number of steps (maturity days)
                for step in range(num_steps):
                    epsilon = np.random.normal(0, 1)
                    delta_S = (r2 - r1) * S_t * dt + sigma * S_t * epsilon * np.sqrt(dt)
                    S_t += delta_S

                # Calculate the payoff at the end of the simulation path
                option_payoffs[sim] = max(S_t - strike_price, 0)

            # Calculate the average payoff for the scenario
            average_payoff = np.mean(option_payoffs)

            # Write the results for the current scenario to the CSV file
            csv_writer.writerow([maturity_days, S, average_payoff])

            # Print completion message for the scenario
            print(f"Completed simulations for Maturity Days: {maturity_days}, Initial Spot Rate: {S}, Average Payoff: {average_payoff:.4f}")
