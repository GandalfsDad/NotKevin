#!/usr/bin/env python
from NotKevin.Agent import Agent
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clear", dest = "clear",help="Clears the memory before running", action="store_true")

def cli():
    args = parser.parse_args()
    clear = False
    if args.clear:
        clear = True
    agent = Agent(autosave=True)
    
    if clear:
        agent.clear_memory(save=True)
    agent.run()

if __name__ == "__main__":
    cli()

