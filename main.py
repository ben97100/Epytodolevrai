import sys
from crud import add_entry, get_entry, delete_entry, update_entry


def main():
    if len(sys.argv) < 4:
        print("Error: Not enough arguments", file=sys.stderr)
        sys.exit(84)
    command = sys.argv[1]
    resource = sys.argv[2]
    args = sys.argv[3:]
    if resource not in ["user", "todo"]:
        print(f"Error: Invalid resource '{resource}'", file=sys.stderr)
        sys.exit(84)
    try:
        if command == "get":
            if len(args) != 1:
                raise ValueError("get requires <id>")
            get_entry(resource, args[0])
        elif command == "del":
            if len(args) != 1:
                raise ValueError("del requires <id>")
            delete_entry(resource, args[0])
        elif command == "add":
            add_entry(resource, args)
        elif command == "update":
            if len(args) < 2:
                raise ValueError("update requires <id> <fields...>")
            update_entry(resource, args[0], args[1:])
        else:
            raise ValueError(f"Unknown command '{command}'")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(84)


if __name__ == "__main__":
    main()
