package assign07;

import static org.junit.Assert.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.junit.Before;
import org.junit.Test;

import com.gradescope.jh61b.grader.GradedTest;

public class GraphUtilityPreTester {
	
	private ArrayList<String> strSources, strDests;
	private ArrayList<Integer> intSources, intDests;

	@Before
	public void setUp() throws Exception {
		strSources = new ArrayList<String>();
		strDests = new ArrayList<String>();
		intSources = new ArrayList<Integer>();
		intDests = new ArrayList<Integer>();		
	}
	
	@Test
    @GradedTest(name="expects examplegraph5.dot is acyclic", max_score=1, visibility="visible")
	public void testIsCyclicFalse() {
		buildListsFromDot("src/assign07/examplegraph5.dot", strSources, strDests);
		assertFalse(GraphUtility.isCyclic(strSources, strDests));
	}
	
	@Test
    @GradedTest(name="expects examplegraph10.dot is cyclic", max_score=1, visibility="visible")
	public void testIsCyclicTrue() {
		buildListsFromDot("src/assign07/examplegraph10.dot", strSources, strDests);
		assertTrue(GraphUtility.isCyclic(strSources, strDests));
	}
	
	@Test(expected = IllegalArgumentException.class)
    @GradedTest(name="expects exception when vertex with data1 not in graph", max_score=1, visibility="visible")
	public void testAreConnectedException() {
		intSources.add(1);
		intDests.add(2);
		GraphUtility.areConnected(intSources, intDests, 3, 2);
	}
	
	@Test
    @GradedTest(name="expects there is no path from vertex 2 to vertex 1 in examplegraph.dot", max_score=1, visibility="visible")
	public void testAreConnected() {
		buildListsFromDot("src/assign07/examplegraph.dot", strSources, strDests);
		assertFalse(GraphUtility.areConnected(strSources, strDests, "vertex 2", "vertex 1"));
	}
	
	@Test(expected = IllegalArgumentException.class)
    @GradedTest(name="expects exception when graph is cyclic", max_score=1, visibility="visible")
	public void testSortException() {
		strSources.add("dog");
		strDests.add("cat");
		strSources.add("cat");
		strDests.add("dog");		
		GraphUtility.sort(strSources, strDests);
	}
	
	@Test
    @GradedTest(name="expects the ordering examplegraph5.dot is 1, 2, 3, 4, 5", max_score=1, visibility="visible")
	public void testSort() {
		buildListsFromDot("src/assign07/examplegraph5.dot", strSources, strDests);
		List<String> actual = GraphUtility.sort(strSources, strDests);
		assertEquals(5, actual.size());
		for(int i = 1; i <= 5; i++)
			assertEquals(i + "", actual.get(i - 1));
	}

	private static void buildListsFromDot(String filename, ArrayList<String> sources, ArrayList<String> destinations) {
		
		Scanner scan = null;
		try {
			scan = new Scanner(new File(filename));
		}
		catch(FileNotFoundException e) {
			System.out.println(e.getMessage());
			System.exit(0);
		}

		scan.useDelimiter(";|\n");

		// Determine if graph is directed (i.e., look for "digraph id {").
		String line = "", edgeOp = "";
		while(scan.hasNext()) {
			line = scan.next();

			// Skip //-style comments.
			line = line.replaceFirst("//.*", "");

			if(line.indexOf("digraph") >= 0) {
				edgeOp = "->";
				line = line.replaceFirst(".*\\{", "");
				break;
			}
		}
		if(edgeOp.equals("")) {
			System.out.println("DOT graph must be directed (i.e., digraph).");
			scan.close();
			System.exit(0);

		}
		
		// Look for edge operator -> and determine the source and destination
		// vertices for each edge.
		while(scan.hasNext()) {
			String[] substring = line.split(edgeOp);

			for(int i = 0; i < substring.length - 1; i += 2) {
				// remove " and trim whitespace from node string on the left
				String vertex1 = substring[0].replace("\"", "").trim();
				// if string is empty, try again
				if(vertex1.equals(""))
					continue;

				// do the same for the node string on the right
				String vertex2 = substring[1].replace("\"", "").trim();
				if(vertex2.equals(""))
					continue;

				// indicate edge between vertex1 and vertex2
				sources.add(vertex1);
				destinations.add(vertex2);
			}

			// do until the "}" has been read
			if(substring[substring.length - 1].indexOf("}") >= 0)
				break;

			line = scan.next();

			// Skip //-style comments.
			line = line.replaceFirst("//.*", "");
		}

		scan.close();
	}
}