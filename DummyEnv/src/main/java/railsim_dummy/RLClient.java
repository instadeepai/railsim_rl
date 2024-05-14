package railsim_dummy;
import io.grpc.*;

import java.lang.String;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

import railsim_dummy.proto.*;

public class RLClient {
    private final RailsimConnecterGrpc.RailsimConnecterBlockingStub blockingStub;
    private static final Logger logger = Logger.getLogger(RLClient.class.getName());
    public RLClient(Channel channel){
        blockingStub = RailsimConnecterGrpc.newBlockingStub(channel);
    }

    public Map<String, Integer> getAction(Map<String, Observation> obMap){
        // railsim_dummy.proto.ObservationMap ob_message =  railsim_dummy.proto.ObservationMap.newBuilder().addRepeatedField("train1", obMap.get("train1"));
        ObservationMap.Builder observationMapBuilder = ObservationMap.newBuilder();

        for (Map.Entry<String, railsim_dummy.Observation> entry: obMap.entrySet()){
            railsim_dummy.proto.Observation.Builder observationProtoBuilder = railsim_dummy.proto.Observation.newBuilder();

            // Copy values from the Observation object into protoObservation object
            railsim_dummy.Observation origOb= entry.getValue();
            observationProtoBuilder.addAllObsTree(origOb.getObsTree());
            observationProtoBuilder.addAllTrainState( origOb.getTrainState());
            observationProtoBuilder.addAllPositionNextNode(origOb.getPositionNextNode());

            // Build the proto Observation
            railsim_dummy.proto.Observation protoOb = observationProtoBuilder.build();

            // Store the key value pairs in the dictionary
            observationMapBuilder.putDictObservation(entry.getKey(), protoOb);
        }

        // Build the protoObservationMap that will be sent to the python server as a request
        ObservationMap protoObservationMap = observationMapBuilder.build();

        ActionMap actionMap;

        try {
            // Call the original method on the server.
            actionMap = blockingStub.getAction(protoObservationMap);
        } catch (StatusRuntimeException e) {
            // Log a warning if the RPC fails.
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return null;
        }

        return actionMap.getDictActionMap();
    }

    public static void  main(String args[]) throws InterruptedException {

        String user = "world";
        // Access a service running on the local machine on port 50051
        String target = "localhost:50051";

        // Create a communication channel to the server, known as a Channel. Channels are thread-safe
        // and reusable. It is common to create channels at the beginning of your application and reuse
        // them until the application shuts down.
        //
        // For the example we use plaintext insecure credentials to avoid needing TLS certificates. To
        // use TLS, use TlsChannelCredentials instead.
        ManagedChannel channel = Grpc.newChannelBuilder(target, InsecureChannelCredentials.create())
                .build();
        try {
            RLClient client = new RLClient(channel);
            railsim_dummy.Observation ob = new railsim_dummy.Observation(2, true);
            Map<String, railsim_dummy.Observation> obMap = Map.of("train1", ob);
            Map<String, Integer> actionMap = client.getAction(obMap);
            System.out.println(actionMap);

        } finally {
            // ManagedChannels use resources like threads and TCP connections. To prevent leaking these
            // resources the channel should be shut down when it will no longer be used. If it may be used
            // again leave it running.
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
