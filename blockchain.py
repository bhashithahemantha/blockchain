import functools

MINING_REWARD = 10 # reward for miners to add coins to the system

# genesis block
genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions': []
}
blockchain = [genesis_block]
open_transactions = [] # for outstanding transactions
owner = 'bhashi'
participants = {'bhashi'}


def get_last_blockchain_value():
    """ Returns the last blockchain value."""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender = owner, amount = 1.0):
    """ Append new open trnasaction to the blockchain.

        Args:
            sender: sender of the coins
            recipient: recipient of the coins
            amount: amount of coins
    """
    # use dictionary
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False    


def mine_block():
    """ Get open transactions and added to a new block which then added to the blockchain """
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    # reward for mining transaction
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:] # make a copy of open transactions to manipulate list of transactions localy
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Get user inputs. """
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Enter the amount of the transaction: "))
    return (tx_recipient, tx_amount) # returns tuple


def get_user_choice():
    """ Get user choice. """
    return input("Your choice: ")


def print_blockchain_elements():
    """ output individuals in the list/ blockchain. """
    for block in blockchain:
        print("Printing block. ")
        print(block)
    else:
        print('-' * 20)    

 
def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def get_balance(participant):
    # nested list comprehension
    tx_sender = [[tx['amount'] for tx in block['transactions']if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    # reduce list of amount to one number only using reduce()
    # returns tx_sum at the end
    # lambda function will add all the items together tx_sender list, starting from first one / [0]
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    # fetch recieved coin amout of transactionsthat were already in blocks of the blockchain
    # we ignore open transactions here because you shuldn't be able to spend coins before the transaction is confirmed 
    tx_recipient = [[tx['amount'] for tx in block['transactions']if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # return total balance
    return amount_recieved - amount_sent

def verify_chain():
    """ verify the blockchain - matches the stored hash in a given block with the recalculated hash of the previouse block """
    for (index, block) in enumerate(blockchain): # by wrapping a list with enumerate gives a tuple like (index, element)
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True   

# check the transaction is valid or not
def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


waiting_for_input = True

# use while loop to get user input sevaral times
while waiting_for_input:
    print("Your choice? ")
    print("1: Add a new transaction value. ")
    print("2: Mine a new block. ")
    print("3: Display the blockchain values. ")
    print("4: Display the participants. ")
    print("h: Manipulate the chain. ")
    print("q: Quit. ")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        # unpack data from the tuple to the function. 1st_ele -> 1st variable
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('transaction added!')
        else:
            print('transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block(): # if all the open blocks are mined, set open_transactions to []
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)    
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                    'previous_hash': '',
                    'index': 0,
                    'transactions': [{'sender': 'A', 'recipient': 'B', 'amount': 100}]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("enter a choice from the list. ")
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain')
        # breakout of the loop
        break
    print('Balance of {}: {:6.2f}.'.format('bhashi',get_balance('bhashi')))    
else:
    print('User left!')


print("Done!")
