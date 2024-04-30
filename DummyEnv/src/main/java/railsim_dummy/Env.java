package railsim_dummy;

import java.util.*;

//import java.util.Random;
class Observation{

    List<Double> obsTree = new ArrayList<>();
    double[] trainState = new double[4];
    double[] positionNextNode = new double[2];
    public List<Double> getObsTree() {
        return obsTree;
    }

    public void setObsTree(List<Double> obsTree) {
        this.obsTree = obsTree;
    }

    public double[] getTrainState() {
        return trainState;
    }

    public void setTrainState(double[] trainState) {
        this.trainState = trainState;
    }

    public double[] getPositionNextNode() {
        return positionNextNode;
    }

    public void setPositionNextNode(double[] positionNextNode) {
        this.positionNextNode = positionNextNode;
    }


    @Override
    public String toString() {
        return "Observation{" +
                "obsTree=" + obsTree +
                ", trainState=" + Arrays.toString(trainState) +
                ", positionNextNode=" + Arrays.toString(positionNextNode) +
                '}';
    }

    public void generateRandomObservation(double depthObservationTree){
        for (int i= 0; i<4; i++){
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

    public Observation getObservation() {
        return observation;
    }

    public void setObservation(Observation observation) {
        this.observation = observation;
    }

    public double getReward() {
        return reward;
    }

    public void setReward(double reward) {
        this.reward = reward;
    }

    public boolean isTerminated() {
        return terminated;
    }

    public void setTerminated(boolean terminated) {
        this.terminated = terminated;
    }

    public boolean isTruncated() {
        return truncated;
    }

    public void setTruncated(boolean truncated) {
        this.truncated = truncated;
    }

    public Map<String, String> getInfo() {
        return info;
    }

    public void setInfo(Map<String, String> info) {
        this.info = info;
    }

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

    public Observation getObs() {
        return obs;
    }

    public void setObs(Observation obs) {
        this.obs = obs;
    }

    Map<String, String> info;

    public Map<String, String> getInfo() {
        return info;
    }

    public void setInfo(Map<String, String> info) {
        this.info = info;
    }

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

    public Map<String, ResetOutput> reset(){

        Map<String, ResetOutput> resetout = new HashMap<String, ResetOutput>();
        for (String aid: this.agentIds){
            ResetOutput resetOutputPerAgent = new ResetOutput(this.depthObservationTree, this.random);
            resetout.put(aid, resetOutputPerAgent);
        }
        return resetout;
    }

    public Map<String, StepOutput> step (Map<String, Integer> action){

        Map<String, StepOutput> stepout = new HashMap<String, StepOutput>();
        for (String aid: this.agentIds){
            StepOutput stepOutputPerAgent = new StepOutput(this.depthObservationTree, this.random);
            stepout.put(aid, stepOutputPerAgent);
        }
        return stepout;
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
