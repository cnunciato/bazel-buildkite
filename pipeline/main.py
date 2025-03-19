from buildkite_sdk import Pipeline, CommandStep
from emojis.emojis import bazel, buildkite

def generate_pipeline():
	pipeline = Pipeline()

	pipeline.add_agent("queue", "hosted-macos")

	pipeline.add_step(CommandStep(
		label="{} Build the pipeline binary".format(bazel),
		commands=[
			"brew install bazelisk",
			"bazel build //pipeline:main"
		],
	))
	
	pipeline.add_step(CommandStep(
		label="{} Test the pipeline binary".format(bazel),
		commands=[
			"bazel test //pipeline:test_main"
		],
	))

	pipeline.add_step(CommandStep(
		key="build",
		label="{} Build the emoji library".format(bazel),
		commands=[
			"bazel build //emojis:emojis"
		],
	))
	
	pipeline.add_step(CommandStep(
		key="test",
		label="{} Test the emoji library".format(bazel),
		commands=[
			"bazel test //emojis:test_emojis"
		],
	))

	pipeline.add_step(CommandStep(
		label="{} Upload the package".format(buildkite),
		commands=[
			"bazel build //emojis:all",
			"curl -X POST https://api.buildkite.com/v2/packages/organizations/nunciato/registries/bazel-buildkite-emojis/packages " + 
				"-H \"Authorization: Bearer $(buildkite-agent oidc request-token " + 
				"--audience 'https://packages.buildkite.com/nunciato/bazel-buildkite-emojis' " +
				"--lifetime 300)\" " +
				"-F file=@bazel-bin/emojis/dist/emojis-0.0.5-py3-none-any.whl",
		],
		depends_on=[
			"test",
			"build",
		]
	))

	return pipeline.to_json()

print(generate_pipeline())
