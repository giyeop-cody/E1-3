from enum import Enum
from typing import List

class Label(Enum):
    """표준 라벨을 정의하는 열거형 클래스 (Label Normalization)"""
    CROSS = "Cross"
    X = "X"
    UNDECIDED = "UNDECIDED"

    @classmethod
    def normalize(cls, value: str) -> 'Label':
        """다양한 입력 형식을 표준 라벨로 변환합니다."""
        clean_val = str(value).strip().lower()
        if clean_val in ['+', 'cross']:
            return cls.CROSS
        if clean_val in ['x']:
            return cls.X
        return cls.UNDECIDED

class Matrix:
    """
    2차원 수치 데이터를 관리하고 보호하는 엔티티
    """
    def __init__(self, data: List[List[float]]):
        self._validate(data)
        self._data = data
        self._size = len(data)

    def _validate(self, data: List[List[float]]):
        """행렬의 유효성을 검사합니다 (정사각형 여부 등)."""
        if not data:
            raise ValueError("데이터가 비어있습니다.")
        
        row_count = len(data)
        for i, row in enumerate(data):
            if len(row) != row_count:
                raise ValueError(f"행렬은 정사각형이어야 합니다. 행 {i}의 길이가 {len(row)}입니다.")

    @property
    def size(self) -> int:
        """행렬의 크기(N)를 반환합니다."""
        return self._size

    def get_value(self, row: int, col: int) -> float:
        """특정 위치의 값을 안전하게 반환합니다."""
        if 0 <= row < self._size and 0 <= col < self._size:
            return self._data[row][col]
        raise IndexError(f"인덱스 범위를 벗어났습니다: ({row}, {col})")

    def to_flat_list(self) -> List[float]:
        """보너스 과제 대비: 2차원 배열을 1차원으로 변환하여 반환합니다."""
        return [item for row in self._data for item in row]

    def __repr__(self) -> str:
        return f"Matrix({self._size}x{self._size})"

class TestCase:
    """
    하나의 분석 단위(패턴, 필터들, 기대값)를 캡슐화하는 클래스
    """
    def __init__(self, case_id: str, pattern: Matrix, expected: Label):
        self.case_id = case_id
        self.pattern = pattern
        self.expected = expected
        self.results = {}  # {Label.CROSS: score, Label.X: score}

    def set_score(self, label: Label, score: float):
        self.results[label] = score

    def get_final_decision(self, epsilon: float = 1e-9) -> Label:
        """MAC 점수를 기반으로 최종 라벨을 판정합니다."""
        score_cross = self.results.get(Label.CROSS, 0.0)
        score_x = self.results.get(Label.X, 0.0)

        if abs(score_cross - score_x) < epsilon:
            return Label.UNDECIDED
        
        return Label.CROSS if score_cross > score_x else Label.X
