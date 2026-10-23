class NotificationSystem:
    """
        Manages notifications, alerts, and communication logs across different user roles
        (Admin, Buyer, and Seller) within the marketplace system.
        """
    delistedItems = {}
    soldItems = {}
    lockedUsers = []
    Buyers_Log = {'ADMIN' : ['Platinum', ''],
                  'MANU' : ['Gold', f'[UNLOCK OFFER] Spend ${1000.00:.2f} more this year to upgrade your membership to Platinum.'],
                  'PREET': ['Standard',f'[UNLOCK OFFER] Spend ${1000.00:.2f} more this year to upgrade your membership to Gold.'],
                  'MANRAJ': ['Standard',f'[UNLOCK OFFER] Spend ${1000.00:.2f} more this year to upgrade your membership to Gold.'],
                  'RIPAN': ['Standard', f'[UNLOCK OFFER] Spend ${1000.00:.2f} more this year to upgrade your membership to Gold.']
                  }

    messages = {}
    appealLog = []
    UserList = ['ADMIN', 'MANU', 'PREET', 'RIPAN', 'MANRAJ']

    def __init__(self, user):
        self.user = user
        self.sellerLog = []
        self.seller_alerts_2_pop = set()
        self.buyerLog = []

    def receive_alerts(self, role):
        """
                Retrieves and prints appropriate notifications depending on the user's role
                ('ADMIN', 'BUYER', or 'SELLER').
        """
        # Handle notifications for the ADMIN role
        if role == 'ADMIN':
            if len(NotificationSystem.lockedUsers) > 0 or len(NotificationSystem.appealLog) > 0:
                print("ADMIN NOTIFICATIONS:")

                # Notify admin of any locked user accounts needing review
                if len(NotificationSystem.lockedUsers) > 0:
                    is_or_are = 'is' if len(NotificationSystem.lockedUsers) == 1 else 'are'
                    user_or_users = 'user' if is_or_are == 'is' else 'users'
                    print(f"- There {is_or_are} {len(NotificationSystem.lockedUsers)} {user_or_users} whose account has been locked. Please review.")
                    print(f"- The {user_or_users} {is_or_are}:")
                    for index,userid in enumerate(NotificationSystem.lockedUsers):
                        print(f' {index+1}. {userid}')
                # Display pending appeals submitted by sellers/users
                if len(NotificationSystem.appealLog) > 0:
                    for appeals in NotificationSystem.appealLog:
                        print(f'- {appeals}')
                    print("- To reply, use 'Send Alert to a User' (Option 8)")

        elif role == 'BUYER':
            #Alert for Buyers
            # Check if user exists in the Buyers_Log configuration dictionary
            if self.user in NotificationSystem.Buyers_Log.keys():
                # If user membership is higher than 'Standard' (e.g., Gold or Platinum)
                if NotificationSystem.Buyers_Log[self.user][0] != 'Standard':
                    self.buyerLog.append(f"[MEMBERSHIP PERKS] Exclusive marketplace discounts are available for your "
                                         f"{NotificationSystem.Buyers_Log[self.user][0]} Membership.")
                    # Add specific upgrade prompt if tier is Gold (encouraging upgrade to Platinum)
                    if NotificationSystem.Buyers_Log[self.user][0] == 'Gold':
                        self.buyerLog.append(NotificationSystem.Buyers_Log[self.user][1])
                # Default upgrade offer message for Standard tier users
                else:
                     self.buyerLog.append(NotificationSystem.Buyers_Log[self.user][1])

                # Print all compiled buyer notifications
                if len(self.buyerLog) > 0:
                    print("\nNOTIFICATIONS:")
                    for log in self.buyerLog:
                        print(log)
            else:
                # Default fallback for new buyers
                NotificationSystem.Buyers_Log[self.user] = ['Standard']
                print("\nNOTIFICATIONS:")
                print(f'[UNLOCK OFFER] Spend ${1000.00:.2f} more this year to upgrade your membership to Gold.')

        #Alert for Sellers
        else:
            # Check for recently sold items belonging to the current user
            for item in NotificationSystem.soldItems:
                if NotificationSystem.soldItems[item]['Seller'] == self.user:
                    self.sellerLog.append(f"[SOLD] {item} listed for ${NotificationSystem.soldItems[item]['Price']:.2f}\n "
                                          f"-> Check 'View Sold History' for details (Option 5)")
                    self.seller_alerts_2_pop.add(item)
            # Check for recently delisted items belonging to the current user
            for item in NotificationSystem.delistedItems:
                if NotificationSystem.delistedItems[item]['Seller'] == self.user:
                    self.sellerLog.append(f"[DELISTED] {item} listed for ${NotificationSystem.delistedItems[item]['Price']:.2f}\n "
                                          f"-> Check 'View Delisted Items' for details (Option 6)\n "
                                          f"-> If you think this is incorrect and need further clarification, "
                                          f"you can contest this using 'Appeal Delisted Item to Admin' (Option 7)")
                    self.seller_alerts_2_pop.add(item)
            # Print accumulated seller notifications
            if len(self.sellerLog) > 0:
                print("\nNOTIFICATIONS:\n")
                for log in self.sellerLog:
                    print(log)
        # Check and display any custom inbox messages directed to the current user
        if self.user in NotificationSystem.messages.keys():
            for message in NotificationSystem.messages[self.user]:
                print(f'[CUSTOM ALERT] : {message}')

    def clear_alerts(self, role):
        if role == 'SELLER':
            """
                            Clears processed seller alerts (sold/delisted items) and inbox messages for the current user.
            """
            for item in self.seller_alerts_2_pop:
                if item in NotificationSystem.soldItems.keys():
                    NotificationSystem.soldItems.pop(item)

            for item in self.seller_alerts_2_pop:
                if item in NotificationSystem.delistedItems.keys():
                    NotificationSystem.delistedItems.pop(item)
            # Reset the instance's seller log and alerts set
            self.sellerLog = {}
            self.seller_alerts_2_pop.clear()

        # Clear custom direct messages for this user if they exist in the dictionary
        if self.user in NotificationSystem.messages.keys():
            NotificationSystem.messages.pop(self.user)

    @staticmethod
    def clear_alerts_4_admin():
        """Static method to clear all locked user accounts and appeal logs for the admin."""
        NotificationSystem.lockedUsers.clear()
        NotificationSystem.appealLog.clear()

    @staticmethod
    def send_alert_2_user(user_receiver, message):
        """
                Static method allowing the system/admin to send a direct custom message to a specified user.
        """
        try:
            if user_receiver in NotificationSystem.UserList:
                if message != '':
                    if user_receiver not in NotificationSystem.messages.keys():
                        NotificationSystem.messages[user_receiver] = [message]
                    else:
                        NotificationSystem.messages[user_receiver].append(message)
                    print(f"[MESSAGE SENT] | To: {user_receiver} | Message: {message}")
                else:
                    raise ValueError ("Error: Can't send empty messages")
            else:
                raise ValueError("Registration Error: User not found")
        except ValueError as e:
            print(e)

    @staticmethod
    def send_alert_2_admin(message):
        """
                Static method for users (such as sellers) to submit an appeal message directly to the admin log.
        """
        NotificationSystem.appealLog.append(message)
        print(f"[APPEAL SENT] | To: ADMIN | Message: {message}")
