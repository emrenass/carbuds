package com.example.magus.bitmapconverter;

import android.graphics.Bitmap;
import android.util.Log;
public class MyCustomPFPSetListener implements IAsynchProfileSetterListener {

    // AN EXAMPLE CLASS RUNNING ON ASYNCH SETTER
    Bitmap result;


    boolean rr;

    public MyCustomPFPSetListener() {
        rr =false;
    }

    public void execute(Bitmap bitmap){
        rr = false;
        result = null;
        final IAsynchProfileSetterListener ias = this;
        final Bitmap runnableBitmap = bitmap;
        Thread t = new Thread() {
            public void run() {
                PFPSetActivity pfpSet = new PFPSetActivity( 7357 , 0, runnableBitmap, ias) ;
            }
        };
        t.run();
    }

    @Override
    public void PFPSetFinished(Bitmap bmp) {
        Log.e("Bitmap", "POST");
        result = bmp;
        rr = true;
    }

    public boolean isResultReady(){
        return rr;
    }

    public Bitmap getResult(){
        if( isResultReady()) return result;
        else return null;
    }
}
