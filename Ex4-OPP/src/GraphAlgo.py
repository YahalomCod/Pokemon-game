import math
import sys
import tkinter
from tkinter import simpledialog
from typing import List
import json

from DiGraph import *
from GraphAlgoInterface import GraphAlgoInterface
from queue import PriorityQueue
import pygame
from pygame import Color, display, gfxdraw
from pygame.constants import RESIZABLE

def scale(data, min_screen, max_screen, min_data, max_data):
    return int(((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen)
def draw_arrow(color, start, end,screen):
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(screen, color, (
        (end[0] + 10 * math.sin(math.radians(rotation)), end[1] + 10 * math.cos(math.radians(rotation))),
        (end[0] + 10 * math.sin(math.radians(rotation - 120)), end[1] + 10 * math.cos(math.radians(rotation - 120))),
        (end[0] + 10 * math.sin(math.radians(rotation + 120)), end[1] + 10 * math.cos(math.radians(rotation + 120)))))


class GraphAlgo(GraphAlgoInterface):

    def __init__(self , g = DiGraph()):
      self.g = g

    """This abstract class represents an interface of a graph."""

    def get_graph(self) -> GraphInterface: #v
        return self.g

    def load_from_json(self, file_name: str) -> bool: #v
        with open(file_name , 'r') as f:
            data = json.load(f)
        for p in data['Nodes']:
            if 'pos' in p:
                self.g.add_node(p['id'] , p['pos'])
            else:
                self.g.add_node(p['id'])
                # self.g.nodes.get(p['id']).pos = tuple([np.random.uniform(0, 35), np.random.uniform(0, 35), 0.0])
        for p in data['Edges']:
            self.g.add_edge(p['src'] , p['dest'] , p['w'])
        return True

    def load_from_jsonString(self, data: str) -> bool: #v
        for p in data['Nodes']:
            p = vars(p)
            if 'pos' in p:
                self.g.add_node(p['id'] , p['pos'])
            else:
                self.g.add_node(p['id'])
                # self.g.nodes.get(p['id']).pos = tuple([np.random.uniform(0, 35), np.random.uniform(0, 35), 0.0])
        for p in data['Edges']:
            p = vars(p)
            self.g.add_edge(p['src'] , p['dest'] , p['w'])
        return True


    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        raise NotImplementedError

    def shortest_path(self, id1: int, id2: int) -> (float, list): #v Needs to reverse the path!!
        if (id1 == id2): return float('inf') , []
        if id1 not in self.g.nodes: return float('inf'),[]
        if id2 not in self.g.nodes: return float('inf'),[]
        D = {v:float('inf') for v in self.g.get_all_v()}
        # print(D)
        visited = []
        parents = {}
        # print(visited)
        D[id1] = 0
        pq =PriorityQueue()
        pq.put((0 , id1))

        while not pq.empty():
            (dist , currV) = pq.get()
            visited.append(currV)

            for neighbor in self.g.nodes:
                if neighbor == currV: continue
                if (currV , neighbor) in self.g.edges:
                    distance = self.g.edges[(currV , neighbor)].getWeight()
                    if neighbor not in visited:
                        prevCost = D[neighbor]
                        newCost = D[currV] + distance
                        if newCost < prevCost:
                            pq.put((newCost , neighbor))
                            D[neighbor] = newCost
                            parents[neighbor] = currV
        child = id2
        src = id1
        path =[]
        path.append(id2)
        for node in parents:
            parent = parents.get(child)
            path.append(parent)
            if parent == src: break
            child = parent
        if id1 not in path:path =[]
        path.reverse()
        return (D[id2] , path)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        allContaintsList = []
        for node in node_lst:
            if node not in self.g.nodes.keys(): return None

        allListPathes = []
        for nodeSrc in node_lst:
            for nodeDest in node_lst:
                if nodeSrc == nodeDest: continue
                allListPathes.append(self.shortest_path(nodeSrc , nodeDest)[1])

        for list in allListPathes:
            result = all(elem in list for elem in node_lst)
            if result:
                allContaintsList.append(list)

        if len(allContaintsList) ==0:
            for list1 in allListPathes:
                if len(list1) == 0 : continue
                for list2 in allListPathes:
                    if list1 == list2:continue
                    if len(list1) != 0 and len(list2) !=0:
                        if (list1[len(list1)-1] == list2[0] and list1[0] != list2[len(list2)-1]):
                                allContaintsList.append(list1[0:len(list1)-1] + list2)

        newAllContains = []
        for list in allContaintsList:
            result = all(elem in list for elem in node_lst)
            if result:
                newAllContains.append(list)
        result = newAllContains[0]
        for list in newAllContains:
            something = self.checkWeightOfPath(list)
            if (self.checkWeightOfPath(list) <= self.checkWeightOfPath(result)):
                result = list


        return result , self.checkWeightOfPath(result)

        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float): #v
        pq = {}
        tmpList ={}
        for nodeSrc in self.g.nodes.keys():
                tmpList = self.DjikstraHelper(nodeSrc)
                pq[nodeSrc] =max(tmpList.values())
                tmpList ={}
        if float('inf') in pq.values(): return (-1 , float('inf'))
        resultKey = min(pq , key=pq.get)
        resultFloat = min(pq.values())
        result = (resultKey , resultFloat)
        return result #v

    def plot_graph(self) -> None:
        WIDTH , HEIGHT = 1080 , 720
        pygame.init()
        screen = display.set_mode((WIDTH , HEIGHT) , depth=32 , flags= RESIZABLE)
        clock = pygame.time.Clock()
        pygame.font.init()
        FONT = pygame.font.SysFont('Arial' , 20 , bold=True)
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = 0
        max_y = 0
        for node in self.g.nodes.values():
            if (min_x > node.pos[0]): min_x = node.pos[0]
            if (min_y > node.pos[1]): min_y = node.pos[1]
            if (max_x < node.pos[0]): max_x = node.pos[0]
            if (max_y < node.pos[1]): max_y = node.pos[1]

        running = True
        isCenter =[]
        tsp =[]

        while running:
            click = False
            screen.fill(Color(0 , 0 ,0))
            scaled_x ={}
            scaled_y ={}
            for node in self.g.nodes.values():
                x = scale(node.pos[0] , 50 , screen.get_width() - 50 , min_x , max_x)
                y = scale(node.pos[1] , 50 , screen.get_height() - 50 , min_y , max_y)
                scaled_x[node.id] = x
                scaled_y[node.id] = y
                gfxdraw.filled_circle(screen , x , y , 10 , Color(0,0,255))
                gfxdraw.aacircle(screen ,x , y , 10 , Color(255,255,255))
                if isCenter == node.id:
                    gfxdraw.filled_circle(screen ,x , y , 10 , Color(255, 0, 0))
                if len(tsp) != 0 and id in tsp:
                    gfxdraw.filled_circle(screen , x ,y , 10 , Color(0,255,0))
                id_srf = FONT.render(str(node.id) , True , pygame.Color(255,255,255))
                rect = id_srf.get_rect(center=(x,y))
                screen.blit(id_srf , rect)

            for e in self.g.edges.keys():
                src_x = scale(self.g.nodes[e[0]].pos[0] , 50 , screen.get_width() -50 , min_x ,max_x)
                src_y = scale(self.g.nodes[e[0]].pos[1] , 50 , screen.get_height() -50 , min_y ,max_y)
                dest_x = scale(self.g.nodes[e[1]].pos[0] , 50 , screen.get_width() -50 , min_x ,max_x)
                dest_y = scale(self.g.nodes[e[1]].pos[1] , 50 , screen.get_height() -50 , min_y ,max_y)
                pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y), width=1)
                draw_arrow("white", [src_x, src_y], [(src_x + dest_x) / 2, (src_y + dest_y) / 2], screen)

            for i in range(len(tsp) - 1):
                src_x = scale(self.g.nodes[tsp[i]].pos[0], 50, screen.get_width() - 50, min_x, max_x)
                src_y = scale(self.g.nodes[tsp[i]].pos[1], 50, screen.get_height() - 50, min_y, max_y)
                dest_x = scale(self.g.nodes[tsp[i + 1]].pos[0], 50, screen.get_width() - 50, min_x, max_x)
                dest_y = scale(self.g.nodes[tsp[i + 1]].pos[1], 50, screen.get_height() - 50, min_y, max_y)
                pygame.draw.line(screen, Color(255, 0, 0),
                                 (src_x, src_y), (dest_x, dest_y), width=2)
                draw_arrow("red", [src_x, src_y], [(src_x + dest_x) / 2, (src_y + dest_y) / 2], screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    click = True
                    print(pygame.mouse.get_pos())
                    for i in range(len(scaled_y)):
                        if (scaled_y[i] + 10 > pygame.mouse.get_pos()[1] > scaled_y[i] - 10) and \
                                (scaled_x[i] + 10 > pygame.mouse.get_pos()[0] > scaled_x[i] - 10):
                            print()

            button1 = pygame.Rect(0, 0, 60, 45)
            pygame.draw.rect(screen, (0, 0, 255), button1, border_radius=10)
            font1 = pygame.font.SysFont("Gutman", 20)
            screen.blit((font1.render('Center', True, (255, 255, 255))), (10, 15))
            button2 = pygame.Rect(65, 0, 60, 45)
            pygame.draw.rect(screen, (0, 0, 255), button2, border_radius=10)
            screen.blit((font1.render('TSP', True, (255, 255, 255))), (75, 15))
            button3 = pygame.Rect(130, 0, 60, 45)
            pygame.draw.rect(screen, (0, 0, 255), button3, border_radius=10)
            screen.blit((font1.render('Shortest Path', True, (255, 255, 255))), (140, 15))
            button4 = pygame.Rect(195, 0, 60, 45)
            pygame.draw.rect(screen, (0, 0, 255), button4, border_radius=10)
            screen.blit((font1.render('Refresh', True, (255, 255, 255))), (205, 15))
            button5 = pygame.Rect(260, 0, 60, 45)
            pygame.draw.rect(screen , (0,0,255) , button5 , border_radius=10)
            screen.blit((font1.render('Load' , True , (255 ,255 ,255))) , (270,15))

            if click:
                pos = pygame.mouse.get_pos()
                if button1.collidepoint(pos):
                    center = self.centerPoint()
                    isCenter = center[0]
                elif button2.collidepoint(pos):
                    ROOT = tkinter.Tk()
                    ROOT.withdraw()
                    cities = simpledialog.askstring(title="TSP",
                                                    prompt="Enter city Id's and space between each city")
                    cities = cities.split()
                    for i in range(len(cities)):
                        cities[i] = int(cities[i])
                    tsp = self.TSP(cities)
                    tkinter.messagebox.showinfo("Length Of Path", tsp[1])
                    tsp = tsp[0]
                elif button3.collidepoint(pos):
                    ROOT = tkinter.Tk()
                    ROOT.withdraw()
                    src = simpledialog.askstring(title="Shortest Path",
                                                 prompt="Source")
                    dest = simpledialog.askstring(title="Shortest Path",
                                                  prompt=["Destination"])
                    tsp = self.shortest_path(int(src), int(dest))
                    print(tsp)
                    tkinter.messagebox.showinfo("Length Of Path", tsp[0])
                    tsp = tsp[1]
                elif button4.collidepoint(pos):
                    isCenter = []
                    tsp = []
                elif button5.collidepoint(pos):
                    ROOT = tkinter.Tk()
                    ROOT.withdraw()
                    isCenter =[]
                    tsp = []
                    self.g.nodes ={}
                    self.g.edges ={}
                    graph = simpledialog.askstring(title="Load" , prompt=["Choose graph"])
                    graph += ".json"
                    self.load_from_json(graph)
            display.update()
            clock.tick(60)

    def DjikstraHelper(self, id1):
        if id1 not in self.g.nodes: return float('inf'),[]
        D = {v:float('inf') for v in self.g.get_all_v()}
        visited = []
        D[id1] = 0
        pq =PriorityQueue()
        pq.put((0 , id1))

        while not pq.empty():
            (dist , currV) = pq.get()
            visited.append(currV)

            for neighbor in self.g.nodes:
                if neighbor == currV: continue
                if (currV , neighbor) in self.g.edges:
                    distance = self.g.edges[(currV , neighbor)].getWeight()
                    if neighbor not in visited:
                        prevCost = D[neighbor]
                        newCost = D[currV] + distance
                        if newCost < prevCost:
                            pq.put((newCost , neighbor))
                            D[neighbor] = newCost
        return D

    def checkWeightOfPath(self , list): #Check the return value !!!
        result = 0
        for i in range(len(list)-1):
            edge = self.g.getEdges().get((list[i] , list[i+1])).getWeight()
            result += edge
        return result