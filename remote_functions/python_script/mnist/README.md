# Python Script Execution Using Robbie
To run this example, make sure your `venv` is activated and install the requirements:

```shell
pip install -r requirements.txt
```

Then run the script:
```shell
python robbie_remote_function_pytorch_mnist.py
```

You will see your remote job's output in your console.

The example Python file sets the `tail` and `environment_id` in the `@remote` decorator. The other parameters you can set are:

- `funding_group_id` If you want to use a Funding Group other than your Personal Funding Group, set the id here. Check [My Resources](https://robbie.run/portal/app/my-resources) in the Robbie Portal to see if you have access to Funding Groups. The Funding Group id will be displayed when you select one on this page.
- `image` The [Image](../../../README.md#images) to use for job execution
- `max_tokens` Maximum number of tokens to use for the job
- `max_time` Maximum time to allot for job execution, in hh:mm. For example, `0:30` is 30 minutes.
