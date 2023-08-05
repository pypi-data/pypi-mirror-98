#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Where the Bugs are" - a chapter of "The Debugging Book"
# Web site: https://www.debuggingbook.org/html/ChangeCounter.html
# Last change: 2021-03-09 18:23:35+01:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Debugging Book - Where the Bugs are

This file can be _executed_ as a script, running all experiments:

    $ python ChangeCounter.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from debuggingbook.ChangeCounter import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.debuggingbook.org/html/ChangeCounter.html

This chapter provides two classes `ChangeCounter` and `FineChangeCounter` that allow to mine and visualize the distribution of changes in a given `git` repository.

`ChangeCounter` is initialized as

change_counter = ChangeCounter(repository)

where `repository` is either 

* a _directory_ containing a `git` clone (i.e., it contains a `.git` directory)
* the URL of a `git` repository.

Additional arguments are being passed to the underlying `RepositoryMining` class from the [PyDriller](https://pydriller.readthedocs.io/) Python package. A `filter` keyword argument, if given, is a predicate that takes a modification (from PyDriller) and returns True if it should be included.

In a change counter, all elements in the repository are represented as _nodes_ – tuples $(f_1, f_2, ..., f_n)$ that denote a _hierarchy_: Each $f_i$ is a directory holding $f_{i+1}$, with $f_n$ being the actual file.

A `change_counter` provides a number of attributes. `changes` is a mapping of nodes to the number of changes in that node:

>>> change_counter.changes[('README.md',)]

11

The `messages` attribute holds all commit messages related to that node:

>>> change_counter.messages[('README.md',)]

['first commit',
 'Adjusted to debuggingbook',
 'New Twitter handle: @Debugging_Book',
 'Doc update',
 'Doc update',
 'Doc update',
 'Doc update',
 'Added link to author homepage',
 'Doc update',
 'Doc update',
 'Doc update']

The `sizes` attribute holds the (last) size of the respective element:

>>> change_counter.sizes[('README.md',)]

11221

`FineChangeCounter` acts like `ChangeCounter`, but also retrieves statistics for elements _within_ the respective files; it has been tested for C, Python, and Jupyter Notebooks and should provide sufficient results for programming languages with similar syntax.

The `map()` method of `ChangeCounter` and `FineChangeCounter` produces an interactive tree map that allows to explore the elements of a repository. The redder (darker) a rectangle, the more changes it has seen; the larger a rectangle, the larger its size in bytes.

>>> fine_change_counter.map()


   

The included classes offer several methods that can be overridden in subclasses to customize what to mine and how to visualize it. See the chapter for details.

Here are all the classes defined in this chapter:

For more details, source, and documentation, see
"The Debugging Book - Where the Bugs are"
at https://www.debuggingbook.org/html/ChangeCounter.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'debuggingbook'


# Where the Bugs are
# ==================

if __name__ == '__main__':
    print('# Where the Bugs are')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo("Aifq0JOc1Jc")

if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from . import Tracking

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Mining Change Histories
## -----------------------

if __name__ == '__main__':
    print('\n## Mining Change Histories')



## Mining with PyDriller
## ---------------------

if __name__ == '__main__':
    print('\n## Mining with PyDriller')



from pydriller import RepositoryMining  # https://pydriller.readthedocs.io/
from pydriller.domain.commit import Commit

import os

from typing import Sequence, Any, Callable, Optional, Type, Tuple, Any
from typing import Dict, Union, Set, List, FrozenSet, cast

def current_repo() -> Optional[str]:
    path = os.getcwd()
    while True:
        if os.path.exists(os.path.join(path, '.git')):
            return os.path.normpath(path)

        # Go one level up
        new_path = os.path.normpath(os.path.join(path, '..'))
        if new_path != path:
            path = new_path
        else:
            return None

    return None

if __name__ == '__main__':
    current_repo()

if __name__ == '__main__':
    book_miner = RepositoryMining(current_repo())

if __name__ == '__main__':
    book_commits = book_miner.traverse_commits()
    book_first_commit = next(book_commits)

if __name__ == '__main__':
    [attr for attr in dir(book_first_commit) if not attr.startswith('_')]

if __name__ == '__main__':
    book_first_commit.msg

if __name__ == '__main__':
    [attr for attr in dir(book_first_commit.author) if not attr.startswith('_')]

if __name__ == '__main__':
    book_first_commit.author.name, book_first_commit.author.email

if __name__ == '__main__':
    book_first_commit.modifications

if __name__ == '__main__':
    [attr for attr in dir(book_first_commit.modifications[0]) if not attr.startswith('_')]

if __name__ == '__main__':
    book_first_commit.modifications[0].new_path

if __name__ == '__main__':
    print(book_first_commit.modifications[0].source_code)

if __name__ == '__main__':
    print(book_first_commit.modifications[0].source_code_before)

if __name__ == '__main__':
    book_second_commit = next(book_commits)

if __name__ == '__main__':
    [m.new_path for m in book_second_commit.modifications]

if __name__ == '__main__':
    readme_modification = [m for m in book_second_commit.modifications if m.new_path == 'README.md'][0]

if __name__ == '__main__':
    print(readme_modification.source_code_before)

if __name__ == '__main__':
    print(readme_modification.source_code[:400])

if __name__ == '__main__':
    print(readme_modification.diff[:100])

if __name__ == '__main__':
    readme_modification.diff_parsed['added'][:10]

## Counting Changes
## ----------------

if __name__ == '__main__':
    print('\n## Counting Changes')



if __name__ == '__main__':
    tuple('debuggingbook/notebooks/ChangeExplorer.ipynb'.split('/'))

Node = Tuple

class ChangeCounter:
    """Count the number of changes for a repository."""

    def __init__(self, repo: str, *, 
                 filter: Optional[Callable[[Commit], bool]] = None, 
                 log: bool = False, 
                 **kwargs: Any) -> None:
        """
        Constructor.
        `repo` is a git repository (as URL or directory).
        `filter` is a predicate that takes a modification and returns True 
        if it should be considered (default: consider all).
        `log` turns on logging if set.
        `kwargs` are passed to the `RepositoryMining()` constructor.
        """
        self.repo = repo
        self.log = log

        if filter is None:
            def filter(m: Commit) -> bool:
                return True
        assert filter is not None

        self.filter = filter

        # A node is an tuple (f_1, f_2, f_3, ..., f_n) denoting
        # a folder f_1 holding a folder f_2 ... holding a file f_n.

        # Mapping node -> #of changes
        self.changes: Dict[Node, int] = {}

         # Mapping node -> list of commit messages
        self.messages: Dict[Node, List[str]] = {}

        # Mapping node -> last size seen
        self.sizes: Dict[Node, int] = {}

        # All hashes already considered
        self.hashes: Set[str] = set()

        self.mine(**kwargs)

class ChangeCounter(ChangeCounter):
    def mine(self, **kwargs: Any) -> None:
        """Gather data from repository. To be extended in subclasses."""
        miner = RepositoryMining(self.repo, **kwargs)

        for commit in miner.traverse_commits():
            for m in commit.modifications:
                m.hash = commit.hash
                m.committer = commit.committer
                m.committer_date = commit.committer_date
                m.msg = commit.msg

                if self.include(m):
                    self.update_stats(m)

class ChangeCounter(ChangeCounter):
    def include(self, m: Commit) -> bool:
        """
        Return True if the modification `m` should be included
        (default: the `filter` predicate given to the constructor).
        To be overloaded in subclasses.
        """
        return self.filter(m)

class ChangeCounter(ChangeCounter):
    def update_stats(self, m: Commit) -> None:
        """Update counters with modification `m`. Can be extended in subclasses."""
        if not m.new_path:
            return

        node = tuple(m.new_path.split('/'))

        if m.hash not in self.hashes:
            self.hashes.add(m.hash)
            self.update_size(node, len(m.source_code) if m.source_code else 0)
            self.update_changes(node, m.msg)

        self.update_elems(node, m)

class ChangeCounter(ChangeCounter):
    def update_size(self, node: Tuple, size: int) -> None:
        """Update counters for `node` with `size`. Can be extended in subclasses."""
        self.sizes[node] = size

class ChangeCounter(ChangeCounter):
    def update_changes(self, node: Tuple, commit_msg: str) -> None:
        """
        Update stats for `node` changed with `commit_msg`.
        Can be extended in subclasses.
        """
        self.changes.setdefault(node, 0)
        self.changes[node] += 1

        self.messages.setdefault(node, [])
        self.messages[node].append(commit_msg)

class ChangeCounter(ChangeCounter):
    def update_elems(self, node: Tuple, m: Commit) -> None:
        """
        Update counters for subelements of `node` with modification `m`.
        To be defined in subclasses.
        """
        pass

DEBUGGINGBOOK_REPO = current_repo()

if __name__ == '__main__':
    DEBUGGINGBOOK_REPO

def debuggingbook_change_counter(cls: Type) -> Any:
    """Instantiate a ChangeCounter (sub)class `cls` with the debuggingbook repo"""

    def filter(m: Commit) -> bool:
        """Do not include the `docs/` directory; it only holds Web pages"""
        return m.new_path and not m.new_path.startswith('docs/')

    return cls(DEBUGGINGBOOK_REPO, filter=filter)

from .Timer import Timer

if __name__ == '__main__':
    with Timer() as t:
        change_counter = debuggingbook_change_counter(ChangeCounter)

    t.elapsed_time()

if __name__ == '__main__':
    list(change_counter.changes.keys())[:10]

if __name__ == '__main__':
    change_counter.changes[('Chapters.makefile',)]

if __name__ == '__main__':
    change_counter.messages[('Chapters.makefile',)]

if __name__ == '__main__':
    for node in change_counter.changes:
        assert len(change_counter.messages[node]) == change_counter.changes[node]

if __name__ == '__main__':
    change_counter.sizes[('Chapters.makefile',)]

## Visualizing Past Changes
## ------------------------

if __name__ == '__main__':
    print('\n## Visualizing Past Changes')



import easyplotly as ep
import plotly.graph_objects as go

import math

class ChangeCounter(ChangeCounter):
    def map_node_sizes(self) -> Dict[Node, Union[int, float]]:
        """Return a mapping of nodes to sizes. Can be overloaded in subclasses."""
        # Default: use log scale
        return {node: math.log(self.sizes[node]) if self.sizes[node] else 0
                for node in self.sizes}

        # Alternative: use sqrt size
        return {node: math.sqrt(self.sizes[node]) for node in self.sizes}

        # Alternative: use absolute size
        return self.sizes

class ChangeCounter(ChangeCounter):
    def map_node_color(self, node: Node) -> Optional[int]:
        """Return a color of the node, as a number. Can be overloaded in subclasses."""
        if node and node in self.changes:
            return self.changes[node]
        return None

class ChangeCounter(ChangeCounter):
    def map_node_text(self, node: Node) -> Optional[str]:
        """
        Return the text to be shown for the node (default: #changes).
        Can be overloaded in subclasses.
        """
        if node and node in self.changes:
            return str(self.changes[node])
        return None

class ChangeCounter(ChangeCounter):
    def map_hoverinfo(self) -> str:
        """
        Return the text to be shown when hovering over a node.
        To be overloaded in subclasses.
        """
        return 'label+text'

    def map_colorscale(self) -> str:
        """
        Return the colorscale for the map. To be overloaded in subclasses.
        """
        return 'YlOrRd'

class ChangeCounter(ChangeCounter):
    def map(self) -> go.Figure:
        """Produce an interactive tree map of the repository."""
        treemap = ep.Treemap(
                     self.map_node_sizes(),
                     text=self.map_node_text,
                     hoverinfo=self.map_hoverinfo(),
                     marker_colors=self.map_node_color,
                     marker_colorscale=self.map_colorscale(),
                     root_label=self.repo,
                     branchvalues='total'
                    )

        fig = go.Figure(treemap)
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))

        return fig

if __name__ == '__main__':
    change_counter = debuggingbook_change_counter(ChangeCounter)

if __name__ == '__main__':
    change_counter.map()

if __name__ == '__main__':
    all_nodes = list(change_counter.changes.keys())
    all_nodes.sort(key=lambda node: change_counter.changes[node], reverse=True)
    [(node, change_counter.changes[node]) for node in all_nodes[:4]]

if __name__ == '__main__':
    all_notebooks = [node for node in change_counter.changes.keys()
                     if len(node) == 2 and node[1].endswith('.ipynb')]
    all_notebooks.sort(key=lambda node: change_counter.changes[node], reverse=True)

from .bookutils import quiz

if __name__ == '__main__':
    quiz("Which two notebooks have seen the most changes over time?",
        [
            f"`{all_notebooks[0][1].split('.')[0]}`",
            f"`{all_notebooks[3][1].split('.')[0]}`",
            f"`{all_notebooks[1][1].split('.')[0]}`",
            f"`{all_notebooks[2][1].split('.')[0]}`",
        ], '[1234 % 3, 3702 / 1234]')

if __name__ == '__main__':
    all_notebooks[0][1].split('.')[0], all_notebooks[1][1].split('.')[0]

## Counting Past Fixes
## -------------------

if __name__ == '__main__':
    print('\n## Counting Past Fixes')



class FixCounter(ChangeCounter):
    """
    Count the fixes for files in the repository.
    Fixes are all commits whose message starts with the word 'Fix: '
    """

    def include(self, m: Commit) -> bool:
        """Include all modifications whose commit messages start with 'Fix:'"""
        return super().include(m) and m and m.msg.startswith("Fix:")

class FixCounter(FixCounter):
    def map_node_text(self, node: Node) -> str:
        if node and node in self.messages:
            return "<br>".join(self.messages[node])
        return ""

    def map_hoverinfo(self) -> str:
        return 'label'

if __name__ == '__main__':
    fix_counter = debuggingbook_change_counter(FixCounter)

if __name__ == '__main__':
    fix_counter.map()

## Counting Fine-Grained Changes
## -----------------------------

if __name__ == '__main__':
    print('\n## Counting Fine-Grained Changes')



### Mapping Elements to Locations

if __name__ == '__main__':
    print('\n### Mapping Elements to Locations')



import magic

if __name__ == '__main__':
    magic.from_buffer('''
#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Hello, world!\n")
}
''')

if __name__ == '__main__':
    magic.from_buffer('''
def foo():
    print("Hello, world!")
''')

if __name__ == '__main__':
    magic.from_buffer(open(os.path.join(current_repo(),   # type: ignore
                                        'notebooks',
                                        'Assertions.ipynb')).read())

import re

from typing import Pattern

DELIMITERS: List[Tuple[Pattern, Pattern, Pattern]] = [
    (
        # Python
        re.compile(r'^python.*'),

        # Beginning of element
        re.compile(r'^(async\s+)?(def|class)\s+(?P<name>\w+)\W.*'),

        # End of element
        re.compile(r'^[^#\s]')
    ),
    (
        # Jupyter Notebooks
        re.compile(r'^(json|exported sgml|jupyter).*'),
        re.compile(r'^\s+"(async\s+)?(def|class)\s+(?P<name>\w+)\W'),
        re.compile(r'^(\s+"[^#\s\\]|\s+\])')
    ),
    (
        # C source code (actually, any { }-delimited language)
        re.compile(r'^(c |c\+\+|c#|java|perl|php).*'),
        re.compile(r'^[^\s].*\s+(?P<name>\w+)\s*[({].*'),
        re.compile(r'^[}]')
    )
]

def rxdelim(content: str) -> Tuple[Optional[Pattern], Optional[Pattern]]:
    """
    Return suitable begin and end delimiters for the content `content`.
    If no matching delimiters are found, return `None, None`.
    """
    tp = magic.from_buffer(content).lower()
    for rxtp, rxbegin, rxend in DELIMITERS:
        if rxtp.match(tp):
            return rxbegin, rxend

    return None, None

Mapping = List[Optional[str]]

def elem_mapping(content: str, log: bool = False) -> Mapping:
    """Return a list of the elements in `content`, indexed by line number."""
    rxbegin, rxend = rxdelim(content)
    if rxbegin is None:
        return []
    if rxend is None:
        return []

    mapping: List[Optional[str]] = [None]
    current_elem = None
    lineno = 0

    for line in content.split('\n'):
        lineno += 1

        match = rxbegin.match(line)
        if match:
            current_elem = match.group('name')
        elif rxend.match(line):
            current_elem = None

        mapping.append(current_elem)

        if log:
            print(f"{lineno:3} {str(current_elem):15} {line}")

    return mapping

if __name__ == '__main__':
    some_c_source = """
#include <stdio.h>

int foo(int x) {
    return x;
}

struct bar {
    int x, y;
}

int main(int argc, char *argv[]) {
    return foo(argc);
}

"""
    some_c_mapping = elem_mapping(some_c_source, log=True)

if __name__ == '__main__':
    some_c_mapping[1], some_c_mapping[8]

if __name__ == '__main__':
    some_python_source = """
def foo(x):
    return x

class bar(blue):
    x = 25
    def f(x):
        return 26

def main(argc):
    return foo(argc)

"""
    some_python_mapping = elem_mapping(some_python_source, log=True)

### Determining Changed Elements

if __name__ == '__main__':
    print('\n### Determining Changed Elements')



def changed_elems_by_mapping(mapping: Mapping, start: int, length: int = 0) -> Set[str]:
    """
    Within `mapping`, return the set of elements affected by a change
    starting in line `start` and extending over `length` additional lines.
    """
    elems = set()
    for line in range(start, start + length + 1):
        if line < len(mapping) and mapping[line]:
            elem = mapping[line]
            assert elem is not None
            elems.add(elem)

    return elems

if __name__ == '__main__':
    changed_elems_by_mapping(some_python_mapping, start=2, length=4)

def elem_size(elem: str, source: str) -> int:
    """Within `source`, return the size of `elem`"""
    source_lines = [''] + source.split('\n')
    size = 0
    mapping = elem_mapping(source)

    for line_no in range(len(mapping)):
        if mapping[line_no] == elem or mapping[line_no] is elem:
            size += len(source_lines[line_no] + '\n')

    return size

if __name__ == '__main__':
    elem_size('foo', some_python_source)

if __name__ == '__main__':
    assert sum(elem_size(name, some_python_source) 
               for name in ['foo', 'bar', 'main']) == len(some_python_source)

from .ChangeDebugger import diff  # minor dependency

from diff_match_patch import diff_match_patch

def changed_elems(old_source: str, new_source: str) -> Set[str]:
    """Determine the elements affected by the change from `old_source` to `new_source`"""
    patches = diff(old_source, new_source)

    old_mapping = elem_mapping(old_source)
    new_mapping = elem_mapping(new_source)

    elems = set()

    for patch in patches:
        old_start_line = patch.start1 + 1
        new_start_line = patch.start2 + 1

        for (op, data) in patch.diffs:
            length = data.count('\n')

            if op == diff_match_patch.DIFF_INSERT:
                elems |= changed_elems_by_mapping(old_mapping, old_start_line)
                elems |= changed_elems_by_mapping(new_mapping, new_start_line, length)
            elif op == diff_match_patch.DIFF_DELETE:
                elems |= changed_elems_by_mapping(old_mapping, old_start_line, length)
                elems |= changed_elems_by_mapping(new_mapping, new_start_line)

            old_start_line += length
            new_start_line += length

    return elems

if __name__ == '__main__':
    some_new_python_source = """
def foo(y):
    return y

class qux(blue):
    x = 25
    def f(x):
        return 26

def main(argc):
    return foo(argc)

"""

if __name__ == '__main__':
    changed_elems(some_python_source, some_new_python_source)

### Putting it all Together

if __name__ == '__main__':
    print('\n### Putting it all Together')



class FineChangeCounter(ChangeCounter):
    """Count the changes for files in the repository and their elements"""

    def update_elems(self, node: Node, m: Commit) -> None:
        old_source = m.source_code_before if m.source_code_before else ""
        new_source = m.source_code if m.source_code else ""

        for elem in changed_elems(old_source, new_source):
            elem_node = node + (elem,)

            self.update_size(elem_node, elem_size(elem, new_source))
            self.update_changes(elem_node, m.msg)

if __name__ == '__main__':
    with Timer() as t:
        fine_change_counter = debuggingbook_change_counter(FineChangeCounter)

    t.elapsed_time()

if __name__ == '__main__':
    fine_change_counter.map()

if __name__ == '__main__':
    elem_nodes = [node for node in fine_change_counter.changes.keys()
                  if len(node) == 3 and node[1].endswith('.ipynb')]
    elem_nodes.sort(key=lambda node: fine_change_counter.changes[node], reverse=True)
    [(node, fine_change_counter.changes[node]) for node in elem_nodes[:1]]

from .bookutils import quiz

if __name__ == '__main__':
    quiz("Which is the _second_ most changed element?",
        [
            f"`{elem_nodes[3][2]}` in `{elem_nodes[3][1].split('.ipynb')[0]}`",
            f"`{elem_nodes[1][2]}` in `{elem_nodes[1][1].split('.ipynb')[0]}`",
            f"`{elem_nodes[2][2]}` in `{elem_nodes[2][1].split('.ipynb')[0]}`",
            f"`{elem_nodes[0][2]}` in `{elem_nodes[0][1].split('.ipynb')[0]}`",
        ], '1975308642 // 987654321')

if __name__ == '__main__':
    [(node, fine_change_counter.changes[node]) for node in elem_nodes[:5]]

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    change_counter.changes[('README.md',)]

if __name__ == '__main__':
    change_counter.messages[('README.md',)]

if __name__ == '__main__':
    change_counter.sizes[('README.md',)]

if __name__ == '__main__':
    fine_change_counter.map()

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy([FineChangeCounter, FixCounter],
                            public_methods=[
                                ChangeCounter.__init__,
                                ChangeCounter.map
                            ],
                            project='debuggingbook')

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Fine-Grained Fixes

if __name__ == '__main__':
    print('\n### Exercise 1: Fine-Grained Fixes')



class FineFixCounter(FixCounter, FineChangeCounter):
    pass

if __name__ == '__main__':
    fine_fix_counter = debuggingbook_change_counter(FineFixCounter)

if __name__ == '__main__':
    fine_fix_counter.map()
