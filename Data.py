import json
import random

MENU_FILE = "menu.json" # You couldn't have expected me to write to JSON correctly without googling/using AI


def readInt(prompt):
    """Asks until the user enters a whole number (protection from non-numeric input)."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введіть число!")


# ---------------------------------------------------------------- Dishes

class Dish:
    category = "dish"

    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value.strip() == "":
            raise ValueError("Назва не може бути порожньою")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Ціна має бути додатною")
        self._price = value

    def describe(self):
        return f"{self.name} - {self.price} грн"

    def toDict(self):
        return {"type": self.category, "name": self.name, "price": self.price}


class MainCourse(Dish):
    category = "main"

    def __init__(self, name, price, weight_g=250):
        super().__init__(name, price)
        self.weight_g = weight_g

    def describe(self):
        return super().describe() + f" (головна страва, {self.weight_g} г)"

    def toDict(self):
        data = super().toDict()
        data["weight_g"] = self.weight_g
        return data


class Drink(Dish):
    category = "drink"

    def __init__(self, name, price, volume_ml=250, alcohol=False):
        super().__init__(name, price)
        self.volume_ml = volume_ml
        self.alcohol = alcohol

    def describe(self):
        kind = "алкогольний" if self.alcohol else "безалкогольний"
        return super().describe() + f" (напій, {self.volume_ml} мл, {kind})"

    def toDict(self):
        data = super().toDict()
        data["volume_ml"] = self.volume_ml
        data["alcohol"] = self.alcohol
        return data


class Dessert(Dish):
    category = "dessert"

    def __init__(self, name, price, is_vegan=False):
        super().__init__(name, price)
        self.is_vegan = is_vegan

    def describe(self):
        vegan = "веганський" if self.is_vegan else "не веганський"
        return super().describe() + f" (десерт, {vegan})"

    def toDict(self):
        data = super().toDict()
        data["is_vegan"] = self.is_vegan
        return data


def dishFromDict(data):
    """Builds the right Dish subclass from a dictionary (used when loading menu.json)."""
    if data["type"] == "main":
        return MainCourse(data["name"], data["price"], data["weight_g"])
    if data["type"] == "drink":
        return Drink(data["name"], data["price"], data["volume_ml"], data["alcohol"])
    if data["type"] == "dessert":
        return Dessert(data["name"], data["price"], data["is_vegan"])
    raise ValueError("Невідомий тип страви")


# ---------------------------------------------------------------- Table

class Table:
    def __init__(self, number, seats, isBusy=False):
        self.number = number
        self.seats = seats
        self.isBusy = isBusy

    @property
    def isBusy(self):
        return self._isBusy

    @isBusy.setter
    def isBusy(self, value):
        if type(value) != bool:
            raise ValueError("isBusy is a boolean!")
        self._isBusy = value

    def occupy(self):
        self.isBusy = True

    def free(self):
        self.isBusy = False

    def describe(self):
        state = "зайнятий" if self.isBusy else "вільний"
        return f"Столик №{self.number}, місць: {self.seats}, {state}"


# ---------------------------------------------------------------- Restaurant

class Restaurant:
    def __init__(self):
        self.dishes = [
            MainCourse("Борщ", 120, 350),
            Drink("Узвар", 40, 250),
            Dessert("Медовик", 90, False),
            MainCourse("Вареники", 110, 300),
            MainCourse("Деруни", 95, 250),
            Drink("Компот", 35, 250),
            Dessert("Сирники", 85, False),
            MainCourse("Солянка", 130, 350),
            Drink("Квас", 45, 330),
            Dessert("Фруктовий сорбет", 70, True),
        ]
        # sorted from the least seats to the most seats (for seatGuests)
        self.tables = [
            Table(3, 1),
            Table(1, 2),
            Table(2, 4),
            Table(5, 4),
            Table(4, 6),
            Table(6, 8),
        ]
        # shift data
        self.servedTables = 0
        self.income = 0
        self.ratings = []
        self.receiptCount = 0

        self.loadMenu()
        # bonus: dish of the day, -20%
        self.dishOfDay = random.choice(self.dishes)

    # ---------- menu

    def priceOf(self, dish):
        if dish is self.dishOfDay:
            return dish.price * 0.8
        return dish.price

    def showMenu(self, dishes=None):
        if dishes is None:
            dishes = self.dishes
        if len(dishes) == 0:
            print("Нічого не знайдено")
            return
        for number, dish in enumerate(dishes, 1):
            note = ""
            if dish is self.dishOfDay:
                note = f"  * СТРАВА ДНЯ -20% = {self.priceOf(dish):.2f} грн"
            print(number, dish.describe() + note)

    def addDish(self):
        while True:
            try:
                kind = input("Тип (1 - головна, 2 - напій, 3 - десерт): ")
                if kind not in ("1", "2", "3"):
                    raise ValueError("Оберіть 1, 2 або 3")
                name = input("Назва страви: ")
                price = int(input("Ціна: "))
                if kind == "1":
                    dish = MainCourse(name, price, int(input("Вага (г): ")))
                elif kind == "2":
                    volume = int(input("Об'єм (мл): "))
                    alcohol = input("Алкогольний? (Y/N): ").upper() == "Y"
                    dish = Drink(name, price, volume, alcohol)
                else:
                    vegan = input("Веганський? (Y/N): ").upper() == "Y"
                    dish = Dessert(name, price, vegan)
                break
            except ValueError as error:
                print("Помилка введення:", error)
        self.dishes.append(dish)
        print("Страву додано:", dish.describe())

    def filterMenu(self, mode):
        if mode == 1:
            return [d for d in self.dishes if isinstance(d, Dessert) and d.is_vegan]
        if mode == 2:
            return [d for d in self.dishes if isinstance(d, Drink) and not d.alcohol]
        return []

    def saveMenu(self):
        try:
            with open(MENU_FILE, "w", encoding="utf-8") as file:
                json.dump([d.toDict() for d in self.dishes], file,
                          ensure_ascii=False, indent=2)
        except OSError:
            print("Не вдалося зберегти меню")

    def loadMenu(self):
        try:
            with open(MENU_FILE, "r", encoding="utf-8") as file:
                loaded = [dishFromDict(item) for item in json.load(file)]
        except FileNotFoundError:
            return  # no file yet - keep the default menu
        except (ValueError, KeyError, TypeError):
            print("Файл menu.json пошкоджений, використано стандартне меню")
            return
        if len(loaded) > 0:
            self.dishes = loaded

    # ---------- tables

    def showTables(self):
        for table in self.tables:
            print(table.describe())

    def seatGuests(self, guests):
        for table in self.tables:
            if table.seats >= guests and not table.isBusy:
                table.occupy()
                return table
        return None

    def chooseBusyTable(self):
        busy = [t for t in self.tables if t.isBusy]
        if len(busy) == 0:
            print("Немає зайнятих столиків")
            return None
        for table in busy:
            print(table.describe())
        number = readInt("Номер столика: ")
        for table in busy:
            if table.number == number:
                return table
        print("Такого зайнятого столика немає")
        return None

    def freeTable(self, table):
        table.free()

    # ---------- orders

    def takeOrder(self, table):
        order = []
        self.showMenu()
        while True:
            number = readInt("Номер страви (0 - завершити): ")
            if number == 0:
                return order
            if 1 <= number <= len(self.dishes):
                order.append(self.dishes[number - 1])
            else:
                print("Такої страви немає")

    def calcTotal(self, order):
        total = 0
        for dish in order:
            total += self.priceOf(dish)
        if total > 2000:
            total = total * 0.9
        elif total > 1000:
            total = total * 0.95
        return total

    def makeReceipt(self, table, order):
        lines = [f"===== ЧЕК, столик №{table.number} ====="]
        subtotal = 0
        for dish in order:
            price = self.priceOf(dish)
            star = " *" if dish is self.dishOfDay else ""
            lines.append(f"{dish.name}{star} - {price:.2f} грн")
            subtotal += price

        # bonus: every 5th table gets a free dessert
        if (self.servedTables + 1) % 5 == 0:
            for dish in self.dishes:
                if isinstance(dish, Dessert):
                    lines.append(f"{dish.name} (VIP-подарунок) - 0.00 грн")
                    break

        total = self.calcTotal(order)
        lines.append(f"Сума: {subtotal:.2f} грн")
        if subtotal - total > 0.001:
            lines.append(f"Знижка: -{subtotal - total:.2f} грн")
        lines.append(f"До сплати: {total:.2f} грн")
        if self.dishOfDay in order:
            lines.append("* - страва дня зі знижкою 20%")
        return "\n".join(lines), total

    def closeOrder(self, table, order):
        text, total = self.makeReceipt(table, order)
        print(text)

        self.receiptCount += 1
        try:
            with open(f"check_{self.receiptCount}.txt", "w", encoding="utf-8") as file:
                file.write(text)
        except OSError:
            print("Не вдалося зберегти чек у файл")

        self.servedTables += 1
        self.income += total
        self.freeTable(table)

        rating = random.randint(1, 5)
        self.ratings.append(rating)
        print(f"Відгук гостя: {rating}/5")

    # ---------- shift

    def showShiftInfo(self):
        print("Обслужено столиків:", self.servedTables)
        print(f"Загальна виручка: {self.income:.2f} грн")
        if len(self.ratings) > 0:
            print(f"Середня оцінка: {sum(self.ratings) / len(self.ratings):.1f}/5")
        else:
            print("Відгуків ще немає")