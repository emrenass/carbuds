package com.ali.cs491.carbuds;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import java.util.ArrayList;

public class MatchmakingActivity extends AppCompatActivity {
    private static ImageView imageView;
    private static ArrayList<Profile> profiles;
    private static int profileIndex;
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
}
