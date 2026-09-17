import numpy as np
from src.metrics import compute_aspect_ratio, compute_ear, compute_mar

def test_compute_aspect_ratio():
    # Mock landmarks for a perfect square "eye"
    # p1, p2, p3, p4, p5, p6
    # p1 = (0, 1), p2 = (1, 2), p3 = (2, 2), p4 = (3, 1), p5 = (2, 0), p6 = (1, 0)
    mock_landmarks = np.array([
        [0, 1],
        [1, 2],
        [2, 2],
        [3, 1],
        [2, 0],
        [1, 0]
    ])
    indices = [0, 1, 2, 3, 4, 5]
    
    # Vert1 (p2-p6) = (1,2) to (1,0) = 2
    # Vert2 (p3-p5) = (2,2) to (2,0) = 2
    # Horiz (p1-p4) = (0,1) to (3,1) = 3
    # Ratio = (2 + 2) / (2 * 3) = 4 / 6 = 0.666...
    ratio = compute_aspect_ratio(mock_landmarks, indices)
    assert np.isclose(ratio, 0.666666)

def test_compute_ear_none():
    assert compute_ear(None) == 0.0

def test_compute_mar_none():
    assert compute_mar(None) == 0.0
