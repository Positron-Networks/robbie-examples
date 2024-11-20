import subprocess
import os

def main():

    # print the passed environment variable
    print(os.environ['TEST_ENV_VAR'])
    
    # show  GPU information
    subprocess.Popen('nvidia-smi', shell=True)

if __name__ == "__main__":
    main()
