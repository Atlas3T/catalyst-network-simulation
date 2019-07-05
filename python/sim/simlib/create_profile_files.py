import time
import post_processing
import latency_cities_generator


def create_profile_lat():
    p=10
    x=10
    iterations = 1
    list = [1000,10000]

    file_latencies = 'list1.txt'
    filename = latency_cities_generator.get_latencies_filename(file_latencies)
    post_processing.percentage_under_cuttoff_latency(list,p,x,filename,200)

if __name__ == '__main__':
    create_profile_lat()