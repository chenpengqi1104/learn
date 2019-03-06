public class First {
    public static void main(String[] args){
        int[] arr=new int[]{4,3,1,5,7,8,2};
        int[] arr2=new int[arr.length];
        int a=0;
        int b=arr.length-1;
        for(int i=0;i<arr.length;i++){
            if(a<arr.length){
                arr2[a]=arr[b];
                a++;
                b--;

            }

        }
        for(int i=0;i<arr2.length;i++){
            System.out.print(arr2[i]+",");

        }


    }


}
