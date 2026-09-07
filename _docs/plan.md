# Vehicle Manufacturing Task Management System — Final Scope

## Overview
A tool for managing the full manufacturing workflow of heavy industrial vehicles, designed for use by managers, supervisors, and workers.

## Core Features

### Users
- Managers, supervisors, and workers

### Vehicle Type
- Heavy industrial vehicles

### Project Creation
- Manager creates a project, then assigns vehicles and tasks to it

### Manufacturing Stages
- Design → Fabrication → Assembly → Testing → Delivery

### Task Creation & Assignment
- Manager creates tasks
- Supervisor assigns tasks to workers

### Completion Flow
- Worker submits a completed task
- Supervisor approves or rejects it, with a reason required on rejection

### Rejected Tasks
- Returns to the previous manufacturing stage (not just back to the same worker)

### Parts & Materials
- Full tracking of parts, inventory/stock, and suppliers

### Inventory Rule
- A task cannot start until all required parts/materials are available

### Manager Dashboard
- Overall project progress
- Vehicle-by-vehicle progress
- Inventory, costs, suppliers, and delays

### Worker Access
- Assigned tasks only, plus relevant vehicle/stage information

### Costs
- Parts + labor + other manufacturing costs tracked

### Audit Log
- Complete audit log of all changes

## Core Workflow

```
Manager creates project
      │
      ▼
Adds heavy industrial vehicles
      │
      ▼
Creates manufacturing tasks
      │
      ▼
Design → Fabrication → Assembly → Testing → Delivery
      │
      ▼
For each stage:
      │
      ▼
Supervisor assigns worker
      │
      ▼
Worker performs task
      │
      ▼
Worker submits task
      │
      ▼
Supervisor reviews
      │
      ├── Approved → Continue to next stage
      │
      └── Rejected (with reason) → Back to previous manufacturing stage
```

## Core Business Rule
A task cannot start until all required parts/materials are available.

## Summary
This scope defines a full-workflow manufacturing task management system for heavy industrial vehicles — stage-based production, role-separated task creation/assignment, supervisor approval with stage-level rejection handling, full parts/inventory/supplier tracking with a hard availability gate, cost tracking, and a complete audit log.
