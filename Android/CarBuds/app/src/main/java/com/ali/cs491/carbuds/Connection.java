package com.ali.cs491.carbuds;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class Connection {
    public static final String SIGNUP="signup";
    public static final String LOGIN="login";
    private String responseMessage;
    public Connection(){
    }
    public void setConnection(String type, JSONObject jsonObj){
        HttpURLConnection urlConnection;
        OutputStream out = null;
        try {
           // URL url = new URL("http://35.205.45.78:5053/" + type);
              URL url = new URL("http://10.0.2.2:5000/signup");
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod("POST");
            urlConnection.setRequestProperty("Content-Type","application/json");

            urlConnection.setDoOutput(true);
            out = new BufferedOutputStream(urlConnection.getOutputStream());
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
            writer.write(jsonObj.toString());
            writer.flush();
            writer.close();
            out.close();
            urlConnection.connect();
            responseMessage = urlConnection.getResponseMessage();
            Log.i("Carbuds" , responseMessage);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            Log.i("Carbuds","exception");
        }
    }
    public String getResponseMessage(){
        return responseMessage;
    }
    /*
    HttpURLConnection urlConnection;
            try {
        URL url = new URL("http://35.205.45.78:5053/signup");
        //  URL url = new URL("http://10.42.0.221:5000/signup");

        urlConnection = (HttpURLConnection) url.openConnection();
        urlConnection.setRequestMethod("POST");
        urlConnection.setRequestProperty("Content-Type","application/json");

        urlConnection.setDoOutput(true);
        out = new BufferedOutputStream(urlConnection.getOutputStream());
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
        writer.write(jsonObj.toString());
        writer.flush();
        writer.close();
        out.close();
        urlConnection.connect();
        Log.i("Carbuds" , urlConnection.getResponseMessage());
    } catch (Exception e) {
        System.out.println(e.getMessage());
        Log.i("Carbuds","exception");
    }*/
}
