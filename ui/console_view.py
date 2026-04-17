from typing import List, Dict
from core.interfaces import IResultReporter
from core.entities import Label

class ConsoleView(IResultReporter):

    def print_menu(self):
        print("\n" + "="*40)
        print("      Mini NPU Simulator      ")
        print("="*40)
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")
        print("-" * 40)

    def print_case_result(self, case_id: str, score_cross: float, score_x: float, 
                          final_label: Label, expected_label: Label, is_pass: bool):
        status = "PASS" if is_pass else "FAIL"
        
        print(f"\n- -- {case_id} ---")
        print(f"Cross 점수: {score_cross:.10f}")
        print(f"X 점수     : {score_x:.10f}")
        
        decision_str = final_label.value
        if final_label == Label.UNDECIDED:
            decision_str = f"UNDECIDED (|Cross - X| < 1e-9)"
            
        print(f"판정: {decision_str} | expected: {expected_label.value} | {status}")

    def report_performance(self, size_list: List[int], time_list: List[float], ops_list: List[int]):

        print("\n#---------------------------------------")
        print("# [3] 성능 분석 (평균/10회)")
        print("#---------------------------------------")
        print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
        print("-" * 45)
        
        for size, avg_time, ops in zip(size_list, time_list, ops_list):
            size_str = f"{size}x{size}"
            print(f"{size_str:<10} {avg_time:<15.4f} {ops:<10}")
        print("-" * 45)

    def report_summary(self, total: int, passed: int, failed: int, fail_details: List[str]):
        print("\n#---------------------------------------")
        print("# [4] 결과 요약")
        print("#---------------------------------------")
        print(f"총 테스트 : {total}개")
        print(f"통과      : {passed}개")
        print(f"실패      : {failed}개")
        
        if fail_details:
            print("\n실패 케이스 목록:")
            for detail in fail_details:
                print(f"- {detail}")
        
        print("\n(상세 원인 분석 및 복잡도 설명은 README.md를 확인하세요.)")

    def display_error(self, message: str):
        print(f"\n[오류] {message}")

    def display_message(self, message: str):
        print(message)
