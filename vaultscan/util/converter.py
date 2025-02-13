class TypeConverter:
    @staticmethod
    def string_to_boolean(input: str) -> bool:
        if input == 'True' or input == 'true':
            return True
        return False
