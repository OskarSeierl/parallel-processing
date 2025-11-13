import matplotlib.pyplot as plt

def seq_kmeans():
    cores = [1,2,4,8,16,32,64]
    time  = [30.4870, 30.4776, 30.4712, 30.5218, 30.4735, 30.5166, 30.4760]

    plt.plot(cores, time, marker='x', label='seq_kmeans')

    plt.xlabel('threads')
    plt.ylabel('time')
    plt.title('Sequential kmeans algorithm')
    plt.grid(True)
    plt.legend()

    plt.savefig('kmeans_sequential.png')

seq_kmeans()