# main.py - Point d'entrée principal
import _thread
import time
import core0_network
import core1_motion

# Création du dictionnaire partagé entre les deux cœurs
shared_state = {
    'speed': 0,        # Vitesse (-100 à 100)
    'turn': 0,         # Direction (-100 à 100)
    'timestamp': time.ticks_ms(), # Pour le Failsafe
    'angle_x': 0.0,
    'angle_y': 0.0
}

print("=== DÉMARRAGE DU PROTOROVER ===")

# 1. Lancement du Cœur 1 (Asservissement Moteurs) dans un Thread séparé
print("Lancement du Cœur 1...")
_thread.start_new_thread(core1_motion.run_motion_loop, (shared_state,))

# 2. Lancement du Cœur 0 (Réseau) sur le Thread principal
print("Lancement du Cœur 0...")
core0_network.run_network_loop(shared_state)
