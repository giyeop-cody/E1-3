from typing import List, Dict
from core.interfaces import IMACCalculator, IDataLoader, IResultReporter
from core.entities import Label, TestCase, Matrix

class AnalyzerService:
    """
    [Application Service] 
    패턴 매칭 분석의 전체 워크플로우를 관리합니다.
    계층 간 의존성을 주입받아 사용하며, 순수 비즈니스 로직의 흐름에 집중합니다.
    """
    def __init__(self, 
                 calculator: IMACCalculator, 
                 loader: IDataLoader, 
                 reporter: IResultReporter):
        # 의존성 주입 (Dependency Injection)
        self._calculator = calculator
        self._loader = loader
        self._reporter = reporter
        self._epsilon = 1e-9

    def analyze_json_data(self, file_path: str):
        """
        JSON 데이터를 로드하여 일괄 판정하고 결과를 리포팅합니다.
        """
        # 1. 필터 및 패턴 로드
        filters_map = self._loader.load_filters(file_path)
        patterns_data = self._loader.load_patterns(file_path)

        results = []
        passed_count = 0
        failed_count = 0
        fail_details = []

        # 2. 각 패턴별 루프 수행
        for item in patterns_data:
            case_id = item['id']
            size = item['size']
            input_matrix = item['input']
            expected_label = item['expected']

            # 크기에 맞는 필터 가져오기 (Cross, X)
            size_key = f"size_{size}"
            if size_key not in filters_map:
                fail_details.append(f"{case_id}: 필터 크기 불일치 (size_{size} 필터 없음)")
                failed_count += 1
                continue

            current_filters = filters_map[size_key]
            
            # 3. MAC 연산 수행 (Cross 필터 vs X 필터)
            score_cross = self._calculator.calculate(input_matrix, current_filters[Label.CROSS])
            score_x = self._calculator.calculate(input_matrix, current_filters[Label.X])

            # 4. 결과 판정
            final_decision = self._calculator.compare_scores(score_cross, score_x, self._epsilon)
            is_pass = (final_decision == expected_label)

            if is_pass:
                passed_count += 1
            else:
                failed_count += 1
                fail_details.append(f"{case_id}: 판정 {final_decision.value} != 기대 {expected_label.value}")

            # 5. 개별 결과 출력 요청 (UI 계층 대행)
            self._reporter.print_case_result(
                case_id, score_cross, score_x, final_decision, expected_label, is_pass
            )

        # 6. 전체 요약 리포트
        self._reporter.report_summary(len(patterns_data), passed_count, failed_count, fail_details)

    def run_performance_benchmark(self, patterns: List[Dict]):
        """
        다양한 크기의 패턴들에 대해 성능 측정을 수행합니다.
        """
        # 중복 크기 제외하고 크기별로 하나씩 측정
        measured_sizes = set()
        
        for p in patterns:
            size = p['size']
            if size in measured_sizes:
                continue
            
            # 임시 필터 생성 (성능 측정용)
            dummy_matrix = p['input']
            
            # 인터페이스를 통한 시간 측정 호출
            # (Note: 구현체인 MACCalculator에 measure_performance가 있다고 가정하거나 
            #  여기서 직접 반복문을 돌려 측정 가능)
            avg_time = self._measure_avg_time(dummy_matrix, dummy_matrix)
            
            self._reporter.report_performance(size, avg_time, size * size)
            measured_sizes.add(size)

    def _measure_avg_time(self, mat_a: Matrix, mat_b: Matrix, iterations: int = 10) -> float:
        """내부 헬퍼: 순수 연산 시간 측정"""
        import time
        start = time.perf_counter()
        for _ in range(iterations):
            self._calculator.calculate(mat_a, mat_b)
        end = time.perf_counter()
        return ((end - start) / iterations) * 1000  # ms 변환
