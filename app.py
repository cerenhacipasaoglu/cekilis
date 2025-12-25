import streamlit as st
import random
from typing import Dict, List, Set, Tuple

# -------------------------
# İSİMLER
# -------------------------
NAMES: List[str] = [
    "ceren hacipasaoglu",
    "miray aktarma",
    "defne mesci",
    "hira erokyar",
    "zeynep akkiprik",
    "gaye deniz",
    "eylul gulkanat",
    "ferzin kilic",
    "zeynep arpacioglu",
]

# -------------------------
# YASAKLI ÇİFTLER
# -------------------------
BAD_PAIRS: Set[Tuple[str, str]] = {
    ("eylul gulkanat", "ferzin kilic"),
    ("gaye deniz", "miray aktarma"),
    ("gaye deniz", "ferzin kilic"),
    ("defne mesci", "gaye deniz"),
}

# -------------------------
# ZORUNLU
# -------------------------
FORCED: Dict[str, str] = {
    "defne mesci": "zeynep arpacioglu",
    "zeynep arpacioglu": "defne mesci",
}

def normalize(s: str) -> str:
    return s.strip().lower()

def build_forbidden(pairs):
    out = set()
    for a, b in pairs:
        a, b = normalize(a), normalize(b)
        out.add((a, b))
        out.add((b, a))
    return out

FORBIDDEN = build_forbidden(BAD_PAIRS)

def allowed(giver, receiver):
    if giver == receiver:
        return False
    if (giver, receiver) in FORBIDDEN:
        return False
    return True

@st.cache_data
def make_draw():
    random.seed(20251225)
    names = [normalize(n) for n in NAMES]

    assignment = dict(FORCED)
    used = set(assignment.values())

    remaining = [n for n in names if n not in assignment]

    candidates = {
        g: [r for r in names if allowed(g, r) and r not in used]
        for g in remaining
    }

    givers_sorted = sorted(remaining, key=lambda g: len(candidates[g]))

    def backtrack(i):
        if i == len(givers_sorted):
            return True
        g = givers_sorted[i]
        opts = candidates[g][:]
        random.shuffle(opts)
        for r in opts:
            if r in used:
                continue
            assignment[g] = r
            used.add(r)
            if backtrack(i + 1):
                return True
            used.remove(r)
            del assignment[g]
        return False

    backtrack(0)
    return assignment

# -------------------------
# STREAMLIT UI
# -------------------------
st.set_page_config(page_title="Yılbaşı Çekilişi", page_icon="🎁")
st.title("🎁 Yılbaşı Çekilişi")

draw = make_draw()

name = normalize(st.text_input("İsmini gir"))

if name:
    if name not in draw:
        st.error("Bu isim listede yok.")
    else:
        st.success("🎯 Çektiğin kişi:")
        st.markdown(f"## **{draw[name]}**")
