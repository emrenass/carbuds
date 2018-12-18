package com.example.magus.bitmapconverter;

import android.graphics.Bitmap;

import java.net.MalformedURLException;

public class MyCustomPFPGetListener implements IAsynchProfilePictureListener{

    //AN EXAMPLE CLASS RUNNING ON ASYNCH GETTER
    Bitmap bmp;// set @ pfp
    boolean isReady;
    boolean isDefReady;
    ProfilePictureNOGUI pfp;

    public MyCustomPFPGetListener(){
        isReady = false;
        isDefReady = false;
        try {
            pfp = new ProfilePictureNOGUI( this, 7357,7357, 0);

        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
    }

    public void reExecute(){
        isReady = false;
        pfp.synch();
    }

    public boolean isReady(){
        return isReady;
    }


    public Bitmap getBitmap(){
        if(isDefReady)
        return bmp;
        else return null;
    }

    //called from pfp YOU DO NOTHING BUT CONSTRUCTING THE PFP!!!
    //this is how you "GET" image
    //the initiator thread CANNOT receive the callback unless its IDLE
    //you CANT WAIT for it to finish from the initiator thread
    @Override
    public void setImageBitmap(Bitmap bitmap) {
        bmp = bitmap;
        isReady = true;
    }

    @Override
    public void setDefault(Bitmap bitmap) {
        isDefReady = true;
        bmp = bitmap;
    }
}
