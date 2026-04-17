import time
from core.interfaces import IMACCalculator
from core.entities import Matrix, Label

class MACCalculator(IMACCalculator):
    def calculate(self, pattern: Matrix, filter_obj: Matrix) -> float:

        if pattern.size != filter_obj.size:
            raise ValueError(f"연산 불가: 패턴 크기({pattern.size})와 필터 크기({filter_obj.size})가 일치하지 않습니다.")

        total_score = 0.0
        n = pattern.size

        for r in range(n):
            for c in range(n):
                product = pattern.get_value(r, c) * filter_obj.get_value(r, c)
                total_score += product

        return total_score

    def compare_scores(self, score_a: float, score_b: float, epsilon: float = 1e-9) -> Label:
        diff = score_a - score_b

        if abs(diff) < epsilon:
            return Label.UNDECIDED
        
        return Label.CROSS if diff > 0 else Label.X

    def measure_performance(self, pattern: Matrix, filter_obj: Matrix, iterations: int = 10) -> float:

        start_time = time.perf_counter()
        
        for _ in range(iterations):
            self.calculate(pattern, filter_obj)
            
        end_time = time.perf_counter()
        
        avg_time_ms = ((end_time - start_time) / iterations) * 1000
        return avg_time_ms
