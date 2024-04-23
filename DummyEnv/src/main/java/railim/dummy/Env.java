package railim.dummy;

import java.util.*;

//import java.util.Random;
class Observation{
    List<Double> obsTree = new ArrayList<>();
    double[] trainState = new double[5];
    double[] positionNextNode = new double[2];

    @Override
    public String toString() {
        return "Observation{" +
                "obsTree=" + obsTree +
                ", trainState=" + Arrays.toString(trainState) +
                ", positionNextNode=" + Arrays.toString(positionNextNode) +
                '}';
    }

    public void generateRandomObservation(double depthObservationTree){
        for (int i= 0; i<5; i++){
            this.trainState[i] = Math.random();
        }
        for (int i= 0; i<2; i++){
            this.positionNextNode[i] = Math.random();
        }
        int lenObsTree = (int)(Math.pow(2.0, depthObservationTree+1)-1)*17;
        for (int i=0; i<lenObsTree; i++){
            this.obsTree.add(Math.random());
        }
    }
    public Observation(double depthObservationTree, boolean random){

        if (random){
            this.generateRandomObservation(depthObservationTree);
        }
    }
}
class StepOutput{
    Observation observation;
    double reward;
    boolean terminated;
    boolean truncated;
    Map<String, String> info;

    @Override
    public String toString() {
        return "StepOutput{" +
                "observation=" + observation +
                ", reward=" + reward +
                ", terminated=" + terminated +
                ", truncated=" + truncated +
                ", info=" + info +
                '}';
    }

    public StepOutput(int depthObservationTree, boolean random){
        if (random){
            this.observation = new Observation(depthObservationTree, random);
            this.reward = 0;
            this.terminated = false;
            this.truncated = false;
            this.info = Collections.emptyMap();
        }
    }

}
class ResetOutput{
    Observation obs;
    Map<String, String> info;

    @Override
    public String toString() {
        return "ResetOutput{" +
                "obs=" + obs +
                ", info=" + info +
                '}';
    }

    public ResetOutput(int depthObservationTree, boolean random) {
        if (random){
            this.obs = new Observation(depthObservationTree, random);
            this.info = Collections.emptyMap();
        }
    }

}

public class Env {
    List<String> agentIds = new ArrayList<>();
    int numAgents;
    int depthObservationTree;
    boolean random;
    public Env(int numAgents, int depthObservationTree, boolean random){
        this.depthObservationTree=depthObservationTree;
        this.random = random;
        this.numAgents = numAgents;
        if (random){
            for (Integer i=0; i<numAgents; i++){
                agentIds.add(i.toString());
            }
        }
    }

    public ResetOutput reset(){

        ResetOutput resetOutput = new ResetOutput(depthObservationTree, random);
        return resetOutput;
    }

    public StepOutput step (Map<String, Integer> action){
        StepOutput stepOutput = new StepOutput(depthObservationTree, random);
        return stepOutput;
    }

    public List<String> getAgents(){
        return this.agentIds;
    }

//    public static void main(String args[]){
//        Env env = new Env(3, 2, true);
//
//        System.out.println(env.reset());
//
//
//    }

}
