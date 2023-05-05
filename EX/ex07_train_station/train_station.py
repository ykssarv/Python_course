"""Train Station."""


class Passenger:
    """Something."""

    def __init__(self, passenger_id: str, seat: str):
        """Something."""
        self.passenger_id = passenger_id
        self.seat = seat


class Train:
    """Something."""

    def __init__(self, train_id: str, carriages: int, seats_in_carriage: int):
        """Something."""
        self.train_id = train_id
        self.carriages = carriages
        self.seats_in_carriage = seats_in_carriage
        self.passengers = []

    @property
    def carriages(self) -> int:
        """Something."""
        return self._carriages

    @property
    def train_id(self) -> str:
        """Something."""
        return self._train_id

    @property
    def seats_in_carriage(self) -> int:
        """Something."""
        return self._seats_in_carriage

    def get_seats_in_train(self) -> int:
        """Something."""
        return self.carriages * self.seats_in_carriage

    def get_number_of_passengers(self) -> int:
        """Something."""
        return len(self.passengers)

    def get_passengers_in_carriages(self) -> dict:
        """Something."""
        passengers_in_a_carriage = {}
        for i in range(1, self._carriages + 1):
            passengers_in_a_carriage[str(i)] = []
        for passenger in self.passengers:
            carriage = passenger.seat.split("-")[1]
            passengers_in_a_carriage[carriage].append(passenger)
        return passengers_in_a_carriage

    @train_id.setter
    def train_id(self, value: str):
        """Something."""
        self._train_id = value

    @carriages.setter
    def carriages(self, value: int):
        """Something."""
        self._carriages = value

    @seats_in_carriage.setter
    def seats_in_carriage(self, value: int):
        """Something."""
        self._seats_in_carriage = value

    def add_passenger(self, passenger: Passenger):
        """Something."""
        if passenger.seat.split("-")[0] == self.train_id:
            if 0 < int(passenger.seat.split("-")[1]) <= self.carriages:
                if 0 < int(passenger.seat.split("-")[2]) <= self.seats_in_carriage:
                    for current in self.passengers:
                        if int(current.seat.split("-")[1]) == int(passenger.seat.split("-")[1]):
                            if int(current.seat.split("-")[2]) == int(passenger.seat.split("-")[2]):
                                return False
                    self.passengers.append(passenger)
                    return True
        return False

    def get_train_overview(self):
        """Something."""
        train_overview = {"train_id": self.train_id,
                          "carriages": self.carriages,
                          "seats": (str(len(self.passengers)) + "/" + str(self.seats_in_carriage * self._carriages))}
        return train_overview


class TrainStation:
    """Something."""

    def __init__(self, trains: list, passengers: list):
        """Something."""
        self.trains = trains
        self.passengers = passengers

    def get_station_overview(self) -> list:
        """Something."""
        station_overview = []
        for train in self.trains:
            station_overview.append(train.get_train_overview())
        return station_overview

    def get_number_of_passengers(self):
        """Something."""
        return len(self.passengers)

    @property
    def passengers(self):
        """Something."""
        return self._passengers

    @passengers.setter
    def passengers(self, value_list: list):
        """Something."""
        self._passengers = []
        for passenger in value_list:
            for train in self.trains:
                if train.add_passenger(passenger):
                    self._passengers.append(passenger)

    @property
    def trains(self):
        """Something."""
        return self._trains

    @trains.setter
    def trains(self, value_list: list):
        """Something."""
        self._trains = value_list
