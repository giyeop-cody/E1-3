from abc import ABC, abstractmethod
from typing import List, Optional, Protocol, runtime_checkable
from core.entities import Matrix, Label

@runtime_checkable
class IMACCalculator(Protocol):

    @abstractmethod
    def calculate(self, pattern: Matrix, filter_obj: Matrix) -> float:
        pass

    @abstractmethod
    def compare_scores(self, score_a: float, score_b: float, epsilon: float = 1e-9) -> Label:
        pass


class IDataLoader(ABC):
    @abstractmethod
    def load_filters(self, source: str) -> dict:
        pass

    @abstractmethod
    def load_patterns(self, source: str) -> List[dict]:
        pass


class IResultReporter(ABC):
    @abstractmethod
    def report_performance(self, size: int, avg_time_ms: float, operations: int):
        pass

    @abstractmethod
    def report_summary(self, total: int, passed: int, failed: int, fail_details: List[str]):
        pass

    @abstractmethod
    def print_case_result(self, case_id: str, score_cross: float, score_x: float, 
                          final_label: Label, expected_label: Label, is_pass: bool):
        pass
