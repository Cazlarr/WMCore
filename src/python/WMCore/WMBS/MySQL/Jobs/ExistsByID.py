#!/usr/bin/env python
"""
_ExistsByID_

MySQL implementation of Jobs.ExistsByID
"""

__all__ = []
__revision__ = "$Id: ExistsByID.py,v 1.2 2009/01/11 17:44:41 sfoulkes Exp $"
__version__ = "$Revision: 1.2 $"

from WMCore.Database.DBFormatter import DBFormatter

class ExistsByID(DBFormatter):
    sql = "SELECT id FROM wmbs_job WHERE id = :id"
    
    def format(self, result):
        result = DBFormatter.format(self, result)

        if len(result) == 0:
            return False
        else:
            return result[0][0]
    
    def getBinds(self, id):
        return self.dbi.buildbinds(self.dbi.makelist(id), "id")
        
    def execute(self, id, conn = None, transaction = False):
        result = self.dbi.processData(self.sql, self.getBinds(id),
                                      conn = conn, transaction = transaction)
        return self.format(result)
