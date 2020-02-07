# Prompt Papermill

This kicks off execution of a notebook when a run completes. It is an example of
"prompt" data analysis.

This is a sketch developed at JPLS. There is work to be done to generalize it for
wider use.

## What does this do?

* Receives documents forwarded by ``bluesky-0MQ-proxy``
* Examines the Run Start document to determine if it can do anything with it.
  Currently, it looks at the ``plan_name``, but it could grow to be more
  sophisticated in time.
* Invokes [papermill](https://papermill.readthedocs.io/en/latest/) to run a
  notebook that loads that data from this run and generates artifacts (e.g.
  matplotlib figures saved as image files). A copy of this executed notebook is
  saved. It would be easy to adapt this code to execute multiple notebooks with
  different parameters if needed.

## Deployment

This expects `bluesky-0MQ-proxy` is running. DAMA has tools for configuring
this automatically and can provide it upon request.

The Python script that listens for new Runs and starts papermill is placed at:

```
/opt/bluesky_workers/papermill_worker.py
```

It is managed by supervisor using a configuration file at

```
/opt/supervisor/conf.d/papermill-worker.conf
```

Supervisor runs the scripts in a conda environment created like

```
conda create -p /opt/conda_envs/papermill-worker
pip install <requirements>
```

where `<requirements>` are given by `requirements.txt` in this repo.
Additionally, the requirements for the specific notebook must be installed.

The notebook(s) run by papermill are sorted in directories named by the
corresponding plan_name:

```
/opt/bluesky_postprocess/{plan_name}/papermill_templates
```

The results generated are placed in the directory

```
/opt/bluesky_postprocess/{plan_name}/results
```

They will be given names like `<notebook_filename_{uid}.ipynb>`.

The output directory should be changed in the future! No proper storage is
currently available, so this is a temporary solution.

## Common Tasks

### Check on the worker

```
sudo supervisorctl status
```

Pay attention to the uptime shown. If it is very low and the worker was not
recently (intentionally) restated, and may have recently crashed.

### Stop or Restart the worker

```
sudo supervisorctl stop
```

It is not necessary to manually `stop` if you just want to restart.

```
sudo supervisorctl restart
```

### Check the logs

```
tail -n 100 -f /var/log/papermill-worker.stderr.log 
```

### Update the notebook

Copy the working copy (likely in a home directory) to the system location where
the papermill worker looks for it.

```
sudo cp path/to/working/copy /opt/bluesky_postprocess/{plan_name}/papermill_templates/my_notebook.ipynb
```

It is not necessary to restart the worker; the changes will take effect next
time papermill is invoked.
