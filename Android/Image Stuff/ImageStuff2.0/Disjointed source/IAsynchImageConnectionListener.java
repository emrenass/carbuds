package com.example.magus.bitmapconverter;

import java.io.InputStream;

public interface IAsynchImageConnectionListener{
    public void interpretBitmapStringResponse( InputStream strm);
}
