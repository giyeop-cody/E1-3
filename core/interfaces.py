from abc import ABC, abstractmethod
from typing import List, Optional, Protocol, runtime_checkable
from core.entities import Matrix, Score, Label

@runtime_checkable
class IMACCalculator(Protocol):
    """
    [Interface] MAC(Multiply-Accumulate) 연산을 수행하는 계산기 인터페이스
    """
    @abstractmethod
    def calculate(self, pattern: Matrix, filter_obj: Matrix) -> float:
        """
        두 행렬을 입력받아 MAC 연산 점수를 반환합니다.
        :param pattern: 입력된 데이터 행렬
        :param filter_obj: 비교 기준이 되는 필터 행렬
        :return: 누적 합계 점수
        """
        pass

    @abstractmethod
    def compare_scores(self, score_a: float, score_b: float, epsilon: float = 1e-9) -> Label:
        """
        두 점수를 비교하여 더 높은 쪽의 라벨을 반환합니다.
        :param score_a: 필터 A의 점수
        :param score_b: 필터 B의 점수
        :param epsilon: 부동소수점 오차 허용 범위
        :return: Label.CROSS, Label.X 또는 Label.UNDECIDED
        """
        pass


class IDataLoader(ABC):
    """
    [Interface] 외부로부터 데이터를 로드하고 정규화하는 데이터 로더 인터페이스
    """
    @abstractmethod
    def load_filters(self, source: str) -> dict:
        """
        크기별 필터 데이터를 로드하여 사전 형태로 반환합니다.
        :return: { 'size_5': {'Cross': Matrix, 'X': Matrix}, ... }
        """
        pass

    @abstractmethod
    def load_patterns(self, source: str) -> List[dict]:
        """
        테스트용 패턴 데이터를 로드하여 리스트 형태로 반환합니다.
        :return: [{'id': str, 'input': Matrix, 'expected': Label, 'size': int}, ...]
        """
        pass


class IResultReporter(ABC):
    """
    [Interface] 분석 결과를 출력하거나 기록하는 리포터 인터페이스
    """
    @abstractmethod
    def report_performance(self, size: int, avg_time_ms: float, operations: int):
        """성능 지표를 표 형태로 출력합니다."""
        pass

    @abstractmethod
    def report_summary(self, total: int, passed: int, failed: int, fail_details: List[str]):
        """최종 결과 요약을 출력합니다."""
        pass

    @abstractmethod
    def print_case_result(self, case_id: str, score_cross: float, score_x: float, 
                          final_label: Label, expected_label: Label, is_pass: bool):
        """개별 테스트 케이스의 결과를 출력합니다."""
        pass
