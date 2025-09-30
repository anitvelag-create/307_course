import tkinter as tk
from tkinter import ttk, messagebox


class CarWashApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚗 Автомойка Премиум")
        self.geometry("800x750")
        self.configure(bg='#f0f0f0')

        # Настройка стилей
        self.setup_styles()

        # Изначальные данные
        self.service_list = [("Мойка кузова", 800), ("Вакуумирование салона", 1200)]
        self.date_list = ["2024-06-01", "2024-06-02", "2024-06-03"]
        self.car_list = ["BMW X5", "Audi A4"]
        self.client_list = ["Иван Иванов", "Петр Петров"]
        self.staff_list = ["Мария", "Алексей"]

        self.records = []

        # Создаем основной контейнер с прокруткой
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Заголовок
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(header_frame, text="🚗 Автомойка Премиум",
                  font=('Arial', 16, 'bold'),
                  foreground='#2c3e50').pack(pady=5)

        ttk.Label(header_frame, text="Система управления записями",
                  font=('Arial', 10),
                  foreground='#7f8c8d').pack()

        self.notebook = ttk.Notebook(self.main_frame, height=350)
        self.notebook.pack(fill='both', expand=True, pady=(0, 10))

        self.create_service_tab()
        self.create_date_tab()
        self.create_car_tab()
        self.create_client_tab()
        self.create_staff_tab()

        self.create_records_section()
        self.create_records_display()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Настройка цветовой схемы
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 9))
        style.configure('TButton', font=('Arial', 9))
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', font=('Arial', 9, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'), foreground='#2c3e50')
        style.configure('Success.TButton', background='#27ae60', foreground='white')

    def create_service_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎯 Услуги")

        # Основной контейнер с отступами
        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True, padx=15, pady=15)

        ttk.Label(container, text="Управление услугами автомойки",
                  style='Header.TLabel').grid(column=0, row=0, columnspan=2, pady=(0, 15), sticky='w')

        ttk.Label(container, text="Наименование услуги:").grid(column=0, row=1, padx=5, pady=8, sticky='w')
        ttk.Label(container, text="Цена услуги (руб.):").grid(column=0, row=2, padx=5, pady=8, sticky='w')

        self.service_name_cb = ttk.Combobox(container, values=[name for name, _ in self.service_list],
                                            font=('Arial', 9), width=25)
        self.service_name_cb.grid(column=1, row=1, padx=5, pady=8, sticky='w')

        self.service_price_entry = ttk.Entry(container, font=('Arial', 9), width=15)
        self.service_price_entry.grid(column=1, row=2, padx=5, pady=8, sticky='w')

        add_btn = ttk.Button(container, text="💾 Добавить / Обновить",
                             command=self.add_service, width=20)
        add_btn.grid(column=1, row=3, padx=5, pady=12, sticky='w')

        # Список услуг в рамке
        list_frame = ttk.LabelFrame(container, text="Список услуг")
        list_frame.grid(column=0, row=4, columnspan=2, padx=5, pady=10, sticky='we')

        self.service_listbox = tk.Listbox(list_frame, height=8, width=60,
                                          font=('Arial', 9), bg='white',
                                          relief='solid', bd=1)
        self.service_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.update_service_listbox()

    def add_service(self):
        name = self.service_name_cb.get().strip()
        price_text = self.service_price_entry.get().strip()

        if not name:
            messagebox.showwarning("Ошибка", "Введите название услуги")
            return
        if not price_text.isdigit():
            messagebox.showwarning("Ошибка", "Цена должна быть числом")
            return

        price = int(price_text)
        found = False
        for i, (n, p) in enumerate(self.service_list):
            if n == name:
                self.service_list[i] = (name, price)
                found = True
                break
        if not found:
            self.service_list.append((name, price))

        self.update_service_listbox()
        self.service_name_cb.set('')
        self.service_price_entry.delete(0, tk.END)
        self.update_records_comboboxes()
        messagebox.showinfo("Успех", f"Услуга '{name}' успешно добавлена!")

    def update_service_listbox(self):
        self.service_name_cb['values'] = [name for name, _ in self.service_list]
        self.service_listbox.delete(0, tk.END)
        for name, price in self.service_list:
            self.service_listbox.insert(tk.END, f"🎯 {name} - {price} руб.")

    def create_date_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📅 Даты")

        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True, padx=15, pady=15)

        ttk.Label(container, text="Управление датами записи",
                  style='Header.TLabel').grid(column=0, row=0, columnspan=2, pady=(0, 15), sticky='w')

        ttk.Label(container, text="Дата (YYYY-MM-DD):").grid(column=0, row=1, padx=5, pady=8, sticky='w')

        self.date_cb = ttk.Combobox(container, values=self.date_list,
                                    font=('Arial', 9), width=20)
        self.date_cb.grid(column=1, row=1, padx=5, pady=8, sticky='w')

        add_btn = ttk.Button(container, text="📅 Добавить дату",
                             command=self.add_date, width=20)
        add_btn.grid(column=1, row=2, padx=5, pady=12, sticky='w')

        list_frame = ttk.LabelFrame(container, text="Доступные даты")
        list_frame.grid(column=0, row=3, columnspan=2, padx=5, pady=10, sticky='we')

        self.date_listbox = tk.Listbox(list_frame, height=8, width=60,
                                       font=('Arial', 9), bg='white')
        self.date_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.update_date_listbox()

    def add_date(self):
        date = self.date_cb.get().strip()
        if not date:
            messagebox.showwarning("Ошибка", "Введите дату")
            return
        if date not in self.date_list:
            self.date_list.append(date)
            self.update_date_listbox()
            messagebox.showinfo("Успех", f"Дата {date} добавлена!")
        else:
            messagebox.showinfo("Информация", "Такая дата уже есть")
        self.date_cb.set('')
        self.update_records_comboboxes()

    def update_date_listbox(self):
        self.date_cb['values'] = self.date_list
        self.date_listbox.delete(0, tk.END)
        for date in sorted(self.date_list):
            self.date_listbox.insert(tk.END, f"📅 {date}")

    def create_car_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🚗 Машины")

        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True, padx=15, pady=15)

        ttk.Label(container, text="Управление автомобилями",
                  style='Header.TLabel').grid(column=0, row=0, columnspan=2, pady=(0, 15), sticky='w')

        ttk.Label(container, text="Марка и модель:").grid(column=0, row=1, padx=5, pady=8, sticky='w')

        self.car_cb = ttk.Combobox(container, values=self.car_list,
                                   font=('Arial', 9), width=25)
        self.car_cb.grid(column=1, row=1, padx=5, pady=8, sticky='w')

        add_btn = ttk.Button(container, text="🚗 Добавить машину",
                             command=self.add_car, width=20)
        add_btn.grid(column=1, row=2, padx=5, pady=12, sticky='w')

        list_frame = ttk.LabelFrame(container, text="Зарегистрированные автомобили")
        list_frame.grid(column=0, row=3, columnspan=2, padx=5, pady=10, sticky='we')

        self.car_listbox = tk.Listbox(list_frame, height=8, width=60,
                                      font=('Arial', 9), bg='white')
        self.car_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.update_car_listbox()

    def add_car(self):
        car = self.car_cb.get().strip()
        if not car:
            messagebox.showwarning("Ошибка", "Введите марку и модель машины")
            return
        if car not in self.car_list:
            self.car_list.append(car)
            self.update_car_listbox()
            messagebox.showinfo("Успех", f"Автомобиль {car} добавлен!")
        else:
            messagebox.showinfo("Информация", "Такая машина уже есть")
        self.car_cb.set('')
        self.update_records_comboboxes()

    def update_car_listbox(self):
        self.car_cb['values'] = self.car_list
        self.car_listbox.delete(0, tk.END)
        for car in self.car_list:
            self.car_listbox.insert(tk.END, f"🚗 {car}")

    def create_client_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👤 Клиенты")

        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True, padx=15, pady=15)

        ttk.Label(container, text="Управление клиентами",
                  style='Header.TLabel').grid(column=0, row=0, columnspan=2, pady=(0, 15), sticky='w')

        ttk.Label(container, text="ФИО клиента:").grid(column=0, row=1, padx=5, pady=8, sticky='w')

        self.client_cb = ttk.Combobox(container, values=self.client_list,
                                      font=('Arial', 9), width=25)
        self.client_cb.grid(column=1, row=1, padx=5, pady=8, sticky='w')

        add_btn = ttk.Button(container, text="👤 Добавить клиента",
                             command=self.add_client, width=20)
        add_btn.grid(column=1, row=2, padx=5, pady=12, sticky='w')

        list_frame = ttk.LabelFrame(container, text="Зарегистрированные клиенты")
        list_frame.grid(column=0, row=3, columnspan=2, padx=5, pady=10, sticky='we')

        self.client_listbox = tk.Listbox(list_frame, height=8, width=60,
                                         font=('Arial', 9), bg='white')
        self.client_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.update_client_listbox()

    def add_client(self):
        client = self.client_cb.get().strip()
        if not client:
            messagebox.showwarning("Ошибка", "Введите ФИО клиента")
            return
        if client not in self.client_list:
            self.client_list.append(client)
            self.update_client_listbox()
            messagebox.showinfo("Успех", f"Клиент {client} добавлен!")
        else:
            messagebox.showinfo("Информация", "Такой клиент уже есть")
        self.client_cb.set('')
        self.update_records_comboboxes()

    def update_client_listbox(self):
        self.client_cb['values'] = self.client_list
        self.client_listbox.delete(0, tk.END)
        for client in self.client_list:
            self.client_listbox.insert(tk.END, f"👤 {client}")

    def create_staff_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👨‍💼 Сотрудники")

        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True, padx=15, pady=15)

        ttk.Label(container, text="Управление сотрудниками",
                  style='Header.TLabel').grid(column=0, row=0, columnspan=2, pady=(0, 15), sticky='w')

        ttk.Label(container, text="ФИО сотрудника:").grid(column=0, row=1, padx=5, pady=8, sticky='w')

        self.staff_cb = ttk.Combobox(container, values=self.staff_list,
                                     font=('Arial', 9), width=25)
        self.staff_cb.grid(column=1, row=1, padx=5, pady=8, sticky='w')

        add_btn = ttk.Button(container, text="👨‍💼 Добавить сотрудника",
                             command=self.add_staff, width=20)
        add_btn.grid(column=1, row=2, padx=5, pady=12, sticky='w')

        list_frame = ttk.LabelFrame(container, text="Сотрудники автомойки")
        list_frame.grid(column=0, row=3, columnspan=2, padx=5, pady=10, sticky='we')

        self.staff_listbox = tk.Listbox(list_frame, height=8, width=60,
                                        font=('Arial', 9), bg='white')
        self.staff_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.update_staff_listbox()

    def add_staff(self):
        staff = self.staff_cb.get().strip()
        if not staff:
            messagebox.showwarning("Ошибка", "Введите ФИО сотрудника")
            return
        if staff not in self.staff_list:
            self.staff_list.append(staff)
            self.update_staff_listbox()
            messagebox.showinfo("Успех", f"Сотрудник {staff} добавлен!")
        else:
            messagebox.showinfo("Информация", "Такой сотрудник уже есть")
        self.staff_cb.set('')
        self.update_records_comboboxes()

    def update_staff_listbox(self):
        self.staff_cb['values'] = self.staff_list
        self.staff_listbox.delete(0, tk.END)
        for staff in self.staff_list:
            self.staff_listbox.insert(tk.END, f"👨‍💼 {staff}")

    def create_records_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="➕ Новая запись на услугу")
        frame.pack(fill='x', pady=(0, 10))

        container = ttk.Frame(frame)
        container.pack(fill='x', padx=10, pady=10)

        # Заголовки
        headers = ["Услуга:", "Дата:", "Машина:", "Клиент:", "Сотрудник:"]
        for i, header in enumerate(headers):
            ttk.Label(container, text=header, font=('Arial', 9, 'bold')).grid(
                column=i, row=0, padx=3, pady=5, sticky='w')

        # Комбобоксы
        self.record_service_cb = ttk.Combobox(container, font=('Arial', 9), width=15)
        self.record_service_cb.grid(column=0, row=1, padx=3, pady=5, sticky='we')

        self.record_date_cb = ttk.Combobox(container, font=('Arial', 9), width=12)
        self.record_date_cb.grid(column=1, row=1, padx=3, pady=5, sticky='we')

        self.record_car_cb = ttk.Combobox(container, font=('Arial', 9), width=15)
        self.record_car_cb.grid(column=2, row=1, padx=3, pady=5, sticky='we')

        self.record_client_cb = ttk.Combobox(container, font=('Arial', 9), width=15)
        self.record_client_cb.grid(column=3, row=1, padx=3, pady=5, sticky='we')

        self.record_staff_cb = ttk.Combobox(container, font=('Arial', 9), width=15)
        self.record_staff_cb.grid(column=4, row=1, padx=3, pady=5, sticky='we')

        add_record_btn = ttk.Button(container, text="✅ Создать запись",
                                    command=self.add_record, width=15)
        add_record_btn.grid(column=4, row=2, padx=3, pady=10, sticky='e')

        self.update_records_comboboxes()

    def update_records_comboboxes(self):
        self.record_service_cb['values'] = [name for name, _ in self.service_list]
        self.record_date_cb['values'] = sorted(self.date_list)
        self.record_car_cb['values'] = self.car_list
        self.record_client_cb['values'] = self.client_list
        self.record_staff_cb['values'] = self.staff_list

    def add_record(self):
        service = self.record_service_cb.get().strip()
        date = self.record_date_cb.get().strip()
        car = self.record_car_cb.get().strip()
        client = self.record_client_cb.get().strip()
        staff = self.record_staff_cb.get().strip()

        if not all([service, date, car, client, staff]):
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены")
            return

        price = 0
        for name, p in self.service_list:
            if name == service:
                price = p
                break

        record = {
            'service': service,
            'date': date,
            'car': car,
            'client': client,
            'staff': staff,
            'price': price
        }
        self.records.append(record)
        self.update_records_display()

        self.record_service_cb.set('')
        self.record_date_cb.set('')
        self.record_car_cb.set('')
        self.record_client_cb.set('')
        self.record_staff_cb.set('')

        messagebox.showinfo("Успех", "✅ Запись добавлена успешно!")

    def create_records_display(self):
        frame = ttk.LabelFrame(self.main_frame, text="📋 Текущие записи")
        frame.pack(fill='both', expand=True)

        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ("Услуга", "Цена", "Дата", "Машина", "Клиент", "Сотрудник")

        # Создаем Treeview с полосой прокрутки
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill='both', expand=True)

        self.records_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

        # Настраиваем столбцы
        column_widths = [120, 80, 100, 120, 120, 100]
        for col, width in zip(columns, column_widths):
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=width, anchor='center')

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)

        self.records_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Статистика
        stats_frame = ttk.Frame(container)
        stats_frame.pack(fill='x', pady=(10, 0))

        self.stats_label = ttk.Label(stats_frame, text="Всего записей: 0",
                                     font=('Arial', 9, 'bold'), foreground='#2c3e50')
        self.stats_label.pack(side='left')

    def update_records_display(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        for record in self.records:
            self.records_tree.insert("", "end", values=(
                record['service'],
                f"{record['price']} руб.",
                record['date'],
                record['car'],
                record['client'],
                record['staff']
            ))

        self.stats_label.config(text=f"Всего записей: {len(self.records)}")


if __name__ == "__main__":
    app = CarWashApp()
    app.mainloop()