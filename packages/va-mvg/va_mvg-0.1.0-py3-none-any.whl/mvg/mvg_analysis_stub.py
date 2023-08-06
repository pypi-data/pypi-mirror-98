# fmt: off
# pylint:disable=C0103
"""
MVG analysis stub
provides stub analysis functions
for developing jupyter NB.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

from mvg.mvg import MVG


logger = logging.getLogger(__name__)

VALID_TOKEN = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2MTA0NTY3NTQsImV4cCI6MTg5MzQ1NjAw"
    "MCwiY2xpZW50X2lkIjoiYXBmZWwiLCJzaXRlX2lkIjoic3RydWRlbCJ9.m7LYLLbTW0voLzEOTYY8nf5d"
    "Kl_XPp2c5YOyF_66M6mnPICdqBVzF2JcaN7hUlQEWBzxysma5tw6QfU1NspwPeDGT87_sZKAWWqnBmgjP"
    "7OYUNYvt1fg-o5lylsHSriradI6SBJv0vcHYU3y_Mey_OmV9Vu12OnQWRBam14qqT0"
)

OK_JOB_ID = "0ba47835806e110513fc204e4c94ffe1"


class MVG_analysis_stub(MVG):
    """Subclass with stubbed analysis calls for jupyter development"""

    def __init__(self, endpoint: str, token: str):
        """
        Constructor

        Parameters
        ----------
        endpoint : str
            the server address (URL), string

        token : str
            not used

        """
        super().__init__(endpoint, VALID_TOKEN)

    # Analysis
    def request_analysis(
        self,
        sid: str,
        feature: str,
        parameters: dict = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
    ):
        """Request an analysis on the given endpoint with given parameters

        Parameters
        ----------
        sid : str
            source id
        feature : str
            name of feature to run
        parameters : dict
            name value pairs of parameters
        start_timestamp : int
            start of analysis time window [optional]
        end_timestamp : int
            start of analysis time window [optional]

        Returns
        -------
        jobid: analysis identifier

        """
        logger.info(
            f"(STUBBED) Sending analysis {feature} request for source id={sid} "
            f"with params {parameters} "
            f"from {start_timestamp}_to {end_timestamp} "
            f"on endpoint {self.endpoint}"
        )

        # Package info for db to be submitted
        analysis_info = {"source_id": sid, "feature": feature, "params": parameters}

        response = self._request("post", "/analyses/", json=analysis_info)

        return response.json()

    def get_analysis(self, jobid: str):
        """Retrieves an analysis with given jobId
        The format of the result structure depends on the feature.

        Parameters
        ----------
        jobid : str
            job id

        Returns
        -------
        results: dict
            a diticionary with the results in case available.

        """
        logger.info(
            f"(STUBBED) Get analysis with jobid={jobid} on endpoint {self.endpoint}"
        )

        # Build url
        # url = self.endpoint + "/analyses/" + f"{jobid}"

        # send request (do the call)
        # response = requests.get(url, headers=self._get_headers())

        # check status code
        # va_raise_for_status(response)
        job_folder_path = Path(__file__).parent / "stub_data" / jobid
        logger.info(f"(STUBBED) Trying to read from {job_folder_path}")

        # Intialize to empty results
        res = {"success": False, "labels": None}
        # Check for job folder
        if job_folder_path.exists():
            # There is a job folder

            # Output.json
            output_json = Path(job_folder_path) / "output.json"
            if output_json.exists():
                # There is an output.json
                # Maybe if there is none we should raise a
                # correct http error, but that's for the
                # backend to implement
                with output_json.open() as json_file:
                    res["success"] = json.load(json_file)["success"]

            # Labels Table
            # Only read if output.json indicates successful run
            logger.info(".. exists, looking for labels_table.csv")
            labels_tab = Path(job_folder_path) / "labels_table.csv"
            if labels_tab.exists() and res["success"]:
                labels = pd.read_csv(labels_tab)

                def to_epoch(time):
                    milliseconds = (
                        datetime.strptime(
                            time,
                            "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)
                    ).total_seconds() * 1000
                    return int(milliseconds)

                labels["Timestamp"] = labels["Timestamp"].apply(to_epoch)
                labels = labels.drop(columns=["mode_responsibility"])
                res["labels"] = labels.to_dict(orient="list")
        else:
            logger.info("Job does not exist")

        return res
