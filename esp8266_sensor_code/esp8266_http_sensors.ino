#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <DHT.h>

#ifndef STASSID
#define STASSID "DESKTOP-9433016 5225"
#define STAPSK "11111111"
#endif

// Configuration WiFi
const char* ssid = STASSID;
const char* password = STAPSK;

// Configuration du serveur Django
const char* serverUrl = "http://192.168.137.1:8080/api/sensor-data/";  // Adresse IP du partage de connexion Windows

// Configuration des capteurs
#define DHTPIN D4          // Pin du capteur DHT
#define DHTTYPE DHT22      // Type de capteur DHT (DHT22 ou DHT11)
#define LDR_PIN A0         // Pin du capteur de luminosité (LDR)

DHT dht(DHTPIN, DHTTYPE);
WiFiClient wifiClient;
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  
  // Initialisation du capteur DHT
  dht.begin();
  
  // Connexion au WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connexion au WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connecté !");
  Serial.print("Adresse IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  sendSensorData();
  handleClientRequest();
  delay(5000);
}

void sendSensorData() {
  if (WiFi.status() == WL_CONNECTED) {
    // Lecture des capteurs
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int luminosity = analogRead(LDR_PIN);
    unsigned long uptime = millis() / 1000;

    // Vérification des valeurs
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Erreur de lecture du capteur DHT!");
      return;
    }

    HTTPClient http;
    http.begin(wifiClient, serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Construction du JSON
    String jsonPayload = "{\"temperature\": " + String(temperature, 1) + 
                        ", \"humidity\": " + String(humidity, 1) + 
                        ", \"luminosity\": " + String(luminosity) + 
                        ", \"uptime\": " + String(uptime) + "}";

    Serial.println("Envoi des données: " + jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse HTTP: " + String(httpResponseCode));
      Serial.println("Réponse: " + response);
    } else {
      Serial.println("Erreur d'envoi: " + String(httpResponseCode));
    }

    http.end();
  } else {
    Serial.println("WiFi déconnecté!");
  }
}

void handleClientRequest() {
  WiFiClient client = server.available();
  if (!client) return;

  Serial.println("Client connecté!");
  while (client.connected() && !client.available()) delay(1);

  String req = client.readStringUntil('\r');
  client.flush();

  // Lecture des capteurs pour la page web
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int luminosity = analogRead(LDR_PIN);
  
  String response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                   "<!DOCTYPE HTML><html><head>"
                   "<meta charset='utf-8'>"
                   "<meta http-equiv='refresh' content='5'>"
                   "<style>body{font-family:Arial;margin:20px;}</style>"
                   "</head><body>"
                   "<h2>Serre Agricole Connectée</h2>";
  
  if (!isnan(temperature) && !isnan(humidity)) {
    response += "<p>Température: " + String(temperature, 1) + "°C</p>"
                "<p>Humidité: " + String(humidity, 1) + "%</p>";
  } else {
    response += "<p>Erreur de lecture DHT</p>";
  }
  
  response += "<p>Luminosité: " + String(luminosity) + " lx</p>"
              "<p>Uptime: " + String(millis() / 1000) + " sec</p>"
              "</body></html>";

  client.print(response);
  client.stop();
}
