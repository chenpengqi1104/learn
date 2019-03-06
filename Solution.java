public class Solution {
   public static void main(String[] args){

       int[] nums=new int[]{1,2,3,4,5,6};
       int target=3;
       sum(nums,target);

   }


   public static void sum(int[] arr,int target){
       int a=-1;int b=-1;
       for(int i=0;i<arr.length;i++){
           for(int j=0;j<arr.length;j++){
               if(arr[i]+arr[j]==target){
                   a=i;
                   b=j;
               }
           }
       }
       System.out.print("["+a+","+b+"]");
   }
}