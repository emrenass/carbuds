package com.ali.cs491.carbuds;

import com.google.android.gms.maps.model.LatLng;

public class Route {
    private LatLng startPoint;
    private LatLng endPoint;
    private  int userType;
    public Route(LatLng startPoint, LatLng endPoint, int userType){
        this.startPoint = startPoint;
        this.endPoint   = endPoint;
        this.userType   = userType;
    }

    public LatLng getStartPoint() {
        return startPoint;
    }

    public LatLng getEndPoint() {
        return endPoint;
    }

    public int getUserType() {
        return userType;
    }
}