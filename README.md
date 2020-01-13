# Compiler project: LitUml

## Quick start

### Requirements
* Python3.5 +

### Install

* `git clone https://github.com/RoscaS/compiler_lit-uml`
* `pip install -r requirements.txt`

On linux you might need to specify `pip3` instead of `pip`

### Test it
Inside the root folder:
* `python parser.py input/XX.lituml` where `XX` are two digits
refering to a file inside `/input` to display lexems.
* `python parser.py input/XX.lituml` where `XX` are two digits
refering to a file inside `/input` to generate the AST tree inside /out folder.
* `python interpreter.py input/XX.lituml` where `XX` are two digits
 refering to a file inside `/input` to generate an UML diagram inside /out
  folder.


On linux you might need to specify `python3` instead of `python`
See /docs to read about syntax specifications.

### Try yourself

Lets déclare a class (It must be followed by `("")` and first empty bloc

```
{
    House("")
}

```

Now, we could add a stereotype (or whatever else) if needed to caracterise it:

```
{
    House("<<abstract>>")
}

```

To add an attribute, we must first add a bloc and put it inside (the format
 inside double quotes doesn't matter):

```
{
    House("<<abstract>>"),
    [
        "- name : string",
    ]
}

```

Some methods magic (again, format it however you want):
```
{
    House("<<abstract>>"),
    [
        "- name : string",
    ],
    [
        "+ sell(): float",
        "+ clean()"
    ]
}
```

You can add how many blocs you want and the format doesn't matter:
```
{
    House("<<abstract>>"),
    [
        "- name : string",
    ],
    [
        "+ sell(): float",
        "+ clean()"
    ],
    [ "weird stuff", "some more" ]
}
```


Let's remove that thing and add a new class (you don't need to put a coma
 between two definitions):

```
{
    House("<<abstract>>"),
    [
        "- name : string",
    ],
    [
        "+ sell(): float",
        "+ clean()"
    ]
}
{
    Room(""),
    [
        "- size : double",
    ]
}

```

To start using the declared classes, let's add a triple dash: `---`:

```
{
    House("<<abstract>>"),
    [
        "- name : string",
    ],
    [
        "+ sell(): float",
        "+ clean()"
    ]
}
{
    Room(""),
    [
        "- size : double",
    ]
}

---


```

Now we can create relationships between our classes:

```
{
    House("<<abstract>>"),
    [
        "- name : string",
    ],
    [
        "+ sell(): float",
        "+ clean()"
    ]
}
{
    Room(""),
    [
        "- size : double",
    ]
}

---

House <-- Room
```

That's it. For now.
