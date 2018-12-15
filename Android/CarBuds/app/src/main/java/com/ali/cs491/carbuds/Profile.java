package com.ali.cs491.carbuds;

import android.media.Image;

public class Profile {
    private String name;
    private Image image;
    private int imageID; // gecici
    public Profile(String name, int imageID){
        this.name = name;
        this.imageID = imageID;
    }

    public Image getImage() {
        return image;
    }

    public int getImageID() {
        return imageID;
    }
}
