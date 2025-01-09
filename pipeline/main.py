from buildkite_sdk import Pipeline
from emojis.emojis import bazel

def generate_pipeline():
	pipeline = Pipeline()

	pipeline.add_command_step({
		"label": "{} Run bazel build //pipeline:all".format(bazel),
		"command": "bazel build //pipeline:main",
	})
	
	pipeline.add_command_step({
		"label": "{} Run Bazel tests".format(bazel),
		"command": "bazel test //pipeline:test_main",
	})

	pipeline.add_command_step({
		"label": "{} Run Bazel build".format(bazel),
		"command": "bazel build //emojis:emojis",
	})
	
	pipeline.add_command_step({
		"label": "{} Run Bazel tests".format(bazel),
		"command": "bazel test //emojis:test_emojis",
	})
	
	return pipeline.to_json()

print(generate_pipeline())
