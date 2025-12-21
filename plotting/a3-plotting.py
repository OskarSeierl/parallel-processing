import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(filename):
    # Load the new file which contains All_GPU data
    df = pd.read_csv(filename)
    target_block_sizes = [32, 48, 64, 128, 238, 512, 1024]

    seq_data = df[df['Implementation'] == 'Sequential']

    # Filter and sort data for each implementation
    naive_data = df[(df['Implementation'] == 'Naive') & (df['blockSize'].isin(target_block_sizes))].sort_values('blockSize')
    transpose_data = df[(df['Implementation'] == 'Transpose') & (df['blockSize'].isin(target_block_sizes))].sort_values('blockSize')
    shmem_data = df[(df['Implementation'] == 'Shmem') & (df['blockSize'].isin(target_block_sizes))].sort_values('blockSize')
    all_gpu_data = df[(df['Implementation'] == 'All_GPU') & (df['blockSize'].isin(target_block_sizes))].sort_values('blockSize')

    return seq_data, naive_data, transpose_data, shmem_data, all_gpu_data

def plot_speedup_comparison(seq_time, naive_data, transpose_data, shmem_data, all_gpu_data, output_file):
    # Calculate Speedups
    naive_speedup = seq_time / naive_data['av_loop_t'].values
    transpose_speedup = seq_time / transpose_data['av_loop_t'].values
    shmem_speedup = seq_time / shmem_data['av_loop_t'].values
    all_gpu_speedup = seq_time / all_gpu_data['av_loop_t'].values

    block_sizes = naive_data['blockSize'].values.astype(str)

    x = np.arange(len(block_sizes))
    width = 0.20  # Width adjusted for 4 bars

    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot Bars
    r1 = ax.bar(x - 1.5*width, naive_speedup, width, label='Naive', color='#9467bd', alpha=0.8, edgecolor='black')
    r2 = ax.bar(x - 0.5*width, transpose_speedup, width, label='Transpose', color='#2ca02c', alpha=0.8, edgecolor='black')
    r3 = ax.bar(x + 0.5*width, shmem_speedup, width, label='Shared Mem', color='#d62728', alpha=0.8, edgecolor='black')
    r4 = ax.bar(x + 1.5*width, all_gpu_speedup, width, label='All GPU', color='#bcbd22', alpha=0.8, edgecolor='black')

    # Plot Trend Lines
    ax.plot(x - 1.5*width, naive_speedup, color='#5e3c99', marker='o', linestyle='-', alpha=0.5)
    ax.plot(x - 0.5*width, transpose_speedup, color='#006d2c', marker='o', linestyle='-', alpha=0.5)
    ax.plot(x + 0.5*width, shmem_speedup, color='#8c1b1b', marker='o', linestyle='-', alpha=0.5)
    ax.plot(x + 1.5*width, all_gpu_speedup, color='#8c8c1b', marker='o', linestyle='-', alpha=0.5)

    ax.set_ylabel('Speedup Factor (vs Sequential)')
    ax.set_xlabel('Block Size')
    ax.set_title('Speedup Comparison: Naive vs Transpose vs Shared Mem vs All GPU')
    ax.set_xticks(x)
    ax.set_xticklabels(block_sizes)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Add labels
    ax.bar_label(r1, padding=3, fmt='%.1f', fontsize=6, rotation=90)
    ax.bar_label(r2, padding=3, fmt='%.1f', fontsize=6, rotation=90)
    ax.bar_label(r3, padding=3, fmt='%.1f', fontsize=6, rotation=90)
    ax.bar_label(r4, padding=3, fmt='%.1f', fontsize=6, rotation=90)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_combined_execution_time(seq_data, naive_data, transpose_data, shmem_data, all_gpu_data, output_file):
    seq_time = seq_data['av_loop_t'].values[0]
    block_sizes = naive_data['blockSize'].values

    # Prepare Plot Data
    labels = ['Sequential']
    gpu_times = [0]
    trans_times = [0]
    cpu_times = [seq_time]

    for bs in block_sizes:
        labels.extend([f'N-{bs}', f'T-{bs}', f'S-{bs}', f'A-{bs}'])

        def get_vals(df, bs):
            row = df[df['blockSize'] == bs]
            if not row.empty:
                return row['t_gpu_avg'].values[0], row['t_transfers_avg'].values[0], row['t_cpu_avg'].values[0]
            return 0, 0, 0

        # Collect data for all 4 implementations
        for data in [naive_data, transpose_data, shmem_data, all_gpu_data]:
            g, t, c = get_vals(data, bs)
            gpu_times.append(g)
            trans_times.append(t)
            cpu_times.append(c)

    x_pos = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(18, 8))

    # Stacked Bars
    p1 = ax.bar(x_pos, gpu_times, label='GPU Execution', color='#1f77b4', edgecolor='black', width=0.8)
    p2 = ax.bar(x_pos, trans_times, bottom=gpu_times, label='Memory Transfer', color='#ff7f0e', edgecolor='black', width=0.8)
    bottom_cpu = np.array(gpu_times) + np.array(trans_times)
    p3 = ax.bar(x_pos, cpu_times, bottom=bottom_cpu, label='CPU / Sequential', color='#2ca02c', edgecolor='black', width=0.8)

    # Formatting
    ax.set_ylabel('Execution Time (s)')
    ax.set_title('Execution Time Breakdown: Naive (N), Transpose (T), Shmem (S), All GPU (A)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=90, ha='center', fontsize=8)
    ax.set_xlabel('Implementation - Block Size')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Add Total Time Text
    total_times = bottom_cpu + np.array(cpu_times)
    for i, v in enumerate(total_times):
        if v > 0:
            ax.text(i, v + 0.1, f'{v:.2f}', ha='center', fontsize=6, rotation=90)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def main():
    filename = 'assignments/a3/Execution_logs/Sz-1024_Coo-32_Cl-64.csv'
    try:
        seq_data, naive_data, transpose_data, shmem_data, all_gpu_data = load_data(filename)
        seq_time = seq_data['av_loop_t'].values[0]

        plot_combined_execution_time(seq_data, naive_data, transpose_data, shmem_data, all_gpu_data, 'combined_execution_time_all.png')
        plot_speedup_comparison(seq_time, naive_data, transpose_data, shmem_data, all_gpu_data, 'speedup_comparison_all.png')

        print("Plots generated successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()