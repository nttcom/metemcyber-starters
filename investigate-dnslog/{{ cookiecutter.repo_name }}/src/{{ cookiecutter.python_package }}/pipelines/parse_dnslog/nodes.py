#
#    Copyright 2021, NTT Communications Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import logging
import datetime
import pandas as pd
from typing import Dict, List

log = logging.getLogger(__name__)


def parse_dns_log(logfile: str) -> pd.DataFrame:
    """parse dns query log and store pandas dataframe
    """
    # create data list to append dataframe
    timestamp_list: List[datetime.datetime] = []
    client_list: List[str] = []
    qname_list: List[str] = []
    for query in logfile.splitlines():
        query_list = query.split()
        time_str = f"{query_list[0]} {query_list[1]}"
        timestamp_list.append(
            datetime.datetime.strptime(
                time_str, '%d-%b-%Y %H:%M:%S.%f'))
        client_list.append(query_list[3].split('#')[0])
        qname_list.append(query_list[4].rstrip('):').lstrip('('))

    # Create dns log dataframe
    df_dns = pd.DataFrame(
        data={'timestamp': timestamp_list, 'client': client_list, 'qname': qname_list},
        columns=['timestamp', 'client', 'qname'])

    return df_dns


def summarize_log(df_dns: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """parse dns query log and store pandas dataframe
    """
    # create data list to append dataframe
    df_summary = df_dns.groupby(['client', 'qname']).size(
    ).sort_values(ascending=False).reset_index(name='size')

    df_unique_qname = df_summary.qname.drop_duplicates()
    return df_summary, df_unique_qname
