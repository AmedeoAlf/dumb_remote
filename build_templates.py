from os import scandir
from components import events


substitute = {
    "/*EVENTLIST*/": lambda: "\n".join(map(lambda ev: ev.do_codegen(), events))
}


def rfind_or_end(string: str, val: str) -> int:
    pos = string.rfind(val)
    return pos if pos != -1 else len(string)


for fname in scandir("client"):
    if not fname.is_file():
        continue

    if "_t" not in fname.name:
        continue

    new_file = fname.name.replace("_t.", ".")
    new_file = fname.path[:fname.path.rfind(fname.name)] + new_file

    with open(fname.path) as template, open(new_file, "w") as generated:
        for line in template:
            generated.write(
                substitute[line.strip()]() if line.strip() in substitute else line)
