import os, sys, argparse

class Args:
    def __init__(self):
        self.argc = len(sys.argv)
        self.argv = sys.argv
    def getArgv(self):
        return self.argv
    def getArgc(self):
        return self.argc



def dockerService():
    os.system("docker-compose -f Services/compose.yml up -d --build")

def main(args: Args):
    if(args.getArgc() == 1):
        dockerService()
    if(args.getArgc() == 2):
        if(args.getArgv()[1] == "stop"):
            os.system("docker-compose -f Services/compose.yml down")
    print("http://localhost:5173")
    
    
if __name__ == "__main__":
    print(__name__)
    main(Args())
