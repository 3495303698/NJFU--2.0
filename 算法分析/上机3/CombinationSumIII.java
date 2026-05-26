import java.util.ArrayList;
import java.util.List;

public class CombinationSumIII {
    public List<List<Integer>> combinationSum3(int k, int n) {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> current = new ArrayList<>();
        int minSum = k * (k + 1) / 2;
        if (minSum > n) {
            return result;
        }
        backtrack(result, current, k, n, 1, 0);
        return result;
    }
    
    private void backtrack(List<List<Integer>> result, List<Integer> current, int k, int n, int start, int sum) {
        if (current.size() == k) {
            if (sum == n) {
                result.add(new ArrayList<>(current));
            }
            return;
        }
        
        int remainingCount = k - current.size(); 
        int remainingSum = n - sum;
        
        for (int i = start; i <= 9; i++) {
            if (i > remainingSum) {
                break;
            }
            
            if (i + (remainingCount - 1) > 9) {
                break;
            }
            
            int minPossibleRemainingSum = 0;
            for (int j = 1; j < remainingCount; j++) {
                minPossibleRemainingSum += (i + j);
            }
            if (sum + i + minPossibleRemainingSum > n) {
                break;
            }
            
            current.add(i);
            backtrack(result, current, k, n, i + 1, sum + i);
            current.remove(current.size() - 1);
        }
    }
    
    public static void main(String[] args) {
        CombinationSumIII solution = new CombinationSumIII();
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        
        System.out.print("Enter k value (2-9): ");
        int k = scanner.nextInt();
        
        System.out.print("Enter n value (1-60): ");
        int n = scanner.nextInt();
        
        if (k < 2 || k > 9) {
            System.out.println("Error: k must be between 2 and 9");
            return; 
        }
        
        if (n < 1 || n > 60) {
            System.out.println("Error: n must be between 1 and 60");
            return;
        }
        
        List<List<Integer>> result = solution.combinationSum3(k, n);
        System.out.println("Result: " + result);
        
        scanner.close();
    }
}