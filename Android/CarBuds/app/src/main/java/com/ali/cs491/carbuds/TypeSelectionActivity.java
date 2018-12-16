package com.ali.cs491.carbuds;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import org.json.JSONException;
import org.json.JSONObject;

public class TypeSelectionActivity extends AppCompatActivity {
    private Deneme task;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        task = new Deneme();
        task.execute((Void) null);
        setContentView(R.layout.activity_type_selection);
        Button carOwnerButton = findViewById(R.id.carOwnerButton);
        Button hitchhikerButton = findViewById(R.id.hitchhikerButton);
        Button settingsButton = findViewById(R.id.settingsButton);
        carOwnerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                RouteManager.setUserType(RouteManager.DRIVER);
                Intent intent = new Intent(TypeSelectionActivity.this, StartSelectionActivity.class);
                startActivity(intent);
            }
        });
        hitchhikerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                RouteManager.setUserType(RouteManager.HITCHHIKER);
                Intent intent = new Intent(TypeSelectionActivity.this, StartSelectionActivity.class);
                startActivity(intent);
            }
        });
        settingsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(TypeSelectionActivity.this, SettingsActivity.class);
                startActivity(intent);
            }
        });


    }
    private void getCandidate(String str, String id){
        JSONObject jsonObj = new JSONObject();
        Connection connection = new Connection();
        try {
            jsonObj.put("token", LoginActivity.token );
            jsonObj.put("user_id",id);
            connection.setConnection(str,jsonObj);
            connection.getResponseMessage();
        }catch (JSONException e) {
            e.printStackTrace();
        }
    }
    private void switchProfile(){
        JSONObject jsonObj = new JSONObject();
        Connection connection = new Connection();
        try {
            jsonObj.put("token", LoginActivity.token );
            jsonObj.put("user_id","2");
            connection.setConnection(Connection.SWITCH_PROFILE,jsonObj);
            connection.getResponseMessage();
        }catch (JSONException e) {
            e.printStackTrace();
        }
    }
    private void driverProfileSetup(){
        JSONObject jsonObj = new JSONObject();
        Connection connection = new Connection();
        try {
            jsonObj.put("token", LoginActivity.token );
            jsonObj.put("gender_preference","{Male, Female}"); // "{Male, Female}"
            jsonObj.put("music_preference", "{Electro, Pop, Rock}");
            jsonObj.put("passanger_seats","3");
            jsonObj.put("licence_plate","06 AOC 01");
            jsonObj.put("car_brand","BMW");
            jsonObj.put("car_model","320d");
            jsonObj.put("user_id","2");
           // connection.setConnection(Connection.INITIAL_DRIVER_PROFILE_SETUP,jsonObj);
            connection.setConnection(Connection.UPDATE_DRIVER_PROFILE,jsonObj);
            connection.getResponseMessage();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    private void hitchhikerProfileSetup(){
        JSONObject jsonObj = new JSONObject();
        Connection connection = new Connection();
        try{
            jsonObj.put("token", LoginActivity.token );
            jsonObj.put("gender_preference","{Male}"); // "{Male, Female}"
            jsonObj.put("music_preference", "{Electro, Rock, Rap}");
            jsonObj.put("user_id","2");
           // connection.setConnection(Connection.INITIAL_HITCHIKER_PROFILE_SETUP,jsonObj);
              connection.setConnection(Connection.UPDATE_HITCHHIKER_PROFILE,jsonObj);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    public class Deneme extends AsyncTask<Void, Void, Boolean> {

        @Override
        protected Boolean doInBackground(Void... voids) {
           // switchProfile();
          //  hitchhikerProfileSetup();
         //   getCandidate(Connection.GET_DRIVER_CANDIDATE, "14");
          //  getCandidate(Connection.GET_HITCHHIKER_CANDIDATE, "13");
            return null;
        }
    }

}
