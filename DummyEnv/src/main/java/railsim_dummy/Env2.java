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
    ManagedChannel channel;
    public Env2(int numAgents, int depthObservationTree, boolean random, int port){
        this.depthObservationTree=depthObservationTree;
        this.random = random;
        this.numAgents = numAgents;
        agentIds.add("train0");

        System.out.println("Env2() -> Created new environment with id: "+port);
        String target = "localhost:"+port;

        channel = Grpc.newChannelBuilder(target, InsecureChannelCredentials.create())
                .build();
        rlClient = new RLClient(channel);
    }
    // reset() function needs to be called by Python
    public void reset() throws InterruptedException {
        System.out.println("reset() -> START the simulation");

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
    }
    public void stepEnv(int num_steps){

        for(int i = 0; i< 100000000; i ++){
            System.out.println("Step: "+i);

            Map<String, Observation> obMap = null;
            for (String aid: this.agentIds){
                railsim_dummy.Observation ob = new railsim_dummy.Observation(this.depthObservationTree, this.random);
                obMap = Map.of(aid, ob);
            }

            System.out.println("Calling RLClient. Get action for state: " + i);
            Map<String, Integer> actionMap = rlClient.getAction(obMap);
            System.out.println("Action Map: " + actionMap);

            System.out.println("Calling RLClient. Send back the observation for state: "+(i+1));
            String response = rlClient.sendObservation(obMap);
        }

    }

    public void close() throws InterruptedException {
        channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
    }
    public List<String> getAgents(){
        return this.agentIds;
    }

}
