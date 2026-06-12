NAME="PassTurtle"
AUTHOR="Dev"


while True:
    commands = input()
    if "go" in commands:
        print("pass", flush=True)
    if "cgp" in commands:
        print(f"name {NAME}", flush=True)
        print(f"author {AUTHOR}", flush=True)
        print("version 1.0", flush=True)
        print("cgpok", flush=True)
    if "setup" in commands:
        print("setupok", flush=True)
    if "ready" in commands:
        print("readyok", flush=True)
    if "rack" in commands or "position" in commands:
        continue
    if "quit" in commands:
        break