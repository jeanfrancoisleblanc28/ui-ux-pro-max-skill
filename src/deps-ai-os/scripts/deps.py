#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEPS AI Operating System - Interface en ligne de commande.

Usage:
  python3 deps.py route "<demande>" [-n 5] [--json]
  python3 deps.py module <ID|nom> [--sans-qa] [--json]
  python3 deps.py pipeline [<ID|nom>] [--json]
  python3 deps.py params [--fonds FLI] [--statut A_VALIDER] [--module P3] [--json]
  python3 deps.py formule [<cle|recherche>] [--module F3] [--json]
  python3 deps.py qa [--module Q1] [--bloquants] [--json]
  python3 deps.py preflight [--type NOTE-CIC] [--json]
  python3 deps.py nomenclature [--type NOTE-CIC] [--module P4] [--json]
  python3 deps.py doctor [--json]
"""

import argparse
import io
import json
import sys

from deps_core import (
    DOMAINES,
    REFERENCE_PAR_DOMAINE,
    MAX_RESULTS,
    chaine_modules,
    controles,
    doctor,
    formules,
    get_module,
    get_pipeline,
    load_csv,
    nomenclature,
    parametres,
    preflight,
    router,
    sequence_pipeline,
    split_list,
    split_methode,
)

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

TIRET = "-" * 72


def _titre(texte):
    return "\n%s\n%s" % (texte, TIRET)


def _puces(valeur):
    """Rend une liste en puces, avec majuscule initiale sur chaque element."""
    elements = []
    for element in split_list(valeur):
        elements.append("  - %s%s" % (element[:1].upper(), element[1:]))
    return elements


def _ligne_module(module):
    return "  %-3s %-28s %-24s" % (module["ID"], module["Domaine"], module["Module"])


MAX_CLES_PAR_SOURCE = 4


def _bloc_avertissements(avertissements):
    """
    Resume les parametres non valides en les groupant par document source.

    Le regroupement par source est la forme actionnable: il dit quel document
    ouvrir et combien de lignes y renseigner. Derouler les 22 parametres a
    chaque routage occuperait la moitie de la reponse et entrainerait surtout
    le lecteur a ne plus lire l'avertissement. Le detail complet reste
    disponible par `params --statut A_VALIDER` et dans la sortie --json.
    """
    if not avertissements:
        return []

    par_source = {}
    for parametre in avertissements:
        par_source.setdefault(parametre["source"], []).append(parametre["cle"])

    out = [_titre("[!] %d PARAMETRES DE POLITIQUE NON VALIDES MOBILISES" % len(avertissements)),
           "Aucun chiffre qui en depend ne peut etre presente comme definitif (controle C18).",
           "A renseigner depuis :"]
    for source in sorted(par_source):
        cles = sorted(par_source[source])
        visibles = ", ".join(cles[:MAX_CLES_PAR_SOURCE])
        reste = len(cles) - MAX_CLES_PAR_SOURCE
        if reste > 0:
            visibles += ", +%d autres" % reste
        out.append("  %2d  %s" % (len(cles), source))
        out.append("      %s" % visibles)
    out.append("Liste complete et mise en service : deps.py params --statut A_VALIDER")
    return out


# ============ FORMATAGE ============
def format_route(resultat):
    out = ["## DEPS AI OS - Routage", 'Demande: "%s"' % resultat["demande"]]
    reco = resultat["recommandation"]

    if not reco:
        out.append("\nAucune correspondance. Reformulez la demande ou consultez "
                   "`deps.py pipeline` pour la liste des parcours disponibles.")
        return "\n".join(out)

    cible = reco["cible"]
    if reco["type"] == "pipeline":
        out.append(_titre("RECOMMANDATION - pipeline %s : %s (score %.2f)"
                          % (cible["ID"], cible["Pipeline"], reco["score"])))
        out.append("Objectif : %s" % cible["Objectif"])
        out.append("Livrable : %s" % cible["Livrable final"])
        out.append("Controle humain : %s" % cible["Point de contrôle humain"])
        out.append("Regle : %s" % cible["Note"])
    else:
        out.append(_titre("RECOMMANDATION - module %s : %s (score %.2f)"
                          % (cible["ID"], cible["Module"], reco["score"])))
        out.append("Domaine  : %s" % DOMAINES.get(cible["Domaine"], cible["Domaine"]))
        out.append("Objectif : %s" % cible["Objectif"])

    sequence = reco.get("sequence") or []
    out.append(_titre("SEQUENCE D'EXECUTION (%d etapes)" % len(sequence)))
    for rang, module in enumerate(sequence, 1):
        out.append("%2d. %s" % (rang, _ligne_module(module).strip()))
        out.append("    -> %s" % module["Sorties"].split(";")[0].strip())

    out.extend(_bloc_avertissements(resultat["avertissements"]))

    if resultat["pipelines"]:
        out.append(_titre("AUTRES PARCOURS"))
        for pipeline, score in resultat["pipelines"][1:]:
            out.append("  %-4s %-22s %.2f  %s" % (pipeline["ID"], pipeline["Pipeline"],
                                                  score, pipeline["Objectif"][:70]))
    if resultat["modules"]:
        out.append(_titre("MODULES CONNEXES"))
        for module, score in resultat["modules"][:MAX_RESULTS]:
            out.append("  %-3s %-24s %.2f  %s" % (module["ID"], module["Module"],
                                                  score, module["Objectif"][:70]))
    return "\n".join(out)


def format_module(module, sequence):
    out = ["## %s - %s" % (module["ID"], module["Module"]),
           "Domaine : %s" % DOMAINES.get(module["Domaine"], module["Domaine"]),
           "",
           module["Objectif"]]

    out.append(_titre("ENTREES REQUISES"))
    out.extend(_puces(module["Entrées"]))

    out.append(_titre("METHODE"))
    for etape in split_methode(module["Méthode"]):
        out.append("  %s" % etape)

    out.append(_titre("SORTIES"))
    out.extend(_puces(module["Sorties"]))

    out.append(_titre("PIEGES A EVITER"))
    out.extend(_puces(module["Pièges"]))

    liees = formules(module=module["ID"])
    if liees:
        out.append(_titre("FORMULES MOBILISEES"))
        for formule in liees:
            out.append("  %-16s %s" % (formule["Clé"], formule["Formule"]))
            if formule["Statut du seuil"] == "INDICATIF":
                out.append("  %-16s seuil indicatif : %s (non contractuel)"
                           % ("", formule["Seuil indicatif"]))

    requis = parametres(module=module["ID"])
    if requis:
        out.append(_titre("PARAMETRES DE POLITIQUE REQUIS"))
        for parametre in requis:
            marque = "[!]" if parametre["Statut"] == "A_VALIDER" else "[ok]"
            out.append("  %s %-26s %s" % (marque, parametre["Clé"], parametre["Libellé"]))

    gates = controles(module=None)
    gates = [c for c in gates if c["Module"] in split_list(module["Gate QA"])]
    if gates:
        out.append(_titre("PORTES DE CONTROLE (%s)" % module["Gate QA"]))
        for controle in gates:
            if controle["Bloquant"].strip().upper() == "OUI":
                out.append("  %-5s %-9s %s" % (controle["ID"], controle["Sévérité"], controle["Contrôle"]))

    out.append(_titre("CHAINE D'EXECUTION COMPLETE"))
    for rang, etape in enumerate(sequence or [], 1):
        marque = " <=" if etape["ID"] == module["ID"] else ""
        out.append("%2d. %s%s" % (rang, _ligne_module(etape).strip(), marque))

    reference = REFERENCE_PAR_DOMAINE.get(module["Domaine"])
    if reference:
        out.append("\nDoctrine detaillee : references/%s" % reference)
    return "\n".join(out)


def format_pipelines(rows):
    out = ["## DEPS AI OS - Parcours disponibles"]
    for row in rows:
        out.append(_titre("%s : %s" % (row["ID"], row["Pipeline"])))
        out.append(row["Objectif"])
        out.append("Sequence : %s" % " > ".join(split_list(row["Séquence"])))
        out.append("Livrable : %s" % row["Livrable final"])
    return "\n".join(out)


def format_pipeline(pipeline, sequence):
    out = ["## %s - %s" % (pipeline["ID"], pipeline["Pipeline"]),
           "",
           pipeline["Objectif"],
           "",
           "Livrable final   : %s" % pipeline["Livrable final"],
           "Controle humain  : %s" % pipeline["Point de contrôle humain"],
           "Regle du parcours: %s" % pipeline["Note"]]
    out.append(_titre("SEQUENCE (%d etapes)" % len(sequence)))
    for rang, module in enumerate(sequence, 1):
        out.append("%2d. %-3s %-28s %s" % (rang, module["ID"], module["Module"], module["Objectif"][:60]))
    return "\n".join(out)


def format_params(rows):
    out = ["## Parametres de politique (%d)" % len(rows),
           "Un parametre au statut A_VALIDER ne peut alimenter aucun chiffre presente",
           "sans signalement explicite. Renseignez la valeur et la source, puis passez",
           "le statut a VALIDE avec sa date."]
    for row in rows:
        marque = "[!]" if row["Statut"] == "A_VALIDER" else "[ok]"
        out.append(_titre("%s %s" % (marque, row["Clé"])))
        out.append("  Libelle    : %s" % row["Libellé"])
        out.append("  Fonds      : %-12s Unite : %s" % (row["Fonds"], row["Unité"]))
        out.append("  Valeur     : %s" % row["Valeur"])
        out.append("  Statut     : %s" % row["Statut"])
        out.append("  Source     : %s" % row["Source"])
        out.append("  Utilise par: %s" % row["Utilisé par"])
        out.append("  Note       : %s" % row["Note"])
    return "\n".join(out)


def format_formules(rows):
    out = ["## Formules normalisees (%d)" % len(rows)]
    for row in rows:
        out.append(_titre("%s - %s  [%s]" % (row["Clé"], row["Nom"], row["Catégorie"])))
        out.append("  %s" % row["Formule"])
        out.append("  Termes         : %s" % row["Termes"])
        out.append("  Interpretation : %s" % row["Interprétation"])
        out.append("  Seuil          : %s (%s)" % (row["Seuil indicatif"], row["Statut du seuil"]))
        out.append("  Pieges         : %s" % row["Pièges"])
        out.append("  Modules        : %s" % row["Modules"])
    return "\n".join(out)


def format_qa(rows):
    out = ["## Controles qualite (%d)" % len(rows)]
    for row in rows:
        out.append("\n%-5s %-3s %-9s %s" % (row["ID"], row["Module"], row["Sévérité"], row["Contrôle"]))
        out.append("      Portee   : %s" % row["Portée"])
        out.append("      Methode  : %s" % row["Comment vérifier"])
        out.append("      Reussite : %s" % row["Critère de réussite"])
        out.append("      Bloquant : %s" % row["Bloquant"])
    return "\n".join(out)


def format_preflight(donnees):
    out = ["## PREFLIGHT - barriere de sortie",
           "Aucun livrable ne quitte l'organisation sans un statut rendu et date."]

    convention = donnees["convention"]
    if convention:
        out.append(_titre("NOMENCLATURE ATTENDUE (%s)" % convention["Code"]))
        out.append("  Patron  : %s" % convention["Patron de nom"])
        out.append("  Exemple : %s" % convention["Exemple"])
        out.append("  Version : %s" % convention["Règle de version"])
    elif donnees["type_livrable"]:
        out.append("\n[!] Type de livrable inconnu : %s" % donnees["type_livrable"])
        out.append("    Consultez `deps.py nomenclature` pour la liste des codes.")

    out.append(_titre("CONTROLES BLOQUANTS (%d)" % len(donnees["critiques"])))
    for controle in donnees["critiques"]:
        out.append("  [ ] %-5s %-3s %s" % (controle["ID"], controle["Module"], controle["Contrôle"]))

    out.append(_titre("CONTROLES MAJEURS (%d)" % len(donnees["majeurs"])))
    for controle in donnees["majeurs"]:
        out.append("  [ ] %-5s %-3s %s" % (controle["ID"], controle["Module"], controle["Contrôle"]))

    out.append(_titre("CONTROLES INFORMATIFS (%d)" % len(donnees["informatifs"])))
    for controle in donnees["informatifs"]:
        out.append("  [ ] %-5s %-3s %s" % (controle["ID"], controle["Module"], controle["Contrôle"]))

    non_valides = donnees["parametres_non_valides"]
    out.append(_titre("[!] PARAMETRES DE POLITIQUE NON VALIDES (%d)" % len(non_valides)))
    if non_valides:
        out.append("Tant qu'un parametre reste A_VALIDER, tout chiffre qui en depend doit etre")
        out.append("presente comme provisoire et signale au lecteur (controle C18).")
        for parametre in non_valides:
            out.append("  - %-26s (%s)" % (parametre["Clé"], parametre["Source"]))
    else:
        out.append("Aucun. Tous les parametres mobilisables sont valides.")

    out.append(_titre("STATUT DE SORTIE"))
    out.append("  ( ) PRET            tous les controles bloquants passes")
    out.append("  ( ) PRET SOUS RESERVE  reserves nommees et acceptees par le destinataire")
    out.append("  ( ) BLOQUE          motifs a inscrire ci-dessous")
    return "\n".join(out)


def format_nomenclature(rows):
    out = ["## Conventions de nommage (%d)" % len(rows)]
    for row in rows:
        out.append(_titre("%s - %s (module %s)" % (row["Code"], row["Type de livrable"], row["Module"])))
        out.append("  Patron  : %s" % row["Patron de nom"])
        out.append("  Exemple : %s" % row["Exemple"])
        out.append("  Version : %s" % row["Règle de version"])
        out.append("  Note    : %s" % row["Note"])
    return "\n".join(out)


def format_doctor(anomalies):
    if not anomalies:
        return "## Doctor\nReferentiel sain : aucune anomalie detectee."
    out = ["## Doctor", "%d anomalie(s) detectee(s) :" % len(anomalies)]
    for anomalie in anomalies:
        out.append("  - %s" % anomalie)
    return "\n".join(out)


# ============ CLI ============
def build_parser():
    parser = argparse.ArgumentParser(
        prog="deps.py",
        description="DEPS AI Operating System - routage et referentiel de travail.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="commande")

    p_route = sub.add_parser("route", help="Oriente une demande vers un pipeline ou un module")
    p_route.add_argument("demande")
    p_route.add_argument("-n", "--max-results", type=int, default=MAX_RESULTS)
    p_route.add_argument("--json", action="store_true")

    p_module = sub.add_parser("module", help="Fiche complete d'un module")
    p_module.add_argument("identifiant")
    p_module.add_argument("--sans-qa", action="store_true", help="Chaine sans les portes de controle")
    p_module.add_argument("--json", action="store_true")

    p_pipeline = sub.add_parser("pipeline", help="Parcours pre-cables")
    p_pipeline.add_argument("identifiant", nargs="?")
    p_pipeline.add_argument("--json", action="store_true")

    p_params = sub.add_parser("params", help="Parametres de la politique d'investissement")
    p_params.add_argument("--fonds")
    p_params.add_argument("--statut")
    p_params.add_argument("--module")
    p_params.add_argument("--json", action="store_true")

    p_formule = sub.add_parser("formule", help="Formules financieres normalisees")
    p_formule.add_argument("recherche", nargs="?")
    p_formule.add_argument("--module")
    p_formule.add_argument("--json", action="store_true")

    p_qa = sub.add_parser("qa", help="Controles qualite")
    p_qa.add_argument("--module")
    p_qa.add_argument("--bloquants", action="store_true")
    p_qa.add_argument("--json", action="store_true")

    p_pre = sub.add_parser("preflight", help="Barriere de sortie avant remise")
    p_pre.add_argument("--type", dest="type_livrable")
    p_pre.add_argument("--json", action="store_true")

    p_nom = sub.add_parser("nomenclature", help="Conventions de nommage des livrables")
    p_nom.add_argument("--type", dest="code")
    p_nom.add_argument("--module")
    p_nom.add_argument("--json", action="store_true")

    p_doc = sub.add_parser("doctor", help="Controle d'integrite du referentiel")
    p_doc.add_argument("--json", action="store_true")

    return parser


def executer(args):
    """Retourne un couple (donnees_json, texte) selon la commande demandee."""
    if args.commande == "route":
        resultat = router(args.demande, args.max_results)
        payload = {
            "demande": resultat["demande"],
            "recommandation": resultat["recommandation"],
            "pipelines": [{"pipeline": p, "score": s} for p, s in resultat["pipelines"]],
            "modules": [{"module": m, "score": s} for m, s in resultat["modules"]],
            "avertissements": resultat["avertissements"],
        }
        return payload, format_route(resultat)

    if args.commande == "module":
        module = get_module(args.identifiant)
        if not module:
            return {"erreur": "Module inconnu: %s" % args.identifiant}, \
                "Module inconnu: %s" % args.identifiant
        sequence = chaine_modules(module["ID"], avec_qa=not args.sans_qa)
        return {"module": module, "sequence": sequence}, format_module(module, sequence)

    if args.commande == "pipeline":
        if not args.identifiant:
            rows = load_csv("pipelines")
            return {"pipelines": rows}, format_pipelines(rows)
        sequence = sequence_pipeline(args.identifiant)
        if sequence is None:
            return {"erreur": "Pipeline inconnu: %s" % args.identifiant}, \
                "Pipeline inconnu: %s" % args.identifiant
        pipeline = get_pipeline(args.identifiant)
        return {"pipeline": pipeline, "sequence": sequence}, format_pipeline(pipeline, sequence)

    if args.commande == "params":
        rows = parametres(fonds=args.fonds, statut=args.statut, module=args.module)
        return {"parametres": rows}, format_params(rows)

    if args.commande == "formule":
        rows = formules(module=args.module, recherche=args.recherche)
        return {"formules": rows}, format_formules(rows)

    if args.commande == "qa":
        rows = controles(module=args.module, bloquants_seulement=args.bloquants)
        return {"controles": rows}, format_qa(rows)

    if args.commande == "preflight":
        donnees = preflight(args.type_livrable)
        return donnees, format_preflight(donnees)

    if args.commande == "nomenclature":
        rows = nomenclature(code=args.code, module=args.module)
        return {"nomenclature": rows}, format_nomenclature(rows)

    if args.commande == "doctor":
        anomalies = doctor()
        return {"anomalies": anomalies, "sain": not anomalies}, format_doctor(anomalies)

    return None, None


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.commande:
        parser.print_help()
        return 0

    payload, texte = executer(args)
    if payload is None:
        parser.print_help()
        return 0

    if getattr(args, "json", False):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(texte)

    if args.commande == "doctor" and payload.get("anomalies"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
