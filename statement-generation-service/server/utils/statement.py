def generate_monthly_statement(user_id, month, year):
    '''
    Get user monthly transaction statement (returns dummy response for now) 
    '''
    return {
        'user_id': user_id,
        'month': month,
        'year': year,
        'statement': {
            'total_transaction': 2,
            'monthly_average_balance':
                [
                    {
                        'title': 'Sent 100₹ to dummyuser.',
                        'transaction_type': 'debit',
                        'amount': 100,
                    },
                    {
                        'title': 'Received 36₹ in dividend from Union Bank.',
                        'transaction_type': 'credit',
                        'amount': 36
                    }
                ]
        },
    }
