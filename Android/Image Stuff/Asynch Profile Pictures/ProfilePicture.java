/*

ADDD   YOUR PACKAGE HERE

*/

import android.os.AsyncTask;
import android.widget.ImageView;
import android.graphics.BitmapFactory;
import android.graphics.Bitmap;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import android.util.Log;
import java.util.Base64;
import org.apache.commons.io.IOUtils;


public class ProfilePicture {

    static URL DEFAULT_PFP_URL;
    static int MIN_HEIGHT = 128;
    static int MIN_WIDTH = 128;

    private String imageServerUrl = "http://35.196.41.87:443/get_pfp";
    private String jsonRequestData = "";

    private int owner_id;
    private int target_id;
    private int session_id;

    static {
        try {
            DEFAULT_PFP_URL = new URL("https://cdn.discordapp.com/attachments/172784982882779136/516567510968041472/yukari.jpg");
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
    }

    ImageView display;
    Bitmap bitmap;
    ImageConnectionAPI connection;

    public ProfilePicture( ImageView display, int owner_id, int target_id, int session_id) throws MalformedURLException {

        this.display = display;
        this.owner_id = owner_id;
        this.target_id = target_id;
        this.session_id = session_id;

        jsonRequestData = "{\"user_id\":" + ((Integer)owner_id).toString() + ",\"target_id\":" + ((Integer)target_id).toString()
                + ",\"session_id\":" + ((Integer)session_id).toString() + "}";
        
        loadDefaultPfp();
        connection = new ImageConnectionAPI( this);
        connection.execute( imageServerUrl, jsonRequestData);
    }

    private void loadDefaultPfp(){
        try {
            HttpURLConnection connection = (HttpURLConnection)DEFAULT_PFP_URL.openConnection() ;
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            Bitmap pre =  BitmapFactory.decodeStream(input);

            Bitmap scaledBmp = scale(pre);
            bitmap = scaledBmp;
            display.setImageBitmap(bitmap);


        } catch (IOException e) {
            Log.w("Bitmap","cant load the default picture");
            e.printStackTrace();
        }

    }

    private Bitmap scale( Bitmap original){
        return Bitmap.createScaledBitmap( original, MIN_WIDTH, MIN_HEIGHT, false);
    }

    private Bitmap byteArrayToBitmap( byte[] bytes ){
        Bitmap bmp = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
        return bmp;
    }

    public void synch(){
        if(connection.getStatus() == AsyncTask.Status.FINISHED)
        {
            connection.execute( imageServerUrl, jsonRequestData);
        }
    }

    public void interpretBitmapStringResponse( InputStream strm){
        byte[] bytes = new byte[0];
        try {
            String result64= IOUtils.toString(strm, "ISO-8859-1");
            bytes = Base64.getDecoder().decode(result64.getBytes());

        } catch (IOException e) {
            Log.w("Bitmap","Profile Picture cant decode the base64 string");
            try {
                strm.close();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            return;
        }

        Bitmap bmp = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);

        if(bmp == null){
            Log.w("Bitmap","Profile Picture cant create a Bitmap from the base64 string");
            try {
                strm.close();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            return;
        }

        bitmap = bmp;
        display.setImageBitmap(bitmap);
        display.invalidate();
        try {
            strm.close();
        } catch (IOException e1) {
            e1.printStackTrace();
        }
    }


}