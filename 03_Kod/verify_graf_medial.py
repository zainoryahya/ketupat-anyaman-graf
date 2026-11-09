# -*- coding: utf-8 -*-
"""
Pengesahan: graf medial bagi bentuk kelongsong (bahagian 'Skop dan Had Rangka Kerja' dalam manuskrip)

Dakwaan (assert; senyap = lulus):
  - M(tetrahedron) isomorfik dengan oktahedron
  - M(kubus) isomorfik dengan kuboktahedron
  - M(prisma segi tiga) ialah graf 4-sekata dengan 9 bucu
  - M(piramid m-gon) isomorfik dengan antiprisma m-gon, bagi 3 <= m <= 9
Graf medial M(P): satu bucu bagi setiap sisi P; dua bucu bersambung jika sisi
sepadan berturutan pada sempadan sesuatu muka P. Ia sentiasa 4-sekata.
Keperluan: numpy, networkx.
"""
import itertools
import numpy as np
import networkx as nx


def medial(muka):
    G = nx.Graph()
    for f in muka:
        n = len(f)
        for k in range(n):
            G.add_edge(frozenset((f[k], f[(k+1) % n])), frozenset((f[(k+1) % n], f[(k+2) % n])))
    return G


def antiprisma(m):
    G = nx.Graph()
    for k in range(m):
        G.add_edge(("a", k), ("a", (k+1) % m)); G.add_edge(("b", k), ("b", (k+1) % m))
        G.add_edge(("a", k), ("b", k)); G.add_edge(("a", (k+1) % m), ("b", k))
    return G


def kuboktahedron():
    pts = sorted({tuple(s*x for s, x in zip(sg, p))
                  for p in set(itertools.permutations((1, 1, 0)))
                  for sg in itertools.product((1, -1), repeat=3)})
    P = np.array(pts, float)
    return nx.Graph([(i, j) for i in range(12) for j in range(i+1, 12)
                     if abs(np.linalg.norm(P[i]-P[j]) - np.sqrt(2)) < 1e-9])


if __name__ == "__main__":
    tetra = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    kubus = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    prisma = [(0, 1, 2), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]

    assert nx.is_isomorphic(medial(tetra), nx.octahedral_graph())
    assert nx.is_isomorphic(medial(kubus), kuboktahedron())
    Mp = medial(prisma)
    assert Mp.number_of_nodes() == 9 and set(dict(Mp.degree()).values()) == {4}
    for m in range(3, 10):
        piramid = [tuple(range(m))] + [(k, (k+1) % m, "puncak") for k in range(m)]
        assert nx.is_isomorphic(medial(piramid), antiprisma(m))
    print("Semua dakwaan lulus.")
