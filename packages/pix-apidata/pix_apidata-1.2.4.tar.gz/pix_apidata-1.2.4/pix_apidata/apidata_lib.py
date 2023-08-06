from signalrcore_async.hub_connection_builder import HubConnectionBuilder
#from signalrcore_async.protocol.msgpack import MessagePackHubProtocol
import logging
from urllib.parse import quote



class ApiData():
    """
    Provides methods and properties to connect, stream and get market data
    """

    def __init__(self):
        self.connection_started = None
        self.connection_stopped = None
        self.on_trade = None
        self.on_best = None
        self.on_refs = None
        self.on_srefs = None

    async def initialize(self, api_token, api_host):
        """
        initialize the api with token for authentication and authorization
        """
        api_token = quote(api_token)
        print(api_token)
        protocol = "http"
        host = api_host
        # host = "localhost:5011"
        hub_url = f"{protocol}://{host}/api/fda/apidata/stream?api_token={api_token}"
        global connection
        connection = HubConnectionBuilder()\
            .with_url(hub_url)\
            .build()
        connection.on_close(self.connection_stopped)
        connection.on_open(self.connection_started)

        try:
            await connection.start()
            print("connection estabilished")

            connection.on("_t", self.on_trade)
            connection.on("t", self.on_trade)
            connection.on("_b", self.on_best)
            connection.on("b", self.on_best)
            connection.on("f", self.on_refs)
            connection.on("_r", self.on_srefs)
            
            
            return "ok"
        except Exception as err:
            print(err)
            return "not_ok"

    def on_connection_started(self, callback):
        self.connection_started = callback

    def on_connection_stopped(self, callback):
        self.connection_stopped = callback

    # region callbacks

    def on_trade_update(self, callback):
        """
        Tick data update.
        Returns apidata_models.Trade as json
        """
        self.on_trade = callback

    def on_best_update(self, callback):
        self.on_best = callback
        
    def on_refs_update(self, callback):
        self.on_refs = callback

    def on_srefs_update(self, callback):
        self.on_srefs = callback

    # endregion
    
    #region stream subscription methods

    async def subscribeTrade(self, syms):
        await connection.invoke("Ticks", [syms])

    async def subscribeBestAndRefs(self, syms):
        await connection.invoke("Others", [syms])

    async def subscribeAll(self, syms):
        await connection.invoke("SubscribeAll", [syms])

    #endregion

    #region eod data -start
    async def get_eod(self, ticker, startDate, endDate):
        """
        @param : ticker , startDate , EndDate
        ticker : BANKNIFTY-1 , NIFTY-1 , TCS
        startDate and endDate : formate : yyyyMMdd eg:20201001

        eg : ['NIFTY-1','20200828', '20200901']
        """
        if((not ticker) or (startDate.isdigit() == False) or (len(startDate) != 8) or (len(endDate) != 8) or (endDate.isdigit() == False)):
            print("not enough arguments")
            return

        ed = await connection.invoke("Eod", [ticker, startDate, endDate])
        return ed

    async def get_eod_contract(self, underlyingTicker, startDate, endDate, contractExpiry):
        """
        @param : ticker , startDate , EndDate , contractExpiry
        underlyingTicker : BANKNIFTY , NIFTY
        startDate and endDate : formate : yyyyMMdd eg:20201001
        contractExpiry : formate : yyyyMMdd eg: 20201126

        eg: ['NIFTY', '20200828', '20200901', '20201029']
        
        """
        
        if((not underlyingTicker) or (startDate.isdigit() == False) or (len(startDate) != 8 ) or (endDate.isdigit() == False) or (len(endDate) != 8) or (contractExpiry.isdigit() == False) or (len(contractExpiry) != 8)):
            print("not enough arguments")
            return

        ed = await connection.invoke("EodContract", [underlyingTicker, startDate, endDate, contractExpiry])
        return ed

    async def get_intra_eod(self, ticker = "" , startDate = "", endDate = "", resolution="5"):
        """
        @param : ticker , startDate , EndDate , resolution
        ticker : BANKNIFTY-1 , NIFTY-1 , TCS
        startDate and endDate : formate : yyyyMMdd eg:20201001
        resolution : time resolution in minutes. default: 5 minutes

        eg : ['NIFTY-1', '20200828', '20200901', '5']
        """
        if((not ticker) or (startDate.isdigit() == False) or (len(startDate) !=8) or (endDate.isdigit() == False) or (len(endDate) != 8) or (not resolution)):
            print("not enough arguments")
            return

        ied = await connection.invoke("IEod", [ticker, startDate, endDate, resolution])
        return ied

    async def get_intra_eod_contract(self , underlyingTicker = "" , startDate = "" , endDate = "" , contractExpiry = "" , resolution = "5"):
        """
        @param : ticker , startDate , EndDate , contractExpiry , resolution

        ticker : BANKNIFTY-1 , NIFTY-1 , TCS
        startDate and endDate : formate : yyyyMMdd eg:20201001
        contractExpiry : formate : yyyyMMdd eg: 20201126
        resolution : time resolution in minutes. default: 5 minutes

        eg:['NIFTY', '20200828', '20200901', '20201029', '5']
        """
        if((not underlyingTicker) or (startDate.isdigit() == False) or (len(startDate) != 8) or (endDate.isdigit() == False) or (len(endDate) != 8) or (not resolution)):
            print("not enough arguments")
            return

        ied = await connection.invoke("IEodContract", [underlyingTicker, startDate, endDate, contractExpiry, resolution])
        return ied

    async def get_back_ticks(self,ticker,lastDateTime):
        
        if((not ticker) or (not lastDateTime)):
            print("not enough arguments")
            return

        ied = await connection.invoke("TicksHistory", [ticker,lastDateTime])
        return ied
        
    # endregion
