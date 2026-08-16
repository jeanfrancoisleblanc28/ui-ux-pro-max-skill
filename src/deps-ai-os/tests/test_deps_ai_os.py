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


# ============ LISIBILITE DE LA SORTIE ============
def test_le_routage_resume_les_avertissements_sans_les_noyer():
    """
    Un signal repete 22 fois a chaque routage cesse d'etre un signal: le bloc
    d'avertissements doit rester une fraction minoritaire de la reponse, et
    dire quel document ouvrir plutot que derouler chaque parametre.
    """
    import deps  # noqa: E402

    resultat = core.router("monter un dossier de financement complet pour le comité")
    assert len(resultat["avertissements"]) > 10, "cas de test devenu non representatif"

    texte = deps.format_route(resultat)
    lignes = texte.splitlines()
    bloc = deps._bloc_avertissements(resultat["avertissements"])

    assert len(bloc) < len(lignes) / 3, (
        "le bloc d'avertissements occupe %d lignes sur %d" % (len(bloc), len(lignes))
    )
    # Le compte exact reste annonce, et le chemin vers le detail aussi.
    rendu = "\n".join(bloc)
    assert str(len(resultat["avertissements"])) in rendu, "le nombre exact doit rester affiche"
    assert "params --statut A_VALIDER" in rendu, "le chemin vers le detail doit rester donne"


def test_le_json_conserve_tous_les_avertissements():
    """Le resume est une affaire d'affichage: aucun consommateur ne perd de donnee."""
    resultat = core.router("monter un dossier de financement complet pour le comité")
    cles = {avertissement["cle"] for avertissement in resultat["avertissements"]}
    attendues = {p["Clé"] for p in core.parametres_non_valides()
                 if set(core.split_list(p["Utilisé par"]))
                 & {m["ID"] for m in resultat["recommandation"]["sequence"]}}
    assert cles == attendues


# ============ ORDRE D'EXECUTION ============
def _violations_d_ordre(sequence, par_id):
    """Dependances declarees qui apparaissent apres ce qui les consomme."""
    rang = {mid: i for i, mid in enumerate(sequence)}
    return [(mid, amont) for mid in sequence
            for amont in core.split_list(par_id[mid]["Amont"])
            if amont in rang and rang[amont] > rang[mid]]


def test_toutes_les_chaines_respectent_les_dependances():
    """
    Trier par position dans le CSV n'est pas un tri topologique: F2 declare P1
    en amont alors que P1 lui est posterieur dans le fichier. La chaine doit
    respecter les dependances, pas l'ordre du fichier.
    """
    par_id = {m["ID"]: m for m in core.load_csv("modules")}
    fautives = []
    for module_id in par_id:
        for avec_qa in (False, True):
            sequence = [m["ID"] for m in core.chaine_modules(module_id, avec_qa=avec_qa)]
            for mid, amont in _violations_d_ordre(sequence, par_id):
                fautives.append("chaine(%s, qa=%s): %s precede son amont %s"
                                % (module_id, avec_qa, mid, amont))
    assert fautives == [], "\n".join(fautives)


def test_la_chaine_place_p1_avant_f2():
    """Cas concret du defaut: le montage financier consomme l'admissibilite."""
    sequence = [m["ID"] for m in core.chaine_modules("F3", avec_qa=False)]
    assert sequence.index("P1") < sequence.index("F2")


def test_tous_les_pipelines_respectent_les_dependances():
    """
    Un parcours peut omettre une dependance (le diagnostic express saute le
    montage), mais s'il la mobilise, elle doit preceder ce qui la consomme.
    """
    par_id = {m["ID"]: m for m in core.load_csv("modules")}
    fautifs = []
    for pipeline in core.load_csv("pipelines"):
        sequence = core.split_list(pipeline["Séquence"])
        for mid, amont in _violations_d_ordre(sequence, par_id):
            fautifs.append("%s: %s precede son amont %s" % (pipeline["ID"], mid, amont))
    assert fautifs == [], "\n".join(fautifs)


def test_les_dependances_ne_forment_pas_de_cycle():
    assert [a for a in core.doctor() if "Cycle" in a] == []


# ============ INVARIANT DE VALIDATION DES PARAMETRES ============
def test_un_parametre_valide_mais_vide_n_est_pas_valide():
    """
    Passer un statut a VALIDE sans renseigner la valeur eteindrait l'alerte
    tout en laissant la case vide. Le systeme doit echouer ferme.
    """
    incomplet = {"Clé": "TEST", "Statut": "VALIDE",
                 "Valeur": "À_RENSEIGNER", "Date de validation": ""}
    assert not core.est_valide(incomplet)
    assert core.lacunes_parametre(incomplet) == [
        "valeur non renseignee", "date de validation absente",
    ]


def test_un_parametre_valide_sans_date_n_est_pas_valide():
    sans_date = {"Clé": "TEST", "Statut": "VALIDE",
                 "Valeur": "150 000 $", "Date de validation": "  "}
    assert not core.est_valide(sans_date)


def test_un_parametre_complet_est_valide():
    complet = {"Clé": "TEST", "Statut": "VALIDE",
               "Valeur": "150 000 $", "Date de validation": "2026-01-15"}
    assert core.est_valide(complet)
    assert core.lacunes_parametre(complet) == []


def _referentiel_avec_parametre_force(tmp_path, cle, statut):
    """Copie le referentiel en forcant le statut d'un parametre, sans y toucher."""
    import csv as csv_module

    rows = list(csv_module.DictReader(
        open(core.DATA_DIR / core.FILES["parametres"], encoding="utf-8")))
    for row in rows:
        if row["Clé"] == cle:
            row["Statut"] = statut
    dossier = tmp_path / "data"
    dossier.mkdir()
    for fichier in core.FILES.values():
        (dossier / fichier).write_bytes((core.DATA_DIR / fichier).read_bytes())
    with open(dossier / core.FILES["parametres"], "w", encoding="utf-8", newline="") as handle:
        writer = csv_module.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return dossier


def test_doctor_signale_un_valide_incomplet(tmp_path, monkeypatch):
    """Le controle d'integrite doit nommer un parametre declare valide a tort."""
    dossier = _referentiel_avec_parametre_force(tmp_path, "PLAFOND_ENTREPRISE_FLI", "VALIDE")
    monkeypatch.setattr(core, "DATA_DIR", dossier)
    anomalies = [a for a in core.doctor() if "VALIDE" in a]
    assert anomalies, "un parametre declare VALIDE sans valeur doit etre signale"
    assert any("PLAFOND_ENTREPRISE_FLI" in a for a in anomalies)


def test_un_parametre_valide_a_tort_continue_d_alerter(tmp_path, monkeypatch):
    """Il doit rester dans les avertissements de routage et de preflight."""
    dossier = _referentiel_avec_parametre_force(tmp_path, "PLAFOND_ENTREPRISE_FLI", "VALIDE")
    monkeypatch.setattr(core, "DATA_DIR", dossier)
    cles = {p["Clé"] for p in core.parametres_non_valides()}
    assert "PLAFOND_ENTREPRISE_FLI" in cles


def test_un_parametre_non_applicable_sort_des_alertes():
    """NON_APPLICABLE declare que le parametre ne s'applique pas: pas une lacune."""
    non_applicable = {"Clé": "TEST", "Statut": "NON_APPLICABLE",
                      "Valeur": "À_RENSEIGNER", "Date de validation": ""}
    assert not core.est_valide(non_applicable)
    assert core.STATUT_NON_APPLICABLE in core.STATUTS_PARAMETRE
