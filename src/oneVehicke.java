

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Stack;

public class oneVehicke {

    public static void main(String[] args) {
        ArrayList<Integer> tw1 = new ArrayList<>();tw1.add(30);tw1.add(60);
        ArrayList<Integer> tw2 = new ArrayList<>();tw2.add(40);tw2.add(70);
        ArrayList<Integer> tw3 = new ArrayList<>();tw3.add(60);tw3.add(140);

        ArrayList<ArrayList<Integer>> timeWindows = new ArrayList<>();
        timeWindows.add(tw1);timeWindows.add(tw2);timeWindows.add(tw3);

        int[][] timeMatrix = {
                {0,20,30},
                {20,0,10},
                {30,10,0}
        };
//        int[][] timeMatrix = {
//                {0,20},
//                {20,0},
//        };
//        System.out.println(timeWindows);
        int nodeCount = 0;
        ArrayList<ArrayList<Integer>> discreteTimeWindows = new ArrayList<>();
        ArrayList<ArrayList<Integer>> nodes = new ArrayList<>();
        for(int i=0;i<timeWindows.size();i++){
            int st = timeWindows.get(i).get(0);
            int et = timeWindows.get(i).get(1);

            ArrayList<Integer> window= new ArrayList<>();
            ArrayList<Integer> verticesOfSingleCust= new ArrayList<>();
            for(int j=st;j<=et;j=j+10){
                window.add(j);
                verticesOfSingleCust.add(nodeCount); nodeCount++;
            }
            discreteTimeWindows.add(window);
            nodes.add(verticesOfSingleCust);
        }
        System.out.println("discreteTimeWindows"+":"+discreteTimeWindows);
        System.out.println("Nodes "+":"+nodes);
        System.out.println("Nodes Count"+":"+nodeCount); // one more than # of vertices

        ArrayList<ArrayList<Integer>> graph = new ArrayList<>();

        graph = constructGraph(timeWindows,timeMatrix,nodes,discreteTimeWindows);
        int[] topologicalSorted = topologicalSort(graph);
        String maxPath= maxNode(topologicalSorted,graph,nodes);


//        System.out.println(maxPath);



    }
    public static int numberOfVehicles(ArrayList<ArrayList<Integer>> timeWindows,int[][] timeMatrix,ArrayList<ArrayList<Integer>> nodes,ArrayList<ArrayList<Integer>> discreteTimeWindows){
        ArrayList<ArrayList<Integer>> graph = new ArrayList<>();
        int vehicleCount = 0;
        int removedCustomers = 0;
        graph = constructGraph(timeWindows,timeMatrix,nodes,discreteTimeWindows);

        int totalCustomers = graph.size();
        while (removedCustomers < totalCustomers){
            int[] topologicalSorted = topologicalSort(graph);
            String maxNodes = maxNode(topologicalSorted,graph,nodes);
            ArrayList<Integer> removed = new ArrayList<>();
            removed.add(-1);
            for(int i=0;i<maxNodes.length();i++){
                int node = Character.getNumericValue(maxNodes.charAt(i));
                for (int j=0;j< nodes.size();j++){
                    if(nodes.get(j).contains(node)){
                        for(int k = 0;k<nodes.get(j).size();k++){ // removing nodes of a particular customer
                            int nodeToBeRemoved = nodes.get(j).get(i);
                            // marking node in graph as removed by replacing with {-1}
                            graph.set(nodeToBeRemoved,removed);
                            for (int l=0;l< graph.size();l++){
                                if(graph.get(l).contains(nodeToBeRemoved)){
                                    // removing all edges connected to a node of interest
                                    int indexToRemove = graph.get(l).indexOf(nodeToBeRemoved);
                                    System.out.println("index to remove "+indexToRemove);
                                    graph.get(l).remove(indexToRemove);

                                }
                            }
                        }
                        nodes.set(j,removed);
                        discreteTimeWindows.set(j,removed);
                        System.out.println("removed "+j+" "+nodes);
                        System.out.println("nodes "+nodes);
                        System.out.println("discreteTimeWindows "+discreteTimeWindows);
                        System.out.println("graph "+graph);
                        removedCustomers++;
                        break;
                    }
                }
            }

            // this should return max Nodes with distinct customers
            //remove all visited customer's time window and repeat
        }



        return 0;
    }
    public static void dfs(int node, ArrayList<ArrayList<Integer>> adjMatrix,boolean[] visited,Stack<Integer> st) {
        visited[node] = true;
        for (int i=0;i<adjMatrix.get(node).size();i++){
            int newnode = adjMatrix.get(node).get(i);
            if(visited[newnode] == false){
                dfs(newnode,adjMatrix,visited,st);
            }
            // new node fully explored
        }
        st.push(node);
    }

    public static int[] topologicalSort(ArrayList<ArrayList<Integer>> graph){
        Stack <Integer> st = new Stack<>();
        boolean[] visited = new boolean[graph.size()];


        for(int i=0;i<graph.size();i++){
            if(!visited[i]){
                dfs(i,graph,visited,st);
            }
        }
        System.out.println(st);
        int[] topologicalSorted = new int[graph.size()];
        for(int i=0;i<topologicalSorted.length ;i++){topologicalSorted[i] = st.pop();}
        System.out.println(Arrays.toString(topologicalSorted));
        return topologicalSorted;

    }

    public static ArrayList<ArrayList<Integer>> constructGraph(ArrayList<ArrayList<Integer>> timeWindows,int[][] timeMatrix,ArrayList<ArrayList<Integer>> nodes,ArrayList<ArrayList<Integer>> discreteTimeWindows){
        //converting to discrete time intervals
        ArrayList<ArrayList<Integer>> graph = new ArrayList<>();
        for(int i=0;i<nodes.size();i++){
            for(int j=0;j<nodes.get(i).size();j++){
                int currNode = nodes.get(i).get(j);
                int currTime = discreteTimeWindows.get(i).get(j);
                ArrayList<Integer> reachableNodes = new ArrayList<>();
                for(int k = 0;k<nodes.size();k++){
                    if(k!=i){   // not calculating for same nodes
                        for(int l=0;l<nodes.get(k).size();l++){
                            int secNode = nodes.get(k).get(l);
                            int secTime = discreteTimeWindows.get(k).get(l);
                            int timereq = timeMatrix[i][k]; // time from ith to kth node
                            if(timereq + currTime <= secTime){ reachableNodes.add(secNode); }
                        }
                    }
                }
                graph.add(reachableNodes);
            }
        }
        System.out.println("Graph :");
        for (int i=0;i< graph.size();i++){
            System.out.println((i)+":"+graph.get(i));
        }
        return graph;
    }

    public static String maxNode(int[] arr,ArrayList<ArrayList<Integer>> graph,ArrayList<ArrayList<Integer>> nodes) {
        int[] dp = new int[arr.length]; // dp[i] -> maximum nodes from s to i
        String[] path = new String[arr.length];
        dp[0] = 1; path[0] = ""+arr[0];
        for (int i = 1; i<arr.length;i++){
            dp[i]=1;
            path[i] = ""+arr[i];
            for (int j = i-1;j >=0;j--){
                if(graph.get(arr[j]).contains(arr[i])) {// there is an edge from j -> i
                    if(dp[i]<1+dp[j]){
//                        path[i] = path[j]+"->"+path[i];
                        path[i] = path[j]+" "+path[i];
                        dp[i] =1+dp[j];
                    }
                }
            }
        }
        int maxNodes = 0;int mN = 0;int index = 0;
        for(int i=0;i<dp.length;i++){  maxNodes = Math.max(maxNodes,dp[i]); }
        for(int i=0;i<dp.length;i++){  if( mN < dp[i]  ){ index = i;} }
        System.out.println(Arrays.toString(dp));
        System.out.println(Arrays.toString(path));
        System.out.println("maxNodes = "+maxNodes);

        String maxPath = maxPathDistinctCustomer(path,graph,nodes);
        return maxPath;
    }
    public static String maxPathDistinctCustomer (String[] path,ArrayList<ArrayList<Integer>> graph,ArrayList<ArrayList<Integer>> nodes){ // n-> number of customers

        int maxCount = 0; // stores distinct customer
        String maxPath = "";

        for(int i=0;i<path.length;i++){
            String[] paths  = path[i].split(" "); //[1 2 3 10]
            ArrayList<Integer> arr = new ArrayList<>();
            for (String nodeValue : paths){
                System.out.println("NodeValues :"+nodeValue);
                for(int j=0;j<nodes.size();j++){
                    if(nodes.get(j).contains(Integer.valueOf(nodeValue))){
                        if(arr.contains(j) == false) {arr.add(j);
                            System.out.println(arr); }
                    }
                }

            }
            System.out.println("distinct customer in "+path[i]+" are : "+arr.size());
            if(maxCount < arr.size()){ maxPath = path[i]; maxCount = arr.size(); }
//            maxCount =Math.max(maxCount,count);
//            }

        }

        return maxPath;


    }
}
