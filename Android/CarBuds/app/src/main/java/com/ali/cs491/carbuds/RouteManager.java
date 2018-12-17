package com.ali.cs491.carbuds;

import com.google.android.gms.maps.model.LatLng;

import java.util.Date;

public class RouteManager {
    private static Trip trip;
    private static LatLng startPoint;
    private static LatLng endPoint;
    private static int userType;
    private static Date date;
    public static final int  DRIVER = 0;
    public static final int  HITCHHIKER = 1;

    public static void setUserType(int type){
        userType = type;
    }
    public static void setStartPoint(LatLng point){
        trip = null;
        startPoint = point;
    }
    public static void setEndPoint(LatLng point){
        endPoint = point;

        // todo: send trip to server
    }
    public static void setDate(Date dt){
        date = dt;
        trip = new Trip(startPoint, endPoint, userType,date);
    }
    public static Trip getTrip(){
        return trip;
    }
    public static String getPointString(LatLng point){
        return String.format("%.6f",point.latitude) + "," + String.format("%.6f",point.longitude);
    }
}
