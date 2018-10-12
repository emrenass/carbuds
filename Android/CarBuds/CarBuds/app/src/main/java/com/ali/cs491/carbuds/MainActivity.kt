package com.ali.cs491.carbuds

import android.content.Intent
import android.graphics.Color
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        loginButton.text = "Login"

        signupButton.text = "SignUp"

        loginButton.setOnClickListener {
            val intent = Intent(this, LoginActivity :: class.java )
            startActivity(intent)
        }
        signupButton.setOnClickListener {
            val intent = Intent(this, SignupActivity :: class.java )
            startActivity(intent)
        }
        loginButton.setBackgroundColor(Color.GREEN)
        signupButton.setBackgroundColor(Color.RED)
    }
}
