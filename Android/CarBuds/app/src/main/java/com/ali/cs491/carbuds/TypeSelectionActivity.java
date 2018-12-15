package com.ali.cs491.carbuds;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class TypeSelectionActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
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
}
