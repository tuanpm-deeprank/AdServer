import py4j.GatewayServer;

public class UETSegmenterExecute {
	
	private UETSegmentResponse response;

	
	public UETSegmentResponse getResponse() {
		return response;
	}

	public UETSegmenterExecute() {
		response = new UETSegmentResponse();
	}

	public static void main(String[] args) {
		GatewayServer gatewayServer = new GatewayServer(new UETSegmenterExecute());
		gatewayServer.start();
		System.out.println("Gateway started!!!!!!!!!!!!");
	}

}
