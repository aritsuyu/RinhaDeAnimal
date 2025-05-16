from Engine.brain import Animais
#Tipos
Tipos={"Fogo", "Água", "Terra", "Ar", "Sombrio", "Eletrico", "Dragão","Rei", "Lutador", "Apostador",}
#Bestiario
FireBoy = Animais("FireBoy", "Fogo", 145, [
    {"nome": "Lança Chamas", "dano_min": 20, "dano_max": 40},
    {"nome": "Explosão", "dano_min": 30, "dano_max": 50}
])

WaterGirl = Animais("WaterGirl", "Água", 95, [
    {"nome": "Jato D'água", "dano_min": 35, "dano_max": 35},
    {"nome": "Tsunami", "dano_min": 25, "dano_max": 55}
])

Galo = Animais("Galo", "Lutador", 135, [
    {"nome": "Dilacerar", "dano_min": 18, "dano_max": 45},
    {"nome": "Investida", "dano_min": 10, "dano_max": 35}
])

Leao = Animais("Leão", "Rei", 240, [
    {"nome": "Mordida", "dano_min": 15, "dano_max": 40},
    {"nome": "Arranhão", "dano_min": 10, "dano_max": 20}
])

Tigrinho = Animais("Tigrinho", "Apostador", 105, [
    {"nome": "Jogar moeda", "dano_min": 1, "dano_max": 35},
    {"nome": "Carta Paralizante", "dano_min": 0, "dano_max": 0},
    {"nome": "Apostar", "dano_min": 0, "dano_max": 0}
])

pokemons = [FireBoy, WaterGirl, Galo, Leao, Tigrinho]