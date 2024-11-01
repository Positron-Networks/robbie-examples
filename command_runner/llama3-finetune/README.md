# Prerequisites  
In order to run this example, you will need a [Hugging Face token](https://huggingface.co/settings/tokens), 
access to the [meta-llama models](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct),
access to one of Robbie's Medium GPU environments, and 20 Robbie tokens. 

# How to run the example
In `job_config.yaml`, replace `<your hugging face token>` with your actual token before running the example.

View [My Resources](https://robbie.run/portal/app/my-resources) in the Robbie Portal and copy the `environment_id` of
a Medium GPU environment you have access to. 

Execute the `robbie run` command:  
```shell
robbie run --environment_id=<Medium GPU environment_id>
```
