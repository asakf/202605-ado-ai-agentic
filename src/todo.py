import argparse
import json
from pathlib import Path
from typing import List, Dict

TASKS_FILE = Path(__file__).resolve().parent.parent / "tasks.json"


def load_tasks() -> List[Dict]:
    if not TASKS_FILE.exists():
        return []
    with TASKS_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks: List[Dict]):
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TASKS_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(title: str):
    tasks = load_tasks()
    next_id = max((t.get("id", 0) for t in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{next_id}: {title}")


def list_tasks(show_all: bool = False):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        if not show_all and t.get("done"):
            continue
        status = "x" if t.get("done") else " "
        print(f"[{status}] {t.get('id')}: {t.get('title')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="Simple todo CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Title of the task")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true", help="Show completed tasks too")

    return parser


def main(argv: List[str] = None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks(show_all=args.all)


if __name__ == "__main__":
    main()
