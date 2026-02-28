import os
import time
from utils.auto_updater import get_all_texts, refresh_vector_store
from vector_store.fiass_db import FAISSVectorStore

LOG_PATH = "vector_store/last_update.txt"

def log_last_update():
    with open(LOG_PATH, "w") as f:
        f.write(str(time.time()))

def read_last_update():
    if not os.path.exists(LOG_PATH):
        return "Never"
    with open(LOG_PATH, "r") as f:
        timestamp = float(f.read().strip())
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def view_sources():
    print("\nCurrent Sources in `sources/`:")
    for fname in os.listdir("sources"):
        if fname.endswith(".txt"):
            print(" -", fname)

def view_index_info():
    store = FAISSVectorStore()
    print(f"\nCurrent vector DB has {len(store.text_chunks)} chunks.")

def manual_update():
    print("\nManually updating vector store...")
    refresh_vector_store()
    log_last_update()
    print("Update complete!")

def dashboard():
    while True:
        print("Knowledge Base Admin CLI")
        print("============================")
        print("1. View Sources")
        print("2. View DB Stats")
        print("3. View Last Update Time")
        print("4. Trigger Manual Update")
        print("5. Exit")

        choice = input("Enter option [1–5]: ").strip()
        if choice == "1":
            view_sources()
        elif choice == "2":
            view_index_info()
        elif choice == "3":
            print("\nLast Update:", read_last_update())
        elif choice == "4":
            manual_update()
        elif choice == "5":
            print("Exiting Admin CLI...")
            break
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    dashboard()

