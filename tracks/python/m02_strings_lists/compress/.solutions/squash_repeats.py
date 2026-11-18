def squash_repeats(lines):
    result = []
    if not lines:
        return result
    current, count = lines[0], 1
    for line in lines[1:]:
        if line == current:
            count += 1
        else:
            result.append(current if count == 1 else f"{current} (x{count})")
            current, count = line, 1
    result.append(current if count == 1 else f"{current} (x{count})")
    return result
