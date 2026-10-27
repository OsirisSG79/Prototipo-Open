#!/usr/bin/env bash
# ==============================================================================
# OpenBreak — Fast Rigorous Logic & Integration Test Runner (V8.1.5)
# Executes all real logic, adversarial and integration suites directly with
# detailed timing, clear exit codes, and zero dependency on presence assertions.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "    OPEN BREAK OS — FAST LOGIC & INTEGRATION PIPELINE (V8.1.5)        "
echo "======================================================================"
echo "Started at: $(date -u)"
START_TIME=$(date +%s%N)

FAILURES=0

run_test() {
  local suite_name="$1"
  shift
  local t_start=$(date +%s%N)
  echo -n "▶ [TEST] $suite_name ... "
  if "$@" > /tmp/test_out.log 2>&1; then
    local t_end=$(date +%s%N)
    local elapsed=$(( (t_end - t_start) / 1000000 ))
    echo "PASS (${elapsed} ms)"
  else
    local t_end=$(date +%s%N)
    local elapsed=$(( (t_end - t_start) / 1000000 ))
    echo "FAIL (${elapsed} ms)"
    cat /tmp/test_out.log
    FAILURES=$((FAILURES + 1))
  fi
}

# 1. Core Build
run_test "Build Site Bundle" python3 build_site.py

# 2. AUD-013 Acceptance Suite (9 Invariants)
run_test "AUD-013 Full Acceptance Criteria" node tests/test_audit_013_acceptance.js

# 3. AUD-013 Adversarial P0 Scenarios
run_test "AUD-013 Adversarial P0 Scenarios" node tests/test_audit_013_adversarial_p0.js

# 4. AUD-012 Adversarial P0 Scenarios
run_test "AUD-012 Adversarial P0 Scenarios" node tests/test_audit_012_adversarial_p0.js

# 5. AUD-010 Mathematical Integrity
run_test "AUD-010 Mathematical Integrity" python3 -m unittest tests/test_audit_010_p0_p1_integrity.py

# 6. AUD-090 Three-Student Isolation
run_test "AUD-090 Three-Student Isolation" python3 tests/test_audit_090_three_student_isolation.py

# 7. AUD-009 Adversarial Security
run_test "AUD-009 Adversarial Security" node tests/test_audit_009_adversarial.js

# 8. AUD-011 Extended Resilience & Burst
run_test "AUD-011 Extended Resilience" node tests/test_audit_011_resilience.js

# 9. AUD-015 End-to-End User Journeys
run_test "AUD-015 User Journeys Simulation" node tests/test_audit_015_e2e_user_journeys.js

# 10. AUD-094 FSM State Machine Invariance
run_test "AUD-094 FSM Transition Invariance" python3 tests/test_audit_094_fsm_transition_invariance.py

# 11. AUD-096 Concurrency Storm & Race Conditions
run_test "AUD-096 Concurrency Storm Invariance" python3 tests/test_audit_096_concurrency_storm_invariance.py

# 12. AUD-064 Waitlist Promotion Debit
run_test "AUD-064 Waitlist Promotion Debit" python3 tests/test_audit_064_waitlist_promotion_debit.py

# 13. AUD-065 Multi-Student Independent Cancellation
run_test "AUD-065 Multi-Student Cancellation" python3 tests/test_audit_065_multistudent_cancellation.py

# 14. AUD-068 Multi-Queue Cascading Waitlist
run_test "AUD-068 Multi-Queue Waitlist Cascade" python3 tests/test_audit_068_multiqueue_waitlist_cascade.py

# 15. AUD-069 Multi-Student Concurrency Stress
run_test "AUD-069 Concurrency Stress Burst" python3 tests/test_audit_069_concurrency_stress_burst.py

# 16. AUD-073 Microbenchmark GC Invariance
run_test "AUD-073 Microbenchmark Stress" python3 tests/test_audit_073_microbenchmark_gc_invariance.py

# 17. AUD-099 Microtask Heap Retention
run_test "AUD-099 Heap Retention & Teardown" python3 tests/test_audit_099_heap_retention_event_teardown.py

# 18. Store Concurrency Verification
run_test "DemoStore Concurrency & Consistency" node tests/test_store_concurrency.js

# 19. Waitlist FIFO Verification
run_test "Waitlist FIFO Order" node tests/test_waitlist_fifo.js

# 20. Documentation Governance & Version Integrity
run_test "AUD-016 Documentation Governance" python3 tests/test_audit_016_documentation_governance.py

# 21. DOM Behavioral & Visual Invariants (AUD-014 P1-03)
run_test "AUD-014 DOM Behavioral & Visual" node tests/test_audit_014_dom_behavioral.js

# 22. AUD-014 / V8.1.5 Adversarial Multi-Student Wallet Hardening
run_test "AUD-014 Adversarial Multi-Wallet" node tests/test_audit_014_adversarial_p0.js

# 23. AUD-015 Mandatory Acceptance Certification
run_test "AUD-015 Acceptance Certification" node tests/test_audit_015_acceptance_certification.js

# 24. AUD-017 Visual & Smartphone Fidelity
run_test "AUD-017 Visual & Smartphone Fidelity" node tests/test_audit_017_visual_and_schedule_fidelity.js

# 25. AUD-018 Scroll Choreography & Motion
run_test "AUD-018 Scroll Choreography & Motion" node tests/test_audit_018_scroll_choreography_and_motion.js

END_TIME=$(date +%s%N)
TOTAL_ELAPSED=$(( (END_TIME - START_TIME) / 1000000 ))

echo "======================================================================"
if [ $FAILURES -eq 0 ]; then
  echo "✔ ALL CRITICAL LOGIC, BEHAVIORAL & INTEGRATION SUITES PASSED (100%)"
  echo "Total Execution Duration: ${TOTAL_ELAPSED} ms ($(( TOTAL_ELAPSED / 1000 )) seconds)"
  echo "======================================================================"
  exit 0
else
  echo "✖ $FAILURES SUITES FAILED"
  echo "======================================================================"
  exit 1
fi
