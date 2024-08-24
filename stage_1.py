import numpy as np
import csv

np.random.seed(66)

# Initialize parameters
S = 140        # Initial spot rate (USD/JPY)
strike_price = 140  # Strike price for the option
r1 = 0.0535    # Interest rate of the foreign currency (USD)
r2 = -0.0031   # Interest rate of the domestic currency (JPY)
sigma = 0.108  # Volatility of the underlying spot rate
maturity_days = 90  # Maturity period in days

# Define time intervals and the number of simulations
time_intervals = [30, 7, 1]  # Different time intervals: one month, one week, one day
num_simulations_list = [20, 200, 1000, 10000, 100000]  # Number of simulations to run for each interval

# Open the CSV files to write the results
with open('simulation_results_stage1.csv', 'w', newline='') as summary_csvfile, \
     open('simulation_results_stage1_detail.csv', 'w', newline='') as detail_csvfile:

    # Set up CSV writers
    summary_csv_writer = csv.writer(summary_csvfile)
    detail_csv_writer = csv.writer(detail_csvfile)

    # Write headers to both CSV files
    summary_csv_writer.writerow(['Interval (days)', 'Number of Simulations', 'Average Payoff'])
    detail_csv_writer.writerow(['Interval (days)', 'Number of Simulations', 'Simulation Number', 'Spot Rate', 'Payoff'])

    # Run simulations
    for interval in time_intervals:
        dt = interval / 365  # Convert the interval into a fraction of a year
        nstep = maturity_days // interval  # Calculate the number of steps based on the interval

        for num_simulations in num_simulations_list:
            final_spot_rates = np.zeros(num_simulations)
            option_payoffs = np.zeros(num_simulations)

            # Simulate each simulation path
            for sim in range(num_simulations):
                S_t = S  # Reset the spot rate to the initial value at the start of each simulation
                for step in range(nstep):
                    epsilon = np.random.normal(0, 1)  # Generate a random number from a standard normal distribution
                    delta_S = (r2 - r1) * S_t * dt + sigma * S_t * epsilon * np.sqrt(dt)
                    S_t += delta_S  # Update the spot rate
                
                final_spot_rates[sim] = S_t  # Store the final spot rate
                option_payoffs[sim] = max(S_t - strike_price, 0)  # Calculate the payoff of the option

                # Write each simulation result to the detailed CSV file
                detail_csv_writer.writerow([interval, num_simulations, sim + 1, final_spot_rates[sim], option_payoffs[sim]])

            # Calculate the average payoff for the current scenario
            average_payoff = np.mean(option_payoffs)

            # Print the summary result to the console
            print(f"Interval: {interval} days, Simulations: {num_simulations}, Average Payoff: {average_payoff:.4f}")

            # Write the summary result to the summary CSV file
            summary_csv_writer.writerow([interval, num_simulations, average_payoff])

print("Simulation results saved to 'simulation_results_stage1.csv' and 'simulation_results_stage1_detail.csv'.")
