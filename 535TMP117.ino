#include <TimeLib.h>
#include <Wire.h>
#include <SparkFun_TMP117.h>

TMP117 sensor; // Initalize sensor
#define TIME_MSG_LEN 11 // time sync to PC is HEADER followed by Unix time_t as ten ASCII digits
#define TIME_HEADER 'T' // Header tag for serial time sync message
#define TIME_REQUEST 7 // ASCII bell character requests a time sync message
//#define DEFAULT_TIME 1357041600 //Jan 1st 2013

void setup() {
  Wire.begin();
  Serial.begin(115200);    // Start serial communication at 115200 baud
  // put your setup code here, to run once:
  Wire.setClock(400000);   // Set clock speed to be the fastest for better communication (fast mode)

  setTime(1357041600);

  //Serial.println("TMP117 Example 1: Basic Readings");
  if (sensor.begin() == true){ // Function to check if the sensor will correctly self-identify with the proper Device ID/Address
    //Serial.println("Begin");
  }
  else{
    Serial.println("Device failed to setup- Freezing code.");
    while (1); // Runs forever
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    processSyncMessage();
  }
  if (timeStatus() == timeNotSet)
    Serial.println("waiting for sync message");
  else{
    if (sensor.dataReady() == true){ // Function to make sure that there is data ready to be printed, only prints temperature values when data is ready
      float tempC = sensor.readTempC();
      float tempF = sensor.readTempF();
      // Print temperature in °C and °F
      /*
      Serial.println(); // Create a white space for easier viewing
      Serial.print("Temperature in Celsius: ");
      Serial.println(tempC);
      Serial.print("Temperature in Fahrenheit: ");
      Serial.println(tempF);
      */  
      time_t t = now();
      float h = hour();
      float m = minute();
      float s = second();
      float curr = now();
      String tmpC = "";
      tmpC.concat(tempC);
      float sum = s+curr;
      Serial.println(tmpC + "#" + sum);
      delay(500); // Delay added for easier readings
    }
    /*
    if (Serial.available()){
      processSyncMessage();
    }*/
  }
}

void processSyncMessage(){
  // if time sync available from serial port, update time and return true
  unsigned long pctime;
  if(Serial.find(TIME_HEADER)) {
     pctime = Serial.parseInt();
     if( pctime >= 1357041600) { // check the integer is a valid time (greater than Jan 1 2013)
       setTime(pctime); // Sync Arduino clock to the time received on the serial port
     }
  }
}
