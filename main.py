import sys
from infrastructure.json_loader import JSONLoader
from ui.console_view import ConsoleView
from ui.input_handler import InputHandler
from core.calculator import MACCalculator
from services.analyzer_service import AnalyzerService

def main():
    loader = JSONLoader()
    view = ConsoleView()
    input_handler = InputHandler()
    calculator = MACCalculator()

    service = AnalyzerService(
        loader=loader,
        reporter=view,
        calculator=calculator
    )

    while True:
        view.print_menu()
        choice = input_handler.get_user_choice()

        if choice == '1':
            try:
                size = 3
                view.display_message(f"\n--- [모드 1] {size}x{size} 사용자 입력 모드 ---")
                
                filter_a = input_handler.input_matrix(size, "필터 A")
                filter_b = input_handler.input_matrix(size, "필터 B")
                pattern = input_handler.input_matrix(size, "입력 패턴")

                service.analyze_user_input(filter_a, filter_b, pattern)
                
            except Exception as e:
                view.display_error(f"실행 중 오류 발생: {e}")
            
            input_handler.wait_for_enter()

        elif choice == '2':
            try:
                file_path = input_handler.ask_file_path("data.json")
                view.display_message(f"\n--- [모드 2] {file_path} 분석 시작 ---")
                
                service.analyze_json_file(file_path)
                
            except FileNotFoundError as e:
                view.display_error(str(e))
            except Exception as e:
                view.display_error(f"파일 분석 중 예상치 못한 오류 발생: {e}")
                
            input_handler.wait_for_enter()

        elif choice == '0':
            view.display_message("프로그램을 종료합니다. 이용해 주셔서 감사합니다.")
            sys.exit(0)

        else:
            view.display_error("잘못된 선택입니다. 다시 입력해 주세요.")

if __name__ == "__main__":
    main()