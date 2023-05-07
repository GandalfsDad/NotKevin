#!/usr/bin/env python
from NotKevin.Agent import Agent
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clear", dest = "clear",help="Clears the memory before running", action="store_true")
parser.add_argument("-n", "--name", dest = "name", help="Name of the agent", default="NotKevin")
parser.add_argument("-h", "--headless", dest = "nosave", help="Does not save the memory", action="store_true")

def cli():
    args = parser.parse_args()
    clear = False
    if args.clear:
        clear = True

    autosave = True
    if args.nosave:
        autosave = False

    agent = Agent(name=args.name, autosave=autosave)
    
    if clear:
        agent.clear_memory(save=True)
    agent.run()

if __name__ == "__main__":
    cli()

