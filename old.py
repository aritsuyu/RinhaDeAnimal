import random
import time

# Fraquezas
fraquezas = {
    "Lutador": ["Rei"],
    "Rei": ["Pombo"],
    "Apostador": ["Lutador"]
}

class Animais:
    def __init__(self, nome, tipo, hp, ataques):
        self.nome = nome
        self.tipo = tipo
        self.hp = hp
        self.ataques = ataques
        self.efeitos_pendentes = []
        self.paralisado = False

    def aplicar_efeitos(self):
        novos_efeitos = []
        for efeito in self.efeitos_pendentes:
            efeito["turnos"] -= 1
            if efeito["turnos"] <= 0:
                self.hp -= efeito["dano"]
                self.hp = max(self.hp, 0)
                print(f"{self.nome} recebeu {efeito['dano']} de dano atrasado do efeito '{efeito['nome']}'!")
            else:
                novos_efeitos.append(efeito)
        self.efeitos_pendentes = novos_efeitos

    def atacar(self, outro):
        if self.paralisado:
            print(f"{self.nome} está paralisado e perdeu o turno!\n")
            self.paralisado = False
            return

        ataque = random.choice(self.ataques)

        # Skill Stun
        if ataque["nome"] == "Carta Paralizante":
            print(f"{self.nome} usou {ataque['nome']}! {outro.nome} foi paralisado!")
            outro.paralisado = True
            outro.efeitos_pendentes.append({
                "nome": "Explosão da Carta",
                "turnos": 2,
                "dano": random.randint(45, 55)
            })
            return

        # Aposta
        if ataque["nome"] == "Apostar":
            valor = random.randint(1, 15)
            print(f"{self.nome} usou {ataque['nome']}! Valor sorteado: {valor}")
            if valor > 7:
                outro.hp -= valor
                outro.hp = max(outro.hp, 0)
                print(f"Funcionou! {outro.nome} perdeu {valor} de HP!")
            else:
                print("Aposta falhou! Nenhum dano foi causado.")
            print()
            return

        # Attck normal
        dano = random.randint(ataque["dano_min"], ataque["dano_max"])

        if outro.tipo in fraquezas.get(self.tipo, []):
            dano = int(dano * 1.5)
            print("É super efetivo!")

        outro.hp -= dano
        outro.hp = max(outro.hp, 0)

        print(f"{self.nome} usou {ataque['nome']} e causou {dano} de dano!")
        print(f"{outro.nome} agora tem {outro.hp} de HP.\n")

# Animais
Galo = Animais("Galo", "Lutador", 70, [
    {"nome": "Dilacerar", "dano_min": 18, "dano_max": 45},
    {"nome": "Investida", "dano_min": 10, "dano_max": 35}
])

Leão = Animais("Leão", "Rei", 140, [
    {"nome": "Mordida", "dano_min": 15, "dano_max": 22},
    {"nome": "Arranhão", "dano_min": 10, "dano_max": 14}
])

Tigrinho = Animais("Trigrinho", "Apostador", 50, [
    {"nome": "Jogar moeda", "dano_min": 1, "dano_max": 35},
    {"nome": "Carta Paralizante", "dano_min": 0, "dano_max": 0},
    {"nome": "Apostar", "dano_min": 0, "dano_max": 0}
])

pokemons = [Galo, Leão, Tigrinho]

# Player
print("Escolha seu Animal:")
for i, p in enumerate(pokemons):
    print(f"{i + 1}. {p.nome}")

escolha = int(input("Digite o número do Animal: ")) - 1
jogador = pokemons[escolha]
inimigos = [p for i, p in enumerate(pokemons) if i != escolha]
inimigo = random.choice(inimigos)

print(f"\nVocê escolheu {jogador.nome}!")
print(f"O inimigo escolheu {inimigo.nome}!\n")

# Loop
while jogador.hp > 0 and inimigo.hp > 0:
    jogador.aplicar_efeitos()
    jogador.atacar(inimigo)

    time.sleep(1)

    if inimigo.hp <= 0:
        print(f"{inimigo.nome} foi destruido! Você venceu! 🎉")
        break

    inimigo.aplicar_efeitos()
    inimigo.atacar(jogador)

    time.sleep(1)

    if jogador.hp <= 0:
        print(f"{jogador.nome} foi destruido! Você perdeu! 💔")
        break
