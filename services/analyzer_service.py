from typing import List, Dict
from core.interfaces import IMACCalculator, IDataLoader, IResultReporter
from core.entities import Label, TestCase, Matrix

class AnalyzerService:

    def __init__(self, 
                 calculator: IMACCalculator, 
                 loader: IDataLoader, 
                 reporter: IResultReporter):
        self._calculator = calculator
        self._loader = loader
        self._reporter = reporter
        self._epsilon = 1e-9

    def analyze_user_input(self, filter_a: Matrix, filter_b: Matrix, pattern: Matrix):

        avg_time = self._measure_avg_time(pattern, filter_a, iterations=10)

        score_a = self._calculator.calculate(pattern, filter_a)
        score_b = self._calculator.calculate(pattern, filter_b)

        final_decision = self._calculator.compare_scores(score_a, score_b, self._epsilon)

        res_map = {Label.CROSS: "A", Label.X: "B", Label.UNDECIDED: "판정 불가"}
        decision_text = res_map.get(final_decision, "판정 불가")

        self._reporter.display_message(f"\n[결과]")
        self._reporter.display_message(f"A 점수: {score_a:.4f}")
        self._reporter.display_message(f"B 점수: {score_b:.4f}")
        self._reporter.display_message(f"연산 시간(평균/10회): {avg_time:.4f} ms")
        self._reporter.display_message(f"판정: {decision_text}")

    def analyze_json_file(self, file_path: str):
        filters_map = self._loader.load_filters(file_path)
        patterns_data = self._loader.load_patterns(file_path)

        passed_count = 0
        failed_count = 0
        fail_details = []

        for item in patterns_data:
            case_id = item['id']
            size = item['size']
            input_matrix = item['input']
            expected_label = item['expected']

            size_key = f"size_{size}"
            if size_key not in filters_map:
                failed_count += 1
                fail_details.append(f"{case_id}: 크기 {size}에 맞는 필터가 없음")
                continue

            filters = filters_map[size_key]
            
            score_cross = self._calculator.calculate(input_matrix, filters[Label.CROSS])
            score_x = self._calculator.calculate(input_matrix, filters[Label.X])

            final_decision = self._calculator.compare_scores(score_cross, score_x, self._epsilon)
            is_pass = (final_decision == expected_label)

            if is_pass:
                passed_count += 1
            else:
                failed_count += 1
                fail_details.append(f"{case_id}: 판정 {final_decision.value} != 기대 {expected_label.value}")

            self._reporter.print_case_result(
                case_id, score_cross, score_x, final_decision, expected_label, is_pass
            )

        self.run_performance_benchmark(patterns_data)
        self._reporter.report_summary(len(patterns_data), passed_count, failed_count, fail_details)

    def run_performance_benchmark(self, patterns: List[Dict]):

        measured_sizes = set()
        size_list = []
        time_list = []
        ops_list = []
        
        sorted_patterns = sorted(patterns, key=lambda x: x['size'])

        for p in sorted_patterns:
            size = p['size']
            if size in measured_sizes:
                continue
            
            avg_time = self._measure_avg_time(p['input'], p['input'])
            
            size_list.append(size)
            time_list.append(avg_time)
            ops_list.append(size * size)
            measured_sizes.add(size)
            
        self._reporter.report_performance(size_list, time_list, ops_list)

    def _measure_avg_time(self, mat_a: Matrix, mat_b: Matrix, iterations: int = 10) -> float:
        import time
        start = time.perf_counter()
        for _ in range(iterations):
            self._calculator.calculate(mat_a, mat_b)
        end = time.perf_counter()
        return ((end - start) * 1000) / iterations