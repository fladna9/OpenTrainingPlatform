import yaml


def ConfigFromYAML(filename="config.yaml"):
    with open(filename) as f:
        return yaml.safe_load(f)


def ConfigToYAML(config, filename="config.yaml"):
    with open(filename, "w") as outputfile:
        return outputfile.write(yaml.dump(config))
