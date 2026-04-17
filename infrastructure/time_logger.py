import time
from typing import Callable, Any, Dict

class TimeLogger:
    """
    [Infrastructure Layer]
    성능 측정 및 시간 기록을 담당하는 유틸리티 클래스입니다.
    순수 연산 시간을 정밀하게 측정하기 위한 헬퍼 메서드를 제공합니다.
    """

    @staticmethod
    def measure_ms(func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        특정 함수의 실행 시간을 밀리초(ms) 단위로 측정합니다.
        
        :param func: 측정할 함수 (콜백)
        :param args: 함수에 전달할 인자
        :param kwargs: 함수에 전달할 키워드 인자
        :return: {'result': 함수 결과, 'time_ms': 소요 시간}
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        elapsed_ms = (end_time - start_time) * 1000
        return {
            'result': result,
            'time_ms': elapsed_ms
        }

    @staticmethod
    def measure_average_ms(iterations: int, func: Callable, *args, **kwargs) -> float:
        """
        함수를 여러 번 반복 실행하여 평균 소요 시간(ms)을 측정합니다.
        최소 10회 이상의 반복 측정을 통해 정밀도를 확보합니다.
        """
        if iterations < 1:
            iterations = 1
            
        total_time_ms = 0.0
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time_ms += (end_time - start_time) * 1000
            
        return total_time_ms / iterations

    @staticmethod
    def format_ms(ms: float) -> str:
        """시간 데이터를 가독성 좋은 문자열로 변환합니다."""
        return f"{ms:.4f} ms"
