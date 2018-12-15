package com.ali.cs491.carbuds;

import com.google.android.gms.maps.model.LatLng;

public class RouteManager {
    private static Route route;
    private static LatLng startPoint;
    private static LatLng endPoint;
    public static void setStartPoint(LatLng point){
        route = null;
        startPoint = point;
    }
    public static void setEndPoint(LatLng point){
        endPoint = point;
        route = new Route(startPoint,endPoint);
        // todo: send route to server
    }
}
