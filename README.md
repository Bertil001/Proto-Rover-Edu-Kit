# 🚀 P.R.E.K. (Proto-Rover Edu-Kit)

**P.R.E.K.** est une plateforme d'exploration robotique 6x6 open-source conçue pour l'apprentissage et le prototypage avancé. Basé sur un microcontrôleur ESP32 et un châssis "Rocker-Bogie", le rover embarque son propre serveur web tactile, une centrale inertielle 6-axes et une architecture logicielle asynchrone Dual-Core.

---

## ⚙️ Fonctionnalités Principales

* **Châssis Rocker-Bogie :** Suspension mécanique passive permettant de franchir des obstacles asymétriques tout en gardant la plateforme électronique stable.
* **Architecture Dual-Core (MicroPython) :**
  * **Core 0 :** Gestion du réseau, création du point d'accès Wi-Fi, serveur HTTP asynchrone et interface web (UI).
  * **Core 1 :** Cinématique de contrôle moteur (PWM à 1000 Hz), mixage Tank-Drive, rampe d'accélération et calcul trigonométrique de l'assiette.
* **Système Fail-Safe :** Arrêt d'urgence automatique en cas de perte de la trame réseau (délai > 500ms).
* **Interface "Tactical OS" :** IHM web full-responsive hébergée sur l'ESP32, avec vue éclatée SVG interactive et télémétrie en temps réel (Tangage, Roulis, RSSI Wi-Fi).

---

## 🛠️ Matériel Requis (BOM)

* **Microcontrôleur :** 1x ESP32 (WROOM-32)
* **Puissance :** 
  * 1x Batterie Li-Po (7.4V ou 11.1V)
  * 1x Module Buck Converter (12V > 5V) pour isoler le circuit logique
  * 2x Drivers moteur BTS7960 (Pont en H 43A)
* **Motricité :** 6x Micromoteurs N20 avec réducteurs + roues tout-terrain
* **Capteur :** 1x Centrale Inertielle MPU6050 (Accéléromètre / Gyroscope)
* **Sécurité :** Fusible automobile 10A et câblage de puissance adapté

---

## 📂 Arborescence du Projet

* `/src/` : Code source MicroPython embarqué sur l'ESP32.
  * `main.py` : Lanceur Dual-Core.
  * `core0_network.py` : Serveur réseau et code HTML/CSS/JS de l'interface.
  * `core1_motion.py` : Boucle cinématique et gestion matérielle (Moteurs & MPU).
  * `lib_mpu6050.py` : Pilote I2C pour le capteur inertiel.
* `/hardware/` : Fichiers de conception physique (Modèles 3D STEP/STL, Schémas de câblage).
* `/docs/` : Documentation d'ingénierie (Cahier des charges, plans de tests, bilan technique).

---

## 🚀 Démarrage Rapide (Quick Start)

### 1. Déploiement Logiciel
1. Flashez votre ESP32 avec le dernier firmware **MicroPython**.
2. Utilisez un IDE comme [Thonny](https://thonny.org/) ou l'outil **WebREPL** pour transférer l'intégralité du contenu du dossier `/src/` à la racine matérielle de l'ESP32.
3. Redémarrez le microcontrôleur.

### 2. Connexion et Pilotage
Une fois l'ESP32 alimenté, le rover génère son propre réseau autonome :
* **Réseau Wi-Fi (SSID) :** `ProtoRover_AP`
* **Mot de passe Wi-Fi :** *(Réseau ouvert)*
* **URL de l'Interface de Contrôle :** Ouvrez `http://192.168.4.1` sur le navigateur d'un smartphone ou d'un PC.

### 3. Maintenance Sans Fil (OTA)
Le P.R.E.K. intègre le protocole WebREPL pour la mise à jour du code sans câble USB :
* **Adresse WebSocket :** `ws://192.168.4.1:8266`
* **Mot de passe WebREPL :** `rover123`

---

## 📝 Licence
Ce projet est distribué sous la Licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.
