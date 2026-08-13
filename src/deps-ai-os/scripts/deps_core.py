#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEPS AI Operating System - Coeur du moteur.

Chargement des bases CSV, recherche BM25 insensible aux accents, resolution
des chaines de modules et controles de coherence du referentiel.

Aucune dependance externe: bibliotheque standard uniquement.
"""

import csv
import re
import unicodedata
from pathlib import Path
from math import log
from collections import defaultdict

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
REFERENCES_DIR = Path(__file__).parent.parent / "references"
MAX_RESULTS = 5

DOMAINES = {
    "01-FINANCEMENT": "01 - FINANCEMENT",
    "02-FLI-FLS": "02 - FLI / FLS",
    "03-EVALUATION": "03 - EVALUATION",
    "04-DEVELOPPEMENT-ECONOMIQUE": "04 - DEVELOPPEMENT ECONOMIQUE",
    "05-PRODUCTION": "05 - PRODUCTION",
    "06-QA": "06 - QA",
}

REFERENCE_PAR_DOMAINE = {
    "01-FINANCEMENT": "01-financement.md",
    "02-FLI-FLS": "02-fli-fls.md",
    "03-EVALUATION": "03-evaluation.md",
    "04-DEVELOPPEMENT-ECONOMIQUE": "04-developpement-economique.md",
    "05-PRODUCTION": "05-production.md",
    "06-QA": "06-qa.md",
}

FILES = {
    "modules": "modules.csv",
    "pipelines": "pipelines.csv",
    "formules": "formules.csv",
    "parametres": "parametres-politique.csv",
    "controles": "controles-qa.csv",
    "nomenclature": "nomenclature.csv",
}

# Colonnes indexees pour le routage
ROUTE_COLS_MODULES = ["ID", "Module", "Objectif", "Déclencheurs", "Domaine"]
ROUTE_COLS_PIPELINES = ["ID", "Pipeline", "Objectif", "Déclencheurs"]

STATUT_A_VALIDER = "A_VALIDER"
LIST_SEP = ";"
METHODE_SEP = "|"


# ============ UTILITAIRES ============
def strip_accents(text):
    """Retire les diacritiques pour comparer 'admissibilite' et 'admissibilité'."""
    decomposed = unicodedata.normalize("NFD", str(text))
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def split_list(value):
    """Decoupe un champ liste separe par des points-virgules."""
    if not value:
        return []
    return [item.strip() for item in str(value).split(LIST_SEP) if item.strip()]


def split_methode(value):
    """
    Decoupe un champ methode. Les etapes numerotees sont separees par une barre
    verticale, ce qui permet aux etapes elles-memes de contenir des virgules et
    des points-virgules.
    """
    if not value:
        return []
    return [item.strip() for item in str(value).split(METHODE_SEP) if item.strip()]


def load_csv(name):
    """Charge une base CSV du referentiel et retourne une liste de dictionnaires."""
    if name not in FILES:
        raise KeyError("Base inconnue: %s" % name)
    path = DATA_DIR / FILES[name]
    if not path.exists():
        raise FileNotFoundError("Base introuvable: %s" % path)
    with open(path, "r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# ============ BM25 ============
class BM25:
    """Classement BM25, insensible aux accents et a la casse."""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        """Minuscules, sans accents, sans ponctuation, mots de plus de 2 lettres."""
        normalized = strip_accents(str(text).lower())
        normalized = re.sub(r"[^\w\s]", " ", normalized)
        return [word for word in normalized.split() if len(word) > 2]

    def fit(self, documents):
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N

        for doc in self.corpus:
            for word in set(doc):
                self.doc_freqs[word] += 1

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        query_tokens = self.tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            total = 0.0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1
            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    total += self.idf[token] * numerator / denominator
            scores.append((idx, total))
        return sorted(scores, key=lambda pair: pair[1], reverse=True)


def _index(rows, columns):
    """Construit un index BM25 sur la concatenation des colonnes indiquees."""
    documents = [" ".join(str(row.get(col, "")) for col in columns) for row in rows]
    engine = BM25()
    engine.fit(documents)
    return engine


def _exact_boost(row, query, keys):
    """Bonus quand la requete nomme explicitement un identifiant ou un nom."""
    query_norm = strip_accents(query.lower())
    query_tokens = set(re.sub(r"[^\w\s]", " ", query_norm).split())
    boost = 0.0
    for key in keys:
        value = strip_accents(str(row.get(key, "")).lower()).strip()
        if not value:
            continue
        if value in query_tokens:
            boost += 6.0
        elif len(value) > 3 and value in query_norm:
            boost += 4.0
    return boost


# ============ ACCES AU REFERENTIEL ============
def get_module(identifiant):
    """Retourne un module par son ID (F1) ou par son nom (analyse-financiere)."""
    cible = strip_accents(str(identifiant).lower()).strip()
    for row in load_csv("modules"):
        if strip_accents(row["ID"].lower()) == cible:
            return row
        if strip_accents(row["Module"].lower()) == cible:
            return row
    return None


def get_pipeline(identifiant):
    """Retourne un pipeline par son ID (PL1) ou par son nom (dossier-cic)."""
    cible = strip_accents(str(identifiant).lower()).strip()
    for row in load_csv("pipelines"):
        if strip_accents(row["ID"].lower()) == cible:
            return row
        if strip_accents(row["Pipeline"].lower()) == cible:
            return row
    return None


def modules_par_domaine(domaine=None):
    """Liste les modules, filtres sur un domaine si fourni."""
    rows = load_csv("modules")
    if not domaine:
        return rows
    cible = strip_accents(str(domaine).lower())
    return [r for r in rows if cible in strip_accents(r["Domaine"].lower())]


def chaine_modules(identifiant, avec_qa=True):
    """
    Reconstitue la chaine d'execution d'un module: dependances amont d'abord,
    puis le module, puis ses portes de controle qualite.

    L'ordre canonique est celui de modules.csv, ce qui garantit un resultat
    stable et un ordre de domaine croissant.
    """
    rows = load_csv("modules")
    par_id = {r["ID"]: r for r in rows}
    ordre = {r["ID"]: i for i, r in enumerate(rows)}

    cible = get_module(identifiant)
    if not cible:
        return None

    requis = set()
    vus = set()

    def descendre(module_id):
        if module_id in vus or module_id not in par_id:
            return
        vus.add(module_id)
        for amont in split_list(par_id[module_id]["Amont"]):
            if amont in par_id:
                requis.add(amont)
                descendre(amont)

    descendre(cible["ID"])
    sequence = sorted(requis, key=lambda mid: ordre[mid])
    sequence.append(cible["ID"])

    if avec_qa:
        gates = []
        for module_id in sequence:
            for gate in split_list(par_id[module_id]["Gate QA"]):
                if gate in par_id and gate not in gates and gate not in sequence:
                    gates.append(gate)
        sequence.extend(sorted(gates, key=lambda mid: ordre[mid]))

    return [par_id[mid] for mid in sequence]


def sequence_pipeline(identifiant):
    """Retourne les modules d'un pipeline dans l'ordre declare."""
    pipeline = get_pipeline(identifiant)
    if not pipeline:
        return None
    par_id = {r["ID"]: r for r in load_csv("modules")}
    return [par_id[mid] for mid in split_list(pipeline["Séquence"]) if mid in par_id]


def parametres(fonds=None, statut=None, module=None):
    """Filtre les parametres de politique par fonds, statut ou module utilisateur."""
    rows = load_csv("parametres")
    if fonds:
        cible = strip_accents(fonds.lower())
        rows = [r for r in rows if cible in strip_accents(r["Fonds"].lower())]
    if statut:
        cible = strip_accents(statut.lower())
        rows = [r for r in rows if strip_accents(r["Statut"].lower()) == cible]
    if module:
        cible = module.upper()
        rows = [r for r in rows if cible in split_list(r["Utilisé par"])]
    return rows


def parametres_non_valides():
    """Parametres de politique qui ne peuvent pas alimenter un chiffre presente."""
    return parametres(statut=STATUT_A_VALIDER)


def formules(module=None, recherche=None):
    """Filtre les formules par module mobilisateur ou par recherche libre."""
    rows = load_csv("formules")
    if module:
        cible = module.upper()
        rows = [r for r in rows if cible in split_list(r["Modules"])]
    if recherche:
        cible = strip_accents(recherche.lower())
        rows = [r for r in rows
                if cible in strip_accents((r["Clé"] + " " + r["Nom"] + " " + r["Catégorie"]).lower())]
    return rows


def controles(module=None, bloquants_seulement=False):
    """Filtre les controles qualite par module et par caractere bloquant."""
    rows = load_csv("controles")
    if module:
        cible = module.upper()
        rows = [r for r in rows if r["Module"].upper() == cible]
    if bloquants_seulement:
        rows = [r for r in rows if r["Bloquant"].strip().upper() == "OUI"]
    return rows


def nomenclature(code=None, module=None):
    """Retourne les conventions de nommage, filtrees par code ou par module."""
    rows = load_csv("nomenclature")
    if code:
        cible = strip_accents(code.lower())
        rows = [r for r in rows if strip_accents(r["Code"].lower()) == cible]
    if module:
        cible = module.upper()
        rows = [r for r in rows if r["Module"].upper() == cible]
    return rows


# ============ ROUTAGE ============
def router(demande, max_results=MAX_RESULTS):
    """
    Oriente une demande en langage naturel vers un pipeline ou un module.

    Retourne les pipelines et les modules classes, ainsi qu'une recommandation
    unique: un pipeline s'il domine clairement, sinon le module le mieux classe
    accompagne de sa chaine d'execution.
    """
    modules = load_csv("modules")
    pipelines = load_csv("pipelines")

    index_modules = _index(modules, ROUTE_COLS_MODULES)
    index_pipelines = _index(pipelines, ROUTE_COLS_PIPELINES)

    scores_modules = []
    for idx, score in index_modules.score(demande):
        total = score + _exact_boost(modules[idx], demande, ["ID", "Module"])
        if total > 0:
            scores_modules.append((modules[idx], round(total, 3)))
    scores_modules.sort(key=lambda pair: pair[1], reverse=True)

    scores_pipelines = []
    for idx, score in index_pipelines.score(demande):
        total = score + _exact_boost(pipelines[idx], demande, ["ID", "Pipeline"])
        if total > 0:
            scores_pipelines.append((pipelines[idx], round(total, 3)))
    scores_pipelines.sort(key=lambda pair: pair[1], reverse=True)

    meilleur_module = scores_modules[0] if scores_modules else None
    meilleur_pipeline = scores_pipelines[0] if scores_pipelines else None

    recommandation = None
    if meilleur_pipeline and (not meilleur_module or meilleur_pipeline[1] >= meilleur_module[1] * 0.85):
        recommandation = {
            "type": "pipeline",
            "cible": meilleur_pipeline[0],
            "score": meilleur_pipeline[1],
            "sequence": sequence_pipeline(meilleur_pipeline[0]["ID"]),
        }
    elif meilleur_module:
        recommandation = {
            "type": "module",
            "cible": meilleur_module[0],
            "score": meilleur_module[1],
            "sequence": chaine_modules(meilleur_module[0]["ID"]),
        }

    return {
        "demande": demande,
        "recommandation": recommandation,
        "pipelines": scores_pipelines[:max_results],
        "modules": scores_modules[:max_results],
        "avertissements": avertissements_politique(recommandation),
    }


def avertissements_politique(recommandation):
    """
    Signale les parametres de politique non valides mobilises par la sequence
    retenue. Un chiffre construit sur un parametre non valide ne peut pas etre
    presente sans signalement explicite (controle C18).
    """
    if not recommandation or not recommandation.get("sequence"):
        return []
    ids = {module["ID"] for module in recommandation["sequence"]}
    touches = []
    for parametre in parametres_non_valides():
        utilisateurs = set(split_list(parametre["Utilisé par"]))
        if utilisateurs & ids:
            touches.append({
                "cle": parametre["Clé"],
                "libelle": parametre["Libellé"],
                "source": parametre["Source"],
                "modules": sorted(utilisateurs & ids),
            })
    return touches


# ============ PREFLIGHT ============
def preflight(type_livrable=None):
    """
    Assemble la barriere de sortie: controles bloquants, controles majeurs et
    parametres non valides a signaler avant toute remise.
    """
    tous = controles()
    bloquants = [c for c in tous if c["Bloquant"].strip().upper() == "OUI"]
    majeurs = [c for c in bloquants if c["Sévérité"] == "MAJEUR"]
    critiques = [c for c in bloquants if c["Sévérité"] == "BLOQUANT"]
    convention = nomenclature(code=type_livrable) if type_livrable else []
    return {
        "type_livrable": type_livrable,
        "convention": convention[0] if convention else None,
        "critiques": critiques,
        "majeurs": majeurs,
        "informatifs": [c for c in tous if c["Bloquant"].strip().upper() != "OUI"],
        "parametres_non_valides": parametres_non_valides(),
        "total_controles": len(tous),
    }


# ============ CONTROLE DE COHERENCE DU REFERENTIEL ============
def _verifier_modules(modules, ids):
    """Coherence interne des modules: domaine, references croisees, champs vitaux."""
    anomalies = []
    for row in modules:
        if row["Domaine"] not in DOMAINES:
            anomalies.append("Module %s: domaine inconnu '%s'" % (row["ID"], row["Domaine"]))
        for champ in ("Amont", "Aval", "Gate QA"):
            for ref in split_list(row[champ]):
                if ref not in ("Tous", "") and ref not in ids:
                    anomalies.append("Module %s: %s reference un module inexistant '%s'"
                                     % (row["ID"], champ, ref))
        etapes = split_methode(row["Méthode"])
        if len(etapes) < 3:
            anomalies.append("Module %s: methode trop courte pour etre executable (%d etapes)"
                             % (row["ID"], len(etapes)))
        for champ in ("Entrées", "Sorties", "Pièges"):
            if not split_list(row[champ]):
                anomalies.append("Module %s: champ %s vide" % (row["ID"], champ))
    return anomalies


def _verifier_pipelines(ids):
    """Chaque parcours doit mobiliser des modules existants et se refermer sur le preflight."""
    anomalies = []
    for row in load_csv("pipelines"):
        etapes = split_list(row["Séquence"])
        if not etapes:
            anomalies.append("Pipeline %s: sequence vide" % row["ID"])
            continue
        for ref in etapes:
            if ref not in ids:
                anomalies.append("Pipeline %s: sequence reference un module inexistant '%s'"
                                 % (row["ID"], ref))
        if etapes[-1] != "Q4":
            anomalies.append("Pipeline %s: ne se referme pas sur le preflight Q4" % row["ID"])
    return anomalies


def _verifier_parametres(ids):
    """Statuts connus, modules utilisateurs valides, source declaree."""
    anomalies = []
    statuts_valides = {STATUT_A_VALIDER, "VALIDE", "NON_APPLICABLE"}
    for row in load_csv("parametres"):
        if row["Statut"] not in statuts_valides:
            anomalies.append("Parametre %s: statut inconnu '%s'" % (row["Clé"], row["Statut"]))
        if not row["Source"].strip():
            anomalies.append("Parametre %s: source attendue non declaree" % row["Clé"])
        for ref in split_list(row["Utilisé par"]):
            if ref not in ids:
                anomalies.append("Parametre %s: utilise par un module inexistant '%s'"
                                 % (row["Clé"], ref))
    return anomalies


def _verifier_formules(ids):
    """Rattachement des formules a des modules existants et statut de seuil connu."""
    anomalies = []
    statuts_seuil = {"INDICATIF", "SANS OBJET", STATUT_A_VALIDER, "BLOQUANT"}
    for row in load_csv("formules"):
        if row["Statut du seuil"] not in statuts_seuil:
            anomalies.append("Formule %s: statut de seuil inconnu '%s'"
                             % (row["Clé"], row["Statut du seuil"]))
        for ref in split_list(row["Modules"]):
            if ref not in ids:
                anomalies.append("Formule %s: reference un module inexistant '%s'"
                                 % (row["Clé"], ref))
    return anomalies


def _verifier_controles(ids):
    """Rattachement des controles et validite du champ bloquant."""
    anomalies = []
    for row in load_csv("controles"):
        if row["Module"] not in ids:
            anomalies.append("Controle %s: reference un module inexistant '%s'"
                             % (row["ID"], row["Module"]))
        if row["Bloquant"].strip().upper() not in ("OUI", "NON"):
            anomalies.append("Controle %s: champ Bloquant invalide '%s'"
                             % (row["ID"], row["Bloquant"]))
    return anomalies


def _verifier_nomenclature(ids):
    """Rattachement des conventions de nommage a des modules existants."""
    anomalies = []
    for row in load_csv("nomenclature"):
        if row["Module"] not in ids:
            anomalies.append("Nomenclature %s: reference un module inexistant '%s'"
                             % (row["Code"], row["Module"]))
    return anomalies


def _verifier_references():
    """Presence du document de doctrine de chaque domaine."""
    anomalies = []
    for domaine, fichier in REFERENCE_PAR_DOMAINE.items():
        if not (REFERENCES_DIR / fichier).exists():
            anomalies.append("Domaine %s: document de reference manquant (%s)" % (domaine, fichier))
    return anomalies


def doctor():
    """
    Verifie l'integrite du referentiel: references croisees, domaines connus,
    statuts valides et presence des documents de doctrine.

    Retourne la liste des anomalies; une liste vide signifie referentiel sain.
    """
    modules = load_csv("modules")
    ids = {row["ID"] for row in modules}

    anomalies = []
    anomalies.extend(_verifier_modules(modules, ids))
    anomalies.extend(_verifier_pipelines(ids))
    anomalies.extend(_verifier_parametres(ids))
    anomalies.extend(_verifier_formules(ids))
    anomalies.extend(_verifier_controles(ids))
    anomalies.extend(_verifier_nomenclature(ids))
    anomalies.extend(_verifier_references())
    return anomalies
