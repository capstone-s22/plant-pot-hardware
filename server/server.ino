#include <WiFi.h>
#include <WebServer.h>

const char* POT_ID = "0001";

/*Put your SSID & Password*/
const char* ssid = "Redmi";  // Enter SSID here
const char* password = "youshanhotspot";  //Enter Password here

WebServer server(80);

void setup() {
  Serial.begin(115200);
  Serial.println("Connecting to ");
  Serial.println(ssid);

  //connect to your local wi-fi network
  WiFi.begin(ssid, password);

  //check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());

  server.on("/", handle_OnConnect);
  server.onNotFound(handle_NotFound);

  server.begin();
  Serial.println("HTTP server started");
}
void loop() {
  server.handleClient();
}

void handle_OnConnect() {
  Serial.println("Received");
  server.send(200, "text/plain", POT_ID); 
}

void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
}

