public class MatrixChain {
    public static void matrixChain(int[] p, int[][] m, int[][] s) {
        int n = p.length - 1;
        for (int i = 1; i <= n; i++) {
            m[i][i] = 0;
        }
        for (int r = 2; r <= n; r++) {
            for (int i = 1; i <= n - r + 1; i++) {
                int j = i + r - 1;
                m[i][j] = m[i + 1][j] + p[i - 1] * p[i] * p[j];
                s[i][j] = i;
                for (int k = i + 1; k < j; k++) {
                    int t = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                    if (t < m[i][j]) {
                        m[i][j] = t;
                        s[i][j] = k;
                    }
                }
            }
        }
    }

    public static void printOptimalParens(int[][] s, int i, int j) {
        if (i == j) {
            System.out.print("A" + i);
        } else {
            System.out.print("(");
            printOptimalParens(s, i, s[i][j]);
            printOptimalParens(s, s[i][j] + 1, j);
            System.out.print(")");
        }
    }

    public static void main(String[] args) {
        int[] b = {30, 35, 15, 5, 10, 20, 25};
        int n = b.length - 1;
        int[][] m = new int[n + 1][n + 1];
        int[][] s = new int[n + 1][n + 1];
        
        matrixChain(b, m, s);
        
        System.out.println("\nInput array:");
        for (int i = 0; i < b.length; i++) {
            System.out.print(b[i] + " ");
        }
        System.out.println("\n");
        
        System.out.println("Optimal value table m:");
        for (int i = 1; i < m.length; i++) {
            for (int j = 1; j < m[i].length; j++) {
                System.out.print(m[i][j] + "\t");
            }
            System.out.println();
        }
        
        System.out.println("\nPath table s:");
        for (int i = 1; i < s.length; i++) {
            for (int j = 1; j < s[i].length; j++) {
                System.out.print(s[i][j] + "\t");
            }
            System.out.println();
        }
        
        System.out.print("\nOptimal parenthesization:");
        printOptimalParens(s, 1, n);
        System.out.println();
        
        System.out.println("\nMinimum multiplication operations: " + m[1][n]);
    }
}