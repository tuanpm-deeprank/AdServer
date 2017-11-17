import java.util.ArrayList;

import vn.adtech.nlp.ner.VCNER;

public class UETSegmentResponse {

	private String UETSegmentResponse = "";
	
	private String modelsPath = "/home/tuanpm/Desktop/AdProject/py4j/models";
	private vn.edu.vnu.uet.nlp.segmenter.UETSegmenter segmenter = new vn.edu.vnu.uet.nlp.segmenter.UETSegmenter(modelsPath);
	VCNER app = new VCNER("ner-model-vi.ser.gz");
	public String getUETSegmentResponse() {
		return UETSegmentResponse;
	}

	public void setUETSegmentResponse(String uETSegmentResponse) {
		UETSegmentResponse = uETSegmentResponse;
	}
	
	public ArrayList<String> NerExecute(){
		ArrayList<String> response = null;
		try{
			String t = app.NERDetection(UETSegmentResponse);
			NERRules ner = new NERRules();
			response = ner.getAllUniqueNamedEntities(t);
			for (String s: response) {
	    			System.out.println(s);
			}
		}catch(Exception e) {
			e.printStackTrace();
		}
		return response;
	}
	
	public String execute() {
		String response = segmenter.segmentTokenizedText(UETSegmentResponse);
		System.out.println(response);
		return response;
	}

}
