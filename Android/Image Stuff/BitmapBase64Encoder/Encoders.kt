import java.util.Base64;
import java.io.ByteArrayOutputStream;


    @JvmField var MinHeight = 128
    @JvmField var MinWidth = 128
    
    fun convertToByteArray( bmp : Bitmap): ByteArray {

        /*
        !!!! TO PASS THE BMP; bmp = intent.getExtras().get("data"); < - use something like
         this to handle the response from the file system, before passing it to here
         dialogs should return as such
        */
        //scale the Bitmap for standardization
        val scaledBmp = Bitmap.createScaledBitmap( bmp, MinWidth, MinHeight, false);
        val stream : ByteArrayOutputStream
        val bytes : ByteArray

        stream = ByteArrayOutputStream()

        //turn it into PNG for standardization
        scaledBmp.compress(Bitmap.CompressFormat.PNG, 0, stream)

        bytes = stream.toByteArray()

        //release the bitmap
        scaledBmp.recycle();

        return bytes
    }

    fun convertToBase64( bytes : ByteArray): String{
        return Base64.getEncoder().encodeToString(bytes)
    }