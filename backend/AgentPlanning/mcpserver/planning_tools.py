#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : planning_tools.py
# @Author: Assistant
# @Desc  : Outils MCP pour la planification de projets BTP

from fastmcp import FastMCP
import json
from datetime import datetime, timedelta
from typing import List, Dict

mcp = FastMCP("Outils Planning BTP")


def calculate_end_date(start_date: datetime, duration_days: int, exclude_weekends: bool = True) -> datetime:
    """Calcule la date de fin en excluant les week-ends si demandé"""
    if not exclude_weekends:
        return start_date + timedelta(days=duration_days)

    days_added = 0
    current_date = start_date

    while days_added < duration_days:
        current_date += timedelta(days=1)
        # 0 = lundi, 6 = dimanche
        if current_date.weekday() < 5:  # Lundi à vendredi
            days_added += 1

    return current_date


@mcp.tool()
def createGanttChart(
    project_name: str,
    start_date: str,
    tasks: list
) -> dict:
    """
    Crée un diagramme de Gantt pour le planning du projet.

    :param project_name: Nom du projet
    :param start_date: Date de début du projet (format YYYY-MM-DD)
    :param tasks: Liste de tâches avec {name, duration_days, dependencies[], trade}
    :return: Données du diagramme de Gantt
    """
    try:
        project_start = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Format de date invalide. Utiliser YYYY-MM-DD"}

    # Dictionnaire pour stocker les tâches avec leurs dates
    task_schedule = {}

    # Fonction récursive pour calculer la date de début d'une tâche
    def calculate_task_start(task_name: str, task_data: dict, processed: set) -> datetime:
        if task_name in processed:
            return task_schedule[task_name]["start"]

        dependencies = task_data.get("dependencies", [])

        if not dependencies:
            # Pas de dépendances, commence au début du projet
            return project_start

        # Trouver la fin la plus tardive parmi les dépendances
        latest_end = project_start
        for dep_name in dependencies:
            dep_task = next((t for t in tasks if t["name"] == dep_name), None)
            if dep_task:
                dep_start = calculate_task_start(dep_name, dep_task, processed)
                dep_end = calculate_end_date(dep_start, dep_task["duration_days"])
                if dep_end > latest_end:
                    latest_end = dep_end

        return latest_end

    # Calculer le planning pour chaque tâche
    processed_tasks = set()
    gantt_data = []

    for task in tasks:
        task_name = task["name"]
        task_start = calculate_task_start(task_name, task, processed_tasks)
        task_end = calculate_end_date(task_start, task["duration_days"])

        task_schedule[task_name] = {
            "start": task_start,
            "end": task_end,
            "duration_days": task["duration_days"]
        }

        gantt_entry = {
            "task_name": task_name,
            "trade": task.get("trade", "Non spécifié"),
            "start_date": task_start.strftime("%Y-%m-%d"),
            "end_date": task_end.strftime("%Y-%m-%d"),
            "duration_days": task["duration_days"],
            "dependencies": task.get("dependencies", []),
            "week_number": task_start.isocalendar()[1]
        }

        gantt_data.append(gantt_entry)
        processed_tasks.add(task_name)

    # Calculer la date de fin du projet
    project_end = max([task_schedule[t]["end"] for t in task_schedule])
    total_duration = (project_end - project_start).days

    return {
        "project_info": {
            "name": project_name,
            "start_date": project_start.strftime("%Y-%m-%d"),
            "end_date": project_end.strftime("%Y-%m-%d"),
            "total_duration_days": total_duration,
            "total_duration_weeks": round(total_duration / 7, 1)
        },
        "gantt_chart": sorted(gantt_data, key=lambda x: x["start_date"]),
        "notes": [
            "Les week-ends sont exclus des calculs",
            "Prévoir marge de 10-15% pour intempéries",
            "Vérifier disponibilité des ressources"
        ]
    }


@mcp.tool()
def detectCriticalPath(
    tasks: list
) -> dict:
    """
    Identifie le chemin critique du projet (séquence de tâches déterminant la durée minimale).

    :param tasks: Liste de tâches avec {name, duration_days, dependencies[]}
    :return: Chemin critique et analyse
    """
    # Construction du graphe de dépendances
    task_dict = {task["name"]: task for task in tasks}

    # Calcul des dates au plus tôt (forward pass)
    earliest_start = {}
    earliest_finish = {}

    def calculate_earliest(task_name: str, visited: set) -> int:
        if task_name in visited:
            return earliest_finish[task_name]

        visited.add(task_name)
        task = task_dict[task_name]
        dependencies = task.get("dependencies", [])

        if not dependencies:
            earliest_start[task_name] = 0
        else:
            earliest_start[task_name] = max(
                calculate_earliest(dep, visited) for dep in dependencies
            )

        earliest_finish[task_name] = earliest_start[task_name] + task["duration_days"]
        return earliest_finish[task_name]

    # Calculer pour toutes les tâches
    visited_set = set()
    for task in tasks:
        calculate_earliest(task["name"], visited_set)

    # Durée totale du projet
    project_duration = max(earliest_finish.values())

    # Calcul des dates au plus tard (backward pass)
    latest_start = {}
    latest_finish = {}

    # Initialiser les tâches finales
    for task_name, ef in earliest_finish.items():
        if ef == project_duration:
            latest_finish[task_name] = project_duration

    def calculate_latest(task_name: str, visited: set):
        if task_name in visited:
            return

        visited.add(task_name)
        task = task_dict[task_name]

        # Trouver les tâches qui dépendent de celle-ci
        dependents = [
            t["name"] for t in tasks
            if task_name in t.get("dependencies", [])
        ]

        if not dependents:
            # Tâche finale
            latest_finish[task_name] = project_duration
        else:
            # Calculer d'abord les dépendants
            for dep in dependents:
                if dep not in visited:
                    calculate_latest(dep, visited)

            latest_finish[task_name] = min(
                latest_start[dep] for dep in dependents
            )

        latest_start[task_name] = latest_finish[task_name] - task["duration_days"]

    # Calculer pour toutes les tâches
    visited_set_backward = set()
    # Commencer par les tâches finales
    final_tasks = [name for name, ef in earliest_finish.items() if ef == project_duration]
    for task_name in final_tasks:
        calculate_latest(task_name, visited_set_backward)

    # Identifier les tâches critiques (marge = 0)
    critical_tasks = []
    task_analysis = []

    for task_name in task_dict:
        if task_name not in latest_start:
            continue

        slack = latest_start[task_name] - earliest_start[task_name]
        is_critical = slack == 0

        if is_critical:
            critical_tasks.append(task_name)

        task_analysis.append({
            "task_name": task_name,
            "duration_days": task_dict[task_name]["duration_days"],
            "earliest_start": earliest_start[task_name],
            "earliest_finish": earliest_finish[task_name],
            "latest_start": latest_start[task_name],
            "latest_finish": latest_finish[task_name],
            "slack_days": slack,
            "is_critical": is_critical,
            "priority": "CRITIQUE" if is_critical else "NORMALE" if slack <= 5 else "FLEXIBLE"
        })

    # Reconstruire le chemin critique
    critical_path = []
    current_tasks = [t for t in critical_tasks if not any(
        t in task_dict[other].get("dependencies", [])
        for other in critical_tasks
    )]

    while current_tasks:
        task_name = current_tasks.pop(0)
        critical_path.append(task_name)

        # Trouver les successeurs critiques
        successors = [
            t for t in critical_tasks
            if task_name in task_dict[t].get("dependencies", [])
            and t not in critical_path
        ]
        current_tasks.extend(successors)

    return {
        "project_duration_days": project_duration,
        "critical_path": critical_path,
        "critical_tasks_count": len(critical_tasks),
        "task_analysis": sorted(task_analysis, key=lambda x: x["earliest_start"]),
        "recommendations": [
            f"Surveiller étroitement les {len(critical_tasks)} tâches critiques",
            "Tout retard sur le chemin critique retarde le projet entier",
            "Allouer des ressources prioritaires aux tâches critiques",
            "Anticiper les risques sur ces tâches"
        ]
    }


@mcp.tool()
def optimizeResourceAllocation(
    tasks: list,
    available_resources: dict,
    start_date: str
) -> dict:
    """
    Optimise l'allocation des ressources pour éviter les sur/sous-utilisations.

    :param tasks: Liste de tâches avec {name, duration_days, dependencies[], required_resources{trade: count}}
    :param available_resources: Ressources disponibles {trade: max_count}
    :param start_date: Date de début (YYYY-MM-DD)
    :return: Planning optimisé des ressources
    """
    try:
        project_start = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Format de date invalide"}

    # Première passe : calculer le planning sans contraintes de ressources
    task_schedule = {}

    def calculate_task_dates(task_name: str, task_data: dict, processed: set):
        if task_name in processed:
            return

        dependencies = task_data.get("dependencies", [])

        if not dependencies:
            task_start = project_start
        else:
            latest_dep_end = project_start
            for dep in dependencies:
                dep_task = next((t for t in tasks if t["name"] == dep), None)
                if dep_task and dep not in processed:
                    calculate_task_dates(dep, dep_task, processed)

                if dep in task_schedule:
                    dep_end = task_schedule[dep]["end"]
                    if dep_end > latest_dep_end:
                        latest_dep_end = dep_end

            task_start = latest_dep_end

        task_end = calculate_end_date(task_start, task_data["duration_days"])

        task_schedule[task_name] = {
            "start": task_start,
            "end": task_end,
            "duration": task_data["duration_days"],
            "resources": task_data.get("required_resources", {})
        }

        processed.add(task_name)

    # Calculer les dates pour toutes les tâches
    processed = set()
    for task in tasks:
        calculate_task_dates(task["name"], task, processed)

    # Analyse de l'utilisation des ressources par période
    project_end = max(t["end"] for t in task_schedule.values())
    current_date = project_start

    resource_timeline = []
    conflicts = []

    while current_date <= project_end:
        daily_usage = {trade: 0 for trade in available_resources.keys()}

        # Compter les ressources utilisées ce jour
        active_tasks = []
        for task_name, schedule in task_schedule.items():
            if schedule["start"] <= current_date < schedule["end"]:
                active_tasks.append(task_name)
                for trade, count in schedule["resources"].items():
                    daily_usage[trade] = daily_usage.get(trade, 0) + count

        # Détecter les conflits
        day_conflicts = []
        for trade, usage in daily_usage.items():
            if trade in available_resources and usage > available_resources[trade]:
                day_conflicts.append({
                    "trade": trade,
                    "required": usage,
                    "available": available_resources[trade],
                    "overflow": usage - available_resources[trade]
                })

        if day_conflicts:
            conflicts.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "conflicts": day_conflicts,
                "active_tasks": active_tasks
            })

        resource_timeline.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "usage": daily_usage,
            "utilization_percent": {
                trade: round((daily_usage.get(trade, 0) / available_resources[trade] * 100), 1)
                for trade in available_resources.keys()
                if available_resources[trade] > 0
            }
        })

        current_date += timedelta(days=1)

    # Calculer les statistiques d'utilisation
    avg_utilization = {}
    for trade in available_resources.keys():
        if available_resources[trade] > 0:
            total_util = sum(
                day["usage"].get(trade, 0) / available_resources[trade]
                for day in resource_timeline
            )
            avg_utilization[trade] = round((total_util / len(resource_timeline) * 100), 1)

    # Recommandations
    recommendations = []
    if conflicts:
        recommendations.append(f"⚠️ {len(conflicts)} jour(s) avec conflits de ressources détectés")
        recommendations.append("Considérer l'ajout de ressources ou le décalage de tâches non-critiques")

    for trade, util in avg_utilization.items():
        if util < 50:
            recommendations.append(f"{trade}: Sous-utilisation ({util}%) - réduire les ressources?")
        elif util > 90:
            recommendations.append(f"{trade}: Sur-utilisation ({util}%) - ajouter des ressources?")

    return {
        "summary": {
            "project_start": project_start.strftime("%Y-%m-%d"),
            "project_end": project_end.strftime("%Y-%m-%d"),
            "total_days": (project_end - project_start).days,
            "conflicts_detected": len(conflicts) > 0,
            "conflict_days_count": len(conflicts)
        },
        "available_resources": available_resources,
        "average_utilization_percent": avg_utilization,
        "resource_conflicts": conflicts[:10],  # Limiter à 10 premiers conflits
        "recommendations": recommendations,
        "optimization_tips": [
            "Privilégier les tâches sur le chemin critique",
            "Lisser la charge de travail dans le temps",
            "Prévoir des ressources tampons pour les imprévus"
        ]
    }


@mcp.tool()
def simulateScenario(
    base_duration_days: int,
    scenario_type: str,
    impact_percent: int
) -> dict:
    """
    Simule l'impact de différents scénarios sur le planning.

    :param base_duration_days: Durée de base du projet en jours
    :param scenario_type: Type de scénario (intempéries, retard_livraison, main_oeuvre, optimiste)
    :param impact_percent: Impact en pourcentage (positif=retard, négatif=avance)
    :return: Analyse du scénario
    """
    scenarios_description = {
        "intempéries": "Impact des conditions météorologiques défavorables",
        "retard_livraison": "Retard dans la livraison des matériaux",
        "main_oeuvre": "Disponibilité réduite de la main-d'œuvre",
        "optimiste": "Conditions idéales et optimisation des processus",
        "accident": "Incident de chantier nécessitant un arrêt temporaire",
        "modification_client": "Changements demandés par le client en cours de projet"
    }

    # Calcul de l'impact
    duration_change = (base_duration_days * impact_percent) / 100
    new_duration = base_duration_days + duration_change

    # Probabilité d'occurrence (simplifié)
    probabilities = {
        "intempéries": 0.65,
        "retard_livraison": 0.35,
        "main_oeuvre": 0.25,
        "optimiste": 0.15,
        "accident": 0.10,
        "modification_client": 0.40
    }

    probability = probabilities.get(scenario_type, 0.5)

    # Coût estimé de l'impact
    daily_cost = 500  # Coût journalier moyen d'un chantier (simplifié)
    cost_impact = abs(duration_change) * daily_cost

    # Mesures d'atténuation suggérées
    mitigation_measures = {
        "intempéries": [
            "Planifier les tâches extérieures en saison favorable",
            "Prévoir des bâches et protections",
            "Avoir des tâches intérieures en backup"
        ],
        "retard_livraison": [
            "Commander avec délais de sécurité de 2 semaines",
            "Identifier des fournisseurs alternatifs",
            "Stocker les matériaux critiques en avance"
        ],
        "main_oeuvre": [
            "Contractualiser avec plusieurs équipes",
            "Planifier avec marge de capacité de 10-15%",
            "Former du personnel polyvalent"
        ],
        "optimiste": [
            "Capitaliser sur cette avance pour améliorer la qualité",
            "Anticiper les phases suivantes",
            "Utiliser le temps gagné pour les finitions"
        ],
        "accident": [
            "Souscrire assurances chantier adaptées",
            "Former à la sécurité",
            "Audits sécurité réguliers"
        ],
        "modification_client": [
            "Formaliser un processus de gestion du changement",
            "Chiffrer immédiatement l'impact délai/coût",
            "Prévoir une clause de révision dans le contrat"
        ]
    }

    return {
        "scenario": {
            "type": scenario_type,
            "description": scenarios_description.get(scenario_type, "Scénario personnalisé"),
            "probability_percent": round(probability * 100, 1),
            "impact_percent": impact_percent
        },
        "duration_impact": {
            "base_duration_days": base_duration_days,
            "duration_change_days": round(duration_change, 1),
            "new_projected_duration_days": round(new_duration, 1),
            "difference_weeks": round(duration_change / 7, 1)
        },
        "financial_impact": {
            "estimated_cost_impact_euro": round(cost_impact, 2),
            "daily_cost_euro": daily_cost
        },
        "risk_level": "FAIBLE" if abs(impact_percent) < 10 else "MOYEN" if abs(impact_percent) < 20 else "ÉLEVÉ",
        "mitigation_measures": mitigation_measures.get(scenario_type, ["Analyser les causes spécifiques", "Définir un plan d'action adapté"]),
        "recommendation": f"Prévoir une marge de {abs(impact_percent)}% sur le planning initial" if impact_percent > 0 else "Capitaliser sur cette optimisation"
    }


@mcp.tool()
def generateMilestoneReport(
    project_name: str,
    milestones: list,
    current_date: str
) -> dict:
    """
    Génère un rapport sur les jalons du projet.

    :param project_name: Nom du projet
    :param milestones: Liste des jalons avec {name, planned_date, actual_date, status}
    :param current_date: Date actuelle (YYYY-MM-DD)
    :return: Rapport des jalons
    """
    try:
        today = datetime.strptime(current_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Format de date invalide"}

    milestone_status = []
    delays = []
    upcoming = []

    for milestone in milestones:
        planned = datetime.strptime(milestone["planned_date"], "%Y-%m-%d")
        actual = datetime.strptime(milestone["actual_date"], "%Y-%m-%d") if milestone.get("actual_date") else None
        status = milestone.get("status", "en_cours")

        if actual:
            delay_days = (actual - planned).days
        elif status == "en_cours":
            delay_days = (today - planned).days if today > planned else 0
        else:
            delay_days = 0

        milestone_info = {
            "name": milestone["name"],
            "planned_date": milestone["planned_date"],
            "actual_date": milestone.get("actual_date", "Non atteint"),
            "status": status,
            "delay_days": delay_days if status != "à_venir" else None,
            "status_icon": "✅" if status == "terminé" else "🔄" if status == "en_cours" else "📅"
        }

        milestone_status.append(milestone_info)

        if delay_days > 0 and status in ["terminé", "en_cours"]:
            delays.append({
                "milestone": milestone["name"],
                "delay_days": delay_days,
                "planned": milestone["planned_date"]
            })

        if status == "à_venir" and planned > today:
            days_until = (planned - today).days
            if days_until <= 30:
                upcoming.append({
                    "milestone": milestone["name"],
                    "date": milestone["planned_date"],
                    "days_until": days_until
                })

    # Statistiques
    total_milestones = len(milestones)
    completed = sum(1 for m in milestones if m.get("status") == "terminé")
    in_progress = sum(1 for m in milestones if m.get("status") == "en_cours")
    completion_rate = (completed / total_milestones * 100) if total_milestones > 0 else 0

    avg_delay = sum(d["delay_days"] for d in delays) / len(delays) if delays else 0

    return {
        "project_name": project_name,
        "report_date": current_date,
        "statistics": {
            "total_milestones": total_milestones,
            "completed": completed,
            "in_progress": in_progress,
            "pending": total_milestones - completed - in_progress,
            "completion_rate_percent": round(completion_rate, 1),
            "average_delay_days": round(avg_delay, 1)
        },
        "milestones": milestone_status,
        "delays": sorted(delays, key=lambda x: x["delay_days"], reverse=True),
        "upcoming_milestones": sorted(upcoming, key=lambda x: x["days_until"]),
        "alerts": [
            f"⚠️ {len(delays)} jalon(s) en retard" if delays else "✅ Aucun retard",
            f"📅 {len(upcoming)} jalon(s) à venir dans les 30 jours" if upcoming else "Aucun jalon imminent"
        ]
    }


if __name__ == '__main__':
    # Tests
    print("=== Test Gantt Chart ===")
    tasks = [
        {"name": "Fondations", "duration_days": 15, "dependencies": [], "trade": "maçon"},
        {"name": "Murs", "duration_days": 20, "dependencies": ["Fondations"], "trade": "maçon"},
        {"name": "Charpente", "duration_days": 10, "dependencies": ["Murs"], "trade": "charpentier"},
        {"name": "Toiture", "duration_days": 8, "dependencies": ["Charpente"], "trade": "couvreur"}
    ]
    result = createGanttChart("Maison Exemple", "2025-03-01", tasks)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== Test Chemin Critique ===")
    result = detectCriticalPath(tasks)
    print(json.dumps(result, indent=2, ensure_ascii=False))
