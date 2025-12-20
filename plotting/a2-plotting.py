import matplotlib.pyplot as plt

def seq_kmeans():
    cores = [1,2,4,8,16,32,64]
    time  = [30.4870, 30.4776, 30.4712, 30.5218, 30.4735, 30.5166, 30.4760]

    plt.plot(cores, time, marker='x', label='seq_kmeans')

    plt.xlabel('threads')
    plt.ylabel('time (s)')
    plt.title('Sequential kmeans algorithm')
    plt.grid(True)
    plt.legend()

    plt.savefig('kmeans_sequential.png')

def naive_kmeans():
    cores = [1,2,4,8,16,32,64]
    time  = [37.1963, 24.8800, 13.9567, 7.2850, 8.4043, 8.3289, 8.1785]

    plt.plot(cores, time, marker='x', label='omp_naive_kmeans')

    plt.xlabel('threads')
    plt.ylabel('time (s)')
    plt.title('Shared clusters kmeans algorithm')
    plt.grid(True)
    plt.legend()

    plt.savefig('kmeans_naive.png')

def reduction_kmeans():
    cores = [1,2,4,8,16,32,64]
    time1  = [26.2247, 13.1255, 6.5845, 3.3014, 3.5317, 3.4199, 3.4395]
    time2  = [11.9020, 8.8732, 8.7983, 6.0873, 3.4842, 2.3613, 1.9351]

    plt.plot(cores, time1, marker='x', label='{256, 16, 32, 10}')
    plt.plot(cores, time2, marker='x', label=' {256, 1, 4, 10}')

    plt.xlabel('threads')
    plt.ylabel('time (s)')
    plt.title('Reduction kmeans algorithm')
    plt.grid(True)
    plt.legend()

    plt.savefig('kmeans_reduction.png')

def combined_kmeans():
    cores = [1,2,4,8,16,32,64]
    time_seq  = [30.4870, 30.4776, 30.4712, 30.5218, 30.4735, 30.5166, 30.4760]
    time_naive  = [37.1963, 24.8800, 13.9567, 7.2850, 8.4043, 8.3289, 8.1785]
    time_reduction  = [26.2247, 13.1255, 6.5845, 3.3014, 3.5317, 3.4199, 3.4395]

    plt.plot(cores, time_seq, marker='x', label='seq_kmeans')
    plt.plot(cores, time_naive, marker='x', label='omp_naive_kmeans')
    plt.plot(cores, time_reduction, marker='x', label='omp_reduction_kmeans')

    plt.xlabel('threads')
    plt.ylabel('time (s)')
    plt.title('Kmeans Algorithm Comparison')
    plt.grid(True)
    plt.legend()

    plt.savefig('kmeans_comparison.png')

def fw_1024():
    cores = [1,2,4,8,16,32,64]
    time  = [1.5631, 1.5332, 1.7056, 1.8887, 1.9374, 2.0055, 2.0529]

    plt.plot(cores, time, marker='x', label='fw_1024')

    plt.xlabel('threads')
    plt.ylabel('time (s)')
    plt.title('Floyd-Warshall Algorithm on 1024 nodes')
    plt.grid(True)
    plt.legend()

    plt.savefig('fw_1024.png')

def fw_2048():
    cores = [1,2,4,8,16,32,64]
    time  = [12.3188, 12.3135, 13.2260, 13.2966, 14.3502, 14.6057, 14.5842]

    plt.plot(cores, time, marker='x', label='fw_2048')

    plt.xlabel('threads')
    plt.ylabel('time (s)')
    plt.title('Floyd-Warshall Algorithm on 2048 nodes')
    plt.grid(True)
    plt.legend()

    plt.savefig('fw_2048.png')

def fw_4096():
    cores = [1,2,4,8,16,32,64]
    time  = [102.6385, 101.9390, 105.8651, 107.4590, 110.5474, 111.6533, 112.8505]

    plt.plot(cores, time, marker='x', label='fw_4096')

    plt.xlabel('threads')
    plt.ylabel('time (s)')
    plt.title('Floyd-Warshall Algorithm on 4096 nodes')
    plt.grid(True)
    plt.legend()

    plt.savefig('fw_4096.png')
