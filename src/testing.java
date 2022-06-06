import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class testing {
    public static void main(String[] args) {
        HashMap<Integer,String> hm = new HashMap<>();
        hm.put(1,"a");
        System.out.println(hm.get(2));
        String csv = "1 2 3 10";
        String[] elements = csv.split(" ");
        System.out.println(Arrays.toString(elements));
        for (String var:elements){
            System.out.println(var);
        }
//        int i = Integer.valueOf("123");
//        System.out.println(i);

        ArrayList<Integer> a = new ArrayList<>();
        a.add(0);
        a.add(1);
        a.add(2);
        a.add(3);
        a.add(4);
        a.add(5);
        for(int i=0;i<a.size();i++){
            if(i==2){a.remove(2);}
            System.out.println("index :"+i+" element :"+a.get(i));

        }

    }
}
