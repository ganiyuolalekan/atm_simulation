class ATMTransactionSimulator:

    @staticmethod
    def message_or_value(result):
        return type(result), result

    def transaction(self, amount, customer, operation='transfer', transact_customer=None):
        if amount % 500 != 0:
            return self.message_or_value("The amount specified can't be withdrawn!")
        elif amount > customer.amount:
            return self.message_or_value("Insufficient Funds")
        else:
            if operation == 'transfer':
                transact_customer.amount += amount
                customer.amount -= amount
                customer.save()
            elif operation == 'withdraw' or operation == 'mobile_recharge':
                customer.amount -= amount
                customer.save()
            else:
                return self.message_or_value("")


transaction_api = ATMTransactionSimulator()
