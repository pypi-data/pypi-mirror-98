from setuptools import setup

ld=\
"""
Rejoice, Linux users, for you no longer have to:

`mv forbidden_memes.txt ~/.recycling/fordbidden_memes.txt`

and get an error:

`File exists or something lol`

Command Example
---------------
Command:

`python3 -m quicktrash 43245_ways_to_kill_barney.txt some_manifesto.pdf`

Output:
```
/home/babybop/.quicktrash/0x2/home/babybop/Documents/43245_ways_to_kill_barney.txt
/home/babybop/.quicktrash/0x2/home/babybop/Documents/some_manifesto.pdf
```

Python Examples
---------------
Using context:
```python
import quicktrash

with quicktrash.Trash("example-trashdir") as trash:
    trash.recycle("example-file.txt")
```
Using next()
```python
import quicktrash

tr = quicktrash.Trash("example-trashdir")
trlet:quicktrash.Trashlet = next(tr)
trlet.recycle("example-file.txt")
```
"""

setup(
    name='quicktrash',
    packages=["quicktrash"],
    version='1.0.2',
    description="EzPz Recycling",
    long_description=ld,
    long_description_content_type="text/markdown",
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["filelock~=3.0"]
)