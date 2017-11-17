import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
//import org.apache.commons.lang.StringUtils;

public class NERRules {
	public static final String LOCATION_NEXT_WORD_REGEX = "(tỉnh|đường|ngõ|quận)\\s*(.*?)\\s";
	public static final String KEY_LOC = "LOC";
	public static final String KEY_PER = "PER";
	public static final String KEY_ORG = "ORG";
	public static final String KEY_PRO = "PRO";

	/**
	 * Detect NAME ENTITY using Rule
	 * 
	 * @param content
	 * @return
	 */
	public List<String> NextWordOfMatchedWord(String content) {
		List<String> listWords = new ArrayList<String>();
		Pattern p = Pattern.compile(LOCATION_NEXT_WORD_REGEX);
		Matcher m = p.matcher(content);

		while (m.find()) {
			listWords.add(m.group(1) + "\t" + m.group(2));
		}
		return listWords;
	}

	/**
	 * get Named Entities by label
	 * 
	 * @param content
	 * @param label
	 * @return
	 */
	public Map<String, List<String>> getNamedEntities(String content,
			String label) {
		Map<String, List<String>> mapOfNE = new HashMap<String, List<String>>();
		content = content.replace("\n", " ");
		content = content.replace("/O", "");
		String[] splits = content.split(" ");
		Set<String> setOfEntities = new HashSet<String>();
		for (int i = 0; i < splits.length; i++) {
			if (splits[i].contains("B-" + label)) {
				StringBuilder strORG = new StringBuilder();
				strORG.append(splits[i]).append(" ");
				for (int j = i + 1; j <= splits.length - 1; j++) {
					if (splits[j].contains("I-" + label) == true) {
						strORG.append(splits[j]).append(" ");
					} else {
						i = j - 1;
						break;
					}
				}

				String entity = strORG.toString().replace("/B-" + label, "")
						.replace("/I-" + label, "").trim();

				setOfEntities.add(entity);

			}
		}

		mapOfNE.put(label, new ArrayList<String>(setOfEntities));
		return mapOfNE;
	}
	
	//get entities with repeat
	public ArrayList<String> getAllNamedEntities(String content, String label) {
		ArrayList<String> entities = new ArrayList<String>();
		
		content = content.replace("\n", " ");
		content = content.replace("/O", "");
		String[] splits = content.split(" ");
		
		for (int i = 0; i < splits.length; i++) {
			if (splits[i].contains("B-" + label)) {
				StringBuilder strORG = new StringBuilder();
				strORG.append(splits[i].substring(0, splits[i].indexOf("B-" + label) + 5)).append(" ");
				for (int j = i + 1; j <= splits.length - 1; j++) {
					if (splits[j].contains("I-" + label) == true) {
						strORG.append(splits[j].substring(0, splits[j].indexOf("I-" + label) + 5)).append(" ");
					} else {
						i = j - 1;
						break;
					}
				}

				String entity = strORG.toString().replace("/B-" + label, "")
						.replace("/I-" + label, "").trim();

				entities.add(entity);
			}
		}
		
		return entities;
	}

        public ArrayList<String> getAllUniqueNamedEntities(String content) {
	    ArrayList<String> flag = new ArrayList<String>();
	    flag.add("PER");
	    flag.add("LOC");
	    flag.add("ORG");
	    flag.add("PRO");

	    ArrayList<String> temp1 = new ArrayList<String>();
            ArrayList<String> temp2 = new ArrayList<String>();
	    for (int flagIndex = 0; flagIndex < flag.size(); flagIndex++) {
		temp1 = getAllNamedEntities(content, flag.get(flagIndex));
		for(String d:temp1) {
       		    if (!temp2.contains(d)) {
		        temp2.add(d);
		    }
                }
	    }
	    return temp2;
	}


}
