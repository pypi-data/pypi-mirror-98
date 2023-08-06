# delphai-ml-utils

## Installation

```bash
pip install delphai-ml-utils
```

## Usage

- **Upload to Azure Blob**

The `delphai-hybrid` cluster allows model training with gpu. This feature allows uploading the trained model from inside the cluster to Azure blobs.

This works by adding a config file to your project `config/ml-config.yml` . 

With this yaml file you can configure to which storage account you want to upload your trained model.

```yaml
cluster: delphai-hybrid
training_dir: model-gpu
model_name: test-model
dest:
  storage_account_secret: azure-storage/connection-string
```

`training_dir` : is the output directory of your trained model (model directory)

`model_name`   : Name your model and with it name the new created azure container to save the model into it (Note if the container name already exists will throw an error)

`storage_account_secret`: Here add the kubernetes secret name that contains the connection string to the storage account. example `azure-storage/conenction-string`

How to use with python:

```python
from ml_utils import upload
# Train Model
model.train_model(train_df, use_cuda=True)
# Upload to Azure blob with delphai-ml-utils
upload.upload_to_azure_blob()
```

- **register gpu**

If your model will serve with gpu, we need to monitor every request that comes to the model so kubernetes removes the deployment once it's not being used.

NOTE: if you don't register the model for gpu, it will be destroyed once deployed

```python
from ml_utils import upload, gpu

# serving function
def foo():
    gpu.monitor()

    #
    # Some Logic
    #

    return bar
```
