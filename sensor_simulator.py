import asyncio
import websockets
import json
import random
import time
from datetime import datetime

async def send_sensor_data():
    uri = "ws://localhost:8000/ws/sensors/"
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connecté au serveur WebSocket")
                
                while True:
                    # Simuler des données de capteurs
                    data = {
                        "temperature": round(random.uniform(20, 30), 1),
                        "humidity": round(random.uniform(40, 60), 1),
                        "luminosity": round(random.uniform(100, 1000), 0),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Envoyer les données
                    await websocket.send(json.dumps(data))
                    print(f"Données envoyées: {data}")
                    
                    # Attendre 2 secondes avant le prochain envoi
                    await asyncio.sleep(2)
                    
        except websockets.exceptions.ConnectionClosed:
            print("Connexion perdue. Tentative de reconnexion...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Erreur: {str(e)}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    print("Démarrage du simulateur de capteurs...")
    asyncio.run(send_sensor_data())
