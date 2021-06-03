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

from kedro.pipeline import Pipeline, node

from .nodes import parse_dns_log, summarize_log


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=parse_dns_log,
                inputs="query_log",
                outputs="query_dataframe",
                name="parse_dns_log",
            ),
            node(
                func=summarize_log,
                inputs="query_dataframe",
                outputs=["summary_dataframe", "unique_qname"],
                name="summarize_log",
            ),
        ]
    )
