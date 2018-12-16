package com.ali.cs491.carbuds;

import android.util.Log;

import com.google.android.gms.common.util.IOUtils;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Connection {
    public static final String SIGNUP="signup";
    public static final String LOGIN="login";
    public static final String SET_TRIP_DRIVER = "set_trip_driver";
    public static final String SET_TRIP_HITCHHIKER = "set_trip_hitchhiker";
    public static final String INITIAL_DRIVER_PROFILE_SETUP = "initial_driver_profile_setup";
    public static final String INITIAL_HITCHIKER_PROFILE_SETUP = "initial_hitchhiker_profile_setup";
    public static final String UPDATE_DRIVER_PROFILE = "update_driver_profile";
    public static final String UPDATE_HITCHHIKER_PROFILE = "update_hitchhiker_profile";
    public static final String SWITCH_PROFILE = "switch_profile";
    public static final String GET_DRIVER_CANDIDATE = "get_driver_candidate";
    public static final String GET_HITCHHIKER_CANDIDATE = "get_hitchhiker_candidate";

    private String msg;
    public Connection(){
        msg = "";
    }
    public void setConnection(String type, JSONObject jsonObj){
        HttpURLConnection urlConnection = null;
        OutputStream out = null;
        try {
            URL url = new URL("http://35.205.45.78/" + type);
           // URL url = new URL("http://10.0.2.2:5000/"+ type);
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
            InputStream in = urlConnection.getInputStream();
            InputStreamReader inputStreamReader = new InputStreamReader(in);

            int inputStreamData = inputStreamReader.read();
            msg = "";
            while (inputStreamData != -1) {
                char currentData = (char) inputStreamData;
                inputStreamData = inputStreamReader.read();
                msg += currentData;
            }
            System.out.println("ok");
            Log.i("Carbuds - msg",msg);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            try {
                Log.i("Carbuds", urlConnection.getResponseMessage());
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            Log.i("Carbuds","exception");
        }
    }
    public String getResponseMessage(){
        return msg;
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
