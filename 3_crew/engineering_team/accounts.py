"""Account management module for a trading simulation platform."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional


# Custom Exceptions

class InvalidTransactionError(Exception):
    """Raised when a precondition for a transaction is violated."""
    pass


class InsufficientFundsError(Exception):
    """Raised when a cash-withdrawing operation would leave the balance negative."""
    pass


class InsufficientSharesError(Exception):
    """Raised when a sell attempts to sell more shares than owned."""
    pass


class InvalidSymbolError(Exception):
    """Raised when get_share_price() is called with an unknown ticker."""
    pass


# Data Structures

class TransactionType(Enum):
    """Enumeration of transaction types."""
    DEPOSIT = auto()
    WITHDRAWAL = auto()
    BUY = auto()
    SELL = auto()


@dataclass(frozen=True)
class Transaction:
    """Represents a single transaction in the account."""
    timestamp: datetime
    transaction_type: TransactionType
    symbol: Optional[str] = None  # Stock ticker (present for BUY/SELL, None for cash ops)
    quantity: Optional[int] = None  # Number of shares (for BUY/SELL)
    price: Optional[float] = None  # Share price at time of trade (for BUY/SELL). None for cash ops.
    amount: float = 0.0  # Cash amount involved (deposit/withdrawal or total trade cost/proceeds)


# Helper Functions

def get_share_price(symbol: str) -> float:
    """
    Return the current market price for a given ticker.
    
    Parameters
    ----------
    symbol : str
        Ticker symbol (e.g. "AAPL").
    
    Returns
    -------
    float
        Price per share.
    
    Raises
    ------
    InvalidSymbolError
        If symbol is not recognized.
    """
    PRICES = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0,
    }
    if symbol not in PRICES:
        raise InvalidSymbolError(f"Unknown symbol: {symbol}")
    return PRICES[symbol]


def create_account(user_id: str, initial_deposit: float = 0.0) -> "Account":
    """
    Factory function to instantiate a new Account.
    
    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    initial_deposit : float, optional
        Cash to fund the account at creation (default 0.0).
    
    Returns
    -------
    Account
        Newly created account object.
    """
    return Account(user_id, initial_deposit)


# Account Class

class Account:
    """
    A trading account that supports cash operations and share trading.
    """
    
    def __init__(self, user_id: str, initial_deposit: float = 0.0) -> None:
        """
        Create a new trading account.
        
        Parameters
        ----------
        user_id : str
            Unique identifier for the account (e.g. username or UUID).
        initial_deposit : float, optional
            Amount of cash to deposit at creation time (default 0.0). If >0,
            a DEPOSIT transaction is recorded.
        """
        self._user_id = user_id
        self._cash_balance = 0.0
        self._holdings: Dict[str, int] = {}
        self._transactions: List[Transaction] = []
        self._net_investment = 0.0
        
        # Record initial deposit as a transaction if provided
        if initial_deposit > 0:
            self.deposit(initial_deposit)
    
    @property
    def cash_balance(self) -> float:
        """Current cash balance (read-only)."""
        return self._cash_balance
    
    @property
    def user_id(self) -> str:
        """Account owner identifier (read-only)."""
        return self._user_id
    
    def deposit(self, amount: float) -> None:
        """
        Add cash to the account.
        
        Parameters
        ----------
        amount : float
            Positive amount to add.
        
        Raises
        ------
        InvalidTransactionError
            If amount <= 0.
        """
        if amount <= 0:
            raise InvalidTransactionError("Deposit amount must be positive.")
        
        self._cash_balance += amount
        self._net_investment += amount
        
        transaction = Transaction(
            timestamp=datetime.utcnow(),
            transaction_type=TransactionType.DEPOSIT,
            amount=amount
        )
        self._transactions.append(transaction)
    
    def withdraw(self, amount: float) -> None:
        """
        Remove cash from the account.
        
        Parameters
        ----------
        amount : float
            Positive amount to withdraw.
        
        Raises
        ------
        InvalidTransactionError
            If amount <= 0.
        InsufficientFundsError
            If cash balance would become negative after withdrawal.
        """
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be positive.")
        
        if self._cash_balance - amount < 0:
            raise InsufficientFundsError(
                f"Insufficient funds. Available: {self._cash_balance}, Requested: {amount}"
            )
        
        self._cash_balance -= amount
        self._net_investment -= amount
        
        transaction = Transaction(
            timestamp=datetime.utcnow(),
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount
        )
        self._transactions.append(transaction)
    
    def buy(self, symbol: str, quantity: int) -> None:
        """
        Purchase shares.
        
        Parameters
        ----------
        symbol : str
            Stock ticker (e.g. "AAPL").
        quantity : int
            Number of shares to buy (must be > 0).
        
        Raises
        ------
        InvalidSymbolError
            If symbol is not recognized by get_share_price().
        InvalidTransactionError
            If quantity <= 0.
        InsufficientFundsError
            If total cost (price * quantity) exceeds cash balance.
        """
        if quantity <= 0:
            raise InvalidTransactionError("Quantity must be positive.")
        
        # Get the current price (may raise InvalidSymbolError)
        price = get_share_price(symbol)
        
        total_cost = price * quantity
        
        if self._cash_balance < total_cost:
            raise InsufficientFundsError(
                f"Insufficient funds. Available: {self._cash_balance}, Cost: {total_cost}"
            )
        
        # Execute the buy
        self._cash_balance -= total_cost
        self._holdings[symbol] = self._holdings.get(symbol, 0) + quantity
        
        transaction = Transaction(
            timestamp=datetime.utcnow(),
            transaction_type=TransactionType.BUY,
            symbol=symbol,
            quantity=quantity,
            price=price,
            amount=total_cost
        )
        self._transactions.append(transaction)
    
    def sell(self, symbol: str, quantity: int) -> None:
        """
        Sell shares.
        
        Parameters
        ----------
        symbol : str
            Stock ticker.
        quantity : int
            Number of shares to sell (must be > 0).
        
        Raises
        ------
        InvalidSymbolError
            If symbol is not recognized.
        InvalidTransactionError
            If quantity <= 0.
        InsufficientSharesError
            If holdings[symbol] < quantity.
        """
        if quantity <= 0:
            raise InvalidTransactionError("Quantity must be positive.")
        
        # Check if we have enough shares
        current_holdings = self._holdings.get(symbol, 0)
        if current_holdings < quantity:
            raise InsufficientSharesError(
                f"Insufficient shares. Owned: {current_holdings}, Requested to sell: {quantity}"
            )
        
        # Get the current price (may raise InvalidSymbolError)
        price = get_share_price(symbol)
        
        proceeds = price * quantity
        
        # Execute the sell
        self._cash_balance += proceeds
        new_holdings = current_holdings - quantity
        if new_holdings > 0:
            self._holdings[symbol] = new_holdings
        else:
            del self._holdings[symbol]
        
        transaction = Transaction(
            timestamp=datetime.utcnow(),
            transaction_type=TransactionType.SELL,
            symbol=symbol,
            quantity=quantity,
            price=price,
            amount=proceeds
        )
        self._transactions.append(transaction)
    
    def get_holdings(self) -> Dict[str, int]:
        """
        Return a copy of the current holdings.
        
        Returns
        -------
        Dict[str, int]
            Mapping from ticker symbols to number of shares owned.
        """
        return dict(self._holdings)
    
    def get_portfolio_value(self) -> float:
        """
        Total value of the account (cash + market value of all holdings).
        
        Returns
        -------
        float
            Cash + sum(holdings[sym] * get_share_price(sym)).
        """
        holdings_value = 0.0
        for symbol, quantity in self._holdings.items():
            price = get_share_price(symbol)
            holdings_value += price * quantity
        
        return self._cash_balance + holdings_value
    
    def get_net_investment(self) -> float:
        """
        Total amount of cash that has been deposited minus total withdrawals.
        
        Returns
        -------
        float
            Sum of all DEPOSIT transactions - sum of all WITHDRAWAL transactions.
        """
        return self._net_investment
    
    def get_profit_loss(self) -> float:
        """
        Profit (or loss) relative to the net cash invested.
        
        Returns
        -------
        float
            get_portfolio_value() - get_net_investment().
            Positive values indicate profit; negative values indicate loss.
        """
        return self.get_portfolio_value() - self.get_net_investment()
    
    def get_transactions(self) -> List[Transaction]:
        """
        Return the complete list of recorded transactions, ordered by time.
        
        Returns
        -------
        List[Transaction]
            Each element is a Transaction dataclass.
        """
        return list(self._transactions)


# Main execution for testing
if __name__ == "__main__":
    # Create a new account with an initial deposit of $10,000
    acc = create_account("trader_001", initial_deposit=10_000.0)
    
    # Deposit additional cash
    acc.deposit(2_000.0)
    
    # Buy 10 shares of AAPL (price = 150.0) -> cost = $1,500
    acc.buy("AAPL", 10)
    
    # Buy 5 shares of TSLA (price = 700.0) -> cost = $3,500
    acc.buy("TSLA", 5)
    
    # Current holdings
    print(acc.get_holdings())           # {'AAPL': 10, 'TSLA': 5}
    
    # Total portfolio value
    print(acc.get_portfolio_value())   # cash (8,500) + AAPL (1,500) + TSLA (3,500) = 13,500
    
    # Profit/Loss relative to net investment
    print(acc.get_profit_loss())       # 13,500 - 12,000 (net deposit) = 1,500 profit
    
    # Sell 2 shares of AAPL (price = 150.0) -> proceeds = $300
    acc.sell("AAPL", 2)
    
    # Check holdings after sale
    print(acc.get_holdings())           # {'AAPL': 8, 'TSLA': 5}
    
    # Attempt to withdraw more than available cash -> raises InsufficientFundsError
    try:
        acc.withdraw(20_000.0)
    except InsufficientFundsError as e:
        print(f"Cannot withdraw: {e}")
    
    # Transaction log
    for txn in acc.get_transactions():
        print(txn)
