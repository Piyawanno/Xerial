Module xerial.AsyncDBSessionPool
================================

Classes
-------

`AsyncDBSessionPool(config)`
:   

    ### Ancestors (in MRO)

    * xerial.DBSessionPool.DBSessionPool

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

    `getSession(self) ‑> xerial.AsyncDBSessionBase.AsyncDBSessionBase`
    :

    `reconnectDB(self) ‑> xerial.AsyncDBSessionBase.AsyncDBSessionBase`
    :

    `release(self, session)`
    :