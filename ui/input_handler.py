from typing import List, Optional
from core.entities import Matrix

class InputHandler:


    def get_user_choice(self) -> str:
        return input("선택: ").strip()

    def input_matrix(self, size: int, label: str) -> Matrix:

        print(f"\n{label} ({size}줄 입력, 공백 구분)")
        
        while True:
            matrix_data = []
            error_occurred = False
            
            for i in range(size):
                line = input(f"{i+1}행: ").strip()
                try:
                    row = [float(x) for x in line.split()]
                    
                    if len(row) != size:
                        print(f"입력 형식 오류: 한 줄에 {size}개의 숫자가 있어야 합니다. (현재 {len(row)}개)")
                        error_occurred = True
                        break
                    matrix_data.append(row)
                except ValueError:
                    print("입력 형식 오류: 숫자만 입력 가능합니다.")
                    error_occurred = True
                    break
            
            if not error_occurred and len(matrix_data) == size:
                try:
                    return Matrix(matrix_data)
                except ValueError as e:
                    print(f"검증 오류: {e}")
            
            print("행렬 입력을 처음부터 다시 시작합니다.")

    def ask_file_path(self, default: str = "data.json") -> str:
        """분석할 JSON 파일 경로를 입력받습니다."""
        path = input(f"JSON 파일 경로 입력 (기본값: {default}): ").strip()
        return path if path else default

    def wait_for_enter(self):
        """사용자가 확인을 위해 엔터를 누를 때까지 대기합니다."""
        input("\n계속하려면 엔터를 누르세요...")
