# Examples

This repo contains a collection of PyTorch examples adapted for usage on the Positron/Robbie platform.
Each example will, by default, run on a Nvidia A10 GPU.

Prerequisites:
- Python 3.10 or greater installed
- pip installed

## Setup

### 1. Create a python virtual environment. 

Navigate to a directory that you would like the environment to live in and run the venv command.

On Windows or Mac enter the following at the command line/shell:
```sh
python -m venv positronpython
```

### 2. Activate your virtual environment

Mac:
```sh
source ./positronpython/bin/activate
```
Windows:
```sh
cd positronpython/Scripts && activate && cd ../../
```

### 3. Install the Positron Python package

This command will install the Robbie Python package on your local machine.
```sh
pip install positron_networks
```

This command will pop up a web browswer anad ask you to signup and enter an email and password.
```sh
positron login
```

### 4. Download the Robbie Examples to your local machine:

[https://github.com/Positron-Networks/robbie-examples](https://github.com/Positron-Networks/robbie-examples)

## 5. Validate your setup by running `getting_started`.

Run the job.

```sh
cd getting_started
positron run-job
```
Take note of the job name (e.g. `occupational_amethyst_sebulba`) then go to Robbie Portal in your browser to monitor the job.

Robbie Portal: [https://beta.positronsupercompute.com](https://beta.positronsupercompute.com)

**NOTE: The is a beta service and the the portal landing page is not fully functional.
Please login (if you are not already, and click the "My Dashboard" button in the upper righthand corner.

<img width="222" alt="image" src="https://github.com/user-attachments/assets/3eff3c03-c949-4e96-9a8b-58fb5ab4c50c">


You can also run with the `--stream-stdout` to see realtime job logs in your command line.

```sh
positron run-job --stream-stdout
```

See available CLI options with `positron run-job --help`.

### 6. Try other examples 

```sh
cd <example>
positron run-job
```

## Customizing your jobs

In each directory, there is a `job_config.yaml` file that contains the parameters to run your job.

Here is a short explanation of each parameters

### 1. `funding_group_id:` - This is how your job is billed. Please do not change this.

| Funding Group Name   | ID                                   |
| -------------------- | ------------------------------------ |
| Test                 | 5e9e3b08-0063-41ac-a782-d4964cfb8960 |


### 2. `environment_id:` (optional) - This is the hardware that is used to run your job.
You can change to any of the environmetns that you have permission to use.

| Environment | ID                                   |
| ----------- | ------------------------------------ |
| CPU Only    | 29cf5d14-7dee-4a76-86fc-5a2971c76d96 |
| A10 GPU     | 733c1c70-a85a-4d1d-8974-28e189649955 |   <--Default for the examples
| T4 GPU      | 836d7c78-f2da-4c8d-b769-a3cbb8d4e2f4 |

### 3. `image:` (optional) - This is the container image that is used for your job.
Postiron automatically chooses a default image.

| Image Name                                       |
| -------------------------------------------------|          
| pytorch-training:2.2.0-cpu-py310-ubuntu20.04-ec2 |
| pytorch-training:2.1.0-cpu-py310-ubuntu20.04-ec2 |
| pytorch-training:1.13.1-cpu-py39-ubuntu20.04-ec2 |

### 4. `max_tokens:` (optional) - Maximum number of tokens your job can consume before Positron automatically stops it.

For example:
```sh
max_tokens: "100"
```

### 5. `max_time:` (optional) - Maximum time your job can run before Positron automatically stops it.

For example:
```sh
max_time: "2:30"
```

### 6. `commands:` One or more shell commands to run on the remote machine in Postiron's cloud.

For example:
```sh
  commands: |
    python main.py
```


