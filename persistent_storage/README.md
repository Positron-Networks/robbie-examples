## Persistent Storage
Each Robbie user gets a persistent storage space on the remote machine that they can use for things like dataset storage or model checkpointing across multiple runs.

This directory provides an computer vision example of how to upload and access data sets using persistent storage.

- `cv_example.py` - Example code from https://github.com/huggingface/accelerate/tree/main/examples
- `requirements.txt` - Python dependencies
- `upload_dataset_to_persistent.yaml` - Robbie run configuration to upload the dataset from an internet location to Robbie persistent storage.
- `run_cv_example.yaml` - Robbie run configuration to execute the demo code in the Robbie cloud.

### Background - Directory structure on the remote machine
To better understand how to use Robbie, let's explore the runtime environment when your code starts to run in Robbie. Your code will have access to the following directory structure:
```
/home/job-user
|
|---job-execution
|   |--- file1
|   |--- file2
|   |--- file3
|
|---persistent-disk
```
- `job-execution` directory - contains the files copied from the local machine directory if the `include_local_dir` flag is set to `true`. You can access any of these files during your run. For example you might have one or more .py files that you'd like to execute as part of our job (e.g. `python file1.py`). You might also have small data files like a .csv on your local machine that you'd like to use on the remote machine. Keep in mind, however, that any files produced during your run, or left over after your run, that are stored in `/home/job-user/job-execution` will be automatically uploaded to your run-specific artifacts. As a result, try to avoid storing large files or datasets in `/home/job-user/job-execution`. Files left in `/home/job-user/job-execution` are not available on your next run. 

- `persistent-disk` directory - Contains files that you would like to store across job runs. Use this directory to storate files like checkpoints and datasets.

### Uploading data to persistent storage (`/home/job-user/persistent-disk`)
Currently you just run a robbie job (run) in order to upload data to the persistent disk.

In the example directory there is a job_configure file called `upload.yaml` 
that you can use to load the sample dataset on to the persistent storage.

```
version: 1.1
python_job:
  job_type: BASH_COMMAND_RUNNER
  mode: generic
  funding_group_id: cecfc347-5680-4fb0-ae99-b029941b08dd
  environment_id: 52dbdaa5-eb8e-4a3d-9745-77db52b91b34
  image: auto-select
  include_local_dir: true
  commands:
  - wget https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
  - mkdir ../persistent-disk/cv_example
  - mv ./images.tar.gz ../persistent-disk/cv_example
  - ls ../persistent-disk/cv_example
```

The `commands` are the important thing here.
- Step 1 - `wget https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz`
This download the image dataset into `/home/job-user/job-execution`
- Step 2 - `mkdir ../persistent-disk/cv_example` - Create a directory on the persistent disk to store the image data.
- Step 3 - `mv ./images.tar.gz ../persistent-disk/cv_example` - move the tar file over. Keep it zip for now.
- Step 4 - `ls ../persistent-disk/cv_example` - show the the file was moved.

To execute this steps on robbie, type:
```bash
robbie run --f upload_dataset_to_persistent.yaml --y --tail
``` 
in the same directory as the demo code.

You should noticed that `images.tar.gz` is availabe on the persistent storage.

If you are adventurous you can run the command directly from the command line like this:
```bash
robbie run "wget https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz && mkdir ../persistent-disk/cv_example && mv ./images.tar.gz ../persistent-disk/cv_example & ls ../persistent-disk/cv_example" --y --tail
```

### Running the example
Now that the image data is stored on your robbie persistent disk, you can use it for your training runs.
The computer vision example `cv_example.py` is provided.

To run this example, you'll use the `run_cv_example.yaml` job configuration file:

```
version: 1.1
python_job:
  job_type: BASH_COMMAND_RUNNER
  mode: python
  funding_group_id: cecfc347-5680-4fb0-ae99-b029941b08dd
  environment_id: 16abcbd3-ef81-4720-98d2-0aa7480a10f1
  image: auto-select
  include_local_dir: true
  dependencies: requirements.txt
  commands:
  - cp ../persistent-disk/cv_example/images.tar.gz .
  - tar -xzf images.tar.gz
  - python ./cv_example.py --data_dir ./images
  - rm -rf images
  - rm images.tar.gz
```

The `commands` are the important thing here.
- Step 1 - `cp ../persistent-disk/cv_example/images.tar.gz .` - Copy the previously uploaded dataset into `/home/job-user/job-execution`
- Step 2 - `tar -xzf images.tar.gz` - Extract the invidual image data (.jpg files) into the `images` directory in `/home/job-user/job-execution`
- Step 3 - `python ./cv_example.py --data_dir ./images` - move the tar file over. Keep it zip for now.
- Step 4 - `rm -rf images` - deletes the `images` directory so it will not be uploaded to job artifacts.
- Step 5 - `rm images.tar.gz` - deletes the tar file so it will not be uploaded to job artifacts.

To execute this steps on robbie, type:
```bash
robbie run --f run_cv_example.yaml --y --tail
``` 
in the same directory as the demo code.

