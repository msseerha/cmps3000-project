from datetime import date, datetime
from smart_notifications import NotificationSystem


# USER|BUYER|SELLER|ADMIN CLASSES DETAILING THEIR RESPECTIVE FUNCTIONS
class User:
    """
        Base class representing a system user. Manages global user records,
        the active marketplace catalogue, and shared utility methods.
        """
    users = {'ADMIN': {"name": "ADMIN", "password": "admin", "adminRole": True,
                       "memberStatus": "Platinum", "accountLocked": False, "loginAttempts" : 3},
             'MANU': {"name": "Manu", "password": "secret", "adminRole": False,
                      "memberStatus": "Gold","accountLocked": False, "loginAttempts" : 3},
             'RIPAN': {"name": "Ripan", "password": "data", "adminRole": False,
                       "memberStatus": "Standard", "accountLocked": False, "loginAttempts" : 3},
             'PREET': {"name": "Balpreet", "password": "pointers", "adminRole": False,
                       "memberStatus": "Standard", "accountLocked": False, "loginAttempts" : 3},
             'MANRAJ': {"name": "Manraj", "password": "singh", "adminRole": False,
                        "memberStatus": "Standard", "accountLocked": False, "loginAttempts" : 3}
             }

# Global inventory catalogue of items available for purchase
    Catalogue = {
        "Coffee Mug": {"Price": 52.00, "Seller": "PREET"},
        "Ballpoint Pen": {"Price": 85.00, "Seller": "MANU"},
        "Water Bottle": {"Price": 120.00, "Seller": "RIPAN"},
        "Backpack": {"Price": 245.00, "Seller": "PREET"},
        "Desk Lamp": {"Price": 185.00, "Seller": "MANRAJ"},
        "Wireless Mouse": {"Price": 150.00, "Seller": "MANU"},
        "Mouse Pad": {"Price": 75.00, "Seller": "RIPAN"},
        "Usb Flash Drive": {"Price": 95.00, "Seller": "PREET"},
        "Wall Clock": {"Price": 210.00, "Seller": "MANRAJ"},
        "Sticky Notes": {"Price": 55.00, "Seller": "MANU"},
        "Stapler": {"Price": 115.00, "Seller": "RIPAN"},
        "Scissors": {"Price": 60.00, "Seller": "PREET"},
        "Phone Stand": {"Price": 140.00, "Seller": "MANRAJ"},
        "Charging Cable": {"Price": 89.99, "Seller": "MANU"},
        "Power Bank": {"Price": 350.00, "Seller": "RIPAN"},
        "Earbuds": {"Price": 450.00, "Seller": "PREET"},
        "Key Chain": {"Price": 50.00, "Seller": "MANRAJ"},
        "Desk Organizer": {"Price": 280.00, "Seller": "MANU"},
        "Hand Sanitizer": {"Price": 65.00, "Seller": "RIPAN"},
        "Standing Desk": {"Price": 850.00, "Seller": "PREET"},
        "Ergonomic Chair": {"Price": 1200.00, "Seller": "MANRAJ"},
        "4K Monitor": {"Price": 1450.00, "Seller": "MANU"},
        "Laptop Station": {"Price": 1999.99, "Seller": "RIPAN"}
    }

    BoughtFromCatalogue = {} # Tracks items that have been purchased
    DelistedCatalogue = {} # Tracks items removed by admin action

    Appeal_log = [] # Log for user/seller appeals

    def __init__(self, name, userid, password, adminRole = False, memberStatus = "Standard", accountLocked = False):
        """
                Initializes a new User account, validating unique credentials and constraints
                before registering them into the system.
                """
        try:
            # Check for duplicate user IDs
            if userid in User.users:
                raise ValueError(f"\nRegistration Error: User ID '{userid}' already exists.\n")
            # Validate non-empty fields and spacing constraints
            if userid == "":
                raise ValueError(f"\nRegistration Error: User ID cannot be empty.\n")
            if password == "":
                raise ValueError(f"\nRegistration Error: Password cannot be empty.\n")
            if " " in userid:
                raise ValueError(f"\nRegistration Error: Invalid User ID: '{userid}'.\n")
            # Assign instance attributes
            self.name = name
            self.userid = userid
            self.password = password
            self.adminRole = adminRole
            self.memberStatus = memberStatus
            self.accountLocked = accountLocked
            User.users[self.userid] = {"name": self.name, "password": self.password, "adminRole": self.adminRole, "memberStatus": self.memberStatus, "accountLocked": self.accountLocked, "loginAttempts": 3}
            print(f"\nThe account has been created. You can login now using your username {self.userid} and password.\n")
            # sync with NotificationSystem user list
            NotificationSystem.UserList.append(self.userid)

        except ValueError as e:
            print(e)

    @staticmethod
    def view_catalogue(min_price = 0.00, max_price = float("inf"), seller_id ='ALL'):
        """Displays and filters the catalogue based on price range and specific seller ID."""
        count = 1
        is_seller_found = False
        try:
            for items in User.Catalogue:
                if min_price <= User.Catalogue[items]["Price"] < max_price:
                    if seller_id == 'ALL' or seller_id == User.Catalogue[items]["Seller"]:
                        print(f"{count}. {items}\nPrice: ${float(User.Catalogue[items]['Price']):.2f}\nSeller: {User.Catalogue[items]['Seller']}\n")
                        count += 1

            if count > 1:
                is_seller_found = True

            if max_price < min_price:
                raise ValueError("Input Error: Maximum price cannot be less than minimum price.\n")

            if not is_seller_found:
                print(f'Search Error: Seller {seller_id} not found\n')

        except ValueError as e:
            print(e)
        except KeyError as e:
            print(e)

    def view_user_info(self):
        """Prints current profile details for the logged-in user."""
        print (f"Name: {self.name} | UserID: {self.userid} | Admin Status: {self.adminRole} | Membership: {self.memberStatus}" )

    def set_password(self, password, userid):
        """Updates the password for the specified user account."""
        try:
            if password == "":
                raise ValueError(f"\nRegistration Error: Password cannot be empty.\n")

            self.password = password
            User.users[userid]["password"] = password
            print(f'Password set successfully for: {userid}')
        except ValueError as e:
            print(e)
        except KeyError:
            print(f"Search Error: {userid} not found.")


class Buyer(User):
    """
        Represents a marketplace buyer. Manages shopping carts, payment methods,
        discounts, and purchase history.
        """
    cardTypes = ['VISA','MASTERCARD','AMEX']
    buyer_paymentInfo = {}
    buyer_yearly_expense = {
        'ADMIN': {2026 : 2000.00},
        'MANU':{2026 : 1000.00}
    }
    buyer_purchase_history = {}

    def __init__(self, name, userid, password):
        super().__init__(name, userid, password)
        self.cart = {}
        self.payment = {}
        # self.payment = {"Card Type": None, "Card Number": None, "Expiry Date": None, "CVV": None}
        self.isPaymentValid = False
        self.purchase_history = {}

    @classmethod
    def buyer_login(cls, userid, password):
        """Authenticates buyer credentials, managing login attempts and account locking rules."""

        try:
            if userid not in User.users:
                raise ValueError (f"Login Error: User {userid} does not exist.\n")

            if User.users[userid]["accountLocked"]:
                raise PermissionError (f"Login Error: Account for {userid} is locked. An unlock notification has been sent to the Admin.\n")

            if User.users[userid]["password"] == password:
                buyer_instance = cls.__new__(cls)
                buyer_instance.userid = userid
                buyer_instance.password = password
                buyer_instance.name = User.users[userid]["name"]
                buyer_instance.adminRole = User.users[userid]["adminRole"]
                buyer_instance.memberStatus = User.users[userid]["memberStatus"]
                buyer_instance.cart = {}
                # Retrieve existing purchase history if available
                if userid not in Buyer.buyer_purchase_history:
                    buyer_instance.purchase_history = {}
                else:
                    buyer_instance.purchase_history = Buyer.buyer_purchase_history[userid]
                # Retrieve saved payment info if available
                if userid in Buyer.buyer_paymentInfo:
                    buyer_instance.payment = Buyer.buyer_paymentInfo[userid]
                    buyer_instance.isPaymentValid = True
                else:
                    buyer_instance.payment = {}
                    buyer_instance.isPaymentValid = False
                # Reset login counters
                User.users[userid]["accountLocked"] = False
                User.users[userid]["loginAttempts"] = 3

                return buyer_instance
            else:
                # Decrement attempts on incorrect password
                User.users[userid]["loginAttempts"] -= 1

                if User.users[userid]["loginAttempts"] > 0:
                    raise ValueError(f"Credential Error: Incorrect Password. You have {User.users[userid]["loginAttempts"]} more tries left. \n")
                else:
                    # Lock account and notify admin if attempts hit zero
                    User.users[userid]["accountLocked"] = True
                    NotificationSystem.lockedUsers.append(userid)
                    raise PermissionError (f"Login Error: Account for {userid} is locked. An unlock notification has been sent to the Admin.\n")

        except ValueError as e:
            print(e)

        except PermissionError as e:
            print(e)

    @staticmethod
    def lookup_item(item):
        """Searches for a specific item in the catalogue and displays its price and seller."""
        if item in User.Catalogue:
            print (f'{item} is listed for ${float(User.Catalogue[item]['Price']):.2f} and sold by {User.Catalogue[item]['Seller']}')
        else:
            print (f'{item} not listed in catalogue')

    def add_2_cart (self, item):
        """Moves an item from the active catalogue into the buyer's cart."""
        if item in User.Catalogue:
            self.cart[item] = User.Catalogue[item]
            User.BoughtFromCatalogue[item] = User.Catalogue[item]
            NotificationSystem.soldItems[item] = User.Catalogue[item]
            User.Catalogue.pop(item)
            print (f'{item} added to cart')
        else:
            print (f'{item} not listed in catalogue')

    def remove_item(self, item):
        """Removes an item from the cart and returns it to the main catalogue."""
        if item in self.cart:
            User.Catalogue[item] = self.cart[item]
            self.cart.pop(item)
            User.BoughtFromCatalogue.pop(item)
            NotificationSystem.soldItems.pop(item)
            print ("Item removed from cart")
        else:
            print ("Item not in cart")

    def view_cart (self):
        """Displays all items in the cart, subtotal, and any applicable membership discounts."""
        if len(self.cart) > 0:
            counter = 1
            for items in self.cart:
                print(f"{counter}: {items}: ${self.cart[items]["Price"]:.2f}")
                counter += 1
            cost = self.calculate_cart()
            print('---------------------')
            print(f'Total: ${cost:.2f}')
            discounted_total = self.calculate_discount()
            if self.memberStatus == "Platinum":
                print(f'Since you are a Platinum member. You are eligible for 20% discount.')
                print(f'New Total: {cost:.2f} after 20% rebate = ${discounted_total:.2f}')
            elif self.memberStatus == "Gold":
                print(f'Since you are a Gold member. You are eligible for 10% discount.')
                print(f'New Total: {cost:.2f} after 10% rebate = ${discounted_total:.2f}')
        else:
            print('Your cart is currently empty')

    def add_payment(self, cardType, cardNumber, expiryDate, CVV):
        """Validates and saves credit card payment details based on card type rules."""
        today = datetime.today()
        try:
            if cardType not in Buyer.cardTypes:
                raise ValueError("\nNot a Valid Card Type. Pick between (VISA, MASTERCARD, AMEX)")

            if datetime.strptime(expiryDate, "%Y-%m-%d") >= today:
                # Validation for VISA and MASTERCARD (16 digit card, 3 digit CVV)
                if len(cardNumber) == 16 and cardType != 'AMEX' and len(CVV) == 3:
                    self.payment["Card Number"] = int(cardNumber)
                    self.payment["CVV"] = int(CVV)
                    self.payment["Card Type"] = cardType
                    self.payment["Expiry Date"] = datetime.strptime(expiryDate, "%Y-%m-%d")
                    self.isPaymentValid = True
                    Buyer.buyer_paymentInfo.update({self.userid : self.payment})
                # Validation for AMEX (15 digit card, 4 digit CVV)
                elif len(cardNumber) == 15 and cardType == 'AMEX' and len(CVV) == 4:
                    self.payment["Card Number"] = int(cardNumber)
                    self.payment["CVV"] = int(CVV)
                    self.payment["Card Type"] = cardType
                    self.payment["Expiry Date"] = datetime.strptime(expiryDate, "%Y-%m-%d")
                    self.isPaymentValid = True
                    Buyer.buyer_paymentInfo.update({self.userid : self.payment})
                else:
                    raise ValueError("Invalid Payment Details:\n- Card Number must be 16 Digits (VISA/MASTERCARD) or 15 digits (AMEX)\n- CVV must be 3 digits (VISA/MASTERCARD) or 4 digits (AMEX) ")
                print("\nPayment Method Successfully Added")
            else:
                raise TypeError("ERROR: Invalid Expiry Date")
        except ValueError as e:
            self.payment["Card Number"] = None
            self.payment["CVV"] = None
            self.payment["Card Type"] = None
            self.payment["Expiry Date"] = None
            self.isPaymentValid = False
            print (f'\n{e}')
        except TypeError as e:
            print (f'\n{e}')

    def show_payment_info(self):
        """Displays saved payment method details for the buyer."""
        if self.userid in Buyer.buyer_paymentInfo:
            print (f"Card Type: {Buyer.buyer_paymentInfo[self.userid]['Card Type']}\nCard Number: {Buyer.buyer_paymentInfo[self.userid]['Card Number']}\nExpiry Date: {Buyer.buyer_paymentInfo[self.userid]['Expiry Date']}\nCVV: {Buyer.buyer_paymentInfo[self.userid]['CVV']}")
        else:
            print ("Payment method needs to be added first.")

    def calculate_cart(self):
        """Calculates the raw subtotal cost of all items in the cart."""
        current_value = 0.00
        for item in self.cart:
            current_value += float(self.cart[item]["Price"])
        return current_value

    def eligible_2_upgrade_member_status(self):
        """Evaluates yearly expenses and upgrades membership tiers (Gold/Platinum) when thresholds are met."""
        if self.userid in Buyer.buyer_yearly_expense:
            old_status = self.memberStatus

            if Buyer.buyer_yearly_expense[self.userid][datetime.now().year] >= 2000.00:
                self.memberStatus = "Platinum"
                NotificationSystem.Buyers_Log[self.userid][0] = "Platinum"
            elif Buyer.buyer_yearly_expense[self.userid][datetime.now().year] >= 1000.00:
                self.memberStatus = "Gold"
                NotificationSystem.Buyers_Log[self.userid][0] = "Gold"

            if self.memberStatus != old_status:
                print(f"Congratulations, {self.userid}! Your membership tier has been upgraded to {self.memberStatus}.")
            return True
        return False

    def make_purchase(self):
        """Processes checkout, updates yearly spending totals, evaluates membership upgrades, and logs transaction history."""
        if len(self.cart) > 0 and self.isPaymentValid == True:
            if self.userid not in Buyer.buyer_yearly_expense:
                Buyer.buyer_yearly_expense[self.userid] = {datetime.now().year: 0.00}
            Buyer.buyer_yearly_expense[self.userid][datetime.now().year] += self.calculate_discount()
            # Check for tier upgrades and update notification logs
            if self.memberStatus != "Platinum":
                self.eligible_2_upgrade_member_status()
                if self.memberStatus == "Standard":
                    if 1000.00-float(Buyer.buyer_yearly_expense[self.userid][datetime.now().year]) > 0:
                        NotificationSystem.Buyers_Log[self.userid] = [self.memberStatus,f"[UNLOCK OFFER] Spend ${1000.00-float(Buyer.buyer_yearly_expense[self.userid][datetime.now().year]):.2f} more this year to upgrade your membership to Gold."]
                        # print (f"Spend ${1000.00-float(Buyer.buyer_yearly_expense[self.userid][datetime.now().year]):.2f} more this year to upgrade your membership to Gold.")
                else:
                    if 2000.00-float(Buyer.buyer_yearly_expense[self.userid][datetime.now().year]) > 0:
                        NotificationSystem.Buyers_Log[self.userid] = [self.memberStatus, f"[UNLOCK OFFER] Spend ${2000.00-float(Buyer.buyer_yearly_expense[self.userid][datetime.now().year]):.2f} more this year to upgrade your membership to Platinum."]
                        # print (f"Spend ${2000.00-float(Buyer.buyer_yearly_expense[self.userid][datetime.now().year]):.2f} more this year to upgrade your membership to Platinum.")
            amount_calculate = {'Subtotal' : self.calculate_cart(), 'Total Paid (after discounts)' : self.calculate_discount()}
            combined = self.cart | amount_calculate
            # Record transaction in purchase history
            if date.today() not in self.purchase_history:
                self.purchase_history[date.today()] = {'Transaction ' + str(len(self.purchase_history)+1) : combined}
            else:
                self.purchase_history[date.today()]['Transaction ' + str(len(self.purchase_history[date.today()])+1)] = combined
            self.cart = {}
            Buyer.buyer_purchase_history[self.userid] = self.purchase_history
            print(f"Payment Successful! Your card has been charged with ${amount_calculate['Total Paid (after discounts)']:.2f}. See 'View Purchase History' (Option 9) for details.")
        else:
            if len(self.cart) == 0:
                print("Your cart is currently empty")
            else:
                print("ERROR: Credit Card not set. Use 'Add/Update Payment Method' (Option 7)")

    def view_yearly_expense(self):
        """Displays yearly expense tracking for the buyer."""
        if self.userid in Buyer.buyer_yearly_expense:
            print (f' {Buyer.buyer_yearly_expense[self.userid]}\n')
        else:
            "User does not have any purchase history yet."

    def view_purchase_history(self):
        """Displays historical transaction records grouped by purchase date."""
        if len(self.purchase_history) > 0:
            for trx_date, trx in self.purchase_history.items():
                trx_date = trx_date.strftime("%Y-%m-%d")
                print(trx_date)
                for trx_number, details in trx.items():
                    print(f'\n{trx_number}')
                    for more, extra in details.items():
                        if type(extra) == dict:
                            print(f'{more} | ${extra["Price"]:.2f}')
                        else:
                            print(f'{more}: ${extra:.2f}')
        else:
            print("User does not have any purchase history.")

    def calculate_discount(self):
        """Calculates final price after applying membership rebates (Gold: 10%, Platinum: 20%)."""
        total = self.calculate_cart()
        if self.memberStatus == "Gold":
            total -= total*0.10
        elif self.memberStatus == "Platinum":
            total -= total*0.20
        return float(total)

    def empty_cart(self):
        """Clears cart and restores items back to the general catalogue upon log out."""
        if len(self.cart) > 0:
            for item in self.cart:
                User.Catalogue[item] = self.cart[item]
                User.BoughtFromCatalogue.pop(item,None)
            self.cart = {}

class Seller(User):
    """Represents a marketplace seller. Manages item listings, inventory, and delisting appeals."""
    def __init__(self, name, userid, password):
        super().__init__(name, userid, password)
        self.my_Inventory = {}
        self.my_soldItems = {}
        self.my_delistItems = {}

    @classmethod
    def seller_login(cls, userid, password):
        """Authenticates seller credentials and manages login lockouts."""
        try:
            if userid not in User.users:
                raise ValueError (f"Login Error: User {userid} does not exist.\n")

            if User.users[userid]["accountLocked"]:
                raise PermissionError (f"Login Error: User {userid} is locked. Account unlock Alert has been sent to ADMIN.\n")

            if User.users[userid]["password"] == password:
                seller_instance = cls.__new__(cls)
                seller_instance.userid = userid
                seller_instance.password = password
                seller_instance.name = User.users[userid]["name"]
                # seller_instance.adminRole = User.users[userid]["adminRole"]
                seller_instance.my_Inventory = {}
                seller_instance.my_soldItems = {}
                seller_instance.my_delistItems = {}
                # seller_instance.memberStatus = User.users[userid]["memberStatus"]

                User.users[userid]["accountLocked"] = False
                User.users[userid]["loginAttempts"] = 3

                return seller_instance
            else:
                User.users[userid]["loginAttempts"] -= 1

                if User.users[userid]["loginAttempts"] > 0:
                    raise ValueError(
                        f"Credential Error: Incorrect Password. You have {User.users[userid]["loginAttempts"]} more tries left. \n")
                else:
                    User.users[userid]["accountLocked"] = True
                    NotificationSystem.lockedUsers.append(userid)
                    raise PermissionError (f"Login Error: User {userid} is locked. Account unlock Alert has been sent to ADMIN.\n")

        except ValueError as e:
            print(e)

        except PermissionError as e:
            print(e)

    def add_item4_sale(self, item, price):
        """Lists a new item for sale in the marketplace catalogue."""
        try:
            if float(price):
                User.Catalogue[item] =  {"Price": float(price), "Seller": self.userid}
                print (f"Item {item} listed for ${float(price):.2f}")
            else:
                raise ValueError("Enter valid price")
        except ValueError:
            print("Value Error: Please enter valid price")

    def set_price(self, item, price):
        """Updates the price of an existing item listed by the seller."""
        try:
            if item in User.Catalogue:
                if User.Catalogue[item]["Seller"] == self.userid:
                    if float(price):
                        User.Catalogue[item]["Price"] = float(price)
                    else:
                        print ("Please enter a valid $ amount")
                else:
                    raise PermissionError
            else:
                raise ValueError
        except ValueError:
            print ("Item not in your active listing.")
        except PermissionError:
            print ("You are not the seller for this listing.")

    def delete_item4_sale(self, item):
        """Removes an active item listing from the catalogue."""
        try:
            if item in User.Catalogue:
                if User.Catalogue[item]["Seller"] == self.userid:
                    User.Catalogue.pop(item)
                    print (f'Item {item} removed from your active listing.')
                else:
                    raise PermissionError
            else:
                raise ValueError
        except ValueError:
            print ("Item not in your active listing.")
        except PermissionError:
            print ("You are not the seller for this listing.")

    def view_inventory(self):
        """Displays all active item listings belonging to the seller."""
        for items in User.Catalogue:
            if User.Catalogue[items]["Seller"] == self.userid:
                self.my_Inventory[items] = User.Catalogue[items]
                print (f'{items} | Listed for: ${float(self.my_Inventory[items]["Price"]):.2f}')

        if len(self.my_Inventory) == 0:
            print("No items in your active listing.")


    def view_sold_items(self):
        """Displays items successfully sold by the seller."""
        for items in User.BoughtFromCatalogue:
            if User.BoughtFromCatalogue[items]["Seller"] == self.userid:
                self.my_soldItems[items] = User.BoughtFromCatalogue[items]
                print(f'{items} | Sold for: ${float(self.my_soldItems[items]["Price"]):.2f}')

        if len(self.my_soldItems) == 0:
            print("User has not sold anything yet")

    def view_delisted_items(self):
        """Displays items removed by the admin alongside administrative reasons."""
        for items in User.DelistedCatalogue:
            if User.DelistedCatalogue[items]["Seller"] == self.userid:
                self.my_delistItems[items] = User.DelistedCatalogue[items]
                print(f'{items} | for: ${float(self.my_delistItems[items]["Price"]):.2f} | delisted by Admin | Reason provided: {self.my_delistItems[items]["Reason"]} ')

        if len(self.my_delistItems) == 0:
            print("User has no delisted items")

    def appeal_delisted_item(self, item, message):
        """Allows a seller to submit an appeal to the admin regarding a delisted item."""
        try:
            if item in User.DelistedCatalogue:
                if User.DelistedCatalogue[item]["Seller"] == self.userid:
                    print("Appeal Submitted!")
                    NotificationSystem.send_alert_2_admin(f"{self.userid} requested to appeal the decision to delist item: {item} | Message: {message}")
            else:
                raise ValueError(f"Search Error: No such delisted item - {item} found under seller {self.userid}\n")
        except ValueError as e:
            print(e)

class Admin(User):
    """Represents a system administrator with moderation privileges and user management controls."""
    def __init__(self, name, userid, password):
        super().__init__(name, userid, password, adminRole = True)

    @classmethod
    def admin_login(cls, userid, password):
        """Authenticates admin login credentials and permissions."""
        try:
            if userid not in User.users:
                raise ValueError (f"Login Error: User {userid} does not exist.\n")
            if User.users[userid]["adminRole"] != True:
                raise PermissionError (f"Permission Error: '{userid}' is not allowed to be an Admin.\n")
            if User.users[userid]["accountLocked"]:
                raise PermissionError (f"Login Error: User {userid} is locked. Account unlock Alert has been sent to ADMIN. \n")

            if User.users[userid]["password"] == password:
                admin_instance = cls.__new__(cls)
                admin_instance.name = User.users[userid]["name"]
                admin_instance.userid = userid
                admin_instance.password = password
                admin_instance.adminRole = True
                admin_instance.memberStatus = User.users[userid]["memberStatus"]
                return admin_instance
            else:
                User.users[userid]["loginAttempts"] -= 1
                if User.users[userid]["loginAttempts"] > 0:
                    raise ValueError(f"Credential Error: Incorrect Password. You have {User.users[userid]["loginAttempts"]} more tries left. \n")
                else:
                    User.users[userid]["accountLocked"] = True
                    NotificationSystem.lockedUsers.append(userid)
                    raise PermissionError (f"Login Error: User {userid} is locked. Account unlock Alert has been sent to ADMIN.\n")
        except ValueError as e:
            print(e)
        except PermissionError as e:
            print (e)

    @staticmethod
    def list_all_users():
        """Lists all registered users in the system."""
        for user in User.users:
            print(f'UserID: {user} | Name: {User.users[user]["name"]} | Admin: {User.users[user]["adminRole"]} | Membership: {User.users[user]["memberStatus"]}')

    @staticmethod
    def change_admin_status (userid, status):
        """Grants or revokes administrative rights for a specified user."""
        try:
            if userid in User.users:
                if status:
                    if User.users[userid]["adminRole"] == True:
                        raise ValueError(f"{userid} is already an Admin.")
                    else:
                        User.users[userid]["adminRole"] = True
                        print(f"{userid} is an Admin now.")
                else:
                    if User.users[userid]["adminRole"] == False:
                        raise ValueError(f"{userid} is already not an Admin.")
                    else:
                        User.users[userid]["adminRole"] = False
                        print(f"{userid} no longer has Admin rights.")
            else:
                raise KeyError (f'Search Error: User {userid} does not exist')
        except ValueError as e:
            print (e)
        except KeyError as e:
            print (e)

    @staticmethod
    def delete_user(userid):
        """Deletes a non-admin user account from the system."""
        try:
            if userid in User.users:
                if not User.users[userid]["adminRole"]:
                    User.users.pop(userid)
                    print (f"User {userid} has been deleted.")
                else:
                    raise PermissionError ("You can't delete Admin users.")
            else:
                raise ValueError (f'Search Error: User {userid} does not exist')
        except ValueError as e:
            print (e)
        except PermissionError as e:
            print (e)

    @staticmethod
    def unlock_user(userid):
        """Unlocks a locked user account and resets login attempts."""
        try:
            if userid in User.users:
                if User.users[userid]["accountLocked"]:
                    User.users[userid]["accountLocked"] = False
                    User.users[userid]["loginAttempts"] = 3
                    NotificationSystem.lockedUsers.remove(userid)
                    print(f"User {userid} has been unlocked.")
                else:
                    raise ValueError(f"User {userid} is already unlocked.")
            else:
                raise ValueError (f'Search Error: User {userid} does not exist')
        except ValueError as e:
            print (e)

    @staticmethod
    def delist_item(item, reason):
        """Removes an item from the active catalogue for policy or moderation reasons."""
        try:
            if item in User.Catalogue:
                User.DelistedCatalogue[item] = User.Catalogue[item]
                NotificationSystem.delistedItems[item] = User.Catalogue[item]
                User.Catalogue.pop(item)
                User.DelistedCatalogue[item]['Reason'] = reason
                NotificationSystem.delistedItems[item]['Reason'] = reason
                print ("[ITEM DELISTED FROM THE CATALOGUE]")
                print(f"[ALERT SENT] | To: Seller - {User.DelistedCatalogue[item]['Seller']}")

            else:
                raise ValueError("Search Error: Item not in Catalogue\n")
        except ValueError as e:
            print (e)

#Main Code
def main():
    """Runs the main command-line interface loop for navigation and user authentication."""
    while True:
        print("Hello! Welcome to Marketplace!\nPlease choose an option\n"
              "1. Create an account\n"
              "2. Buyer Login\n"
              "3. Seller Login\n"
              "4. Admin Login\n"
              "5. Exit\n")
        user_input = input("")
        match user_input:
            case "1":
                print("Please provide your user details for account creation: ")
                user_name = input("Name: ").strip().title()
                user_username = input("Username: ").upper()
                user_password = input("Password: ").strip()
                try:
                    User(user_name, user_username, user_password)
                except ValueError as e:
                    print(e)
            case "2":
                print("Please enter your login details: ")
                buyer_username = input("Username: ").upper()
                buyer_password = input("Password: ")
                buyerator = Buyer.buyer_login(buyer_username, buyer_password)
                if buyerator:
                    print("\nSuccess! You are now logged in")
                    buyer_notifier = NotificationSystem(buyer_username)
                    buyer_notifier.receive_alerts("BUYER")
                    while True:
                        print("\n===BUYER MENU===")
                        print("Choose an option:\n"
                              "1. View Catalogue\n"
                              "2. Search Item\n"
                              "3. Add Item to Cart\n"
                              "4. Remove Item from Cart\n"
                              "5. View Cart\n"
                              "6. Proceed to Checkout\n"
                              "7. Add/Update Payment Method\n"
                              "8. View Saved Payment Info\n"
                              "9. View Purchase History\n"
                              "10. View Buyer Profile\n"
                              "11. Change password\n"
                              "12. Log Out\n")
                        buyer_choice = input("").strip()
                        match buyer_choice:
                            case "1":
                                buyerator.view_catalogue()

                                while True:
                                    print("Do you want to filter Catalogue by price/seller (Y/N):\n")
                                    buyer_choice1 = input("").strip().upper()
                                    match buyer_choice1:
                                        case "Y":
                                            print("Press [ENTER] to skip any filters: ")
                                            buyer_choice1_1 = input("Minimum Price ($) [DEFAULT: 0.00]:  ").strip()
                                            buyer_choice1_2 = input("Maximum Price ($) [DEFAULT: Any]: ").strip()
                                            buyer_choice1_3 = input("Seller ID [DEFAULT: ALL]: ").strip().upper()

                                            if buyer_choice1_1 == "":
                                                buyer_choice1_1 = 0.0

                                            if buyer_choice1_2 == "":
                                                buyer_choice1_2 = float("inf")

                                            if buyer_choice1_3 == "":
                                                buyer_choice1_3 = "ALL"

                                            try:
                                                buyerator.view_catalogue(float(buyer_choice1_1), float(buyer_choice1_2), buyer_choice1_3)
                                            except ValueError:
                                                print("ERROR: Invalid input. Please enter a valid price.\n")

                                        case "N":
                                            break
                                        case _:
                                            print("Please enter a valid choice (Y/N)")
                            case "2":
                                buyer_choice2 = input("Enter Item you are looking for: ").strip().title()
                                buyerator.lookup_item(buyer_choice2)
                            case "3":
                                buyer_choice3 = input("Enter Item you wish to add to cart: ").strip().title()
                                buyerator.add_2_cart(buyer_choice3)
                            case "4":
                                buyer_choice4 = input("Enter Item you wish to remove from cart: ").strip().title()
                                buyerator.remove_item(buyer_choice4)
                            case "5":
                                buyerator.view_cart()
                            case "6":
                                buyerator.make_purchase()
                            case "7":
                                print("Enter Card details: ")
                                buyer_choice7 = input("Card Type (VISA/MASTERCARD/AMEX): ").strip().upper()
                                buyer_choice7_1 = input("Card Number: ").strip()
                                buyer_choice7_2 = input("Expiry Date (YYYY-MM-DD): ").strip()
                                buyer_choice7_3 = input("CVV: ").strip()
                                buyerator.add_payment(buyer_choice7, buyer_choice7_1, buyer_choice7_2, buyer_choice7_3)
                            case "8":
                                buyerator.show_payment_info()
                            case "9":
                                buyerator.view_purchase_history()
                            case "10":
                                buyerator.view_user_info()
                            case "11":
                                buyer_choice11 = input("Enter new password: ").strip()
                                buyerator.set_password(buyer_choice11, buyer_username)
                            case "12":
                                buyerator.empty_cart()
                                buyer_notifier.clear_alerts("BUYER")
                                print(f"{buyer_username} logged out successfully.\n")
                                break
                            case _:
                                print("Please enter valid input (1-12)")
            case "3":
                print("Please enter your login details:")
                seller_username = input("Username: ").upper()
                seller_password = input("Password: ")
                sellerator = Seller.seller_login(seller_username, seller_password)
                if sellerator:
                    print("\nSuccess! You are now logged in")
                    seller_notifier = NotificationSystem(seller_username)
                    seller_notifier.receive_alerts("SELLER")
                    while True:
                        print("\n===SELLER MENU===")
                        print("Choose an option: \n"
                              "1. List New Item for Sale \n"
                              "2. Update Item Price \n"
                              "3. Remove Listed Item \n"
                              "4. View Active Listings \n"
                              "5. View Sold History \n"
                              "6. View Delisted Items\n"
                              "7. Appeal Delisted Item to Admin\n"
                              "8. Change password \n"
                              "9. Log Out \n")
                        seller_choice = input ("")
                        match seller_choice:
                            case "1":
                                seller_choice1 = input("Item Name: ").strip().title()
                                seller_choice1_2 = input("Item Price: ").strip()
                                sellerator.add_item4_sale(seller_choice1, seller_choice1_2)
                            case "2":
                                seller_choice2 = input("Which item is this for: ").strip().title()
                                seller_choice2_2 = input("New Price: ").strip()
                                sellerator.set_price(seller_choice2, seller_choice2_2)
                            case "3":
                                seller_choice3 = input("Which of your items you wish to remove?: ").strip().title()
                                sellerator.delete_item4_sale(seller_choice3)
                            case "4":
                                sellerator.view_inventory()
                            case "5":
                                sellerator.view_sold_items()
                            case "6":
                                sellerator.view_delisted_items()
                            case "7":
                                seller_choice7 = input("Which item is this for: ").strip().title()
                                seller_choice7_2 = input("Send Message (optional): ").strip()
                                sellerator.appeal_delisted_item(seller_choice7, seller_choice7_2)
                            case "8":
                                seller_choice8 = input("Enter new password: ").strip()
                                sellerator.set_password(seller_choice8, seller_username)
                            case "9":
                                print(f"{seller_username} logged out successfully.\n")
                                seller_notifier.clear_alerts("SELLER")
                                break
                            case _:
                                print ("Enter a valid input (1-9)\n")
            case "4":
                print("Please enter your login details:")
                admin_username = input("Username: ").upper()
                admin_password = input("Password: ")
                administrator = Admin.admin_login(admin_username, admin_password)
                if administrator:
                    print("\nSuccess! You are now logged in")
                    admin_notifier = NotificationSystem(admin_username)
                    admin_notifier.receive_alerts("ADMIN")
                    while True:
                        print("\n===ADMIN MENU===")
                        print ("Choose an option:\n"
                               "1. Delist an Item \n"
                               "2. List all users \n"
                               "3. Remove/Grant Admin Role to a user \n"
                               "4. Delete User \n"
                               "5. Reset password for a user \n"
                               "6. Unlock a Locked Account\n"
                               "7. View User Profile \n"
                               "8. Send Alert to a User \n"
                               "9. Clear Admin Alerts\n"
                               "10. Log Out \n")
                        admin_choice = input("")
                        match admin_choice:
                            case "1":
                                admin_choice1 = input("Enter the item you want to delist: ").strip().title()
                                admin_choice1_1 = input("Reason: ").strip()
                                administrator.delist_item(admin_choice1, admin_choice1_1)
                            case "2":
                                administrator.list_all_users()
                            case "3":
                                admin_choice3 = input("Enter the userID to update: ").strip().upper()
                                admin_choice3_1 = input("Select Action (1: Grant Admin | 2: Remove Admin): ").strip()
                                try:
                                    if admin_choice3_1 == "1":
                                        administrator.change_admin_status(admin_choice3, 1)
                                    elif admin_choice3_1 == "2":
                                        administrator.change_admin_status(admin_choice3, 0)
                                    else:
                                        raise ValueError("Enter a valid input (1-2)")
                                except ValueError as e:
                                    print (f'{e}')
                            case "4":
                                admin_choice4 = input("Provide userID of the user you want to delete: ").strip().upper()
                                administrator.delete_user(admin_choice4)
                            case "5":
                                admin_choice5 = input("Enter the userID of the user you want to reset password for (enter your own to change yours): ").strip().upper()
                                admin_choice5_5 = input("Set new password: ").strip()
                                administrator.set_password(admin_choice5_5,admin_choice5)
                            case "6":
                                admin_choice6 = input("Enter the userID you want to unlock: ").strip().upper()
                                administrator.unlock_user(admin_choice6)
                            case "7":
                                administrator.view_user_info()
                            case "8":
                                admin_choice8 = input("Enter the userID you want to send Alerts to: ").strip().upper()
                                admin_choice9 = input(f"Alert message you want to send to user {admin_choice8}: ").strip()
                                admin_notifier.send_alert_2_user(admin_choice8,admin_choice9)
                            case "9":
                                admin_notifier.clear_alerts_4_admin()
                                print("ADMIN ALERTS CLEARED")
                            case "10":
                                print(f"{admin_username} logged out successfully.\n")
                                break
                            case _:
                                print ("Enter a valid input (1-10)\n")
            case "5":
                break
            case _:
                print("Enter a valid input (1-5)\n")


#Executing the program
if __name__ == '__main__':
    main()


