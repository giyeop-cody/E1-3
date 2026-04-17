import json
import os
from typing import List, Dict
from core.interfaces import IDataLoader
from core.entities import Matrix, Label

class JSONLoader(IDataLoader):
    """
    [Infrastructure Layer]
    data.json 파일을 읽어 도메인 객체(Matrix, Label)로 변환하는 클래스입니다.
    """

    def _read_file(self, source: str) -> dict:
        """파일 존재 여부 확인 및 JSON 로드 내부 메서드"""
        if not os.path.exists(source):
            raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {source}")
        
        with open(source, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_filters(self, source: str) -> Dict[str, Dict[Label, Matrix]]:
        """
        JSON에서 필터 데이터를 읽어 표준 라벨로 매핑된 Matrix 딕셔너리를 반환합니다.
        결과 예시: {'size_5': {Label.CROSS: Matrix, Label.X: Matrix}}
        """
        raw_data = self._read_file(source)
        filters_section = raw_data.get('filters', {})
        processed_filters = {}

        for size_key, filter_types in filters_section.items():
            processed_filters[size_key] = {}
            for label_key, matrix_data in filter_types.items():
                # 라벨 정규화 (cross -> Label.CROSS)
                normalized_label = Label.normalize(label_key)
                processed_filters[size_key][normalized_label] = Matrix(matrix_data)
        
        return processed_filters

    def load_patterns(self, source: str) -> List[dict]:
        """
        JSON에서 패턴 데이터를 읽어 분석용 리스트를 생성합니다.
        키(size_N_idx)에서 크기(N)를 추출하는 규칙을 처리합니다.
        """
        raw_data = self._read_file(source)
        patterns_section = raw_data.get('patterns', {})
        test_cases = []

        for pattern_id, details in patterns_section.items():
            # 1. 패턴 식별자에서 크기 N 추출 (예: "size_13_1" -> 13)
            try:
                size = int(pattern_id.split('_')[1])
            except (IndexError, ValueError):
                # 명명 규칙이 어긋난 경우 건너뛰거나 기본값 처리
                continue

            # 2. 데이터 추출 및 객체화
            input_data = details.get('input', [])
            expected_raw = details.get('expected', '')

            # 3. 데이터 구조화 (정규화 포함)
            test_cases.append({
                'id': pattern_id,
                'size': size,
                'input': Matrix(input_data),
                'expected': Label.normalize(expected_raw)
            })

        return test_cases
