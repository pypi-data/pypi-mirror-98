
class ValidationBroker(Exception):

    def __init__(self) -> None:
        self.message = 'Need a broker to use Arsene'
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
