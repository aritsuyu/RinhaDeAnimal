#Coração
import pygame
import random
import sys
from Engine.bestiary import pokemons
from Engine.fraquezas import fraquezas
from Engine.brain import Animais

def escolher_animal():
    print("Número de pokemons disponíveis:", len(pokemons))  # Debug
    ...
pygame.init()

# Tela
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Batalha de Animais")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

# Font
font = pygame.font.SysFont(None, 28)
font_big = pygame.font.SysFont(None, 40)

# Seleção de Lutador
def escolher_animal():
    escolha = None
    while escolha is None:
        screen.fill(WHITE)
        text = font_big.render("Escolha seu Lutador:", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 30))
        for i, p in enumerate(pokemons):
            txt = font.render(f"{i+1}. {p.nome} (HP: {p.hp})", True, BLACK)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 100 + i*40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(pokemons):
                        escolha = index
    return escolha


# Desenha barra de HP
def draw_hp_bar(pokemon, x, y):
    bar_width = 250
    bar_height = 25
    fill = (pokemon.hp / pokemon.max_hp) * bar_width
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, fill, bar_height))
    hp_text = font.render(f"{pokemon.hp} / {pokemon.max_hp}", True, BLACK)
    screen.blit(hp_text, (x + bar_width//2 - hp_text.get_width()//2, y + 2))
    
class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = GRAY

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        txt = font.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + (self.rect.width - txt.get_width())//2,
                          self.rect.y + (self.rect.height - txt.get_height())//2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    escolha = escolher_animal()
    jogador = pokemons[escolha]
    inimigos = [p for i, p in enumerate(pokemons) if i != escolha]
    inimigo = random.choice(inimigos)

    mensagem = f"Você escolheu {jogador.nome}! O inimigo escolheu {inimigo.nome}!"

    clock = pygame.time.Clock()
    player_turn = True
    running = True
    ataque_buttons = []
    waiting_for_enemy = False
    delay_enemy = 0

    # Botões de Ataque
    def criar_botoes():
        botoes = []
        start_x = 30
        start_y = HEIGHT - 100
        largura = 150
        altura = 40
        espaçamento = 20
        for i, atk in enumerate(jogador.ataques):
            btn = Button((start_x + (largura + espaçamento)*i, start_y, largura, altura), atk["nome"])
            botoes.append(btn)
        return botoes

    ataque_buttons = criar_botoes()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn and not waiting_for_enemy:
                pos = pygame.mouse.get_pos()
                for btn in ataque_buttons:
                    if btn.is_clicked(pos):
                        # Jogador ataca
                        mensagem = jogador.atacar(inimigo, btn.text)
                        inimigo.aplicar_efeitos()
                        player_turn = False
                        waiting_for_enemy = True
                        delay_enemy = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Nome e HP
        nome_jog = font_big.render(f"Você: {jogador.nome}", True, BLACK)
        screen.blit(nome_jog, (30, 20))
        draw_hp_bar(jogador, 30, 60)

        nome_ini = font_big.render(f"Inimigo: {inimigo.nome}", True, BLACK)
        screen.blit(nome_ini, (WIDTH - 300, 20))
        draw_hp_bar(inimigo, WIDTH - 300, 60)

        # Botões
        if player_turn and not waiting_for_enemy:
            for btn in ataque_buttons:
                btn.draw()
        else:
            msg_ataque = font.render("Inimigo está atacando...", True, BLACK)
            screen.blit(msg_ataque, (WIDTH//2 - msg_ataque.get_width()//2, HEIGHT - 90))

        # Mensagem de habilidade
        msg = font.render(mensagem, True, BLACK)
        screen.blit(msg, (30, HEIGHT//2))

        # Turnos inimigo
        if waiting_for_enemy:
            now = pygame.time.get_ticks()
            if now - delay_enemy > 1500:
                msg_ataque_inimigo = inimigo.atacar(jogador, random.choice([atk["nome"] for atk in inimigo.ataques]))
                jogador.aplicar_efeitos()
                mensagem = msg_ataque_inimigo
                player_turn = True
                waiting_for_enemy = False

        # Win/Derrota
        if jogador.hp <= 0:
            mensagem = f"{jogador.nome} foi destruído! Você perdeu! 💔"
            player_turn = False
            waiting_for_enemy = False
        elif inimigo.hp <= 0:
            mensagem = f"{inimigo.nome} foi destruído! Você venceu! 🎉"
            player_turn = False
            waiting_for_enemy = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
