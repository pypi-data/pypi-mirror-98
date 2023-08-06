from sqlalchemy import create_engine
import logging
from .creds import EQUIP_DB_USERNAME, EQUIP_DB_PASSWORD

logger = logging.getLogger(__name__)

class UMnetequip:
    '''
    This class wraps helpful equip db queries in python.
    The API is lame.
    '''
    def __init__(self, host='mallard.dsc.umich.edu', port=1521):

        self._url = f"oracle://{EQUIP_DB_USERNAME}:{EQUIP_DB_PASSWORD}@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))(CONNECT_DATA=(SID=PC13)))"
        self._e = create_engine(self._url)
        
        logger.debug(f"Created DB engine {self._url}")

    def _build_select(self, select, table, joins=[], where=[], order_by=None, limit=None, group_by=None, distinct=False):
        '''
        Generic 'select' query string builder built from standard query components as input.
        The user is required to generate substrings for the more complex inputs
        (eg joins, where statements), this function just puts all the components
        together in the right order with appropriately-added newlines (for debugging purposes)
        and returns the result.

        :select: a list of columns to select
          ex: ["nip.mac", "nip.ip", "n.switch", "n.port"]
        :table: a string representing a table (or comma-separated tables, with our without aliases)
          ex: "node_ip nip"
        :joins: a list of strings representing join statements. Include the actual 'join' part!
          ex: ["join node n on nip.mac = n.mac", "join device d on d.ip = n.switch"]
        :where: A list of 'where' statements without the 'where'. The list of statements are
          "anded". If you need "or", embed it in one of your list items
          ex: ["node_ip.ip = '1.2.3.4'", "node.switch = '10.233.0.5'"]
        :order_by: A string representing a column name (or names) to order by
        :group_by: A string representing a column name (or names) to group by
        :limit: An integer

        '''

        # First part of the sql statement is the 'select'
        distinct = 'distinct ' if distinct else ''
        sql = f"select {distinct}" + ", ".join(select) + "\n"

        # Next is the table
        sql += f"from {table}\n"

        # Now are the joins. The 'join' keyword(s) need to be provided
        # as part of the input, allowing for different join types
        for j in joins:
            sql += f"{j}\n"

        # Next are the filters. They are 'anded'
        sql += "where\n"
        sql += " and\n".join(where) + "\n"

        # Finally the other options
        if order_by:
            sql += f"order by {order_by}\n"

        if group_by:
            sql += f"group by {group_by}\n"

        if limit:
            sql += f"limit {limit}\n"
        
        logger.debug(f"Generated SQL command:\n****\n{sql}\n****\n")

        return sql

    def _execute(self, sql):
        '''
        Generic sqlalchemy "execute this sql command and give me all the results"
        '''
        with self._e.begin() as c:
            r = c.execute(sql)
        return r.fetchall()

    def get_devices_by_category(self, category, active_only=False):
        '''
        Queries equip db for devices by category. You can also
        specify if you only want active devices.
        '''

        select = [ 'eq.monitored_device', 
                   'eq.rancid',
                   'eq.off_line',
                   'eq.dns_name',
                   'eq.ip_address',
                 ]
        table = 'ARADMIN1.MAC_SLA_EQUIPMENT eq'

        where = [f"eq.category = '{category}'"]

        # Equipshim status numbers (see ARADMIN1.UMNET_EQUIPMENT_STATUS)
        # 1: RESERVE, 2:ACTIVE, 3:RETIRED
        if active_only:
            where.append("eq.status = 2")
        
        sql = self._build_select(select, table, where=where, distinct=True)
        return self._execute(sql)
