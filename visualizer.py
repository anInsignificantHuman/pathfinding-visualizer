import sys, math, copy, time, pygame, pygame.midi
from random import randint
from random import random as randfloat
from typing import Any
from collections import deque
from pq import PQ

pygame.init()
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(71)
GRAY = (18, 18, 18)
WHITE = (255, 255, 255)
RED = (207, 102, 121)
YELLOW = (255, 224, 130)
GREEN = (3, 218, 198)
BLUE = (144, 202, 249)
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
block_size = 30

def create_graph(rows: int, cols: int):  
    graph: dict = {}
    for i in range(rows * cols):  
        r, l, u, d = i + 1, i - 1, i - cols, i + cols
        # Top left corner
        if i == 0:
            graph[i] = [r, d]

        # Top right corner
        elif i == cols - 1:  
            graph[i] = [d, l]
        
        # Bottom left corner
        elif i == cols * (rows - 1):  
            graph[i] = [u, r]

        # Bottom right corner
        elif i == cols * rows - 1:  
            graph[i] = [u, l]
        
        # Left edges
        elif i % cols == 0:  
            graph[i] = [u, r, d] 

        # Right edges
        elif i % cols == cols - 1:  
            graph[i] = [u, d, l]

        # Top edges 
        elif i in range(cols):  
            graph[i] = [r, d, l] 

        # Bottom edges 
        elif i in range(cols * (rows - 1), cols * rows):  
            graph[i] = [u, r, l]

        # Centers  
        else:  
            graph[i] = [u, r, d, l]         
    return graph

graph: dict = create_graph(HEIGHT // block_size, WIDTH // block_size)
barriers = set({})

def sound(num: int, target: int):  
    dist = sum([abs(coord(num)[i] - coord(target)[i]) for i in range(2)])
    note = int(dist / ((WIDTH // block_size) * (HEIGHT // block_size)) * 57) + 60
    player.note_on(note, 127)
    time.sleep(0.005)
    player.note_off(note, 127)

def drawRect(color: tuple[int, int, int], num: int):
    pygame.draw.rect(SCREEN, color, coord(num), 0)
    pygame.draw.rect(SCREEN, WHITE, coord(num), 1)

def setBarrier(graph: dict, num: int):
    drawRect(WHITE, num)
    barriers.add(num)

def dist(p1: int, p2: int):  
    return sum([abs(coord(p1)[i] - coord(p2)[i]) for i in range(2)])

def greedy(graph: dict, start: Any, target: Any):  
    found = False
    visited = set({start})
    path = [start] 
    queue = PQ(lambda f: dist(f, target))
    queue.append(start)
    queue.add_path(start, path)
    drawRect(RED, start)
    drawRect(GREEN, target)

    while (len(queue.arr)):
        current = queue.pop()
        path = queue.get_path(current)

        for neighbor in graph[current]:  
            if neighbor not in visited and neighbor not in barriers: 
                if neighbor == target:
                    queue.arr.clear()
                    found = True
                    break
                else: 
                    visited.add(neighbor)
                    queue.add_path(neighbor, path + [neighbor])
                    queue.append(neighbor)
                    drawRect(YELLOW, neighbor)
                    time.sleep(0.0001)
                    pygame.display.flip()
                    drawRect(BLUE, neighbor)
                    sound(neighbor, target)
                pygame.display.flip()
    
    if found:
        for i in path[1:]:
            drawRect(YELLOW, i)
            sound(i, target)
            time.sleep(0.001)
            pygame.display.flip()

def bfs(graph: dict, start: Any, target: Any):  
    found = False
    visited = set({start}) 
    path = [start]
    queue = deque([[start]])
    drawRect(RED, start)
    drawRect(GREEN, target)

    while (len(queue)):
        path = queue.popleft()

        for neighbor in graph[path[-1]]:  
            if neighbor not in visited and neighbor not in barriers: 
                if neighbor == target: 
                    queue.clear()
                    found = True
                    break
                else:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
                    drawRect(YELLOW, neighbor)
                    time.sleep(0.0005)
                    pygame.display.flip()
                    drawRect(BLUE, neighbor)
                    sound(neighbor, target)
                pygame.display.flip()

    if found:
        for i in path[1:]:
            drawRect(YELLOW, i)
            sound(i, target)
            time.sleep(0.001)
            pygame.display.flip()

# Starts at the root node and explores as far as possible, 
# backtracking if the target is not found.
# Worst time complexity: O(|V| + |E|)
def dfs(graph: dict, start: Any, target: Any):  
    visited = set({start})
    path = [start]
    stack = [[i, path + [i]] for i in copy.deepcopy(graph[start])]
    drawRect(RED, start)
    drawRect(GREEN, target)

    while (len(stack)): 
        current, path = stack.pop(0)
        if current not in barriers:
            if current == target:  
                break
            if current not in visited:
                visited.add(current) 
                drawRect(YELLOW, current)
                pygame.display.flip()
                time.sleep(0.0001)
                drawRect(BLUE, current)
                sound(current, target)
                for neighbor in reversed(graph[current]):
                    stack.insert(0, [neighbor, path + [neighbor]])
        pygame.display.flip()

    for i in path[1:-1]:
        drawRect(YELLOW, i)
        sound(i, target)
        time.sleep(0.0005)
        pygame.display.flip()

def drawGrid():
    SCREEN.fill(GRAY)
    for x in range(WIDTH // block_size):  
        for y in range(HEIGHT // block_size):  
            pygame.draw.rect(SCREEN, WHITE, (x * block_size, y * block_size, block_size, block_size), 1)
    pygame.display.flip()

def coord(num: int):  
    x = num % (WIDTH // block_size) * block_size
    try: 
        y = (num // (WIDTH // block_size)) * block_size
    except ZeroDivisionError:
        y = 0
    return (x, y, block_size, block_size)

def num(coord: tuple[int, int]):
    x = coord[0] // block_size 
    y = coord[1] // block_size * (WIDTH // block_size) 
    return y + x

def main(): 
    maxNum = WIDTH * HEIGHT // block_size ** 2 - 1
    start, end = None, None
    drawGrid()
    while True:
        for event in pygame.event.get():  
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                pos = num(pygame.mouse.get_pos())
                if start is None:
                    start = pos
                    drawRect(RED, start)
                elif end is None and pos != start:
                    end = pos
                    drawRect(GREEN, end)
                elif pos != start and pos != end:
                    setBarrier(graph, pos)
                pygame.display.flip()
            elif pygame.mouse.get_pressed(num_buttons=3)[2]:
                pos = num(pygame.mouse.get_pos())
                drawRect(GRAY, pos)
                if pos == start:
                    start = None
                elif pos == end:
                    end = None
                elif pos in barriers:
                    barriers.remove(pos)
                pygame.display.flip()
            elif event.type == pygame.KEYDOWN:
                if start is not None and end is not None:
                    if event.key == pygame.K_1:
                        drawGrid()
                        for i in barriers:
                            setBarrier(graph, i)
                            time.sleep(0.0005)
                            pygame.display.flip()
                        greedy(graph, start, end)
                    elif event.key == pygame.K_2:
                        drawGrid()
                        for i in barriers:
                            setBarrier(graph, i)
                            time.sleep(0.0005)
                            pygame.display.flip()
                        bfs(graph, start, end)
                    elif event.key == pygame.K_3:
                        drawGrid()
                        for i in barriers:
                            setBarrier(graph, i)
                            time.sleep(0.0005)
                            pygame.display.flip()
                        dfs(graph, start, end)
                    if event.key == pygame.K_ESCAPE:
                        return
                if event.key == pygame.K_BACKSPACE:
                    start, end = None, None
                    barriers.clear()
                    drawGrid()
            elif event.type == pygame.QUIT:
                return      

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit(0)