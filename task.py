# importing packages
import argparse
import csv

def Sort(tasks):
        tasks.sort(key= lambda x: int(x[1]))
        return tasks


def csvReader(filename):
    try:
        file = open(filename)
        csv_reader = csv.reader(file)
        tasks = [task for task in csv_reader]
        return tasks
    except FileNotFoundError:
        return []

def csvWriter(filename, tasks):
    try:
        file = open(filename, "w", newline="")
        csv_writer = csv.writer(file)
        csv_writer.writerows(tasks)
        return 0
    except FileNotFoundError:
        return -1

def main():
    # create a parser
    parser = argparse.ArgumentParser(description="Task Manager", add_help=False)
    subparser = parser.add_subparsers(dest="command")

    add = subparser.add_parser("add")
    ls = subparser.add_parser("ls")
    delete = subparser.add_parser("del")
    done = subparser.add_parser("done")
    change = subparser.add_parser("change")
    help = subparser.add_parser("help")
    report = subparser.add_parser("report")

    add.add_argument("add", nargs="*")
    ls.add_argument("ls", action="store_true")
    delete.add_argument("num", nargs="*")
    done.add_argument("num", nargs="*")
    change.add_argument("chg", nargs="*")
    help.add_argument("help", action="store_true")
    report.add_argument("report", action="store_true")

    args = parser.parse_args()

    pending_tasks = []

    alphaASCII = list(range(65,91)) + list(range(97, 123))

    if args.command == "add":
        if not args.add or len(args.add) == 1:
            parser.exit("Error: Missing tasks string. Nothing added!")
        elif ord(args.add[0][0]) in alphaASCII:
            tasks = args.add
            for count, task in enumerate(tasks, start=1):
                pending_tasks.append([task, count])
            csvWriter("Pending Tasks.csv", pending_tasks)
            print(f"Added task: {tasks}")
        elif len(args.add) == 2:
            priority_num = args.add[0]
            task = args.add[1]
            pending_tasks = csvReader("Pending Tasks.csv")
            pending_tasks.append([task, priority_num])
            pending_tasks = Sort(pending_tasks)
            if csvWriter("Pending Tasks.csv", pending_tasks) == 0:
                print(f"Added task: \"{task}\" with priority {priority_num}")
        else:
            parser.exit("Error: SyntaxError...Check help for usage of commands.")
    elif args.command == "ls":
        pending_tasks = csvReader("Pending Tasks.csv")
        if len(pending_tasks) == 0:
            parser.exit("There are no pending tasks!")
        else:
            for count, i in enumerate(pending_tasks, start=1):
                print(f"{count}. {i[0]} [{i[1]}]")

    elif args.command == "del":
        if not args.num:
            parser.exit("Error: Missing NUMBER for deleting tasks.")
        else:
            pending_tasks = csvReader("Pending Tasks.csv")
            for i in range(len(args.num)):
                task_num = int(args.num[i])
                if task_num > len(pending_tasks):
                    parser.exit(f"Error: task with index #{task_num} does not exist. Nothing deleted.")
                else:
                    pending_tasks.pop(task_num-1)
                    if csvWriter("Pending Tasks.csv", pending_tasks) == 0:
                        print(f"Deleted task: #{task_num}")

    elif args.command == "done":
        if not args.num:
            parser.exit("Error: Missing NUMBER for marking task as done.")
        else:
            task_num = int(args.num[0])
            pending_tasks = csvReader("Pending Tasks.csv")
            try:
                task_done = pending_tasks.pop(task_num-1)
                print(task_done)
            except IndexError:
                parser.exit("Error: no incomplete item exists.")
            completed_tasks = csvReader("Completed Tasks.csv")
            completed_tasks.append(task_done)
            completed_tasks = Sort(completed_tasks)
            if csvWriter("Completed Tasks.csv", completed_tasks) == 0:
                csvWriter("Pending Tasks.csv", pending_tasks)
                print("Marked task as done.")

    elif args.command == "change":
        if not args.chg:
            parser.exit("Error: Missing arguments string. Nothing changed!")
        elif len(args.chg) == 2 and ord(args.chg[1][0]) not in alphaASCII:
            task_name = args.chg[0]
            priority_num = args.chg[1]
            pending_tasks = csvReader("Pending Tasks.csv")
            for count,i in enumerate(pending_tasks):
                if pending_tasks[count][0].lower() == task_name.lower():
                    pending_tasks[count][1] = priority_num
                    pending_tasks = Sort(pending_tasks)
                    if csvWriter("Pending Tasks.csv", pending_tasks) == 0:
                        print(f"Changed task: {task_name} to priority #{priority_num}")
                    break
            else:
                parser.exit("Task doesn't exists!!Nothing changed.")
        else:
            parser.exit("Error: SyntaxError...Check help for usage of commands.")

    elif args.command == "help" or not args.command:
        msg = "Usage :-\n$ ./task add 2 \"hello world\"  # Add a new item with priority 2 and text \"hello world\" to the list\n$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order\n$ ./task del INDEX            # Delete the incomplete item with the given index\n$ ./task done INDEX           # Mark the incomplete item with the given index as complete\n$ ./task help                 # Show usage\n$ ./task report               # Statistics"
        print(msg)

    elif args.command == "report":
        pending_tasks = csvReader("Pending Tasks.csv")
        completed_tasks = csvReader("Completed Tasks.csv")
        print(f"Pending : {len(pending_tasks)}")
        for count, i in enumerate(pending_tasks, start=1):
            print(f"{count}. {i[0]} [{i[1]}]")
        print()
        print(f"Completed : {len(completed_tasks)}")
        for count, i in enumerate(completed_tasks, start=1):
            print(f"{count}. {i[0]}")


if __name__ == "__main__":
    main()