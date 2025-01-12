from buildkite_sdk import Pipeline
from emojis.emojis import bazel, buildkite

def generate_pipeline():
	pipeline = Pipeline()

	pipeline.add_command_step({
		"label": "{} Build the pipeline binary".format(bazel),
		"command": "bazel build //pipeline:main",
	})
	
	pipeline.add_command_step({
		"label": "{} Test the pipeline binary".format(bazel),
		"command": "bazel test //pipeline:test_main",
	})

	pipeline.add_command_step({
		"label": "{} Build the emoji library".format(bazel),
		"command": "bazel build //emojis:emojis",
	})
	
	pipeline.add_command_step({
		"label": "{} Test the emoji library".format(bazel),
		"command": "bazel test //emojis:test_emojis",
	})

	pipeline.add_command_step({
		"label": "{}".format(buildkite),
		"command": "buildkite-agent oidc request-token --audience 'https://packages.buildkite.com/nunciato/bazel-buildkite-emojis' --lifetime 300"
	})

	# pipeline.add_command_step({
	# 	"label": "{}".format(buildkite),
	# 	"command": "buildkite-agent oidc request-token --audience 'https://packages.buildkite.com/nunciato/bazel-buildkite-emojis' --lifetime 300"
	# })

	return pipeline.to_json()

print(generate_pipeline())
