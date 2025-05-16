import random
from Engine.fraquezas import fraquezas
class Animais:
    def __init__(self, nome, tipo, hp, ataques):
        self.nome = nome
        self.tipo = tipo
        self.max_hp = hp
        self.hp = hp
        self.ataques = ataques
        self.efeitos_pendentes = []
        self.paralisado = False

    def aplicar_efeitos(self):
        novos_efeitos = []
        dano_total = 0
        for efeito in self.efeitos_pendentes:
            efeito["turnos"] -= 1
            if efeito["turnos"] <= 0:
                self.hp -= efeito["dano"]
                self.hp = max(self.hp, 0)
                dano_total += efeito['dano']
            else:
                novos_efeitos.append(efeito)
        self.efeitos_pendentes = novos_efeitos
        return dano_total

    def atacar(self, outro, ataque_escolhido):
        if self.paralisado:
            self.paralisado = False
            return f"{self.nome} está paralisado e perdeu o turno!\n"

        ataque = None
        for atk in self.ataques:
            if atk["nome"] == ataque_escolhido:
                ataque = atk
                break

        if not ataque:
            return f"Ataque {ataque_escolhido} inválido!"

        # Skill Stun
        if ataque["nome"] == "Carta Paralizante":
            valorstuntigre = random.randint(1, 100)
            if valorstuntigre > 50:
                outro.paralisado = True
                outro.efeitos_pendentes.append({
                    "nome": "Explosão da Carta",
                    "turnos": 2,
                    "dano": random.randint(15, 35)
                })
                return f"{self.nome} usou {ataque['nome']}! {outro.nome} foi paralisado!"
            else:
                return f"{self.nome} usou {ataque['nome']}! Mas não funcionou!"

        # Aposta
        if ataque["nome"] == "Apostar":
            valor = random.randint(35, 75)
            msg = f"{self.nome} usou {ataque['nome']}! Valor sorteado: {valor}\n"
            if valor > 38:
                outro.hp -= valor
                outro.hp = max(outro.hp, 0)
                msg += f"Funcionou! {outro.nome} perdeu {valor} de HP!"
            else:
                msg += "Aposta falhou! Nenhum dano foi causado."
            return msg

        # Ataque normal
        dano = random.randint(ataque["dano_min"], ataque["dano_max"])

        if outro.tipo in fraquezas.get(self.tipo, []):
            dano = int(dano * 1.5)
            dano_msg = "É super efetivo!"
        else:
            dano_msg = ""

        outro.hp -= dano
        outro.hp = max(outro.hp, 0)

        return f"{self.nome} usou {ataque['nome']} e causou {dano} de dano! {dano_msg}"