# Copyright 2021 Mathias Lechner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Union
import numpy as np


def parse_timeout(timeout: Union[int, float, str]):
    if isinstance(timeout, float) or isinstance(timeout, int):
        return timeout
    if " " in timeout:
        # 5d 1h or 5d 1:0:0 pattern
        parts = timeout.split(" ")
        total_time = 0
        for part in parts:
            total_time += parse_timeout(part)
        return total_time
    elif ":" in timeout:
        # h:m:s or m:s pattern
        parts = timeout.split(":")
        total_time = 0
        for part in parts:
            total_time *= 60
            total_time += int(part)
        return total_time
    elif "d" in timeout:
        timeout = timeout.replace("days", "").replace("day", "").replace("d", "")
        if timeout.strip() == "":
            raise ValueError(
                "Could not parse number of days in timeout-string. Hint: no spaces are allowed between the number and the units, e.g., 3days"
            )
        return int(timeout) * 60 * 60 * 24
    elif "h" in timeout:
        timeout = timeout.replace("hours", "").replace("hour", "").replace("h", "")
        if timeout.strip() == "":
            raise ValueError(
                "Could not parse number of hours in timeout-string. Hint: no spaces are allowed between the number and the units, e.g., 12h"
            )
        return int(timeout) * 60 * 60
    elif "m" in timeout:
        # TODO: maybe just get rid of the non-digit characters
        timeout = (
            timeout.replace("minutes", "")
            .replace("minute", "")
            .replace("mins", "")
            .replace("min", "")
            .replace("m", "")
        )
        if timeout.strip() == "":
            raise ValueError(
                "Could not parse number of minutes in timeout-string. Hint: no spaces are allowed between the number and the units, e.g., 60min"
            )
        return int(timeout) * 60
    else:
        # TODO: maybe just get rid of the non-digit characters
        timeout = (
            timeout.replace("seconds", "")
            .replace("second", "")
            .replace("secs", "")
            .replace("sec", "")
            .replace("s", "")
        )
        if timeout.strip() == "":
            raise ValueError(
                "Could not parse number of seconds in timeout-string. Hint: no spaces are allowed between the number and the units, e.g., 10s"
            )
        return int(timeout)


def sanitize_bounds(lb, ub):
    if lb is not None and ub is None:
        if np.any(lb <= 0):
            raise ValueError(
                "Cannot register parameter. If only a single bound is provided it is treated as upper bound and the lower bound defaults to 0, but the provided bound is negative. Providing both bounds."
            )
        ub = lb
        lb = 0
    if lb is None and ub is not None:
        if np.any(ub <= 0):
            raise ValueError(
                "Cannot register parameter. If only a single bound is provided it is treated as upper bound and the lower bound defaults to 0, but the provided bound is negative. Providing both bounds."
            )
        lb = 0
    if lb is not None and ub is not None:
        temp = np.minimum(lb, ub)
        ub = np.maximum(lb, ub)
        lb = temp
    return lb, ub


def infer_shape(*args):
    # TODO: If there are multiple np.ndarray the shape should be the largest one while making sure the others are broadcastable
    shape = None
    for v in args:
        if isinstance(v, np.ndarray):
            shape = v.shape
    return shape


def steps_to_pretty_str(steps):
    if steps > 1e6:
        return f"{steps//1e6:0.0f}M"
    if steps > 1e3:
        return f"{steps//1e3:0.0f}k"
    return str(steps)


def time_to_pretty_str(elapsed):
    seconds = elapsed % 60
    elapsed = elapsed // 60
    minutes = elapsed % 60
    elapsed = elapsed // 60
    hours = elapsed % 60
    days = elapsed // 24

    if days == 1:  # 1 day 03:39:01 (h:m:s)
        return f"{elapsed:d} day {hours:02d}:{minutes:02d}:{seconds:02.0f} (h:m:s)"
    elif days > 1:  # 3 days 03:39:01 (h:m:s)
        return f"{elapsed:d} days {hours:02d}:{minutes:02d}:{seconds:02.0f} (h:m:s)"
    elif hours > 0:  # 03:39:01 (h:m:s)
        return f"{hours:02d}:{minutes:02d}:{seconds:02.0f} (h:m:s)"
    elif minutes > 0:  # 39:01 (m:s)
        return f"{minutes:02d}:{seconds:02.0f} (m:s)"
    elif seconds > 20:  # 27s
        return f"{seconds:02.0f} s"
    elif seconds < 1:  # 837ms
        return f"{1000*seconds:0.0f} ms"
    else:  # 9.83s
        return f"{seconds:0.02f} s"


if __name__ == "__main__":

    def print_t(inp):
        # print(f"{str(inp)} -> {parse_timeout(inp)}")
        print(f"assert parse_timeout('{str(inp)}') == {parse_timeout(inp)}")

    print_t(1723)
    print_t(934.0438)
    print_t("1d")
    print_t("1d 2h")
    print_t("2h 60min")
    print_t("1h 30min")
    print_t("1:30")
    print_t("1m 30s")
    print_t("1m 30sec")
    print_t("1min 30sec")
    print_t("1:1:30")
    print_t("1:01:30")
    print_t("1h 1m 30s")