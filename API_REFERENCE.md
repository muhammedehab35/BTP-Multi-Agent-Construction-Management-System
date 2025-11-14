# 📚 API Reference - BTP Multi-Agent System

## Overview

This document describes all MCP tools available in each agent.

---

## 🏛️ Agent Architect Tools

### 1. validateBlueprintCompliance

Validates project compliance with building regulations.

**Parameters:**
```python
{
  "project_type": str,        # residential, commercial, industrial
  "building_height": float,   # in meters
  "total_surface": float,     # in m²
  "num_floors": int,          # number of floors
  "location": str             # city, country
}
```

**Returns:**
```json
{
  "project_info": {...},
  "compliance": {
    "status": "compliant",
    "checks": [...],
    "warnings": [...],
    "recommendations": [...]
  }
}
```

**Example:**
```json
{
  "project_type": "residential",
  "building_height": 25.0,
  "total_surface": 1200.0,
  "num_floors": 8,
  "location": "Nice"
}
```

---

### 2. calculate3DVolume

Calculates 3D volume of structures.

**Parameters:**
```python
{
  "length": float,           # in meters
  "width": float,            # in meters
  "height": float,           # in meters
  "shape": str               # rectangular, cylindrical, pyramidal
}
```

**Returns:**
```json
{
  "dimensions": {...},
  "calculations": {
    "volume_m3": float,
    "surface_base_m2": float,
    "surface_totale_m2": float
  },
  "material_estimates": {
    "concrete_m3": float,
    "steel_kg": float
  }
}
```

---

### 3. suggestMaterialsOptimization

Suggests optimized materials based on criteria.

**Parameters:**
```python
{
  "structure_type": str,            # walls, roofing, foundations, facade
  "budget_level": str,              # economic, standard, premium
  "environmental_priority": bool,   # prioritize eco-friendly
  "climate": str                    # temperate, mediterranean, mountain, tropical
}
```

**Returns:**
```json
{
  "recommended_material": str,
  "structure_type": str,
  "budget_level": str,
  "environmental": bool,
  "climate_adaptation": str,
  "energy_performance_class": str,
  "additional_tips": [...]
}
```

---

### 4. calculateStructuralLoad

Calculates structural loads for dimensioning.

**Parameters:**
```python
{
  "floor_type": str,         # concrete, wood, mixed
  "surface_m2": float,       # floor surface in m²
  "usage": str,              # residential, office, storage, commercial, parking
  "num_supports": int        # number of support points
}
```

**Returns:**
```json
{
  "input_parameters": {...},
  "load_calculations": {
    "dead_load_kN_m2": float,
    "exploitation_load_kN_m2": float,
    "total_load_kN_m2": float,
    "total_load_kN": float,
    "load_per_support_kN": float
  },
  "recommendations": {...}
}
```

---

### 5. generateTechnicalReport

Generates a formatted technical report.

**Parameters:**
```python
{
  "project_name": str,
  "analysis_data": dict      # analysis results
}
```

**Returns:** String with formatted technical report

---

## 💰 Agent Cost Estimator Tools

### 1. estimateMaterialCost

Estimates material costs with market variability.

**Parameters:**
```python
{
  "materials": [
    {
      "name": str,           # concrete, steel, brick, etc.
      "quantity": float,
      "unit": str            # optional, auto-detected
    }
  ],
  "include_transport": bool,
  "project_location": str    # urban, suburban, rural
}
```

**Returns:**
```json
{
  "estimation_date": str,
  "project_location": str,
  "material_details": [...],
  "cost_summary": {
    "subtotal_materials_euro": float,
    "contingency_12_percent_euro": float,
    "estimated_total_euro": float
  },
  "warnings": [...],
  "notes": [...]
}
```

**Example:**
```json
{
  "materials": [
    {"name": "concrete", "quantity": 50},
    {"name": "steel", "quantity": 2000},
    {"name": "brick", "quantity": 5000}
  ],
  "include_transport": true,
  "project_location": "urban"
}
```

---

### 2. calculateLaborHours

Calculates labor hours and associated costs.

**Parameters:**
```python
{
  "tasks": [
    {
      "task_name": str,
      "trade": str,          # mason, carpenter, electrician, plumber, etc.
      "estimated_hours": float
    }
  ],
  "team_composition": {
    "trade": int             # number of workers per trade
  }
}
```

**Returns:**
```json
{
  "task_breakdown": [...],
  "summary_by_trade": [...],
  "cost_summary": {
    "base_labor_cost_euro": float,
    "social_charges_45_percent_euro": float,
    "site_management_8_percent_euro": float,
    "total_labor_cost_euro": float
  },
  "project_timeline": {
    "estimated_duration_days": float,
    "estimated_duration_weeks": float,
    "duration_by_trade": [...]
  },
  "notes": [...]
}
```

---

### 3. trackBudgetDeviation

Tracks budget deviations and projects final cost.

**Parameters:**
```python
{
  "initial_budget": float,            # in euros
  "spent_to_date": float,            # in euros
  "work_completion_percent": float,  # 0-100
  "remaining_costs_estimate": float  # in euros
}
```

**Returns:**
```json
{
  "budget_analysis": {
    "initial_budget_euro": float,
    "spent_to_date_euro": float,
    "work_completion_percent": float,
    "expected_cost_at_stage_euro": float,
    "current_deviation_euro": float,
    "current_deviation_percent": float
  },
  "projection": {
    "remaining_costs_estimate_euro": float,
    "projected_final_cost_euro": float,
    "budget_deviation_euro": float,
    "deviation_percent": float,
    "status": str,
    "alert_level": str
  },
  "recommendations": [...],
  "key_indicators": {...}
}
```

---

### 4. generateCostBreakdown

Generates a detailed quote.

**Parameters:**
```python
{
  "project_name": str,
  "material_costs": {
    "category": float
  },
  "labor_costs": {
    "category": float
  },
  "other_costs": {
    "category": float
  }
}
```

**Returns:**
```json
{
  "project_info": {...},
  "material_costs": {...},
  "labor_costs": {...},
  "other_costs": {...},
  "totals": {
    "subtotal_ht_euro": float,
    "tva_20_percent_euro": float,
    "total_ttc_euro": float
  },
  "payment_terms": {...},
  "validity": str,
  "notes": [...]
}
```

---

### 5. comparePriceAlternatives

Compares different price alternatives.

**Parameters:**
```python
{
  "base_option": {
    "name": str,
    "description": str,
    "total_cost": float
  },
  "alternative_options": [
    {
      "name": str,
      "description": str,
      "total_cost": float,
      "pros": [...],
      "cons": [...]
    }
  ]
}
```

**Returns:**
```json
{
  "base_option": {...},
  "alternatives": [...],
  "best_savings_option": str,
  "max_potential_savings_euro": float
}
```

---

## 📅 Agent Planning Tools

### 1. createGanttChart

Creates a Gantt chart for project planning.

**Parameters:**
```python
{
  "project_name": str,
  "start_date": str,         # YYYY-MM-DD
  "tasks": [
    {
      "name": str,
      "duration_days": int,
      "dependencies": [...],
      "trade": str
    }
  ]
}
```

**Returns:**
```json
{
  "project_info": {
    "name": str,
    "start_date": str,
    "end_date": str,
    "total_duration_days": int,
    "total_duration_weeks": float
  },
  "gantt_chart": [...],
  "notes": [...]
}
```

**Example:**
```json
{
  "project_name": "House Construction",
  "start_date": "2025-04-01",
  "tasks": [
    {"name": "Foundations", "duration_days": 15, "dependencies": [], "trade": "mason"},
    {"name": "Walls", "duration_days": 20, "dependencies": ["Foundations"], "trade": "mason"},
    {"name": "Roofing", "duration_days": 8, "dependencies": ["Walls"], "trade": "roofer"}
  ]
}
```

---

### 2. detectCriticalPath

Identifies the critical path (sequence determining minimum duration).

**Parameters:**
```python
{
  "tasks": [
    {
      "name": str,
      "duration_days": int,
      "dependencies": [...]
    }
  ]
}
```

**Returns:**
```json
{
  "project_duration_days": int,
  "critical_path": [...],
  "critical_tasks_count": int,
  "task_analysis": [
    {
      "task_name": str,
      "duration_days": int,
      "earliest_start": int,
      "earliest_finish": int,
      "latest_start": int,
      "latest_finish": int,
      "slack_days": int,
      "is_critical": bool,
      "priority": str
    }
  ],
  "recommendations": [...]
}
```

---

### 3. optimizeResourceAllocation

Optimizes resource allocation to avoid over/under-utilization.

**Parameters:**
```python
{
  "tasks": [
    {
      "name": str,
      "duration_days": int,
      "dependencies": [...],
      "required_resources": {
        "trade": int        # number of workers needed
      }
    }
  ],
  "available_resources": {
    "trade": int            # max available workers
  },
  "start_date": str         # YYYY-MM-DD
}
```

**Returns:**
```json
{
  "summary": {...},
  "available_resources": {...},
  "average_utilization_percent": {...},
  "resource_conflicts": [...],
  "recommendations": [...],
  "optimization_tips": [...]
}
```

---

### 4. simulateScenario

Simulates impact of different scenarios on planning.

**Parameters:**
```python
{
  "base_duration_days": int,
  "scenario_type": str,        # weather, delivery_delay, labor, optimistic, accident, client_change
  "impact_percent": int        # positive=delay, negative=advance
}
```

**Returns:**
```json
{
  "scenario": {
    "type": str,
    "description": str,
    "probability_percent": float,
    "impact_percent": int
  },
  "duration_impact": {...},
  "financial_impact": {...},
  "risk_level": str,
  "mitigation_measures": [...],
  "recommendation": str
}
```

---

### 5. generateMilestoneReport

Generates a milestone report.

**Parameters:**
```python
{
  "project_name": str,
  "milestones": [
    {
      "name": str,
      "planned_date": str,     # YYYY-MM-DD
      "actual_date": str,      # YYYY-MM-DD or null
      "status": str            # completed, in_progress, pending
    }
  ],
  "current_date": str          # YYYY-MM-DD
}
```

**Returns:**
```json
{
  "project_name": str,
  "report_date": str,
  "statistics": {
    "total_milestones": int,
    "completed": int,
    "in_progress": int,
    "pending": int,
    "completion_rate_percent": float,
    "average_delay_days": float
  },
  "milestones": [...],
  "delays": [...],
  "upcoming_milestones": [...],
  "alerts": [...]
}
```

---

## 🔗 A2A Protocol Endpoints

All agents expose standard A2A endpoints:

### GET /.well-known/agent.json
Returns agent card with capabilities

### POST /
Main endpoint for A2A requests. Accepts:
- `tasks/send` - Non-streaming task
- `tasks/sendSubscribe` - Streaming task (SSE)
- `tasks/get` - Get task status
- `tasks/cancel` - Cancel task

---

## 🌐 Host Agent API

The Host Agent Orchestrator exposes:

### POST /conversation/create
Create a new conversation

### POST /message/send
Send a message to agents

### POST /agent/register
Register a new A2A agent

### POST /agent/list
List all registered agents

---

## 💡 Usage Tips

1. **Always include units** in parameters for clarity
2. **Use realistic values** for better estimations
3. **Chain tools** for complex workflows
4. **Check warnings** in responses for important info
5. **Use contingency margins** for budget estimates

---

For implementation details, see the source code in `backend/Agent*/mcpserver/*.py`
