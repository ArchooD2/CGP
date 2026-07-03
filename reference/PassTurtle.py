NAME = "PassTurtle"
AUTHOR = "Dev"


while True:
    command = input().strip()
    if command.startswith("go"):
        print("bestmove pass", flush=True)
    if command == "cgp":
        print(f"name {NAME}", flush=True)
        print(f"author {AUTHOR}", flush=True)
        print("version 1.0", flush=True)
        print("cgpok", flush=True)
    if command.startswith("setup"):
        print("setupok", flush=True)
    if command == "ready":
        print("readyok", flush=True)
    if command.startswith(("rack", "position", "unseen")):
        continue
    if command == "quit":
        break
