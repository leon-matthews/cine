#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from collections import OrderedDict

import pygraphviz


class DatabaseDiagram(object):
    def __init__(self, path=None):
        self.graph = None
        if path is not None:
            self.read(path)

    def create_graph(self):
        """
        Create graph programatically.
        """
        self.graph = pygraphviz.AGraph(directed=True, overlap=False, rankdir='LR', splines='spline', labeljust='l', labelloc='t')
        self.graph.node_attr['label'] = '\\N'
        self.graph.node_attr['shape'] = 'plaintext'

        self.graph.edge_attr['color'] = 'gray50'
        self.graph.edge_attr['minlen'] = 2
        self.graph.edge_attr['style'] = 'solid'

    def add_table(self, name, fields):
        """
        Add database table to diagram.
        """
        self._add_node(name, fields)

    def add_edges(self):
        self.graph.add_edge('names', 'professions')
        self.graph.add_edge('names', 'titles')
        self.graph.add_edge('titles', 'genres')
        self.graph.add_edge('akas', 'titles')
        self.graph.add_edge('crew', 'titles')
        self.graph.add_edge('crew', 'names')
        self.graph.add_edge('title_episodes', 'titles')
        self.graph.add_edge('title_principals', 'titles')
        self.graph.add_edge('title_principals', 'names')
        self.graph.add_edge('title_principals', 'characters')
        self.graph.add_edge('ratings', 'titles', headlabel='<<FONT>1</FONT>>',
                label='<<FONT> away </FONT>>',
                taillabel='<<FONT>0..N</FONT>>')

    def render(self, path):
        """
        Render graph to image file.
        """
        self.graph.layout()
        self.graph.draw(path)

    def read(self, path):
        """
        Load graph object from dotfile.
        """
        self.graph = pygraphviz.AGraph(path)

    def save(self, path):
        """
        Save graph to dotfile.
        """
        self.graph.write(path)

    def _add_node(self, title, fields):
        parts = [
            '<<font face="helvetica">',
            '<table border="0" cellborder="1" cellpadding="4" cellspacing="0">',
            '<tr><td><b><font point-size="16">{}</font></b></td></tr>'.format(title),
        ]
        row = '<tr><td align="left"><font>{} &rarr; <i>{}</i></font></td></tr>'
        for name, type_ in fields.items():
            parts.append(row.format(name, type_))
        parts.append('</table></font>>')
        self.graph.add_node(title, label=''.join(parts))

    def __str__(self):
        return str(self.graph)


if __name__ == '__main__':
    # Create programatically
    a = DatabaseDiagram()
    a.create_graph()

    a.add_table('names', OrderedDict([
        ('nconst', 'int'),
        ('primary_name', 'str'),
        ('birth_year', 'int'),
        ('death_year', 'int'),
        ('primary_profession', 'professions'),
        ('known_for_titles', 'titles'),
        ]),
    )

    a.add_table('titles', OrderedDict([
        ('tconst', 'int'),
        ('title_type', 'XXXX'),
        ('primary_title', 'str'),
        ('original_title', 'str'),
        ('is_adult', 'bool'),
        ('start_year', 'int'),
        ('end_year', 'int'),
        ('runtime_minutes', 'int'),
        ('genres', 'genres'),
        ]),
    )

    a.add_table('akas', OrderedDict([
        ('id', 'int'),
        ('title_id', 'titles'),
        ('ordering', 'int'),
        ('title', 'str'),
        ('region', 'str'),
        ('language', 'str'),
        ('types', 'XXXX'),
        ('attributes', 'XXXX'),
        ('is_original_title', 'to_bool'),
        ]),
    )

    a.add_table('crew', OrderedDict([
        ('tconst', 'titles'),
        ('directors', 'names'),
        ('writers', 'names'),
        ]),
    )

    a.add_table('title_episodes', OrderedDict([
        ('tconst', 'titles'),
        ('parent_tconst', 'titles'),
        ('season_number', 'int'),
        ('episode_number', 'int'),
        ]),
    )

    a.add_table('title_principals', OrderedDict([
        ('tconst', 'titles'),
        ('ordering', 'int'),
        ('nconst', 'names'),
        ('category', 'XXXX'),
        ('job', 'XXXX'),
        ('characters', 'characters'),
        ]),
    )

    a.add_table('ratings', OrderedDict([
        ('tconst', 'titles'),
        ('average_rating', 'float'),
        ('num_votes', 'int'),
        ]),
    )

    a.add_table('professions', OrderedDict([
        ('id', 'int'),
        ('name', 'str'),
        ]),
    )

    a.add_table('genres', OrderedDict([
        ('id', 'int'),
        ('name', 'str'),
        ]),
    )

    a.add_table('characters', OrderedDict([
        ('id', 'int'),
        ('name', 'str'),
        ]),
    )

    a.add_edges()
    print(a)
    a.save('simple.dot')

    # Read from dotfile, create image file
    b = DatabaseDiagram('simple.dot')
    b.render('simple.png')
