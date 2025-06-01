import time
import tracemalloc
import random
import copy
import sys


# Merge Sort implementation
def merge_sort(array):
    if len(array) > 1:
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]

        # Recursively sort both halves
        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        # Merge the sorted halves back into the original array
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        # Copy remaining elements from left, if any
        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        # Copy remaining elements from right, if any
        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

# Quick Sort implementation with random pivot selection
def quick_sort(array, low, high):
    if low < high:
        # Partition the array with a random pivot and get the pivot index
        pivot_index = partition(array, low, high)
        # Recursively sort elements before and after the pivot
        quick_sort(array, low, pivot_index - 1)
        quick_sort(array, pivot_index + 1, high)

def partition(array, low, high):
    # Choose a random pivot and swap with the last element
    pivot_idx = random.randint(low, high)
    array[pivot_idx], array[high] = array[high], array[pivot_idx]
    
    # Use the last element (now the random pivot) for partitioning
    pivot = array[high]
    i = low - 1

    # Move elements smaller than the pivot to the left
    for j in range(low, high):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]

    # Place the pivot in its final position
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1

# Function to generate test datasets
def generate_datasets(size):
    # Sorted dataset: [1, 2, ..., size]
    sorted_array = list(range(1, size + 1))
    
    # Reverse-sorted dataset: [size, size-1, ..., 1]
    reverse_sorted_array = list(range(size, 0, -1))
    
    # Random dataset: random integers between 1 and 1000
    random_array = [random.randint(1, 1000) for _ in range(size)]
    
    return sorted_array, reverse_sorted_array, random_array

# Function to measure performance of a sorting algorithm
def measure_performance(algorithm, data, is_merge_sort=True):
    # Create a copy of the data to avoid modifying the original
    data_copy = copy.deepcopy(data)
    
    # Start memory tracking
    tracemalloc.start()
    
    # Measure execution time
    start_time = time.perf_counter()
    
    if is_merge_sort:
        algorithm(data_copy)
    else:
        algorithm(data_copy, 0, len(data_copy) - 1)
    
    end_time = time.perf_counter()
    
    # Get memory usage (peak memory in KB)
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return (end_time - start_time) * 1000, peak_memory / 1024  # Time in ms, memory in KB

# Main function to run tests and collect performance metrics
def run_tests():
    sizes = [100, 1000, 5000]  # Reduced max size to avoid recursion depth issues
    
    for size in sizes:
        # Generate datasets
        sorted_array, reverse_sorted_array, random_array = generate_datasets(size)
        
        # Test Merge Sort
        sorted_time_ms, sorted_mem_kb = measure_performance(merge_sort, sorted_array, True)
        reverse_time_ms, reverse_mem_kb = measure_performance(merge_sort, reverse_sorted_array, True)
        random_time_ms, random_mem_kb = measure_performance(merge_sort, random_array, True)
        
        # Test Quick Sort
        sorted_time_qs, sorted_mem_qs = measure_performance(quick_sort, sorted_array, False)
        reverse_time_qs, reverse_mem_qs = measure_performance(quick_sort, reverse_sorted_array, False)
        random_time_qs, random_mem_qs = measure_performance(quick_sort, random_array, False)
        
        # Print results in a simple text format
        print(f"\nResults for size {size}:")
        print("Merge Sort:")
        print(f"  Sorted: Time = {sorted_time_ms:.3f} ms, Memory = {sorted_mem_kb:.3f} KB")
        print(f"  Reverse Sorted: Time = {reverse_time_ms:.3f} ms, Memory = {reverse_mem_kb:.3f} KB")
        print(f"  Random: Time = {random_time_ms:.3f} ms, Memory = {random_mem_kb:.3f} KB")
        print("Quick Sort:")
        print(f"  Sorted: Time = {sorted_time_qs:.3f} ms, Memory = {sorted_mem_qs:.3f} KB")
        print(f"  Reverse Sorted: Time = {reverse_time_qs:.3f} ms, Memory = {reverse_mem_qs:.3f} KB")
        print(f"  Random: Time = {random_time_qs:.3f} ms, Memory = {random_mem_qs:.3f} KB")

if __name__ == "__main__":
    run_tests()
