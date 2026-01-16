import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_serial_heat_comparison():
    algos = ['Midpoint Jacobi', 'GaussSeidelSOR', 'RedBlackSOR']
    iterations = np.array([68000, 700, 600])
    times = np.array([27.888961, 0.501670, 0.280424])

    x = np.arange(len(algos))
    width = 0.4

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax2 = ax1.twinx()

    ax1.bar(x - width / 2, times, width=width, color='C0', label='Time (s)')
    ax2.bar(x + width / 2, iterations, width=width, color='C1', alpha=0.6, label='Iterations')

    ax1.set_xlabel('Algorithm')
    ax1.set_xticks(x)
    ax1.set_xticklabels(algos, rotation=25, ha='right')
    ax1.set_ylabel('Time (s)')
    ax2.set_ylabel('Iterations')

    ax2.set_yscale('log')  # iterations span many orders of magnitude
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    fig.savefig('serial-heat-comparison.png')

# python
def plot_kmeans_speedup():
    # Data from your output
    mpi_processes = [1, 2, 4, 8, 16, 32, 64]
    execution_times = [27.4519, 13.8013, 6.9068, 3.4575, 1.7447, 0.8885, 0.4641]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(mpi_processes, execution_times, marker='o', linestyle='-', color='blue', linewidth=2, label='Measured Time')

    # Formatting the axes
    plt.title('K-Means Execution Time vs. MPI Processes', fontsize=14)
    plt.xlabel('Number of MPI Processes', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.grid(True, which='both', linestyle='--', alpha=0.7)

    # Set x-ticks to match the specific MPI counts used
    plt.xticks(mpi_processes)

    # Optional: Log scale for better visibility if needed (uncomment next lines)
    # plt.xscale('log', base=2)
    # plt.yscale('log')

    # Show/Save the plot
    plt.legend()
    plt.tight_layout()
    plt.savefig('kmeans-speedup.png')


def get_heat_transfer_data():
    """
    Creates the DataFrame from the raw data.
    """
    data = [
        ["2048 x 2048", 1, 256, 8.413702, 8.414123],
        ["2048 x 2048", 2, 256, 6.024697, 6.152518],
        ["2048 x 2048", 4, 256, 4.314543, 4.450864],
        ["2048 x 2048", 8, 256, 4.202319, 4.449088],
        ["2048 x 2048", 16, 256, 1.881960, 2.202697],
        ["2048 x 2048", 32, 256, 0.428457, 0.840580],
        ["2048 x 2048", 64, 256, 0.053749, 0.510428],
        ["4096 x 4096", 1, 256, 33.620226, 33.620841],
        ["4096 x 4096", 2, 256, 24.088592, 24.349077],
        ["4096 x 4096", 4, 256, 17.226597, 17.544666],
        ["4096 x 4096", 8, 256, 17.102705, 17.758703],
        ["4096 x 4096", 16, 256, 8.414368, 9.490479],
        ["4096 x 4096", 32, 256, 4.389757, 5.731105],
        ["4096 x 4096", 64, 256, 3.116035, 4.503513],
        ["6144 x 6144", 1, 256, 75.647966, 75.648631],
        ["6144 x 6144", 2, 256, 54.119991, 54.624610],
        ["6144 x 6144", 4, 256, 38.837143, 256.0], # Raw data value
        ["6144 x 6144", 8, 256, 38.524304, 39.831681],
        ["6144 x 6144", 16, 256, 19.312184, 21.276588],
        ["6144 x 6144", 32, 256, 10.010550, 12.850533],
        ["6144 x 6144", 64, 256, 8.011463, 10.742320]
    ]
    df = pd.DataFrame(data, columns=["Grid Size", "Threads", "Iterations", "Computation Time (s)", "Total Time (s)"])
    return df

def plot_heat_transfer_performance(df, grid_size):
    """
    Generates and saves a plot for a specific grid size.
    """
    subset = df[df["Grid Size"] == grid_size]

    plt.figure(figsize=(10, 6))
    plt.plot(subset["Threads"], subset["Total Time (s)"], marker='o', label='Total Time (s)')
    plt.plot(subset["Threads"], subset["Computation Time (s)"], marker='x', linestyle='--', label='Computation Time (s)')

    plt.title(f"Performance for Grid Size: {grid_size}")
    plt.xlabel("MPI Threads")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.grid(True)

    # Save the file
    filename = f"performance_{grid_size.replace(' ', '').replace('x', '_')}.png"
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_heat_transfer_without_convergence():
    df = get_heat_transfer_data()
    unique_grids = df["Grid Size"].unique()

    for grid in unique_grids:
        plot_heat_transfer_performance(df, grid)

if __name__ == "__main__":
    plot_heat_transfer_without_convergence()