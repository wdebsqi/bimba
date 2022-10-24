from typing import Any


class TypeValidator:
    @staticmethod
    def validate_type(value: Any, type_to_validate_against: type) -> bool:
        """Validates if a value can be converted to the given type"""
        try:
            type_to_validate_against(value)
            return True
        except Exception:
            return False
