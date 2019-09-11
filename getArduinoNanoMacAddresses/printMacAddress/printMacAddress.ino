#include <SPI.h>
#include <WiFiNINA.h>

char ssid[] = "yourNetwork";     // the name of your network
int status = WL_IDLE_STATUS;     // the Wifi radio's status

byte mac[6];                     // the MAC address of your Wifi Module


void setup(){
 Serial.begin(9600);
 while (!Serial){
 }
  WiFi.macAddress(mac);
}

void loop () {
  Serial.print(mac[5],HEX);
  Serial.print(":");
  Serial.print(mac[4],HEX);
  Serial.print(":");
  Serial.print(mac[3],HEX);
  Serial.print(":");
  Serial.print(mac[2],HEX);
  Serial.print(":");
  Serial.print(mac[1],HEX);
  Serial.print(":");
  Serial.println(mac[0],HEX);

  delay (1000);
  }
