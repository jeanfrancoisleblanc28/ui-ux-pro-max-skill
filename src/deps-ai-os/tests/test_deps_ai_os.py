#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests du referentiel et du moteur du DEPS AI Operating System.

Ces tests protegent trois invariants:
  1. le referentiel est coherent (references croisees valides);
  2. le routage envoie une demande courante vers le bon parcours;
  3. aucun parametre de politique non valide ne porte de valeur chiffree.
"""

import re
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import deps_core as core  # noqa: E402


# ============ INTEGRITE DU REFERENTIEL ============
def test_referentiel_sans_anomalie():
    """Le controle d'integrite complet ne doit remonter aucune anomalie."""
    anomalies = core.doctor()
    assert anomalies == [], "Anomalies detectees:\n" + "\n".join(anomalies)


def test_les_six_domaines_sont_peuples():
    modules = core.load_csv("modules")
    domaines = {row["Domaine"] for row in modules}
    assert domaines == set(core.DOMAINES), "Domaines manquants ou inattendus: %s" % domaines


def test_organigramme_conforme():
    """
    Le systeme reproduit exactement l'organigramme retenu: 22 modules repartis
    en 6 domaines. Toute addition ou suppression doit etre un choix explicite.
    """
    effectifs = {}
    for row in core.load_csv("modules"):
        effectifs[row["Domaine"]] = effectifs.get(row["Domaine"], 0) + 1
    assert effectifs == {
        "01-FINANCEMENT": 4,
        "02-FLI-FLS": 4,
        "03-EVALUATION": 4,
        "04-DEVELOPPEMENT-ECONOMIQUE": 3,
        "05-PRODUCTION": 3,
        "06-QA": 4,
    }
    assert sum(effectifs.values()) == 22


def test_identifiants_de_modules_uniques():
    ids = [row["ID"] for row in core.load_csv("modules")]
    assert len(ids) == len(set(ids))


def test_chaque_module_est_joignable_par_un_pipeline():
    """Un module qu'aucun parcours n'atteint est un module mort."""
    couverts = set()
    for pipeline in core.load_csv("pipelines"):
        couverts.update(core.split_list(pipeline["Séquence"]))
    tous = {row["ID"] for row in core.load_csv("modules")}
    assert tous - couverts == set(), "Modules jamais mobilises: %s" % (tous - couverts)


# ============ CHAINES ET PIPELINES ============
def test_chaine_place_les_dependances_avant_le_module():
    chaine = core.chaine_modules("P4")
    ids = [module["ID"] for module in chaine]
    for amont in ("F1", "F2", "F3", "F4", "P1", "P2", "P3"):
        assert ids.index(amont) < ids.index("P4"), "%s doit preceder P4" % amont


def test_chaine_termine_par_les_portes_de_qualite():
    chaine = core.chaine_modules("P4")
    assert chaine[-1]["ID"] == "Q4", "La chaine doit se refermer sur le preflight"


def test_chaine_sans_qa_exclut_les_portes():
    chaine = core.chaine_modules("F3", avec_qa=False)
    assert all(module["Domaine"] != "06-QA" for module in chaine)


def test_dossier_cic_tranche_l_admissibilite_en_premier():
    """Un dossier non admissible ne doit jamais consommer d'analyse financiere."""
    sequence = core.sequence_pipeline("dossier-cic")
    assert sequence[0]["ID"] == "P1"


def test_tarification_vient_apres_la_cotation_de_risque():
    ids = [module["ID"] for module in core.sequence_pipeline("dossier-cic")]
    assert ids.index("F4") < ids.index("P2"), "La tarification suit la cotation, jamais l'inverse"


def test_evaluation_commence_par_la_normalisation():
    sequence = core.sequence_pipeline("evaluation-entreprise")
    assert sequence[0]["ID"] == "E1"


def test_tous_les_pipelines_se_terminent_par_le_preflight():
    for pipeline in core.load_csv("pipelines"):
        etapes = core.split_list(pipeline["Séquence"])
        assert etapes[-1] == "Q4", "Pipeline %s ne se referme pas sur Q4" % pipeline["ID"]


def test_pipeline_inconnu_retourne_none():
    assert core.sequence_pipeline("parcours-inexistant") is None


# ============ ROUTAGE ============
@pytest.mark.parametrize("demande,attendu", [
    ("monter un dossier de financement complet pour le comité", "PL1"),
    ("combien vaut cette entreprise", "PL2"),
    ("vérifie ce document avant que je l'envoie", "PL7"),
    ("vérifie ma note avant que je l'envoie au comité", "PL7"),
    ("quelles subventions pour un projet d'agrandissement", "PL6"),
    ("challenge mon analyse, qu'est-ce que j'oublie", "PL8"),
])
def test_routage_vers_le_bon_parcours(demande, attendu):
    resultat = core.router(demande)
    reco = resultat["recommandation"]
    assert reco is not None
    assert reco["type"] == "pipeline"
    assert reco["cible"]["ID"] == attendu


def test_routage_insensible_aux_accents():
    """'admissibilite' sans accent doit router comme 'admissibilité'."""
    avec = core.router("admissibilité au territoire")
    sans = core.router("admissibilite au territoire")
    assert avec["recommandation"]["cible"]["ID"] == sans["recommandation"]["cible"]["ID"]


def test_routage_nomme_un_module_explicitement():
    resultat = core.router("ouvre le module F3")
    reco = resultat["recommandation"]
    assert reco["type"] == "module"
    assert reco["cible"]["ID"] == "F3"


def test_routage_sans_correspondance_ne_plante_pas():
    resultat = core.router("zzzz qqqq wwww")
    assert resultat["recommandation"] is None
    assert resultat["avertissements"] == []


def test_routage_signale_les_parametres_non_valides():
    """Un parcours qui mobilise un parametre A_VALIDER doit le signaler."""
    resultat = core.router("monter un dossier de financement complet pour le comité")
    cles = {avertissement["cle"] for avertissement in resultat["avertissements"]}
    assert "PLAFOND_ENTREPRISE_FLI" in cles


# ============ PARAMETRES DE POLITIQUE ============
def test_aucun_parametre_non_valide_ne_porte_de_valeur_chiffree():
    """
    Invariant central du systeme: tant qu'un parametre n'est pas valide contre
    la politique en vigueur, il ne doit porter aucune valeur inventee.
    """
    fautifs = []
    for parametre in core.parametres_non_valides():
        valeur = parametre["Valeur"]
        if re.search(r"\d", valeur):
            fautifs.append("%s = %s" % (parametre["Clé"], valeur))
    assert fautifs == [], "Parametres non valides porteurs d'une valeur chiffree: %s" % fautifs


def test_chaque_parametre_declare_sa_source_attendue():
    for parametre in core.load_csv("parametres"):
        assert parametre["Source"].strip(), "Parametre %s sans source" % parametre["Clé"]


def test_chaque_parametre_est_mobilise_par_un_module():
    for parametre in core.load_csv("parametres"):
        assert core.split_list(parametre["Utilisé par"]), \
            "Parametre %s mobilise par aucun module" % parametre["Clé"]


def test_filtre_des_parametres_par_module():
    cles = {parametre["Clé"] for parametre in core.parametres(module="P2")}
    assert "TAUX_REFERENCE" in cles
    assert "SECTEURS_EXCLUS" not in cles


# ============ FORMULES ============
def test_seuils_indicatifs_sont_qualifies():
    """Un seuil ne doit jamais passer pour une regle de politique."""
    statuts_admis = {"INDICATIF", "SANS OBJET", "A_VALIDER", "BLOQUANT"}
    for formule in core.load_csv("formules"):
        assert formule["Statut du seuil"] in statuts_admis, \
            "Formule %s: statut de seuil inconnu '%s'" % (formule["Clé"], formule["Statut du seuil"])


def test_chaque_formule_declare_ses_pieges():
    for formule in core.load_csv("formules"):
        assert formule["Pièges"].strip(), "Formule %s sans piege documente" % formule["Clé"]


def test_formules_de_la_capacite_de_remboursement():
    cles = {formule["Clé"] for formule in core.formules(module="F3")}
    assert {"RCD", "FTDSD"} <= cles


# ============ CONTROLES QUALITE ============
def test_controles_bloquants_declarent_leur_critere():
    for controle in core.controles(bloquants_seulement=True):
        assert controle["Critère de réussite"].strip(), \
            "Controle %s bloquant sans critere de reussite" % controle["ID"]
        assert controle["Comment vérifier"].strip(), \
            "Controle %s bloquant sans methode de verification" % controle["ID"]


def test_chaque_module_qa_porte_des_controles():
    for module_id in ("Q1", "Q2", "Q3", "Q4"):
        assert core.controles(module=module_id), "Module %s sans controle" % module_id


def test_preflight_assemble_la_barriere_de_sortie():
    donnees = core.preflight("NOTE-CIC")
    assert donnees["convention"] is not None
    assert donnees["convention"]["Code"] == "NOTE-CIC"
    assert donnees["critiques"], "Le preflight doit porter des controles bloquants"
    assert donnees["total_controles"] == len(core.load_csv("controles"))


def test_preflight_sur_type_inconnu_reste_utilisable():
    donnees = core.preflight("TYPE-INEXISTANT")
    assert donnees["convention"] is None
    assert donnees["critiques"]


# ============ NOMENCLATURE ============
def test_codes_de_nomenclature_uniques():
    codes = [row["Code"] for row in core.load_csv("nomenclature")]
    assert len(codes) == len(set(codes))


def test_patrons_de_nom_portent_date_et_version():
    for row in core.load_csv("nomenclature"):
        patron = row["Patron de nom"]
        assert patron.startswith("AAAAMMJJ"), "Patron %s sans date en tete" % row["Code"]
        assert patron.endswith("_vN"), "Patron %s sans indice de version" % row["Code"]


# ============ ACCES PAR IDENTIFIANT ============
def test_module_accessible_par_id_et_par_nom():
    par_id = core.get_module("F1")
    par_nom = core.get_module("analyse-financiere")
    assert par_id == par_nom


def test_module_inconnu_retourne_none():
    assert core.get_module("ZZ9") is None


def test_documents_de_reference_presents_pour_chaque_domaine():
    for domaine, fichier in core.REFERENCE_PAR_DOMAINE.items():
        chemin = core.REFERENCES_DIR / fichier
        assert chemin.exists(), "Reference manquante pour %s" % domaine
        assert chemin.stat().st_size > 2000, "Reference trop courte pour %s" % domaine
