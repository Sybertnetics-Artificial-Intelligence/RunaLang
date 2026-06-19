// Properties with get/set accessors
using System;

namespace PropertyTest
{
    public class Account
    {
        // Auto-implemented property
        public string Name { get; set; }

        // Property with backing field
        private decimal balance;
        public decimal Balance
        {
            get { return balance; }
            set
            {
                if (value >= 0)
                    balance = value;
            }
        }

        // Read-only property
        public string AccountNumber { get; }

        // Expression-bodied property
        public bool IsActive => balance > 0;

        public Account(string name, string accountNumber)
        {
            Name = name;
            AccountNumber = accountNumber;
            balance = 0;
        }

        public void Deposit(decimal amount)
        {
            Balance = Balance + amount;
        }
    }
}
