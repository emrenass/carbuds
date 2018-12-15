package com.ali.cs491.carbuds;

import com.google.android.gms.maps.model.LatLng;

public class RouteManager {
    private static Route route;
    private static LatLng startPoint;
    private static LatLng endPoint;
    private static int userType;
    public static final int  DRIVER = 0;
    public static final int  HITCHHIKER = 1;

    public static void setUserType(int type){
        userType = type;
    }
    public static void setStartPoint(LatLng point){
        route = null;
        startPoint = point;
    }
    public static void setEndPoint(LatLng point){
        endPoint = point;
        route = new Route(startPoint, endPoint, userType);
        // todo: send route to server
    }
    public static Route getRoute(){
        return route;
    }
    public static String getPointString(LatLng point){
        return point.latitude + "," + point.longitude;
    }
}
