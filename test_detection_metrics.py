"""
test_detection_metrics.py
-------------------------
Yeh woh tests hain jo CI pipeline har push/PR par automatically chalayegi.
Command locally: pytest -v
"""

import pytest
from detection_metrics import (
    DetectionEvent,
    validate_event,
    confusion_matrix,
    precision,
    recall,
    f1_score,
)


# ---------- validate_event ke tests ----------

def test_valid_event_passes():
    e = DetectionEvent("CAM-01", "2026-06-12T14:30:00", "person", 0.92)
    assert validate_event(e) is True


def test_empty_camera_id_fails():
    e = DetectionEvent("", "2026-06-12T14:30:00", "person", 0.92)
    assert validate_event(e) is False


def test_bad_timestamp_fails():
    e = DetectionEvent("CAM-01", "12-06-2026 14:30", "person", 0.92)
    assert validate_event(e) is False


def test_confidence_out_of_range_fails():
    e = DetectionEvent("CAM-01", "2026-06-12T14:30:00", "fire", 1.4)
    assert validate_event(e) is False


# ---------- confusion_matrix ke tests ----------

def test_confusion_matrix_counts():
    predicted = [True, True, False, False]
    actual = [True, False, True, False]
    cm = confusion_matrix(predicted, actual)
    assert cm == {"TP": 1, "FP": 1, "FN": 1, "TN": 1}


def test_mismatched_length_raises():
    with pytest.raises(ValueError):
        confusion_matrix([True], [True, False])


# ---------- metrics ke tests ----------

def test_precision_recall_f1():
    cm = {"TP": 8, "FP": 2, "FN": 2, "TN": 88}
    assert precision(cm) == pytest.approx(0.8)
    assert recall(cm) == pytest.approx(0.8)
    assert f1_score(cm) == pytest.approx(0.8)


def test_no_predictions_gives_zero():
    cm = {"TP": 0, "FP": 0, "FN": 5, "TN": 10}
    assert precision(cm) == 0.0
    assert f1_score(cm) == 0.0
