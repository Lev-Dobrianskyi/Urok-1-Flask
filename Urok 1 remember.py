import Data as data

restaurant = data.Restaurant()
print("Страва дня:", restaurant.dishOfDay.name, "(-20%)")

endShift = False

while endShift == False:
    try:
        choice = int(input("===== РЕСТОРАН «Смакота» =====\n1. Показати меню\n2. Додати страву\n3. Показати столики\n4. Посадити гостей\n5. Прийняти замовлення\n6. Закрити зміну\n7. Фільтр меню\n0. Вихід\n"))
    except ValueError:
        print("Введіть число від 0 до 7!")
        continue

    if choice == 1:
        restaurant.showMenu()
    elif choice == 2:
        restaurant.addDish()
        restaurant.saveMenu()
    elif choice == 3:
        restaurant.showTables()
    elif choice == 4:
        guests = data.readInt("Кількість гостей: ")
        if guests <= 0:
            print("Кількість гостей має бути більше 0")
        else:
            table = restaurant.seatGuests(guests)
            if table is None:
                print("Місць немає")
            else:
                print(f"Гостей посаджено за столик №{table.number}")
    elif choice == 5:
        table = restaurant.chooseBusyTable()
        if table is not None:
            order = restaurant.takeOrder(table)
            if len(order) == 0:
                print("Замовлення порожнє")
            else:
                restaurant.closeOrder(table, order)
    elif choice == 6:
        restaurant.showShiftInfo()
        if input("Ви впевнені, що хочете завершити зміну? (Y/N) ").upper() == "Y":
            endShift = True
    elif choice == 7:
        mode = data.readInt("1 - веганські десерти, 2 - безалкогольні напої: ")
        restaurant.showMenu(restaurant.filterMenu(mode))
    elif choice == 0:
        endShift = True
    else:
        print("Невірне значення1")

restaurant.saveMenu()
print("Гарного вечора!")