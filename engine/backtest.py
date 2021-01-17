#!/usr/bin/python
# -*- coding: utf-8 -*-

# backtest.py

import datetime
import pprint
import queue
import time

class Backtest(object):
    """
    Encapsulates the settings and components for carring out
    an event-driven backtest.
    """

    def __init__(
        self, csv_dir, symbol_list, initial_capital,
        heartbeat, start_date, data_handler,
        execution_handler, portfolio, strategy
        ):
        """
        Initialized the backtest.

        Parameters:
        csv_dir - The hard root to the CSV data directory.
        symbol_list - The list of symbol strings.
        initial_capital - The starting capaital for the portfolio.
        heartbeat - Backtest "heartbeat" in seconds
        start_date - The start datetime of the strategy.
        data_handler - (Class) Handles the market data feed.
        execution_handler - (Class) Handles the orders/fills for trades.
        portfolio = (Class) Keeps track of portfolio current
            and prior positions.
        strategy - (Class) Generates signals based on market data.
        """
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.initial_capital = initial_capital
        self.heartbeat = heartbeat
        self.start_date = start_date

        self.data_handler_cls = data_handler
        self.execution_handler_cls = executiom_handler
        self.portfolio_cls = portfolio
        self.srategy_cls = strategy

        self.events = queue.Queue()

        self.signals = 0
        self.order = 0
        self.fills = 0
        self.num_strats = 1

        self.generate_trading_instances()

        def _generate_trading_intances(self):
            """
            Generate the trading instance objects from their class types.
            """
            s1 = "Creating DataHandler, Strategy"
            s2 = ", Portfolio and ExecutionHandler"
            s3 = s1 + s2
            print(s3)
            self.daat_handler = self.data_handler_cls(self.events,
                                                      self.csv_dir,
                                                      self.symbol_list)
            self.strategy = self.strategy_cls(self.data_handler,
                                              self.events)
            self.portfolio = self.portfolio_cls(self.data_handler,
                                                self.events.
                                                self.start_date,
                                                self.initial_capital)
            self.execution_handler = self.execution_handler_cls(self.events)
            
        def _run_backtest(self):
            """
            Executes the backtest.
            """
            i = 0
            while True:
                i += 1
                print(i)
                # Update the market bars
                if self.data_handler.continue_backtest == True:
                    self.data_handler.update_bars()
                else:
                    break

                # Handle the events
                while True:
                    try:
                        event = self.events.get(False)
                    except queue.Empty:
                        break
                    else:
                        if event is not None:
                            if event.type == 'MARKET':
                                self.strategy.calculate_signals(event)
                                self.portfolio.update_timeindex(event)

                            elif event.type == 'SIGNAL':
                                self.signals += 1
                                self.portfolio.update_signal(event)

                            elif event.type == 'ORDER':
                                self.orders += 1
                                self.execution_handler.execute_order(event)

                            elif event.type == 'FILL':
                                self.fills += 1
                                self.portfolio.update_fill(event)

                time.sleep(self.heartbeat)

        def _output_performance(self):
            """
            Outputs the strategy performance from the backtest.
            """
            self.portfolio.create_equity_curve_dataframe()

            print("Creating summary stats...")
            stats = self.portfolio.output_summary_stats()

            print("Creating equity curve...")
            print(self.portfolio.equity_curve.tail(10))
            pprint.pprint(stats)

            print("Signals: %s" % self.signals)
            print("Orders: %s" % self.orders)
            print("Fills: %s" % self.fills)

        def simulate_trading(self):
            """
            Simulates the backtest and outputs portfolio performance.
            """
            sle._run_backtest()
            self._output_performace()
            





                
