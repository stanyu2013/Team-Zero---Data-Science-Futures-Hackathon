import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

import java.io.FileFilter;

import com.amazonaws.services.rekognition.AmazonRekognition;
import com.amazonaws.services.rekognition.AmazonRekognitionClientBuilder;
import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.rekognition.model.AmazonRekognitionException;
import com.amazonaws.services.rekognition.model.DetectLabelsRequest;
import com.amazonaws.services.rekognition.model.DetectLabelsResult;
import com.amazonaws.services.rekognition.model.DetectTextRequest;
import com.amazonaws.services.rekognition.model.DetectTextResult;
import com.amazonaws.services.rekognition.model.Image;
import com.amazonaws.services.rekognition.model.Label;
import com.amazonaws.services.rekognition.model.TextDetection;
import com.amazonaws.util.IOUtils;

public class DetectLabels
{
	public static class ImageFilenameFilter implements FileFilter {
		public boolean accept(File f) {
			String name = f.getName();
			return (name.endsWith(".png") || name.endsWith(".jpg") || name.endsWith(".gif"));
		}
	}
	
	public static void outputCsv(PrintStream out, File file, String type, String text, float confidence)
		throws Exception
	{
		String filename = file.getName();
		out.println(file.getAbsolutePath() + ", " +
				    filename + ", " +
				    type + ", " +
				    text + ", " +
				    confidence );
	}
	
    public static void main(String[] args) throws Exception {
    	
    	if (args.length == 0) {
    		System.err.println("Usage: DetectLabels <file>");
    		System.exit(1);;
    	}
    	
        AWSCredentials credentials;
        try {
            credentials = new ProfileCredentialsProvider("rekognitionClient").getCredentials();
        } catch (Exception e) {
            throw new AmazonClientException(
            		"Cannot load the credentials from the credential profiles file. "
                    + "Please make sure that your credentials file is at the correct "
                    + "location (.aws/credentials), and is in a valid format.", e);
        }

        AmazonRekognition rekognitionClient = AmazonRekognitionClientBuilder
          		.standard()
          		.withRegion(Regions.US_EAST_1)
        		.withCredentials(new AWSStaticCredentialsProvider(credentials))
        		.build();
        
        HashMap<String,Label> allLabels = new HashMap<String,Label>();
        HashMap<String,TextDetection> allText = new HashMap<String,TextDetection>();
        final String LABEL = "LABEL";
        final String TEXT  = "TEXT";
        
        // Populate allFiles list with photo files
        ArrayList<File> allFiles = new ArrayList<File>();
        File firstFile = new File(args[0]);
        boolean processingDirectory = firstFile.isDirectory(); 
        if (processingDirectory) {
    		FileFilter filter = new ImageFilenameFilter();
    		File files[] = firstFile.listFiles(filter);
    		for (File fileInDir : files) {
    			allFiles.add(fileInDir);
    		}        	
        }
        else {
    		allFiles.add(firstFile);        	
        }
        
        File detailFile = null;
        File summaryFile = null;
        PrintStream detailOut = null;
        PrintStream summaryOut = null;
        if (processingDirectory) {
        	detailFile = new File(firstFile, "recognition_detail.csv");
        	detailOut = new PrintStream(new BufferedOutputStream(new FileOutputStream(detailFile)));        	
        	summaryFile = new File(firstFile, "recognition_summary.csv");
        	summaryOut = new PrintStream(new BufferedOutputStream(new FileOutputStream(summaryFile)));
        }
        
        for (File photo : allFiles) {
        	System.err.println("Processing: " + photo);
        	// System.out.println("Processing: " + photo);

        	ByteBuffer imageBytes;
            InputStream inputStream = null;
            try {
            	inputStream = new FileInputStream(photo);
                imageBytes = ByteBuffer.wrap(IOUtils.toByteArray(inputStream));
            }
            finally {
            	if (inputStream != null) inputStream.close();
            }

            DetectLabelsRequest labelsRequest = new DetectLabelsRequest()
                    .withImage(new Image()
                            .withBytes(imageBytes))
                    .withMaxLabels(10)
                    .withMinConfidence(75F);

            try {
                DetectLabelsResult result = rekognitionClient.detectLabels(labelsRequest);
                List <Label> labels = result.getLabels();
                System.err.println("  Num Labels Found:" + labels.size());
                for (Label label : labels) {
                	// System.out.println("  " + label.getName());
                	allLabels.put(label.getName(), label);
                	outputCsv(detailOut, photo, LABEL, label.getName(), label.getConfidence());
                }
                
            } catch (AmazonRekognitionException e) {
                e.printStackTrace();
            }

        
            DetectTextRequest request = new DetectTextRequest()
                    .withImage(new Image()
                            .withBytes(imageBytes));
            		
            try {
                DetectTextResult result = rekognitionClient.detectText(request);
                List<TextDetection> textDetections = result.getTextDetections();
                int confidentTextCount = 0;
	            for (TextDetection text: textDetections)
	            {
	            	if ((text.getConfidence() > 75.0f) && (text.getDetectedText().length() > 2)) {
		            	allText.put(text.getDetectedText(), text);
		            	outputCsv(detailOut, photo, TEXT, text.getDetectedText(), text.getConfidence());
		            	confidentTextCount++;
	            	}
	            }
                System.err.println("  Num Text Found:" + confidentTextCount);
            }
	        catch (AmazonRekognitionException e) {
	            e.printStackTrace();
	        }
        }
        
        for (String key: allLabels.keySet()) {
        	Label label = allLabels.get(key);
        	// System.out.println(label);
        	outputCsv(summaryOut, firstFile, LABEL, label.getName(), label.getConfidence());
        }
        
        for (String key: allText.keySet()) {
        	TextDetection text = allText.get(key);
        	// System.out.println(text);
        	outputCsv(summaryOut, firstFile, TEXT, text.getDetectedText(), text.getConfidence());
        }
        
        detailOut.close();
        summaryOut.close();
    }
    
    /**
     * Resizes an image using a Graphics2D object backed by a BufferedImage.
     * @param srcImg - source image to scale
     * @param w - desired width
     * @param h - desired height
     * @return - the new resized image
     */
    public static java.awt.Image getScaledImage(java.awt.Image srcImg, int w, int h){
    	if (srcImg.getWidth(null) > srcImg.getHeight(null)) {
    		float scale = (float)w / (float)srcImg.getWidth(null);
    		h = Math.round(srcImg.getHeight(null) * scale);
    	}
    	else {
    		float scale = (float)h / (float)srcImg.getHeight(null);
    		w = Math.round(srcImg.getWidth(null) * scale);
    	}
        BufferedImage resizedImg = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = resizedImg.createGraphics();
        g2.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2.drawImage(srcImg, 0, 0, w, h, null);
        g2.dispose();
        return resizedImg;
    }
    

}