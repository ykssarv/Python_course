"""Train."""


class Train:
    """Something."""

    def __init__(self, passengers: list, carriages: int, seats_in_carriage: int):
        """Something."""
        self.carriages = carriages
        self.seats_in_carriage = seats_in_carriage
        self.passengers = passengers

    @property
    def passengers(self) -> list:
        """Something."""
        return self._passengers

    @property
    def carriages(self) -> int:
        """Something."""
        return self._carriages

    @property
    def seats_in_carriage(self) -> int:
        """Something."""
        return self._seats_in_carriage

    def get_seats_in_train(self) -> int:
        """Something."""
        return self.seats_in_carriage * self.carriages

    def get_number_of_passengers(self) -> int:
        """Something."""
        return len(self.passengers)

    def get_passengers_in_carriages(self) -> dict:
        """Something."""
        passengers_in_a_carriage = {}
        for i in range(1, self._carriages + 1):
            passengers_in_a_carriage[str(i)] = []
        for passenger in self.passengers:
            carriage = passenger.seat.split("-")[0]
            passengers_in_a_carriage[carriage].append(passenger.__dict__())
            passengers_in_a_carriage[carriage][-1]['seat'] = passengers_in_a_carriage[carriage][-1]['seat'].split("-")[1]
        return passengers_in_a_carriage

    @passengers.setter
    def passengers(self, value_list: list):
        """Something."""
        self._passengers = []
        for passenger in value_list:
            seat = passenger.seat
            seat = seat.split("-")
            if int(seat[0]) <= self.carriages and int(seat[1]) <= self.seats_in_carriage:
                self._passengers.append(passenger)

    @carriages.setter
    def carriages(self, value: int):
        """Something."""
        self._carriages = value

    @seats_in_carriage.setter
    def seats_in_carriage(self, value: int):
        """Something."""
        self._seats_in_carriage = value


class Passenger:
    """Something."""

    def __init__(self, passenger_id: str, seat: str):
        """Something."""
        self.passenger_id = passenger_id
        self.seat = seat

    def __dict__(self):
        """Something."""
        passenger_dict = {"id": self.passenger_id, "seat": self.seat}
        return passenger_dict


if __name__ == '__main__':
    p_1 = Passenger('123', '1-9')
    p_2 = Passenger('321', '2-11')
    p_3 = Passenger('456', '4-5')
    t = Train([p_1, p_2, p_3], 3, 10)
    print(t.passengers)
    print(t.get_passengers_in_carriages())
    print(p_1.__dict__())
