import numpy as np
import csv

# Set the seed for reproducibility
np.random.seed(66)

# Parameters
S = 140        # Initial spot rate (USD/JPY)
strike_price = 140  # Strike price for the option
r1 = 0.0535    # Interest rate of the foreign currency (USD)
r2 = -0.0031   # Interest rate of the domestic currency (JPY)
num_simulations = 10000 # Number of simulations
dt = 1 / 365   # Time period (1 day)

# Scenarios
maturity_days_scenarios = [1, 7, 30, 90, 180, 360, 720]  # Different maturity periods
sigma_scenarios = [0.0, 0.025, 0.05, 0.075, 0.1, 0.108, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]  # Different volatilities

# Open a CSV file to write the results
with open('simulation_results_stage3_2.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header to the CSV file
    csv_writer.writerow(['Maturity Days', 'Sigma', 'Average Payoff'])

    # Loop through each combination of maturity days and sigma scenarios
    for maturity_days in maturity_days_scenarios:
        for sigma in sigma_scenarios:

            option_payoffs = np.zeros(num_simulations)  # Initialize payoff array

            # Simulate each path
            for sim in range(num_simulations):
                S_t = S  # Start with the initial spot rate for this simulation
                
                # Simulate over the number of steps (maturity days)
                for step in range(maturity_days):
                    epsilon = np.random.normal(0, 1)
                    delta_S = (r2 - r1) * S_t * dt + sigma * S_t * epsilon * np.sqrt(dt)
                    S_t += delta_S

                # Calculate the payoff at the end of the simulation path
                option_payoffs[sim] = max(S_t - strike_price, 0)

            # Calculate the average payoff for the current scenario
            average_payoff = np.mean(option_payoffs)

            # Write the results for the current scenario to the CSV file
            csv_writer.writerow([maturity_days, sigma, average_payoff])

            # Print completion message for the scenario
            print(f"Completed simulations for Maturity Days: {maturity_days}, Sigma: {sigma}, Average Payoff: {average_payoff:.4f}")

print("\nAll simulations completed. Results are written to 'simulation_results_stage3_2.csv'.")
