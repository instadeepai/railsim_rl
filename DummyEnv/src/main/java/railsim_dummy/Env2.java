package railsim_dummy;

import io.grpc.Grpc;
import io.grpc.InsecureChannelCredentials;
import io.grpc.ManagedChannel;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class Env2 {

    static RLClient rlClient;

    int numAgents;
    int depthObservationTree;
    boolean random;
    List<String> agentIds = new ArrayList<>();
    public Env2(int numAgents, int depthObservationTree, boolean random){
        this.depthObservationTree=depthObservationTree;
        this.random = random;
        this.numAgents = numAgents;
        if (random){
            for (Integer i=0; i<numAgents; i++){
                agentIds.add(i.toString());
            }
        }
    }
    // reset() function needs to be called by Python
    public void reset() throws InterruptedException {
        System.out.println("START the simulation");

        String target = "localhost:50051";

        ManagedChannel channel = Grpc.newChannelBuilder(target, InsecureChannelCredentials.create())
                .build();

        try {
            rlClient = new RLClient(channel);

            // send the initial observation
            System.out.println("Send the initial observation");
            Map<String, Observation> obMap = new HashMap<>();
            for (String aid: this.agentIds){
                railsim_dummy.Observation ob = new railsim_dummy.Observation(this.depthObservationTree, this.random);
                obMap.put(aid, ob);
            }
            rlClient.sendObservation(obMap);

            // start the simulation loop
            System.out.println("Start the simulation loop");
            this.stepEnv(10);

        } finally {
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
    public void stepEnv(int num_steps){

        for(int i = 0; i< num_steps; i ++){
            System.out.println("Step: "+i);

            Map<String, Observation> obMap = null;
            for (String aid: this.agentIds){
                railsim_dummy.Observation ob = new railsim_dummy.Observation(this.depthObservationTree, this.random);
                obMap = Map.of(aid, ob);
            }

            System.out.println("Calling RLClient. Get action for state: " + i);
            Map<String, Integer> actionMap = rlClient.getAction(obMap);
            System.out.println(actionMap);

            System.out.println("Calling RLClient. Send back the observation for state: "+(i+1));
            String response = rlClient.sendObservation(obMap);
        }

    }
    public List<String> getAgents(){
        return this.agentIds;
    }
//    public static void main(String args[]) throws InterruptedException {
//        String target = "localhost:50051";
//
//        ManagedChannel channel = Grpc.newChannelBuilder(target, InsecureChannelCredentials.create())
//                .build();
//
//        try {
//            rlClient = new RLClient(channel);
//            Env2 env = new Env2();
//            env.stepEnv(10);
//
//        } finally {
//            // ManagedChannels use resources like threads and TCP connections. To prevent leaking these
//            // resources the channel should be shut down when it will no longer be used. If it may be used
//            // again leave it running.
//            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
//        }
//    }

    public static void main(String args[]) throws InterruptedException {
        Env2 env = new Env2(2, 2, true);
        env.reset();
    }

}
