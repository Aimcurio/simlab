# AS-08: SOP Stress Plan
**Experiment ID**: `EXP-ST-03-SOP`  
**Target Primitive**: `PR-ORG-02`  
**Lifecycle State**: `PHASE_4_DESIGN`  

---

## 1. Primary Research Question
Under what task conditions and team sizes does rigid assembly-line SOP structure degrade performance, induce deadlock, or fail compared to dynamic or unstructured interaction?

---

## 2. Progressive Stress Dimensions

### A. Task Ambiguity & Exploratory Stress:
1. **Clear Specification (Baseline)**: Deterministic I/O requirements with pre-written test assertions.
2. **Ambiguous Requirements**: Prompts with underspecified edge cases and missing constraints.
3. **Exploratory Open-Ended Tasks**: Creative design or open-ended simulation tasks without ground-truth answers.
4. **Mid-Stream Requirement Shifts**: Requirements mutated dynamically after Phase 2 (Coding) has commenced.
5. **Upstream Defect Injection**: Injecting a subtle architectural flaw in Phase 1 (Design) to test whether downstream stages can trigger backward phase rollback or become deadlocked.

### B. Team Size Scaling:
- Team size varied across $K \in \{1, 2, 3, 5, 10\}$ agents within the SOP pipeline.

---

## 3. Dependent Variables & Failure Boundaries
- **Task Completion Rate**: Percentage of tasks successfully terminating with valid code artifacts.
- **Deadlock Frequency**: Number of infinite review cycles between Programmer and Reviewer exceeding turn limits.
- **Rollback Overhead**: Token cost incurred when correcting upstream phase errors.
- **Pre-Registered Failure Boundary**: SOP structure is declared maladaptive for a task class if deadlock rate exceeds $15\%$ or task completion drops $> 20\%$ below unstructured baseline.
