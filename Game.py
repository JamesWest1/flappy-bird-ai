import pygame
from Bird import Bird
from Pipe import Pipe
import os
import neat

SCREENHEIGHT = 800
SCREENWIDTH = 500
BACKGROUND = pygame.image.load(os.path.join('images', 'background.PNG'))
BACKGROUND = pygame.transform.rotozoom(BACKGROUND, 0, 2)
GROUND = pygame.image.load(os.path.join('images', 'ground.PNG'))

def eval_genomes(genomes, config):
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    birds = []
    pipes = []
    gs = []
    nns = []
    for _, g in genomes:
        g.fitness = 0
        gs.append(g)
        nn = neat.nn.FeedForwardNetwork.create(g, config)
        nns.append(nn)
        birds.append(Bird(SCREENHEIGHT))
    groundPos = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill("black")
        screen.blit(BACKGROUND, (0,0))
        pipeCount = 0
        for pipe in pipes:
            pipe.update()
            if pipe.offScreen():
                pipes.remove(pipe)
                pipeCount += 1
        for x, g in enumerate(gs):
            gs[x].fitness += pipeCount * 3
        if len(pipes) == 0:
            pipes.append(Pipe(700))
        while len(pipes) < 4:
            lastPipe = pipes[len(pipes) - 1]
            pipes.append(Pipe(lastPipe.x + 400))
        for x, bird in enumerate(birds):
            nextPipe = pipes[0]
            for p in pipes:
                if bird.x - bird.width / 2 < p.x + p.width:
                    nextPipe = p
                    break
            output = nns[x].activate((bird.y, bird.vel, nextPipe.x, nextPipe.height))
            if output[0] > 0.5:
                bird.jump()
        for x, bird in enumerate(birds):
            bird.update(dt)
            if bird.hitGround():
                gs[x].fitness -= 10
                birds.pop(x)
                nns.pop(x)
                gs.pop(x)
        for pipe in pipes:
            pipe.draw(screen)
            for x, bird in enumerate(birds):
                if bird.checkCollision(pipe):
                    gs[x].fitness -= 5
                    birds.pop(x)
                    nns.pop(x)
                    gs.pop(x)
        if len(birds) == 0:
            break
        for bird in birds:
            bird.draw(screen)
        groundPos -= 4
        if groundPos < -100:
            groundPos = 0
        screen.blit(GROUND, (groundPos,730))
        pygame.display.flip()
        dt = clock.tick(60) / 1000

def run(config_file):
    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    pygame.init()
    winner = p.run(eval_genomes, 30)
    pygame.quit()
    quit()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
