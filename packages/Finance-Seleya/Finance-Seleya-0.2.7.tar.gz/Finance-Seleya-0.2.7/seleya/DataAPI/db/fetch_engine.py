import importlib,pdb
import pandas as pd
from sqlalchemy import create_engine, select, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.engine import reflection

class SQLEngine(object):
    def __init__(self, url):
        self._engine = create_engine(url, echo=False)
        
    def __del__(self):
        conn.dispose()
        
    def sql_engine(self):
        return self._engine
    
class FetchEngine(object):
    def __init__(self, name, url):
        self._name = name
        self._engine = SQLEngine(url)
        print(url)
        self._base = automap_base()
        self._base.prepare(self._engine.sql_engine(), reflect=True)
        self._insp = reflection.Inspector.from_engine(self._engine.sql_engine())
        
    @classmethod
    def create_engine(cls, name):
        if name == 'sly':
            from . sly import sly_engine
            return sly_engine.__getattribute__('FetchSLYEngine')
        
    
    def custom(self, query):
        return pd.read_sql(query, con=self._engine.sql_engine())
    
    def base(self, table, begin_date, end_date, codes, time_name='trade_date', 
             key=None, columns=None, freq=None, dates=None, clause_list=None):
        if dates is not None:
            condition = and_(table.trade_date.in_(dates), table.__dict__[key].in_(codes)
                            ) if clause_list is None else clause_list
        else:
            condition = and_(table.trade_date >= begin_date, table.trade_date <= end_date,
                         table.__dict__[key].in_(codes)) if clause_list is None else clause_list
        cols = [table.__dict__[time_name]]
        if key is not None:
            cols.append(table.__dict__[key])
        if columns is not None:
            for col in columns:
                cols.append(table.__dict__[col])
        else:
            cols = [table]
        if dates is not None:
            query = select(cols).where(condition)
        else:
            query = select(cols).where(condition)
        result = pd.read_sql(query, self._engine.sql_engine())
        return result
    
    def base_notime(self, table, codes=None, key=None, columns=None, freq=None,  clause_list=None):
        if codes is not None:
            condition = and_(table.__dict__[key].in_(codes),
                            table.__dict__['flag'] == 1) if clause_list is None else clause_list
        elif codes is None and clause_list is not None:
            condition = clause_list
        cols = []
        if columns is not None:
            if codes is not None:
                cols.append(table.__dict__[key])
            for col in columns:
                cols.append(table.__dict__[col])
        else:
            cols = [table]
        query = select(cols).where(condition) if key is not None else select(cols)
        result = pd.read_sql(query, self._engine.sql_engine())
        return result
    
    def base_multiple(self, table, clause_list=None, columns=None):
        condition = clause_list
        cols = []
        if columns is not None:
            for col in columns:
                cols.append(table.__dict__[col])
        else:
            cols = [table]
        query = select(cols).where(condition) if clause_list is not None else select(cols)
        result = pd.read_sql(query, self._engine.sql_engine())
        return result
        