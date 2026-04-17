import json
import os
from typing import List, Dict
from core.interfaces import IDataLoader
from core.entities import Matrix, Label

class JSONLoader(IDataLoader):
    def _read_file(self, source: str) -> dict:
        if not os.path.exists(source):
            raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {source}")
        
        with open(source, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_filters(self, source: str) -> Dict[str, Dict[Label, Matrix]]:
        raw_data = self._read_file(source)
        filters_section = raw_data.get('filters', {})
        processed_filters = {}

        for size_key, filter_types in filters_section.items():
            processed_filters[size_key] = {}
            for label_key, matrix_data in filter_types.items():
                normalized_label = Label.normalize(label_key)
                processed_filters[size_key][normalized_label] = Matrix(matrix_data)
        
        return processed_filters

    def load_patterns(self, source: str) -> List[dict]:

        raw_data = self._read_file(source)
        patterns_section = raw_data.get('patterns', {})
        test_cases = []

        for pattern_id, details in patterns_section.items():
            try:
                size = int(pattern_id.split('_')[1])
            except (IndexError, ValueError):
                continue

            input_data = details.get('input', [])
            expected_raw = details.get('expected', '')

            test_cases.append({
                'id': pattern_id,
                'size': size,
                'input': Matrix(input_data),
                'expected': Label.normalize(expected_raw)
            })

        return test_cases
