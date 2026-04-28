import matplotlib.pyplot as plt

data_points = []


class data_point:
    def __init__(self, date, amount):
        self.date = date
        self.amount = amount


while True:
    input_date = input("Enter day of year, 'q' for exit:")
    input_amount = input("Enter new amount:")

    print(input_date)
    if input_date == 'q':
        break

    data_points.append(data_point(int(input_date), int(input_amount)))

    plt.ylabel('Amount (£)')
    plt.xlabel('Day of year')

    plt.plot(
        [x.date for x in data_points],
        [x.amount for x in data_points])

plt.show()
