from QiDataProcessing.Core.Exchange import Exchange


class FutureExchange(Exchange):
    """
    期货交易所
    """
    def __init__(self):
        super().__init__()
        self.products = []