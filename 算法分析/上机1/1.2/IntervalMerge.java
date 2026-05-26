import java.util.*;

public class IntervalMerge {
    public int[][] merge(int[][] intervals) {
        // Check if input is empty
        if (intervals.length <= 1) {
            return intervals;
        }
        
        // Sort intervals by start time
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        
        List<int[]> merged = new ArrayList<>();
        // Add the first interval to merged list
        merged.add(intervals[0]);
        
        for (int i = 1; i < intervals.length; i++) {
            // Get the last interval in merged list
            int[] last = merged.get(merged.size() - 1);
            // Current interval's start and end
            int currentStart = intervals[i][0];
            int currentEnd = intervals[i][1];
            
            // If current interval overlaps with last interval, merge them
            if (currentStart <= last[1]) {
                // Update the end of the last interval to the maximum value
                last[1] = Math.max(last[1], currentEnd);
            } else {
                // Otherwise, add current interval to merged list
                merged.add(intervals[i]);
            }
        }
        
        // Convert merged list to array and return
        return merged.toArray(new int[merged.size()][]);
    }
    
    // Main method that reads input from user
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        IntervalMerge solution = new IntervalMerge();
        
        System.out.println("Please enter intervals (format: [[1,3],[2,6],[8,10],[15,18]]): ");
        String input = scanner.nextLine();
        
        // Parse the input string to int[][] intervals
        int[][] intervals = parseInput(input);
        
        // Merge intervals
        int[][] result = solution.merge(intervals);
        
        // Print result
        System.out.println("Merged intervals:");
        for (int[] interval : result) {
            System.out.print("[" + interval[0] + ", " + interval[1] + "] ");
        }
        
        scanner.close();
    }
    
    // Helper method to parse input string to 2D array
    private static int[][] parseInput(String input) {
        // Remove all whitespace and normalize the input
        input = input.replaceAll("\\s+", "");
        
        // Remove outer brackets if present
        if (input.startsWith("[") && input.endsWith("]")) {
            input = input.substring(1, input.length() - 1);
        }
        
        // Split by '],[' to get individual interval strings
        String[] intervalStrs = input.split("\\],\\[");
        List<int[]> intervalList = new ArrayList<>();
        
        for (String intervalStr : intervalStrs) {
            // Remove any remaining brackets
            intervalStr = intervalStr.replace("[", "").replace("]", "");
            
            // Split by comma to get start and end values
            String[] values = intervalStr.split(",");
            if (values.length == 2) {
                try {
                    int start = Integer.parseInt(values[0]);
                    int end = Integer.parseInt(values[1]);
                    intervalList.add(new int[]{start, end});
                } catch (NumberFormatException e) {
                    System.err.println("Invalid number format in interval: " + intervalStr);
                }
            }
        }
        
        // Convert list to array
        return intervalList.toArray(new int[intervalList.size()][]);
     }
}