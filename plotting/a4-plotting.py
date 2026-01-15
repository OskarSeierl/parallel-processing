import numpy as np
import matplotlib.pyplot as plt

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


if __name__ == "__main__":
    plot_kmeans_speedup()