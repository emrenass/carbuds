package com.ali.cs491.carbuds;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnSuccessListener;

import java.util.List;

public class StartSelectionActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private Marker startMarker;
    private Marker endMarker;
    private FusedLocationProviderClient mFusedLocationClient;
    private boolean First = false;
    private Button searchButton;
    private TextView searchBar;
    private double home_long,home_lat;
    private LatLng latLng;
    private String addressText,addMarker;
    private MarkerOptions markerOptions;

    protected void search(List<Address> addresses) {

        Address address = (Address) addresses.get(0);
        home_long = address.getLongitude();
        home_lat = address.getLatitude();
        latLng = new LatLng(address.getLatitude(), address.getLongitude());

        addressText = String.format(
                "%s, %s",
                address.getMaxAddressLineIndex() > 0 ? address
                        .getAddressLine(0) : "", address.getCountryName());

        markerOptions = new MarkerOptions();

        markerOptions.position(latLng);
        markerOptions.title(addressText);

        mMap.clear();
        mMap.addMarker(markerOptions);
        mMap.moveCamera(CameraUpdateFactory.newLatLng(latLng));
        mMap.animateCamera(CameraUpdateFactory.zoomTo(15));
        //locationTv.setText("Latitude:" + address.getLatitude() + ", Longitude:"
          //      + address.getLongitude());


    }
    public void firstDone() {
        First = true;
        endMarker.setVisible(true);
      //  searchBar.setText("Select End Point");
        searchButton.setText("Done");
    }

    public boolean isFirstDone() {
        return First;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_selection);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        searchBar = findViewById(R.id.searchBar);
        searchBar.setCursorVisible(true);
      
        searchButton = findViewById(R.id.searchButton);

        searchButton.setText("Next");
        searchBar.setOnKeyListener(new View.OnKeyListener() {
            @Override
            public boolean onKey(View v, int keyCode, KeyEvent event) {
                // If the event is a key-down event on the "enter" button
                if ((keyCode == KeyEvent.KEYCODE_ENTER)) {
                    String g = searchBar.getText().toString();

                    Geocoder geocoder = new Geocoder(getBaseContext());
                    List<Address> addresses = null;

                    try {
                        // Getting a maximum of 3 Address that matches the input
                        // text
                        addresses = geocoder.getFromLocationName(g, 3);
                        if (addresses != null && !addresses.equals(""))
                            search(addresses);

                    } catch (Exception e) {

                    }
                    return true;
                }
                return false;
            }
        });
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if (isFirstDone()) {
                    RouteManager.setStartPoint(startMarker.getPosition());
                    RouteManager.setEndPoint(endMarker.getPosition());
                    Intent intent = new Intent(StartSelectionActivity.this, DatePickerActivity.class);
                    startActivity(intent);
                } else {
                    firstDone();
                }
            }
        });
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        LatLng konum = new LatLng(39.8698382, 32.7486015); // bilkent
        startMarker = mMap.addMarker(new MarkerOptions().position(konum).title("Start Point").draggable(true));
        endMarker = mMap.addMarker(new MarkerOptions().position(konum).title("End Point").draggable(true).icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN)));
        endMarker.setVisible(false);
        mMap.moveCamera(CameraUpdateFactory.newLatLng(konum));
        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(konum, 16.0f));
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {

            @Override
            public void onMapClick(LatLng latlng) {
                // TODO Auto-generated method stub
                if (isFirstDone()){
                    endMarker.setPosition(latlng);
                } else{
                    startMarker.setPosition(latlng);
                }
            }
        });
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            mFusedLocationClient.getLastLocation()
                    .addOnSuccessListener(this, new OnSuccessListener<Location>() {
                        @Override
                        public void onSuccess(Location location) {
                            // Got last known location. In some rare situations this can be null.
                            if (location != null) {
                                LatLng konum = new LatLng(location.getLatitude(), location.getLongitude());
                                startMarker = mMap.addMarker(new MarkerOptions().position(konum).title("Start Point").draggable(true));
                                endMarker = mMap.addMarker(new MarkerOptions().position(konum).title("End Point").draggable(true).icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN)));
                                endMarker.setVisible(false);
                             //   startMarker.showInfoWindow();
                            //    endMarker.showInfoWindow();
                                mMap.moveCamera(CameraUpdateFactory.newLatLng(konum));
                                mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(konum, 12.0f));
                                // Logic to handle location object
                            }
                        }
                    });
            return;
        }

    }
}
