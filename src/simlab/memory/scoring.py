"""Mathematically Rigorous Normalization and Scoring Functions."""

import math
from typing import List, Sequence
import numpy as np


def min_max_norm(vals: Sequence[float], baseline_on_uniform: float = 0.0) -> List[float]:
    """
    Min-Max feature scaling into [0.0, 1.0].
    
    Tie / Zero-Variance Policy:
    When max == min (all values identical, e.g. uniform importance or zero similarity),
    returns baseline_on_uniform (default 0.0) rather than 1.0. This prevents uninformative,
    zero-variance components from dominating retrieval scoring.
    
    Empty input returns empty list [].
    """
    if not vals:
        return []

    vals_arr = np.array(vals, dtype=float)
    if not np.all(np.isfinite(vals_arr)):
        # Guard against NaN/Inf
        vals_arr = np.nan_to_num(vals_arr, nan=0.0, posinf=1.0, neginf=0.0)

    mn = float(np.min(vals_arr))
    mx = float(np.max(vals_arr))

    if mx == mn:
        return [float(baseline_on_uniform)] * len(vals)

    normed = (vals_arr - mn) / (mx - mn)
    return normed.tolist()


def z_score_norm(vals: Sequence[float]) -> List[float]:
    """Z-score standardization (mean=0, std=1). Zero std returns zeros."""
    if not vals:
        return []
    arr = np.array(vals, dtype=float)
    std = float(np.std(arr))
    if std == 0.0 or not math.isfinite(std):
        return [0.0] * len(vals)
    return ((arr - float(np.mean(arr))) / std).tolist()


def softmax_norm(vals: Sequence[float], temperature: float = 1.0) -> List[float]:
    """Numerically stable softmax normalization."""
    if not vals:
        return []
    temp = max(1e-6, temperature)
    arr = np.array(vals, dtype=float) / temp
    arr = arr - np.max(arr)  # Prevent exponent overflow
    exp_arr = np.exp(arr)
    sum_exp = float(np.sum(exp_arr))
    if sum_exp == 0.0 or not math.isfinite(sum_exp):
        return [1.0 / len(vals)] * len(vals)
    return (exp_arr / sum_exp).tolist()


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Cosine similarity between two vector representations."""
    a = np.array(vec_a, dtype=float)
    b = np.array(vec_b, dtype=float)
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    sim = float(np.dot(a, b) / (norm_a * norm_b))
    return max(-1.0, min(1.0, sim))


def calculate_recency_decay(delta_hours: float, decay_rate: float = 0.995) -> float:
    """
    Standard Smallville exponential recency decay.
    recency = decay_rate ** delta_hours
    """
    if delta_hours < 0:
        delta_hours = 0.0
    return float(decay_rate ** delta_hours)


def calculate_tri_factor_scores(
    recencies: Sequence[float],
    relevances: Sequence[float],
    importances: Sequence[float],
    alpha: float = 1.0,
    beta: float = 1.0,
    gamma: float = 1.0,
    norm_fn=min_max_norm
) -> List[float]:
    """
    Compute combined tri-factor score:
    Score = alpha * norm(recency) + beta * norm(relevance) + gamma * norm(importance)
    """
    n_rec = norm_fn(recencies)
    n_rel = norm_fn(relevances)
    n_imp = norm_fn(importances)

    scores = []
    for r, rel, imp in zip(n_rec, n_rel, n_imp):
        score = (alpha * r) + (beta * rel) + (gamma * imp)
        scores.append(float(score))
    return scores


def compute_retrieval_score(
    recency_norm: float,
    similarity_norm: float,
    importance_norm: float,
    alpha: float = 1.0 / 3.0,
    beta: float = 1.0 / 3.0,
    gamma: float = 1.0 / 3.0
) -> float:
    """Compute individual retrieval score from normalized components."""
    return float(alpha * recency_norm + beta * similarity_norm + gamma * importance_norm)

