"""
Meneroka KELUARGA PENUH anyaman n-daun seimbang pada kuboktahedron.

Tujuan: menyemak (dan membetulkan) dakwaan dalam kertas kerja tentang
syarat kebolehbahagian. Skrip ini:
  1. Menerbitkan set nilai n yang MUNGKIN secara aritmetik, menggunakan
     dua syarat perlu:  (a) n | E,  (b) 3 <= E/n <= |V|
     (kerana satu kitaran ringkas mesti ada >=3 sisi, dan tidak boleh
      melebihi |V| sisi kerana ia tidak boleh mengulang bucu).
  2. Mencari secara TUNTAS (exhaustive backtracking) sama ada penguraian
     sebenar wujud bagi setiap n yang lulus syarat aritmetik.
  3. Mengesahkan setiap penguraian yang dijumpai terhadap keempat-empat
     syarat Definisi 2 dalam kertas kerja.
"""
import numpy as np
import networkx as nx
from itertools import combinations

# ---------- 1. Bina graf kuboktahedron daripada geometri ----------
bucu = np.array([
    [ 1, 1, 0], [-1, 1, 0], [-1,-1, 0], [ 1,-1, 0],
    [ 1, 0, 1], [-1, 0, 1], [ 0, 1, 1], [ 0,-1, 1],
    [ 1, 0,-1], [-1, 0,-1], [ 0, 1,-1], [ 0,-1,-1],
], dtype=float)
n_bucu = len(bucu)

d = {(i, j): round(float(np.linalg.norm(bucu[i] - bucu[j])), 6)
     for i, j in combinations(range(n_bucu), 2)}
dmin = min(d.values())
E_list = sorted(e for e, v in d.items() if abs(v - dmin) < 1e-6)
G = nx.Graph(); G.add_nodes_from(range(n_bucu)); G.add_edges_from(E_list)
E_set = set(E_list)
V, E = G.number_of_nodes(), G.number_of_edges()
assert (V, E) == (12, 24)
assert all(dg == 4 for _, dg in G.degree())
print(f"Graf kuboktahedron: V={V}, E={E}, semua bucu darjah 4.\n")


# ---------- 2. Syarat perlu aritmetik ----------
print("=== SYARAT PERLU (aritmetik sahaja) ===")
print("Syarat (a) n | E ; Syarat (b) 3 <= E/n <= V  [panjang kitaran ringkas]")
pembahagi = [k for k in range(1, E + 1) if E % k == 0]
lulus_a = pembahagi
lulus_ab = [k for k in pembahagi if 3 <= E // k <= V]
print(f"  Pembahagi E=24            : {lulus_a}")
print(f"  Lulus (a) DAN (b)         : {lulus_ab}   (panjang kitaran = {[E//k for k in lulus_ab]})")
ditolak_b = [k for k in lulus_a if k not in lulus_ab]
print(f"  Lulus (a) tetapi GAGAL (b): {ditolak_b}"
      f"  -> contoh: n=12 perlu kitaran 2-sisi (mustahil), n=1 perlu kitaran 24-sisi > 12 bucu.\n")


# ---------- 3. Enumerasi semua kitaran ringkas berpanjangan tepat L ----------
def kitaran_panjang(G, L):
    """Semua kitaran ringkas panjang tepat L, sebagai frozenset sisi (tanpa pendua)."""
    hasil = set()
    nodes = sorted(G.nodes())
    def dfs(mula, semasa, laluan, dilawat):
        if len(laluan) == L:
            if G.has_edge(semasa, mula):
                sisi = frozenset(
                    tuple(sorted((laluan[i], laluan[(i + 1) % L]))) for i in range(L))
                if len(sisi) == L:
                    hasil.add(sisi)
            return
        for w in G.neighbors(semasa):
            if w < mula or w in dilawat:
                continue
            dfs(mula, w, laluan + [w], dilawat | {w})
    for s in nodes:
        dfs(s, s, [s], {s})
    return sorted(hasil, key=lambda f: sorted(f))


# ---------- 4. Carian tuntas penguraian sisi-asing ----------
def cari_penguraian(kitaran, E_set, n):
    """Backtracking exact-cover: pilih n kitaran sisi-asing yang meliputi semua sisi."""
    sisi_tersusun = sorted(E_set)
    ikut_sisi = {s: [c for c in kitaran if s in c] for s in sisi_tersusun}

    def cari(belum, dipilih):
        if not belum:
            return list(dipilih) if len(dipilih) == n else None
        if len(dipilih) == n:
            return None
        sasar = min(belum)                      # sisi pertama yang belum diliputi
        for c in ikut_sisi[sasar]:
            if c <= belum:                      # semua sisi kitaran masih belum diliputi
                r = cari(belum - c, dipilih + [c])
                if r:
                    return r
        return None

    return cari(frozenset(sisi_tersusun), [])


# ---------- 5. Pengesahan terhadap Definisi 2 ----------
def sahkan_definisi2(daun, G, E_set):
    """Semak keempat-empat syarat Definisi 2. Kembalikan (bool, mesej)."""
    n = len(daun)
    # (i) setiap E_i kitaran ringkas: semua bucu darjah 2 dalam subgraf & terhubung
    for i, c in enumerate(daun):
        H = nx.Graph(); H.add_edges_from(c)
        if not (all(dg == 2 for _, dg in H.degree()) and nx.is_connected(H)):
            return False, f"Daun {i+1} bukan kitaran ringkas tunggal"
    # (iii) sisi-asing
    for a, b in combinations(range(n), 2):
        if daun[a] & daun[b]:
            return False, f"Daun {a+1} & {b+1} berkongsi sisi"
    # (ii) liputan penuh
    gabung = set().union(*daun)
    if gabung != E_set:
        return False, f"Liputan tidak lengkap ({len(gabung)}/{len(E_set)})"
    # (iv) setiap bucu disentuh tepat 2 daun
    for v in G.nodes():
        kira = sum(1 for c in daun if any(v in s for s in c))
        if kira != 2:
            return False, f"Bucu {v} disentuh {kira} daun (sepatutnya 2)"
    return True, "LULUS semua 4 syarat Definisi 2"


# ---------- 6. Jalankan bagi setiap n yang lulus syarat aritmetik ----------
print("=== CARIAN PENGURAIAN SEBENAR (exhaustive) ===")
ringkasan = {}
for n in lulus_ab:
    L = E // n
    kit = kitaran_panjang(G, L)
    hasil = cari_penguraian(kit, E_set, n)
    if hasil is None:
        ringkasan[n] = None
        print(f"n={n:2d} (kitaran {L}-sisi): {len(kit):4d} calon kitaran -> TIADA penguraian sah")
        continue
    ok, msg = sahkan_definisi2(hasil, G, E_set)
    ringkasan[n] = hasil if ok else None
    status = "WUJUD" if ok else "DITOLAK"
    print(f"n={n:2d} (kitaran {L}-sisi): {len(kit):4d} calon kitaran -> {status}; {msg}")
    for i, c in enumerate(sorted(hasil, key=lambda f: sorted(f))):
        print(f"        Daun {i+1}: {sorted(tuple(s) for s in c)}")
    assert ok

# ---------- 7. Semakan silang khusus: muka segi tiga & segi empat ----------
print("\n=== SEMAKAN SILANG: muka polihedron sebagai 'daun' ===")
# 8 muka segi tiga kuboktahedron = semua 3-kitaran
segitiga = kitaran_panjang(G, 3)
print(f"Bilangan 3-kitaran (muka segi tiga) = {len(segitiga)}")
ok_t, msg_t = sahkan_definisi2(segitiga, G, E_set)
print(f"  8 muka segi tiga sebagai anyaman 8-daun: {msg_t}")
assert ok_t and len(segitiga) == 8

# 6 muka segi empat = 4-kitaran yang bukan gabungan lain; ambil 4-kitaran yang
# merupakan muka sebenar (semua bucunya sepesawat & membentuk muka hull)
empat = kitaran_panjang(G, 4)
hasil6 = cari_penguraian(empat, E_set, 6)
ok_s, msg_s = sahkan_definisi2(hasil6, G, E_set)
print(f"  Bilangan 4-kitaran = {len(empat)}; penguraian 6-daun: {msg_s}")
assert ok_s

print("\n=== KESIMPULAN ===")
wujud = sorted(k for k, v in ringkasan.items() if v is not None)
tiada = sorted(k for k, v in ringkasan.items() if v is None)
print(f"n lulus syarat aritmetik      : {lulus_ab}")
print(f"n yang penguraiannya WUJUD    : {wujud}")
print(f"n yang penguraiannya TIADA    : {tiada if tiada else '(tiada)'}")
print(f"n ditolak oleh syarat panjang : {ditolak_b}")
