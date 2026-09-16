import numpy as np
import scipy.stats as stats

print("=" * 80)
print("DEBATE SYCOPHANCY & FALSE CONSENSUS DYNAMICS VS B1-SC")
print("=" * 80)

# Compare 3-agent debate final accuracy vs B1-SC (K=9 token-matched or K=6 call-matched)
# Let p0 be the single-agent initial accuracy on a task.

def debate_accuracy(p0, p_sycophancy=0.50, p_truth_persuade=0.30):
    # Round 1 outcomes:
    # 3 correct:
    p_3c = p0 ** 3
    # 2 correct, 1 wrong:
    p_2c = 3 * (p0 ** 2) * (1 - p0)
    # 1 correct, 2 wrong:
    p_1c = 3 * p0 * ((1 - p0) ** 2)
    # 0 correct:
    p_0c = (1 - p0) ** 3
    
    # In 2 correct, 1 wrong: truth wins unless 2 correct agents capitulate to 1 wrong (rare, say 5%)
    p_win_from_2c = 1.0 - 0.05
    # In 1 correct, 2 wrong:
    # 1 correct agent could persuade the 2 wrong (p_truth_persuade)
    # OR 1 correct agent capitulates to the 2 wrong (p_sycophancy)
    # If neither, vote remains 1-2 (wrong).
    p_win_from_1c = p_truth_persuade
    
    final_acc = p_3c * 1.0 + p_2c * p_win_from_2c + p_1c * p_win_from_1c
    false_consensus_rate = p_1c * p_sycophancy # agent abandoned correct initial answer
    return final_acc, false_consensus_rate

def b1sc_accuracy(p0, K):
    m = (K // 2) + 1
    return 1.0 - stats.binom.cdf(m - 1, K, p0)

print(f"{'p0':<8} | {'B1-SC (K=6)':<14} | {'B1-SC (K=9)':<14} | {'Debate (Syc=0.5)':<18} | {'Debate False Consensus':<24} | {'Debate vs K=9 Delta':<20}")
print("-" * 105)

for p0 in [0.50, 0.60, 0.70, 0.80, 0.85]:
    acc_k6 = b1sc_accuracy(p0, 6) # Even K=6 with coin tie
    # Add coin-tie:
    acc_k6 = (1.0 - stats.binom.cdf(3, 6, p0)) + 0.5 * stats.binom.pmf(3, 6, p0)
    acc_k9 = b1sc_accuracy(p0, 9)
    acc_deb, fcr = debate_accuracy(p0, p_sycophancy=0.50, p_truth_persuade=0.25)
    delta = (acc_deb - acc_k9) * 100
    print(f"{p0:<8.2f} | {acc_k6*100:<13.2f}% | {acc_k9*100:<13.2f}% | {acc_deb*100:<17.2f}% | {fcr*100:<23.2f}% | {delta:<+19.2f}%")
