#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://127.0.0.1:5000/api/log";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void loop() {
  if (Serial.available()) {
    String received = Serial.readStringUntil('\n');

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverUrl);
      http.addHeader("Content-Type", "application/json");

      String payload = "{\"resident_name\":\"Resident A\",\"event_type\":\"uart_event\",\"status\":\"normal\",\"notes\":\"" + received + "\"}";
      http.POST(payload);
      http.end();
    }
  }
}
