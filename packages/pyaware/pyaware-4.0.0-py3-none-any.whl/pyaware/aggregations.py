"""
Aggregations to data
"""
import ruamel.yaml

agg_types = {
    "latest": lambda x: x[max(x)],
    "samples": lambda x: len(x),
    "min": lambda x: min(x.values()),
    "max": lambda x: max(x.values()),
    "sum": lambda x: sum(x.values()),
    "all": lambda x: list(x.items()),
}


def aggregate(data, reference):
    aggregated = []
    keys = set(data).intersection(set(reference))
    for k in keys:
        raw = data[k]
        aggregated.append(
            dict({"name": k}, **{agg: agg_types[agg](raw) for agg in reference[k]})
        )
    return aggregated


def build_from_device_config(path):
    """
    Builds the triggers from a configuration file
    :param path:
    :return:
    """
    with open(path) as f:
        parsed = ruamel.yaml.safe_load(f)
    aggregations = {}
    defaults = parsed.get("default_aggregations", ["latest", "samples"])
    for param, data in parsed["parameters"].items():
        aggs = data.get("aggregations", defaults)
        try:
            data["triggers"]["process"]["send"]
        except:
            continue
        aggregations[param] = [agg for agg in aggs if agg in agg_types]
    return aggregations
