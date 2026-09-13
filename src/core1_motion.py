import time
import math
from machine import Pin, PWM, I2C
from lib_mpu6050 import MPU6050

class MotionController:
    def __init__(self, l_fwd=12, l_rev=13, r_fwd=14, r_rev=27):
        # Initialisation des broches PWM pour le driver BTS7960
        self.lpwm_l = PWM(Pin(l_fwd), freq=1000, duty=0)
        self.rpwm_l = PWM(Pin(l_rev), freq=1000, duty=0)
        self.lpwm_r = PWM(Pin(r_fwd), freq=1000, duty=0)
        self.rpwm_r = PWM(Pin(r_rev), freq=1000, duty=0)

    def set_motors(self, speed_left, speed_right):
        MAX_DUTY = 1023 
        duty_l = int((abs(speed_left) / 100) * MAX_DUTY)
        duty_r = int((abs(speed_right) / 100) * MAX_DUTY)
        
        # Arrêt de toutes les broches avant d'appliquer la nouvelle direction
        self.lpwm_l.duty(0)
        self.rpwm_l.duty(0)
        self.lpwm_r.duty(0)
        self.rpwm_r.duty(0)
        
        # Moteur Gauche
        if speed_left > 0:
            self.lpwm_l.duty(duty_l)
        elif speed_left < 0:
            self.rpwm_l.duty(duty_l)
            
        # Moteur Droit
        if speed_right > 0:
            self.lpwm_r.duty(duty_r)
        elif speed_right < 0:
            self.rpwm_r.duty(duty_r)

def run_motion_loop(*args):
    print("[Core 1] Démarrage de la boucle de contrôle et télémétrie 6-axes !")
    motion = MotionController()
    state = args[0]
    
    # --- 1. Initialisation du capteur MPU6050 ---
    try:
        ligne_i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
        capteur = MPU6050(ligne_i2c)
        capteur_ok = True
    except Exception as e:
        print("[Core 1] ERREUR : MPU6050 introuvable !", e)
        capteur_ok = False
        
    # --- 2. Fonction pour calculer les angles X et Y ---
    def get_angles():
        if not capteur_ok: return 0.0, 0.0
        
        x, y, z = capteur.get_accel()
        
        # Correction vitale pour les nombres négatifs (complément à 2)
        if x > 32767: x -= 65536
        if y > 32767: y -= 65536
        if z > 32767: z -= 65536
        
        # Calcul trigonométrique (Tangage et Roulis)
        angle_x = math.atan2(-x, math.sqrt(y * y + z * z)) * (180.0 / math.pi)
        angle_y = math.atan2(y, math.sqrt(x * x + z * z)) * (180.0 / math.pi)
        
        return angle_x, angle_y

    compteur_affichage = 0

    # --- 3. Boucle principale ---
    while True:
        # Lecture des ordres moteurs sécurisée par .get()
        vitesse = state.get('speed', 0)
        direction = state.get('turn', 0)
        
        # Mixage des vitesses pour les chenilles/roues
        vitesse_gauche = vitesse + direction
        vitesse_droite = vitesse - direction
        
        # Action sur les moteurs
        motion.set_motors(vitesse_gauche, vitesse_droite)
        
        # Récupération et sauvegarde des deux angles pour le Core 0
        ax, ay = get_angles()
        state['angle_x'] = ax
        state['angle_y'] = ay
        
        # Affichage console (1 fois par seconde environ)
        compteur_affichage += 1
        if compteur_affichage >= 20: 
            print(f"| Tangage(X): {ax:>6.1f}° | Roulis(Y): {ay:>6.1f}° | Mot: G={vitesse_gauche}% D={vitesse_droite}% |")
            compteur_affichage = 0
            
        time.sleep(0.05)