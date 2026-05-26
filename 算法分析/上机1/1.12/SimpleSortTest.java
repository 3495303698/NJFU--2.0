import java.util.Arrays;

public class SimpleSortTest {
    public static void main(String[] args) {
        // Test array from example
        int[] array = {1, 5, 3, 8, 6, 2};
        System.out.println("Original array: " + Arrays.toString(array));
        
        // Test merge sort
        int[] mergeArray = array.clone();
        mergeSort(mergeArray);
        System.out.println("Merge sort result: " + Arrays.toString(mergeArray));
        
        // Test quick sort
        int[] quickArray = array.clone();
        quickSort(quickArray);
        System.out.println("Quick sort result: " + Arrays.toString(quickArray));
    }
    
    // Simple merge sort implementation
    public static void mergeSort(int[] arr) {
        if (arr.length > 1) {
            int[] left = Arrays.copyOfRange(arr, 0, arr.length / 2);
            int[] right = Arrays.copyOfRange(arr, arr.length / 2, arr.length);
            
            mergeSort(left);
            mergeSort(right);
            
            merge(arr, left, right);
        }
    }
    
    private static void merge(int[] result, int[] left, int[] right) {
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        while (i < left.length) {
            result[k++] = left[i++];
        }
        while (j < right.length) {
            result[k++] = right[j++];
        }
    }
    
    // Simple quick sort implementation
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }
    
    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
    
    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = (low - 1);
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        return i + 1;
    }
}