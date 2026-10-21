import re
import json

with open('/home/user/openbreak/assets/data_uris.json', 'r', encoding='utf-8') as f:
    images = json.load(f)

with open('/home/user/openbreak/assets/three.min.js', 'r', encoding='utf-8') as f:
    three_min_js = f.read()

img_reformer_1 = images.get("reformer_1", "")
img_reformer_2 = images.get("reformer_2", "")
img_reformer_3 = images.get("reformer_3", "")
img_coach_1 = images.get("coach_1", "")
img_coach_2 = images.get("coach_2", "")

cards_data = [
    {"num": "01 LIVE", "title": "Cima Studio Polanco", "desc": "12 Camas Allegro 2 · CDMX", "img": img_reformer_1, "tag": "98% Ocupación"},
    {"num": "02 LIVE", "title": "Marea Barre Condesa", "desc": "Sala Principal · 18 Barras", "img": img_coach_1, "tag": "Waitlist Auto"},
    {"num": "03 LIVE", "title": "Aura Reformer Roma Norte", "desc": "10 Camas Custom Nogal", "img": img_reformer_2, "tag": "Bloqueo Atómico"},
    {"num": "04 LIVE", "title": "Pulse Cycling Juárez", "desc": "32 Bicis Stages SC3", "img": img_coach_2, "tag": "Check-in 1-Tap"},
    {"num": "05 LIVE", "title": "Zenith Yoga Cuauhtémoc", "desc": "Shala Caliente · 24 Mats", "img": img_reformer_3, "tag": "0% Stripe"},
    {"num": "06 LIVE", "title": "Komorebi San Pedro", "desc": "14 Reformers Peak · NL", "img": img_reformer_1, "tag": "Ledger Directo"},
    {"num": "07 LIVE", "title": "Lina Studio Guadalajara", "desc": "Pilates Clásico & Reformer", "img": img_coach_1, "tag": "Waitlist Auto"},
    {"num": "08 LIVE", "title": "Soma Movement Zapopan", "desc": "Entrenamiento Funcional Boutique", "img": img_reformer_2, "tag": "99% Retención"},
    {"num": "09 LIVE", "title": "Vela Movement Querétaro", "desc": "8 Camas Reformer Studio", "img": img_coach_2, "tag": "1-Tap Lobby"},
    {"num": "10 LIVE", "title": "Néctar Barre Santa Fe", "desc": "20 Barras & Studio Pilates", "img": img_reformer_3, "tag": "0% Comisión"},
    {"num": "11 LIVE", "title": "Prana Hot Yoga Puebla", "desc": "Shala Infrarrojo · 20 Mats", "img": img_reformer_1, "tag": "Bloqueo Atómico"},
    {"num": "12 LIVE", "title": "Equilibrio Studio Mérida", "desc": "10 Reformers · Altabrisa", "img": img_coach_2, "tag": "Stripe Connect"}
]

print(f"Data verified with {len(cards_data)} luxury studio cards.")
