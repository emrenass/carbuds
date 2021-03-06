package com.example.magus.bitmapconverter;

import android.os.AsyncTask;
import android.util.Log;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.OutputStream;
import java.net.URL;
import java.net.HttpURLConnection;
import 	java.io.BufferedWriter;
import 	java.io.OutputStreamWriter;
import java.io.InputStream;


public class ImageConnectionAPI extends AsyncTask< String, String, InputStream> {


    ProfilePicture pfp;
    public ImageConnectionAPI( ProfilePicture pfp) {
        //set default image at display
        this.pfp = pfp;

    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
    }

    @Override
    protected InputStream doInBackground(String... strings) {
        String urlString = strings[0]; // URL to call
        String data = strings[1]; //data to post
        JSONObject jsonObj = null;
        try {
             jsonObj= new JSONObject(data);
        } catch (JSONException e) {
            Log.e("Bitmap", "Profile Picture Invalid Json");
            e.printStackTrace();
        }


        try {

            URL url = new URL(urlString);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod("POST");
            urlConnection.setRequestProperty("Content-Type", "application/json");
            urlConnection.setRequestProperty("Accept", "*/*");
            urlConnection.setConnectTimeout(2000);
            urlConnection.setDoOutput(true);
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(urlConnection.getOutputStream()));
            writer.write(jsonObj.toString());
            writer.close();
            urlConnection.connect();
            InputStream strm;
            int statusCode = urlConnection.getResponseCode();
            if (statusCode >= 200 && statusCode < 400) {
                // Create an InputStream in order to extract the response object
                strm = urlConnection.getInputStream();
            }
            else {
                strm = urlConnection.getErrorStream();
                Log.e("Bitmap", "Error stream");
            }

            return strm;
        } catch (Exception e) {
            System.out.println(e.getMessage());
            return null;
        }

    }

    protected void onPostExecute(InputStream result) {
        if( result == null){
            Log.e("Bitmap", "Connection Error");
            return;
        }
        pfp.interpretBitmapStringResponse(result);
    }
}
