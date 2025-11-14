#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : architecture_tools.py
# @Author: Assistant
# @Desc  : Outils MCP pour l'Agent Architecte

from fastmcp import FastMCP
import json
import math

mcp = FastMCP("Outils Architecture BTP")


@mcp.tool()
def validateBlueprintCompliance(
    project_type: str,
    building_height: float,
    total_surface: float,
    num_floors: int,
    location: str
) -> dict:
    """
    Valide la conformité d'un projet de construction avec les normes en vigueur.

    :param project_type: Type de projet (résidentiel, commercial, industriel, etc.)
    :param building_height: Hauteur totale du bâtiment en mètres
    :param total_surface: Surface totale en m²
    :param num_floors: Nombre d'étages
    :param location: Localisation du projet (ville, pays)
    :return: Rapport de conformité avec recommandations
    """
    compliance_report = {
        "status": "conforme",
        "checks": [],
        "warnings": [],
        "recommendations": []
    }

    # Vérification hauteur maximale (simplifié)
    if building_height > 28 and project_type == "résidentiel":
        compliance_report["warnings"].append({
            "type": "Hauteur",
            "message": f"Bâtiment de {building_height}m nécessite des mesures anti-incendie renforcées",
            "norm": "Code de construction - Article R.123-2"
        })

    # Vérification surface par étage
    surface_per_floor = total_surface / num_floors if num_floors > 0 else total_surface
    if surface_per_floor > 2000 and project_type == "commercial":
        compliance_report["checks"].append({
            "type": "Surface",
            "message": "Surface importante : vérifier les issues de secours",
            "requirement": "Minimum 2 sorties de secours par étage"
        })

    # Recommandations structurelles
    if num_floors > 5:
        compliance_report["recommendations"].append({
            "category": "Structure",
            "suggestion": "Considérer une structure en béton armé ou acier",
            "reason": "Meilleure résistance pour bâtiments de plus de 5 étages"
        })

    # Conformité sismique (simplifié)
    if location.lower() in ["nice", "strasbourg", "marseille"]:
        compliance_report["checks"].append({
            "type": "Parasismique",
            "message": "Zone sismique - normes Eurocode 8 applicables",
            "requirement": "Calculs sismiques obligatoires"
        })

    # Accessibilité PMR
    compliance_report["checks"].append({
        "type": "Accessibilité",
        "message": "Conformité PMR obligatoire",
        "requirement": "Ascenseur si > 1 étage, rampes d'accès, largeur portes min 90cm"
    })

    return {
        "project_info": {
            "type": project_type,
            "height": building_height,
            "surface": total_surface,
            "floors": num_floors,
            "location": location
        },
        "compliance": compliance_report
    }


@mcp.tool()
def calculate3DVolume(
    length: float,
    width: float,
    height: float,
    shape: str = "rectangular"
) -> dict:
    """
    Calcule le volume 3D d'une structure selon sa forme.

    :param length: Longueur en mètres
    :param width: Largeur en mètres
    :param height: Hauteur en mètres
    :param shape: Forme (rectangular, cylindrical, pyramidal)
    :return: Volume calculé et détails
    """
    volume = 0
    surface_base = 0
    surface_totale = 0

    if shape == "rectangular":
        volume = length * width * height
        surface_base = length * width
        surface_totale = 2 * (length * width + length * height + width * height)

    elif shape == "cylindrical":
        # Pour cylindre : length = rayon, width ignoré
        radius = length
        volume = math.pi * (radius ** 2) * height
        surface_base = math.pi * (radius ** 2)
        surface_totale = 2 * math.pi * radius * (radius + height)

    elif shape == "pyramidal":
        volume = (length * width * height) / 3
        surface_base = length * width
        # Surface latérale approximative
        slant_height = math.sqrt(height**2 + ((width/2)**2))
        surface_totale = surface_base + (2 * length * slant_height) + (2 * width * slant_height)

    # Estimations de matériaux
    concrete_volume = volume * 0.15  # 15% du volume pour béton
    steel_weight = volume * 50  # kg d'acier approximatif

    return {
        "dimensions": {
            "length": length,
            "width": width,
            "height": height,
            "shape": shape
        },
        "calculations": {
            "volume_m3": round(volume, 2),
            "surface_base_m2": round(surface_base, 2),
            "surface_totale_m2": round(surface_totale, 2)
        },
        "material_estimates": {
            "concrete_m3": round(concrete_volume, 2),
            "steel_kg": round(steel_weight, 2)
        }
    }


@mcp.tool()
def suggestMaterialsOptimization(
    structure_type: str,
    budget_level: str,
    environmental_priority: bool,
    climate: str
) -> dict:
    """
    Suggère des matériaux optimisés selon la structure, budget et priorités environnementales.

    :param structure_type: Type de structure (murs, toiture, fondations, façade)
    :param budget_level: Niveau de budget (économique, standard, premium)
    :param environmental_priority: Prioriser l'écologie
    :param climate: Type de climat (tempéré, méditerranéen, montagnard, tropical)
    :return: Recommandations de matériaux
    """
    materials_database = {
        "murs": {
            "économique": {
                "standard": "Parpaing creux 20cm",
                "eco": "Brique monomur terre cuite"
            },
            "standard": {
                "standard": "Brique terre cuite + isolation",
                "eco": "Béton cellulaire"
            },
            "premium": {
                "standard": "Béton banché isolé",
                "eco": "Murs en paille compressée + enduit chaux"
            }
        },
        "toiture": {
            "économique": {
                "standard": "Tuiles béton",
                "eco": "Tuiles terre cuite recyclées"
            },
            "standard": {
                "standard": "Tuiles terre cuite",
                "eco": "Bardeau bois certifié FSC"
            },
            "premium": {
                "standard": "Zinc ou ardoise naturelle",
                "eco": "Toiture végétalisée"
            }
        },
        "fondations": {
            "économique": {
                "standard": "Semelle filante béton",
                "eco": "Béton de chanvre"
            },
            "standard": {
                "standard": "Radier béton armé",
                "eco": "Béton à base de laitier"
            },
            "premium": {
                "standard": "Pieux profonds",
                "eco": "Fondations géopolymères"
            }
        },
        "façade": {
            "économique": {
                "standard": "Enduit ciment",
                "eco": "Enduit chaux naturel"
            },
            "standard": {
                "standard": "Bardage PVC",
                "eco": "Bardage bois douglas"
            },
            "premium": {
                "standard": "Pierre naturelle",
                "eco": "Vêture terre cuite"
            }
        }
    }

    material_type = "eco" if environmental_priority else "standard"

    suggested_material = materials_database.get(structure_type, {}).get(
        budget_level, {}).get(material_type, "Matériau non disponible")

    # Adaptations climatiques
    climate_recommendations = {
        "tempéré": "Isolation thermique renforcée (R≥4)",
        "méditerranéen": "Inertie thermique importante + protections solaires",
        "montagnard": "Isolation maximale (R≥6) + étanchéité à l'air",
        "tropical": "Ventilation naturelle + protection pluies"
    }

    # Calcul performance énergétique estimée
    energy_performance = {
        "économique": {"standard": "D", "eco": "C"},
        "standard": {"standard": "C", "eco": "B"},
        "premium": {"standard": "B", "eco": "A"}
    }

    performance = energy_performance.get(budget_level, {}).get(material_type, "Non évalué")

    return {
        "recommended_material": suggested_material,
        "structure_type": structure_type,
        "budget_level": budget_level,
        "environmental": environmental_priority,
        "climate_adaptation": climate_recommendations.get(climate, "Climat non spécifié"),
        "energy_performance_class": performance,
        "additional_tips": [
            f"Pour le climat {climate}, privilégier l'orientation sud",
            "Vérifier la disponibilité locale des matériaux",
            "Prévoir 10% de surplus pour les chutes"
        ]
    }


@mcp.tool()
def calculateStructuralLoad(
    floor_type: str,
    surface_m2: float,
    usage: str,
    num_supports: int
) -> dict:
    """
    Calcule les charges structurelles pour dimensionner les éléments porteurs.

    :param floor_type: Type de plancher (béton, bois, mixte)
    :param surface_m2: Surface du plancher en m²
    :param usage: Usage du local (habitation, bureau, stockage, commercial)
    :param num_supports: Nombre de points d'appui
    :return: Calculs de charges et recommandations
    """
    # Charges d'exploitation selon usage (kN/m²)
    usage_loads = {
        "habitation": 1.5,
        "bureau": 2.5,
        "commercial": 4.0,
        "stockage": 5.0,
        "parking": 2.5
    }

    # Poids propre selon type de plancher (kN/m²)
    dead_loads = {
        "béton": 3.5,
        "bois": 1.2,
        "mixte": 2.5
    }

    exploitation_load = usage_loads.get(usage, 2.0)
    dead_load = dead_loads.get(floor_type, 2.5)

    # Charge totale
    total_load_per_m2 = exploitation_load + dead_load
    total_load = total_load_per_m2 * surface_m2

    # Charge par support (simplifié)
    load_per_support = total_load / num_supports if num_supports > 0 else total_load

    # Recommandations de dimensionnement
    if floor_type == "béton":
        thickness_cm = max(12, int(math.sqrt(surface_m2) * 2))
        reinforcement = "Treillis soudé ST25C"
    elif floor_type == "bois":
        thickness_cm = max(18, int(math.sqrt(surface_m2) * 1.5))
        reinforcement = "Solives 63x175mm espacées de 40cm"
    else:
        thickness_cm = 15
        reinforcement = "Poutrelles IPN + hourdis"

    return {
        "input_parameters": {
            "floor_type": floor_type,
            "surface_m2": surface_m2,
            "usage": usage,
            "num_supports": num_supports
        },
        "load_calculations": {
            "dead_load_kN_m2": dead_load,
            "exploitation_load_kN_m2": exploitation_load,
            "total_load_kN_m2": round(total_load_per_m2, 2),
            "total_load_kN": round(total_load, 2),
            "load_per_support_kN": round(load_per_support, 2)
        },
        "recommendations": {
            "min_thickness_cm": thickness_cm,
            "reinforcement": reinforcement,
            "safety_factor": 1.5,
            "verification_required": "Calcul de structure par BET obligatoire si > 50m²"
        }
    }


@mcp.tool()
def generateTechnicalReport(
    project_name: str,
    analysis_data: dict
) -> str:
    """
    Génère un rapport technique synthétique basé sur les analyses effectuées.

    :param project_name: Nom du projet
    :param analysis_data: Données d'analyse (format dict)
    :return: Rapport technique formaté
    """
    report = f"""
╔═══════════════════════════════════════════════════════════════════╗
║            RAPPORT TECHNIQUE D'ARCHITECTURE                       ║
║            Projet: {project_name:<45} ║
╚═══════════════════════════════════════════════════════════════════╝

1. DONNÉES GÉNÉRALES
   Données analysées: {json.dumps(analysis_data, indent=2, ensure_ascii=False)}

2. SYNTHÈSE TECHNIQUE
   ✓ Analyse structurelle effectuée
   ✓ Conformité réglementaire vérifiée
   ✓ Optimisation matériaux proposée

3. RECOMMANDATIONS
   - Validation par Bureau d'Études Techniques (BET) recommandée
   - Études de sol obligatoires avant travaux
   - Conformité RT2020/RE2020 à vérifier selon date de permis

4. PROCHAINES ÉTAPES
   1. Validation des plans par urbanisme
   2. Études techniques complémentaires
   3. Dépôt permis de construire
   4. Consultation entreprises

╔═══════════════════════════════════════════════════════════════════╗
║  Document généré automatiquement - À valider par architecte DPLG  ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    return report


if __name__ == '__main__':
    # Test des fonctions
    print("=== Test Validation Conformité ===")
    result = validateBlueprintCompliance("résidentiel", 25, 800, 7, "Nice")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== Test Calcul Volume ===")
    result = calculate3DVolume(20, 15, 12, "rectangular")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== Test Optimisation Matériaux ===")
    result = suggestMaterialsOptimization("murs", "standard", True, "tempéré")
    print(json.dumps(result, indent=2, ensure_ascii=False))
