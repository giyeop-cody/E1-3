import time
from core.interfaces import IMACCalculator
from core.entities import Matrix, Label

class MACCalculator(IMACCalculator):
    """
    [Domain Service] MAC(Multiply-Accumulate) 연산의 실제 구현체
    """

    def calculate(self, pattern: Matrix, filter_obj: Matrix) -> float:
        """
        패턴과 필터를 순회하며 위치별 곱셈의 합(MAC)을 계산합니다.
        성능 측정을 위해 순수 연산 로직만 포함합니다.
        
        시간 복잡도: O(N^2) (N은 행렬의 한 변의 길이)
        """
        if pattern.size != filter_obj.size:
            raise ValueError(f"연산 불가: 패턴 크기({pattern.size})와 필터 크기({filter_obj.size})가 일치하지 않습니다.")

        total_score = 0.0
        n = pattern.size

        # O(N^2) 중첩 반복문을 통한 MAC 연산 수행
        for r in range(n):
            for c in range(n):
                # 위치별 곱셈 (Multiply)
                product = pattern.get_value(r, c) * filter_obj.get_value(r, c)
                # 누적 덧셈 (Accumulate)
                total_score += product

        return total_score

    def compare_scores(self, score_a: float, score_b: float, epsilon: float = 1e-9) -> Label:
        """
        두 점수의 차이를 epsilon(허용오차) 기준으로 비교하여 판정합니다.
        """
        diff = score_a - score_b

        # 허용오차 범위 내라면 동점(UNDECIDED) 처리
        if abs(diff) < epsilon:
            return Label.UNDECIDED
        
        # 더 높은 점수를 가진 필터의 라벨 반환
        return Label.CROSS if diff > 0 else Label.X

    def measure_performance(self, pattern: Matrix, filter_obj: Matrix, iterations: int = 10) -> float:
        """
        [Utility] 특정 연산을 반복 수행하여 평균 실행 시간(ms)을 측정합니다.
        I/O 시간을 제외하고 오직 calculate 호출 시간만 측정합니다.
        """
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            self.calculate(pattern, filter_obj)
            
        end_time = time.perf_counter()
        
        # 전체 소요 시간을 반복 횟수로 나누어 평균 ms 계산
        avg_time_ms = ((end_time - start_time) / iterations) * 1000
        return avg_time_ms
