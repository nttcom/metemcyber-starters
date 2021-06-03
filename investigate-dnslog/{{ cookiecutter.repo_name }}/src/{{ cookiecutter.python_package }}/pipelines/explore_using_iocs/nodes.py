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
import pandas as pd
from typing import Dict, List

log = logging.getLogger(__name__)


def isin_iocs(target_domain: str, ioc_domains: List[str]):
    # If target_domain equals ioc_domains or subdomain of ioc domains, return true
    return any([target_domain == ioc or target_domain.endswith(
        f".{ioc}") for ioc in ioc_domains])


def extract_suspicious_log(
        df_qname: pd.DataFrame,
        ioc_qname: str) -> Dict[str, pd.DataFrame]:
    """Search iocs from dnslog
    """
    iocs_list = ioc_qname.splitlines()
    df_matched = df_qname[df_qname['qname'].apply(
        lambda x: isin_iocs(x, iocs_list)
    )]

    discoverd_qname = df_matched['qname'].drop_duplicates()
    return df_matched, discoverd_qname
