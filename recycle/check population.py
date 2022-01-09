# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 16:22:36 2021

@author: ruili
"""

import sqlite3
import pandas as pd

conn = sqlite3.Connection(r"C:\test_codes_delete_later\db_test\db_test.db")
query = 'SELECT agentid FROM s0 WHERE vulnerable = 1'
df = pd.read_sql_query(query, conn)
vulnerable_agent = df.drop_duplicates()
agents_query = f"SELECT agents.agentid, AbmPerson.* FROM agents \
        INNER JOIN AbmPerson ON (AbmPerson.hhid = agents.hhid) \
        AND (AbmPerson.pnum = agents.pnum) \
        WHERE agents.agentid IN {tuple(vulnerable_agent.agentid)}"

vul_agents_detail = pd.read_sql_query(agents_query, conn)
agents_detail = pd.read_sql_query("SELECT agents.agentid, AbmPerson.* FROM agents \
        INNER JOIN AbmPerson ON (AbmPerson.hhid = agents.hhid) \
        AND (AbmPerson.pnum = agents.pnum)", conn)
conn.close()
vul_agents_detail_temp = vul_agents_detail.groupby('age').agg({'persType':'count'}).reset_index()
agents_detail_temp = agents_detail.groupby('age').agg({'persType':'count'}).reset_index()
