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
		"key": "build",
		"label": "{} Build the emoji library".format(bazel),
		"command": "bazel build //emojis:emojis",
	})
	
	pipeline.add_command_step({
		"key": "test",
		"label": "{} Test the emoji library".format(bazel),
		"command": "bazel test //emojis:test_emojis",
	})

	pipeline.add_command_step({
		"key": "auth",
		"label": "{}".format(buildkite),
		"command": "buildkite-agent oidc request-token --audience 'https://packages.buildkite.com/nunciato/bazel-buildkite-emojis' --lifetime 300"
	})

	pipeline.add_command_step({
		"label": "{}".format(buildkite),
		"commands": [
			"BUILDKITE_REGISTRY_TOKEN=\"$(buildkite-agent oidc request-token --audience 'https://packages.buildkite.com/nunciato/bazel-buildkite-emojis' --lifetime 300)\"",
			"twine upload -u buildkite -p $BUILDKITE_REGISTRY_TOKEN ./bazel-bin/emojis/dist/emojis-0.0.1-py3-none-any.whl"
		],
		"depends_on": [
			"test",
			"build",
			"auth",
		]
	})

	return pipeline.to_json()

print(generate_pipeline())
