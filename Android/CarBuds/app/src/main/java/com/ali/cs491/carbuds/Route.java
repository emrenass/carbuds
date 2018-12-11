package com.ali.cs491.carbuds;

import com.google.android.gms.maps.model.LatLng;

public class Route {
    private LatLng startPoint;
    private LatLng endPoint;
    public Route(LatLng startPoint, LatLng endPoint){
        this.startPoint = startPoint;
        this.endPoint   = endPoint;
    }

    public LatLng getStartPoint() {
        return startPoint;
    }

    public LatLng getEndPoint() {
        return endPoint;
    }
}
