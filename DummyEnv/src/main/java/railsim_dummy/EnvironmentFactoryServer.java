package railsim_dummy;
import io.grpc.Grpc;
import io.grpc.InsecureServerCredentials;
import io.grpc.Server;
import io.grpc.stub.StreamObserver;
import railsim_dummy.proto.ConfirmationResponse;
import railsim_dummy.proto.GrpcPort;
import railsim_dummy.proto.RailsimFactoryGrpc;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;
public class EnvironmentFactoryServer {

    private static final Logger logger = Logger.getLogger(EnvironmentFactoryServer.class.getName());

    private Server server;

    private void start() throws IOException {
        /* The port on which the server should run */
        int factoryServerPort = 50051;
        server = Grpc.newServerBuilderForPort(factoryServerPort, InsecureServerCredentials.create())
                .addService(new RailsimFactory())
                .build()
                .start();
        logger.info("Server started, listening on " + factoryServerPort);
        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                // Use stderr here since the logger may have been reset by its JVM shutdown hook.
                System.err.println("*** shutting down gRPC server since JVM is shutting down");
                try {
                    EnvironmentFactoryServer.this.stop();
                } catch (InterruptedException e) {
                    e.printStackTrace(System.err);
                }
                System.err.println("*** server shut down");
            }
        });
    }

    private void stop() throws InterruptedException {
        if (server != null) {
            server.shutdown().awaitTermination(30, TimeUnit.SECONDS);
        }
    }

    /**
     * Await termination on the main thread since the grpc library uses daemon threads.
     */
    private void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }

    /**
     * Main launches the server from the command line.
     */
    public static void main(String[] args) throws IOException, InterruptedException {
        final EnvironmentFactoryServer server = new EnvironmentFactoryServer();
        server.start();
        server.blockUntilShutdown();
    }


    // Implementation of the gRPC service on the server-side.
    private class RailsimFactory extends RailsimFactoryGrpc.RailsimFactoryImplBase {

        Map<Integer, Env2> envMap = new HashMap<>();

        @Override
        public void getEnvironment(GrpcPort grpcPort, StreamObserver<ConfirmationResponse> responseObserver) {
            //     Create an instance of the environment and store it in a map
            System.out.println("getEnvironment() -> Create env with id: "+grpcPort);

            // Send the reply back to the client.
            ConfirmationResponse.Builder confirmationResponseBuilder = ConfirmationResponse.newBuilder();
            confirmationResponseBuilder.setAck("OK");
            ConfirmationResponse response = confirmationResponseBuilder.build();
            responseObserver.onNext(response);
            responseObserver.onCompleted();

            Env2 env = new Env2(1, 2, true, grpcPort.getGrpcPort());
            // Store the environment created with it's key being the port
            this.envMap.put(grpcPort.getGrpcPort(), env);
        }

        @Override
        public void resetEnv(GrpcPort grpcPort, StreamObserver<ConfirmationResponse> responseObserver) {
            //     Start the Env2 simulation
            System.out.println("Reset env id: "+grpcPort);
            // Send the reply back to the client.
            ConfirmationResponse.Builder confirmationResponseBuilder = ConfirmationResponse.newBuilder();
            confirmationResponseBuilder.setAck("OK");
            ConfirmationResponse response = confirmationResponseBuilder.build();

            responseObserver.onNext(response);

            // Indicate that no further messages will be sent to the client.
            responseObserver.onCompleted();
            Env2 env = this.envMap.get(grpcPort.getGrpcPort());

            try{
                env.reset();
            }
            catch (Exception e){
                System.err.println("Error happened while resetting the environment" + e);
            }
        }
    }

}
