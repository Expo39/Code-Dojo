def split_names(Person):
    changed = []
    for person in Person.objects.filter(first_name=""):
        words = person.full_name.split()
        if not words:
            continue
        if len(words) == 1:
            person.first_name, person.last_name = words[0], ""
        else:
            person.first_name, person.last_name = " ".join(words[:-1]), words[-1]
        changed.append(person)
    Person.objects.bulk_update(changed, ["first_name", "last_name"])
    return len(changed)
