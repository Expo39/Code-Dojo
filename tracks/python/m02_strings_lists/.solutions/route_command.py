def route_command(command):
    match command.lower().split():
        case ["go", direction]:
            return f"You walk {direction}."
        case ["take", *item] if item:
            return f"You take the {' '.join(item)}."
        case ["look"]:
            return "You look around."
        case ["quit"]:
            return "Goodbye."
        case _:
            return "I don't understand that."
