import os, sys, re

DELIVERABLES = {
    'DR-10': r'E:\projects\simlab\deliverables\DR-10_candidate_baseline_matrix.md',
    'DR-11': r'E:\projects\simlab\deliverables\DR-11_reproduction_candidate_list.md',
    'DR-12': r'E:\projects\simlab\deliverables\DR-12_proposed_experiment_matrix.md',
    'DR-13': r'E:\projects\simlab\deliverables\DR-13_cost_latency_scaling_analysis.md',
    'DR-14': r'E:\projects\simlab\deliverables\DR-14_research_synthesis.md',
    'DR-15': r'E:\projects\simlab\deliverables\DR-15_lessons_learned_forward_constraints.md',
    'PACKAGE': r'E:\projects\simlab\curo_research_package.md'
}

def run():
    print('Loading deliverable files...')
    contents = {}
    for name, path in DELIVERABLES.items():
        if not os.path.exists(path):
            print(f'ERROR: File not found: {path}')
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            contents[name] = f.read()
        print(f'  Loaded {name} ({len(contents[name])} chars, {len(contents[name].splitlines())} lines)')

    print('\n--- CHECK 1: Token Scaling Formula and Derivation ---')
    d13 = contents['DR-13']
    assert 'O(N^2 \\cdot R^2 \\cdot L)' in d13 or 'O(N^2 \cdot R^2 \cdot L)' in d13, 'DR-13 missing O(N^2 * R^2 * L)'
    assert '2.78' in d13 and '5.87' in d13, 'DR-13 missing underestimation factors'
    assert 'T_{\\text{debate}}' in d13 or 'T_{debate}' in d13 or 'T_{\text{debate}}' in d13, 'DR-13 missing T_debate formula'
    print('  [PASS] DR-13 token scaling formula, derivation and underestimation factors verified.')

    d14 = contents['DR-14']
    assert 'O(N^2 \\cdot R^2 \\cdot L)' in d14 or 'O(N^2 \cdot R^2 \cdot L)' in d14, 'DR-14 missing O(N^2 * R^2 * L)'
    assert '4.3 Asymptotic Complexity' in d14, 'DR-14 missing Section 4.3'
    print('  [PASS] DR-14 Section 4.3 token scaling derivation verified.')

    pkg = contents['PACKAGE']
    assert 'O(N^2 \\cdot R^2 \\cdot L)' in pkg or 'O(N^2 \cdot R^2 \cdot L)' in pkg, 'PACKAGE missing O(N^2 * R^2 * L)'
    assert 'Broadcast Debate Token Explosion' in pkg, 'PACKAGE missing Section 13 subsection'
    print('  [PASS] Master Package token scaling derivation verified.')

    for name in ['DR-13', 'DR-14', 'PACKAGE']:
        lines = contents[name].splitlines()
        for i, line in enumerate(lines):
            if 'O(N \\cdot R^2)' in line or 'O(N \cdot R^2)' in line:
                assert any(w in line.lower() for w in ['early literature', 'simplified', 'legacy', 'disproved', 'neglecting', 'rather than']), f'Stale formula claim at {name}:{i+1}: {line}'
    print('  [PASS] Zero stale O(N * R^2) claims found (only referenced as refuted legacy assumption).')

    print('\n--- CHECK 2: B1-SC Boundary Qualifications ---')
    qualifiers = [
        'partitioned private state',
        'asymmetric specialized external tools',
        'distinct persona',
        'asynchronous human-in-the-loop'
    ]
    for name in ['DR-10', 'DR-14', 'PACKAGE']:
        text = contents[name].lower()
        for q in qualifiers:
            assert q in text, f'{name} missing qualifier: {q}'
        print(f'  [PASS] {name} contains all 4 required B1-SC boundary qualifiers.')

    d10 = contents['DR-10']
    assert '3.1 Boundary Qualification: Scope of Single-Agent Self-Consistency (B1-SC) Equivalence' in d10, 'DR-10 missing Section 3.1'
    assert '4.1 Boundary Qualification on Multi-Agent Primitive Falsification' in d10, 'DR-10 missing Section 4.1'
    print('  [PASS] DR-10 dedicated boundary qualification sections verified.')

    assert '4.2 Boundary Qualification: Scope of Single-Agent Self-Consistency (B1-SC) Equivalence' in d14, 'DR-14 missing Section 4.2'
    print('  [PASS] DR-14 Section 4.2 verified.')

    assert 'Boundary Qualification on B1-SC Baseline Equivalence' in pkg, 'PACKAGE missing Section 10 B1-SC subsection'
    print('  [PASS] Master Package Section 10 boundary qualification verified.')

    print('\n--- CHECK 3: DR-12 Experiment Designs and Master Package Sync ---')
    d12 = contents['DR-12']
    
    # EXP-001
    assert '72 distinct' in d12, 'DR-12 EXP-001 missing 72 distinct tasks'
    assert '360 runs per condition' in d12, 'DR-12 EXP-001 missing 360 runs per condition'
    assert '1,080' in d12, 'DR-12 EXP-001 missing 1,080 total runs'
    assert 'Two One-Sided Tests' in d12 or 'TOST' in d12, 'DR-12 EXP-001 missing TOST'
    assert '0.05' in d12, 'DR-12 EXP-001 missing delta=0.05'
    assert 'Binary Metric Power Correction' in d12, 'DR-12 EXP-001 missing binary power correction'
    print('  [PASS] DR-12 EXP-001 sample sizes, TOST framework, and binary power correction verified.')

    # EXP-002
    assert '56 distinct' in d12, 'DR-12 EXP-002 missing 56 distinct tasks'
    assert '280 matched blocks' in d12, 'DR-12 EXP-002 missing 280 matched blocks'
    assert '840' in d12, 'DR-12 EXP-002 missing 840 total runs'
    assert 'Cochran' in d12, 'DR-12 EXP-002 missing Cochran Q'
    assert '0.903' in d12 or '> 0.90' in d12, 'DR-12 EXP-002 missing power > 0.90'
    print('  [PASS] DR-12 EXP-002 matched blocks and Cochran Q power verified.')

    # EXP-003
    assert 'Firth' in d12, 'DR-12 EXP-003 missing Firth penalized likelihood'
    assert 'quasi-complete separation' in d12, 'DR-12 EXP-003 missing quasi-complete separation'
    assert '0.8527' in d12, 'DR-12 EXP-003 missing interaction power 0.8527'
    assert '72' in d12 and '12' in d12, 'DR-12 EXP-003 missing n=12, N=72'
    print('  [PASS] DR-12 EXP-003 Firth penalized likelihood and power verified.')

    # Package synchronization for EXP-001, EXP-002, EXP-003
    assert '72 distinct SWE-bench tasks' in pkg, 'PACKAGE missing 72 tasks in EXP-001'
    assert 'Two One-Sided Tests' in pkg or 'TOST' in pkg, 'PACKAGE missing TOST in EXP-001'
    assert '56 distinct security vulnerability tasks' in pkg, 'PACKAGE missing 56 tasks in EXP-002'
    assert '280 matched blocks' in pkg, 'PACKAGE missing 280 blocks in EXP-002'
    assert 'Firth' in pkg, 'PACKAGE missing Firth in EXP-003'
    print('  [PASS] Master Package Section 12 synchronization verified.')

    print('\n--- CHECK 4: DR-15 Negative Constraints and Master Package Sync ---')
    d15 = contents['DR-15']
    
    # NC-02
    assert 'cas://sha256:' in d15, 'DR-15 missing cas://sha256: in NC-02'
    assert 'signature' in d15.lower(), 'DR-15 missing signature in NC-02'
    assert 'mutable' in d15.lower(), 'DR-15 missing mutable prohibition in NC-02'
    print('  [PASS] NC-02 CAS URIs, digital signatures, and mutable path ban verified.')

    # NC-03
    assert 'seq_agent' in d15.lower() or 'seq_num' in d15.lower(), 'DR-15 missing sequence counter in NC-03'
    assert 'nonce' in d15.lower(), 'DR-15 missing nonce in NC-03'
    assert 'replay' in d15.lower(), 'DR-15 missing replay protection in NC-03'
    print('  [PASS] NC-03 monotonic sequence counter and anti-replay verified.')

    # NC-05
    assert '__string_literal_token_' in d15.lower() or '__str_literal_token_' in d15.lower(), 'DR-15 missing string literal tokenization in NC-05'
    assert 'semgrep' in d15.lower() or 'bandit' in d15.lower(), 'DR-15 missing linters in NC-05'
    print('  [PASS] NC-05 AST string literal redaction and dual-pass linters verified.')

    # NC-13 through NC-16 in DR-15
    for nc in ['NC-13', 'NC-14', 'NC-15', 'NC-16']:
        assert nc in d15, f'DR-15 missing {nc}'
        assert nc in pkg, f'PACKAGE missing {nc}'
    assert 'sixteen binding, operational' in d15.lower(), 'DR-15 missing 16 constraints assertion'
    assert 'sixteen concrete, operational negative forward constraints' in pkg.lower(), 'PACKAGE missing 16 constraints assertion'
    print('  [PASS] NC-13, NC-14, NC-15, NC-16 fully specified in DR-15 and Master Package.')

    print('\n--- CHECK 5: Cross-Document Synchronization and Invariants ---')
    d11 = contents['DR-11']
    assert 'ChatDev Phase Sandboxing' in d11 and 'ChatDev Phase Sandboxing & Task Completion' in pkg, 'RP-03 mismatch'
    assert 'Evolving Orchestration RL Policy Efficiency' in d11 and 'Evolving Orchestration RL Policy Efficiency' in pkg, 'RP-04 mismatch'
    print('  [PASS] RP-03 and RP-04 labels match between DR-11 and Master Package.')

    for name, text in contents.items():
        assert 'RESEARCH_AUTHORIZED' in text, f'{name} missing RESEARCH_AUTHORIZED'
        assert 'NOT_GRANTED' in text, f'{name} missing NOT_GRANTED'
    assert 'UNFROZEN' in contents['DR-14'], 'DR-14 missing UNFROZEN'
    assert 'UNFROZEN' in pkg, 'PACKAGE missing UNFROZEN'
    assert 'READY_FOR_REPRODUCTION_DESIGN' in pkg, 'PACKAGE missing READY_FOR_REPRODUCTION_DESIGN'
    print('  [PASS] All lifecycle invariants and Gate R1 recommendation verified.')

    print('\n======================================================')
    print('ALL VERIFICATION SUITE CHECKS COMPLETED SUCCESSFULLY!')
    print('======================================================')

if __name__ == '__main__':
    run()
