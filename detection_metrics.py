"""
detection_metrics.py
---------------------
Chhota sa module jo CCTV/AI detection events ko validate karta hai
aur basic accuracy metrics (Precision, Recall, F1) nikalta hai.

Yeh deliberately simple rakha hai taaki CI/CD seekhte time
focus pipeline par ho, code par nahi. But theme aapke HawkVision
kaam se match karta hai (detection events + confusion matrix).
"""

from dataclasses import dataclass


@dataclass
class DetectionEvent:
    camera_id: str
    timestamp: str          # ISO format, e.g. "2026-06-12T14:30:00"
    label: str              # e.g. "person", "vehicle", "fire"
    confidence: float       # 0.0 se 1.0 ke beech


def validate_event(event: DetectionEvent) -> bool:
    """
    Ek detection event valid hai ya nahi check karta hai.
    Real QA me yahi cheezein aap manually verify karti hain —
    yahan hum automate kar rahe hain.
    """
    if not event.camera_id or not event.camera_id.strip():
        return False
    if not event.timestamp or "T" not in event.timestamp:
        return False
    if not event.label or not event.label.strip():
        return False
    if not (0.0 <= event.confidence <= 1.0):
        return False
    return True


def confusion_matrix(predicted: list[bool], actual: list[bool]) -> dict:
    """
    predicted: model ne detect kiya (True) ya nahi (False)
    actual:    ground truth — sach me tha (True) ya nahi (False)

    Returns: TP, FP, FN, TN counts.
    """
    if len(predicted) != len(actual):
        raise ValueError("predicted aur actual ki length same honi chahiye")

    tp = fp = fn = tn = 0
    for p, a in zip(predicted, actual):
        if p and a:
            tp += 1
        elif p and not a:
            fp += 1
        elif not p and a:
            fn += 1
        else:
            tn += 1
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn}


def precision(cm: dict) -> float:
    denom = cm["TP"] + cm["FP"]
    return cm["TP"] / denom if denom else 0.0


def recall(cm: dict) -> float:
    denom = cm["TP"] + cm["FN"]
    return cm["TP"] / denom if denom else 0.0


def f1_score(cm: dict) -> float:
    p, r = precision(cm), recall(cm)
    return (2 * p * r) / (p + r) if (p + r) else 0.0
