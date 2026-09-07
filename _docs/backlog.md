# Vehicle Manufacturing Task Management — Django Backlog

## Epic 1 — Project & User Setup

- [x] **BE-01** Define custom user model with roles: `manager`, `supervisor`, `worker`
- [x] **BE-02** Configure role-based permissions and Django groups
- [x] **BE-03** Implement login / logout with session auth
- [x] **BE-04** Restrict views by role using decorators or mixins

---

## Epic 2 — Project Management

- [ ] **BE-05** Create `Project` model (name, description, status, created_by, created_at)
- [ ] **BE-06** Manager CRUD views for projects
- [ ] **BE-07** List view showing all projects with status summary

---

## Epic 3 — Vehicle Management

- [ ] **BE-08** Create `Vehicle` model (project FK, type, serial number, current stage)
- [ ] **BE-09** Manager views to add/edit/remove vehicles on a project
- [ ] **BE-10** Vehicle detail page showing stage progress

---

## Epic 4 — Manufacturing Stages & Tasks

- [ ] **BE-11** Define stage choices: `Design → Fabrication → Assembly → Testing → Delivery`
- [ ] **BE-12** Create `Task` model (vehicle FK, stage, title, description, status, assigned_to, created_by)
- [ ] **BE-13** Manager view to create tasks per vehicle/stage
- [ ] **BE-14** Supervisor view to assign tasks to workers
- [ ] **BE-15** Worker view showing only their assigned tasks

---

## Epic 5 — Task Completion Flow

- [ ] **BE-16** Worker action: submit task for review (status → `pending_review`)
- [ ] **BE-17** Supervisor action: approve task (status → `approved`, advance vehicle stage)
- [ ] **BE-18** Supervisor action: reject task with required reason (status → `rejected`, revert vehicle to previous stage)
- [ ] **BE-19** Display rejection reason to the worker on their task view

---

## Epic 6 — Parts, Inventory & Suppliers

- [ ] **BE-20** Create `Supplier` model (name, contact info)
- [ ] **BE-21** Create `Part` model (name, SKU, unit, supplier FK, unit cost)
- [ ] **BE-22** Create `Inventory` model (part FK, quantity in stock)
- [ ] **BE-23** Manager views for CRUD on suppliers, parts, and inventory levels
- [ ] **BE-24** Implement inventory gate: block task from starting if required parts are unavailable
- [ ] **BE-25** Create `TaskPart` join model linking tasks to required parts with quantities
- [ ] **BE-26** Deduct inventory when a task is approved/started

---

## Epic 7 — Cost Tracking

- [ ] **BE-27** Create `CostEntry` model (project FK, category: `parts/labor/other`, amount, description, recorded_by)
- [ ] **BE-28** Auto-record part costs when inventory is consumed
- [ ] **BE-29** Manual labor and other cost entry for managers
- [ ] **BE-30** Per-project cost summary view

---

## Epic 8 — Manager Dashboard

- [ ] **BE-31** Dashboard view: overall project progress (tasks completed / total)
- [ ] **BE-32** Vehicle-by-vehicle progress breakdown per project
- [ ] **BE-33** Inventory status panel (stock levels, low-stock alerts)
- [ ] **BE-34** Cost summary panel (parts, labor, other, total)
- [ ] **BE-35** Delays panel: tasks blocked by inventory shortage or pending review

---

## Epic 9 — Audit Log

- [ ] **BE-36** Create `AuditLog` model (user, action, target model, target id, timestamp, detail)
- [ ] **BE-37** Hook audit logging to all key actions (task create/assign/submit/approve/reject, inventory change, cost entry)
- [ ] **BE-38** Audit log list view for managers with filters (user, action, date range)

---

## Epic 10 — Admin & Polish

- [ ] **BE-39** Register all models in Django Admin with useful list displays and filters
- [ ] **BE-40** Add basic pagination to all list views
- [ ] **BE-41** Form validation and user-facing error messages throughout
- [ ] **BE-42** Write model-level unit tests for core business rules (inventory gate, stage progression, rejection flow)
