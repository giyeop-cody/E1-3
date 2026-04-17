from enum import Enum
from typing import List

class Label(Enum):
    CROSS = "Cross"
    X = "X"
    UNDECIDED = "UNDECIDED"

    @classmethod
    def normalize(cls, value: str) -> 'Label':
        clean_val = str(value).strip().lower()
        if clean_val in ['+', 'cross']:
            return cls.CROSS
        if clean_val in ['x']:
            return cls.X
        return cls.UNDECIDED

class Matrix:
    def __init__(self, data: List[List[float]]):
        self._validate(data)
        self._data = data
        self._size = len(data)

    def _validate(self, data: List[List[float]]):
        if not data:
            raise ValueError("데이터가 비어있습니다.")
        
        row_count = len(data)
        for i, row in enumerate(data):
            if len(row) != row_count:
                raise ValueError(f"행렬은 정사각형이어야 합니다. 행 {i}의 길이가 {len(row)}입니다.")

    @property
    def size(self) -> int:
        return self._size

    def get_value(self, row: int, col: int) -> float:
        if 0 <= row < self._size and 0 <= col < self._size:
            return self._data[row][col]
        raise IndexError(f"인덱스 범위를 벗어났습니다: ({row}, {col})")

    def to_flat_list(self) -> List[float]:
        return [item for row in self._data for item in row]

    def __repr__(self) -> str:
        return f"Matrix({self._size}x{self._size})"

class TestCase:

    def __init__(self, case_id: str, pattern: Matrix, expected: Label):
        self.case_id = case_id
        self.pattern = pattern
        self.expected = expected
        self.results = {}  # {Label.CROSS: score, Label.X: score}

    def set_score(self, label: Label, score: float):
        self.results[label] = score

    def get_final_decision(self, epsilon: float = 1e-9) -> Label:
        score_cross = self.results.get(Label.CROSS, 0.0)
        score_x = self.results.get(Label.X, 0.0)

        if abs(score_cross - score_x) < epsilon:
            return Label.UNDECIDED
        
        return Label.CROSS if score_cross > score_x else Label.X
