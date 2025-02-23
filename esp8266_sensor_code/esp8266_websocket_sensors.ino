#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// Configuration WiFi
const char* ssid = "VOTRE_SSID";
const char* password = "VOTRE_PASSWORD";

// Configuration WebSocket
const char* websocket_server = "192.168.1.X";  // Remplacez par l'IP de votre serveur Django
const int websocket_port = 8000;
const char* websocket_path = "/ws/sensors/";

// Configuration des capteurs
#define DHTPIN D4          // Pin du capteur DHT
#define DHTTYPE DHT22      // Type de capteur DHT (DHT22 ou DHT11)
#define LDR_PIN A0         // Pin du capteur de luminosité (LDR)

// Initialisation des objets
WebSocketsClient webSocket;
DHT dht(DHTPIN, DHTTYPE);

// Variables pour stocker les données des capteurs
float temperature = 0;
float humidity = 0;
int luminosity = 0;
bool isConnected = false;

// Variables pour la gestion du temps
unsigned long lastUpdate = 0;
const long updateInterval = 2000;  // Intervalle de mise à jour (2 secondes)

void setup() {
    // Initialisation de la communication série
    Serial.begin(115200);
    Serial.println("Démarrage...");

    // Initialisation du capteur DHT
    dht.begin();

    // Configuration de la LED intégrée
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);  // LED éteinte au démarrage

    // Connexion au WiFi
    WiFi.begin(ssid, password);
    Serial.print("Connexion au WiFi");
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("");
    Serial.println("WiFi connecté");
    Serial.println("Adresse IP: ");
    Serial.println(WiFi.localIP());

    // Configuration du WebSocket
    webSocket.begin(websocket_server, websocket_port, websocket_path);
    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(5000);
}

void loop() {
    webSocket.loop();

    unsigned long currentMillis = millis();
    
    // Mise à jour des données toutes les 2 secondes
    if (currentMillis - lastUpdate >= updateInterval) {
        lastUpdate = currentMillis;
        updateSensorData();
        if (isConnected) {
            sendSensorData();
        }
    }
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("WebSocket déconnecté!");
            isConnected = false;
            digitalWrite(LED_BUILTIN, HIGH);  // LED éteinte
            break;
            
        case WStype_CONNECTED:
            Serial.println("WebSocket connecté!");
            isConnected = true;
            digitalWrite(LED_BUILTIN, LOW);   // LED allumée
            break;
            
        case WStype_TEXT:
            // Gestion des messages reçus si nécessaire
            break;
    }
}

void updateSensorData() {
    // Lecture de la température et de l'humidité
    float newTemp = dht.readTemperature();
    float newHum = dht.readHumidity();
    
    // Vérification des valeurs du DHT
    if (!isnan(newTemp) && !isnan(newHum)) {
        temperature = newTemp;
        humidity = newHum;
    }

    // Lecture de la luminosité
    luminosity = analogRead(LDR_PIN);
    // Conversion de la valeur analogique (0-1023) en pourcentage (0-100)
    luminosity = map(luminosity, 0, 1023, 0, 100);
}

void sendSensorData() {
    // Création du message JSON
    StaticJsonDocument<200> doc;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["luminosity"] = luminosity;
    doc["is_connected"] = isConnected;

    // Sérialisation du JSON
    String jsonString;
    serializeJson(doc, jsonString);

    // Envoi des données
    webSocket.sendTXT(jsonString);
    
    // Debug
    Serial.println("Données envoyées: " + jsonString);
}
