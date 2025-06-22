
class Sorting:
    def bubble_sort(self, arr):
        """
        This function implements the bubble sort algorithm to sort a list of elements in ascending order.
        
        Args:
            arr (list): The list of elements to be sorted.
        
        Returns:
            None
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

    def insertion_sort(self, arr):
        """
        This function implements the insertion sort algorithm to sort a list of elements in ascending order.
        
        Args:
            arr (list): The list of elements to be sorted.
        
        Returns:
            None
        """
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    def quick_sort(self, arr):
        """
        This function implements the quick sort algorithm to sort a list of elements in ascending order.
        
        Args:
            arr (list): The list of elements to be sorted.
        
        Returns:
            list: The sorted list of elements.
        """
        if len(arr) <= 1:
            return arr
        pivot = arr[0]
        left = [x for x in arr[1:] if x <= pivot]
        right = [x for x in arr[1:] if x > pivot]
        return self.quick_sort(left) + [pivot] + self.quick_sort(right)

    def merge_sort(self, arr):
        """
        This function implements the merge sort algorithm to sort a list of elements in ascending order.
        
        Args:
            arr (list): The list of elements to be sorted.
        
        Returns:
            list: The sorted list of elements.
        """
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        """
        This function merges two sorted lists into a single sorted list.
        
        Args:
            left (list): The first sorted list.
            right (list): The second sorted list.
        
        Returns:
            list: The merged sorted list.
        """
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def generate_random_list(self, size, max_value):

        """
        This function generates a list of random integers.
        
        Args:
            size (int): The number of elements in the list.
            max_value (int): The maximum value of the random integers.
        
        Returns:
            list: The list of random integers.
        """
        import random
        return [random.randint(0, max_value) for _ in range(size)]

    def print_list(self, label, arr):
        """
        This function prints a list with a label.
        
        Args:
            label (str): The label to be printed before the list.
            arr (list): The list to be printed.
        
        Returns:
            None
        """
        print(f"{label}: {arr}")

