package com.ali.cs491.carbuds;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.ArrayList;

public class MatchmakingActivity extends AppCompatActivity {
    private static ImageView imageView;
    private static ArrayList<Profile> profiles;
    private static int profileIndex;
    private SendRouteTask task;
    private void getProfiles(){
        profiles = new ArrayList<Profile>();
        //todo: delete this part after connecting server
        Profile temp;
        profiles.add(new Profile("Ali Osman", R.drawable.image_green));
        profiles.add(new Profile("Ali Osman", R.drawable.common_google_signin_btn_icon_dark));
        profiles.add(new Profile("Ali Osman", R.drawable.common_google_signin_btn_icon_light_normal_background));
        profileIndex =0;
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        task = new SendRouteTask();
        task.execute((Void) null);
        getProfiles();
        setContentView(R.layout.activity_matchmaking);
        imageView = (ImageView) findViewById(R.id.imageView);
        imageView.setImageResource(R.drawable.green);
        Button no = findViewById(R.id.noButton);
        no.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (profileIndex != profiles.size()-1) {
                    profileIndex++;
                } else {
                    profileIndex = 0;
                }
                if (profiles.size()!=0 ) {
                    imageView.setImageResource(profiles.get(profileIndex).getImageID());
                }
            }
        });
    }


    private void sendRoute(){
        Trip trip = RouteManager.getTrip();
        JSONObject jsonObj = new JSONObject();

        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date date = new Date();
        Connection connection = new Connection();
        System.out.println(formatter.format(date));
        try {
            jsonObj.put("token", LoginActivity.token );
            jsonObj.put("user_id", "2"); // get id
            jsonObj.put("trip_start_point", RouteManager.getPointString(trip.getStartPoint()));
            jsonObj.put("trip_end_point", RouteManager.getPointString(trip.getEndPoint()));
            jsonObj.put("trip_start_time", formatter.format(date));
            if(trip.getUserType() == RouteManager.DRIVER) {
                jsonObj.put("available_seat", "2");
                connection.setConnection(Connection.SET_TRIP_DRIVER, jsonObj);
                connection.getResponseMessage();
            } else {
                connection.setConnection(Connection.SET_TRIP_HITCHHIKER,jsonObj);
                connection.getResponseMessage();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    public class SendRouteTask extends AsyncTask<Void, Void, Boolean> {

        @Override
        protected Boolean doInBackground(Void... voids) {
            sendRoute();
            return null;
        }
    }

}
