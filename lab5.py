import random


# ============================================================================
# MIN-MAX DIVIDE AND CONQUER
# ============================================================================

class ComparisonCounter:
    """Thread-safe comparison counter using a class instead of global variable."""
    def __init__(self):
        self.count = 0

    def reset(self):
        self.count = 0

    def increment(self, n=1):
        self.count += n

    def get(self):
        return self.count


def min_max_dc(arr, low, high, counter=None):
    """
    Divide and Conquer Min-Max Algorithm
    Time: O(n), Comparisons: 3n/2 - 2
    """
    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        if counter:
            counter.increment()
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid, counter)
    rmin, rmax = min_max_dc(arr, mid + 1, high, counter)

    # Conquer: combine with 2 comparisons
    if counter:
        counter.increment()
    overall_min = lmin if lmin < rmin else rmin
    if counter:
        counter.increment()
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    """
    Naive Linear Min-Max Algorithm
    Time: O(n), Comparisons: 2(n-1)
    """
    mn, mx = arr[0], arr[0]
    comps = 0
    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x
        comps += 1
        if x > mx:
            mx = x
    return mn, mx, comps
