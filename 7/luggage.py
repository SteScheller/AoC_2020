import re
import functools
import operator
from typing import Dict, List, Tuple

import igraph as ig

def parse_input(file_path: str) -> Dict[str, str]:
    with open(file_path) as f:
        lines = f.readlines()
    regulations = dict()
    for l in lines:
        m = re.match(r'([a-z]+ [a-z]+) bags contain (no other bags\.)?', l)
        outer_bag = m.group(1)
        inner_bags = list()
        if m.group(2) is None:
            inner_bags = [ (bag, int(num)) for (num, bag, _) in \
                    re.findall(r'([0-9]+) ([a-z]+ [a-z]+) (bag|bags)', l) ]
        regulations[outer_bag] = inner_bags
    return regulations

def build_regulations_graph(regulations: Dict[str, List[Tuple[str, int]]]) -> ig.Graph:
    g = ig.Graph(directed=True)
    g.add_vertices([k for k in regulations.keys()])
    for parent, children in regulations.items():
        for child, cost in children:
            g.add_edge(parent, child, cost=cost)
    return g

if __name__ == '__main__':
    g = build_regulations_graph(parse_input('input.txt'))
    v = g.vs.select(name_eq='shiny gold')[0]
    n_in = g.neighborhood(v, order=len(g.vs), mode='in', mindist=1)
    print('{} bags can eventually contain a {} bag.'.format(len(n_in), v['name']) )
    num_bags = 0
    for t in g.neighborhood(v, order=len(g.vs), mode='out', mindist=1):
        paths = g.get_all_simple_paths(v, t)
        for p in paths:
            num_bags = num_bags + functools.reduce(
                    operator.mul,
                    [g.es[g.get_eid(a, b)]['cost'] for a, b in zip(p[:-1], p[1:])] )
    print('One {} bag must contain {} other bags.'.format(v['name'], num_bags) )
