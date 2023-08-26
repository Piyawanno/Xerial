Module xerial.DBSessionPool
===========================

Classes
-------

`DBSessionPool(config)`
:   

    ### Descendants

    * xerial.AsyncDBSessionPool.AsyncDBSessionPool

    ### Static methods

    `browseModel(session, module)`
    :

    `connect(config)`
    :

    `connectRoundRobin(config)`
    :

    ### Methods

    `close(self)`
    :

    `createConnection(self)`
    :

    `getSession(self) ‑> xerial.DBSessionBase.DBSessionBase`
    :

    `reconnectDB(self)`
    :

    `release(self, session)`
    :

    `setSchema(self, schema: str)`
    :