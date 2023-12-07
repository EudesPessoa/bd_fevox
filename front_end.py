import tkinter
from tkinter import ttk
from time import sleep
from PIL import Image
import customtkinter
from tkinter import messagebox
from bd_user import Database_User
from bd_brand import Database_Brand
from bd_model import Database_Model
from bd_product import Database_Product
from bd_color import Database_Color
from bd_stock import Database_Stock
from bd_supplier import Database_Supplier
from bd_invoice import Database_Invoice
from bd_provider import Database_Provider
from bd_costs import Database_Costs
from bd_sales import Database_Sales
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from confirm import (Confirm_if_email,
                 Confirm_if_name_empty,
                 Confirm_if_pass_empty,
                 )

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

verde_claro = '#2fa572'

class App(customtkinter.CTk):


    def Sort_Treeview(self, tree, col, descending):
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
        tree.heading(col, command=lambda: self.Sort_Treeview(tree, col, not descending))

        # ****************  DEFLOGIN  ************************

    def Show_Pass_Login(self):
        if self.show_pass_checkbox.get() == 1:
            self.pass_entry_login.configure(show="")
        else:
            self.pass_entry_login.configure(show="*")


    def Confirm_login(self):
        if_email = Confirm_if_email(
            email=self.user_entry_login.get().upper()
            )
        self.user_entry_login.configure(border_color=if_email)
        if if_email == 'green':
            pass_login = self.pass_entry_login.get()
            confirm_pass_login = Confirm_if_pass_empty(
                senha= pass_login
                )
            self.pass_entry_login.configure(
                border_color=confirm_pass_login
                )
            if confirm_pass_login == 'green':
                connect_db = Database_User()
                check_email_login = connect_db.Search_user(
                    email=self.user_entry_login.get().upper(),
                    pass_user=self.pass_entry_login.get(),
                )
                if check_email_login[0] == 'sim':
                    sleep(1)
                    next_pag = self.Window_App(
                        janela=self.window_login,
                        user=check_email_login[1]
                        )
                else:
                    self.user_entry_login.configure(
                        border_color='red'
                        )
                    self.pass_entry_login.configure(
                        border_color='red'
                        )
                    self.text_user_login.configure(
                        text='Acesso Negado!!!!'
                        )
            elif confirm_pass_login == 'red':
                self.pass_entry_login.configure(
                    border_color=confirm_pass_login
                    )
        else:
            pass

        # ****************  DEFLOGIN  ************************


        # ****************  DEFREGISTER  ************************

    def Show_Pass_Register(self):
        if self.show_pass_checkbox_register.get() == 1:
            self.pass_entry_register.configure(show="")
        else:
            self.pass_entry_register.configure(show="*")
            

    def Register_User_New(self):
        register_name = Confirm_if_name_empty(
            name=self.name_entry_register.get().upper()
            )
        self.name_entry_register.configure(
            border_color=register_name
            )
        if register_name == 'green':

            register_user = Confirm_if_email(
                email=self.user_entry_register.get().upper()
                )
            self.user_entry_register.configure(
                border_color=register_user
                )
            if register_user == 'green':
                pass_user = self.pass_entry_register.get()
                confirm_pass_register = Confirm_if_pass_empty(
                    senha= pass_user
                    )
                self.pass_entry_register.configure(
                    border_color=confirm_pass_register
                    )
                if confirm_pass_register == 'green':
                    connect_db = Database_User()
                    # connect_db.Connect()
                    check_email_register = connect_db.Search_user(
                        email=self.user_entry_register.get().upper(),
                        pass_user=None
                        )
                    if check_email_register == 'existe':
                        self.name_entry_register.configure(
                            border_color='red'
                            )
                        self.user_entry_register.configure(
                            border_color='red'
                            )
                        self.pass_entry_register.configure(
                            border_color='red'
                            )
                        self.text_user_register.configure(
                            text='Usuário já existe!!!!'
                            )
                    else:
                        connect_db.Create_user_table()
                        connect_db.Insert_user(
                            name=self.name_entry_register.get().upper(),
                            email=self.user_entry_register.get().upper(),
                            pass_user=self.pass_entry_register.get()
                        )
                        sleep(1)
                        next_pag = self.Window_App(
                            janela=self.window_register_user,
                            user=self.name_entry_register.get().upper(),
                            )
                elif confirm_pass_register == 'red':
                    self.pass_entry_register.configure(
                        border_color=confirm_pass_register
                        )
            else:
                pass
        else:
            pass

        # ****************  DEFREGISTER  ************************


        # ****************  DEFMARCAS  ************************

    def Display_Data_Brand(self, event):
        selected_item_display = self.table_brands.focus()
        # print(f'Selected_item : {selected_item}')
        if selected_item_display:
            row = self.table_brands.item(selected_item_display)['values']
            self.Clear_Entry_Brand()
            self.id_entry_brand.insert(0,row[2])
        else:
            pass

    def Add_to_Treeview_Brand(self, ):
        connect_db = Database_Brand()

        products = connect_db.Fetch_Brand()
        self.table_brands.delete(*self.table_brands.get_children())
        for product in products:
            self.table_brands.insert('', 'end', values=product)

        self.Sort_Treeview(self.table_brands, 'MARCA', False)

    def Clear_Entry_Brand(self, *clicked):
        if clicked:
            self.table_brands.selection_remove(self.table_brands.focus())
            self.table_brands.focus('')
        self.id_entry_brand.delete(0, 'end')


    def Delete_Brand_Search_Model(self, ):
        connect_db = Database_Model()
        models = connect_db.Fetch_Model()
        models_name_id = []
        for model in models:
            models_name_id.append(f'{model[2]}')
        return models_name_id
    

    def Delete_Brand(self, ):
        model_config = self.Delete_Brand_Search_Model()

        connect_db = Database_Brand()
        selected_item = self.table_brands.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha uma MARCA para EXCLUIR.')
        else:
            item = self.table_brands.focus()
            if item:
                row = self.table_brands.item(item)['values']
            id_brand = row[0]
            name_brand = self.id_entry_brand.get()
            delete = False
            for x in model_config:
                if int(x) == int(id_brand):
                    messagebox.showerror('Error', 'MARCA VINCULADA A MODELOS.')
                    delete = True
                    break
                elif int(x) != int(id_brand):
                    pass
            if delete == False:

                connect_db.Delete_Brand(
                    name_brand=name_brand,
                    id=id_brand
                    )
                self.Add_to_Treeview_Brand()
                self.Clear_Entry_Brand()
                messagebox.showinfo('Sucesso', 'MARCA EXCLUÍDA.')


    def Update_Brand(self, ):
        connect_db = Database_Brand()
        user = self.name_user_current
        selected_item = self.table_brands.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha uma MARCA para atualizar.')
        else:
            item = self.table_brands.focus()
            if item:
                row = self.table_brands.item(item)['values']
            id_brand = row[0]
            name_brand = self.id_entry_brand.get().upper()
            check_name_brand = connect_db.Search_Brand_Name(
                brand_name=name_brand,
                )
            if check_name_brand == 'sim':
                sleep(1)
                messagebox.showerror('Error', 'MARCA já REGISTRADA.')
                self.Add_to_Treeview_Brand()
                self.Clear_Entry_Brand()
            else:
                connect_db.Update_Brand(
                    new_name_brand=name_brand,
                    id=id_brand,
                    name_user=user.upper()
                    )
                self.Add_to_Treeview_Brand()
                self.Clear_Entry_Brand()
                messagebox.showinfo('Sucesso', 'MARCA ATUALIZADA.')
                self.Window_Product_Registration()


    def Insert_Brand(self, ):
        connect_db = Database_Brand()
        # connect_db.Connect()
        connect_db.Create_Brands_Table()
        user = self.name_user_current

        name_brand = self.id_entry_brand.get().upper()

        if not (name_brand):
            messagebox.showerror('Error', 'Digitar uma Marca.')
        else:
            check_name_brand = connect_db.Search_Brand_Name(
                brand_name=name_brand,
                )
            if check_name_brand == 'sim':
                sleep(1)
                self.id_entry_brand.configure(
                    border_color='red',
                    fg_color='red'
                    )
                messagebox.showerror('Error', 'MARCA já REGISTRADA.')
            else:
                connect_db.Insert_Brands(
                    user_name=user,
                    brand_name=name_brand
                    )
                messagebox.showinfo('Sucesso', 'Marca Registrada com SUCESSO.')
                self.Add_to_Treeview_Brand()
                self.Clear_Entry_Brand()
                self.Window_Product_Registration()


        # ****************  DEFMARCAS  ************************


        # ****************  DEFMODELOS  ************************


    def Display_Data_Model(self, event):
        selected_item_display = self.table_models.focus()
        if selected_item_display:
            row = self.table_models.item(selected_item_display)['values']
            self.id_entry_model.delete(0, 'end')
            self.id_entry_model.insert(0,row[3])
            self.optionmenu_model.set(value=row[2])
            self.optionmenu_model.configure(state='disabled')
        else:
            pass


    def Search_Model_Brand(self):
        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()

        brands_name_id = []
        for brand in brands:
            brands_name_id.append(f'{brand[0]}: {brand[2]}')
        return brands_name_id


    def Add_to_Treeview_Model(self, ):
        brands_names = self.Search_Model_Brand()
        item = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item.append(k)

        connect_db = Database_Model()
        products = connect_db.Fetch_Model()
        self.table_models.delete(*self.table_models.get_children())

        brand_choice = self.optionmenu_model.get()

        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                us=product[1]
                bra=product[2]
                mod=product[3]
                bran=''
                for num, namebrand in item:
                    if int(num) == bra:
                        bran=namebrand
                    else:
                        pass

                self.table_models.insert('', 'end', values=[id_p,us,bran,mod])
            self.Sort_Treeview(self.table_models, 'MARCA', False)

        else:
            for product in products:
                id_p=product[0]
                us=product[1]
                bra=product[2]
                mod=product[3]
                bran=''
                for num, namebrand in item:
                    if int(num) == bra:
                        bran=namebrand
                        if bran == brand_choice:
                            self.table_models.insert('', 'end', values=[id_p,us,bran,mod])
                    else:
                        pass

            self.Sort_Treeview(self.table_models, 'MODELO', False)


    def Clear_Entry_Model(self, *clicked):
        if clicked:
            self.table_models.selection_remove(self.table_models.focus())
            self.table_models.focus('')
        self.id_entry_model.delete(0, 'end')
        self.optionmenu_model.configure(state='normal')
        self.optionmenu_model.set('Escolha MARCA')
        self.Add_to_Treeview_Model()


    def Insert_Model_Brand(self):
        brand_name = self.optionmenu_model.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_model = brand[0]
                return id_brand_model
            else:
                pass


    def Insert_Model(self,):
        id_brand_model = self.Insert_Model_Brand()

        connect_db = Database_Model()
        connect_db.Create_Model_Table()
        user = self.name_user_current
        name_model = self.id_entry_model.get().upper()
        brand_name = self.optionmenu_model.get().upper()

        if not (name_model):
            messagebox.showerror('Error', 'Digitar um MODELO.')
        elif brand_name.upper() == 'ESCOLHA MARCA':
            messagebox.showerror('Error', 'Escolher uma MARCA.')
        else:
            check_name_model = connect_db.Search_Model_Name(
                model_name=name_model,
                brand_name_model=id_brand_model,
                )
            if check_name_model == 'sim':
                sleep(1)
                messagebox.showerror('Error', 'MODELO já REGISTRADO.')
            else:
                connect_db.Insert_Model(
                    user_name=user.upper(),
                    brand_name_model=id_brand_model,
                    model_name=name_model.upper()
                    )

                messagebox.showinfo('Sucess', 'MODELO REGISTRADO com SUCESSO.')
                self.Clear_Entry_Model()
                self.Add_to_Treeview_Model()
                self.Window_Product_Registration()


    def Update_Model(self, ):
        id_brand_model = self.Insert_Model_Brand()

        connect_db = Database_Model()
        user = self.name_user_current


        selected_item = self.table_models.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha um MODELO para atualizar.')
        else:
            item = self.table_models.focus()
            if item:
                row = self.table_models.item(item)['values']
            id_model = row[0]
            name_model = self.id_entry_model.get().upper()
            brand_name = id_brand_model

            check_name_model = connect_db.Search_Model_Name(
                model_name=name_model,
                brand_name_model=brand_name,
                )
            if check_name_model == 'sim':
                sleep(1)
                messagebox.showerror('Error', 'MODELO já REGISTRADO.')
            else:
                connect_db.Update_Model(
                    new_name_model=name_model,
                    id=id_model,
                    name_user=user,
                    brand_name_model=brand_name
                    )
                messagebox.showinfo('Sucesso', 'MODELO ATUALIZADO.')
                self.Clear_Entry_Model()
                self.Add_to_Treeview_Model()
                self.Window_Product_Registration()


    def Delete_Model_Search_Product(self, ):
        connect_db = Database_Product()
        products = connect_db.Fetch_Product()
        products_name_id = []
        for product in products:
            products_name_id.append(f'{product[3]}')
        return products_name_id
    

    def Delete_Model(self, ):
        product_config = self.Delete_Model_Search_Product()

        connect_db = Database_Model()

        selected_item = self.table_models.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha um MODELO para EXCLUIR.')
        else:
            item = self.table_models.focus()
            if item:
                row = self.table_models.item(item)['values']
            id_model = row[0]
            name_model = self.id_entry_model.get()
            delete = False
            for x in product_config:
                if int(x) == int(id_model):
                    messagebox.showerror('Error', 'MODELO VINCULADO A PRODUTOS.')
                    delete = True
                    break
                elif int(x) != int(id_model):
                    pass

            if delete == False:
                connect_db.Delete_Model(
                    name_model=name_model,
                    id=id_model
                    )
                messagebox.showinfo('Sucesso', 'MODELO EXCLUÍDO.')
                self.Clear_Entry_Model()
                self.Add_to_Treeview_Model()


        # **************** DEFMODELOS  ************************


        # **************** DEFPRODUTOS  ************************


    def Display_Data_Product(self, event):
        selected_item_display = self.table_product.focus()
        if selected_item_display:
            row = self.table_product.item(selected_item_display)['values']
            self.id_entry_product.delete(0, 'end')
            self.id_entry_product.insert(0,row[3])
            self.optionmenu_brand_product.set(value=row[1])
            self.optionmenu_brand_product.configure(state='disabled')
            self.optionmenu_model_product.set(value=row[2])
            self.optionmenu_model_product.configure(state='disabled')
        else:
            pass

    def Search_Product_Brand(self):
        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        brands_name_id = []
        for brand in brands:
            brands_name_id.append(f'{brand[0]}: {brand[2]}')
        return brands_name_id
    
    def Search_Product_Model(self):
        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        models_name_id = []
        for model in models:
            models_name_id.append(f'{model[0]}: {model[3]}')
        return models_name_id
    
    def Search_Product_Product_Name(self):
        connect_db_product = Database_Product()
        products = connect_db_product.Fetch_Product()
        product_name_id = []
        for product in products:
            product_name_id.append(f'{product[0]}: {product[4]}')
        return product_name_id
    
    def Search_Product_Product_Color(self):
        connect_db_product = Database_Color()
        products = connect_db_product.Fetch_Color()
        product_color_id = []
        for product in products:
            product_color_id.append(f'{product[0]}: {product[5]}')
        return product_color_id

    def Add_to_Treeview_Product(self, ):
        brands_names = self.Search_Product_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        product_names = self.Search_Product_Model()
        item_model = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        connect_db = Database_Product()
        products = connect_db.Fetch_Product()
        self.table_product.delete(*self.table_product.get_children())
        brand_choice = self.optionmenu_brand_product.get()

        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                bra=product[2]
                mod=product[3]
                pro=product[4]
                bran=''
                model=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                model=namemodel
                            else:
                                pass
                    else:
                        pass
                self.table_product.insert('', 'end', values=[id_p,bran,model,pro])
            self.Sort_Treeview(self.table_product, 'MARCA', False)
        else:
            for num, namebrand in item_brands:
                if namebrand == brand_choice:
                    brandnum =num
                        
            for product in products:
                if product[2] == int(brandnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    bran=''
                    model=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                else:
                                    pass
                        else:
                            pass

                    self.table_product.insert('', 'end', values=[id_p,bran,model,pro])
                self.Sort_Treeview(self.table_product, 'MODELO', False)


    def Search_Product_Model_One(self):
        brand_name = self.optionmenu_brand_product.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_product = int(brand[0])
                return id_brand_product
            else:
                pass

    def Search_Product_Model_Two(self):
        id_brand = self.Search_Product_Model_One()

        model_name = self.optionmenu_model_product.get().upper()

        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[3] == model_name:
                if model[2] == id_brand:
                    id_model_product = int(model[0])
                    return id_brand, id_model_product
            else:
                pass
    
    def Add_to_Treeview_Product_Model(self):
        id_brand_product = self.Search_Product_Model_Two()

        brands_names = self.Search_Product_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Product_Model()
        item_model = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        model_name = self.optionmenu_model_product.get().upper()
        connect_db = Database_Product()
        products = connect_db.Fetch_Product()
        self.table_product.delete(*self.table_product.get_children())
        listmodel = []
        if model_name == 'Escolha MARCA':
            pass
        else:
            for product in products:
                if product[2] == int(id_brand_product[0]):
                    if product[3] == int(id_brand_product[1]):
                        listmodel.append(product)
            for prod in listmodel:
                id_p=prod[0]
                bra=prod[2]
                mod=prod[3]
                pro=prod[4]
                bran=''
                model=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        print(f'num {num} e name brand {namebrand}')

                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                print(f'num {num1} e name brand {namemodel}')
                                model=namemodel
                            else:
                                pass
                    else:
                        pass

                self.table_product.insert('', 'end', values=[id_p,bran,model,pro])
            self.Sort_Treeview(self.table_product, 'PRODUTO', False)


    def Clear_Entry_Product(self, *clicked):
        if clicked:
            self.table_product.selection_remove(self.table_product.focus())
            self.table_product.focus('')
        self.id_entry_product.delete(0, 'end')
        self.optionmenu_brand_product.configure(state='normal')
        self.optionmenu_model_product.configure(state='normal')
        self.optionmenu_model_product.configure(values=['Escolha MARCA'])
        self.optionmenu_model_product.set('Escolha MARCA')
        self.optionmenu_brand_product.set('Escolha MARCA')
        self.Add_to_Treeview_Product()


    def Insert_Brand_Product(self):
        brand_name = self.optionmenu_brand_product.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_product = int(brand[0])
                return id_brand_product
            else:
                pass


    def Insert_Model_Product(self):
        id_brand = self.Insert_Brand_Product()

        model_name = self.optionmenu_model_product.get().upper()
        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[3] == model_name:
                if model[2] == id_brand:
                    id_model_product = int(model[0])
                    return id_brand, id_model_product
            else:
                pass


    def Insert_Product(self, ):
        id_model = self.Insert_Model_Product()

        connect_db = Database_Product()
        connect_db.Create_Product_Table()
        user = self.name_user_current
        name_product = self.id_entry_product.get().upper()
        model_product = self.optionmenu_model_product.get()

        if not (name_product):
            messagebox.showerror('Error', 'Digitar um PRODUTO.')
        elif model_product.upper() == 'ESCOLHA MARCA':
            messagebox.showerror('Error', 'Escolher um MODELO.')
        elif model_product.upper() == 'ESCOLHA MODELO':
            messagebox.showerror('Error', 'Escolher um MODELO.')
        else:
            check_name_product = connect_db.Search_Product_Name(
                product_name=name_product,
                model_name_product=id_model[1],
                brand_name_product=id_model[0],
                )
            if check_name_product == 'sim':
                sleep(1)
                messagebox.showerror('Error', 'PRODUTO já REGISTRADO.')
            else:
                connect_db.Insert_Product(
                    user_name=user.upper(),
                    brand_name_product=id_model[0],
                    model_name_product=id_model[1],
                    product_name=name_product.upper(),
                    )
                messagebox.showinfo('Sucess', 'PRODUTO REGISTRADO com SUCESSO.')
                self.Clear_Entry_Product()
                self.Window_Product_Registration()


    def Update_Product(self, ):
        id_brand = self.Insert_Brand_Product()
        id_model = self.Insert_Model_Product()

        connect_db = Database_Product()
        user = self.name_user_current

        selected_item = self.table_product.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha um PRODUTO para atualizar.')
        else:
            item = self.table_product.focus()
            if item:
                row = self.table_product.item(item)['values']
            id_product = row[0]
            name_product = self.id_entry_product.get().upper()

            check_name_product = connect_db.Search_Product_Name(
                product_name=name_product,
                model_name_product=id_model,
                brand_name_product=id_brand,
                )
            if check_name_product == 'sim':
                sleep(1)
                messagebox.showerror('Error', 'PRODUTO já REGISTRADO.')
            else:
                connect_db.Update_Product(
                    product_name=name_product,
                    id=id_product,
                    )
                messagebox.showinfo('Sucesso', 'PRODUTO ATUALIZADO.')
                self.Add_to_Treeview_Product()
                self.Clear_Entry_Product()
                self.Window_Product_Registration()

    def Delete_Product_Search_Color(self, ):
        connect_db = Database_Color()
        products = connect_db.Fetch_Color()
        color_name_id = []
        for product in products:
            color_name_id.append(f'{product[4]}')
        return color_name_id
    
    def Delete_Product(self, ):
        color_config = self.Delete_Product_Search_Color()

        connect_db = Database_Product()
        selected_item = self.table_product.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha um PRODUTO para EXCLUIR.')
        else:
            item = self.table_product.focus()
            if item:
                row = self.table_product.item(item)['values']
            id_product = row[0]
            name_product = self.id_entry_product.get()
            delete = False
            for x in color_config:
                if int(x) == int(id_product):
                    messagebox.showerror('Error', 'PRODUTO VINCULADO A CORES.')
                    delete = True
                    break
                elif int(x) != int(id_product):
                    pass

            if delete == False:
                connect_db.Delete_Product(
                    product_name=name_product,
                    id=id_product
                    )
                messagebox.showinfo('Sucesso', 'PRODUTO EXCLUÍDO.')
                self.Add_to_Treeview_Product()
                self.Clear_Entry_Product()


        # **************** DEFPRODUTOS  ************************


        # **************** DEFCORES  ************************


    def Display_Data_Color(self, event):
        selected_item_display = self.table_color.focus()
        if selected_item_display:
            row = self.table_color.item(selected_item_display)['values']
            self.id_entry_color.delete(0, 'end')
            self.id_entry_color.insert(0,row[4])
            self.optionmenu_brand_color.set(value=row[1])
            self.optionmenu_brand_color.configure(state='disabled')
            self.optionmenu_model_color.set(value=row[2])
            self.optionmenu_model_color.configure(state='disabled')
            self.optionmenu_product_color.set(value=row[3])
            self.optionmenu_product_color.configure(state='disabled')
        else:
            pass

    def Search_Color_Brand(self):
        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        brands_name_id = []
        for brand in brands:
            brands_name_id.append(f'{brand[0]}: {brand[2]}')
        return brands_name_id
    
    def Search_Color_Model(self):
        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        models_name_id = []
        for model in models:
            models_name_id.append(f'{model[0]}: {model[3]}')
        return models_name_id
    
    def Search_Color_Model_Two(self):
        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        models_name_id = []
        for model in models:
            models_name_id.append(f'{model[0]}: {model[2]}: {model[3]}')
        return models_name_id
    
    def Search_Color_Product(self):
        connect_db_product = Database_Product()
        products = connect_db_product.Fetch_Product()
        product_name_id = []
        for product in products:
            product_name_id.append(f'{product[0]}: {product[4]}')
        return product_name_id
    
    def Search_Color_Product_Two(self):
        connect_db_product = Database_Product()
        products = connect_db_product.Fetch_Product()
        product_name_id = []
        for product in products:
            product_name_id.append(f'{product[0]}: {product[3]}: {product[4]}')
        return product_name_id
    
    def Add_to_Treeview_Color(self, ):
        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_model = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Color_Product()
        item_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_product.append(k)

        connect_db = Database_Color()
        products = connect_db.Fetch_Color()
        self.table_color.delete(*self.table_color.get_children())
        brand_choice = self.optionmenu_brand_color.get()
        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                bra=product[2]
                mod=product[3]
                pro=product[4]
                col=product[5]
                bran=''
                model=''
                prod=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                model=namemodel
                                for num2, nameproduct in item_product:
                                    if int(num2) == pro:
                                        prod=nameproduct
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass
                self.table_color.insert('', 'end', values=[id_p,bran,model,prod, col])
            self.Sort_Treeview(self.table_color, 'MARCA', False)
        else:
            for num, namebrand in item_brands:
                if namebrand == brand_choice:
                    brandnum =num
            for product in products:
                if product[2] == int(brandnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    bran=''
                    model=''
                    prod=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, nameproduct in item_product:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_color.insert('', 'end', values=[id_p,bran,model,prod, col])
                self.Sort_Treeview(self.table_color, 'MODELO', False)


    def Search_Product_Treeview_One(self):
        brand_name = self.optionmenu_brand_color.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_color = int(brand[0])
                return id_brand_color
            else:
                pass

    def Search_Color_Treeview_Two(self):
        id_brand = self.Search_Product_Treeview_One()

        model_name = self.optionmenu_model_color.get().upper()
        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[3] == model_name:
                if model[2] == id_brand:
                    id_model = int(model[0])
                    return id_brand, id_model
            else:
                pass
    

    def Add_to_Treeview_Color_Model(self, ):
        id_brand_product = self.Search_Color_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_model = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Color_Product_Two()
        item_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_product.append(k)

        connect_db = Database_Color()
        products = connect_db.Fetch_Color()
        self.table_color.delete(*self.table_color.get_children())
        model_choice = self.optionmenu_model_color.get()
        if model_choice == 'Escolha MARCA':
            pass
        else:
            for product in products:
                if product[3] == int(id_brand_product[1]):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    bran=''
                    model=''
                    prod=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_product:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_color.insert('', 'end', values=[id_p,bran,model,prod, col])
                self.Sort_Treeview(self.table_color, 'PRODUTO', False)


    def Add_to_Treeview_Color_Product(self, ):
        id_brand_product = self.Search_Color_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_model = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Color_Product_Two()
        item_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_product.append(k)

        connect_db = Database_Color()
        products = connect_db.Fetch_Color()
        self.table_color.delete(*self.table_color.get_children())
        product_choice = self.optionmenu_product_color.get()
        for num2, namemodel, nameproduct in item_product:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2
        if product_choice == 'Escolha PPRODUTO':
            pass
        else:
            for product in products:
                if product[4] == int(prodnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    bran=''
                    model=''
                    prod=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_product:
                                        if product_choice == nameproduct:
                                            if int(num2) == pro:
                                                prod=nameproduct
                                                print(prod)

                                            else:
                                                pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_color.insert('', 'end', values=[id_p,bran,model,prod, col])
                self.Sort_Treeview(self.table_color, 'COR', False)


    def Clear_Entry_Color(self, *clicked):
        if clicked:
            self.table_color.selection_remove(self.table_color.focus())
            self.table_color.focus('')
        self.id_entry_color.delete(0, 'end')
        self.optionmenu_brand_color.configure(state='normal')
        self.optionmenu_model_color.configure(state='normal')
        self.optionmenu_product_color.configure(state='normal')
        self.optionmenu_model_color.configure(values=['Escolha MARCA'])
        self.optionmenu_product_color.configure(values=['Escolha MARCA'])
        self.optionmenu_model_color.set('Escolha MARCA')
        self.optionmenu_brand_color.set('Escolha MARCA')
        self.optionmenu_product_color.set('Escolha MARCA')
        self.Add_to_Treeview_Color()


    def Insert_Color_Stock(self, brand, model, product, color ):
        connect_db = Database_Color()
        products = connect_db.Fetch_Color()
        for n_product in products:
            if n_product[5] == color:
                if n_product[4] == product:
                    if n_product[3] == model:
                        if n_product[2] == brand:
                            id_color= n_product[0]
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass


        user = self.name_user_current
        connect_db_stock = Database_Stock()
        connect_db_stock.Create_Stock_Table()

        connect_db_stock.Insert_Stock(
            user_name = user.upper(),
            brand_name_stock = brand,
            model_name_stock = model,
            product_name_stock = product,
            color_product_stock = id_color,
            product_stock_amount = 0
            )


    def Insert_Brand_Color(self):
        brand_name = self.optionmenu_brand_color.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand = int(brand[0])
                return id_brand
            else:
                pass


    def Insert_Model_Color(self):
        id_brand = self.Insert_Brand_Color()

        model_name = self.optionmenu_model_color.get().upper()

        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[2] == id_brand:
                if model[3] == model_name:
                    id_model = int(model[0])
                    return id_brand, id_model
                else:
                    pass
            else:
                pass

    def Insert_Product_Color(self):
        id_model_product = self.Insert_Model_Color()

        product_name = self.optionmenu_product_color.get().upper()
        connect_db_product = Database_Product()
        products = connect_db_product.Fetch_Product()
        for product in products:
            if product[2] == id_model_product[0]:
                if product[3] == id_model_product[1]:
                    if product[4] == product_name:
                        id_product = int(product[0])
                        return id_model_product[0] , id_model_product[1] , id_product
                    else:
                        pass
                else:
                    pass
            else:
                pass


    def Insert_Color(self, ):
        id_product = self.Insert_Product_Color()
        print(id_product)
        connect_db = Database_Color()
        connect_db.Create_Color_Table()
        user = self.name_user_current

        name_color = self.id_entry_color.get().upper()
        model_color = self.optionmenu_model_color.get()

        if not (name_color):
            messagebox.showerror('Error', 'Digitar uma COR.')
        elif model_color.upper() == 'ESCOLHA MARCA':
            messagebox.showerror('Error', 'Escolher um MODELO.')
        elif model_color.upper() == 'ESCOLHA MODELO':
            messagebox.showerror('Error', 'Escolher um MODELO.')
        else:
            check_name_color = connect_db.Search_Color(
                color_name=name_color,
                product_name_color=id_product[2],
                model_name_color=id_product[1],
                brand_name_color=id_product[0]
                )
            if check_name_color == 'sim':
                sleep(1)
                messagebox.showerror('Error', 'COR já REGISTRADA.')
            else:
                connect_db.Insert_Color(
                    user_name=user.upper(),
                    brand_name_color=id_product[0],
                    model_name_color=id_product[1],
                    product_name_color=id_product[2],
                    color_name=name_color.upper(),
                    )
                messagebox.showinfo('Sucess', 'PRODUTO REGISTRADO com SUCESSO.')
                self.Insert_Color_Stock(
                    brand=id_product[0],
                    model=id_product[1],
                    product=id_product[2],
                    color=name_color.upper()
                )
                self.Clear_Entry_Color()
                self.Window_Product_Registration()


    def Update_Color(self, ):
        id_product = self.Insert_Product_Color()

        connect_db = Database_Color()
        user = self.name_user_current

        selected_item = self.table_color.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha uma COR para atualizar.')
        else:
            item = self.table_color.focus()
            if item:
                row = self.table_color.item(item)['values']
            id_color = row[0]
            name_color = self.id_entry_color.get().upper()
            check_name_color = connect_db.Search_Color(
                color_name=name_color,
                product_name_color=id_product[2],
                model_name_color=id_product[1],
                brand_name_color=id_product[0],
                )
            if check_name_color == 'sim':
                messagebox.showerror('Error', 'COR já REGISTRADA.')
            else:
                connect_db.Update_Color(
                    color_name=name_color,
                    id=id_color,
                    )
                messagebox.showinfo('Sucesso', 'COR ATUALIZADO.')
                self.Add_to_Treeview_Color()
                self.Clear_Entry_Color()
                self.Window_Product_Registration()


    def Delete_Color_Search_Stock(self, ):
        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        stock_name_id = []
        for product in products:
            stock_name_id.append(f'{product[5]}: {product[6]}')
        return stock_name_id


    def Delete_Color_Stock(self, id_color):
        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        stock_name_id = []
        for product in products:
            stock_name_id.append(f'{product[6]}')

        connect_db.Delete_Stock_Product(
            color_product_stock=id_color
            )


    def Delete_Color(self, ):
        stock_config = self.Delete_Color_Search_Stock()
        connect_db = Database_Color()

        selected_item = self.table_color.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha uma COR para EXCLUIR.')
        else:
            item = self.table_color.focus()
            if item:
                row = self.table_color.item(item)['values']
            id_color = row[0]
            name_color = self.id_entry_color.get().upper()


            delete = False
            item_stock = []
            for x in stock_config:
                y = str(x)
                k = y.split(': ')
                item_stock.append(k)

            for num_color, num_stock in item_stock:
                if int(num_color) == int(id_color):
                    if int(num_stock) > 0:
                        messagebox.showerror('Error', 'PRODUTO COM ESTOQUE.')
                        delete = True
                        break
                    else:
                        pass
                else:
                    pass

            if delete == False:
                connect_db.Delete_Color(
                    color_name=name_color,
                    id=id_color
                    )
                
                self.Delete_Color_Stock(id_color)
                messagebox.showinfo('Sucesso', 'COR EXCLUÍDA.')
                self.Add_to_Treeview_Color()
                self.Clear_Entry_Color()
                self.Window_Product_Registration()


        # **************** DEFCORES  ************************


        # **************** DEFFORNECEDOR  ************************

    def Display_Data_Supplier(self, event):
        connect_db = Database_Supplier()
        products = connect_db.Fetch_Supplier()
        selected_item_display = self.table_supplier.focus()
        if selected_item_display:
            row = self.table_supplier.item(selected_item_display)['values']
            products = connect_db.Fetch_Supplier()
            for product in products:
                if product[0] == row[0]:

                    self.id_entry_name_supplier.delete(0, 'end')
                    self.id_entry_name_supplier.insert(0,product[1])
                    self.id_entry_name_supplier_fantasy.delete(0, 'end')
                    self.id_entry_name_supplier_fantasy.insert(0,product[2])
                    self.id_entry_supplier_cnpj.delete(0, 'end')
                    self.id_entry_supplier_cnpj.insert(0,product[3])
                    self.id_entry_state_registration.delete(0, 'end')
                    self.id_entry_state_registration.insert(0,product[4])
                    self.id_entry_county_registration.delete(0, 'end')
                    self.id_entry_county_registration.insert(0,product[5])
                    self.id_entry_address.delete(0, 'end')
                    self.id_entry_address.insert(0,product[6])
                    self.id_entry_address_state.delete(0, 'end')
                    self.id_entry_address_state.insert(0,product[7])
                    self.id_entry_supplier_email.delete(0, 'end')
                    self.id_entry_supplier_email.insert(0,product[8])
                    self.id_entry_supplier_phone.delete(0, 'end')
                    self.id_entry_supplier_phone.insert(0,product[9])
                    print(row[0])
                    print(product)

                else:
                    pass
        else:
            pass


    def Clear_Entry_Supplier(self, *clicked):
        if clicked:
            self.table_supplier.selection_remove(self.table_supplier.focus())
            self.table_supplier.focus('')
        self.id_entry_name_supplier.delete(0, 'end')
        self.id_entry_name_supplier_fantasy.delete(0, 'end')
        self.id_entry_supplier_cnpj.delete(0, 'end')
        self.id_entry_state_registration.delete(0, 'end')
        self.id_entry_county_registration.delete(0, 'end')
        self.id_entry_address.delete(0, 'end')
        self.id_entry_address_state.delete(0, 'end')
        self.id_entry_supplier_email.delete(0, 'end')
        self.id_entry_supplier_phone.delete(0, 'end')
        self.Add_to_Treeview_Supplier()


    def Insert_Supplier(self, ):
        connect_db = Database_Supplier()
        connect_db.Create_Supplier_Table()

        user = self.name_user_current

        name_supplier = self.id_entry_name_supplier.get().upper()
        supplier_fantasy = self.id_entry_name_supplier_fantasy.get().upper()
        cnpj = self.id_entry_supplier_cnpj.get().upper()
        state_registration = self.id_entry_state_registration.get().upper()
        county_registration = self.id_entry_county_registration.get().upper()
        address = self.id_entry_address.get().upper()
        address_state = self.id_entry_address_state.get().upper()
        email = self.id_entry_supplier_email.get().upper()
        phone = self.id_entry_supplier_phone.get().upper()

        create = False
        products = connect_db.Fetch_Supplier()
        for product in products:
            if product[3] == cnpj:
                messagebox.showerror('Error', 'CNPJ já Criado.')
                create = True
                break
            else:
                pass

        if create == False:
            if not (name_supplier):
                messagebox.showerror('Error', 'Colocar uma Razão Social.')
            elif not (supplier_fantasy):
                messagebox.showerror('Error', 'Colocar um Nome Fantasia.')
            elif not (cnpj):
                messagebox.showerror('Error', 'Colocar um CNPJ.')
            elif not (state_registration):
                messagebox.showerror('Error', 'Colocar uma Insc. Estadual.')
            elif not (county_registration):
                messagebox.showerror('Error', 'Colocar uma Insc. Municipal.')
            elif not (address):
                messagebox.showerror('Error', 'Colocar um Logradouro.')
            elif not (address_state):
                messagebox.showerror('Error', 'Colocar um Município/Estado.')
            elif not (email):
                messagebox.showerror('Error', 'Colocar um Email.')
            elif not (phone):
                messagebox.showerror('Error', 'Colocar um Contato.')
            
            else:
                print('ok')
                print(f'name_supplier: {name_supplier}')
                print(f'supplier_fantasy: {supplier_fantasy}')
                print(f'cnpj: {cnpj}')
                print(f'state_registration: {state_registration}')
                print(f'county_registration: {county_registration}')
                print(f'address: {address}')
                print(f'address_state: {address_state}')
                print(f'email: {email}')
                print(f'phone: {phone}')
                pass

                connect_db.Insert_Supplier(
                    name_supplier = name_supplier,
                    supplier_fantasy = supplier_fantasy,
                    cnpj = cnpj,
                    state_registration = state_registration,
                    county_registration = county_registration,
                    address = address,
                    address_state = address_state,
                    supplier_email = email,
                    phone = phone
                    )

                messagebox.showinfo('Sucesso', 'Fornecedor Criado.')
                self.Clear_Entry_Supplier()
                self.Window_Product_Registration()
        else:
            pass


    def Add_to_Treeview_Supplier(self, ):
        connect_db = Database_Supplier()
        products = connect_db.Fetch_Supplier()
        self.table_supplier.delete(*self.table_supplier.get_children())
        for product in products:
            id=product[0]
            raz_social=product[1]
            fantasia=product[2]
            cnpj=product[3]
            logra=product[6]

            self.table_supplier.insert('', 'end', values=[id, raz_social,fantasia,cnpj,logra])
   
        self.Sort_Treeview(self.table_supplier, 'NOME FANTASIA', False)
    

    def Update_Supplier(self, ):
        connect_db = Database_Supplier()
        user = self.name_user_current

        selected_item = self.table_supplier.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha um Fornecedor para atualizar.')
        else:
            item = self.table_supplier.focus()
            if item:
                row = self.table_supplier.item(item)['values']
            id_supplier = row[0]
            name_supplier = self.id_entry_name_supplier.get().upper()
            supplier_fantasy = self.id_entry_name_supplier_fantasy.get().upper()
            cnpj = self.id_entry_supplier_cnpj.get().upper()
            state_registration = self.id_entry_state_registration.get().upper()
            county_registration = self.id_entry_county_registration.get().upper()
            address = self.id_entry_address.get().upper()
            address_state = self.id_entry_address_state.get().upper()
            email = self.id_entry_supplier_email.get().upper()
            phone = self.id_entry_supplier_phone.get().upper()

            create = False
            products = connect_db.Fetch_Supplier()
            for product in products:
                if product[3] == cnpj:
                    messagebox.showerror('Error', 'CNPJ já Criado.')
                    create = True
                    break
                else:
                    pass

            if create == False:
                connect_db.Update_Supplier(
                        id=id_supplier,
                        name_supplier=name_supplier,
                        supplier_fantasy=supplier_fantasy,
                        cnpj=cnpj,
                        state_registration=state_registration,
                        county_registration=county_registration,
                        address=address,
                        address_state=address_state,
                        supplier_email=email,
                        phone=phone
                        )
                
                messagebox.showinfo('Sucesso', 'Fornecedor ATUALIZADO.')
                self.Add_to_Treeview_Supplier()
                self.Clear_Entry_Supplier()
                self.Window_Product_Registration()

            else:
                pass

    def Delete_Supplier(self, ):
        connect_db = Database_Supplier()

        selected_item = self.table_supplier.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha um Fornecedor para EXCLUIR.')
        else:
            item = self.table_supplier.focus()
            if item:
                row = self.table_supplier.item(item)['values']
            id_supplier = row[0]
            connect_db.Delete_Supplier(
                    id=id_supplier
                    )
            messagebox.showinfo('Sucesso', 'Fornecedor EXCLUÍDO.')
            self.Add_to_Treeview_Supplier()
            self.Clear_Entry_Supplier()
            self.Window_Product_Registration()


        # **************** DEFFORNECEDOR  ************************


        # **************** DEFPRESTADOR  ************************


    def Display_Data_Provider(self, event):
        connect_db = Database_Provider()
        products = connect_db.Fetch_Provider()
        selected_item_display = self.table_provider.focus()
        # print(f'Selected_item : {selected_item}')
        if selected_item_display:
            row = self.table_provider.item(selected_item_display)['values']
            for product in products:
                if product[0] == row[0]:
                    self.id_entry_name_provider.configure(state='normal')
                    self.id_entry_name_provider.delete(0, 'end')
                    self.id_entry_name_provider.insert(0,product[2])
                    self.optionmenu_supplier_name_provider.set(product[1])
                    self.optionmenu_supplier_name_provider.configure(state='disabled')
        else:
            pass


    def Clear_Entry_Provider(self, *clicked):
        if clicked:
            self.table_provider.selection_remove(self.table_provider.focus())
            self.table_provider.focus('')
        self.id_entry_name_provider.delete(0, 'end')
        self.id_entry_name_provider.configure(state='disabled')
        self.optionmenu_supplier_name_provider.set('FORNECEDOR')
        self.optionmenu_supplier_name_provider.configure(state='normal')

        self.Add_to_Treeview_Provider()



    def Add_to_Treeview_Provider(self, ):
        connect_db = Database_Provider()

        products = connect_db.Fetch_Provider()
        self.table_provider.delete(*self.table_provider.get_children())
        for product in products:
            self.table_provider.insert('', 'end', values=product)

        self.Sort_Treeview(self.table_provider, 'FORNECEDOR', False)

    def Add_to_Treeview_Provider_Name(self, ):
        connect_db = Database_Provider()
        products = connect_db.Fetch_Provider()
        self.table_provider.delete(*self.table_provider.get_children())
        supplier_name = self.optionmenu_supplier_name_provider.get()

        if supplier_name == 'FORNECEDOR':
            pass
        else:
            for product in products:
                if product[1] == supplier_name:
                    id_p=product[0]
                    supl=product[1]
                    prov=product[2]

                    self.table_provider.insert('', 'end', values=[id_p,supl,prov])
                self.Sort_Treeview(self.table_provider, 'SERVIÇO', False)


    def Insert_Provider(self, ):
        connect_db = Database_Provider()
        connect_db.Create_Provider_Table()
        user = self.name_user_current

        supplier_name = self.optionmenu_supplier_name_provider.get()
        name_provider = self.id_entry_name_provider.get().upper()

        if supplier_name == 'FORNECEDOR':
            messagebox.showerror('Error', 'Escolha um Fornecedor.')
        elif not (name_provider):
            messagebox.showerror('Error', 'Digitar um Serviço.')
        else:
            check_name_provider = connect_db.Search_Provider_Name(
                supplier_fantasy=supplier_name,
                provider_supplier=name_provider
                )
            if check_name_provider == 'sim':
                messagebox.showerror('Error', 'Serviço já REGISTRADO.')
            else:
                connect_db.Insert_Provider(
                    supplier_fantasy=supplier_name,
                    provider_supplier=name_provider
                    )
                messagebox.showinfo('Sucesso', 'Serviço Registrado com SUCESSO.')
                self.Add_to_Treeview_Provider()
                self.Clear_Entry_Provider()


    def Update_Provider(self, ):
        connect_db = Database_Provider()
        user = self.name_user_current
        selected_item = self.table_provider.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha um Serviço para atualizar.')
        else:
            item = self.table_provider.focus()
            if item:
                row = self.table_provider.item(item)['values']
            id_provider = row[0]
            supplier_name = self.optionmenu_supplier_name_provider.get()
            name_provider = self.id_entry_name_provider.get().upper()
            check_name_provider = connect_db.Search_Provider_Name(
                supplier_fantasy=supplier_name,
                provider_supplier=name_provider
                )
            if check_name_provider == 'sim':
                messagebox.showerror('Error', 'Serviço já REGISTRADO.')
                self.Add_to_Treeview_Provider()
                self.Clear_Entry_Provider()
            else:
                connect_db.Update_Provider(
                    provider_supplier=name_provider,
                    id=id_provider
                    )
                messagebox.showinfo('Sucesso', 'Serviço ATUALIZADO.')
                self.Add_to_Treeview_Provider()
                self.Clear_Entry_Provider()


    def Delete_Provider(self, ):
        connect_db = Database_Provider()
        selected_item = self.table_provider.focus()

        if not selected_item:
            messagebox.showerror('Error', 'Escolha um Serviço para EXCLUIR.')
        else:
            item = self.table_provider.focus()
            if item:
                row = self.table_provider.item(item)['values']
            id_provider = row[0]
            name_provider = self.id_entry_name_provider.get().upper()

            connect_db.Delete_Provider(
                provider_supplier=name_provider,
                id=id_provider
                )
            self.Add_to_Treeview_Provider()
            self.Clear_Entry_Provider()
            messagebox.showinfo('Sucesso', 'Serviço EXCLUÍDO.')


        # **************** DEFPRESTADOR  ************************


        # **************** DEFESTOQUE  ************************


    def Display_Data_Stock(self, event):
        selected_item_display = self.table_stock.focus()
        if selected_item_display:
            row = self.table_stock.item(selected_item_display)['values']
            self.optionmenu_brand_stock.set(value=row[1])
            self.optionmenu_brand_stock.configure(state='disabled')
            self.optionmenu_model_stock.set(value=row[2])
            self.optionmenu_model_stock.configure(state='disabled')
            self.optionmenu_product_stock.set(value=row[3])
            self.optionmenu_product_stock.configure(state='disabled')
            self.optionmenu_product_color_stock.set(value=row[4])
            self.optionmenu_product_color_stock.configure(state='disabled')
            print(row[0])
            print(row)

        else:
            pass

    def Clear_Entry_Stock(self, *clicked):
        if clicked:
            self.table_stock.selection_remove(self.table_stock.focus())
            self.table_stock.focus('')
        self.optionmenu_brand_stock.configure(state='normal')
        self.optionmenu_model_stock.configure(state='normal')
        self.optionmenu_product_stock.configure(state='normal')
        self.optionmenu_product_color_stock.configure(state='normal')
        self.optionmenu_brand_stock.set('Escolha MARCA')
        self.optionmenu_model_stock.set('Escolha MARCA')
        self.optionmenu_product_stock.set('Escolha MARCA')
        self.optionmenu_product_color_stock.set('Escolha MARCA')
        self.optionmenu_model_stock.configure(values=['Escolha MARCA'])
        self.optionmenu_product_stock.configure(values=['Escolha MARCA'])
        self.optionmenu_product_color_stock.configure(values=['Escolha MARCA'])
        self.Add_to_Treeview_Stock()


    def Add_to_Treeview_Stock(self, ):
        brands_names = self.Search_Product_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        model_names = self.Search_Product_Model()
        item_model = []
        for x in model_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Product_Product_Name()
        name_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            name_product.append(k)

        product_color = self.Search_Product_Product_Color()
        color_product = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_product.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        self.table_stock.delete(*self.table_stock.get_children())
        brand_choice = self.optionmenu_brand_stock.get()

        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                bra=product[2]
                mod=product[3]
                pro=product[4]
                col=product[5]
                qts=product[6]
                bran=''
                model=''
                prod=''
                colo=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                model=namemodel
                                for num2, nameproduct in name_product:
                                    if int(num2) == pro:
                                        prod=nameproduct
                                        for num3, colorproduct in color_product:
                                            if int(num3) == col:
                                                colo=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_stock.insert('', 'end', values=[id_p,bran,model,prod,colo, qts])

            self.Sort_Treeview(self.table_stock, 'MARCA', False)
        else:
            for num, namebrand in item_brands:
                if namebrand == brand_choice:
                    brandnum =num
                        
            for product in products:
                if product[2] == int(brandnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, nameproduct in name_product:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            for num3, colorproduct in color_product:
                                                if int(num3) == col:
                                                    colo=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_stock.insert('', 'end', values=[id_p,bran,model,prod,colo, qts])
                self.Sort_Treeview(self.table_stock, 'MODELO', False)


    def Search_Stock_Treeview_One(self):
        brand_name = self.optionmenu_brand_stock.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_color = int(brand[0])
                return id_brand_color
            else:
                pass

    def Search_Stock_Treeview_Two(self):
        id_brand = self.Search_Stock_Treeview_One()

        model_name = self.optionmenu_model_stock.get().upper()

        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[3] == model_name:
                if model[2] == id_brand:
                    id_model = int(model[0])
                    return id_brand, id_model
            else:
                pass
    
   
    def Add_to_Treeview_Stock_Model(self, ):
        id_brand_product = self.Search_Stock_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)


        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_stock.delete(*self.table_stock.get_children())
        model_choice = self.optionmenu_model_stock.get()

        if model_choice == 'Escolha MARCA':
            pass

        else:
            for product in products:
                if product[3] == int(id_brand_product[1]):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_stock.insert('', 'end', values=[id_p,bran,model,prod, colo, qts])
                self.Sort_Treeview(self.table_stock, 'PRODUTO', False)


    def Add_to_Treeview_Stock_Product(self, ):

        id_brand_product = self.Search_Stock_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_stock.delete(*self.table_stock.get_children())
        product_choice = self.optionmenu_product_stock.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        if product_choice == 'Escolha PPRODUTO':
            pass

        else:
            for product in products:
                if product[4] == int(prodnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_stock.insert('', 'end', values=[id_p,bran,model,prod, colo, qts])
                self.Sort_Treeview(self.table_stock, 'COR', False)


    def Search_Color_Color(self):
        connect_db_product = Database_Color()
        products = connect_db_product.Fetch_Color()
        color_id = []
        for product in products:
            color_id.append(f'{product[0]}: {product[4]}: {product[5]}')
        return color_id
    

    def Add_to_Treeview_Stock_Color(self, ):

        id_brand_product = self.Search_Stock_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        products_colors = self.Search_Color_Color()
        colors_products = []
        for x in products_colors:
            y = str(x)
            k = y.split(': ')
            colors_products.append(k)

        product_choice = self.optionmenu_product_stock.get()
        color_choice = self.optionmenu_product_color_stock.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        for num_color, num_product_color, color in colors_products:
            if color_choice == color:
                if prodnum == num_product_color:
                    colornum=num_color

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_stock.delete(*self.table_stock.get_children())


        if color_choice == 'Escolha COR':
            pass

        else:
            for product in products:
                if product[5] == int(colornum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_stock.insert('', 'end', values=[id_p,bran,model,prod, colo, qts])
                self.Sort_Treeview(self.table_stock, 'COR', False)

 
        # **************** DEFESTOQUE  ************************


        # **************** DEFENTRADANOTAS  ************************


    def Display_Data_Invoice(self, event):
        selected_item_display = self.table_invoice.focus()
        if selected_item_display:
            row = self.table_invoice.item(selected_item_display)['values']
            self.optionmenu_brand_invoice.set(value=row[1])
            self.optionmenu_brand_invoice.configure(state='disabled')
            self.optionmenu_model_invoice.set(value=row[2])
            self.optionmenu_model_invoice.configure(state='disabled')
            self.optionmenu_product_invoice.set(value=row[3])
            self.optionmenu_product_invoice.configure(state='disabled')
            self.optionmenu_product_color_invoice.set(value=row[4])
            self.optionmenu_product_color_invoice.configure(state='disabled')
            self.id_entry_product_invoice_amount.configure(state='normal')
            self.id_entry_product_invoice_unitary_value.configure(state='normal')
            self.id_entry_id_num_invoice.configure(state='normal')
            self.id_entry_id_product_invoice.delete(0, 'end')
            self.id_entry_id_product_invoice.insert(0,row[0])
            self.id_entry_id_product_invoice_amount_return.delete(0, 'end')
            self.id_entry_id_product_invoice_amount_return.insert(0,row[5])
            print(row[0])
            print(row)

        else:
            pass

    def Clear_Entry_Invoice(self, *clicked):
        if clicked:
            self.table_invoice_num.selection_remove(self.table_invoice_num.focus())
            self.table_invoice_num.focus('')
            self.table_invoice.selection_remove(self.table_invoice.focus())
            self.table_invoice.focus('')
        self.id_entry_product_invoice_amount.delete(0, 'end')
        self.id_entry_product_invoice_amount.configure(state='disabled')
        self.id_entry_product_invoice_unitary_value.delete(0, 'end')
        self.id_entry_product_invoice_unitary_value.configure(state='disabled')
        self.id_entry_id_num_invoice.delete(0, 'end')
        self.id_entry_id_num_invoice.configure(state='disabled')
        self.optionmenu_brand_invoice.configure(state='normal')
        self.optionmenu_model_invoice.configure(state='normal')
        self.optionmenu_product_invoice.configure(state='normal')
        self.optionmenu_product_color_invoice.configure(state='normal')
        self.optionmenu_brand_invoice.set('Escolha MARCA')
        self.optionmenu_model_invoice.set('Escolha MARCA')
        self.optionmenu_product_invoice.set('Escolha MARCA')
        self.optionmenu_product_color_invoice.set('Escolha MARCA')
        self.optionmenu_model_invoice.configure(values=['Escolha MARCA'])
        self.optionmenu_product_invoice.configure(values=['Escolha MARCA'])
        self.optionmenu_product_color_invoice.configure(values=['Escolha MARCA'])
        self.optionmenu_supplier_name.set('FORNECEDOR')
        self.id_entry_id_num_invoice.delete(0, 'end')
        self.id_entry_id_product_invoice.delete(0, 'end')
        self.id_entry_id_product_invoice_amount_return.delete(0, 'end')
        self.Add_to_Treeview_Invoice()
        self.Add_to_Treeview_Invoice_Num()


    def Insert_Invoice(self, ):
        connect_db = Database_Invoice()
        connect_db.Create_Invoice_Table()

        user = self.name_user_current

        invoice_number = self.id_entry_id_num_invoice.get()
        supplier = self.optionmenu_supplier_name.get()
        id_stock_product = self.id_entry_id_product_invoice.get()
        stock_amount = self.id_entry_id_product_invoice_amount_return.get()
        stock_amount_new = self.id_entry_product_invoice_amount.get()
        unitary_value = self.id_entry_product_invoice_unitary_value.get().strip()

        def isNumber(n):
            try:
                float(n)
            except ValueError:
                    return False
            return True
        
        if not (stock_amount):
            messagebox.showerror('Error', 'Escolha um PRODUTO.')
        elif supplier == 'FORNECEDOR':
            messagebox.showerror('Error', 'Escolha um Fornecedor.')
        elif invoice_number.strip() == '':
            messagebox.showerror('Error', 'Colocar uma Nota Fiscal.')
        elif stock_amount_new.strip() == '':
            messagebox.showerror('Error', 'Colocar uma Quantidade de Itens.')
        elif unitary_value == '':
            messagebox.showerror('Error', 'Colocar um Valor Unitário.')
        elif stock_amount_new.isdigit() == False:
            messagebox.showerror('Error', 'Colocar uma Quantidade de Itens Válida.')
        elif isNumber(unitary_value) != True:
            messagebox.showerror('Error', 'Colocar um Valor Unitário Válido.')
          
        else:
            print('ok')
            print(f'invoice_number: {invoice_number}')
            print(f'supplier: {supplier}')
            print(f'id_stock_product: {id_stock_product}')
            print(f'stock_amount: {stock_amount}')
            print(f'stock_amount_new: {stock_amount_new}')
            print(f'unitary_value: {unitary_value}')
            check_stock_amount = int(stock_amount) + int(stock_amount_new)
            print(f'soma: {check_stock_amount}')
            today = datetime.date.today()
            print(f'soma: {today}')
            pass

            connect_db.Insert_Invoice(
                user_name = user.upper(),
                date_invoice = today,
                invoice_number = invoice_number,
                supplier = supplier,
                id_product_invoice = id_stock_product,
                product_amount_invoice = stock_amount_new,
                unitary_value = unitary_value
                )


            self.Insert_Invoice_Stock(
                product_stock_amount_new=check_stock_amount,
                id_stock_product=id_stock_product
                )

            messagebox.showinfo('Sucesso', 'Item Nota Fiscal Salva.')
            messagebox.showinfo('Sucesso', 'Estoque Atualizado.')

            self.Clear_Entry_Invoice()


    def Insert_Invoice_Stock(self, product_stock_amount_new, id_stock_product):
        connect_db = Database_Stock()
        user = self.name_user_current

        connect_db.Update_Stock(
                product_stock_amount = product_stock_amount_new,
                id = id_stock_product,
                )
        

    def Add_to_Treeview_Invoice(self, ):
        brands_names = self.Search_Product_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        model_names = self.Search_Product_Model()
        item_model = []
        for x in model_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Product_Product_Name()
        name_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            name_product.append(k)

        product_color = self.Search_Product_Product_Color()
        color_product = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_product.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        self.table_invoice.delete(*self.table_invoice.get_children())
        brand_choice = self.optionmenu_brand_invoice.get()

        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                bra=product[2]
                mod=product[3]
                pro=product[4]
                col=product[5]
                qts=product[6]
                bran=''
                model=''
                prod=''
                colo=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        # print(f'num {num} e name brand {namebrand}')
                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                # print(f'num {num1} e name brand {namemodel}')
                                model=namemodel
                                for num2, nameproduct in name_product:
                                    if int(num2) == pro:
                                        prod=nameproduct
                                        for num3, colorproduct in color_product:
                                            if int(num3) == col:
                                                colo=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_invoice.insert('', 'end', values=[id_p,bran,model,prod,colo, qts])

            self.Sort_Treeview(self.table_invoice, 'MARCA', False)
        else:
            for num, namebrand in item_brands:
                if namebrand == brand_choice:
                    # print(f'num {num} e name brand {namebrand}')
                    brandnum =num
                        
            for product in products:
                if product[2] == int(brandnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, nameproduct in name_product:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            for num3, colorproduct in color_product:
                                                if int(num3) == col:
                                                    colo=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_invoice.insert('', 'end', values=[id_p,bran,model,prod,colo, qts])
                self.Sort_Treeview(self.table_invoice, 'MODELO', False)


    def Search_Invoice_Treeview_One(self):
        brand_name = self.optionmenu_brand_invoice.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_color = int(brand[0])
                return id_brand_color
            else:
                pass

    def Search_Invoice_Treeview_Two(self):
        id_brand = self.Search_Invoice_Treeview_One()

        model_name = self.optionmenu_model_invoice.get().upper()

        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[3] == model_name:
                if model[2] == id_brand:
                    id_model = int(model[0])
                    return id_brand, id_model
            else:
                pass
    
   
    def Add_to_Treeview_Invoice_Model(self, ):
        id_brand_product = self.Search_Invoice_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)


        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_invoice.delete(*self.table_invoice.get_children())
        model_choice = self.optionmenu_model_invoice.get()

        if model_choice == 'Escolha MARCA':
            pass

        else:
            for product in products:
                if product[3] == int(id_brand_product[1]):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_invoice.insert('', 'end', values=[id_p,bran,model,prod, colo, qts])
                self.Sort_Treeview(self.table_invoice, 'PRODUTO', False)


    def Add_to_Treeview_Invoice_Product(self, ):

        id_brand_product = self.Search_Invoice_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_invoice.delete(*self.table_invoice.get_children())
        product_choice = self.optionmenu_product_invoice.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        if product_choice == 'Escolha PPRODUTO':
            pass

        else:
            for product in products:
                if product[4] == int(prodnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_invoice.insert('', 'end', values=[id_p,bran,model,prod, colo, qts])
                self.Sort_Treeview(self.table_invoice, 'COR', False)


    def Search_Color_Color(self):
        connect_db_product = Database_Color()
        products = connect_db_product.Fetch_Color()
        color_id = []
        for product in products:
            color_id.append(f'{product[0]}: {product[4]}: {product[5]}')
        return color_id
    

    def Add_to_Treeview_Invoice_Color(self, ):

        id_brand_product = self.Search_Invoice_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        products_colors = self.Search_Color_Color()
        colors_products = []
        for x in products_colors:
            y = str(x)
            k = y.split(': ')
            colors_products.append(k)

        product_choice = self.optionmenu_product_invoice.get()
        color_choice = self.optionmenu_product_color_invoice.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        for num_color, num_product_color, color in colors_products:
            if color_choice == color:
                if prodnum == num_product_color:
                    colornum=num_color

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_invoice.delete(*self.table_invoice.get_children())


        if color_choice == 'Escolha COR':
            pass

        else:
            for product in products:
                if product[5] == int(colornum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_invoice.insert('', 'end', values=[id_p,bran,model,prod, colo, qts])
                self.Sort_Treeview(self.table_invoice, 'COR', False)

    
    def Search_Invoice_Brand(self):
        connect_db = Database_Brand()
        products = connect_db.Fetch_Brand()
        product_id = []
        for product in products:
            product_id.append(f'{product[0]}: {product[2]}')
        return product_id

    def Search_Invoice_Model(self):
        connect_db = Database_Model()
        products = connect_db.Fetch_Model()
        product_id = []
        for product in products:
            product_id.append(f'{product[0]}: {product[3]}')
        return product_id

    def Search_Invoice_Product(self):
        connect_db = Database_Product()
        products = connect_db.Fetch_Product()
        product_id = []
        for product in products:
            product_id.append(f'{product[0]}: {product[4]}')
        return product_id

    def Search_Invoice_Product_Color(self):
        connect_db = Database_Color()
        products = connect_db.Fetch_Color()
        product_id = []
        for product in products:
            product_id.append(f'{product[0]}: {product[5]}')
        return product_id

    def Search_Invoice_Id_Product_Stock(self):
        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        product_id = []
        for product in products:
            product_id.append(f'{product[0]}: {product[2]}: {product[3]}: {product[4]}: {product[5]}')
        return product_id
    

    def Add_to_Treeview_Invoice_Num(self, ):

        brands_names_ids = self.Search_Invoice_Id_Product_Stock()
        ids_brands = []
        for x in brands_names_ids:
            y = str(x)
            k = y.split(': ')
            ids_brands.append(k)

        brands_names = self.Search_Invoice_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Invoice_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Invoice_Product()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Invoice_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Invoice()
        products = connect_db.Fetch_Invoice()
        self.table_invoice_num.delete(*self.table_invoice_num.get_children())
        supplier = self.optionmenu_supplier_name.get()

        if supplier == 'FORNECEDOR':
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[6]
                bran = ''
                model = ''
                produc = ''
                col = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                for num1, namemodel in item_models:
                                    if int(num1) == model:
                                        model=namemodel
                                        for num2, nameproduct in item_products:
                                            if int(num2) == produc:
                                                produc=nameproduct
                                                for num3, colorproduct in color_products:
                                                    if int(num3) == col:
                                                        col=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_invoice_num.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts])

            self.Sort_Treeview(self.table_invoice_num, 'FORNECEDOR', False)
        else:
            for product in products:
                if product[4] == supplier:
                    id_p=product[0]
                    sup_fant=product[4]
                    in_num=product[3]
                    prod=product[5]
                    qts=product[6]
                    bran = ''
                    model = ''
                    produc = ''
                    col = ''
                    for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                        if int(num) == prod:
                            bran=int(bran_id)
                            model=int(mod_id)
                            produc=int(prod_id)
                            col=int(col_id)
                            for num1, namebrand in item_brands:
                                if int(num1) == bran:
                                    bran=namebrand
                                    for num1, namemodel in item_models:
                                        if int(num1) == model:
                                            model=namemodel
                                            for num2, nameproduct in item_products:
                                                if int(num2) == produc:
                                                    produc=nameproduct
                                                    for num3, colorproduct in color_products:
                                                        if int(num3) == col:
                                                            col=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass

                    self.table_invoice_num.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts])

                self.Sort_Treeview(self.table_invoice_num, 'N° NOTA', False)

        # **************** DEFENTRADANOTAS  ************************


        # **************** DEFCONSULTANOTAS  ************************

    def Display_Data_Invoice_Consult(self, event):
        selected_item_display = self.table_invoice_consult.focus()
        if selected_item_display:
            row = self.table_invoice_consult.item(selected_item_display)['values']
            print(row[0])
            print(row)
        else:
            pass


    def Clear_Entry_Invoice_Consult(self, *clicked):
        if clicked:
            self.table_invoice_consult.selection_remove(self.table_invoice_consult.focus())
            self.table_invoice_consult.focus('')
            self.table_invoice_consult.selection_remove(self.table_invoice_consult.focus())
            self.table_invoice_consult.focus('')
        self.optionmenu_supplier_name_consult.set('FORNECEDOR')
        self.optionmenu_num_invoice_consult.set('Escolha Fornecedor')
        self.optionmenu_num_invoice_consult.configure(values=['Escolha Fornecedor'])
        self.optionmenu_brand_invoice_consult.set('Escolha Fornecedor')
        self.optionmenu_brand_invoice_consult.configure(values=['Escolha Fornecedor'])
        self.Add_to_Treeview_Invoice_Consult()


    def Add_to_Treeview_Invoice_Consult(self, ):

        brands_names_ids = self.Search_Invoice_Id_Product_Stock()
        ids_brands = []
        for x in brands_names_ids:
            y = str(x)
            k = y.split(': ')
            ids_brands.append(k)

        brands_names = self.Search_Invoice_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Invoice_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Invoice_Product()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Invoice_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Invoice()
        products = connect_db.Fetch_Invoice()
        self.table_invoice_consult.delete(*self.table_invoice_consult.get_children())
        supplier = self.optionmenu_supplier_name_consult.get()

        if supplier == 'FORNECEDOR':
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[6]
                val=product[7]
                bran = ''
                model = ''
                produc = ''
                col = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                for num1, namemodel in item_models:
                                    if int(num1) == model:
                                        model=namemodel
                                        for num2, nameproduct in item_products:
                                            if int(num2) == produc:
                                                produc=nameproduct
                                                for num3, colorproduct in color_products:
                                                    if int(num3) == col:
                                                        col=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_invoice_consult.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts,val])

            self.Sort_Treeview(self.table_invoice_consult, 'FORNECEDOR', False)
        else:
            for product in products:
                if product[4] == supplier:
                    id_p=product[0]
                    sup_fant=product[4]
                    in_num=product[3]
                    prod=product[5]
                    qts=product[6]
                    val=product[7]
                    bran = ''
                    model = ''
                    produc = ''
                    col = ''
                    for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                        if int(num) == prod:
                            bran=int(bran_id)
                            model=int(mod_id)
                            produc=int(prod_id)
                            col=int(col_id)
                            for num1, namebrand in item_brands:
                                if int(num1) == bran:
                                    bran=namebrand
                                    for num1, namemodel in item_models:
                                        if int(num1) == model:
                                            model=namemodel
                                            for num2, nameproduct in item_products:
                                                if int(num2) == produc:
                                                    produc=nameproduct
                                                    for num3, colorproduct in color_products:
                                                        if int(num3) == col:
                                                            col=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass

                    self.table_invoice_consult.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts,val])

                self.Sort_Treeview(self.table_invoice_consult, 'N° NOTA', False)


    def Add_to_Treeview_Invoice_Consult_Num(self, ):

        brands_names_ids = self.Search_Invoice_Id_Product_Stock()
        ids_brands = []
        for x in brands_names_ids:
            y = str(x)
            k = y.split(': ')
            ids_brands.append(k)

        brands_names = self.Search_Invoice_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Invoice_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Invoice_Product()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Invoice_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Invoice()
        products = connect_db.Fetch_Invoice()
        self.table_invoice_consult.delete(*self.table_invoice_consult.get_children())
        num_invoice = self.optionmenu_num_invoice_consult.get()

        if num_invoice == 'Escolha Fornecedor':
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[6]
                val=product[7]
                bran = ''
                model = ''
                produc = ''
                col = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                for num1, namemodel in item_models:
                                    if int(num1) == model:
                                        model=namemodel
                                        for num2, nameproduct in item_products:
                                            if int(num2) == produc:
                                                produc=nameproduct
                                                for num3, colorproduct in color_products:
                                                    if int(num3) == col:
                                                        col=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_invoice_consult.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts,val])

            self.Sort_Treeview(self.table_invoice_consult, 'FORNECEDOR', False)
        else:
            for product in products:
                if product[3] == num_invoice:
                    id_p=product[0]
                    sup_fant=product[4]
                    in_num=product[3]
                    prod=product[5]
                    qts=product[6]
                    val=product[7]
                    bran = ''
                    model = ''
                    produc = ''
                    col = ''
                    for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                        if int(num) == prod:
                            bran=int(bran_id)
                            model=int(mod_id)
                            produc=int(prod_id)
                            col=int(col_id)
                            for num1, namebrand in item_brands:
                                if int(num1) == bran:
                                    bran=namebrand
                                    for num1, namemodel in item_models:
                                        if int(num1) == model:
                                            model=namemodel
                                            for num2, nameproduct in item_products:
                                                if int(num2) == produc:
                                                    produc=nameproduct
                                                    for num3, colorproduct in color_products:
                                                        if int(num3) == col:
                                                            col=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass

                    self.table_invoice_consult.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts,val])

                self.Sort_Treeview(self.table_invoice_consult, 'MARCA', False)


    def Add_to_Treeview_Invoice_Consult_Brand(self, ):

        brands_names_ids = self.Search_Invoice_Id_Product_Stock()
        ids_brands = []
        for x in brands_names_ids:
            y = str(x)
            k = y.split(': ')
            ids_brands.append(k)

        brands_names = self.Search_Invoice_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Invoice_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Invoice_Product()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Invoice_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)
        # print(f'item_model:  {item_model}')

        connect_db = Database_Invoice()
        products = connect_db.Fetch_Invoice()
        self.table_invoice_consult.delete(*self.table_invoice_consult.get_children())
        brand_invoice = self.optionmenu_brand_invoice_consult.get()
        num_invoice = self.optionmenu_num_invoice_consult.get()

        if brand_invoice == 'Escolha Fornecedor':
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[6]
                val=product[7]
                bran = ''
                model = ''
                produc = ''
                col = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                for num1, namemodel in item_models:
                                    if int(num1) == model:
                                        model=namemodel
                                        for num2, nameproduct in item_products:
                                            if int(num2) == produc:
                                                produc=nameproduct
                                                for num3, colorproduct in color_products:
                                                    if int(num3) == col:
                                                        col=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_invoice_consult.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts,val])

            self.Sort_Treeview(self.table_invoice_consult, 'FORNECEDOR', False)
        else:
            for product in products:
                if product[3] == num_invoice:
                    id_p = ''
                    sup_fant = ''
                    in_num = ''
                    bran = ''
                    model = ''
                    produc = ''
                    col = ''
                    qts = ''
                    val = ''
                    for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                        if int(num) == product[5]:
                            print(f'product[5] {product[5]} e bran_id {bran_id}')
                            for num1, namebrand in item_brands:
                                if int(num1) == int(bran_id):
                                    print(f'num1 {num1} e namebrand {namebrand}')
                                    if namebrand == brand_invoice:
                                        id_p=product[0]
                                        sup_fant=product[4]
                                        in_num=product[3]
                                        bran = namebrand
                                        model=int(mod_id)
                                        produc=int(prod_id)
                                        col=int(col_id)
                                        qts=product[6]
                                        val=product[7]
                                        for num2, namemodel in item_models:
                                            if int(num2) == model:
                                                model=namemodel
                                                for num3, nameproduct in item_products:
                                                    if int(num3) == produc:
                                                        produc=nameproduct
                                                        for num4, colorproduct in color_products:
                                                            if int(num4) == col:
                                                                col=colorproduct

                                        self.table_invoice_consult.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts,val])

                                    self.Sort_Treeview(self.table_invoice_consult, 'PRODUTO', False)


        # **************** DEFCONSULTANOTAS  ************************


        # **************** DEFPRECIFICAÇÃO  ************************

    def Clear_Entry_Pricing(self, *clicked):
        if clicked:
            self.table_pricing_num.selection_remove(self.table_pricing_num.focus())
            self.table_pricing_num.focus('')
            self.table_pricing_stock.selection_remove(self.table_pricing_stock.focus())
            self.table_pricing_stock.focus('')
        self.optionmenu_brand_pricing.configure(state='normal')
        self.optionmenu_brand_pricing.set('Escolha MARCA')
        self.optionmenu_model_pricing.configure(state='normal')
        self.optionmenu_model_pricing.set('Escolha MARCA')
        self.optionmenu_model_pricing.configure(values=['Escolha MARCA'])
        self.optionmenu_product_pricing.configure(state='normal')
        self.optionmenu_product_pricing.set('Escolha MARCA')
        self.optionmenu_product_pricing.configure(values=['Escolha MARCA'])
        self.optionmenu_product_color_pricing.configure(state='normal')
        self.optionmenu_product_color_pricing.set('Escolha MARCA')
        self.optionmenu_product_color_pricing.configure(values=['Escolha MARCA'])
        self.id_entry_product_pricing_unitary_value.delete(0, 'end')
        self.id_entry_pricing_tax.delete(0, 'end')
        self.id_entry_pricing_value_sale.delete(0, 'end')
        self.id_entry_pricing_value_profit.delete(0, 'end')
        self.id_product_pricing.delete(0, 'end')
        self.Add_to_Treeview_Pricing_Invoice_Brand()
        self.Add_to_Treeview_Stock_Pricing_Brand()


    def Calculate_Profit(self,):
        uni_value = self.id_entry_product_pricing_unitary_value.get()
        tax = self.id_entry_pricing_tax.get()
        value_sale = self.id_entry_pricing_value_sale.get()
        sum_pricing = float(tax) * float(value_sale) / 100
        sum_pricing01 = float(value_sale) - float(sum_pricing)
        sum_pricing02 = float(sum_pricing01) - float(uni_value)
        print(uni_value)
        print(tax)
        print(value_sale)
        print(f'sum_pricing : {sum_pricing}')
        print(f'Lucro Bruto: {sum_pricing01}')
        print(f'Lucro Líquido: {sum_pricing02}')
        self.id_entry_pricing_value_profit.delete(0, 'end')
        self.id_entry_pricing_value_profit.insert(0,sum_pricing02)
        self.add_button_pricing.configure(state='normal')

    def Display_Data_Pricing_Num_Id(self, event):
        selected_item_display = self.table_pricing_stock.focus()
        if selected_item_display:
            row = self.table_pricing_stock.item(selected_item_display)['values']
            self.id_product_pricing.delete(0, 'end')
            self.id_product_pricing.insert(0,row[0])
            print(row)
        else:
            pass


    def Display_Data_Pricing(self, event):
        selected_item_display = self.table_pricing_num.focus()
        if selected_item_display:
            row = self.table_pricing_num.item(selected_item_display)['values']
            self.optionmenu_brand_pricing.set(value=row[3])
            self.optionmenu_brand_pricing.configure(state='disabled')
            self.optionmenu_model_pricing.set(value=row[4])
            self.optionmenu_model_pricing.configure(state='disabled')
            self.optionmenu_product_pricing.set(value=row[5])
            self.optionmenu_product_pricing.configure(state='disabled')
            self.optionmenu_product_color_pricing.set(value=row[6])
            self.optionmenu_product_color_pricing.configure(state='disabled')
            self.id_entry_product_pricing_unitary_value.configure(state='normal')
            self.id_entry_product_pricing_unitary_value.delete(0, 'end')
            self.id_entry_product_pricing_unitary_value.insert(0,row[7])
            self.id_entry_pricing_tax.delete(0, 'end')
            self.id_entry_pricing_tax.configure(state='normal')
            self.id_entry_pricing_value_sale.delete(0, 'end')
            self.id_entry_pricing_value_sale.configure(state='normal')
            self.id_entry_pricing_value_profit.delete(0, 'end')
            self.id_entry_pricing_value_profit.configure(state='normal')
            self.Add_to_Treeview_Stock_Pricing_Brand()
            self.Add_to_Treeview_Stock_Pricing_Model()
            self.Add_to_Treeview_Stock_Pricing_Product()
            self.Add_to_Treeview_Stock_Pricing_Color()
        else:
            pass


    def Add_to_Treeview_Pricing_Invoice_Brand(self, ):
        brands_names_ids = self.Search_Invoice_Id_Product_Stock()
        ids_brands = []
        for x in brands_names_ids:
            y = str(x)
            k = y.split(': ')
            ids_brands.append(k)

        brands_names = self.Search_Invoice_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Invoice_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Invoice_Product()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Invoice_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Invoice()
        products = connect_db.Fetch_Invoice()
        self.table_pricing_num.delete(*self.table_pricing_num.get_children())
        brand_choice = self.optionmenu_brand_pricing.get()

        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[7]
                bran = ''
                model = ''
                produc = ''
                col = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                for num1, namemodel in item_models:
                                    if int(num1) == model:
                                        model=namemodel
                                        for num2, nameproduct in item_products:
                                            if int(num2) == produc:
                                                produc=nameproduct
                                                for num3, colorproduct in color_products:
                                                    if int(num3) == col:
                                                        col=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_pricing_num.insert('', 'end', values=[id_p,sup_fant,in_num,bran,model,produc,col,qts])

            self.Sort_Treeview(self.table_pricing_num, 'FORNECEDOR', False)
        else:
                        
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[6]
                bran = ''
                model = ''
                produc = ''
                col = ''
                id_p1 = ''
                st1 = ''
                in1 = ''
                nb1 = ''
                nm1 = ''
                pr1 = ''
                cl1 = ''
                qts1 = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                if namebrand == brand_choice:
                                    nb1 = namebrand
                                    for num1, namemodel in item_models:
                                        if int(num1) == model:
                                            nm1=namemodel
                                            for num2, nameproduct in item_products:
                                                if int(num2) == produc:
                                                    pr1=nameproduct
                                                    for num3, colorproduct in color_products:
                                                        if int(num3) == col:
                                                            cl1=colorproduct
                                                            id_p1 = product[0]
                                                            in1 = product[3]
                                                            st1 = product[4]
                                                            qts1 = product[7]
                                                            self.table_pricing_num.insert('', 'end', values=[id_p1,st1,in1,nb1,nm1,pr1,cl1,qts1])

                                                        self.Sort_Treeview(self.table_pricing_num, 'N° NOTA', False)

    def Add_to_Treeview_Pricing_Invoice_Model(self, ):

        brands_names_ids = self.Search_Invoice_Id_Product_Stock()
        ids_brands = []
        for x in brands_names_ids:
            y = str(x)
            k = y.split(': ')
            ids_brands.append(k)

        brands_names = self.Search_Invoice_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Invoice_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Invoice_Product()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Invoice_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Invoice()
        products = connect_db.Fetch_Invoice()
        self.table_pricing_num.delete(*self.table_pricing_num.get_children())
        brand_choice = self.optionmenu_brand_pricing.get()
        model_choice = self.optionmenu_model_pricing.get()

        if model_choice == 'Escolha MARCA':
            pass
        else:
                       
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[6]
                bran = ''
                model = ''
                produc = ''
                col = ''

                id_p1 = ''
                st1 = ''
                in1 = ''
                nb1 = ''
                nm1 = ''
                pr1 = ''
                cl1 = ''
                qts1 = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                if namebrand == brand_choice:
                                    nb1 = namebrand
                                    for num1, namemodel in item_models:
                                        if int(num1) == model:
                                            nm1=namemodel
                                            if nm1 == model_choice:
                                                for num2, nameproduct in item_products:
                                                    if int(num2) == produc:
                                                        pr1=nameproduct
                                                        for num3, colorproduct in color_products:
                                                            if int(num3) == col:
                                                                cl1=colorproduct
                                                                id_p1 = product[0]
                                                                in1 = product[3]
                                                                st1 = product[4]
                                                                qts1 = product[7]
                                                                self.table_pricing_num.insert('', 'end', values=[id_p1,st1,in1,nb1,nm1,pr1,cl1,qts1])

                                                            self.Sort_Treeview(self.table_pricing_num, 'N° NOTA', False)


    def Add_to_Treeview_Pricing_Invoice_Product(self, ):

        brands_names_ids = self.Search_Invoice_Id_Product_Stock()
        ids_brands = []
        for x in brands_names_ids:
            y = str(x)
            k = y.split(': ')
            ids_brands.append(k)

        brands_names = self.Search_Invoice_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Invoice_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Invoice_Product()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Invoice_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Invoice()
        products = connect_db.Fetch_Invoice()
        self.table_pricing_num.delete(*self.table_pricing_num.get_children())
        brand_choice = self.optionmenu_brand_pricing.get()
        model_choice = self.optionmenu_model_pricing.get()
        prod_choice = self.optionmenu_product_pricing.get()

        if prod_choice == 'Escolha MARCA':
            pass
        else:
                       
            for product in products:
                id_p=product[0]
                sup_fant=product[4]
                in_num=product[3]
                prod=product[5]
                qts=product[6]
                bran = ''
                model = ''
                produc = ''
                col = ''

                id_p1 = ''
                st1 = ''
                in1 = ''
                nb1 = ''
                nm1 = ''
                pr1 = ''
                cl1 = ''
                qts1 = ''
                for num, bran_id, mod_id, prod_id, col_id in ids_brands:
                    if int(num) == prod:
                        bran=int(bran_id)
                        model=int(mod_id)
                        produc=int(prod_id)
                        col=int(col_id)
                        for num1, namebrand in item_brands:
                            if int(num1) == bran:
                                bran=namebrand
                                if namebrand == brand_choice:
                                    nb1 = namebrand
                                    for num1, namemodel in item_models:
                                        if int(num1) == model:
                                            nm1=namemodel
                                            if nm1 == model_choice:
                                                for num2, nameproduct in item_products:
                                                    if int(num2) == produc:
                                                        pr1=nameproduct
                                                        if pr1 == prod_choice:
                                                            for num3, colorproduct in color_products:
                                                                if int(num3) == col:
                                                                    cl1=colorproduct
                                                                    id_p1 = product[0]
                                                                    in1 = product[3]
                                                                    st1 = product[4]
                                                                    qts1 = product[7]
                                                                    self.table_pricing_num.insert('', 'end', values=[id_p1,st1,in1,nb1,nm1,pr1,cl1,qts1])

                                                                self.Sort_Treeview(self.table_pricing_num, 'N° NOTA', False)


    def Add_to_Treeview_Stock_Pricing_Brand(self, ):
        brands_names = self.Search_Product_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        model_names = self.Search_Product_Model()
        item_model = []
        for x in model_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Product_Product_Name()
        name_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            name_product.append(k)

        product_color = self.Search_Product_Product_Color()
        color_product = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_product.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        self.table_pricing_stock.delete(*self.table_pricing_stock.get_children())
        brand_choice = self.optionmenu_brand_pricing.get()
        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                bra=product[2]
                mod=product[3]
                pro=product[4]
                col=product[5]
                v_venda=product[7]
                v_impos=product[8]
                v_lucro=product[9]
                bran=''
                model=''
                prod=''
                colo=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                model=namemodel
                                for num2, nameproduct in name_product:
                                    if int(num2) == pro:
                                        prod=nameproduct
                                        for num3, colorproduct in color_product:
                                            if int(num3) == col:
                                                colo=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_pricing_stock.insert('', 'end', values=[id_p,bran,model,prod,colo, v_venda, v_impos, v_lucro])

            self.Sort_Treeview(self.table_pricing_stock, 'MARCA', False)
        else:
            for num, namebrand in item_brands:
                if namebrand == brand_choice:
                    brandnum =num
                        
            for product in products:
                if product[2] == int(brandnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    v_venda=product[6]
                    v_impos=product[7]
                    v_lucro=product[8]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, nameproduct in name_product:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            for num3, colorproduct in color_product:
                                                if int(num3) == col:
                                                    colo=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_pricing_stock.insert('', 'end', values=[id_p,bran,model,prod,colo, v_venda, v_impos, v_lucro])
                self.Sort_Treeview(self.table_pricing_stock, 'MODELO', False)


    def Add_to_Treeview_Stock_Pricing_Model_Num(self, ):
        brands_names = self.Search_Product_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        model_names = self.Search_Product_Model()
        item_model = []
        for x in model_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Product_Product_Name()
        name_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            name_product.append(k)

        product_color = self.Search_Product_Product_Color()
        color_product = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_product.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        self.table_pricing_stock.delete(*self.table_pricing_stock.get_children())
        brand_choice = self.optionmenu_brand_pricing.get()

        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                bra=product[2]
                mod=product[3]
                pro=product[4]
                col=product[5]
                v_venda=product[7]
                v_impos=product[8]
                v_lucro=product[9]
                bran=''
                model=''
                prod=''
                colo=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                model=namemodel
                                for num2, nameproduct in name_product:
                                    if int(num2) == pro:
                                        prod=nameproduct
                                        for num3, colorproduct in color_product:
                                            if int(num3) == col:
                                                colo=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_pricing_stock.insert('', 'end', values=[id_p,bran,model,prod,colo, v_venda, v_impos, v_lucro])

            self.Sort_Treeview(self.table_pricing_stock, 'MARCA', False)
        else:
            for num, namebrand in item_brands:
                if namebrand == brand_choice:
                    brandnum =num
                        
            for product in products:
                if product[2] == int(brandnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    v_venda=product[7]
                    v_impos=product[8]
                    v_lucro=product[9]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, nameproduct in name_product:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            for num3, colorproduct in color_product:
                                                if int(num3) == col:
                                                    colo=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_pricing_stock.insert('', 'end', values=[id_p,bran,model,prod,colo, v_venda, v_impos, v_lucro])
                self.Sort_Treeview(self.table_pricing_stock, 'MODELO', False)


    def Search_Stock_Pricing_Treeview_One(self):
        brand_name = self.optionmenu_brand_pricing.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_color = int(brand[0])
                return id_brand_color
            else:
                pass

    def Search_Stock_Pricing_Treeview_Two(self):
        id_brand = self.Search_Stock_Pricing_Treeview_One()

        model_name = self.optionmenu_model_pricing.get().upper()

        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[3] == model_name:
                if model[2] == id_brand:
                    id_model = int(model[0])
                    return id_brand, id_model
            else:
                pass
    
   
    def Add_to_Treeview_Stock_Pricing_Model(self, ):
        id_brand_product = self.Search_Stock_Pricing_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)


        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_pricing_stock.delete(*self.table_pricing_stock.get_children())
        model_choice = self.optionmenu_model_pricing.get()

        if model_choice == 'Escolha MARCA':
            pass

        else:
            for product in products:
                if product[3] == int(id_brand_product[1]):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    v_venda=product[7]
                    v_impos=product[8]
                    v_lucro=product[9]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_pricing_stock.insert('', 'end', values=[id_p,bran,model,prod, colo, v_venda, v_impos, v_lucro])
                self.Sort_Treeview(self.table_pricing_stock, 'PRODUTO', False)


    def Add_to_Treeview_Stock_Pricing_Product(self, ):

        id_brand_product = self.Search_Stock_Pricing_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_pricing_stock.delete(*self.table_pricing_stock.get_children())
        product_choice = self.optionmenu_product_pricing.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        if product_choice == 'Escolha PPRODUTO':
            pass

        else:
            for product in products:
                if product[4] == int(prodnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    v_venda=product[7]
                    v_impos=product[8]
                    v_lucro=product[9]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_pricing_stock.insert('', 'end', values=[id_p,bran,model,prod, colo, v_venda, v_impos, v_lucro])
                self.Sort_Treeview(self.table_pricing_stock, 'COR', False)


    def Add_to_Treeview_Stock_Pricing_Color(self, ):

        id_brand_product = self.Search_Stock_Pricing_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        products_colors = self.Search_Color_Color()
        colors_products = []
        for x in products_colors:
            y = str(x)
            k = y.split(': ')
            colors_products.append(k)

        product_choice = self.optionmenu_product_pricing.get()
        color_choice = self.optionmenu_product_color_pricing.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        for num_color, num_product_color, color in colors_products:
            if color_choice == color:
                if prodnum == num_product_color:
                    colornum=num_color

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_pricing_stock.delete(*self.table_pricing_stock.get_children())


        if color_choice == 'Escolha COR':
            pass

        else:
            for product in products:
                if product[5] == int(colornum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    v_venda=product[7]
                    v_impos=product[8]
                    v_lucro=product[9]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_pricing_stock.insert('', 'end', values=[id_p,bran,model,prod, colo, v_venda, v_impos, v_lucro])
                self.Sort_Treeview(self.table_pricing_stock, 'COR', False)


    def Insert_Pricing(self, ):
        connect_db = Database_Stock()

        user = self.name_user_current

        id_product = self.id_product_pricing.get()
        tax = self.id_entry_pricing_tax.get()
        value_sale = self.id_entry_pricing_value_sale.get()
        value_profit = self.id_entry_pricing_value_profit.get()

        
        if not (id_product):
            messagebox.showerror('Error', 'Escolha um PRODUTO.')
        elif tax.strip() == '':
            messagebox.showerror('Error', 'Colocar um Imposto.')
        elif value_sale.strip() == '':
            messagebox.showerror('Error', 'Colocar uma Valor Venda.')
          
        else:
            self.add_button_pricing.configure(state='disabled')

            connect_db.Update_Stock_Pricing(
                id= id_product,
                value_sale = value_sale,
                tax = tax,
                profit = value_profit,
                )


            messagebox.showinfo('Sucesso', 'Estoque Atualizado.')

            self.Clear_Entry_Pricing()


        # **************** DEFPRECIFICAÇÃO  ************************


        # **************** DEFENTRADACUSTOS  ************************

    def Display_Data_Costs(self, event):
        selected_item_display = self.table_costs.focus()
        if selected_item_display:
            row = self.table_costs.item(selected_item_display)['values']
            self.optionmenu_supplier_name_costs.set(value=row[2])
            self.optionmenu_supplier_name_costs.configure(state='disabled')
            self.optionmenu_type_services.set(value=row[3])
            self.optionmenu_type_services.configure(state='disabled')
            self.optionmenu_types_of_costs.set(value=row[4])
            self.optionmenu_types_of_costs.configure(state='disabled')
            self.optionmenu_days_the_month.set(value=row[5])
            self.optionmenu_days_the_month.configure(state='disabled')
            self.id_entry_value_costs.delete(0, 'end')
            self.id_entry_value_costs.insert(0,row[6])
            self.id_entry_number_of_installments.delete(0, 'end')
            self.id_entry_number_of_installments.insert(0,row[7])
            self.id_entry_invoice_number_costs.delete(0, 'end')
            self.id_entry_invoice_number_costs.insert(0,row[8])
            print(row[0])
            print(row)

        else:
            pass

    def Clear_Entry_Costs(self, *clicked):
        if clicked:
            self.table_costs.selection_remove(self.table_costs.focus())
            self.table_costs.focus('')
        self.optionmenu_supplier_name_costs.set('FORNECEDOR')
        self.optionmenu_supplier_name_costs.configure(state='normal')
        self.optionmenu_type_services.set('Escolha Fornecedor')
        self.optionmenu_type_services.configure(values=['Escolha Fornecedor'])
        self.optionmenu_type_services.configure(state='normal')
        self.optionmenu_types_of_costs.set('Custos')
        self.optionmenu_types_of_costs.configure(values=['Custos Fixos',
            'Custos Variáveis'])
        self.optionmenu_types_of_costs.configure(state='normal')
        self.optionmenu_days_the_month.set('VENCIMENTO')
        self.optionmenu_days_the_month.configure(values=[
            '1','2','3','4','5','6','7','8','9','10',
            '11','12','13','14','15','16','17','18','19','20',
            '21','22','23','24','25','26','27','28','29','30','31'])
        self.optionmenu_days_the_month.configure(state='normal')
        self.id_entry_value_costs.delete(0, 'end')
        self.id_entry_number_of_installments.delete(0, 'end')
        self.id_entry_invoice_number_costs.delete(0, 'end')
        
        self.Add_to_Treeview_Costs()


    def Insert_Costs_Entry(self, ):
        connect_db = Database_Costs()
        connect_db.Create_Costs_Table()

        user = self.name_user_current

        supplier = self.optionmenu_supplier_name_costs.get()
        type_services = self.optionmenu_type_services.get()
        types_of_costs = self.optionmenu_types_of_costs.get()
        days_the_month = self.optionmenu_days_the_month.get()
        value_costs = self.id_entry_value_costs.get().strip()
        number_of_installments = self.id_entry_number_of_installments.get().strip()
        invoice_number = self.id_entry_invoice_number_costs.get().strip()

        if supplier == 'FORNECEDOR':
            messagebox.showerror('Error', 'Escolha um Fornecedor.')
        elif type_services == 'Escolha Fornecedor':
            messagebox.showerror('Error', 'Escolha um Serviço.')
        elif types_of_costs == 'Custos':
            messagebox.showerror('Error', 'Escolha Custos.')
        elif days_the_month == 'VENCIMENTO':
            messagebox.showerror('Error', 'Escolha Dia Vencimento.')
        elif value_costs.strip() == '':
            messagebox.showerror('Error', 'Colocar uma Valor.')
        elif number_of_installments.strip() == '':
            messagebox.showerror('Error', 'Colocar um Número Parcelas.')
        elif invoice_number.strip() == '':
            messagebox.showerror('Error', 'Colocar uma Nota Fiscal.')
        else:
            print('ok')
            print(f'supplier: {supplier}')
            print(f'type_services: {type_services}')
            print(f'types_of_costs: {types_of_costs}')
            print(f'days_the_month: {days_the_month}')
            print(f'value_costs: {value_costs}')
            print(f'number_of_installments: {number_of_installments}')
            print(f'invoice_number: {invoice_number}')
            today = datetime.date.today()
            print(f'soma: {today}')
            pass

            connect_db.Insert_Costs(
                user_name = user.upper(),
                date_costs = today,
                supplier_costs= supplier,
                provider_costs = type_services,
                types_of_costs = types_of_costs,
                days_the_costs = days_the_month,
                value_costs = value_costs,
                number_of_costs = number_of_installments,
                invoice_number_costs = invoice_number
                )
            
            messagebox.showinfo('Sucesso', 'Nota Fiscal Salva.')
            self.Add_to_Treeview_Costs()
            self.Clear_Entry_Costs()


    def Add_to_Treeview_Costs(self, ):
        connect_db = Database_Costs()
        products = connect_db.Fetch_Costs()
        self.table_costs.delete(*self.table_costs.get_children())
        supplier_choice = self.optionmenu_supplier_name_costs.get()

        if supplier_choice == 'FORNECEDOR':
            for product in products:
                id_p=product[0]
                date=product[2]
                supp=product[3]
                prov=product[4]
                types=product[5]
                days=product[6]
                val=product[7]
                num_of_cos=product[8]
                inv_num=product[9]

                self.table_costs.insert('', 'end', values=[id_p,date,supp,prov,types, days, val, num_of_cos, inv_num])

            self.Sort_Treeview(self.table_costs, 'FORNECEDOR', False)
        else:
            for product in products:
                if supplier_choice == product[3]:
                    id_p=product[0]
                    date=product[2]
                    supp=product[3]
                    prov=product[4]
                    types=product[5]
                    days=product[6]
                    val=product[7]
                    num_of_cos=product[8]
                    inv_num=product[9]

                    self.table_costs.insert('', 'end', values=[id_p,date,supp,prov,types, days, val, num_of_cos, inv_num])

                self.Sort_Treeview(self.table_costs, 'SERVIÇO', False)


    def Update_Costs(self, ):
        connect_db = Database_Costs()
        user = self.name_user_current

        selected_item = self.table_costs.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Escolha uma Nota Fiscal para atualizar.')
        else:
            item = self.table_costs.focus()
            if item:
                row = self.table_costs.item(item)['values']
            id_costs = row[0]
            supplier = self.optionmenu_supplier_name_costs.get()
            type_services = self.optionmenu_type_services.get()
            types_of_costs = self.optionmenu_types_of_costs.get()
            days_the_month = self.optionmenu_days_the_month.get()
            value_costs = self.id_entry_value_costs.get().strip()
            number_of_installments = self.id_entry_number_of_installments.get().strip()
            invoice_number = self.id_entry_invoice_number_costs.get().strip()


            connect_db.Update_Costs(
                    id = id_costs,
					supplier_costs = supplier,
					provider_costs = type_services,
					types_of_costs = types_of_costs,
					days_the_costs = days_the_month,
					value_costs = value_costs,
					number_of_costs = number_of_installments,
					invoice_number_costs = invoice_number
                    )
            
            messagebox.showinfo('Sucesso', 'Nota Fiscal ATUALIZADA.')
            self.Add_to_Treeview_Costs()
            self.Clear_Entry_Costs()


    def Delete_Costs(self, ):
        connect_db = Database_Costs()
        selected_item = self.table_costs.focus()

        if not selected_item:
            messagebox.showerror('Error', 'Escolha uma Nota Fiscal para EXCLUIR.')
        else:
            item = self.table_costs.focus()
            if item:
                row = self.table_costs.item(item)['values']
            id_costs = row[0]

            connect_db.Delete_Costs(
                id=id_costs
                )
            self.Add_to_Treeview_Costs()
            self.Clear_Entry_Costs()
            messagebox.showinfo('Sucesso', 'Nota Fiscal EXCLUÍDA.')


        # **************** DEFENTRADACUSTOS  ************************


        # **************** DEFVENDASFRENTE  ************************


    def Display_Data_Checkout_Consult(self, event):
        selected_item_display = self.table_checkout_consult.focus()
        if selected_item_display:
            row = self.table_checkout_consult.item(selected_item_display)['values']
            self.optionmenu_brand_name_checkout.set(value=row[1])
            self.optionmenu_brand_name_checkout.configure(state='disabled')
            self.optionmenu_model_name_checkout.set(value=row[2])
            self.optionmenu_model_name_checkout.configure(state='disabled')
            self.optionmenu_product_name_checkout.set(value=row[3])
            self.optionmenu_product_name_checkout.configure(state='disabled')
            self.optionmenu_color_name_checkout.set(value=row[4])
            self.optionmenu_color_name_checkout.configure(state='disabled')
            self.id_entry_amount_product_checkout.configure(state='normal')
            self.id_entry_amount_product_checkout.delete(0, 'end')
            self.add_button_product_checkout.configure(state='normal')
        else:
            pass

    def Display_Data_Checkout_Item(self, event):
        selected_item_display = self.table_checkout.focus()
        if selected_item_display:
            row = self.table_checkout.item(selected_item_display)['values']
            self.id_entry_edit_item_checkout.configure(state='normal')
            self.id_entry_edit_item_checkout.delete(0, 'end')
            self.id_entry_edit_item_checkout.insert(0, row[1])
            self.delete_button_item_checkout.configure(state='normal')
        else:
            pass

    def Clear_Entry_Checkout_Item(self,):
        self.table_checkout.selection_remove(self.table_checkout.focus())
        self.table_checkout.focus('')
        self.id_entry_edit_item_checkout.delete(0, 'end')
        self.id_entry_edit_item_checkout.configure(state='disabled')
        self.delete_button_item_checkout.configure(state='disabled')


    def Clear_Entry_Checkout_Consult(self, *clicked):
        if clicked:
            self.table_checkout_consult.selection_remove(self.table_checkout_consult.focus())
            self.table_checkout_consult.focus('')
        self.optionmenu_brand_name_checkout.configure(state='normal')
        self.optionmenu_brand_name_checkout.set('Escolha MARCA')
        self.optionmenu_model_name_checkout.configure(state='normal')
        self.optionmenu_model_name_checkout.set('Escolha MARCA')
        self.optionmenu_model_name_checkout.configure(values=['Escolha MARCA'])
        self.optionmenu_product_name_checkout.configure(state='normal')
        self.optionmenu_product_name_checkout.set('Escolha MARCA')
        self.optionmenu_product_name_checkout.configure(values=['Escolha MARCA'])
        self.optionmenu_color_name_checkout.configure(state='normal')
        self.optionmenu_color_name_checkout.set('Escolha MARCA')
        self.optionmenu_color_name_checkout.configure(values=['Escolha MARCA'])
        self.id_entry_amount_product_checkout.delete(0, 'end')
        self.id_entry_amount_product_checkout.configure(state='disabled')
        self.add_button_product_checkout.configure(state='disabled')
        self.Add_to_Treeview_Checkout_Brand()


    def Insert_Checkout_Entry(self, ):

        amount_product = self.id_entry_amount_product_checkout.get()
        if not (amount_product):
            messagebox.showerror('Error', 'Colocar uma quantidade PRODUTO.')
        else:
            num_items = self.id_entry_amount_product_checkout01.get()
            if num_items == '':
                id_items = 1
            else: 
                id_items = int(num_items) + 1

            selected_item_display = self.table_checkout_consult.focus()
            if selected_item_display:
                row = self.table_checkout_consult.item(selected_item_display)['values']
                item = f'{row[1]} - {row[2]} - {row[3]} - {row[4]}'
                print(row)
                self.table_checkout.insert('', 'end', values=[
                    row[0],
                    id_items,
                    item,
                    amount_product,
                    row[6],
                    row[5]
                    ])

            self.Sort_Treeview(self.table_checkout, 'ITEM', False)
            value_id = str(id_items)
            self.id_entry_amount_product_checkout01.delete(0, 'end')
            self.id_entry_amount_product_checkout01.insert(0, value_id)
            qts_item_checkout = self.id_entry_qts_item_checkout.get()
            if qts_item_checkout == '':
                qts_item_checkout = 0
            else:
                pass
            num_amount = int(amount_product)
            num_amount1 = int(qts_item_checkout)
            value_atu = num_amount1 + num_amount
            self.id_entry_qts_item_checkout.delete(0, 'end')
            self.id_entry_qts_item_checkout.insert(0, value_atu)

            value_product = int(row[6])
            num_sum_checkout = int(amount_product)
            sum_checkout = self.id_entry_sum_checkout.get()
            if sum_checkout == '':
                sum_checkout = 0
            else:
                pass

            value_atu_sum = num_sum_checkout * value_product
            value_atu_sum1 = value_atu_sum + float(sum_checkout)
            self.id_entry_sum_checkout.delete(0, 'end')
            self.id_entry_sum_checkout.insert(0, value_atu_sum1)

            self.id_entry_amount_product_checkout.delete(0, 'end')

        self.Clear_Entry_Checkout_Item()
        self.Clear_Entry_Checkout_Consult()


    def Update_Stock_Checkout(self, product_stock_amount_new, id_stock_product):
        connect_db = Database_Stock()
        user = self.name_user_current

        connect_db.Update_Stock_Sales(
                product_stock_amount = product_stock_amount_new,
                id = id_stock_product,
                )


    def Insert_Finish_Checkout(self, ):
        connect_db = Database_Sales()
        connect_db.Create_Sales_Table()
        user = self.name_user_current

        date = datetime.date.today()
        day = date.day
        month = date.month
        year = date.year-2000
        date_str = '{}-{}-{}'.format(day, month, year)
        date_str1 = '{}-{}-{}'.format(day, month, year)

        products = connect_db.Fetch_Cod_Sales_Day()
        print(products)
        if products == None:
            print('igual NONE')
            x2 = [0, 1, 0, 0]
            x3= date_str1
        else:
            x1 = str(products[1])
            x2 = x1.split('-')
            x3 = f'{x2[0]}-{x2[1]}-{x2[2]}'
            print('Não confirmou')

        if x3 == date_str:
            print('é igual')
            x4 = int(x2[3]) + 1
            print(f'proximo é {date_str}-{x4}')
            date = datetime.date.today()
            day = date.day
            month = date.month
            year = date.year-2000
            date_str = '{}-{}-{}'.format(day, month, year)
            num_cod = x4

            cod_sales_day = (f'{date_str}-{num_cod}')
            date_sales = date
            seller_name = user

            selected_item = self.table_checkout.get_children()
            if selected_item:
                for x in selected_item:
                    print(cod_sales_day)
                    print(date_sales)
                    print(seller_name)

                    product_stock_id = self.table_checkout.set(x,0)
                    print(product_stock_id)
                    product_name = self.table_checkout.set(x,2)
                    print(product_name)
                    amount_sales = self.table_checkout.set(x,3)
                    print(amount_sales)
                    value_item_sales = self.table_checkout.set(x,4)
                    print(value_item_sales)
                    sum_sales = int(value_item_sales) * int(amount_sales)
                    print(sum_sales)
                    form_payment = self.optionmenu_form_of_payment.get()
                    print(form_payment)
                    number_payment = self.optionmenu_number_payment.get()
                    print(number_payment)
                    stock_atu = self.table_checkout.set(x,5)
                    print(stock_atu)
                    new_stock = int(stock_atu) - int(amount_sales)
                    print(f'estoque : {new_stock}')
                    print('****')

                    connect_db.Insert_Sales(
                        cod_sales_day=cod_sales_day,
                        date_sales=date_sales,
                        seller_name=seller_name,
                        product_stock_id=product_stock_id,
                        product_name=product_name,
                        amount_sales=amount_sales,
                        value_item_sales=value_item_sales,
                        sum_sales=sum_sales,
                        form_payment=form_payment,
                        number_payment=number_payment,
                    )

                    self.Update_Stock_Checkout(
                                    product_stock_amount_new=new_stock,
                                    id_stock_product=product_stock_id
                                    )

                messagebox.showinfo('Sucesso', 'Venda Concluída.')
                self.Window_Entry_Sales()

        else:
            print('não é igual')

            date = datetime.date.today()
            day = date.day
            month = date.month
            year = date.year-2000
            date_str = '{}-{}-{}'.format(day, month, year)
            num_cod = 1

            cod_sales_day = (f'{date_str}-{num_cod}')
            date_sales = date
            seller_name = user

            selected_item = self.table_checkout.get_children()
            if selected_item:
                for x in selected_item:
                    print(cod_sales_day)
                    print(date_sales)
                    print(seller_name)

                    product_stock_id = self.table_checkout.set(x,0)
                    print(product_stock_id)
                    product_name = self.table_checkout.set(x,2)
                    print(product_name)
                    amount_sales = self.table_checkout.set(x,3)
                    print(amount_sales)
                    value_item_sales = self.table_checkout.set(x,4)
                    print(value_item_sales)
                    sum_sales = int(value_item_sales) * int(amount_sales)
                    print(sum_sales)
                    form_payment = self.optionmenu_form_of_payment.get()
                    print(form_payment)
                    number_payment = self.optionmenu_number_payment.get()
                    print(number_payment)
                    stock_atu = self.table_checkout.set(x,5)
                    print(stock_atu)
                    new_stock = int(stock_atu) - int(amount_sales)
                    print(f'estoque : {new_stock}')
                    print('****')

                    connect_db.Insert_Sales(
                        cod_sales_day=cod_sales_day,
                        date_sales=date_sales,
                        seller_name=seller_name,
                        product_stock_id=product_stock_id,
                        product_name=product_name,
                        amount_sales=amount_sales,
                        value_item_sales=value_item_sales,
                        sum_sales=sum_sales,
                        form_payment=form_payment,
                        number_payment=number_payment,
                    )
                    self.Update_Stock_Checkout(
                        product_stock_amount_new=new_stock,
                        id_stock_product=product_stock_id
                        )

                messagebox.showinfo('Sucesso', 'Venda Concluída.')
                self.Window_Entry_Sales()


    def Delete_Checkout_Item(self, ):
        qts_item_checkout = self.id_entry_qts_item_checkout.get()
        sum_checkout = self.id_entry_sum_checkout.get()
        item_delete = self.id_entry_edit_item_checkout.get()
        selected_item_display = self.table_checkout.focus()
        if selected_item_display:
            row = self.table_checkout.item(selected_item_display)['values']
            qts_items = float(row[3])
            value_item = float(row[4])
            sum_value = qts_items * value_item
            new_sum_value = float(sum_checkout) - float(sum_value)
            new_item_checkout = int(qts_item_checkout) - int(qts_items)

            self.id_entry_qts_item_checkout.delete(0, 'end')
            self.id_entry_qts_item_checkout.insert(0, new_item_checkout)
            self.id_entry_sum_checkout.delete(0, 'end')
            self.id_entry_sum_checkout.insert(0, new_sum_value)
            self.id_entry_edit_item_checkout.delete(0, 'end')
            selected_item = self.table_checkout.selection()[0]
            self.table_checkout.delete(selected_item)
        messagebox.showinfo('Sucesso', 'Item EXCLUÍDO.')


    def Add_to_Treeview_Checkout_Brand(self, ):
        brands_names = self.Search_Product_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        model_names = self.Search_Product_Model()
        item_model = []
        for x in model_names:
            y = str(x)
            k = y.split(': ')
            item_model.append(k)

        product_names = self.Search_Product_Product_Name()
        name_product = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            name_product.append(k)

        product_color = self.Search_Product_Product_Color()
        color_product = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_product.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()
        self.table_checkout_consult.delete(*self.table_checkout_consult.get_children())
        brand_choice = self.optionmenu_brand_name_checkout.get()

        if brand_choice == 'Escolha MARCA':
            for product in products:
                id_p=product[0]
                bra=product[2]
                mod=product[3]
                pro=product[4]
                col=product[5]
                qts=product[6]
                val=product[7]
                bran=''
                model=''
                prod=''
                colo=''
                for num, namebrand in item_brands:
                    if int(num) == bra:
                        bran=namebrand
                        for num1, namemodel in item_model:
                            if int(num1) == mod:
                                model=namemodel
                                for num2, nameproduct in name_product:
                                    if int(num2) == pro:
                                        prod=nameproduct
                                        for num3, colorproduct in color_product:
                                            if int(num3) == col:
                                                colo=colorproduct
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass

                self.table_checkout_consult.insert('', 'end', values=[id_p,bran,model,prod,colo, qts, val])

            self.Sort_Treeview(self.table_checkout_consult, 'MARCA', False)
        else:
            for num, namebrand in item_brands:
                if namebrand == brand_choice:
                    brandnum =num
                        
            for product in products:
                if product[2] == int(brandnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    val=product[7]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_model:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, nameproduct in name_product:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            for num3, colorproduct in color_product:
                                                if int(num3) == col:
                                                    colo=colorproduct
                                                else:
                                                    pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_checkout_consult.insert('', 'end', values=[id_p,bran,model,prod,colo, qts, val])
                self.Sort_Treeview(self.table_checkout_consult, 'MODELO', False)


    def Search_Checkout_Treeview_One(self):
        brand_name = self.optionmenu_brand_name_checkout.get().upper()

        connect_db_brand = Database_Brand()
        brands = connect_db_brand.Fetch_Brand()
        for brand in brands:
            if brand[2] == brand_name:
                id_brand_color = int(brand[0])
                return id_brand_color
            else:
                pass

    def Search_Checkout_Treeview_Two(self):
        id_brand = self.Search_Checkout_Treeview_One()

        model_name = self.optionmenu_model_name_checkout.get().upper()

        connect_db_model = Database_Model()
        models = connect_db_model.Fetch_Model()
        for model in models:
            if model[3] == model_name:
                if model[2] == id_brand:
                    id_model = int(model[0])
                    return id_brand, id_model
            else:
                pass


    def Add_to_Treeview_Checkout_Model(self, ):
        id_brand_product = self.Search_Checkout_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_checkout_consult.delete(*self.table_checkout_consult.get_children())
        model_choice = self.optionmenu_model_name_checkout.get()

        if model_choice == 'Escolha MARCA':
            pass

        else:
            for product in products:
                if product[3] == int(id_brand_product[1]):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    val=product[7]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_checkout_consult.insert('', 'end', values=[id_p,bran,model,prod, colo, qts, val])
                self.Sort_Treeview(self.table_checkout_consult, 'PRODUTO', False)


    def Add_to_Treeview_Checkout_Product(self, ):

        id_brand_product = self.Search_Checkout_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_checkout_consult.delete(*self.table_checkout_consult.get_children())
        product_choice = self.optionmenu_product_name_checkout.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        if product_choice == 'Escolha PPRODUTO':
            pass

        else:
            for product in products:
                if product[4] == int(prodnum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    val=product[7]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_checkout_consult.insert('', 'end', values=[id_p,bran,model,prod, colo, qts, val])
                self.Sort_Treeview(self.table_checkout_consult, 'COR', False)



    def Add_to_Treeview_Checkout_Color(self, ):

        id_brand_product = self.Search_Checkout_Treeview_Two()

        brands_names = self.Search_Color_Brand()
        item_brands = []
        for x in brands_names:
            y = str(x)
            k = y.split(': ')
            item_brands.append(k)

        models_names = self.Search_Color_Model()
        item_models = []
        for x in models_names:
            y = str(x)
            k = y.split(': ')
            item_models.append(k)

        product_names = self.Search_Color_Product_Two()
        item_products = []
        for x in product_names:
            y = str(x)
            k = y.split(': ')
            item_products.append(k)

        product_color = self.Search_Product_Product_Color()
        color_products = []
        for x in product_color:
            y = str(x)
            k = y.split(': ')
            color_products.append(k)

        products_colors = self.Search_Color_Color()
        colors_products = []
        for x in products_colors:
            y = str(x)
            k = y.split(': ')
            colors_products.append(k)

        product_choice = self.optionmenu_product_name_checkout.get()
        color_choice = self.optionmenu_color_name_checkout.get()

        for num2, namemodel, nameproduct in item_products:
            if int(namemodel) == int(id_brand_product[1]):
                if product_choice == nameproduct:
                    prodnum=num2

        for num_color, num_product_color, color in colors_products:
            if color_choice == color:
                if prodnum == num_product_color:
                    colornum=num_color

        connect_db = Database_Stock()
        products = connect_db.Fetch_Stock()

        self.table_checkout_consult.delete(*self.table_checkout_consult.get_children())

        if color_choice == 'Escolha COR':
            pass
        else:
            for product in products:
                if product[5] == int(colornum):
                    id_p=product[0]
                    bra=product[2]
                    mod=product[3]
                    pro=product[4]
                    col=product[5]
                    qts=product[6]
                    val=product[7]
                    bran=''
                    model=''
                    prod=''
                    colo=''
                    for num, namebrand in item_brands:
                        if int(num) == bra:
                            bran=namebrand
                            for num1, namemodel in item_models:
                                if int(num1) == mod:
                                    model=namemodel
                                    for num2, namemodel, nameproduct in item_products:
                                        if int(num2) == pro:
                                            prod=nameproduct
                                            print(prod)
                                            for num3, colorproduct in color_products:
                                                if int(num3) == col:
                                                    colo=colorproduct

                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    self.table_checkout_consult.insert('', 'end', values=[id_p,bran,model,prod, colo, qts, val])
                self.Sort_Treeview(self.table_checkout_consult, 'COR', False)


        # **************** DEFVENDASFRENTE  ************************


        # **************** DEFRELATORIO  ************************

    def Clear_Entry_Checkout_Report(self, *clicked):
        if clicked:
            self.table_checkout_report.selection_remove(self.table_checkout_report.focus())
            self.table_checkout_report.focus('')
        self.optionmenu_date_report.configure(state='normal')
        self.optionmenu_date_report.set('Escolha Data')
        self.optionmenu_seller_name_report.configure(state='normal')
        self.optionmenu_seller_name_report.set('Escolha Data')
        self.Add_to_Treeview_Report()
        self.Clear_Chart()
        self.Create_Chart()


    def Clear_Chart(self, ):
        self.canvas.get_tk_widget().destroy()


    def Create_Chart(self, datex=''):

        selected_display = self.table_checkout_report.get_children()
        qts_items = len(selected_display)
        sale_day = ''
        sales_day = []
        stock_values = []
        sum_value1 = 0

        for item in selected_display:
            row = self.table_checkout_report.item(item)['values']
            if sale_day == '':
                sales_day.append(row[1])
                sale_day = row[1]
                sum_value1 = row[7]

            elif row[1] == sale_day:
                sum_value1 += row[7]

            elif row[1] != sale_day:
                sales_day.append(row[1])
                sale_day = row[1]
                stock_values.append(sum_value1)
                sum_value1 = row[7]

        stock_values.append(sum_value1)
        sum_sales = 0
        for sum_sale in stock_values:
            sum_sales += sum_sale

        if datex == '':
            self.figure = Figure(figsize=(15, 8), dpi=80, facecolor='#0A0B0C')
            self.ax = self.figure.add_subplot(111)
            self.ax.bar(sales_day, stock_values, width=0.1, color='#2fa572')
            self.ax.set_xlabel('', color='#fff', fontsize=30)
            self.ax.set_ylabel('R$', color='#fff', fontsize=30)
            self.ax.set_title(f'RELATÓRIO TOTAL VENDAS R$ {sum_sales}', color='#fff', fontsize=20)
            self.ax.tick_params(axis='y', labelcolor='#fff', labelsize=20)
            self.ax.tick_params(axis='x', labelcolor='#fff', labelsize=20)
            self.ax.set_facecolor('#1B181B')

            self.canvas = FigureCanvasTkAgg(self.figure, self.frame_internal_report_01)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill = 'both', expand = False)
        else:
            self.figure = Figure(figsize=(15, 8), dpi=80, facecolor='#0A0B0C')
            self.ax = self.figure.add_subplot(111)
            self.ax.bar(sales_day, stock_values, width=0.1, color='#2fa572')
            self.ax.set_xlabel('', color='#fff', fontsize=30)
            self.ax.set_ylabel('R$', color='#fff', fontsize=30)
            self.ax.set_title(f'RELATÓRIO TOTAL VENDAS R$ {sum_sales}', color='#fff', fontsize=20)
            self.ax.tick_params(axis='y', labelcolor='#fff', labelsize=20)
            self.ax.tick_params(axis='x', labelcolor='#fff', labelsize=20)
            self.ax.set_facecolor('#1B181B')

            self.canvas = FigureCanvasTkAgg(self.figure, self.frame_internal_report_01)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill = 'both', expand = False)


    def Add_to_Treeview_Report(self, ):

        connect_db = Database_Sales()
        products = connect_db.Fetch_Sales()
        self.table_checkout_report.delete(*self.table_checkout_report.get_children())
        date_choice = self.optionmenu_date_report.get()

        if date_choice == 'Escolha Data':
            for product in products:
                id_p=product[0]
                dat=product[2]
                cod=product[1]
                sel=product[3]
                ite=product[5]
                qts=product[6]
                val=product[7]
                tot=product[8]
                pag=product[9]
                par=product[10]

                self.table_checkout_report.insert('', 'end', values=[id_p,dat,cod,sel,ite, qts, val, tot, pag, par])
            self.Sort_Treeview(self.table_checkout_report, 'DATA', False)
        else:
            pass


    def Add_to_Treeview_Report_Date(self, ):

        connect_db = Database_Sales()
        products = connect_db.Fetch_Sales()
        self.table_checkout_report.delete(*self.table_checkout_report.get_children())
        date_choice = self.optionmenu_date_report.get()

        if date_choice == 'Escolha Data':
            pass
        else:
            for product in products:
                if product[2] == date_choice:
                    id_p=product[0]
                    dat=product[2]
                    cod=product[1]
                    sel=product[3]
                    ite=product[5]
                    qts=product[6]
                    val=product[7]
                    tot=product[8]
                    pag=product[9]
                    par=product[10]
                    self.table_checkout_report.insert('', 'end', values=[id_p,dat,cod,sel,ite, qts, val, tot, pag, par])
                self.Sort_Treeview(self.table_checkout_report, 'DATA', False)
            self.Clear_Chart()
            self.Create_Chart(datex=date_choice)


    def Add_to_Treeview_Report_Date_Seller(self, ):

        connect_db = Database_Sales()
        products = connect_db.Fetch_Sales()
        self.table_checkout_report.delete(*self.table_checkout_report.get_children())
        date_choice = self.optionmenu_date_report.get()
        seller_choice = self.optionmenu_seller_name_report.get()

        if seller_choice == 'Escolha Data':
            pass
        else:
            for product in products:
                if product[2] == date_choice:
                    if product[3] == seller_choice:
                        id_p=product[0]
                        dat=product[2]
                        cod=product[1]
                        sel=product[3]
                        ite=product[5]
                        qts=product[6]
                        val=product[7]
                        tot=product[8]
                        pag=product[9]
                        par=product[10]
                        self.table_checkout_report.insert('', 'end', values=[id_p,dat,cod,sel,ite, qts, val, tot, pag, par])
                self.Sort_Treeview(self.table_checkout_report, 'DATA', False)
            self.Clear_Chart()
            self.Create_Chart(datex=date_choice)


        # **************** DEFRELATORIO  ************************


    def __init__(self):
        super().__init__()  

        self.font1 = ('', 25, 'bold')
        self.font2 = ('', 18, 'bold')
        self.font3 = ('', 13, 'bold')

        self.verde_claro = '#2fa572'
        self.cinza_claro = '#c2e4ee'
        self.cinza_escuro = '#2b2b2b'
        self.cinza_fundo = '#333333'
        self.vermelho = '#ff0000'
        
        self.window_login = customtkinter.CTkFrame(
            self, corner_radius=10
            )
        self.window_login.pack(fill=tkinter.BOTH,
                         expand=True,
                         padx=10,
                         pady=10
                         )
        self.iconbitmap('logo_fevox1.ico')
        self.title("LOGIN FEVOX")
        self.geometry("500x430")

        self.tabview = customtkinter.CTkTabview(
        master=self.window_login,
        segmented_button_fg_color= self.verde_claro,
        text_color=self.cinza_claro,
        segmented_button_selected_color= self.verde_claro,
        segmented_button_selected_hover_color= self.verde_claro,
        )
        self.tabview._segmented_button.configure(
            font=('DejaVu Sans Mono', 30, 'bold')
            )
        self.tabview.pack(
            fill='both', expand=1, padx=10, pady=10
            )
        self.a_name = f'{"FEVOX"}'
        self.tabview.add(self.a_name)

        self.text_user_login = customtkinter.CTkLabel(
            master=self.tabview.tab(self.a_name),
            text='LOGIN',
            font=("", 20, 'bold'),
            text_color= self.cinza_claro
            )
        self.text_user_login.pack(padx=10, pady=10)
        
        self.user_entry_login = customtkinter.CTkEntry(
            master=self.tabview.tab(self.a_name),
            placeholder_text="Seu Login"
            )
        self.user_entry_login.pack(
            ipadx=250, ipady=15, padx=10, pady=10
            )

        self.pass_entry_login = customtkinter.CTkEntry(
            master=self.tabview.tab(self.a_name),
            placeholder_text="Sua Senha",
            show="*"
            )
        self.pass_entry_login.pack(
            ipadx=250, ipady=15, padx=10, pady=10
            )

        self.show_pass_checkbox = customtkinter.CTkCheckBox(
            master=self.tabview.tab(self.a_name),
            text='Mostrar Senha',
            command=self.Show_Pass_Login
        )
        self.show_pass_checkbox.pack(padx=0, pady=0)

        self.btn_access_login = customtkinter.CTkButton(
            master=self.tabview.tab(self.a_name),
            text="Acessar",
            font=("", 20),
            bg_color=self.cinza_escuro,
            command=self.Confirm_login
            )
        self.btn_access_login.pack(ipady=15, padx=10, pady=10)

        self.btn_create_user = customtkinter.CTkButton(
            master=self.tabview.tab(self.a_name),
            text="criar usuário",
            font=("", 15, 'underline'),
            fg_color='transparent',
            bg_color='transparent',
            command=self.Window_Register_User
            )
        self.btn_create_user.pack(ipady=0, pady=0)



    def Window_Register_User(self):
        self.window_login.destroy()

        self.window_register_user = customtkinter.CTkFrame(
            self, corner_radius=10
            )
        self.window_register_user.pack(fill=tkinter.BOTH,
                         expand=True,
                         padx=10,
                         pady=10
                         )
        
        self.title("CADASTRO USUÁRIO FEVOX")
        self.geometry("500x470")

        self.tabview = customtkinter.CTkTabview(
        master=self.window_register_user,
        segmented_button_fg_color= self.verde_claro,
        text_color=self.cinza_claro,
        segmented_button_selected_color= self.verde_claro,
        segmented_button_selected_hover_color= self.verde_claro,
        )
        self.tabview._segmented_button.configure(
            font=('DejaVu Sans Mono', 30, 'bold')
            )
        self.tabview.pack(
            fill='both', expand=1, padx=10, pady=10
            )
        self.b_name = f'{"FEVOX"}'
        self.tabview.add(self.a_name)

        self.text_user_register = customtkinter.CTkLabel(
            master=self.tabview.tab(self.b_name),
            text='CADASTRO USUÁRIO',
            font=("", 20, 'bold'),
            text_color= self.cinza_claro
            )
        self.text_user_register.pack(padx=10, pady=10)

        self.name_entry_register = customtkinter.CTkEntry(
            master=self.tabview.tab(self.b_name),
            placeholder_text="Seu Nome"
            )
        self.name_entry_register.pack(
            ipadx=250, ipady=15, padx=10, pady=10
            )
        
        self.user_entry_register = customtkinter.CTkEntry(
            master=self.tabview.tab(self.b_name),
            placeholder_text="Seu Email"
            )
        self.user_entry_register.pack(
            ipadx=250, ipady=15, padx=10, pady=10
            )

        self.pass_entry_register = customtkinter.CTkEntry(
            master=self.tabview.tab(self.b_name),
            placeholder_text="Sua Senha",
            show="*"
            )
        self.pass_entry_register.pack(
            ipadx=250, ipady=15, padx=10, pady=10
            )
        
        self.show_pass_checkbox_register = customtkinter.CTkCheckBox(
            master=self.tabview.tab(self.b_name),
            text='Mostrar Senha',
            command=self.Show_Pass_Register
        )
        self.show_pass_checkbox_register.pack(padx=0, pady=0)

        self.btn_register_login = customtkinter.CTkButton(
            master=self.tabview.tab(self.b_name),
            text="Criar Usuário",
            font=("", 20),
            bg_color=self.cinza_escuro,
            command=self.Register_User_New
            )
        self.btn_register_login.pack(ipady=15, padx=10, pady=10)



    def Window_App(self, janela, user):

        janela.destroy()
        self.name_user_current = str(user)
        name_user = str(user).split()
        self.title("FEVOX GERENCIAMENTO")

        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth(),
            self.winfo_screenheight()
            ))

        self.font1 = ('', 25, 'bold')
        self.font2 = ('', 18, 'bold')
        self.font3 = ('', 13, 'bold')
        self.verde_claro = '#2fa572'

        # root!
        self.main_container = customtkinter.CTkFrame(
            self, corner_radius=10
            )
        self.main_container.pack(
            fill=tkinter.BOTH, expand=True, padx=10, pady=10
            )

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkFrame(
            self.main_container, width=150, corner_radius=10
            )
        self.left_side_panel.pack(
            side=tkinter.LEFT,
            fill=tkinter.Y,
            expand=False,
            padx=5,
            pady=5
            )

        self.left_side_panel.grid_columnconfigure(
            0, weight=1
            )
        self.left_side_panel.grid_rowconfigure(
            (0, 1, 2, 3, 4, 5, 6, 7), weight=0
            )
        self.left_side_panel.grid_rowconfigure(
            (8, 9, 10), weight=1
            )


        # self.left_side_panel WIDGET
        image1 = customtkinter.CTkImage(Image.open('logo_fevox1.ico'), size=(90, 90))
        image1_label = customtkinter.CTkLabel(
            master=self.left_side_panel,
            text='',
            image=image1
            )
        image1_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10)
            )

        self.logo_label = customtkinter.CTkLabel(
            self.left_side_panel,
            text=f"WELCOME!\n{name_user[0]}",
            font=customtkinter.CTkFont(
                size=20,
                weight="bold"
                )
                )
        self.logo_label.grid(
            row=2,
            column=0,
            padx=20,
            pady=(20, 10)
            )

        # button to select correct frame IN self.left_side_panel WIDGET
        self.btn_brand_registration = customtkinter.CTkButton(
            self.left_side_panel,
            text="Cadastrar",
            command=self.Window_Product_Registration
            )
        self.btn_brand_registration.grid(
            row=3,
            column=0,
            padx=20,
            pady=10
            )

        self.btn_stock_registration = customtkinter.CTkButton(
            self.left_side_panel,
            text="Estoque",
            command=self.Window_Product_Registration_Stock
            )
        self.btn_stock_registration.grid(
            row=4,
            column=0,
            padx=20,
            pady=10
            )

        self.btn_Invoice = customtkinter.CTkButton(
            self.left_side_panel,
            text="Entrada Notas",
            command=self.Window_Entry_Invoice
            )
        self.btn_Invoice.grid(
            row=5,
            column=0,
            padx=20,
            pady=10
            )
        
        self.btn_Costs = customtkinter.CTkButton(
            self.left_side_panel,
            text="Vendas",
            command=self.Window_Entry_Sales
            )
        self.btn_Costs.grid(
            row=6,
            column=0,
            padx=20,
            pady=10
            )
        
        self.btn_Report = customtkinter.CTkButton(
            self.left_side_panel,
            text="Relatório",
            command=self.Window_Report
            )
        self.btn_Report.grid(
            row=7,
            column=0,
            padx=20,
            pady=10
            )
        
        
        self.scaling_label = customtkinter.CTkLabel(
            self.left_side_panel,
            text="Dimensionamento:",
            anchor="w"
            )
        self.scaling_label.grid(
            row=11,
            column=0,
            padx=20,
            pady=(0, 0)
            )

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.left_side_panel,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event
            )
        self.scaling_optionemenu.grid(
            row=12,
            column=0,
            padx=20,
            pady=(10, 20),
            sticky = "s"
            )

        self.btn_Quit = customtkinter.CTkButton(
            self.left_side_panel,
            text="Quit",
            fg_color= '#EA0000',
            hover_color = '#B20000',
            command= self.close_window
            )
        self.btn_Quit.grid(row=13, column=0, padx=20, pady=10)



        # right side panel -> have self.right_dashboard inside it
        self.right_side_panel = customtkinter.CTkFrame(
            self.main_container,
            corner_radius=10,
            fg_color="#000811"
            )
        self.right_side_panel.pack(
            side=tkinter.LEFT,
            fill=tkinter.BOTH,
            expand=True,
            padx=5,
            pady=5
            )


        self.right_dashboard = customtkinter.CTkFrame(
            self.main_container,
            corner_radius=10,
            fg_color="#000811"
            )
        self.right_dashboard.pack(
            in_=self.right_side_panel,
            side=tkinter.TOP,
            fill=tkinter.BOTH,
            expand=True,
            padx=0,
            pady=0
            )


    #  self.right_dashboard   ----> dashboard widget
    def Window_Product_Registration(self):
        self.clear_frame()

        self.tabview  = customtkinter.CTkTabview(master=self.right_dashboard)
        self.tabview.pack(fill='both', expand=1, padx=10, pady=10)

        self.tabview.add("MARCAS")
        self.tabview.add("MODELOS")
        self.tabview.add("PRODUTOS")
        self.tabview.add("CORES")
        self.tabview.add("FORNECEDOR")
        self.tabview.add("PRESTADOR")


        # ****************  PAGE_MARCAS  ************************

        self.frame_internal_brand = customtkinter.CTkFrame(
            self.tabview.tab("MARCAS"),
            corner_radius=10,
            )
        self.frame_internal_brand.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_brand.grid_columnconfigure(1, weight=1)
        self.frame_internal_brand.grid_rowconfigure(1, weight=0)
        self.frame_internal_brand.grid_rowconfigure(0, weight=1)

        # ****************  PAGE_MARCAS  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_brand,
            font=self.font1,
            text='Marcas',
            text_color='#fff',
            )
        self.title_label.place(x=50,y=0,)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_brand,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=300
            )
        self.frame.place(x=0,y=35)

        image1 = customtkinter.CTkImage(Image.open('logo_fevox1.ico'), size=(70, 70))
        image1_label = customtkinter.CTkLabel(
            master=self.frame_internal_brand,
            text='',
            image=image1
            )
        image1_label.place(x=65,y=55)

        self.id_label_brand = customtkinter.CTkLabel(
            self.frame_internal_brand,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_brand.place(x=45,y=140)

        self.id_entry_brand = customtkinter.CTkEntry(
            self.frame_internal_brand,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160
            )
        self.id_entry_brand.place(x=20, y=170)

        self.add_button_brand = customtkinter.CTkButton(
            self.frame_internal_brand,
            font=self.font2,
            command=self.Insert_Brand,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_brand.place(x=15,y=220)

        self.clear_button_brand = customtkinter.CTkButton(
            self.frame_internal_brand,
            font=self.font2,
            command=lambda:self.Clear_Entry_Brand(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_brand.place(x=108,y=220)

        self.update_button_brand = customtkinter.CTkButton(
            self.frame_internal_brand,
            font=self.font2,
            command=self.Update_Brand,
            text_color='#fff',
            text='Update',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.update_button_brand.place(x=15,y=280)

        self.delete_button_brand = customtkinter.CTkButton(
            self.frame_internal_brand,
            font=self.font2,
            command=self.Delete_Brand,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.delete_button_brand.place(x=108,y=280)

        self.frame_internal_brand_01 = customtkinter.CTkFrame(
            self.tabview.tab("MARCAS"),
            corner_radius=10,
            )
        self.frame_internal_brand_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50
            )
        self.frame_internal_brand_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_brand_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_brand_01.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self.frame_internal_brand_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_brands = ttk.Treeview(self.frame_internal_brand_01, height=25)
        self.table_brands['columns'] = ('ID', 'NOME', 'MARCA')
        self.table_brands.column('#0', width=0, stretch=tkinter.NO)
        self.table_brands.column('ID', anchor=tkinter.CENTER, width=350)
        self.table_brands.column('NOME', anchor=tkinter.CENTER, width=350)
        self.table_brands.column('MARCA', anchor=tkinter.CENTER, width=350)

        self.table_brands.heading('ID', text = 'ID')
        self.table_brands.heading('NOME', text = 'NOME')
        self.table_brands.heading('MARCA', text = 'MARCA')
        self.table_brands.pack(fill = 'both', expand = False)

        self.table_brands.bind('<ButtonRelease>', self.Display_Data_Brand)

        self.Add_to_Treeview_Brand()

        # ****************  PAGE_MARCAS  ************************


        # ****************  PAGE_MODELOS  ************************


        self.frame_internal_model = customtkinter.CTkFrame(
            self.tabview.tab("MODELOS"),
            corner_radius=10,
            )
        self.frame_internal_model.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_model.grid_columnconfigure(1, weight=1)
        self.frame_internal_model.grid_rowconfigure(1, weight=0)
        self.frame_internal_model.grid_rowconfigure(0, weight=1)

        # ****************  PAGE_MODELOS  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_model,
            font=self.font1,
            text='Modelos',
            text_color='#fff',
            )
        self.title_label.place(x=50,y=0,)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_model,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=370
            )
        self.frame.place(x=0,y=35)

        image1 = customtkinter.CTkImage(Image.open('logo_fevox1.ico'), size=(70, 70))
        image1_label = customtkinter.CTkLabel(
            master=self.frame_internal_model,
            text='',
            image=image1
            )
        image1_label.place(x=65,y=55)

        self.id_label_model = customtkinter.CTkLabel(
            self.frame_internal_model,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model.place(x=45,y=140)

        brands_option = []
        connect_db = Database_Brand()
        brands = connect_db.Fetch_Brand()
        for product in brands:
            brands_option.append(product[2])
        brands_in_order = sorted(brands_option)

        def optionmenu_callback_model(choice):
            self.Add_to_Treeview_Model()

        self.optionmenu_model = customtkinter.CTkOptionMenu(
            self.frame_internal_model,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=optionmenu_callback_model

            )
        self.optionmenu_model.set('Escolha MARCA')
        self.optionmenu_model.place(x=20, y=170)

        self.id_label_model = customtkinter.CTkLabel(
            self.frame_internal_model,
            font=self.font2,
            text='Nome Modelo:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model.place(x=40,y=210)

        self.id_entry_model = customtkinter.CTkEntry(
            self.frame_internal_model,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160
            )
        self.id_entry_model.place(x=20, y=240)

        self.add_button_model = customtkinter.CTkButton(
            self.frame_internal_model,
            font=self.font2,
            command=self.Insert_Model,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_model.place(x=15,y=290)

        self.clear_button_model = customtkinter.CTkButton(
            self.frame_internal_model,
            font=self.font2,
            command=lambda:self.Clear_Entry_Model(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_model.place(x=108,y=290)

        self.update_button_model = customtkinter.CTkButton(
            self.frame_internal_model,
            font=self.font2,
            command=self.Update_Model,
            text_color='#fff',
            text='Update',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.update_button_model.place(x=15,y=350)

        self.delete_button_model = customtkinter.CTkButton(
            self.frame_internal_model,
            font=self.font2,
            command=self.Delete_Model,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.delete_button_model.place(x=108,y=350)

        self.frame_internal_model_01 = customtkinter.CTkFrame(
            self.tabview.tab("MODELOS"),
            corner_radius=10,
            )
        self.frame_internal_model_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50
            )
        self.frame_internal_model_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_model_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_model_01.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self.frame_internal_model_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_models = ttk.Treeview(self.frame_internal_model_01, height=50)
        self.table_models['columns'] = ('ID', 'NOME', 'MARCA', 'MODELO')
        self.table_models.column('#0', width=0, stretch=tkinter.NO)
        self.table_models.column('ID', anchor=tkinter.CENTER, width=350)
        self.table_models.column('NOME', anchor=tkinter.CENTER, width=350)
        self.table_models.column('MARCA', anchor=tkinter.CENTER, width=350)
        self.table_models.column('MODELO', anchor=tkinter.CENTER, width=350)

        self.table_models.heading('ID', text = 'ID')
        self.table_models.heading('NOME', text = 'NOME')
        self.table_models.heading('MARCA', text = 'MARCA')
        self.table_models.heading('MODELO', text = 'MODELO')
        self.table_models.pack(fill = 'both', expand = False)

        self.table_models.bind('<ButtonRelease>', self.Display_Data_Model)

        self.Add_to_Treeview_Model()

        # ****************  PAGE_MODELOS  ************************


        # ****************  PAGE_PRODUTOS  ************************

        self.frame_internal_product = customtkinter.CTkFrame(
            self.tabview.tab("PRODUTOS"),
            corner_radius=10,
            )
        self.frame_internal_product.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_product.grid_columnconfigure(1, weight=1)
        self.frame_internal_product.grid_rowconfigure(1, weight=0)
        self.frame_internal_product.grid_rowconfigure(0, weight=1)

        # ****************  PAGE_PRODUTOS  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_product,
            font=self.font1,
            text='Produtos',
            text_color='#fff',
            )
        self.title_label.place(x=40,y=0,)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_product,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=440
            )
        self.frame.place(x=0,y=35)

        image1 = customtkinter.CTkImage(Image.open('logo_fevox1.ico'), size=(70, 70))
        image1_label = customtkinter.CTkLabel(
            master=self.frame_internal_product,
            text='',
            image=image1
            )
        image1_label.place(x=65,y=55)

        self.id_label_product = customtkinter.CTkLabel(
            self.frame_internal_product,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product.place(x=45,y=140)

        brands_option_product = []
        connect_db = Database_Brand()
        brands_products = connect_db.Fetch_Brand()
        for brands in brands_products:
            brands_option_product.append(brands[2])
        brands_in_order = sorted(brands_option_product)

        def Option_Brand_Callback_Product(choice):
            # print("optionmenu dropdown clicked:", choice)
            Start_Option_Product_Brand(choice=choice)
            self.Add_to_Treeview_Product()


        self.optionmenu_brand_product = customtkinter.CTkOptionMenu(
            self.frame_internal_product,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Product
            )
        self.optionmenu_brand_product.set('Escolha MARCA')
        self.optionmenu_brand_product.place(x=20, y=170)

        self.id_label_model_product = customtkinter.CTkLabel(
            self.frame_internal_product,
            font=self.font2,
            text='Nome Modelo:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model_product.place(x=35,y=210)


        def Start_Option_Product_Brand(choice):
            brands_names = self.Search_Product_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == choice:
                    bran=int(numbrand)

            models_0123 = []
            connect_db = Database_Model()
            models_products = connect_db.Fetch_Model()
            for brands in models_products:
                if brands[2] == bran:
                    models_0123.append(brands[3])
            models_in_order = sorted(models_0123)
            if not models_0123:
                self.optionmenu_model_product = customtkinter.CTkOptionMenu(
                    self.frame_internal_product,
                    dynamic_resizing=False,
                    values=['SEM MODELOS'],
                    width=160,
                    command=Option_Brand_Callback_Model
                    )
                self.optionmenu_model_product.place(x=20, y=240)
            else:
                self.optionmenu_model_product = customtkinter.CTkOptionMenu(
                    self.frame_internal_product,
                    dynamic_resizing=False,
                    values=models_in_order,
                    width=160,
                    command=Option_Brand_Callback_Model
                    )
                self.optionmenu_model_product.set('Escolha MODELO')
                self.optionmenu_model_product.place(x=20, y=240)


        def Option_Brand_Callback_Model(choice):
            self.Add_to_Treeview_Product_Model()


        self.optionmenu_model_product = customtkinter.CTkOptionMenu(
            self.frame_internal_product,
            dynamic_resizing=False,
            values=['Escolha MODELO'],
            width=160,
            command=Option_Brand_Callback_Model
            )
        self.optionmenu_model_product.place(x=20, y=240)

        self.id_label_product = customtkinter.CTkLabel(
            self.frame_internal_product,
            font=self.font2,
            text='Nome Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product.place(x=35,y=280)

        self.id_entry_product = customtkinter.CTkEntry(
            self.frame_internal_product,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160
            )
        self.id_entry_product.place(x=20, y=310)

        self.add_button_product = customtkinter.CTkButton(
            self.frame_internal_product,
            font=self.font2,
            command=self.Insert_Product,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_product.place(x=15,y=360)

        self.clear_button_product = customtkinter.CTkButton(
            self.frame_internal_product,
            font=self.font2,
            command=lambda:self.Clear_Entry_Product(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_product.place(x=108,y=360)

        self.update_button_product = customtkinter.CTkButton(
            self.frame_internal_product,
            font=self.font2,
            command=self.Update_Product,
            text_color='#fff',
            text='Update',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.update_button_product.place(x=15,y=420)

        self.delete_button_product = customtkinter.CTkButton(
            self.frame_internal_product,
            font=self.font2,
            command=self.Delete_Product,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.delete_button_product.place(x=108,y=420)

        self.frame_internal_product_01 = customtkinter.CTkFrame(
            self.tabview.tab("PRODUTOS"),
            corner_radius=10,
            )
        self.frame_internal_product_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50
            )
        self.frame_internal_product_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_product_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_product_01.grid_rowconfigure(0, weight=1)


        style = ttk.Style(self.frame_internal_product_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_product = ttk.Treeview(self.frame_internal_product_01, height=50,)
        self.table_product['columns'] = ('ID','MARCA', 'MODELO', 'PRODUTO')
        self.table_product.column('#0', width=0, stretch=tkinter.NO)
        self.table_product.column('ID', anchor=tkinter.CENTER, width=200)
        self.table_product.column('MARCA', anchor=tkinter.CENTER, width=300)
        self.table_product.column('MODELO', anchor=tkinter.CENTER, width=300)
        self.table_product.column('PRODUTO', anchor=tkinter.CENTER, width=700)

        self.table_product.heading('ID', text = 'ID')
        self.table_product.heading('MARCA', text = 'MARCA')
        self.table_product.heading('MODELO', text = 'MODELO')
        self.table_product.heading('PRODUTO', text = 'PRODUTO')
        self.table_product.pack(fill = 'both', expand = False)

        self.table_product.bind('<ButtonRelease>', self.Display_Data_Product)

        self.Add_to_Treeview_Product()

        # ****************  PAGE_PRODUTOS  ************************


        # ****************  PAGE_CORES  ************************

        self.frame_internal_color = customtkinter.CTkFrame(
            self.tabview.tab("CORES"),
            corner_radius=10,
            )
        self.frame_internal_color.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_color.grid_columnconfigure(1, weight=1)
        self.frame_internal_color.grid_rowconfigure(1, weight=0)
        self.frame_internal_color.grid_rowconfigure(0, weight=1)

        # ****************  PAGE_CORES  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_color,
            font=self.font1,
            text='Cores',
            text_color='#fff',
            )
        self.title_label.place(x=50,y=0,)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_color,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=510
            )
        self.frame.place(x=0,y=35)

        image1 = customtkinter.CTkImage(Image.open('logo_fevox1.ico'), size=(70, 70))
        image1_label = customtkinter.CTkLabel(
            master=self.frame_internal_color,
            text='',
            image=image1
            )
        image1_label.place(x=65,y=55)

        self.id_label_brand_color = customtkinter.CTkLabel(
            self.frame_internal_color,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_brand_color.place(x=45,y=140)

        brands_option_color = []
        connect_db = Database_Brand()
        brands_color = connect_db.Fetch_Brand()
        for brands in brands_color:
            brands_option_color.append(brands[2])
        brands_in_order = sorted(brands_option_color)

        def Option_Brand_Callback_Brand_Color(choice):
            Start_Option_Color_Brand(choice=choice)
            self.Add_to_Treeview_Color()


        self.optionmenu_brand_color = customtkinter.CTkOptionMenu(
            self.frame_internal_color,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Brand_Color
            )
        self.optionmenu_brand_color.set('Escolha MARCA')
        self.optionmenu_brand_color.place(x=20, y=170)

        self.id_label_model_color = customtkinter.CTkLabel(
            self.frame_internal_color,
            font=self.font2,
            text='Nome Modelo:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model_color.place(x=35,y=210)

        def Start_Option_Color_Brand(choice):
            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == choice:
                    bran=int(numbrand)

            models_0123 = []
            connect_db = Database_Model()
            models_products = connect_db.Fetch_Model()
            for brands in models_products:
                if brands[2] == bran:
                    models_0123.append(brands[3])
            models_in_order = sorted(models_0123)
            if not models_0123:
                self.optionmenu_model_color = customtkinter.CTkOptionMenu(
                    self.frame_internal_color,
                    dynamic_resizing=False,
                    values=['SEM MODELOS'],
                    width=160,
                    command=Option_Model_Callback_Model_Color
                    )
                self.optionmenu_model_color.place(x=20, y=240)
            else:
                self.optionmenu_model_color = customtkinter.CTkOptionMenu(
                    self.frame_internal_color,
                    dynamic_resizing=False,
                    values=models_in_order,
                    width=160,
                    command=Option_Model_Callback_Model_Color
                    )
                self.optionmenu_model_color.set('Escolha MODELO')
                self.optionmenu_model_color.place(x=20, y=240)


        def Option_Model_Callback_Model_Color(choice):
            Start_Option_Color_Model(choice=choice)
            self.Add_to_Treeview_Color_Model()


        self.optionmenu_model_color = customtkinter.CTkOptionMenu(
            self.frame_internal_color,
            dynamic_resizing=False,
            values=['Escolha MODELO'],
            width=160,
            command=Option_Model_Callback_Model_Color
            )
        self.optionmenu_model_color.place(x=20, y=240)

        self.id_label_product_color = customtkinter.CTkLabel(
            self.frame_internal_color,
            font=self.font2,
            text='Nome Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_color.place(x=35,y=280)


        def Start_Option_Color_Model(choice):
            brand_choice = self.optionmenu_brand_color.get()
            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)
            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass
            product_0123 = []
            connect_db = Database_Product()
            models_color = connect_db.Fetch_Product()
            for models in models_color:
                if models[2] == bran:
                    if models[3] == modelnum:
                        product_0123.append(models[4])

            product_in_order = set(product_0123)
            product_in_order01 = sorted(product_in_order)
            if not product_0123:
                print('vazio')
                self.optionmenu_product_color = customtkinter.CTkOptionMenu(
                    self.frame_internal_color,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Product_Callback_Product_Color
                    )
                self.optionmenu_product_color.place(x=20, y=310) 
            else:
                print(product_0123)
                self.optionmenu_product_color = customtkinter.CTkOptionMenu(
                    self.frame_internal_color,
                    dynamic_resizing=False,
                    values=product_in_order01,
                    width=160,
                    command=Option_Product_Callback_Product_Color
                    )
                self.optionmenu_product_color.set('Escolha PRODUTO')
                self.optionmenu_product_color.place(x=20, y=310) 

        def Option_Product_Callback_Product_Color(choice):
            self.Add_to_Treeview_Color_Product()

        self.optionmenu_product_color = customtkinter.CTkOptionMenu(
            self.frame_internal_color,
            dynamic_resizing=False,
            values=['Escolha PRODUTO'],
            width=160,
            command=Option_Product_Callback_Product_Color
            )
        self.optionmenu_product_color.place(x=20, y=310)

        self.id_label_color = customtkinter.CTkLabel(
            self.frame_internal_color,
            font=self.font2,
            text='Cor Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_color.place(x=45,y=350)

        self.id_entry_color = customtkinter.CTkEntry(
            self.frame_internal_color,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_color.place(x=20, y=380)

        self.add_button_color = customtkinter.CTkButton(
            self.frame_internal_color,
            font=self.font2,
            command=self.Insert_Color,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_color.place(x=15,y=430)

        self.clear_button_color = customtkinter.CTkButton(
            self.frame_internal_color,
            font=self.font2,
            command=lambda:self.Clear_Entry_Color(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_color.place(x=108,y=430)

        self.update_button_color = customtkinter.CTkButton(
            self.frame_internal_color,
            font=self.font2,
            command=self.Update_Color,
            text_color='#fff',
            text='Update',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.update_button_color.place(x=15,y=490)

        self.delete_button_color = customtkinter.CTkButton(
            self.frame_internal_color,
            font=self.font2,
            command=self.Delete_Color,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.delete_button_color.place(x=108,y=490)


        self.frame_internal_color_01 = customtkinter.CTkFrame(
            self.tabview.tab("CORES"),
            corner_radius=10,
            )
        self.frame_internal_color_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=0,
            pady=50
            )
        self.frame_internal_color_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_color_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_color_01.grid_rowconfigure(0, weight=1)



        style = ttk.Style(self.frame_internal_color_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_color = ttk.Treeview(self.frame_internal_color_01, height=50,)
        self.table_color['columns'] = ('ID','MARCA', 'MODELO', 'PRODUTO', 'COR')
        self.table_color.column('#0', width=0, stretch=tkinter.NO)
        self.table_color.column('ID', width=0, stretch=tkinter.NO)
        self.table_color.column('MARCA', anchor=tkinter.CENTER, width=250)
        self.table_color.column('MODELO', anchor=tkinter.CENTER, width=350)
        self.table_color.column('PRODUTO', anchor=tkinter.CENTER, width=650)
        self.table_color.column('COR', anchor=tkinter.CENTER, width=250)

        self.table_color.heading('ID', text = 'ID')
        self.table_color.heading('MARCA', text = 'MARCA')
        self.table_color.heading('MODELO', text = 'MODELO')
        self.table_color.heading('PRODUTO', text = 'PRODUTO')
        self.table_color.heading('COR', text = 'COR')
        self.table_color.pack(fill = 'both', expand = False)

        self.table_color.bind('<ButtonRelease>', self.Display_Data_Color)

        self.Add_to_Treeview_Color()

        # ****************  PAGE_CORES  ************************


        # ****************  PAGE_FORNECEDOR  ************************

        self.frame_internal_supplier = customtkinter.CTkFrame(
            self.tabview.tab("FORNECEDOR"),
            corner_radius=10,
            )
        self.frame_internal_supplier.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=10,


            )
        self.frame_internal_supplier.grid_columnconfigure(1, weight=1)
        self.frame_internal_supplier.grid_rowconfigure(1, weight=0)
        self.frame_internal_supplier.grid_rowconfigure(0, weight=1)


        # ****************  PAGE_FORNECEDOR  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font1,
            text='Fornecedor',
            text_color='#fff',
            )
        self.title_label.place(x=25,y=0)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_supplier,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=695
            )
        self.frame.place(x=0,y=35)

        self.id_label_name_supplier = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Razão Social:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_name_supplier.place(x=40,y=55)

        self.id_entry_name_supplier = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_name_supplier.place(x=20,y=85)

        self.id_label_name_supplier_fantasy = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Nome Fantasia:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_name_supplier_fantasy.place(x=30,y=115)

        self.id_entry_name_supplier_fantasy = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_name_supplier_fantasy.place(x=20,y=145)

        self.id_label_supplier_cnpj = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='CNPJ:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_supplier_cnpj.place(x=70,y=175)

        self.id_entry_supplier_cnpj = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_supplier_cnpj.place(x=20,y=205)

        self.id_label_state_registration = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Insc. Estadual:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_state_registration.place(x=35,y=235)

        self.id_entry_state_registration = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_state_registration.place(x=20,y=265)

        self.id_label_county_registration = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Insc. Municipal:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_county_registration.place(x=30,y=295)

        self.id_entry_county_registration = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_county_registration.place(x=20,y=325)

        self.id_label_address = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Logradouro:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_address.place(x=45,y=355)

        self.id_entry_address = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_address.place(x=20,y=385)

        self.id_label_address_state = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Município/Estado:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_address_state.place(x=20,y=415)

        self.id_entry_address_state = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_address_state.place(x=20,y=445)


        self.id_label_supplier_email = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Email:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_supplier_email.place(x=70,y=475)

        self.id_entry_supplier_email = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_supplier_email.place(x=20, y=505)

        self.id_label_supplier_phone = customtkinter.CTkLabel(
            self.frame_internal_supplier,
            font=self.font2,
            text='Contato:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_supplier_phone.place(x=60,y=535)

        self.id_entry_supplier_phone = customtkinter.CTkEntry(
            self.frame_internal_supplier,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_supplier_phone.place(x=20, y=565)

        self.add_button_supplier = customtkinter.CTkButton(
            self.frame_internal_supplier,
            font=self.font2,
            command=self.Insert_Supplier,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_supplier.place(x=15,y=615)

        self.clear_button_supplier = customtkinter.CTkButton(
            self.frame_internal_supplier,
            font=self.font2,
            command=lambda:self.Clear_Entry_Supplier(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_supplier.place(x=108,y=615)

        self.update_button_supplier = customtkinter.CTkButton(
            self.frame_internal_supplier,
            font=self.font2,
            command=self.Update_Supplier,
            text_color='#fff',
            text='Update',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.update_button_supplier.place(x=15,y=675)

        self.delete_button_supplier = customtkinter.CTkButton(
            self.frame_internal_supplier,
            font=self.font2,
            command=self.Delete_Supplier,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.delete_button_supplier.place(x=108,y=675)


        self.frame_internal_supplier_01 = customtkinter.CTkFrame(
            self.tabview.tab("FORNECEDOR"),
            corner_radius=10,
            )
        self.frame_internal_supplier_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=0,
            pady=50
            )
        self.frame_internal_supplier_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_supplier_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_supplier_01.grid_rowconfigure(0, weight=1)



        style = ttk.Style(self.frame_internal_supplier_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_supplier = ttk.Treeview(self.frame_internal_supplier_01, height=50,)
        self.table_supplier['columns'] = ('ID','RAZÃO SOCIAL', 'NOME FANTASIA', 'CNPJ', 'LOGRADOURO')
        self.table_supplier.column('#0', width=0, stretch=tkinter.NO)
        self.table_supplier.column('ID', width=0, stretch=tkinter.NO)
        self.table_supplier.column('RAZÃO SOCIAL', anchor=tkinter.CENTER, width=350)
        self.table_supplier.column('NOME FANTASIA', anchor=tkinter.CENTER, width=350)
        self.table_supplier.column('CNPJ', anchor=tkinter.CENTER, width=350)
        self.table_supplier.column('LOGRADOURO', anchor=tkinter.CENTER, width=650)

        self.table_supplier.heading('ID', text = 'ID')
        self.table_supplier.heading('RAZÃO SOCIAL', text = 'RAZÃO SOCIAL')
        self.table_supplier.heading('NOME FANTASIA', text = 'NOME FANTASIA')
        self.table_supplier.heading('CNPJ', text = 'CNPJ')
        self.table_supplier.heading('LOGRADOURO', text = 'LOGRADOURO')
        self.table_supplier.pack(fill = 'both', expand = False)

        self.table_supplier.bind('<ButtonRelease>', self.Display_Data_Supplier)

        self.Add_to_Treeview_Supplier()
 
 
        # ****************  PAGE_FORNECEDOR  ************************

 
        # ****************  PAGE_PRESTADOR  ************************

        self.frame_internal_provider = customtkinter.CTkFrame(
            self.tabview.tab("PRESTADOR"),
            corner_radius=10,
            )
        self.frame_internal_provider.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_provider.grid_columnconfigure(1, weight=1)
        self.frame_internal_provider.grid_rowconfigure(1, weight=0)
        self.frame_internal_provider.grid_rowconfigure(0, weight=1)


        # ****************  PAGE_PRESTADOR  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_provider,
            font=self.font1,
            text='SERVIÇOS',
            text_color='#fff',
            )
        self.title_label.place(x=35,y=0)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_provider,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=365
            )
        self.frame.place(x=0,y=35)

        image1 = customtkinter.CTkImage(Image.open('logo_fevox1.ico'), size=(70, 70))
        image1_label = customtkinter.CTkLabel(
            master=self.frame_internal_provider,
            text='',
            image=image1
            )
        image1_label.place(x=65,y=55)


        self.id_label_supplier_name_provider = customtkinter.CTkLabel(
            self.frame_internal_provider,
            font=self.font2,
            text='Fornecedor:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_supplier_name_provider.place(x=45,y=140)

        supplier_option_invoice = []
        connect_db = Database_Supplier()
        supplier_names = connect_db.Fetch_Supplier()
        for supplier in supplier_names:
            supplier_option_invoice.append(supplier[2])
        brands_in_order = sorted(supplier_option_invoice)

        def Option_Brand_Callback_Supplier_Provider(choice):
            self.id_entry_name_provider.configure(state='normal')
            self.Add_to_Treeview_Provider_Name()

        self.optionmenu_supplier_name_provider = customtkinter.CTkOptionMenu(
            self.frame_internal_provider,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Supplier_Provider
            )
        self.optionmenu_supplier_name_provider.set('FORNECEDOR')
        self.optionmenu_supplier_name_provider.place(x=20,y=170)


        self.id_label_name_provider = customtkinter.CTkLabel(
            self.frame_internal_provider,
            font=self.font2,
            text='Serviço:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_name_provider.place(x=65,y=205)

        self.id_entry_name_provider = customtkinter.CTkEntry(
            self.frame_internal_provider,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_name_provider.place(x=20, y=235)


        self.add_button_name_provider = customtkinter.CTkButton(
            self.frame_internal_provider,
            font=self.font2,
            command=self.Insert_Provider,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_name_provider.place(x=15,y=285)

        self.clear_button_name_provider = customtkinter.CTkButton(
            self.frame_internal_provider,
            font=self.font2,
            command=lambda:self.Clear_Entry_Provider(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_name_provider.place(x=108,y=285)


        self.update_button_name_provider = customtkinter.CTkButton(
            self.frame_internal_provider,
            font=self.font2,
            command=self.Update_Provider,
            text_color='#fff',
            text='Update',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.update_button_name_provider.place(x=15,y=345)

        self.delete_button_name_provider = customtkinter.CTkButton(
            self.frame_internal_provider,
            font=self.font2,
            command=self.Delete_Provider,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.delete_button_name_provider.place(x=108,y=345)


        self.frame_internal_provider_01 = customtkinter.CTkFrame(
            self.tabview.tab("PRESTADOR"),
            corner_radius=10,
            )
        self.frame_internal_provider_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=0,
            pady=50
            )
        self.frame_internal_provider_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_provider_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_provider_01.grid_rowconfigure(0, weight=1)



        style = ttk.Style(self.frame_internal_provider_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_provider = ttk.Treeview(self.frame_internal_provider_01, height=50,)
        self.table_provider['columns'] = ('ID','FORNECEDOR', 'SERVIÇO')
        self.table_provider.column('#0', width=0, stretch=tkinter.NO)
        self.table_provider.column('ID', width=0, stretch=tkinter.NO)
        self.table_provider.column('FORNECEDOR', anchor=tkinter.CENTER, width=450)
        self.table_provider.column('SERVIÇO', anchor=tkinter.CENTER, width=1200)

        self.table_provider.heading('ID', text = 'ID')
        self.table_provider.heading('FORNECEDOR', text = 'FORNECEDOR')
        self.table_provider.heading('SERVIÇO', text = 'SERVIÇO')
        self.table_provider.pack(fill = 'both', expand = False)

        self.table_provider.bind('<ButtonRelease>', self.Display_Data_Provider)


        self.Add_to_Treeview_Provider()


        # ****************  PAGE_PRESTADOR  ************************


        # ****************  Window_ESTOQUE  ************************


    #  self.right_dashboard   ----> dashboard widget
    def Window_Product_Registration_Stock(self):
        self.clear_frame()

        self.tabview  = customtkinter.CTkTabview(master=self.right_dashboard)
        self.tabview.pack(fill='both', expand=1, padx=10, pady=10)

        self.tabview.add("ESTOQUE")
        self.tabview.add("PRECIFICAÇÃO")


        # ****************  PAGE_ESTOQUE  ************************

        self.frame_internal_stock = customtkinter.CTkFrame(
            self.tabview.tab("ESTOQUE"),
            corner_radius=10,
            )
        self.frame_internal_stock.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_stock.grid_columnconfigure(1, weight=1)
        self.frame_internal_stock.grid_rowconfigure(1, weight=0)
        self.frame_internal_stock.grid_rowconfigure(0, weight=1)

        # ****************  PAGE_ESTOQUE  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_stock,
            font=self.font1,
            text='Estoque',
            text_color='#fff',
            )
        self.title_label.place(x=50,y=0,)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_stock,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=450
            )
        self.frame.place(x=0,y=35)

        image1 = customtkinter.CTkImage(Image.open('logo_fevox1.ico'), size=(70, 70))
        image1_label = customtkinter.CTkLabel(
            master=self.frame_internal_stock,
            text='',
            image=image1
            )
        image1_label.place(x=65,y=55)

        self.id_label_stock = customtkinter.CTkLabel(
            self.frame_internal_stock,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_stock.place(x=45,y=140)

        brands_option_stock = []
        connect_db = Database_Brand()
        brands_stock = connect_db.Fetch_Brand()
        for brands in brands_stock:
            brands_option_stock.append(brands[2])
        brands_in_order = sorted(brands_option_stock)

        def Option_Brand_Callback_Brand_Stock(choice):
            Start_Option_Stock_Brand(choice=choice)
            self.Add_to_Treeview_Stock()


        self.optionmenu_brand_stock = customtkinter.CTkOptionMenu(
            self.frame_internal_stock,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Brand_Stock
            )
        self.optionmenu_brand_stock.set('Escolha MARCA')
        self.optionmenu_brand_stock.place(x=20, y=170)

        self.id_label_model_stock = customtkinter.CTkLabel(
            self.frame_internal_stock,
            font=self.font2,
            text='Nome Modelo:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model_stock.place(x=35,y=210)

        def Start_Option_Stock_Brand(choice):
            brands_names = self.Search_Product_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == choice:
                    bran=int(numbrand)

            models_0123 = []
            connect_db = Database_Model()
            models_products = connect_db.Fetch_Model()
            for brands in models_products:
                if brands[2] == bran:
                    models_0123.append(brands[3])
            models_in_order = sorted(models_0123)
            if not models_0123:
                self.optionmenu_model_stock = customtkinter.CTkOptionMenu(
                    self.frame_internal_stock,
                    dynamic_resizing=False,
                    values=['SEM MODELOS'],
                    width=160,
                    command=Option_Brand_Callback_Model_Stock
                    )
                self.optionmenu_model_stock.place(x=20, y=240)
            else:
                self.optionmenu_model_stock = customtkinter.CTkOptionMenu(
                    self.frame_internal_stock,
                    dynamic_resizing=False,
                    values=models_in_order,
                    width=160,
                    command=Option_Brand_Callback_Model_Stock
                    )
                self.optionmenu_model_stock.set('Escolha MODELO')
                self.optionmenu_model_stock.place(x=20, y=240)


        def Option_Brand_Callback_Model_Stock(choice):
            Start_Option_Stock_Model(choice=choice)
            self.Add_to_Treeview_Stock_Model()


        self.optionmenu_model_stock = customtkinter.CTkOptionMenu(
            self.frame_internal_stock,
            dynamic_resizing=False,
            values=['Escolha MODELO'],
            width=160,
            command=Option_Brand_Callback_Model_Stock
            )
        self.optionmenu_model_stock.place(x=20, y=240)

        self.id_label_product_stock = customtkinter.CTkLabel(
            self.frame_internal_stock,
            font=self.font2,
            text='Nome Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_stock.place(x=35,y=280)


        def Start_Option_Stock_Model(choice):
            brand_choice = self.optionmenu_brand_stock.get()

            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)

            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass


            product_0123 = []
            connect_db = Database_Product()
            models_stock = connect_db.Fetch_Product()
            for models in models_stock:
                if models[2] == bran:
                    if models[3] == modelnum:
                        product_0123.append(models[4])

            product_in_order = set(product_0123)
            product_in_order01 = sorted(product_in_order)
            if not product_0123:
                self.optionmenu_product_stock = customtkinter.CTkOptionMenu(
                    self.frame_internal_stock,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Brand_Callback_Product_Stock
                    )
                self.optionmenu_product_stock.place(x=20, y=310) 
            else:
                print(product_0123)
                self.optionmenu_product_stock = customtkinter.CTkOptionMenu(
                    self.frame_internal_stock,
                    dynamic_resizing=False,
                    values=product_in_order01,
                    width=160,
                    command=Option_Brand_Callback_Product_Stock
                    )
                self.optionmenu_product_stock.set('Escolha PRODUTO')
                self.optionmenu_product_stock.place(x=20, y=310) 


        def Option_Brand_Callback_Product_Stock(choice):
            Start_Option_Stock_Color_Product(choice=choice)
            self.Add_to_Treeview_Stock_Product()


        self.optionmenu_product_stock = customtkinter.CTkOptionMenu(
            self.frame_internal_stock,
            dynamic_resizing=False,
            values=['Escolha PRODUTO'],
            width=160,
            command=Option_Brand_Callback_Product_Stock
            )
        self.optionmenu_product_stock.place(x=20, y=310)

        self.id_label_product_color_stock = customtkinter.CTkLabel(
            self.frame_internal_stock,
            font=self.font2,
            text='Cor Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_color_stock.place(x=45,y=350)


        def Start_Option_Stock_Color_Product(choice):

            brand_choice = self.optionmenu_brand_stock.get()

            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            model_choice = self.optionmenu_model_stock.get()

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)

            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == model_choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass

            product_names = self.Search_Color_Product_Two()
            name_products = []
            for x in product_names:
                y = str(x)
                k = y.split(': ')
                name_products.append(k)

            for numproduct, nummodelproduct, nameproduct in name_products:
                if nameproduct == choice:
                    if int(nummodelproduct) == modelnum:
                        id_product=int(numproduct)

            product_0123 = []
            connect_db = Database_Color()
            product_stock_color = connect_db.Fetch_Color()
            for color in product_stock_color:
                if color[3] == modelnum:
                    if color[4] == id_product:
                        product_0123.append(color[5])
                    product_color_in_order = set(product_0123)
                    product_color_in_order01 = sorted(product_color_in_order)
            if not product_0123:
                print('vazio')
                self.optionmenu_product_color_stock = customtkinter.CTkOptionMenu(
                    self.frame_internal_stock,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Brand_Callback_Color_Stock
                    )
                self.optionmenu_product_color_stock.place(x=20, y=380) 
            else:
                print(product_0123)
                self.optionmenu_product_color_stock = customtkinter.CTkOptionMenu(
                    self.frame_internal_stock,
                    dynamic_resizing=False,
                    values=product_color_in_order01,
                    width=160,
                    command=Option_Brand_Callback_Color_Stock
                    )
                self.optionmenu_product_color_stock.set('Escolha COR')
                self.optionmenu_product_color_stock.place(x=20, y=380) 

        def Option_Brand_Callback_Color_Stock(choice):
            self.Add_to_Treeview_Stock_Color()


        self.optionmenu_product_color_stock = customtkinter.CTkOptionMenu(
            self.frame_internal_stock,
            dynamic_resizing=False,
            values=['Escolha COR'],
            width=160,
            command=Option_Brand_Callback_Color_Stock
            )
        self.optionmenu_product_color_stock.place(x=20, y=380)


        self.clear_button_product_stock_amount = customtkinter.CTkButton(
            self.frame_internal_stock,
            font=self.font2,
            command=lambda:self.Clear_Entry_Stock(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=120
            )
        self.clear_button_product_stock_amount.place(x=40,y=430)

        self.frame_internal_stock_01 = customtkinter.CTkFrame(
            self.tabview.tab("ESTOQUE"),
            corner_radius=10,
            )
        self.frame_internal_stock_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=0,
            pady=50
            )
        self.frame_internal_stock_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_stock_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_stock_01.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self.frame_internal_stock_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_stock = ttk.Treeview(self.frame_internal_stock_01, height=50,)
        self.table_stock['columns'] = ('ID','MARCA', 'MODELO', 'PRODUTO', 'COR', 'QUANTIDADE')
        self.table_stock.column('#0', width=0, stretch=tkinter.NO)
        self.table_stock.column('ID', width=0, stretch=tkinter.NO)
        self.table_stock.column('MARCA', anchor=tkinter.CENTER, width=250)
        self.table_stock.column('MODELO', anchor=tkinter.CENTER, width=350)
        self.table_stock.column('PRODUTO', anchor=tkinter.CENTER, width=650)
        self.table_stock.column('COR', anchor=tkinter.CENTER, width=250)
        self.table_stock.column('QUANTIDADE', anchor=tkinter.CENTER, width=180)

        self.table_stock.heading('ID', text = 'ID')
        self.table_stock.heading('MARCA', text = 'MARCA')
        self.table_stock.heading('MODELO', text = 'MODELO')
        self.table_stock.heading('PRODUTO', text = 'PRODUTO')
        self.table_stock.heading('COR', text = 'COR')
        self.table_stock.heading('QUANTIDADE', text = 'QUANTIDADE')
        self.table_stock.pack(fill = 'both', expand = False)

        self.table_stock.bind('<ButtonRelease>', self.Display_Data_Stock)

        self.Add_to_Treeview_Stock()

        # ****************  PAGE_ESTOQUE  ************************
 
 
        # ****************  PAGE_PRECIFICAÇÃO  ************************

        self.frame_internal_pricing = customtkinter.CTkFrame(
            self.tabview.tab("PRECIFICAÇÃO"),
            corner_radius=10,
            )
        self.frame_internal_pricing.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_pricing.grid_columnconfigure(1, weight=1)
        self.frame_internal_pricing.grid_rowconfigure(1, weight=0)
        self.frame_internal_pricing.grid_rowconfigure(0, weight=1)


        # ****************  PAGE_PRECIFICAÇÃO  ************************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font1,
            text='Precificação',
            text_color='#fff',
            )
        self.title_label.place(x=25,y=0)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_pricing,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=655
            )
        self.frame.place(x=0,y=35)

        self.id_label_brand_pricing = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_brand_pricing.place(x=45,y=55)

        brands_option_invoice = []
        connect_db = Database_Brand()
        brands_stock = connect_db.Fetch_Brand()
        for brands in brands_stock:
            brands_option_invoice.append(brands[2])
        brands_in_order = sorted(brands_option_invoice)

        def Option_Brand_Callback_Brand_Pricing(choice):
            Start_Option_Pricing_Brand(choice=choice)
            self.Add_to_Treeview_Pricing_Invoice_Brand()
            self.Add_to_Treeview_Stock_Pricing_Brand()


        self.optionmenu_brand_pricing = customtkinter.CTkOptionMenu(
            self.frame_internal_pricing,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Brand_Pricing
            )
        self.optionmenu_brand_pricing.set('Escolha MARCA')
        self.optionmenu_brand_pricing.place(x=20,y=85)

        self.id_label_model_pricing = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Nome Modelo:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model_pricing.place(x=40,y=120)

        def Start_Option_Pricing_Brand(choice):
            brands_names = self.Search_Product_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == choice:
                    bran=int(numbrand)

            models_0123 = []
            connect_db = Database_Model()
            models_products = connect_db.Fetch_Model()
            for brands in models_products:
                if brands[2] == bran:
                    models_0123.append(brands[3])
            models_in_order = sorted(models_0123)
            if not models_0123:
                self.optionmenu_model_pricing = customtkinter.CTkOptionMenu(
                    self.frame_internal_pricing,
                    dynamic_resizing=False,
                    values=['SEM MODELOS'],
                    width=160,
                    command=Option_Brand_Callback_Model_Pricing
                    )
                self.optionmenu_model_pricing.place(x=20, y=150)
            else:
                self.optionmenu_model_pricing = customtkinter.CTkOptionMenu(
                    self.frame_internal_pricing,
                    dynamic_resizing=False,
                    values=models_in_order,
                    width=160,
                    command=Option_Brand_Callback_Model_Pricing
                    )
                self.optionmenu_model_pricing.set('Escolha MODELO')
                self.optionmenu_model_pricing.place(x=20, y=150)


        def Option_Brand_Callback_Model_Pricing(choice):
            Start_Option_Pricing_Model(choice=choice)
            self.Add_to_Treeview_Stock_Pricing_Model()
            self.Add_to_Treeview_Pricing_Invoice_Model()


        self.optionmenu_model_pricing = customtkinter.CTkOptionMenu(
            self.frame_internal_pricing,
            dynamic_resizing=False,
            values=['Escolha MODELO'],
            width=160,
            command=Option_Brand_Callback_Model_Pricing
            )
        self.optionmenu_model_pricing.place(x=20, y=150)

        self.id_label_product_pricing = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Nome Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_pricing.place(x=35,y=185)


        def Start_Option_Pricing_Model(choice):
            brand_choice = self.optionmenu_brand_pricing.get()

            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)

            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass

            product_0123 = []
            connect_db = Database_Product()
            models_stock = connect_db.Fetch_Product()
            for models in models_stock:
                if models[2] == bran:
                    if models[3] == modelnum:
                        product_0123.append(models[4])

            product_in_order = set(product_0123)
            product_in_order01 = sorted(product_in_order)
            if not product_0123:
                self.optionmenu_product_pricing = customtkinter.CTkOptionMenu(
                    self.frame_internal_pricing,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Brand_Callback_Product_Pricing
                    )
                self.optionmenu_product_pricing.place(x=20, y=215) 
            else:
                print(product_0123)
                self.optionmenu_product_pricing = customtkinter.CTkOptionMenu(
                    self.frame_internal_pricing,
                    dynamic_resizing=False,
                    values=product_in_order01,
                    width=160,
                    command=Option_Brand_Callback_Product_Pricing
                    )
                self.optionmenu_product_pricing.set('Escolha PRODUTO')
                self.optionmenu_product_pricing.place(x=20, y=215) 


        def Option_Brand_Callback_Product_Pricing(choice):
            Start_Option_Pricing_Color_Product(choice=choice)
            self.Add_to_Treeview_Stock_Pricing_Product()
            self.Add_to_Treeview_Pricing_Invoice_Product()


        self.optionmenu_product_pricing = customtkinter.CTkOptionMenu(
            self.frame_internal_pricing,
            dynamic_resizing=False,
            values=['Escolha PRODUTO'],
            width=160,
            command=Option_Brand_Callback_Product_Pricing
            )
        self.optionmenu_product_pricing.place(x=20, y=215)

        self.id_label_product_color_pricing = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Cor Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_color_pricing.place(x=45,y=250)


        def Start_Option_Pricing_Color_Product(choice):

            brand_choice = self.optionmenu_brand_pricing.get()

            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            model_choice = self.optionmenu_model_pricing.get()

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)

            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == model_choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass

            product_names = self.Search_Color_Product_Two()
            name_products = []
            for x in product_names:
                y = str(x)
                k = y.split(': ')
                name_products.append(k)

            for numproduct, nummodelproduct, nameproduct in name_products:
                if nameproduct == choice:
                    if int(nummodelproduct) == modelnum:
                        id_product=int(numproduct)

            product_0123 = []
            connect_db = Database_Color()
            product_stock_color = connect_db.Fetch_Color()
            for color in product_stock_color:
                if color[3] == modelnum:
                    if color[4] == id_product:
                        product_0123.append(color[5])
                    product_color_in_order = set(product_0123)
                    product_color_in_order01 = sorted(product_color_in_order)
            if not product_0123:
                print('vazio')
                self.optionmenu_product_color_pricing = customtkinter.CTkOptionMenu(
                    self.frame_internal_pricing,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Brand_Callback_Color_Pricing
                    )
                self.optionmenu_product_color_pricing.place(x=20, y=280) 
            else:
                print(product_0123)
                self.optionmenu_product_color_pricing = customtkinter.CTkOptionMenu(
                    self.frame_internal_pricing,
                    dynamic_resizing=False,
                    values=product_color_in_order01,
                    width=160,
                    command=Option_Brand_Callback_Color_Pricing
                    )
                self.optionmenu_product_color_pricing.set('Escolha COR')
                self.optionmenu_product_color_pricing.place(x=20, y=280) 

        def Option_Brand_Callback_Color_Pricing(choice):
            self.Add_to_Treeview_Stock_Pricing_Color()


        self.optionmenu_product_color_pricing = customtkinter.CTkOptionMenu(
            self.frame_internal_pricing,
            dynamic_resizing=False,
            values=['Escolha COR'],
            width=160,
            command=Option_Brand_Callback_Color_Pricing
            )
        self.optionmenu_product_color_pricing.place(x=20, y=280)

        self.id_label_product_pricing_unitary_value = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Valor Unitário:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_pricing_unitary_value.place(x=35,y=315)

        self.id_entry_product_pricing_unitary_value = customtkinter.CTkEntry(
            self.frame_internal_pricing,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_product_pricing_unitary_value.place(x=20, y=340)

        self.id_label_pricing_tax = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Impostos %:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_pricing_tax.place(x=45,y=375)

        self.id_entry_pricing_tax = customtkinter.CTkEntry(
            self.frame_internal_pricing,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_pricing_tax.place(x=20, y=400)

        self.id_label_pricing_value_sale = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Valor Venda:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_pricing_value_sale.place(x=45,y=440)

        self.id_entry_pricing_value_sale = customtkinter.CTkEntry(
            self.frame_internal_pricing,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_pricing_value_sale.place(x=20, y=465)

        self.id_label_pricing_value_profit = customtkinter.CTkLabel(
            self.frame_internal_pricing,
            font=self.font2,
            text='Lucro Líquido:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_pricing_value_profit.place(x=35,y=505)

        self.id_entry_pricing_value_profit = customtkinter.CTkEntry(
            self.frame_internal_pricing,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_pricing_value_profit.place(x=20, y=530)

        self.id_product_pricing = customtkinter.CTkEntry(
            self.frame_internal_pricing,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        # self.id_product_pricing_.place(x=20, y=530)

        self.update_button_pricing = customtkinter.CTkButton(
            self.frame_internal_pricing,
            font=self.font2,
            command=self.Calculate_Profit,
            text_color='#fff',
            text='Calcular',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=160
            )
        self.update_button_pricing.place(x=20,y=580)


        self.add_button_pricing = customtkinter.CTkButton(
            self.frame_internal_pricing,
            font=self.font2,
            command=self.Insert_Pricing,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80,
            state='disabled'
            )
        self.add_button_pricing.place(x=15,y=640)

        self.clear_button_pricing = customtkinter.CTkButton(
            self.frame_internal_pricing,
            font=self.font2,
            command=lambda:self.Clear_Entry_Pricing(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_pricing.place(x=108,y=640)


        self.frame_internal_pricing_01 = customtkinter.CTkFrame(
            self.tabview.tab("PRECIFICAÇÃO"),
            corner_radius=10,
            )
        self.frame_internal_pricing_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=0,
            pady=50
            )
        self.frame_internal_pricing_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_pricing_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_pricing_01.grid_rowconfigure(0, weight=1)


        style = ttk.Style(self.frame_internal_pricing_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_pricing_num = ttk.Treeview(self.frame_internal_pricing_01, height=22,)
        self.table_pricing_num['columns'] = ('ID', 'FORNECEDOR', 'N° NOTA', 'MARCA', 'MODELO', 'PRODUTO', 'COR', 'VALOR')
        self.table_pricing_num.column('#0', width=0, stretch=tkinter.NO)
        self.table_pricing_num.column('ID', width=0, stretch=tkinter.NO)
        self.table_pricing_num.column('FORNECEDOR', anchor=tkinter.CENTER, width=250)
        self.table_pricing_num.column('N° NOTA', anchor=tkinter.CENTER, width=200)
        self.table_pricing_num.column('MARCA', anchor=tkinter.CENTER, width=250)
        self.table_pricing_num.column('MODELO', anchor=tkinter.CENTER, width=250)
        self.table_pricing_num.column('PRODUTO', anchor=tkinter.CENTER, width=300)
        self.table_pricing_num.column('COR', anchor=tkinter.CENTER, width=180)
        self.table_pricing_num.column('VALOR', anchor=tkinter.CENTER, width=130)

        self.table_pricing_num.heading('ID', text = 'ID')
        self.table_pricing_num.heading('FORNECEDOR', text = 'FORNECEDOR')
        self.table_pricing_num.heading('N° NOTA', text = 'N° NOTA')
        self.table_pricing_num.heading('MARCA', text = 'MARCA')
        self.table_pricing_num.heading('MODELO', text = 'MODELO')
        self.table_pricing_num.heading('PRODUTO', text = 'PRODUTO')
        self.table_pricing_num.heading('COR', text = 'COR')
        self.table_pricing_num.heading('VALOR', text = 'VALOR')
        self.table_pricing_num.pack(fill = 'both', expand = False)

        self.table_pricing_num.bind('<ButtonRelease>', self.Display_Data_Pricing)

        self.Add_to_Treeview_Pricing_Invoice_Brand()

        self.title_label_table = customtkinter.CTkLabel(
            self.frame_internal_pricing_01,
            font=self.font1,
            text='',
            text_color='#fff',
            )
        self.title_label_table.pack()

        style = ttk.Style(self.frame_internal_pricing_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_pricing_stock = ttk.Treeview(self.frame_internal_pricing_01, height=25,)
        self.table_pricing_stock['columns'] = ('ID','MARCA', 'MODELO', 'PRODUTO', 'COR', 'VENDA', 'IMPOSTO %', 'LUCRO')
        self.table_pricing_stock.column('#0', width=0, stretch=tkinter.NO)
        self.table_pricing_stock.column('ID', width=0, stretch=tkinter.NO)
        self.table_pricing_stock.column('MARCA', anchor=tkinter.CENTER, width=230)
        self.table_pricing_stock.column('MODELO', anchor=tkinter.CENTER, width=330)
        self.table_pricing_stock.column('PRODUTO', anchor=tkinter.CENTER, width=330)
        self.table_pricing_stock.column('COR', anchor=tkinter.CENTER, width=250)
        self.table_pricing_stock.column('VENDA', anchor=tkinter.CENTER, width=180)
        self.table_pricing_stock.column('IMPOSTO %', anchor=tkinter.CENTER, width=150)
        self.table_pricing_stock.column('LUCRO', anchor=tkinter.CENTER, width=150)

        self.table_pricing_stock.heading('ID', text = 'ID')
        self.table_pricing_stock.heading('MARCA', text = 'MARCA')
        self.table_pricing_stock.heading('MODELO', text = 'MODELO')
        self.table_pricing_stock.heading('PRODUTO', text = 'PRODUTO')
        self.table_pricing_stock.heading('COR', text = 'COR')
        self.table_pricing_stock.heading('VENDA', text = 'VENDA')
        self.table_pricing_stock.heading('IMPOSTO %', text = 'IMPOSTO %')
        self.table_pricing_stock.heading('LUCRO', text = 'LUCRO')
        self.table_pricing_stock.pack(fill = 'both', expand = False)

        self.table_pricing_stock.bind('<ButtonRelease>', self.Display_Data_Pricing_Num_Id)

        self.Add_to_Treeview_Stock_Pricing_Brand()


        # ****************  PAGE_PRECIFICAÇÃO  ************************


        # ****************  Window_ESTOQUE  ************************


        # ****************  Window_Notas  ************************


    #  self.right_dashboard   ----> dashboard widget
    def Window_Entry_Invoice(self):
        self.clear_frame()

        self.tabview  = customtkinter.CTkTabview(master=self.right_dashboard)
        self.tabview.pack(fill='both', expand=1, padx=10, pady=10)

        self.tabview.add("PRESTADOR")
        self.tabview.add("PRODUTO")
        self.tabview.add("CONSULTA 1")

        # ************* PAGE_ENTRADA_NOTA_PRESTADOR  *****************

        self.frame_internal_costs_entry = customtkinter.CTkFrame(
            self.tabview.tab("PRESTADOR"),
            corner_radius=10,
            )
        self.frame_internal_costs_entry.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_costs_entry.grid_columnconfigure(1, weight=1)
        self.frame_internal_costs_entry.grid_rowconfigure(1, weight=0)
        self.frame_internal_costs_entry.grid_rowconfigure(0, weight=1)

        # ************* PAGE_ENTRADA_NOTA_PRESTADOR  *****************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_costs_entry,
            font=self.font1,
            text='Entrada Custos',
            text_color='#fff',
            )
        self.title_label.place(x=5,y=0)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_costs_entry,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=555
            )
        self.frame.place(x=0,y=35)

        self.id_label_supplier_name_costs = customtkinter.CTkLabel(
            self.frame_internal_costs_entry,
            font=self.font2,
            text='Fornecedor:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_supplier_name_costs.place(x=50,y=50)

        supplier_option_invoice = []
        connect_db = Database_Supplier()
        supplier_names = connect_db.Fetch_Supplier()
        for supplier in supplier_names:
            supplier_option_invoice.append(supplier[2])
        brands_in_order = sorted(supplier_option_invoice)

        def Option_Supplier_Callback_Name(choice):
            # print("optionmenu dropdown clicked:", choice)
            Start_Option_Name_Costs(choice=choice)
            self.Add_to_Treeview_Costs()

        self.optionmenu_supplier_name_costs = customtkinter.CTkOptionMenu(
            self.frame_internal_costs_entry,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Supplier_Callback_Name
            )
        self.optionmenu_supplier_name_costs.set('FORNECEDOR')
        self.optionmenu_supplier_name_costs.place(x=20,y=80)

        self.id_label_type_services = customtkinter.CTkLabel(
                self.frame_internal_costs_entry,
                font=self.font2,
                text='Serviço:',
                text_color='#fff',
                bg_color='#1B1B21'
                )
        self.id_label_type_services.place(x=65,y=110)

        def Start_Option_Name_Costs(choice):
            option_name_costs = []
            connect_db = Database_Provider()
            suppliers = connect_db.Fetch_Provider()
            for supplier in suppliers:
                if supplier[1] == choice:
                    option_name_costs.append(supplier[2])
            option_name_costs01 = sorted(option_name_costs)
            print(option_name_costs01)

            if not option_name_costs01:
                self.optionmenu_type_services = customtkinter.CTkOptionMenu(
                    self.frame_internal_costs_entry,
                    dynamic_resizing=False,
                    values=['SEM SERVIÇOS'],
                    width=160,
                    )
                self.optionmenu_type_services.set('Escolha Fornecedor')
                self.optionmenu_type_services.place(x=20,y=140)
            else:
                # print(models_0123)
                self.optionmenu_type_services = customtkinter.CTkOptionMenu(
                    self.frame_internal_costs_entry,
                    dynamic_resizing=False,
                    values=option_name_costs01,
                    width=160,
                    )
                self.optionmenu_type_services.set('Escolha Fornecedor')
                self.optionmenu_type_services.place(x=20,y=140)



        self.optionmenu_type_services = customtkinter.CTkOptionMenu(
            self.frame_internal_costs_entry,
            dynamic_resizing=False,
            values=['Escolha Fornecedor'],
            width=160,
            )
        self.optionmenu_type_services.set('Escolha Fornecedor')
        self.optionmenu_type_services.place(x=20,y=140)

        self.id_label_types_of_costs = customtkinter.CTkLabel(
                self.frame_internal_costs_entry,
                font=self.font2,
                text='Custos:',
                text_color='#fff',
                bg_color='#1B1B21'
                )
        self.id_label_types_of_costs.place(x=65,y=170)

        types_of_costs = [
            'Custos Fixos',
            'Custos Variáveis']
        
        self.optionmenu_types_of_costs = customtkinter.CTkOptionMenu(
            self.frame_internal_costs_entry,
            dynamic_resizing=False,
            values=types_of_costs,
            width=160,
            )
        self.optionmenu_types_of_costs.set('Custos')
        self.optionmenu_types_of_costs.place(x=20,y=200)

        self.id_label_days_the_month = customtkinter.CTkLabel(
            self.frame_internal_costs_entry,
            font=self.font2,
            text='Dia Vencimento:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_days_the_month.place(x=30,y=230)

        days_the_month = ['1','2','3','4','5','6','7','8','9','10',
                          '11','12','13','14','15','16','17','18','19','20',
                          '21','22','23','24','25','26','27','28','29','30',
                          '31']
        
        self.optionmenu_days_the_month = customtkinter.CTkOptionMenu(
            self.frame_internal_costs_entry,
            dynamic_resizing=False,
            values=days_the_month,
            width=160,
            )
        self.optionmenu_days_the_month.set('VENCIMENTO')
        self.optionmenu_days_the_month.place(x=20,y=260)



        self.id_label_value_costs = customtkinter.CTkLabel(
            self.frame_internal_costs_entry,
            font=self.font2,
            text='Valor:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_value_costs.place(x=70,y=290)

        self.id_entry_value_costs = customtkinter.CTkEntry(
            self.frame_internal_costs_entry,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_value_costs.place(x=20, y=315)

        self.id_label_number_of_installments = customtkinter.CTkLabel(
            self.frame_internal_costs_entry,
            font=self.font2,
            text='Número Parcelas:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_number_of_installments.place(x=20,y=345)

        self.id_entry_number_of_installments = customtkinter.CTkEntry(
            self.frame_internal_costs_entry,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_number_of_installments.place(x=20, y=370)

        self.id_label_invoice_number_costs = customtkinter.CTkLabel(
            self.frame_internal_costs_entry,
            font=self.font2,
            text='Número Nota:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_invoice_number_costs.place(x=40,y=400)

        self.id_entry_invoice_number_costs = customtkinter.CTkEntry(
            self.frame_internal_costs_entry,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_invoice_number_costs.place(x=20, y=425)


        self.add_button_registration_costs = customtkinter.CTkButton(
            self.frame_internal_costs_entry,
            font=self.font2,
            command=self.Insert_Costs_Entry,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_registration_costs.place(x=15,y=475)

        self.clear_button_registration_costs = customtkinter.CTkButton(
            self.frame_internal_costs_entry,
            font=self.font2,
            command=lambda:self.Clear_Entry_Costs(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_registration_costs.place(x=108,y=475)

        self.update_button_registration_costs = customtkinter.CTkButton(
            self.frame_internal_costs_entry,
            font=self.font2,
            command=self.Update_Costs,
            text_color='#fff',
            text='Update',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.update_button_registration_costs.place(x=15,y=535)

        self.delete_button_registration_costs = customtkinter.CTkButton(
            self.frame_internal_costs_entry,
            font=self.font2,
            command=self.Delete_Costs,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.delete_button_registration_costs.place(x=108,y=535)


        self.frame_internal_costs_entry_01 = customtkinter.CTkFrame(
            self.tabview.tab("PRESTADOR"),
            corner_radius=10,
            )
        self.frame_internal_costs_entry_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=0,
            pady=50
            )
        self.frame_internal_costs_entry_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_costs_entry_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_costs_entry_01.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self.frame_internal_costs_entry_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_costs = ttk.Treeview(self.frame_internal_costs_entry_01, height=30,)
        self.table_costs['columns'] = ('ID','DATA', 'FORNECEDOR', 'SERVIÇO', 'CUSTOS', 'VENCIMENTO', 'VALOR', 'N° PARCELAS', 'N° NOTA')
        self.table_costs.column('#0', width=0, stretch=tkinter.NO)
        self.table_costs.column('ID', width=0, stretch=tkinter.NO)
        self.table_costs.column('DATA', anchor=tkinter.CENTER, width=150)
        self.table_costs.column('FORNECEDOR', anchor=tkinter.CENTER, width=350)
        self.table_costs.column('SERVIÇO', anchor=tkinter.CENTER, width=450)
        self.table_costs.column('CUSTOS', anchor=tkinter.CENTER, width=200)
        self.table_costs.column('VENCIMENTO', anchor=tkinter.CENTER, width=100)
        self.table_costs.column('VALOR', anchor=tkinter.CENTER, width=150)
        self.table_costs.column('N° PARCELAS', anchor=tkinter.CENTER, width=150)
        self.table_costs.column('N° NOTA', anchor=tkinter.CENTER, width=130)

        self.table_costs.heading('ID', text = 'ID')
        self.table_costs.heading('DATA', text = 'DATA')
        self.table_costs.heading('FORNECEDOR', text = 'FORNECEDOR')
        self.table_costs.heading('SERVIÇO', text = 'SERVIÇO')
        self.table_costs.heading('CUSTOS', text = 'CUSTOS')
        self.table_costs.heading('VENCIMENTO', text = 'VENCIMENTO')
        self.table_costs.heading('VALOR', text = 'VALOR')
        self.table_costs.heading('N° PARCELAS', text = 'N° PARCELAS')
        self.table_costs.heading('N° NOTA', text = 'N° NOTA')
        self.table_costs.pack(fill = 'both', expand = False)

        self.table_costs.bind('<ButtonRelease>', self.Display_Data_Costs)

        self.Add_to_Treeview_Costs()

        # ************* PAGE_ENTRADA_NOTA_PRESTADOR  *****************

        # *************  PAGE_ENTRADA_NOTA_PRODUTOS  ********************

        self.frame_internal_invoice = customtkinter.CTkFrame(
            self.tabview.tab("PRODUTO"),
            corner_radius=10,
            )
        self.frame_internal_invoice.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=50,
            pady=50,


            )
        self.frame_internal_invoice.grid_columnconfigure(1, weight=1)
        self.frame_internal_invoice.grid_rowconfigure(1, weight=0)
        self.frame_internal_invoice.grid_rowconfigure(0, weight=1)


        # *************  PAGE_ENTRADA_NOTA_PRODUTOS  ********************

        self.title_label = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font1,
            text='Entrada Nota',
            text_color='#fff',
            )
        self.title_label.place(x=20,y=0,)

        self.frame = customtkinter.CTkFrame(
            self.frame_internal_invoice,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=200,
            height=635
            )
        self.frame.place(x=0,y=35)

        self.id_label_supplier_name = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Fornecedor:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_supplier_name.place(x=45,y=55)

        supplier_option_invoice = []
        connect_db = Database_Supplier()
        supplier_names = connect_db.Fetch_Supplier()
        for supplier in supplier_names:
            supplier_option_invoice.append(supplier[2])
        brands_in_order = sorted(supplier_option_invoice)

        def Option_Brand_Callback_Supplier(choice):
            self.Add_to_Treeview_Invoice_Num()

        self.optionmenu_supplier_name = customtkinter.CTkOptionMenu(
            self.frame_internal_invoice,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Supplier
            )
        self.optionmenu_supplier_name.set('FORNECEDOR')
        self.optionmenu_supplier_name.place(x=20,y=85)


        self.id_label_num_invoice = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Número Nota:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_num_invoice.place(x=40,y=120)

        self.id_entry_id_num_invoice = customtkinter.CTkEntry(
            self.frame_internal_invoice,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_id_num_invoice.place(x=20, y=150)

        self.id_label_invoice = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_invoice.place(x=45,y=185)

        brands_option_invoice = []
        connect_db = Database_Brand()
        brands_stock = connect_db.Fetch_Brand()
        for brands in brands_stock:
            brands_option_invoice.append(brands[2])
        brands_in_order = sorted(brands_option_invoice)

        def Option_Brand_Callback_Brand_Invoice(choice):
            Start_Option_Invoice_Brand(choice=choice)
            self.Add_to_Treeview_Invoice()


        self.optionmenu_brand_invoice = customtkinter.CTkOptionMenu(
            self.frame_internal_invoice,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Brand_Invoice
            )
        self.optionmenu_brand_invoice.set('Escolha MARCA')
        self.optionmenu_brand_invoice.place(x=20, y=215)

        self.id_label_model_invoice = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Nome Modelo:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model_invoice.place(x=35,y=255)

        def Start_Option_Invoice_Brand(choice):
            brands_names = self.Search_Product_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == choice:
                    bran=int(numbrand)

            models_0123 = []
            connect_db = Database_Model()
            models_products = connect_db.Fetch_Model()
            for brands in models_products:
                if brands[2] == bran:
                    models_0123.append(brands[3])
            models_in_order = sorted(models_0123)
            if not models_0123:
                self.optionmenu_model_invoice = customtkinter.CTkOptionMenu(
                    self.frame_internal_invoice,
                    dynamic_resizing=False,
                    values=['SEM MODELOS'],
                    width=160,
                    command=Option_Brand_Callback_Model_Invoice
                    )
                self.optionmenu_model_invoice.place(x=20, y=285)
            else:
                self.optionmenu_model_invoice = customtkinter.CTkOptionMenu(
                    self.frame_internal_invoice,
                    dynamic_resizing=False,
                    values=models_in_order,
                    width=160,
                    command=Option_Brand_Callback_Model_Invoice
                    )
                self.optionmenu_model_invoice.set('Escolha MODELO')
                self.optionmenu_model_invoice.place(x=20, y=285)


        def Option_Brand_Callback_Model_Invoice(choice):
            Start_Option_Invoice_Model(choice=choice)
            self.Add_to_Treeview_Invoice_Model()


        self.optionmenu_model_invoice = customtkinter.CTkOptionMenu(
            self.frame_internal_invoice,
            dynamic_resizing=False,
            values=['Escolha MODELO'],
            width=160,
            command=Option_Brand_Callback_Model_Invoice
            )
        self.optionmenu_model_invoice.place(x=20, y=285)

        self.id_label_product_invoice = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Nome Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_invoice.place(x=35,y=325)


        def Start_Option_Invoice_Model(choice):
            brand_choice = self.optionmenu_brand_invoice.get()

            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)

            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass


            product_0123 = []
            connect_db = Database_Product()
            models_stock = connect_db.Fetch_Product()
            for models in models_stock:
                if models[2] == bran:
                    if models[3] == modelnum:
                        product_0123.append(models[4])

            product_in_order = set(product_0123)
            product_in_order01 = sorted(product_in_order)
            if not product_0123:
                self.optionmenu_product_invoice = customtkinter.CTkOptionMenu(
                    self.frame_internal_invoice,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Brand_Callback_Product_Invoice
                    )
                self.optionmenu_product_invoice.place(x=20, y=355) 
            else:
                print(product_0123)
                self.optionmenu_product_invoice = customtkinter.CTkOptionMenu(
                    self.frame_internal_invoice,
                    dynamic_resizing=False,
                    values=product_in_order01,
                    width=160,
                    command=Option_Brand_Callback_Product_Invoice
                    )
                self.optionmenu_product_invoice.set('Escolha PRODUTO')
                self.optionmenu_product_invoice.place(x=20, y=355) 


        def Option_Brand_Callback_Product_Invoice(choice):
            Start_Option_Invoice_Color_Product(choice=choice)
            self.Add_to_Treeview_Invoice_Product()


        self.optionmenu_product_invoice = customtkinter.CTkOptionMenu(
            self.frame_internal_invoice,
            dynamic_resizing=False,
            values=['Escolha PRODUTO'],
            width=160,
            command=Option_Brand_Callback_Product_Invoice
            )
        self.optionmenu_product_invoice.place(x=20, y=355)

        self.id_label_product_color_invoice = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Cor Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_color_invoice.place(x=45,y=395)


        def Start_Option_Invoice_Color_Product(choice):
            brand_choice = self.optionmenu_brand_invoice.get()

            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            model_choice = self.optionmenu_model_invoice.get()

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)

            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == model_choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass

            product_names = self.Search_Color_Product_Two()
            name_products = []
            for x in product_names:
                y = str(x)
                k = y.split(': ')
                name_products.append(k)

            for numproduct, nummodelproduct, nameproduct in name_products:
                if nameproduct == choice:
                    if int(nummodelproduct) == modelnum:
                        id_product=int(numproduct)

            product_0123 = []
            connect_db = Database_Color()
            product_stock_color = connect_db.Fetch_Color()
            for color in product_stock_color:
                if color[3] == modelnum:
                    if color[4] == id_product:
                        product_0123.append(color[5])
                    product_color_in_order = set(product_0123)
                    product_color_in_order01 = sorted(product_color_in_order)
            if not product_0123:
                print('vazio')
                self.optionmenu_product_color_invoice = customtkinter.CTkOptionMenu(
                    self.frame_internal_invoice,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Brand_Callback_Color_Invoice
                    )
                self.optionmenu_product_color_invoice.place(x=20, y=425) 
            else:
                print(product_0123)
                self.optionmenu_product_color_invoice = customtkinter.CTkOptionMenu(
                    self.frame_internal_invoice,
                    dynamic_resizing=False,
                    values=product_color_in_order01,
                    width=160,
                    command=Option_Brand_Callback_Color_Invoice
                    )
                self.optionmenu_product_color_invoice.set('Escolha COR')
                self.optionmenu_product_color_invoice.place(x=20, y=425) 

        def Option_Brand_Callback_Color_Invoice(choice):
            self.Add_to_Treeview_Invoice_Color()


        self.optionmenu_product_color_invoice = customtkinter.CTkOptionMenu(
            self.frame_internal_invoice,
            dynamic_resizing=False,
            values=['Escolha COR'],
            width=160,
            command=Option_Brand_Callback_Color_Invoice
            )
        self.optionmenu_product_color_invoice.place(x=20, y=425)

        self.id_label_product_invoice_amount = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Quantidade Itens:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_invoice_amount.place(x=25,y=465)

        self.id_entry_product_invoice_amount = customtkinter.CTkEntry(
            self.frame_internal_invoice,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_product_invoice_amount.place(x=20, y=495)

        self.id_label_product_invoice_unitary_value = customtkinter.CTkLabel(
            self.frame_internal_invoice,
            font=self.font2,
            text='Valor Unitário:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_invoice_unitary_value.place(x=35,y=535)

        self.id_entry_product_invoice_unitary_value = customtkinter.CTkEntry(
            self.frame_internal_invoice,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_product_invoice_unitary_value.place(x=20, y=565)

        self.id_entry_id_product_invoice = customtkinter.CTkEntry(
            self.frame_internal_invoice,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        # self.id_entry_id_product_stock.place(x=20, y=450)

        self.id_entry_id_product_invoice_amount_return = customtkinter.CTkEntry(
            self.frame_internal_invoice,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        # self.id_entry_id_product_stock_amount.place(x=20, y=450)

        self.add_button_product_invoice = customtkinter.CTkButton(
            self.frame_internal_invoice,
            font=self.font2,
            command=self.Insert_Invoice,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.add_button_product_invoice.place(x=15,y=615)

        self.clear_button_product_invoice = customtkinter.CTkButton(
            self.frame_internal_invoice,
            font=self.font2,
            command=lambda:self.Clear_Entry_Invoice(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_product_invoice.place(x=108,y=615)

        self.frame_internal_invoice_01 = customtkinter.CTkFrame(
            self.tabview.tab("PRODUTO"),
            corner_radius=10,
            )
        self.frame_internal_invoice_01.pack(
            side=tkinter.LEFT, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.Y,
            expand=False,
            padx=0,
            pady=50
            )
        self.frame_internal_invoice_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_invoice_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_invoice_01.grid_rowconfigure(0, weight=1)



        style = ttk.Style(self.frame_internal_invoice_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_invoice = ttk.Treeview(self.frame_internal_invoice_01, height=15,)
        self.table_invoice['columns'] = ('ID','MARCA', 'MODELO', 'PRODUTO', 'COR', 'QUANTIDADE')
        self.table_invoice.column('#0', width=0, stretch=tkinter.NO)
        self.table_invoice.column('ID', width=0, stretch=tkinter.NO)
        self.table_invoice.column('MARCA', anchor=tkinter.CENTER, width=250)
        self.table_invoice.column('MODELO', anchor=tkinter.CENTER, width=350)
        self.table_invoice.column('PRODUTO', anchor=tkinter.CENTER, width=650)
        self.table_invoice.column('COR', anchor=tkinter.CENTER, width=250)
        self.table_invoice.column('QUANTIDADE', anchor=tkinter.CENTER, width=180)

        self.table_invoice.heading('ID', text = 'ID')
        self.table_invoice.heading('MARCA', text = 'MARCA')
        self.table_invoice.heading('MODELO', text = 'MODELO')
        self.table_invoice.heading('PRODUTO', text = 'PRODUTO')
        self.table_invoice.heading('COR', text = 'COR')
        self.table_invoice.heading('QUANTIDADE', text = 'QUANTIDADE')
        self.table_invoice.pack(fill = 'both', expand = False)

        self.table_invoice.bind('<ButtonRelease>', self.Display_Data_Invoice)

        self.Add_to_Treeview_Invoice()

        self.title_label_table = customtkinter.CTkLabel(
            self.frame_internal_invoice_01,
            font=self.font1,
            text='',
            text_color='#fff',
            )
        self.title_label_table.pack()


        style = ttk.Style(self.frame_internal_invoice_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_invoice_num = ttk.Treeview(self.frame_internal_invoice_01, height=30,)
        self.table_invoice_num['columns'] = ('ID', 'FORNECEDOR', 'N° NOTA', 'MARCA', 'MODELO', 'PRODUTO', 'COR', 'QUANTIDADE')
        self.table_invoice_num.column('#0', width=0, stretch=tkinter.NO)
        self.table_invoice_num.column('ID', width=0, stretch=tkinter.NO)
        self.table_invoice_num.column('FORNECEDOR', anchor=tkinter.CENTER, width=250)
        self.table_invoice_num.column('N° NOTA', anchor=tkinter.CENTER, width=200)
        self.table_invoice_num.column('MARCA', anchor=tkinter.CENTER, width=250)
        self.table_invoice_num.column('MODELO', anchor=tkinter.CENTER, width=250)
        self.table_invoice_num.column('PRODUTO', anchor=tkinter.CENTER, width=300)
        self.table_invoice_num.column('COR', anchor=tkinter.CENTER, width=180)
        self.table_invoice_num.column('QUANTIDADE', anchor=tkinter.CENTER, width=130)

        self.table_invoice_num.heading('ID', text = 'ID')
        self.table_invoice_num.heading('FORNECEDOR', text = 'FORNECEDOR')
        self.table_invoice_num.heading('N° NOTA', text = 'N° NOTA')
        self.table_invoice_num.heading('MARCA', text = 'MARCA')
        self.table_invoice_num.heading('MODELO', text = 'MODELO')
        self.table_invoice_num.heading('PRODUTO', text = 'PRODUTO')
        self.table_invoice_num.heading('COR', text = 'COR')
        self.table_invoice_num.heading('QUANTIDADE', text = 'QUANTIDADE')
        self.table_invoice_num.pack(fill = 'both', expand = False)

        self.table_invoice_num.bind('<ButtonRelease>', self.Display_Data_Invoice)

        self.Add_to_Treeview_Invoice_Num()

        # *************  PAGE_ENTRADA_NOTA_PRODUTOS  ********************


        # ****************  PAGE_CONSULTA_NOTA1  ************************

        self.frame_internal_consult = customtkinter.CTkFrame(
            self.tabview.tab("CONSULTA 1"),
            corner_radius=10,
            )
        self.frame_internal_consult.pack(
            # top, bottom, left, or right
            side=tkinter.TOP, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.X,
            expand=False,
            padx=350,
            pady=0,
            )
        self.frame_internal_consult.grid_columnconfigure(1, weight=1)
        self.frame_internal_consult.grid_rowconfigure(1, weight=0)
        self.frame_internal_consult.grid_rowconfigure(0, weight=1)


        # ****************  PAGE_CONSULTA_NOTA1  ************************

        self.title_label_space = customtkinter.CTkLabel(
            self.frame_internal_consult,
            font=self.font1,
            text='',
            text_color='#fff',
            )
        self.title_label_space.place(x=230,y=0)

        self.title_label_consult = customtkinter.CTkLabel(
            self.frame_internal_consult,
            font=self.font1,
            text='Consulta Nota',
            text_color='#fff',
            )
        self.title_label_consult.place(x=230,y=35)

        self.frame_consult = customtkinter.CTkFrame(
            self.frame_internal_consult,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=660,
            height=110
            )
        self.frame_consult.place(x=0,y=70)

        self.id_label_consult = customtkinter.CTkLabel(
            self.frame_internal_consult,
            font=self.font2,
            text='Fornecedor:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_consult.place(x=45,y=90)

        supplier_option_invoice = []
        connect_db = Database_Supplier()
        supplier_names = connect_db.Fetch_Supplier()
        for supplier in supplier_names:
            supplier_option_invoice.append(supplier[2])
        brands_in_order = sorted(supplier_option_invoice)

        def Option_Callback_Supplier_Consult(choice):
            # print("optionmenu dropdown clicked:", choice)
            Start_Option_Invoice_Num(choice=choice)
            self.Add_to_Treeview_Invoice_Consult()

        self.optionmenu_supplier_name_consult = customtkinter.CTkOptionMenu(
            self.frame_internal_consult,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Callback_Supplier_Consult
            )
        self.optionmenu_supplier_name_consult.set('FORNECEDOR')
        self.optionmenu_supplier_name_consult.place(x=20,y=120)


        self.id_label_num_invoice_consult = customtkinter.CTkLabel(
            self.frame_internal_consult,
            font=self.font2,
            text='Número Nota:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_num_invoice_consult.place(x=220,y=90)


        def Start_Option_Invoice_Num(choice):

            supplier_option_invoice = []
            connect_db = Database_Invoice()
            suppliers = connect_db.Fetch_Invoice()
            supplier_name = self.optionmenu_supplier_name_consult.get()
            for supplier in suppliers:
                if supplier[4] == supplier_name:
                    supplier_option_invoice.append(supplier[3])
            invoice_in_order1 = list(set(supplier_option_invoice))
            invoice_in_order = sorted(invoice_in_order1)
            if not invoice_in_order:
                self.optionmenu_num_invoice_consult = customtkinter.CTkOptionMenu(
                    self.frame_internal_consult,
                    dynamic_resizing=False,
                    values=['SEM NOTAS'],
                    width=160,
                    command=Option_Callback_Supplier_Consult_Invoice
                    )
                self.optionmenu_num_invoice_consult.place(x=200, y=120)
            else:
                self.optionmenu_num_invoice_consult = customtkinter.CTkOptionMenu(
                    self.frame_internal_consult,
                    dynamic_resizing=False,
                    values=invoice_in_order,
                    width=160,
                    command=Option_Callback_Supplier_Consult_Invoice
                    )
                self.optionmenu_num_invoice_consult.set('Escolha Fornecedor')
                self.optionmenu_num_invoice_consult.place(x=200, y=120)


        def Option_Callback_Supplier_Consult_Invoice(choice):
            Start_Option_Invoice_Num_Brand(choice=choice)
            self.Add_to_Treeview_Invoice_Consult_Num()



        self.optionmenu_num_invoice_consult = customtkinter.CTkOptionMenu(
            self.frame_internal_consult,
            dynamic_resizing=False,
            values=['Escolha Fornecedor'],
            width=160,
            command=Option_Callback_Supplier_Consult_Invoice
            )
        self.optionmenu_num_invoice_consult.place(x=200, y=120)


        self.id_label_brand_invoice_consult = customtkinter.CTkLabel(
            self.frame_internal_consult,
            font=self.font2,
            text='Nome Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_brand_invoice_consult.place(x=395,y=90)


        def Invoice_Search_Stock_Brand():
            connect_db = Database_Stock()
            products = connect_db.Fetch_Stock()
            stock_name_id = []
            for product in products:
                stock_name_id.append(f'{product[0]}: {product[2]}')
            return stock_name_id
        

        def Start_Option_Invoice_Num_Brand(choice):
            brands_names_ids = self.Search_Product_Brand()
            brands_names_ids2 = []
            for x in brands_names_ids:
                y = str(x)
                k = y.split(': ')
                brands_names_ids2.append(k)

            supplier_option_invoice_brand = []
            connect_db = Database_Invoice()
            suppliers = connect_db.Fetch_Invoice()
            supplier_name = self.optionmenu_supplier_name_consult.get()
            for supplier in suppliers:
                if supplier[4] == supplier_name:
                    if supplier[3] == choice:
                        supplier_option_invoice_brand.append(supplier[5])
            invoice_in_order = sorted(supplier_option_invoice_brand)
            print(invoice_in_order)

            items_brands_stock = Invoice_Search_Stock_Brand()
            ids_brands = []
            for x in items_brands_stock:
                y = str(x)
                k = y.split(': ')
                ids_brands.append(k)
            invoice_in_order1 = []
            for invoice_brands_num in invoice_in_order:
                for id_stock, id_brand in ids_brands:
                    if str(id_stock) == str(invoice_brands_num):
                        print(f'{invoice_brands_num} = {id_brand}')
                        invoice_in_order1.append(id_brand)
                    else:
                        pass

            invoice_in_order2 = sorted(invoice_in_order1)
            print(invoice_in_order2)
            names_brands = []
            for brands_num in invoice_in_order2:
                for id_brand2, name_brand2 in brands_names_ids2:
                    if str(id_brand2) == str(brands_num):
                        print(f'{brands_num} = {name_brand2}')
                        names_brands.append(name_brand2)
                    else:
                        pass
            names_brands2 = list(set(names_brands))
            names_brands3 = sorted(names_brands2)
            if not names_brands3:
                self.optionmenu_brand_invoice_consult = customtkinter.CTkOptionMenu(
                    self.frame_internal_consult,
                    dynamic_resizing=False,
                    values=['SEM NOTAS'],
                    width=160,
                    command=Option_Callback_Supplier_Consult_Brand
                    )
                self.optionmenu_brand_invoice_consult.place(x=380, y=120)
            else:
                # print(models_0123)
                self.optionmenu_brand_invoice_consult = customtkinter.CTkOptionMenu(
                    self.frame_internal_consult,
                    dynamic_resizing=False,
                    values=names_brands3,
                    width=160,
                    command=Option_Callback_Supplier_Consult_Brand
                    )
                self.optionmenu_brand_invoice_consult.set('Escolha Fornecedor')
                self.optionmenu_brand_invoice_consult.place(x=380, y=120)


        def Option_Callback_Supplier_Consult_Brand(choice):
            self.Add_to_Treeview_Invoice_Consult_Brand()


        self.optionmenu_brand_invoice_consult = customtkinter.CTkOptionMenu(
            self.frame_internal_consult,
            dynamic_resizing=False,
            values=['Escolha Fornecedor'],
            width=160,
            command=Option_Callback_Supplier_Consult_Brand
            )
        self.optionmenu_brand_invoice_consult.place(x=380, y=120)


        self.clear_button_product_invoice_consult = customtkinter.CTkButton(
            self.frame_internal_consult,
            font=self.font2,
            command=lambda:self.Clear_Entry_Invoice_Consult(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_product_invoice_consult.place(x=560,y=120)

        self.frame_internal_consult_01 = customtkinter.CTkFrame(
            self.tabview.tab("CONSULTA 1"),
            corner_radius=10,
            )
        self.frame_internal_consult_01.pack(
            side=tkinter.TOP, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.X,
            expand=False,
            padx=25,
            pady=5,
            )
        self.frame_internal_consult_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_consult_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_consult_01.grid_rowconfigure(0, weight=1)


        style = ttk.Style(self.frame_internal_consult_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_invoice_consult = ttk.Treeview(self.frame_internal_consult_01, height=45,)
        self.table_invoice_consult['columns'] = ('ID', 'FORNECEDOR', 'N° NOTA', 'MARCA', 'MODELO', 'PRODUTO', 'COR', 'QUANTIDADE', 'VALOR')
        self.table_invoice_consult.column('#0', width=0, stretch=tkinter.NO)
        self.table_invoice_consult.column('ID', width=0, stretch=tkinter.NO)
        self.table_invoice_consult.column('FORNECEDOR', anchor=tkinter.CENTER, width=250)
        self.table_invoice_consult.column('N° NOTA', anchor=tkinter.CENTER, width=200)
        self.table_invoice_consult.column('MARCA', anchor=tkinter.CENTER, width=250)
        self.table_invoice_consult.column('MODELO', anchor=tkinter.CENTER, width=250)
        self.table_invoice_consult.column('PRODUTO', anchor=tkinter.CENTER, width=300)
        self.table_invoice_consult.column('COR', anchor=tkinter.CENTER, width=180)
        self.table_invoice_consult.column('QUANTIDADE', anchor=tkinter.CENTER, width=130)
        self.table_invoice_consult.column('VALOR', anchor=tkinter.CENTER, width=130)

        self.table_invoice_consult.heading('ID', text = 'ID')
        self.table_invoice_consult.heading('FORNECEDOR', text = 'FORNECEDOR')
        self.table_invoice_consult.heading('N° NOTA', text = 'N° NOTA')
        self.table_invoice_consult.heading('MARCA', text = 'MARCA')
        self.table_invoice_consult.heading('MODELO', text = 'MODELO')
        self.table_invoice_consult.heading('PRODUTO', text = 'PRODUTO')
        self.table_invoice_consult.heading('COR', text = 'COR')
        self.table_invoice_consult.heading('QUANTIDADE', text = 'QUANTIDADE')
        self.table_invoice_consult.heading('VALOR', text = 'VALOR')
        self.table_invoice_consult.pack(fill = 'both', expand = False)

        self.table_invoice_consult.bind('<ButtonRelease>', self.Display_Data_Invoice_Consult)

        self.Add_to_Treeview_Invoice_Consult()

        # ****************  PAGE_CONSULTA_NOTA1  ************************

        # ****************  Window_Notas  ************************


        # ****************  Window_Vendas  ************************

    #  self.right_dashboard   ----> dashboard widget
    def Window_Entry_Sales(self):
        self.clear_frame()

        self.tabview  = customtkinter.CTkTabview(master=self.right_dashboard)
        self.tabview.pack(fill='both', expand=1, padx=10, pady=10)

        self.tabview.add("VENDAS")


        # ****************  PAGE_VENDAS_FRENTE  ************************

        self.frame_internal_checkout = customtkinter.CTkFrame(
            self.tabview.tab("VENDAS"),
            corner_radius=10,
            )
        self.frame_internal_checkout.pack(
            # top, bottom, left, or right
            side=tkinter.TOP, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.X,
            expand=False,
            padx=150,
            pady=0,
            )
        self.frame_internal_checkout.grid_columnconfigure(1, weight=1)
        self.frame_internal_checkout.grid_rowconfigure(1, weight=0)
        self.frame_internal_checkout.grid_rowconfigure(0, weight=1)


        # ****************  PAGE_VENDAS_FRENTE  ************************

        self.title_label_space = customtkinter.CTkLabel(
            self.frame_internal_checkout,
            font=self.font1,
            text='',
            text_color='#fff',
            )
        self.title_label_space.place(x=230,y=0)

        self.title_label_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout,
            font=self.font1,
            text='Selecione Item',
            text_color='#fff',
            )
        self.title_label_checkout.place(x=480,y=35)

        self.frame_checkout = customtkinter.CTkFrame(
            self.frame_internal_checkout,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=1120,
            height=110
            )
        self.frame_checkout.place(x=0,y=70)

        self.id_label_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout,
            font=self.font2,
            text='Marca:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_checkout.place(x=70,y=90)

        brands_option_invoice = []
        connect_db = Database_Brand()
        brands_stock = connect_db.Fetch_Brand()
        for brands in brands_stock:
            brands_option_invoice.append(brands[2])
        brands_in_order = sorted(brands_option_invoice)

        def Option_Brand_Callback_Checkout(choice):
            Start_Option_Checkout_Brand(choice=choice)
            self.Add_to_Treeview_Checkout_Brand()

        self.optionmenu_brand_name_checkout = customtkinter.CTkOptionMenu(
            self.frame_internal_checkout,
            dynamic_resizing=False,
            values=brands_in_order,
            width=160,
            command=Option_Brand_Callback_Checkout
            )
        self.optionmenu_brand_name_checkout.set('Escolha MARCA')
        self.optionmenu_brand_name_checkout.place(x=20,y=120)


        self.id_label_model_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout,
            font=self.font2,
            text='Modelo:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_model_checkout.place(x=240,y=90)


        def Start_Option_Checkout_Brand(choice):
            brands_names = self.Search_Product_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == choice:
                    bran=int(numbrand)

            models_0123 = []
            connect_db = Database_Model()
            models_products = connect_db.Fetch_Model()
            for brands in models_products:
                if brands[2] == bran:
                    models_0123.append(brands[3])
            models_in_order = sorted(models_0123)
            
            if not models_0123:
                self.optionmenu_model_name_checkout = customtkinter.CTkOptionMenu(
                    self.frame_internal_checkout,
                    dynamic_resizing=False,
                    values=['SEM MODELOS'],
                    width=160,
                    command=Option_Brand_Callback_Model_Checkout
                    )
                self.optionmenu_model_name_checkout.place(x=200, y=120)
            else:
                self.optionmenu_model_name_checkout = customtkinter.CTkOptionMenu(
                    self.frame_internal_checkout,
                    dynamic_resizing=False,
                    values=models_in_order,
                    width=160,
                    command=Option_Brand_Callback_Model_Checkout
                    )
                self.optionmenu_model_name_checkout.set('Escolha MODELO')
                self.optionmenu_model_name_checkout.place(x=200, y=120)


        def Option_Brand_Callback_Model_Checkout(choice):
            Start_Option_Checkout_Model(choice=choice)
            self.Add_to_Treeview_Checkout_Model()

        self.optionmenu_model_name_checkout = customtkinter.CTkOptionMenu(
            self.frame_internal_checkout,
            dynamic_resizing=False,
            values=['Escolha MODELO'],
            width=160,
            command=Option_Brand_Callback_Model_Checkout
            )
        self.optionmenu_model_name_checkout.place(x=200, y=120)

        self.id_label_brand_invoice_consult = customtkinter.CTkLabel(
            self.frame_internal_checkout,
            font=self.font2,
            text='Produto:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_brand_invoice_consult.place(x=415,y=90)

        def Start_Option_Checkout_Model(choice):
            brand_choice = self.optionmenu_brand_name_checkout.get()
            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)
                
            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass

            product_0123 = []
            connect_db = Database_Product()
            models_stock = connect_db.Fetch_Product()
            for models in models_stock:
                if models[2] == bran:
                    if models[3] == modelnum:
                        product_0123.append(models[4])
            product_in_order = set(product_0123)
            product_in_order01 = sorted(product_in_order)

            if not product_0123:
                self.optionmenu_product_name_checkout = customtkinter.CTkOptionMenu(
                    self.frame_internal_checkout,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Callback_Product_Checkout
                    )
                self.optionmenu_product_name_checkout.place(x=380, y=120)
            else:
                self.optionmenu_product_name_checkout = customtkinter.CTkOptionMenu(
                    self.frame_internal_checkout,
                    dynamic_resizing=False,
                    values=product_in_order01,
                    width=160,
                    command=Option_Callback_Product_Checkout
                    )
                self.optionmenu_product_name_checkout.set('Escolha PRODUTO')
                self.optionmenu_product_name_checkout.place(x=380, y=120)


        def Option_Callback_Product_Checkout(choice):
            Start_Option_Checkout_Color_Product(choice=choice)
            self.Add_to_Treeview_Checkout_Product()

        self.optionmenu_product_name_checkout = customtkinter.CTkOptionMenu(
            self.frame_internal_checkout,
            dynamic_resizing=False,
            values=['Escolha PRODUTO'],
            width=160,
            command=Option_Callback_Product_Checkout
            )
        self.optionmenu_product_name_checkout.place(x=380, y=120)

        self.id_label_color_name_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout,
            font=self.font2,
            text='Cor:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_color_name_checkout.place(x=610,y=90)


        def Start_Option_Checkout_Color_Product(choice):

            brand_choice = self.optionmenu_brand_name_checkout.get()
            brands_names = self.Search_Color_Brand()
            item_brands = []
            for x in brands_names:
                y = str(x)
                k = y.split(': ')
                item_brands.append(k)

            for numbrand, namebrand in item_brands:
                if namebrand == brand_choice:
                    bran=int(numbrand)

            model_choice = self.optionmenu_model_name_checkout.get()

            models_names = self.Search_Color_Model_Two()
            item_models = []
            for x in models_names:
                y = str(x)
                k = y.split(': ')
                item_models.append(k)

            for nummodel, brandmodel, namemodel in item_models:
                if namemodel == model_choice:
                    if int(brandmodel) == bran:
                        modelnum=int(nummodel)
                    else:
                        pass
                else:
                    pass

            product_names = self.Search_Color_Product_Two()
            name_products = []
            for x in product_names:
                y = str(x)
                k = y.split(': ')
                name_products.append(k)

            for numproduct, nummodelproduct, nameproduct in name_products:
                if nameproduct == choice:
                    if int(nummodelproduct) == modelnum:
                        id_product=int(numproduct)

            product_0123 = []
            connect_db = Database_Color()
            product_stock_color = connect_db.Fetch_Color()
            for color in product_stock_color:
                if color[3] == modelnum:
                    if color[4] == id_product:
                        product_0123.append(color[5])
                    product_color_in_order = set(product_0123)
                    product_color_in_order01 = sorted(product_color_in_order)
            if not product_0123:
                self.optionmenu_color_name_checkout = customtkinter.CTkOptionMenu(
                    self.frame_internal_checkout,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Callback_Color_Checkout
                    )
                self.optionmenu_color_name_checkout.place(x=560,y=120) 
            else:
                self.optionmenu_color_name_checkout = customtkinter.CTkOptionMenu(
                    self.frame_internal_checkout,
                    dynamic_resizing=False,
                    values=product_color_in_order01,
                    width=160,
                    command=Option_Callback_Color_Checkout
                    )
                self.optionmenu_color_name_checkout.set('Escolha COR')
                self.optionmenu_color_name_checkout.place(x=560,y=120)

        def Option_Callback_Color_Checkout(choice):
            self.Add_to_Treeview_Checkout_Color()


        self.optionmenu_color_name_checkout = customtkinter.CTkOptionMenu(
            self.frame_internal_checkout,
            dynamic_resizing=False,
            values=['Escolha COR'],
            width=160,
            command=Option_Callback_Color_Checkout
            )
        self.optionmenu_color_name_checkout.place(x=560,y=120)

        self.clear_button_product_checkout = customtkinter.CTkButton(
            self.frame_internal_checkout,
            font=self.font2,
            command=lambda:self.Clear_Entry_Checkout_Consult(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_product_checkout.place(x=740,y=120)

        self.id_label_amount_product_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout,
            font=self.font2,
            text='Quantidade:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_amount_product_checkout.place(x=865,y=90)

        self.id_entry_amount_product_checkout = customtkinter.CTkEntry(
            self.frame_internal_checkout,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_amount_product_checkout.place(x=840, y=120)

        self.id_entry_amount_product_checkout01 = customtkinter.CTkEntry(
            self.frame_internal_checkout,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        # self.id_entry_amount_product_checkout.place(x=840, y=120)

        self.add_button_product_checkout = customtkinter.CTkButton(
            self.frame_internal_checkout,
            font=self.font2,
            command=self.Insert_Checkout_Entry,
            text_color='#fff',
            text='Add',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80,
            state='disabled'
            )
        self.add_button_product_checkout.place(x=1020,y=120)
        
        self.frame_internal_checkout_01 = customtkinter.CTkFrame(
            self.tabview.tab("VENDAS"),
            corner_radius=10,
            )
        self.frame_internal_checkout_01.pack(
            side=tkinter.TOP, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.X,
            expand=False,
            padx=25,
            pady=5,
            )
        self.frame_internal_checkout_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_checkout_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_checkout_01.grid_rowconfigure(0, weight=1)


        style = ttk.Style(self.frame_internal_checkout_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_checkout_consult = ttk.Treeview(self.frame_internal_checkout_01, height=10,)
        self.table_checkout_consult['columns'] = ('ID', 'MARCA', 'MODELO', 'PRODUTO', 'COR', 'QUANTIDADE', 'VALOR')
        self.table_checkout_consult.column('#0', width=0, stretch=tkinter.NO)
        self.table_checkout_consult.column('ID', width=0, stretch=tkinter.NO)
        self.table_checkout_consult.column('MARCA', anchor=tkinter.CENTER, width=250)
        self.table_checkout_consult.column('MODELO', anchor=tkinter.CENTER, width=250)
        self.table_checkout_consult.column('PRODUTO', anchor=tkinter.CENTER, width=300)
        self.table_checkout_consult.column('COR', anchor=tkinter.CENTER, width=180)
        self.table_checkout_consult.column('QUANTIDADE', anchor=tkinter.CENTER, width=130)
        self.table_checkout_consult.column('VALOR', anchor=tkinter.CENTER, width=130)

        self.table_checkout_consult.heading('ID', text = 'ID')
        self.table_checkout_consult.heading('MARCA', text = 'MARCA')
        self.table_checkout_consult.heading('MODELO', text = 'MODELO')
        self.table_checkout_consult.heading('PRODUTO', text = 'PRODUTO')
        self.table_checkout_consult.heading('COR', text = 'COR')
        self.table_checkout_consult.heading('QUANTIDADE', text = 'QUANTIDADE')
        self.table_checkout_consult.heading('VALOR', text = 'VALOR')
        self.table_checkout_consult.pack(fill = 'both', expand = False)

        self.table_checkout_consult.bind('<ButtonRelease>', self.Display_Data_Checkout_Consult)

        self.Add_to_Treeview_Checkout_Brand()


        self.title_label_table = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font1,
            text='',
            text_color='#fff',
            )
        self.title_label_table.pack()

        style = ttk.Style(self.frame_internal_checkout_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_checkout = ttk.Treeview(self.frame_internal_checkout_01, height=20,)
        self.table_checkout['columns'] = ('ID', 'ITEM', 'PRODUTO', 'QUANTIDADE', 'VALOR', 'N_STOCK')
        self.table_checkout.column('#0', width=0, stretch=tkinter.NO)
        self.table_checkout.column('ID', width=0, stretch=tkinter.NO)
        self.table_checkout.column('ITEM', anchor=tkinter.CENTER, width=50)
        self.table_checkout.column('PRODUTO', anchor=tkinter.CENTER, width=750)
        self.table_checkout.column('QUANTIDADE', anchor=tkinter.CENTER, width=200)
        self.table_checkout.column('VALOR', anchor=tkinter.CENTER, width=250)
        self.table_checkout.column('N_STOCK', width=0, stretch=tkinter.NO)

        self.table_checkout.heading('ID', text = 'ID')
        self.table_checkout.heading('ITEM', text = 'ITEM')
        self.table_checkout.heading('PRODUTO', text = 'PRODUTO')
        self.table_checkout.heading('QUANTIDADE', text = 'QUANTIDADE')
        self.table_checkout.heading('VALOR', text = 'VALOR')
        self.table_checkout.heading('N_STOCK', text = 'N_STOCK')
        self.table_checkout.pack(fill = 'both', expand = False)

        self.table_checkout.bind('<ButtonRelease>', self.Display_Data_Checkout_Item)


        self.id_label_ = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='',
            text_color='#fff',
            )
        self.id_label_.pack()
        self.id_label_ = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='',
            text_color='#fff',
            )
        self.id_label_.pack()
        self.id_label_ = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='',
            text_color='#fff',
            )
        self.id_label_.pack()
        self.id_label_ = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='',
            text_color='#fff',
            )
        self.id_label_.pack()

        self.id_label_edit_item_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='Item:',
            text_color='#fff',
            )
        self.id_label_edit_item_checkout.place(x=55, y=480)

        self.id_entry_edit_item_checkout = customtkinter.CTkEntry(
            self.frame_internal_checkout_01,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            state='disabled'
            )
        self.id_entry_edit_item_checkout.place(x=0, y=510)

        self.delete_button_item_checkout = customtkinter.CTkButton(
            self.frame_internal_checkout_01,
            font=self.font2,
            command=self.Delete_Checkout_Item,
            text_color='#fff',
            text='Delete',
            fg_color='#D20B02',
            hover_color='#8F0600',
            cursor='hand2',
            corner_radius=8,
            width=80,
            state='disabled'
            )
        self.delete_button_item_checkout.place(x=40,y=550)

        self.id_label_qts_item_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='Total Itens:',
            text_color='#fff',
            )
        self.id_label_qts_item_checkout.place(x=210, y=480)

        self.id_entry_qts_item_checkout = customtkinter.CTkEntry(
            self.frame_internal_checkout_01,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_qts_item_checkout.place(x=180, y=510)

        self.id_label_sum_checkout = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='Total R$:',
            text_color='#fff',
            )
        self.id_label_sum_checkout.place(x=400, y=480)

        self.id_entry_sum_checkout = customtkinter.CTkEntry(
            self.frame_internal_checkout_01,
            font=self.font2,
            text_color='#000',
            fg_color='#fff',
            border_color='#B2016C',
            border_width=2,
            width=160,
            )
        self.id_entry_sum_checkout.place(x=360, y=510)

        self.id_label_form_of_payment = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='Pagamento:',
            text_color='#fff',
            )
        self.id_label_form_of_payment.place(x=560, y=480)

        form_of_payment = ['Dinheiro', 'Pix', 'Débito', 'Crédito']

        def Option_Form_Of_Payment(choice):
            self.optionmenu_number_payment.set('PARCELAS')
            self.optionmenu_number_payment.configure(state='disabled')
            self.add_button_sum_checkout.configure(state='disabled')
            if choice == 'Crédito':
                self.optionmenu_number_payment.configure(state='normal')
            else:
                self.add_button_sum_checkout.configure(state='normal')


        self.optionmenu_form_of_payment = customtkinter.CTkOptionMenu(
            self.frame_internal_checkout_01,
            dynamic_resizing=False,
            values=form_of_payment,
            width=160,
            command=Option_Form_Of_Payment
            )
        self.optionmenu_form_of_payment.set('PAGAMENTO')
        self.optionmenu_form_of_payment.place(x=540,y=510)

        self.id_label_number_payment = customtkinter.CTkLabel(
            self.frame_internal_checkout_01,
            font=self.font2,
            text='Parcelas:',
            text_color='#fff',
            )
        self.id_label_number_payment.place(x=750, y=480)

        number_of_installments = ['1x', '2x', '3x']

        def Option_Number_Payment(choice):
            self.add_button_sum_checkout.configure(state='normal')

        self.optionmenu_number_payment = customtkinter.CTkOptionMenu(
            self.frame_internal_checkout_01,
            dynamic_resizing=False,
            values=number_of_installments,
            width=160,
            command=Option_Number_Payment,
            state='disabled'
            )
        self.optionmenu_number_payment.set('PARCELAS')
        self.optionmenu_number_payment.place(x=720,y=510)

        self.add_button_sum_checkout = customtkinter.CTkButton(
            self.frame_internal_checkout_01,
            font=self.font2,
            command=self.Insert_Finish_Checkout,
            text_color='#fff',
            text='Finalizar',
            fg_color='#047E43',
            hover_color='#025B30',
            cursor='hand2',
            corner_radius=8,
            width=80,
            state='disabled'
            )
        self.add_button_sum_checkout.place(x=900,y=510)


        # ****************  PAGE_VENDAS_FRENTE  ************************


        # ****************  Window_Vendas  ************************


        # ****************  Window_Relatório  ************************


    #  self.right_dashboard   ----> dashboard widget
    def Window_Report(self):
        self.clear_frame()

        self.tabview  = customtkinter.CTkTabview(master=self.right_dashboard)
        self.tabview.pack(fill='both', expand=1, padx=10, pady=10)

        self.tabview.add("RELATÓRIO")


        # ****************  PAGE_RELATORIO  ************************

        self.frame_internal_report = customtkinter.CTkFrame(
            self.tabview.tab("RELATÓRIO"),
            corner_radius=10,
            )
        self.frame_internal_report.pack(
            # top, bottom, left, or right
            side=tkinter.TOP, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.X,
            expand=False,
            padx=150,
            pady=0,
            )
        self.frame_internal_report.grid_columnconfigure(1, weight=1)
        self.frame_internal_report.grid_rowconfigure(1, weight=0)
        self.frame_internal_report.grid_rowconfigure(0, weight=1)


        # ****************  PAGE_RELATORIO  ************************

        self.title_label_space = customtkinter.CTkLabel(
            self.frame_internal_report,
            font=self.font1,
            text='',
            text_color='#fff',
            )
        self.title_label_space.place(x=130,y=0)

        self.title_label_report = customtkinter.CTkLabel(
            self.frame_internal_report,
            font=self.font1,
            text='Relatório Vendas',
            text_color='#fff',
            )
        self.title_label_report.place(x=420,y=35)

        self.frame_report = customtkinter.CTkFrame(
            self.frame_internal_report,
            fg_color='#1B1B21',
            corner_radius=10,
            border_width=2,
            border_color='#fff',
            width=660,
            height=110
            )
        self.frame_report.place(x=200,y=70)

        self.id_label_report = customtkinter.CTkLabel(
            self.frame_internal_report,
            font=self.font2,
            text='Data:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_report.place(x=270,y=90)

        brands_option_invoice = []
        connect_db = Database_Sales()
        brands_stock = connect_db.Fetch_Sales()
        for brands in brands_stock:
            brands_option_invoice.append(brands[2])
        brands_in_order = set(brands_option_invoice)
        brands_in_order1 = sorted(brands_in_order)


        def Option_Date_Callback_Report(choice):
            # print("optionmenu dropdown clicked:", choice)
            Start_Option_Report_Seller(choice=choice)
            self.Add_to_Treeview_Report_Date()

        self.optionmenu_date_report = customtkinter.CTkOptionMenu(
            self.frame_internal_report,
            dynamic_resizing=False,
            values=brands_in_order1,
            width=160,
            command=Option_Date_Callback_Report
            )
        self.optionmenu_date_report.set('Escolha Data')
        self.optionmenu_date_report.place(x=220,y=120)

        self.id_label_seller_name_report = customtkinter.CTkLabel(
            self.frame_internal_report,
            font=self.font2,
            text='Vendedor:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_seller_name_report.place(x=430,y=90)


        def Start_Option_Report_Seller(choice):
            seller_0123 = []
            connect_db = Database_Sales()
            seller_names = connect_db.Fetch_Sales()
            for name in seller_names:
                if name[2] == choice:
                    seller_0123.append(name[3])
            seller_in_order = set(seller_0123)
            seller_in_order1 = sorted(seller_in_order)
            
            if not seller_0123:
                self.optionmenu_seller_name_report = customtkinter.CTkOptionMenu(
                    self.frame_internal_report,
                    dynamic_resizing=False,
                    values=['SEM VENDAS'],
                    width=160,
                    command=Option_Date_Callback_Product_Report
                    )
                self.optionmenu_seller_name_report.place(x=400, y=120)
            else:
                self.optionmenu_seller_name_report = customtkinter.CTkOptionMenu(
                    self.frame_internal_report,
                    dynamic_resizing=False,
                    values=seller_in_order1,
                    width=160,
                    command=Option_Date_Callback_Product_Report
                    )
                self.optionmenu_seller_name_report.set('Escolha Data')
                self.optionmenu_seller_name_report.place(x=400, y=120)


        def Option_Date_Callback_Product_Report(choice):
            Start_Option_Report_Seller_Product(choice=choice)
            self.Add_to_Treeview_Report_Date_Seller()
            pass

        self.optionmenu_seller_name_report = customtkinter.CTkOptionMenu(
            self.frame_internal_report,
            dynamic_resizing=False,
            values=['Escolha Data'],
            width=160,
            command=Option_Date_Callback_Product_Report
            )
        self.optionmenu_seller_name_report.place(x=400, y=120)

        self.id_label_product_name_report_sale = customtkinter.CTkLabel(
            self.frame_internal_report,
            font=self.font2,
            text='Produtos:',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_product_name_report_sale.place(x=610,y=90)


        def Start_Option_Report_Seller_Product(choice):
            date_choice = self.optionmenu_date_report.get()
            seller_name = choice

            product_0123 = []
            connect_db = Database_Sales()
            sales_seller = connect_db.Fetch_Sales()

            for date in sales_seller:
                if date[2] == date_choice:
                    if date[3] == seller_name:
                        product_0123.append(date[5])
            product_in_order = set(product_0123)
            product_in_order01 = sorted(product_in_order)

            if not product_0123:
                self.optionmenu_product_name_report_sale = customtkinter.CTkOptionMenu(
                    self.frame_internal_report,
                    dynamic_resizing=False,
                    values=['SEM PRODUTOS'],
                    width=160,
                    command=Option_Callback_Product_report
                    )
                self.optionmenu_product_name_report_sale.place(x=580, y=120)
            else:
                self.optionmenu_product_name_report_sale = customtkinter.CTkOptionMenu(
                    self.frame_internal_report,
                    dynamic_resizing=False,
                    values=product_in_order01,
                    width=160,
                    command=Option_Callback_Product_report
                    )
                self.optionmenu_product_name_report_sale.set('Escolha Data')
                self.optionmenu_product_name_report_sale.place(x=580, y=120)


        def Option_Callback_Product_report(choice):
            pass

        self.optionmenu_product_name_report_sale = customtkinter.CTkOptionMenu(
            self.frame_internal_report,
            dynamic_resizing=False,
            values=['Escolha Data'],
            width=160,
            command=Option_Callback_Product_report
            )
        self.optionmenu_product_name_report_sale.place(x=580, y=120)

        self.clear_button_product_report = customtkinter.CTkButton(
            self.frame_internal_report,
            font=self.font2,
            command=lambda:self.Clear_Entry_Checkout_Report(True),
            text_color='#fff',
            text='New',
            fg_color='#E93E05',
            hover_color='#A82A00',
            bg_color='#1B1B21',
            cursor='hand2',
            corner_radius=8,
            width=80
            )
        self.clear_button_product_report.place(x=760,y=120)

        self.frame_internal_report_01 = customtkinter.CTkFrame(
            self.tabview.tab("RELATÓRIO"),
            corner_radius=10,
            )
        self.frame_internal_report_01.pack(
            side=tkinter.TOP, #esquerda
            # side=tkinter.RIGHT, #direita
            fill=tkinter.X,
            expand=False,
            padx=25,
            pady=5,
            )
        self.frame_internal_report_01.grid_columnconfigure(1, weight=1)
        self.frame_internal_report_01.grid_rowconfigure(1, weight=0)
        self.frame_internal_report_01.grid_rowconfigure(0, weight=1)


        style = ttk.Style(self.frame_internal_report_01)

        style.theme_use('clam')
        style.configure(style='Treeview',
                        font=self.font3,
                        foreground='#fff',
                        background=self.verde_claro,#0A0B0C',
                        fieldbackground='#1B1B21',
                        )
        style.map('Treeview', background=[('selected', "#AA04A7")])

        self.table_checkout_report = ttk.Treeview(self.frame_internal_report_01, height=10,)
        self.table_checkout_report['columns'] = ('ID', 'DATA', 'COD', 'VENDEDOR', 'ITEM', 'QUANTIDADE', 'VALOR', 'TOTAL', 'PAGAMENTO', 'PARCELADO')
        self.table_checkout_report.column('#0', width=0, stretch=tkinter.NO)
        self.table_checkout_report.column('ID', width=0, stretch=tkinter.NO)
        self.table_checkout_report.column('DATA', anchor=tkinter.CENTER, width=80)
        self.table_checkout_report.column('COD', anchor=tkinter.CENTER, width=80)
        self.table_checkout_report.column('VENDEDOR', anchor=tkinter.CENTER, width=100)
        self.table_checkout_report.column('ITEM', anchor=tkinter.CENTER, width=450)
        self.table_checkout_report.column('QUANTIDADE', anchor=tkinter.CENTER, width=20)
        self.table_checkout_report.column('VALOR', anchor=tkinter.CENTER, width=50)
        self.table_checkout_report.column('TOTAL', anchor=tkinter.CENTER, width=50)
        self.table_checkout_report.column('PAGAMENTO', anchor=tkinter.CENTER, width=80)
        self.table_checkout_report.column('PARCELADO', anchor=tkinter.CENTER, width=80)

        self.table_checkout_report.heading('ID', text = 'ID')
        self.table_checkout_report.heading('DATA', text = 'DATA')
        self.table_checkout_report.heading('COD', text = 'COD')
        self.table_checkout_report.heading('VENDEDOR', text = 'VENDEDOR')
        self.table_checkout_report.heading('ITEM', text = 'ITEM')
        self.table_checkout_report.heading('QUANTIDADE', text = 'QUANTIDADE')
        self.table_checkout_report.heading('VALOR', text = 'VALOR')
        self.table_checkout_report.heading('TOTAL', text = 'TOTAL')
        self.table_checkout_report.heading('PAGAMENTO', text = 'PAGAMENTO')
        self.table_checkout_report.heading('PARCELADO', text = 'PARCELADO')
        self.table_checkout_report.pack(fill = 'both', expand = False)

        self.table_checkout_report.bind('<ButtonRelease>', self.Display_Data_Checkout_Consult)

        self.Add_to_Treeview_Report()

        self.id_label_01 = customtkinter.CTkLabel(
            self.frame_internal_report_01,
            font=self.font2,
            text='',
            text_color='#fff',
            bg_color='#1B1B21'
            )
        self.id_label_01.pack()

        self.Create_Chart()


        # ****************  PAGE_RELATORIO  ************************


        # ****************  Window_Relatório  ************************

    # Change scaling of all widget 80% to 120%
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(
            new_scaling.replace("%", "")
            ) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    # close the entire window
    def close_window(self):
            App.destroy(self)


    # CLEAR ALL THE WIDGET FROM self.right_dashboard(frame) BEFORE loading the widget of the concerned page
    def clear_frame(self):
        for widget in self.right_dashboard.winfo_children():
            widget.destroy()


a = App()
a.mainloop()

