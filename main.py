
from typing import List, Dict
import json, os

Task = Dict[str, object]

def show_menu() -> None:
    print("\n=== TEHTÄVÄSOVELLUS ===")
    print("1) Lisää tehtävä")
    print("2) Listaa tehtävät")
    print("3) Merkitse tehtävä tehdyksi")
    print("4) Poista tehtävä")
    print("5) Tallenna (JSON)")
    print("6) Lataa (JSON)")
    print("0) Lopeta")

def ask_int(prompt: str, default: int | None = None) -> int:
    while True:
        raw = input(f"{prompt} ").strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("Anna numero.")

def add_task(tasks: List[Task]) -> None:
    title = input("Tehtävän kuvaus: ").strip()
    if not title:
        print("Kuvaus ei voi olla tyhjä.")
        return
    priority = ask_int("Prioriteetti (1-5, Enter=3):", default=3)
    priority = max(1, min(priority, 5))
    tasks.append({"title": title, "priority": priority, "done": False})
    print("Tehtävä lisätty.")

def list_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("Ei tehtäviä.")
        return
    sorted_tasks = sorted(tasks, key=lambda t: (t["done"], t["priority"]))
    print("\n#  Done Pri  Title")
    print("-- ---- ---  -----------------------------")
    for i, t in enumerate(sorted_tasks, start=1):
        done = "X" if t["done"] else " "
        print(f"{i:>2}  [{done}]  {t['priority']:>3}  {t['title']}")

def mark_done(tasks: List[Task]) -> None:
    if not tasks:
        print("Ei tehtäviä.")
        return
    list_tasks(tasks)
    idx = ask_int("Mikä # merkitään tehdyksi?")
    sorted_indices = sorted(range(len(tasks)), key=lambda i: (tasks[i]["done"], tasks[i]["priority"]))
    if 1 <= idx <= len(sorted_indices):
        real_index = sorted_indices[idx - 1]
        tasks[real_index]["done"] = True
        print("Merkitty tehdyksi.")
    else:
        print("Virheellinen valinta.")

def remove_task(tasks: List[Task]) -> None:
    if not tasks:
        print("Ei tehtäviä.")
        return
    list_tasks(tasks)
    idx = ask_int("Mikä # poistetaan?")
    sorted_indices = sorted(range(len(tasks)), key=lambda i: (tasks[i]["done"], tasks[i]["priority"]))
    if 1 <= idx <= len(sorted_indices):
        real_index = sorted_indices[idx - 1]
        removed = tasks.pop(real_index)
        print(f"Poistettu: {removed['title']}")
    else:
        print("Virheellinen valinta.")

def save_tasks(tasks: List[Task], path: str = "tasks.json") -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    print(f"Tallennettu: {path}")

def load_tasks(path: str = "tasks.json") -> List[Task]:
    if not os.path.exists(path):
        print("Tiedostoa ei löydy, aloitetaan tyhjällä listalla.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [{
            "title": str(item.get("title", "")),
            "priority": int(item.get("priority", 3)),
            "done": bool(item.get("done", False))
        } for item in data]
    print("Virheellinen tiedosto, aloitetaan tyhjällä listalla.")
    return []

def main() -> None:
    tasks: List[Task] = []
    while True:
        show_menu()
        choice = input("Valinta: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            remove_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
        elif choice == "6":
            tasks = load_tasks()
        elif choice == "0":
            print("Hei hei!")
            break
        else:
            print("Tuntematon komento.")

if __name__ == "__main__":
    main()
