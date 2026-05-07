# Orcstrate Project Roadmap (Modular Development Plan)

## Project Goal

Build a Linux-focused GTK application that manages and executes command workflows, while demonstrating core Data Structures & Algorithms concepts.

---

# CURRENT STATE (What’s Done)

## Core Engine

* [x] Command class (data model)
* [x] CommandRunner class (execution engine)
* [x] Internal command execution (blocking)
* [x] External command execution (new terminal)
* [x] Environment sanitization (Snap issues handled)

## Data Structures

* [x] Queue (deque) for execution order

---

# IN PROGRESS

## Execution System

* [x] Threaded execution (to prevent GTK freeze)
* [ ] Process tracking (start/stop status)
* [ ] External process lifecycle awareness (optional)

---

# DATA STRUCTURES (CORE REQUIREMENTS)

## 1. Dequeue (DONE, refine later)

* [x] FIFO execution using deque
* [x] Ability to:
  * [x] Add while running
  * [x] Pause/resume queue
  * [x] Inspect queue state (for UI)

* [ ] Undo last command
* [ ] Redo (optional second stack)

---

## 3. Hash Table (REGISTRY) - HIGH PRIORITY

Implement command/project lookup:

* [ ] CommandRegistry (name → Command)
* [ ] ProjectRegistry (name → list of commands)
* [ ] Load project into queue

### Outcome:

* Save/load workflows
* Instant lookup (O(1))

---

## 4. Searching

* [x] Search commands by name
* [ ] Filter command list in UI

### Optional:

* [ ] Compare linear vs binary search

---

## 5. Sorting (OPTIONAL)

* [ ] Sort commands:

  * by name
  * by type (internal/external)
* [ ] Optional: implement custom sort (merge/quick sort)

---

## 6. AVL Tree (OPTIONAL, BONUS)

Only if time allows:

* [ ] Store commands in AVL tree (sorted structure)
* [ ] Use for fast ordered lookup

---

# GUI (GTK) DEVELOPMENT

## Phase 1: Basic UI

* [x] Main window
* [ ] Dequeue window
* [x] Command list display
* [x] Add/remove command buttons
* [x] Checkbox: external execution
* [x] Checkbox: keep open

---

## Phase 2: Interaction

* [ ] Run button → triggers runner
* [ ] Display execution status
* [ ] Show queue state

---

## Phase 3: Advanced UI

* [ ] Undo button
* [x] Search bar
* [ ] Project selector (hash table)

---

# INTEGRATION TASKS

## Runner ↔ UI

* [ ] Implement callbacks:

  * on_command_start
  * on_command_finish
  * on_error
* [ ] Use threading for execution
* [ ] Ensure GTK-safe updates (GLib.idle_add later)

---

# TESTING

* [x] Test sequential execution
* [x] Test parallel execution
* [x] Test queue behavior
* [ ] Test undo system
* [x] Test registry lookup

---

# PROJECT FEATURES (FINAL GOAL)

## Minimum Viable Product

* Command queue execution
* External/internal toggle
* Basic GUI
* Queue + Hash Table + Stack implemented

---

## Stretch Features

* Save/load workflows
* Search + sort
* Multiple projects
* Process monitoring
* AVL tree usage

---

# REPORT / ACADEMIC MAPPING

| Concept    | Where Used                    |
| ---------- | ----------------------------- |
| Queue      | Command execution             |
| Stack      | Undo/redo system              |
| Hash Table | Command/project lookup        |
| Searching  | Command filtering             |
| Sorting    | Command organization          |
| AVL Tree   | (Optional) structured storage |

---