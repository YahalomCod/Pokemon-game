import sys
import threading
from random import randint
from types import SimpleNamespace
from client import Client

# init pygame
from GraphAlgo import *
from src.Pokemon import Pokemon

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
pokemons = vars(pokemons_obj)
# gw.g.initPokemons(pokemons)


print(pokemons)

graph_json = client.get_graph()

graph = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

graph = vars(graph)

gw = GraphAlgo()
gw.load_from_jsonString(graph)

FONT = pygame.font.SysFont('Arial', 20, bold=True)


# load the json string into SimpleNamespace Object


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return int(((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen)


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15


def setAgent(client: Client):
    pokes = []
    x = json.loads(client.get_info())
    y = x.get("GameServer")
    numAgents = y.get('agents')
    x = json.loads(client.get_pokemons())
    i = 0
    for p in x['Pokemons']:
        p = p.get('Pokemon')
        value = float(p['value'])
        type = int(p['type'])
        x, y, _ = p['pos'].split(',')
        x = float(x)
        y = float(y)
        pos = (x, y, 0)
        pokes.append(Pokemon(value, type, pos))
        x = gw.g.findPokemonEdge(pokes[i])
        if i < numAgents:
            client.add_agent("{\"id\":" + str(x[0]) + "}")
        i += 1

    pass


setAgent(client)
print(client.get_agents())
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

min_x = sys.maxsize
min_y = sys.maxsize
max_x = 0
max_y = 0
for node in gw.g.nodes.values():
    if (min_x > node.pos[0]): min_x = node.pos[0]
    if (min_y > node.pos[1]): min_y = node.pos[1]
    if (max_x < node.pos[0]): max_x = node.pos[0]
    if (max_y < node.pos[1]): max_y = node.pos[1]

running = True
isCenter = []
tsp = []
background = pygame.image.load("wallllll.jpg")
pokeball = pygame.image.load("pokeball.png")
pokeball = pygame.transform.scale(pokeball, (30, 30))
pika = pygame.image.load("pika.png")
pika = pygame.transform.scale(pika, (45, 45))

agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
gw.g.initAgents(agents)
something = 0


def run():
    something = 0
    i = 1
    while client.is_running():
        something += 1
        click = False

        screen.fill(Color(0, 0, 0))
        screen.blit(background, (0, 0))
        scaled_x = {}
        scaled_y = {}

        for e in gw.g.edges.keys():
            src_x = scale(gw.g.nodes[e[0]].pos[0], 50, screen.get_width() - 50, min_x, max_x)
            src_y = scale(gw.g.nodes[e[0]].pos[1], 50, screen.get_height() - 50, min_y, max_y)
            dest_x = scale(gw.g.nodes[e[1]].pos[0], 50, screen.get_width() - 50, min_x, max_x)
            dest_y = scale(gw.g.nodes[e[1]].pos[1], 50, screen.get_height() - 50, min_y, max_y)
            pygame.draw.line(screen, Color(0, 0, 0), (src_x, src_y), (dest_x, dest_y), width=3)
            draw_arrow("white", [src_x, src_y], [(src_x + dest_x) / 2, (src_y + dest_y) / 2], screen)

        for node in gw.g.nodes.values():
            x = scale(node.pos[0], 50, screen.get_width() - 50, min_x, max_x)
            y = scale(node.pos[1], 50, screen.get_height() - 50, min_y, max_y)
            scaled_x[node.id] = x
            scaled_y[node.id] = y
            gfxdraw.filled_circle(screen, x, y, 10, Color(0, 0, 255))
            gfxdraw.aacircle(screen, x, y, 10, Color(255, 255, 255))
            # screen.blit(pokeball , (x,y))
            if isCenter == node.id:
                gfxdraw.filled_circle(screen, x, y, 10, Color(255, 0, 0))
            if len(tsp) != 0 and id in tsp:
                gfxdraw.filled_circle(screen, x, y, 10, Color(0, 255, 0))
            id_srf = FONT.render(str(node.id), True, pygame.Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

        for i in range(len(tsp) - 1):
            src_x = scale(gw.g.nodes[tsp[i]].pos[0], 50, screen.get_width() - 50, min_x, max_x)
            src_y = scale(gw.g.nodes[tsp[i]].pos[1], 50, screen.get_height() - 50, min_y, max_y)
            dest_x = scale(gw.g.nodes[tsp[i + 1]].pos[0], 50, screen.get_width() - 50, min_x, max_x)
            dest_y = scale(gw.g.nodes[tsp[i + 1]].pos[1], 50, screen.get_height() - 50, min_y, max_y)
            pygame.draw.line(screen, Color(255, 0, 0),
                             (src_x, src_y), (dest_x, dest_y), width=2)
            draw_arrow("red", [src_x, src_y], [(src_x + dest_x) / 2, (src_y + dest_y) / 2], screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.stop()
            elif event.type == pygame.MOUSEBUTTONUP:
                click = True

        pokemons = client.get_pokemons()
        pokemons_obj = json.loads(pokemons, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        pokemons = vars(pokemons_obj)
        gw.g.initPokemons(pokemons)

        agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
        gw.g.initAgents(agents)
        agents = [agent.Agent for agent in agents]
        for a in agents:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=my_scale(
                float(x), x=True), y=my_scale(float(y), y=True))

        for agent in agents:
            screen.blit(pokeball , (int(agent.pos.x), int(agent.pos.y)))
        i = 0
        for p in gw.g.pokemons.values():  # Draws the pokemons
            p_x = my_scale(p.pos[0], x=True)
            p_y = my_scale(p.pos[1], y=True)
            p.edge = gw.g.findPokemonEdge(p)
            # print(p.edge)p
            screen.blit(pika, ((int(p_x), int(p_y))))

        button1 = pygame.Rect(0, 0, 80, 45)
        pygame.draw.rect(screen, (255, 0, 0), button1, border_radius=10)
        font1 = pygame.font.SysFont("Gutman", 20)
        checkkk = client.get_info().split(',')
        check2 = checkkk[3]
        screen.blit((font1.render(check2, True, (255, 255, 255))), (10, 15))

        display.update()

        clock.tick(60)

        # print(agents)

        if (len(gw.g.agents) >= 1):
            t1 = threading.Thread(target=moveAgent(gw.g.agents[0]))
        if (len(gw.g.agents) >= 2):
            t2 = threading.Thread(target=moveAgent(gw.g.agents[1]))
        if (len(gw.g.agents) >= 3):
            t3 = threading.Thread(target=moveAgent(gw.g.agents[2]))


        pygame.time.wait(randint(80, 110))
        client.move()

        if int(client.time_to_end()) < 300:
            print(client.get_info())
            break
    client.stop_connection()
    exit()

def move1agent(agent):
    cities = []
    for pokemon in gw.g.pokemons.values():
        if pokemon.chased == 1:
            continue
        else:
            cities.append(pokemon.edge[0])
            cities.append(pokemon.edge[1])
    path = gw.TSP(cities)[0]
    print(path)
    short = gw.shortest_path(agent['src'], path[0])[1]
    short += path
    i = 0
    agent['dest'] = short[len(short) - 1]
    while (i != len(path)):
        #    if (path[i] == agent['dest']):
        #        agent['dest'] = path[0]
        next_node = path[i]
        client.choose_next_edge(
            '{"agent_id":' + str(agent['id']) + ', "next_node_id":' + str(next_node) + '}')
        i += 1
    return


def moveAgent(agent):
    moves = int(client.get_info().split("moves")[1].split(',')[0][2:])
    print("Moves :"+str(moves))
    if moves == 386:
        print("STOP")
    minDist = sys.maxsize
    for pokemon in gw.g.pokemons.values():
        if pokemon.chased == 1: continue
        x = my_scale(pokemon.pos[0], x=True)
        y = my_scale(pokemon.pos[1], y=True)
        if (gw.g.distance((x, y), (agent['pos'].x, agent['pos'].y)) <= minDist):
            minDist = gw.g.distance((x, y), (agent['pos'].x, agent['pos'].y))
            resultPoke = pokemon
    resultPoke.chased = 1
    path = gw.shortest_path(agent['src'], resultPoke.edge[0])[1]
    path += resultPoke.edge
    resultPokeReversedEdge = []
    resultPokeReversedEdge.append(resultPoke.edge[1])
    resultPokeReversedEdge.append(resultPoke.edge[0])
    next_node = path[1]
    i = 1
    while (i != len(path)):
        if (path[i] == agent['dest']):
            agent['dest'] = resultPoke.edge[1]
        next_node = path[i]
        # print(pokemon.edge)
        client.choose_next_edge(
            '{"agent_id":' + str(agent['id']) + ', "next_node_id":' + str(next_node) + '}')
        i += 1
    return


if __name__ == '__main__':
    x = threading.Thread(target=run())
    # run()
# game over:
