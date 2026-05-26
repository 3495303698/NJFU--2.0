import java.util.*;
public class SortingAlgorithms {
    private static int[]a;
    public static void main(String[]args) {
        int[]arr={1,5,3,8,6,2};
        System.out.println("Input: [1,5,3,8,6,2]");
        int[]m=arr.clone();
        mergeSort(m);
        System.out.println("Merge: "+Arrays.toString(m));
        a=arr.clone();
        quickSort(0,a.length-1);
        System.out.println("Quick: "+Arrays.toString(a));
    }
    static void mergeSort(int[]arr) {
        mergeSort(arr,0,arr.length-1,new int[arr.length]);
    }
    static void mergeSort(int[]arr,int l,int r,int[]temp) {
        if(l<r) {
            int m=(l+r)/2;
            mergeSort(arr,l,m,temp);
            mergeSort(arr,m+1,r,temp);
            merge(arr,l,m,r,temp);
        }
    }
    static void merge(int[]arr,int l,int m,int r,int[]temp) {
        int i=l,j=m+1,k=0;
        for(;i<=m&&j<=r;)temp[k++]=arr[i]<=arr[j]?arr[i++]:arr[j++];
        for(;i<=m;)temp[k++]=arr[i++];
        for(;j<=r;)temp[k++]=arr[j++];
        for(k=0;l<=r;)arr[l++]=temp[k++];
    }
    static void quickSort(int p,int r) {
        if(p<r) {
            int q=partition(p,r);
            quickSort(p,q-1);
            quickSort(q+1,r);
        }
    }
    static int partition(int p,int r) {
        int i=p,j=r+1,x=a[p];
        while(true) {
            while(++i<r&&a[i]<x);
            while(--j>p&&a[j]>x);
            if(i>=j)break;
            int t=a[i];a[i]=a[j];a[j]=t;
        }
        a[p]=a[j];a[j]=x;
        return j;
    }
}