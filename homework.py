from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    COEF_RUN_GIVEN_1: int = 18
    COEF_RUN_GIVEN_2: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.COEF_RUN_GIVEN_1 * self.get_mean_speed()
                 + self.COEF_RUN_GIVEN_2) * self.weight
                / self.M_IN_KM * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEF_WALK_GIVEN_1: float = 0.035
    COEF_WALK_GIVEN_2: float = 0.029
    COEF_SPEED_UNIT_CONV: float = 0.278  # коэф. для перевода из км/ч в м/с
    COEF_HEIGHT_UNIT_CONV: int = 100    # коэф. для перевода из см в м

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEF_WALK_GIVEN_1 * self.weight
                + ((self.get_mean_speed() * self.COEF_SPEED_UNIT_CONV) ** 2
                 / self.height * self.COEF_HEIGHT_UNIT_CONV)
                * self.COEF_WALK_GIVEN_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    COEF_SWIM_GIVEN_1: float = 1.1
    COEF_SWIM_GIVEN_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:

        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.lenght_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_SWIM_GIVEN_1)
                * self.COEF_SWIM_GIVEN_2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TYPES_OF_TRAINING: dict[str, type] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking
                                          }
    if workout_type not in TYPES_OF_TRAINING:
        raise Exception("Такой тренировки не существует")

    return TYPES_OF_TRAINING[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
    main(training)
