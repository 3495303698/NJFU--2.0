public class LCS {
    public static int lcsLength(char[] x, char[] y, int[][] b, int[][] c) {
        int m = x.length - 1;
        int n = y.length - 1;
        
        for (int i = 0; i <= m; i++) c[i][0] = 0;
        for (int j = 0; j <= n; j++) c[0][j] = 0;
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (x[i] == y[j]) {
                    c[i][j] = c[i-1][j-1] + 1;
                    b[i][j] = 1;
                } else if (c[i-1][j] >= c[i][j-1]) {
                    c[i][j] = c[i-1][j];
                    b[i][j] = 2;
                } else {
                    c[i][j] = c[i][j-1];
                    b[i][j] = 3;
                }
            }
        }
        
        return c[m][n];
    }
    
    public static void lcs(int i, int j, char[] x, int[][] b) {
        if (i == 0 || j == 0) return;
        
        if (b[i][j] == 1) {
            lcs(i-1, j-1, x, b);
            System.out.print(x[i]);
        } else if (b[i][j] == 2) {
            lcs(i-1, j, x, b);
        } else {
            lcs(i, j-1, x, b);
        }
    }
    
    public static void printC(int[][] c) {
        System.out.println("Optimal value table c:");
        for (int i = 0; i < c.length; i++) {
            for (int j = 0; j < c[i].length; j++) System.out.print(c[i][j] + " ");
            System.out.println();
        }
    }
    
    public static void printB(int[][] b) {
        System.out.println("Path table b:");
        for (int i = 0; i < b.length; i++) {
            for (int j = 0; j < b[i].length; j++) System.out.print(b[i][j] + " ");
            System.out.println();
        }
    }
    
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Please provide two sequences as arguments when running the program:");
            System.out.println("Example: java LCS ABCBDAB BDCABA");
            return;
        }
        
        String inputX = args[0];
        String inputY = args[1];
        
        System.out.println("Input sequence X: " + inputX);
        System.out.println("Input sequence Y: " + inputY);
        
        char[] x = new char[inputX.length() + 1];
        char[] y = new char[inputY.length() + 1];
        
        for (int i = 0; i < inputX.length(); i++) x[i + 1] = inputX.charAt(i);
        for (int i = 0; i < inputY.length(); i++) y[i + 1] = inputY.charAt(i);
        
        int m = x.length - 1;
        int n = y.length - 1;
        
        int[][] b = new int[m + 1][n + 1];
        int[][] c = new int[m + 1][n + 1];
        
        int result = lcsLength(x, y, b, c);
        
        System.out.println("Length of LCS: " + result);
        System.out.print("LCS: ");
        lcs(m, n, x, b);
        System.out.println();
        
        printC(c);
        printB(b);
    }
}