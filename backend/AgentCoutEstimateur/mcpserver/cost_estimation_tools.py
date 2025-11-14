#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cost_estimation_tools.py
# @Author: Assistant
# @Desc  : Outils MCP pour l'estimation des coûts BTP

from fastmcp import FastMCP
import json
from datetime import datetime

mcp = FastMCP("Outils Estimation Coûts BTP")

# Base de données simplifiée des prix (€/unité) - Prix indicatifs 2025
MATERIAL_PRICES = {
    "béton": {"unit": "m³", "price": 120, "variance": 0.15},
    "parpaing": {"unit": "unité", "price": 1.2, "variance": 0.10},
    "brique": {"unit": "unité", "price": 0.8, "variance": 0.12},
    "ciment": {"unit": "sac 25kg", "price": 8, "variance": 0.20},
    "sable": {"unit": "tonne", "price": 35, "variance": 0.10},
    "gravier": {"unit": "tonne", "price": 40, "variance": 0.10},
    "acier": {"unit": "kg", "price": 2.5, "variance": 0.25},
    "bois_charpente": {"unit": "m³", "price": 450, "variance": 0.15},
    "plaque_platre": {"unit": "m²", "price": 8, "variance": 0.08},
    "tuile": {"unit": "m²", "price": 35, "variance": 0.12},
    "isolation_laine": {"unit": "m²", "price": 15, "variance": 0.10},
    "peinture": {"unit": "litre", "price": 25, "variance": 0.15},
    "carrelage": {"unit": "m²", "price": 30, "variance": 0.20},
    "fenetre_pvc": {"unit": "unité", "price": 350, "variance": 0.15},
    "porte": {"unit": "unité", "price": 200, "variance": 0.18}
}

# Tarifs horaires main d'œuvre (€/heure)
LABOR_RATES = {
    "maçon": 45,
    "charpentier": 50,
    "électricien": 55,
    "plombier": 55,
    "plâtrier": 42,
    "couvreur": 48,
    "peintre": 40,
    "carreleur": 43,
    "menuisier": 48,
    "chef_chantier": 65,
    "manœuvre": 35
}


@mcp.tool()
def estimateMaterialCost(
    materials: list,
    include_transport: bool = True,
    project_location: str = "urbain"
) -> dict:
    """
    Estime le coût total des matériaux pour un projet de construction.

    :param materials: Liste de dicts avec {name, quantity, unit}
    :param include_transport: Inclure les frais de transport
    :param project_location: Localisation (urbain, péri-urbain, rural)
    :return: Estimation détaillée des coûts
    """
    total_cost = 0
    material_breakdown = []
    warnings = []

    # Coefficient de transport selon localisation
    transport_coeff = {
        "urbain": 1.05,
        "péri-urbain": 1.10,
        "rural": 1.20
    }

    location_multiplier = transport_coeff.get(project_location, 1.10)

    for material in materials:
        material_name = material.get("name", "").lower()
        quantity = material.get("quantity", 0)

        if material_name in MATERIAL_PRICES:
            price_data = MATERIAL_PRICES[material_name]
            unit_price = price_data["price"]
            variance = price_data["variance"]

            # Calcul du coût avec variabilité de marché
            base_cost = unit_price * quantity

            # Ajout transport si nécessaire
            if include_transport:
                transport_cost = base_cost * (location_multiplier - 1)
                total_item_cost = base_cost + transport_cost
            else:
                transport_cost = 0
                total_item_cost = base_cost

            material_breakdown.append({
                "material": material_name,
                "quantity": quantity,
                "unit": price_data["unit"],
                "unit_price_euro": unit_price,
                "base_cost_euro": round(base_cost, 2),
                "transport_cost_euro": round(transport_cost, 2) if include_transport else 0,
                "total_cost_euro": round(total_item_cost, 2),
                "price_variance": f"±{int(variance * 100)}%"
            })

            total_cost += total_item_cost

            # Avertissement si grosse variabilité
            if variance > 0.15:
                warnings.append(f"{material_name}: Forte variabilité de prix ({int(variance*100)}%), vérifier les prix actuels du marché")

        else:
            warnings.append(f"Matériau '{material_name}' non trouvé dans la base de prix")

    # Marge d'imprévus recommandée
    contingency_rate = 0.12
    contingency_amount = total_cost * contingency_rate

    return {
        "estimation_date": datetime.now().strftime("%Y-%m-%d"),
        "project_location": project_location,
        "material_details": material_breakdown,
        "cost_summary": {
            "subtotal_materials_euro": round(total_cost, 2),
            "contingency_12_percent_euro": round(contingency_amount, 2),
            "estimated_total_euro": round(total_cost + contingency_amount, 2)
        },
        "warnings": warnings,
        "notes": [
            "Prix basés sur indices BT01 2025",
            "Variabilité selon fournisseurs et volumes",
            "Marge d'imprévus de 12% recommandée",
            "Valider les prix avec devis fournisseurs"
        ]
    }


@mcp.tool()
def calculateLaborHours(
    tasks: list,
    team_composition: dict
) -> dict:
    """
    Calcule les heures de main-d'œuvre et les coûts associés.

    :param tasks: Liste de tâches avec {task_name, trade, estimated_hours}
    :param team_composition: Composition de l'équipe {trade: num_workers}
    :return: Calcul détaillé des heures et coûts
    """
    labor_breakdown = []
    total_hours_by_trade = {}
    total_cost = 0

    # Traiter chaque tâche
    for task in tasks:
        task_name = task.get("task_name", "Tâche inconnue")
        trade = task.get("trade", "").lower()
        estimated_hours = task.get("estimated_hours", 0)

        if trade in LABOR_RATES:
            hourly_rate = LABOR_RATES[trade]
            task_cost = hourly_rate * estimated_hours

            labor_breakdown.append({
                "task": task_name,
                "trade": trade,
                "hours": estimated_hours,
                "hourly_rate_euro": hourly_rate,
                "total_cost_euro": round(task_cost, 2)
            })

            # Accumulation par corps de métier
            if trade not in total_hours_by_trade:
                total_hours_by_trade[trade] = {
                    "hours": 0,
                    "cost": 0,
                    "rate": hourly_rate
                }

            total_hours_by_trade[trade]["hours"] += estimated_hours
            total_hours_by_trade[trade]["cost"] += task_cost
            total_cost += task_cost

    # Calcul durée projet selon composition équipe
    project_duration_days = 0
    duration_details = []

    for trade, data in total_hours_by_trade.items():
        num_workers = team_composition.get(trade, 1)
        hours_per_worker = data["hours"] / num_workers if num_workers > 0 else data["hours"]
        days_per_worker = hours_per_worker / 8  # 8h par jour

        duration_details.append({
            "trade": trade,
            "total_hours": data["hours"],
            "num_workers": num_workers,
            "hours_per_worker": round(hours_per_worker, 1),
            "days_per_worker": round(days_per_worker, 1)
        })

        # Durée maximale = durée du projet
        project_duration_days = max(project_duration_days, days_per_worker)

    # Coûts supplémentaires (charges sociales ~45%)
    social_charges_rate = 0.45
    social_charges = total_cost * social_charges_rate

    # Coûts de gestion chantier (~8%)
    site_management = (total_cost + social_charges) * 0.08

    total_labor_cost = total_cost + social_charges + site_management

    return {
        "task_breakdown": labor_breakdown,
        "summary_by_trade": [
            {
                "trade": trade,
                "total_hours": data["hours"],
                "hourly_rate_euro": data["rate"],
                "subtotal_euro": round(data["cost"], 2)
            }
            for trade, data in total_hours_by_trade.items()
        ],
        "cost_summary": {
            "base_labor_cost_euro": round(total_cost, 2),
            "social_charges_45_percent_euro": round(social_charges, 2),
            "site_management_8_percent_euro": round(site_management, 2),
            "total_labor_cost_euro": round(total_labor_cost, 2)
        },
        "project_timeline": {
            "estimated_duration_days": round(project_duration_days, 1),
            "estimated_duration_weeks": round(project_duration_days / 5, 1),
            "duration_by_trade": duration_details
        },
        "notes": [
            "Charges sociales estimées à 45%",
            "Gestion de chantier incluse (8%)",
            "Durée calculée sur base 8h/jour",
            "Prévoir délais pour intempéries et approvisionnements"
        ]
    }


@mcp.tool()
def trackBudgetDeviation(
    initial_budget: float,
    spent_to_date: float,
    work_completion_percent: float,
    remaining_costs_estimate: float
) -> dict:
    """
    Suit les écarts budgétaires et projette le coût final.

    :param initial_budget: Budget initial prévu (€)
    :param spent_to_date: Montant dépensé à ce jour (€)
    :param work_completion_percent: Pourcentage d'avancement des travaux (0-100)
    :param remaining_costs_estimate: Estimation des coûts restants (€)
    :return: Analyse des déviations budgétaires
    """
    # Calculs de base
    projected_final_cost = spent_to_date + remaining_costs_estimate
    budget_deviation = projected_final_cost - initial_budget
    deviation_percent = (budget_deviation / initial_budget) * 100 if initial_budget > 0 else 0

    # Coût prévu à ce stade d'avancement
    expected_cost_at_completion = (initial_budget * work_completion_percent) / 100
    current_deviation = spent_to_date - expected_cost_at_completion
    current_deviation_percent = (current_deviation / expected_cost_at_completion) * 100 if expected_cost_at_completion > 0 else 0

    # Statut du projet
    if deviation_percent < -5:
        status = "SOUS BUDGET"
        alert_level = "success"
    elif deviation_percent <= 5:
        status = "DANS LES NORMES"
        alert_level = "info"
    elif deviation_percent <= 15:
        status = "ATTENTION"
        alert_level = "warning"
    else:
        status = "DÉPASSEMENT CRITIQUE"
        alert_level = "critical"

    # Recommandations
    recommendations = []
    if deviation_percent > 5:
        recommendations.append("Analyser les postes de dépassement")
        recommendations.append("Renégocier avec fournisseurs si possible")
        recommendations.append("Identifier les optimisations possibles")

    if current_deviation_percent > 10:
        recommendations.append("Contrôler davantage les dépenses courantes")
        recommendations.append("Revoir la planification des travaux restants")

    if work_completion_percent < 50 and deviation_percent > 10:
        recommendations.append("⚠️ ALERTE: Dépassement précoce, risque d'aggravation")

    return {
        "budget_analysis": {
            "initial_budget_euro": round(initial_budget, 2),
            "spent_to_date_euro": round(spent_to_date, 2),
            "work_completion_percent": work_completion_percent,
            "expected_cost_at_stage_euro": round(expected_cost_at_completion, 2),
            "current_deviation_euro": round(current_deviation, 2),
            "current_deviation_percent": round(current_deviation_percent, 1)
        },
        "projection": {
            "remaining_costs_estimate_euro": round(remaining_costs_estimate, 2),
            "projected_final_cost_euro": round(projected_final_cost, 2),
            "budget_deviation_euro": round(budget_deviation, 2),
            "deviation_percent": round(deviation_percent, 1),
            "status": status,
            "alert_level": alert_level
        },
        "recommendations": recommendations if recommendations else ["Budget maîtrisé, continuer le suivi régulier"],
        "key_indicators": {
            "cost_performance_index": round(expected_cost_at_completion / spent_to_date, 2) if spent_to_date > 0 else 0,
            "budget_remaining_euro": round(initial_budget - spent_to_date, 2),
            "completion_vs_spending_ratio": round(work_completion_percent / (spent_to_date / initial_budget * 100), 2) if spent_to_date > 0 else 0
        }
    }


@mcp.tool()
def generateCostBreakdown(
    project_name: str,
    material_costs: dict,
    labor_costs: dict,
    other_costs: dict
) -> dict:
    """
    Génère un devis détaillé complet du projet.

    :param project_name: Nom du projet
    :param material_costs: Coûts matériaux {category: amount}
    :param labor_costs: Coûts main-d'œuvre {category: amount}
    :param other_costs: Autres coûts {category: amount}
    :return: Devis détaillé formaté
    """
    # Totaux par catégorie
    total_materials = sum(material_costs.values())
    total_labor = sum(labor_costs.values())
    total_other = sum(other_costs.values())

    subtotal = total_materials + total_labor + total_other

    # TVA (20% pour construction neuve, 10% pour rénovation)
    tva_rate = 0.20
    tva_amount = subtotal * tva_rate

    # Total TTC
    total_ttc = subtotal + tva_amount

    # Génération du devis formaté
    breakdown = {
        "project_info": {
            "name": project_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "reference": f"DEVIS-{datetime.now().strftime('%Y%m%d-%H%M')}"
        },
        "material_costs": {
            "details": material_costs,
            "subtotal_euro": round(total_materials, 2),
            "percent_of_total": round((total_materials / subtotal * 100), 1) if subtotal > 0 else 0
        },
        "labor_costs": {
            "details": labor_costs,
            "subtotal_euro": round(total_labor, 2),
            "percent_of_total": round((total_labor / subtotal * 100), 1) if subtotal > 0 else 0
        },
        "other_costs": {
            "details": other_costs,
            "subtotal_euro": round(total_other, 2),
            "percent_of_total": round((total_other / subtotal * 100), 1) if subtotal > 0 else 0
        },
        "totals": {
            "subtotal_ht_euro": round(subtotal, 2),
            "tva_20_percent_euro": round(tva_amount, 2),
            "total_ttc_euro": round(total_ttc, 2)
        },
        "payment_terms": {
            "deposit_30_percent_euro": round(total_ttc * 0.30, 2),
            "progress_payment_40_percent_euro": round(total_ttc * 0.40, 2),
            "final_payment_30_percent_euro": round(total_ttc * 0.30, 2)
        },
        "validity": "Ce devis est valable 90 jours",
        "notes": [
            "Prix fermes et définitifs sauf modification du projet",
            "Paiement selon échéancier: 30% acompte, 40% mi-travaux, 30% livraison",
            "Garantie décennale incluse",
            "Délais sous réserve d'obtention des autorisations administratives"
        ]
    }

    return breakdown


@mcp.tool()
def comparePriceAlternatives(
    base_option: dict,
    alternative_options: list
) -> dict:
    """
    Compare différentes alternatives de prix pour optimiser les coûts.

    :param base_option: Option de base {name, description, total_cost}
    :param alternative_options: Liste d'alternatives avec mêmes champs
    :return: Comparaison détaillée des options
    """
    base_cost = base_option.get("total_cost", 0)

    comparisons = []

    for alt in alternative_options:
        alt_cost = alt.get("total_cost", 0)
        savings = base_cost - alt_cost
        savings_percent = (savings / base_cost * 100) if base_cost > 0 else 0

        comparison = {
            "name": alt.get("name", "Option alternative"),
            "description": alt.get("description", ""),
            "cost_euro": round(alt_cost, 2),
            "vs_base_cost_diff_euro": round(savings, 2),
            "savings_percent": round(savings_percent, 1),
            "pros": alt.get("pros", []),
            "cons": alt.get("cons", []),
            "recommendation": "RECOMMANDÉ" if savings > 0 and savings_percent >= 10 else "À CONSIDÉRER" if savings > 0 else "PLUS CHER"
        }

        comparisons.append(comparison)

    # Tri par économie décroissante
    comparisons.sort(key=lambda x: x["vs_base_cost_diff_euro"], reverse=True)

    return {
        "base_option": {
            "name": base_option.get("name", "Option de base"),
            "description": base_option.get("description", ""),
            "cost_euro": round(base_cost, 2)
        },
        "alternatives": comparisons,
        "best_savings_option": comparisons[0]["name"] if comparisons else None,
        "max_potential_savings_euro": round(comparisons[0]["vs_base_cost_diff_euro"], 2) if comparisons else 0
    }


if __name__ == '__main__':
    # Tests
    print("=== Test Estimation Matériaux ===")
    materials = [
        {"name": "béton", "quantity": 50},
        {"name": "acier", "quantity": 2000},
        {"name": "brique", "quantity": 5000}
    ]
    result = estimateMaterialCost(materials, True, "urbain")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== Test Calcul Main d'Œuvre ===")
    tasks = [
        {"task_name": "Fondations", "trade": "maçon", "estimated_hours": 120},
        {"task_name": "Charpente", "trade": "charpentier", "estimated_hours": 80}
    ]
    team = {"maçon": 3, "charpentier": 2}
    result = calculateLaborHours(tasks, team)
    print(json.dumps(result, indent=2, ensure_ascii=False))
