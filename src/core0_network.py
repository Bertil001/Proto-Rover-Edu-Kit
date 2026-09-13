import network
import socket
import time
import webrepl

HTML_PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>P.R.E.K. OS</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    :root { 
        --cyan: #00e5ff; 
        --cyan-glitch: #0088ff;
        --red: #ff2a2a; 
        --green: #39ff14;
        --bg: #030a11;
        --panel-bg: rgba(3, 10, 17, 0.7);
    }
    
    body { 
        font-family: 'Share Tech Mono', monospace; background-color: var(--bg); color: var(--cyan); 
        margin: 0; height: 100vh; display: flex; flex-direction: column; overflow: hidden; user-select: none; 
    }

    .map-bg {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -2;
        background-image: 
            linear-gradient(rgba(0, 229, 255, 0.15) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.15) 1px, transparent 1px);
        background-size: 50px 50px; animation: panMap 20s linear infinite;
    }
    @keyframes panMap { 0% { background-position: 0 0; } 100% { background-position: 50px 50px; } }
    
    .linear-scanner {
        position: absolute; top: 0; left: 0; width: 100%; height: 6px;
        background: var(--cyan); box-shadow: 0 0 20px 5px var(--cyan);
        z-index: -1; animation: scan-vertical 4s linear infinite; opacity: 0.6;
    }
    @keyframes scan-vertical { 0% { transform: translateY(-10vh); } 100% { transform: translateY(110vh); } }

    .scanlines {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 9998;
        background: linear-gradient(to bottom, transparent 50%, rgba(0, 0, 0, 0.3) 51%);
        background-size: 100% 4px; pointer-events: none;
    }

    #boot-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg); z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 0.5s; }
    .boot-title { font-size: 50px; letter-spacing: 20px; text-shadow: 2px 0 var(--cyan-glitch), -2px 0 var(--red), 0 0 15px var(--cyan); animation: glitch 0.2s infinite; }
    .boot-sub { font-size: 14px; letter-spacing: 6px; color: #88c0d0; margin-top: 10px; text-align: center; }
    .boot-bar { width: 80%; max-width: 400px; height: 2px; background: rgba(0, 229, 255, 0.2); margin-top: 30px; position: relative; overflow: hidden; }
    .boot-progress { position: absolute; left: 0; top: 0; height: 100%; width: 0%; background: var(--cyan); box-shadow: 0 0 15px var(--cyan); animation: load 2s forwards ease-out; }
    @keyframes load { 0% { width: 0%; } 30% { width: 40%; } 60% { width: 60%; } 100% { width: 100%; } }
    @keyframes glitch { 0%, 100% { text-shadow: 2px 0 var(--cyan-glitch), -2px 0 var(--red); } 50% { text-shadow: -2px 0 var(--cyan-glitch), 2px 0 var(--red); } }

    header { text-align: center; padding: 10px; border-bottom: 1px solid var(--cyan); letter-spacing: 8px; font-size: 20px; text-shadow: 0 0 10px var(--cyan); background: rgba(0,0,0,0.8); backdrop-filter: blur(5px); z-index: 10;}

    .main-grid { display: grid; grid-template-columns: 300px 1fr 300px; flex: 1; min-height: 0; padding: 20px; gap: 20px; z-index: 10; overflow-y: hidden; }
    
    .panel { border: 1px solid rgba(0, 229, 255, 0.3); background: var(--panel-bg); backdrop-filter: blur(8px); position: relative; padding: 15px; display: flex; flex-direction: column; box-shadow: 0 0 20px rgba(0, 229, 255, 0.05); }
    .panel::before, .panel::after { content: ''; position: absolute; width: 15px; height: 15px; }
    .panel::before { top: -2px; left: -2px; border-top: 2px solid var(--cyan); border-left: 2px solid var(--cyan); }
    .panel::after { bottom: -2px; right: -2px; border-bottom: 2px solid var(--cyan); border-right: 2px solid var(--cyan); }
    
    .p-title { font-size: 16px; letter-spacing: 3px; border-bottom: 1px dashed rgba(0, 229, 255, 0.5); padding-bottom: 8px; margin-bottom: 15px; font-weight: bold; }
    .teaser-text { font-size: 12px; color: #88c0d0; line-height: 1.6; margin-bottom: 15px; text-align: justify; border-left: 3px solid var(--cyan); padding-left: 10px; background: rgba(0, 229, 255, 0.05); }
    .data-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid rgba(0, 229, 255, 0.1); padding-bottom: 5px;}
    .data-label { font-size: 12px; letter-spacing: 2px; color: #aaa; }
    .data-val { font-size: 20px; text-shadow: 0 0 10px var(--cyan); }
    .data-val.wifi { font-size: 16px; color: var(--green); text-shadow: 0 0 8px var(--green); }
    
    .status-box { font-size: 14px; margin-top: auto; text-align: center; padding: 10px; animation: pulse 2s infinite; font-weight: bold; letter-spacing: 2px;}
    .status-ok { color: var(--green); text-shadow: 0 0 10px var(--green); border: 1px dashed var(--green); background: rgba(57, 255, 20, 0.05);}
    .status-err { color: var(--red); text-shadow: 0 0 10px var(--red); border: 1px dashed var(--red); background: rgba(255, 42, 42, 0.05);}
    @keyframes pulse { 0%, 100% { opacity: 1; box-shadow: inset 0 0 10px transparent; } 50% { opacity: 0.8; box-shadow: inset 0 0 20px currentColor;} }

    #log_box { flex-grow: 1; overflow-y: hidden; font-size: 11px; color: #999; display: flex; flex-direction: column-reverse; margin-bottom: 15px;}
    .log-line { border-left: 2px solid var(--cyan); padding-left: 8px; margin-bottom: 4px; font-family: monospace;}
    
    #comp_info { background: rgba(0, 229, 255, 0.05); padding: 15px; border: 1px solid rgba(0, 229, 255, 0.3); font-size: 12px; line-height: 1.5; margin-bottom: 15px; box-shadow: inset 0 0 10px rgba(0, 229, 255, 0.05);}
    #comp_title { font-weight: bold; color: #fff; margin-bottom: 8px; border-bottom: 1px solid var(--cyan); letter-spacing: 2px; font-size: 14px; text-shadow: 0 0 5px var(--cyan);}

    .center-view { position: relative; display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; overflow: hidden; }
    .exploded-svg { width: 100%; max-height: 100%; filter: drop-shadow(0 0 15px rgba(0,229,255,0.4)); transform: scale(0.95); }
    
    .interactive-group { cursor: pointer; }
    .part { fill: rgba(0, 229, 255, 0.08); stroke: var(--cyan); stroke-width: 2; transition: all 0.2s ease-out; }
    .interactive-group:hover .part { fill: rgba(0, 229, 255, 0.4); filter: drop-shadow(0 0 12px var(--cyan)); stroke-width: 3;}
    .elec { stroke: var(--green); fill: rgba(57, 255, 20, 0.08); stroke-width: 1.5; stroke-dasharray: 4; transition: all 0.2s;}
    .interactive-group:hover .elec { fill: rgba(57, 255, 20, 0.4); filter: drop-shadow(0 0 12px var(--green)); stroke-width: 2.5;}
    .elec-text { fill: var(--green); font-size: 16px; text-shadow: 0 0 5px var(--green);}
    .part-text { fill: var(--cyan); font-size: 16px; text-shadow: 0 0 5px var(--cyan); font-weight: bold;}
    .link-line { stroke: rgba(0, 229, 255, 0.4); stroke-width: 2; stroke-dasharray: 6 4; animation: dash 20s linear infinite;}
    @keyframes dash { to { stroke-dashoffset: 1000; } }

    .bottom-deck { border-top: 1px solid var(--cyan); background: rgba(0,0,0,0.85); padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; z-index: 10; backdrop-filter: blur(5px); flex-shrink: 0;}
    .deck-spacer { flex: 1; }
    .dpad-grid { display: grid; grid-template-columns: 80px 80px 80px; grid-template-rows: 55px 55px; gap: 8px; justify-content: center; flex: 1;}
    .btn { background: rgba(0, 229, 255, 0.05); color: var(--cyan); border: 1px solid rgba(0, 229, 255, 0.4); cursor: pointer; font-family: inherit; font-size: 18px; letter-spacing: 2px; transition: 0.1s; box-shadow: inset 0 0 10px rgba(0,229,255,0.05); border-radius: 4px;}
    .btn:active, .btn.active-cmd { background: var(--cyan); color: var(--bg); box-shadow: 0 0 25px var(--cyan); font-weight: bold;}
    .b-fwd { grid-column: 2; grid-row: 1; } .b-bck { grid-column: 2; grid-row: 2; } .b-lft { grid-column: 1; grid-row: 2; } .b-rgt { grid-column: 3; grid-row: 2; }

    .estop-container { display: flex; justify-content: flex-end; flex: 1;}
    .estop-btn { background: rgba(255, 42, 42, 0.05); border: 2px solid var(--red); color: var(--red); width: 180px; height: 80px; font-size: 26px; font-weight: bold; letter-spacing: 4px; cursor: pointer; transition: 0.1s; box-shadow: inset 0 0 20px rgba(255,42,42,0.1); border-radius: 4px;}
    .estop-btn:active { background: var(--red); color: #fff; box-shadow: 0 0 50px var(--red); transform: scale(0.95); }

    /* --- RESPONSIVE MOBILE --- */
    @media (max-width: 900px) {
        .main-grid { display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden; padding: 10px; gap: 10px; }
        .center-view { min-height: 40vh; }
        .exploded-svg { transform: scale(1); max-height: 45vh; }
        .bottom-deck { padding: 10px; gap: 15px; }
        .deck-spacer { display: none; }
        .dpad-grid { grid-template-columns: 65px 65px 65px; grid-template-rows: 50px 50px; gap: 6px; }
        .btn { font-size: 14px; }
        .estop-btn { width: 100px; height: 100px; font-size: 18px; word-wrap: break-word; line-height: 1.2; padding: 5px;}
    }
</style>
</head>
<body>

<div class="scanlines"></div>
<div class="map-bg"></div>
<div class="linear-scanner"></div>

<div id="boot-screen">
    <div class="boot-title">P.R.E.K.</div>
    <div class="boot-sub">PROTO-ROVER EDU-KIT</div>
    <div class="boot-bar"><div class="boot-progress"></div></div>
    <div id="boot-text" style="margin-top:20px; font-size:12px; letter-spacing:3px; color:#88c0d0;">LINKING TO ROVER UPLINK...</div>
</div>

<header>P.R.E.K. // TACTICAL OS</header>

<div class="main-grid">
    <div class="panel">
        <div class="p-title">> SYS.OVERVIEW</div>
        <div class="data-row"><span class="data-label">TANGAGE (X)</span><span class="data-val" id="ang_x">--.-°</span></div>
        <div class="data-row"><span class="data-label">ROULIS (Y)</span><span class="data-val" id="ang_y">--.-°</span></div>
        <div class="data-row" style="margin-top: 15px;"><span class="data-label">UPLINK RSSI</span><span class="data-val wifi" id="wifi_rssi">-- dBm</span></div>
        <div class="data-row"><span class="data-label">WIFI CLIENTS</span><span class="data-val wifi" id="wifi_clients">-</span></div>
        <div class="status-box status-ok" id="sys_status">LIAISON SÉCURISÉE</div>
    </div>

    <div class="center-view">
        <svg class="exploded-svg" id="view-exploded" viewBox="0 0 1000 800">
            <g transform="translate(0, -30)">
                <line x1="300" y1="400" x2="200" y2="400" class="link-line"/>
                <line x1="700" y1="400" x2="800" y2="400" class="link-line"/>
                <line x1="200" y1="200" x2="100" y2="200" class="link-line"/>
                <line x1="200" y1="400" x2="100" y2="400" class="link-line"/>
                <line x1="200" y1="600" x2="100" y2="600" class="link-line"/>
                <line x1="800" y1="200" x2="900" y2="200" class="link-line"/>
                <line x1="800" y1="400" x2="900" y2="400" class="link-line"/>
                <line x1="800" y1="600" x2="900" y2="600" class="link-line"/>

                <!-- DIFFÉRENTIEL -->
                <g class="interactive-group" onclick="showComp('BARRE DIFFÉRENTIELLE', 'Mécanisme de liaison croisée. Transfère le mouvement d\'un bras de suspension à l\'autre via le pivot central pour moyenner l\'angle du châssis.')">
                    <line x1="220" y1="230" x2="780" y2="230" stroke="var(--cyan)" stroke-width="8" stroke-linecap="round"/>
                    <circle cx="500" cy="230" r="18" fill="var(--bg)" stroke="var(--cyan)" stroke-width="4"/>
                    <circle cx="500" cy="230" r="6" fill="var(--cyan)"/>
                    <path d="M 200 215 L 220 215 L 220 245 L 200 245 Z" class="part"/>
                    <path d="M 780 215 L 800 215 L 800 245 L 780 245 Z" class="part"/>
                </g>

                <!-- SUSPENSIONS & CHASSIS -->
                <g class="interactive-group" onclick="showComp('SUSPENSION GAUCHE', 'Système Rocker-Bogie. Absorbe les chocs asymétriques pour garder la plateforme de test stable.')">
                    <path d="M 180 180 L 220 180 L 220 620 L 180 620 Z" class="part"/>
                </g>
                <g class="interactive-group" onclick="showComp('SUSPENSION DROITE', 'Système Rocker-Bogie droit. Articulation libre connectée au différentiel.')">
                    <path d="M 780 180 L 820 180 L 820 620 L 780 620 Z" class="part"/>
                </g>
                
                <g class="interactive-group" onclick="showComp('CHÂSSIS PRINCIPAL', 'Noyau structurel. Isole l\'électronique de la poussière et centralise le câblage.')">
                    <rect x="300" y="200" width="400" height="400" rx="10" class="part"/>
                    <text x="500" y="225" text-anchor="middle" class="part-text" pointer-events="none">PLATEFORME PREK</text>
                </g>

                <!-- ROUES -->
                <g class="interactive-group" onclick="showComp('ROUE AV GAUCHE', 'Grip maximal pour terrain meuble.')"><rect x="40" y="150" width="60" height="100" rx="5" class="part"/></g>
                <g class="interactive-group" onclick="showComp('ROUE MI GAUCHE', 'Axe de pivot du système bogie.')"><rect x="40" y="350" width="60" height="100" rx="5" class="part"/></g>
                <g class="interactive-group" onclick="showComp('ROUE AR GAUCHE', 'Traction arrière indépendante.')"><rect x="40" y="550" width="60" height="100" rx="5" class="part"/></g>
                <g class="interactive-group" onclick="showComp('ROUE AV DROITE', 'Grip maximal pour terrain meuble.')"><rect x="900" y="150" width="60" height="100" rx="5" class="part"/></g>
                <g class="interactive-group" onclick="showComp('ROUE MI DROITE', 'Axe de pivot du système bogie droit.')"><rect x="900" y="350" width="60" height="100" rx="5" class="part"/></g>
                <g class="interactive-group" onclick="showComp('ROUE AR DROITE', 'Traction arrière indépendante.')"><rect x="900" y="550" width="60" height="100" rx="5" class="part"/></g>

                <!-- MOTEURS N20 -->
                <g class="interactive-group" onclick="showComp('MOTEUR N20 (AV-G)', 'Micromoteur DC 6V avec réducteur. Fournit le couple pour la roue Avant Gauche.')"><rect x="110" y="180" width="40" height="40" class="elec"/><text x="130" y="206" text-anchor="middle" class="elec-text" pointer-events="none">M</text></g>
                <g class="interactive-group" onclick="showComp('MOTEUR N20 (MI-G)', 'Micromoteur DC 6V avec réducteur. Entraîne la roue Milieu Gauche.')"><rect x="110" y="380" width="40" height="40" class="elec"/><text x="130" y="406" text-anchor="middle" class="elec-text" pointer-events="none">M</text></g>
                <g class="interactive-group" onclick="showComp('MOTEUR N20 (AR-G)', 'Micromoteur DC 6V avec réducteur. Entraîne la roue Arrière Gauche.')"><rect x="110" y="580" width="40" height="40" class="elec"/><text x="130" y="606" text-anchor="middle" class="elec-text" pointer-events="none">M</text></g>
                <g class="interactive-group" onclick="showComp('MOTEUR N20 (AV-D)', 'Micromoteur DC 6V avec réducteur. Fournit le couple pour la roue Avant Droite.')"><rect x="850" y="180" width="40" height="40" class="elec"/><text x="870" y="206" text-anchor="middle" class="elec-text" pointer-events="none">M</text></g>
                <g class="interactive-group" onclick="showComp('MOTEUR N20 (MI-D)', 'Micromoteur DC 6V avec réducteur. Entraîne la roue Milieu Droite.')"><rect x="850" y="380" width="40" height="40" class="elec"/><text x="870" y="406" text-anchor="middle" class="elec-text" pointer-events="none">M</text></g>
                <g class="interactive-group" onclick="showComp('MOTEUR N20 (AR-D)', 'Micromoteur DC 6V avec réducteur. Entraîne la roue Arrière Droite.')"><rect x="850" y="580" width="40" height="40" class="elec"/><text x="870" y="606" text-anchor="middle" class="elec-text" pointer-events="none">M</text></g>

                <!-- ÉLECTRONIQUE DE BORD -->
                <g class="interactive-group" onclick="showComp('BATTERIE LI-PO', 'Source de puissance principale. Alimente directement les drivers moteurs et le module Buck.')">
                    <rect x="350" y="240" width="300" height="80" rx="4" class="elec"/>
                    <text x="500" y="285" text-anchor="middle" class="elec-text" pointer-events="none">PACK BATTERIE</text>
                </g>

                <g class="interactive-group" onclick="showComp('FUSIBLE 10A', 'Protection matérielle coupe-circuit. Isole le système en cas de surintensité ou blocage moteur.')">
                    <rect x="360" y="340" width="60" height="50" rx="3" class="elec"/>
                    <text x="390" y="370" text-anchor="middle" class="elec-text" pointer-events="none">FUSE</text>
                </g>

                <g class="interactive-group" onclick="showComp('MODULE BUCK 12V>5V', 'Convertisseur DC-DC Step-Down. Abaisse la tension batterie pour fournir un 5V propre et stable à l\'ESP32.')">
                    <rect x="450" y="340" width="100" height="50" rx="3" class="elec"/>
                    <text x="500" y="370" text-anchor="middle" class="elec-text" pointer-events="none">12V>5V</text>
                </g>

                <g class="interactive-group" onclick="showComp('NOYAU ESP32', 'Microcontrôleur principal. Gère la télémétrie Wi-Fi, la logique de commande et la génération des signaux PWM.')">
                    <rect x="420" y="410" width="160" height="70" rx="3" class="elec"/>
                    <text x="500" y="450" text-anchor="middle" class="elec-text" pointer-events="none">ESP32 CORE</text>
                </g>

                <g class="interactive-group" onclick="showComp('MPU6050 (IMU)', 'Centrale inertielle (Accéléromètre + Gyroscope 6 axes). Calcule l\'assiette du rover en temps réel.')">
                    <rect x="475" y="495" width="50" height="50" rx="3" class="elec"/>
                    <text x="500" y="525" text-anchor="middle" class="elec-text" pointer-events="none">MPU</text>
                </g>

                <g class="interactive-group" onclick="showComp('DRIVER BTS7960 (L)', 'Pont en H de forte puissance (43A). Reçoit les PWM de l\'ESP32 pour piloter la vitesse des 3 moteurs gauches.')">
                    <rect x="320" y="490" width="80" height="90" rx="3" class="elec"/>
                    <text x="360" y="540" text-anchor="middle" class="elec-text" pointer-events="none">BTS-L</text>
                </g>
                
                <g class="interactive-group" onclick="showComp('DRIVER BTS7960 (R)', 'Pont en H de forte puissance (43A). Reçoit les PWM de l\'ESP32 pour piloter la vitesse des 3 moteurs droits.')">
                    <rect x="600" y="490" width="80" height="90" rx="3" class="elec"/>
                    <text x="640" y="540" text-anchor="middle" class="elec-text" pointer-events="none">BTS-R</text>
                </g>
            </g>
        </svg>
    </div>

    <div class="panel">
        <div class="p-title">> DATA.LINK</div>
        <div id="comp_info">
            <div id="comp_title">BALAYAGE ACTIF</div>
            <span id="comp_desc">Sélectionnez un composant sur la matrice tactique pour extraire les spécifications.</span>
        </div>
        <div class="p-title" style="margin-top:auto;">> SYS.TERMINAL</div>
        <div id="log_box">
            <div class="log-line">INIT HTTP SERVER... OK</div>
            <div class="log-line">SYSTEM ONLINE</div>
        </div>
    </div>
</div>

<div class="bottom-deck">
    <div class="deck-spacer"></div>
    <div class="dpad-grid">
        <button id="btn-fwd" class="btn b-fwd" onclick="sendBtn('FORWARD')">FWD</button>
        <button id="btn-lft" class="btn b-lft" onclick="sendBtn('LEFT')">LFT</button>
        <button id="btn-bck" class="btn b-bck" onclick="sendBtn('BACKWARD')">BCK</button>
        <button id="btn-rgt" class="btn b-rgt" onclick="sendBtn('RIGHT')">RGT</button>
    </div>
    <div class="estop-container">
        <button class="estop-btn" onclick="sendEmergencyStop()">E-STOP</button>
    </div>
</div>

<script>
setTimeout(() => { document.getElementById('boot-text').innerText = "CALIBRATING MODULES..."; }, 1000);
setTimeout(() => { 
    document.getElementById('boot-screen').style.opacity = '0'; 
    setTimeout(() => { document.getElementById('boot-screen').style.display = 'none'; }, 500);
}, 2500);

let isFetching = false;
let pendingUrl = null;

function fetchWithLock(url) {
    if (isFetching) { pendingUrl = url; return; }
    isFetching = true;
    fetch(url).then(() => {
        isFetching = false;
        if (pendingUrl) { let next = pendingUrl; pendingUrl = null; fetchWithLock(next); }
    }).catch(() => { isFetching = false; });
}

function log(msg) {
    const box = document.getElementById("log_box");
    const line = document.createElement("div");
    line.className = "log-line";
    line.innerText = "> " + msg;
    box.prepend(line);
    if(box.children.length > 12) box.removeChild(box.lastChild);
}

function sendBtn(cmd) {
    log("VECTEUR: " + cmd);
    const status = document.getElementById("sys_status");
    document.querySelectorAll('.btn').forEach(b => b.classList.remove('active-cmd'));

    if (cmd !== 'STOP') {
        status.innerText = "ENGAGÉ - MOUVEMENT";
        status.className = "status-box status-ok";
        let btnId = cmd === 'FORWARD' ? 'fwd' : cmd === 'BACKWARD' ? 'bck' : cmd === 'LEFT' ? 'lft' : 'rgt';
        document.getElementById('btn-' + btnId).classList.add('active-cmd');
    } else {
        status.innerText = "LIAISON SÉCURISÉE";
    }
    fetchWithLock("/cmd?dir=" + cmd);
}

function sendEmergencyStop() {
    log("!!! EMERGENCY HALT !!!");
    document.getElementById("sys_status").innerText = "HALTED - OVERRIDE";
    document.getElementById("sys_status").className = "status-box status-err";
    sendBtn('STOP');
    fetch("/cmd?dir=STOP");
    pendingUrl = null;
}

function getTelemetry() {
    fetch("/telemetry")
        .then(r => r.text())
        .then(data => { 
            let parts = data.split(',');
            if(parts.length >= 4) {
                document.getElementById("ang_x").innerText = parts[0] + "°";
                document.getElementById("ang_y").innerText = parts[1] + "°";
                document.getElementById("wifi_rssi").innerText = parts[2] + " dBm";
                document.getElementById("wifi_clients").innerText = parts[3];
            }
        }).catch(err => {});
}
setInterval(getTelemetry, 1000);

function showComp(title, desc) {
    document.getElementById("comp_title").innerText = title;
    document.getElementById("comp_desc").innerText = desc;
    log("ANALYSE COMPOSANT: " + title);
}
</script>
</body>
</html>"""

def run_network_loop(*args):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ProtoRover_AP", authmode=0)
    print("[Core 0] Point d'accès Wi-Fi créé :", ap.ifconfig()[0])
    
    webrepl.start(password='rover123')
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    print("[Core 0] Serveur HTTP en écoute sur le port 80")
    
    while True:
        try:
            conn, addr = s.accept()
            conn.settimeout(2.0)
            request = conn.recv(1024).decode('utf-8')
            
            if not request or len(request.split(' ')) < 2:
                conn.close()
                continue
                
            route = request.split(' ')[1]
            
            if route.startswith('/telemetry'):
                ang_x = args[0].get('angle_x', 0.0)
                ang_y = args[0].get('angle_y', 0.0)
                
                rssi = -50
                clients_count = 0
                try:
                    stations = ap.status('stations')
                    clients_count = len(stations)
                    if clients_count > 0:
                        rssi = stations[0][1] # Format: (MAC, RSSI)
                except:
                    pass
                
                conn.send(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{ang_x:.1f},{ang_y:.1f},{rssi},{clients_count}".encode('utf-8'))
                conn.close()
                continue

            if route.startswith('/cmd'):
                if 'dir=FORWARD' in route:
                    args[0]['speed'] = 100; args[0]['turn'] = 0
                elif 'dir=BACKWARD' in route:
                    args[0]['speed'] = -100; args[0]['turn'] = 0
                elif 'dir=LEFT' in route:
                    args[0]['speed'] = 0; args[0]['turn'] = -100
                elif 'dir=RIGHT' in route:
                    args[0]['speed'] = 0; args[0]['turn'] = 100
                elif 'dir=STOP' in route:
                    args[0]['speed'] = 0; args[0]['turn'] = 0
                
                args[0]['timestamp'] = time.ticks_ms()
                conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
                conn.close()
                continue
            
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n\r\n")
            
            chunk_size = 1024
            html_bytes = HTML_PAGE.encode('utf-8')
            for i in range(0, len(html_bytes), chunk_size):
                conn.send(html_bytes[i:i+chunk_size])
            
            conn.close()
            
        except Exception as e:
            try: conn.close()
            except: pass