package com.example.magus.bitmapconverter;

import android.graphics.Bitmap;

import java.io.ByteArrayOutputStream;
import java.util.Base64;

public class Encoder {


    static int MinHeight = 128;
    static int MinWidth = 128;

    public byte[] convertToByteArray( Bitmap bmp){

        /*
        !!!! TO PASS THE BMP; bmp = intent.getExtras().get("data"); < - use something like
         this to handle the response from the file system, before passing it to here
         dialogs should return as such
        */
        //scale the Bitmap for standardization
        Bitmap scaledBmp = Bitmap.createScaledBitmap( bmp, MinWidth, MinHeight, false);
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        byte[] bytes;


        //turn it into PNG for standardization
        scaledBmp.compress(Bitmap.CompressFormat.PNG, 0, stream);

        bytes = stream.toByteArray();

        //release the bitmap
        scaledBmp.recycle();

        return bytes;
    }

    public String convertToBase64( byte[] bytes){
        return Base64.getEncoder().encodeToString(bytes);
    }
}
