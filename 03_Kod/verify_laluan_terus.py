"""
Analisis laluan terus (bahagian 'Sistem Peralihan' dan 'Analisis Laluan Terus' dalam manuskrip): adakah penguraian
daun dalam manuskrip sepadan dengan laluan "terus" (straight-ahead walk)?

Latar: pada peralihan terus, dua jalur bersilang secara melintang; pada
peralihan membelok, jalur dilipat (seperti di penjuru kelongsong). Anyaman
tanpa lipatan ialah penguraian laluan terus, yang ditentukan oleh sistem
putaran (rotation system) benaman graf pada sfera.

Setiap bucu darjah 4 boleh dipecahkan kepada 2 pasangan dalam 3 cara. Hanya
SATU daripadanya ialah "terus". Skrip ini:
  1. Mengira sistem putaran daripada koordinat 3D (susunan sudut jiran pada
     satah tangen setiap bucu).
  2. Menjana penguraian laluan-terus, dan mengira bilangan gelungnya.
  3. Membandingkannya dengan penguraian yang digunakan dalam kertas kerja.
"""
import numpy as np
from itertools import combinations

def bina_graf(bucu):
    d = {(i, j): round(float(np.linalg.norm(bucu[i] - bucu[j])), 6)
         for i, j in combinations(range(len(bucu)), 2)}
    dmin = min(d.values())
    sisi = sorted(e for e, v in d.items() if abs(v - dmin) < 1e-6)
    jiran = {i: [] for i in range(len(bucu))}
    for a, b in sisi:
        jiran[a].append(b); jiran[b].append(a)
    return set(sisi), jiran


def sistem_putaran(bucu, jiran):
    """Susunan jiran mengikut sudut pada satah tangen -- iaitu susunan
    sebenar sisi mengelilingi bucu apabila graf dilihat pada permukaan sfera."""
    putaran = {}
    for v, js in jiran.items():
        n = bucu[v] / np.linalg.norm(bucu[v])          # normal keluar pada sfera
        u = np.array([1.0, 0, 0])
        if abs(np.dot(u, n)) > 0.9:
            u = np.array([0, 1.0, 0])
        e1 = np.cross(n, u); e1 /= np.linalg.norm(e1)
        e2 = np.cross(n, e1)
        sudut = {}
        for w in js:
            t = bucu[w] - bucu[v]
            t = t - np.dot(t, n) * n                   # unjur ke satah tangen
            sudut[w] = np.arctan2(np.dot(t, e2), np.dot(t, e1))
        putaran[v] = sorted(js, key=lambda w: sudut[w])
    return putaran


def laluan_terus(sisi, putaran):
    """Jejak semua gelung tertutup di mana setiap bucu dilalui secara 'terus'
    (jiran bertentangan, iaitu 2 kedudukan dalam susunan putaran)."""
    arah = set()
    for a, b in sisi:
        arah.add((a, b)); arah.add((b, a))
    belum, gelung = set(arah), []
    while belum:
        mula = next(iter(belum))
        laluan, semasa = [], mula
        while semasa in belum:
            belum.discard(semasa)
            laluan.append(semasa)
            u, v = semasa
            r = putaran[v]
            seterusnya = r[(r.index(u) + 2) % 4]       # 'terus' = lawan dalam putaran
            semasa = (v, seterusnya)
        gelung.append(laluan)
    # tapis gelung salinan (setiap gelung dijejak dua kali, satu setiap arah)
    unik, dilihat = [], set()
    for g in gelung:
        kunci = frozenset(frozenset(e) for e in g)
        if kunci not in dilihat:
            dilihat.add(kunci); unik.append(g)
    return unik


def lapor(nama, bucu, daun_kertas):
    print(f"\n{'='*64}\n{nama}\n{'='*64}")
    sisi, jiran = bina_graf(bucu)
    putaran = sistem_putaran(bucu, jiran)
    gelung = laluan_terus(sisi, putaran)
    print(f"V={len(bucu)}, E={len(sisi)}")
    print(f"\nPenguraian LALUAN-TERUS (yang dikenakan oleh fizik anyaman):")
    print(f"  bilangan gelung = {len(gelung)}")
    for i, g in enumerate(sorted(gelung, key=len)):
        bucu_g = [e[0] for e in g]
        print(f"    Gelung {i+1}: {len(g)} sisi -> bucu {bucu_g}")
    semua = [frozenset(e) for g in gelung for e in g]
    print(f"  jumlah sisi diliputi = {len(set(semua))} / {len(sisi)}"
          f"  (sisi-asing: {len(semua) == len(set(semua))})")

    print(f"\nPenguraian yang digunakan dalam KERTAS KERJA:")
    print(f"  bilangan daun = {len(daun_kertas)}, "
          f"panjang = {[len(d)-1 for d in daun_kertas]}")
    set_kertas = {frozenset(frozenset((d[i], d[i+1])) for i in range(len(d)-1))
                  for d in daun_kertas}
    set_terus = {frozenset(frozenset(e) for e in g) for g in gelung}
    sama = set_kertas == set_terus
    print(f"\n>>> Adakah kedua-duanya SAMA? {sama}")
    if not sama:
        print("    -> Penguraian ini BUKAN laluan-terus. Ia memerlukan")
        print("       jalur daun MEMBELOK pada sebahagian silangan.")
    return len(gelung), sama


okta = np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]], dtype=float)
daun_okta = [[4,0,3,5,2,1,4], [4,2,0,5,1,3,4]]

kubo = np.array([[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0],
                 [1,0,1],[-1,0,1],[0,1,1],[0,-1,1],
                 [1,0,-1],[-1,0,-1],[0,1,-1],[0,-1,-1]], dtype=float)
daun_kubo = [[0,4,3,8,10,9,1,6,0], [2,5,6,4,7,3,11,9,2], [0,8,11,2,7,5,1,10,0]]

n1, s1 = lapor("OKTAHEDRON (model 2-daun kertas kerja)", okta, daun_okta)
n2, s2 = lapor("KUBOKTAHEDRON (model 3-daun kertas kerja)", kubo, daun_kubo)

print(f"\n{'='*64}\nRUMUSAN\n{'='*64}")
print(f"Oktahedron    : laluan-terus memberi {n1} gelung; kertas kerja guna 2 daun; padan={s1}")
print(f"Kuboktahedron : laluan-terus memberi {n2} gelung; kertas kerja guna 3 daun; padan={s2}")
