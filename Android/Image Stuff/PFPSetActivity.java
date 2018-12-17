package com.example.magus.bitmapconverter;

import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.util.Log;
import org.apache.commons.io.IOUtils;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;


public class PFPSetActivity {

    SetPfpConnectionAPI slave;

    int owner_id;
    int session_id;

    Bitmap bitmap;
    String bitmap_string;
    private String imageServerUrlSet = "http://35.196.41.87:443/set_pfp";
    private String jsonRequestDataSet = "";



    Bitmap result;

    public PFPSetActivity( int user_id, int session_id, Bitmap bmp){
        this.owner_id = user_id;
        this.session_id = session_id;
        bitmap = bmp;
        Encoder encoder = new Encoder();
        bitmap_string = encoder.convertToBase64(encoder.convertToByteArray( bmp));

        jsonRequestDataSet = "{\"user_id\":" + ((Integer)owner_id).toString()
                + ",\"session_id\":" + ((Integer)session_id).toString()
                + ",\"bitmap\":\"" + bitmap_string + "\"}";

        slave = new SetPfpConnectionAPI(this);

        this.owner_id = owner_id;

    }

    //FOR THE UI ELEMENT ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    //EXTREMELY IMPORTANT
    public void notify_the_watcher(){
        //TODO you need to add the main form as a watcher to notify it here
        Bitmap result;
    }

    public void execute(){
        request_pfp_set();
    }
    public void request_pfp_set(){
        slave.execute( imageServerUrlSet, jsonRequestDataSet);

    }

    public void set_server_responded(InputStream result){
        String resultString ="";
        try {
            resultString= IOUtils.toString(result, "UTF-8");
        } catch (IOException e) {
            e.printStackTrace();
        }
        if( resultString.equals("")){
            Log.e("Bitmap", "PFPSetActivity.set_server_responded response is empty, and shouldn't be");
            this.result = null;
            notify_the_watcher();
            try {
                result.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else if( resultString.equals("0")){
            //success
            this.result = bitmap;
            notify_the_watcher();

            try {
                result.close();
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
        else{
            //TODO do accordingly for other cases
            this.result = null;
            notify_the_watcher();
            try {
                result.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    // can be called to check BUT NEVER it should be done in a locking loop inside the main thread
    public boolean isExecutionFinalized(){
        if(slave.getStatus() == AsyncTask.Status.RUNNING || slave.getStatus()== AsyncTask.Status.PENDING )
        {
            return false;
        }

        return true;
    }

    public class SetPfpConnectionAPI extends AsyncTask< String, String, InputStream> {

        PFPSetActivity master;
        public SetPfpConnectionAPI( PFPSetActivity pfpSetActivity) {
            //set default image at display
            master = pfpSetActivity;
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
                Log.e("Bitmap", "Set Profile Invalid Json");
                e.printStackTrace();
            }


            try {

                URL url = new URL(urlString);

                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();

                urlConnection.setRequestMethod("POST");
                urlConnection.setRequestProperty("Content-Type", "application/json");
                urlConnection.setRequestProperty("Accept", "*/*");
                //urlConnection.setConnectTimeout(2000);
                urlConnection.setDoOutput(true);
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(urlConnection.getOutputStream()));

                writer.write(jsonObj.toString());
                writer.close();
                urlConnection.connect();

                InputStream strm = urlConnection.getInputStream();
                urlConnection.disconnect();
                return strm;
            } catch (Exception e) {
                System.out.println(e.getMessage());
                return null;
            }

        }

        @Override
        protected void onPostExecute(InputStream result) {
            if( result == null){
                Log.e("Bitmap", "Connection Error");
                return;
            }
            master.set_server_responded( result);
        }
    }
}
