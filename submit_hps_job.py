import json
import os
import requests
import time

api_token = os.environ["RESCALE_API_KEY"]
api_token_in_header = "Token " + api_token
platform = os.environ["RESCALE_PLATFORM"]

input_filename = "input.txt"
storage_config_filename  = "storage_config.json"
first_job_config_filename  = "first_job_config.json"
second_job_config_filename = "second_job_config.json"

# Check available regions for the high performance storage
print("# Checking available regions for the High Performance Storage")
url = "https://" + platform + "/api/v2/storage-devices/available-regions/"
raw_reply = requests.get(
  url,
  headers={'Authorization': api_token_in_header}
)
available_regions = json.loads(raw_reply.text)
print("- High Performance Storage will be launched in " + available_regions[0]["name"])

# Read storage configuration
print("# Reading storage configuration")
with open(storage_config_filename) as f:
  storage_config = json.load(f)

# Modify strage configuration
print("# Modifying strage configuration")
storage_config["region"]["id"] = available_regions[0]["id"]

# Create a storage device
print("# Creating a storage device")
url = "https://" + platform + "/api/v2/storage-devices/"
raw_reply = requests.post(
  url,
  headers={'Authorization': api_token_in_header},
  json=storage_config
)
created_storage = json.loads(raw_reply.text)
print("## Created Storage Device")
print("- Storage ID: " + created_storage["id"])
print("- Storage Name: " + created_storage["name"])

# Submit the storage device
print("# Submitting the storage device")
url = "https://" + platform + "/api/v2/storage-devices/" + created_storage["id"] + "/submit/"
requests.post(
  url,
  headers={'Authorization': api_token_in_header}
)

# Poll the storage status until it become available
print("# Launching the storage device")
while True:
  time.sleep(5)

  raw_reply = requests.get(
    "https://" + platform + "/api/v2/storage-devices/" + created_storage["id"] + "/statuses/",
    headers={'Authorization': api_token_in_header}
  )
  storage_status = json.loads(raw_reply.text)["results"][0]["status"]

  if storage_status == "Started":
    break

# Upload an input file
print("# Uploading an input file")
url = "https://" + platform + "/api/v2/files/contents/"
raw_reply = requests.post(
  url,
  headers={'Authorization': api_token_in_header},
  files={"file": open(input_filename, "rb")}
)
uploaded_input_file = json.loads(raw_reply.text)
print("- " + uploaded_input_file["name"] + " have been uploaded as File ID " + uploaded_input_file["id"])

# Read first job configuration
print("# Reading first job configuration")
with open(first_job_config_filename) as f:
  first_job_config = json.load(f)

# Modify job configuration
print("# Modifying job configuration")
first_job_config["jobanalyses"][0]["inputFiles"] = [{"id": uploaded_input_file["id"]}]
first_job_config["jobanalyses"][0]["command"] = "cp {inputFilename} output.txt\necho \"Hello from first job\" >> output.txt\necho \"Done!!\"".format(inputFilename=input_filename)

# Create first job
print("# Creating a job")
url = "https://" + platform + "/api/v2/jobs/"
raw_reply = requests.post(
  url,
  headers={'Authorization': api_token_in_header},
  json=first_job_config
)
created_first_job = json.loads(raw_reply.text)
print("## Created first job")
print("- Job ID: " + created_first_job["id"])
print("- Job Name: " + created_first_job["name"])

# Attach a storage device to the first job
print("# Attaching a storage device")
url = "https://" + platform + "/api/v2/jobs/" + created_first_job["id"] + "/storage-devices/"
requests.post(
  url,
  headers={'Authorization': api_token_in_header},
  json={"storageDevice":{"id":created_storage["id"]}}
)

# Submit the first job
print("# Submitting the first job")
url = "https://" + platform + "/api/v2/jobs/" + created_first_job["id"] + "/submit/"
requests.post(
  url,
  headers={'Authorization': api_token_in_header}
)

# Poll the first job status until it is completed
print("# The first job is running")
while True:
  time.sleep(5)

  raw_reply = requests.get(
    "https://" + platform + "/api/v2/jobs/" + created_first_job["id"] + "/statuses/",
    headers={'Authorization': api_token_in_header}
  )
  first_job_status = json.loads(raw_reply.text)["results"][0]["status"]

  if first_job_status == "Completed":
    break

# Read second job configuration
print("# Reading second job configuration")
with open(second_job_config_filename) as f:
  second_job_config = json.load(f)

# Modify job configuration
print("# Modifying job configuration")
second_job_config["jobanalyses"][0]["command"] = "cp ~/storage_{storageDeviceId}/jobs/{firstJobId}/run/1/output.txt input.txt\ncp input.txt output.txt\necho \"Hello from second Job\" >> output.txt\necho \"Done!!\"".format(
  storageDeviceId=created_storage["id"],
  firstJobId=created_first_job["id"]
)

# Create second job
print("# Creating a job")
url = "https://" + platform + "/api/v2/jobs/"
raw_reply = requests.post(
  url,
  headers={'Authorization': api_token_in_header},
  json=second_job_config
)
created_second_job = json.loads(raw_reply.text)
print("## Created second job")
print("- Job ID: " + created_second_job["id"])
print("- Job Name: " + created_second_job["name"])

# Attach a storage device to the second job
print("# Attaching a storage device")
url = "https://" + platform + "/api/v2/jobs/" + created_second_job["id"] + "/storage-devices/"
requests.post(
  url,
  headers={'Authorization': api_token_in_header},
  json={"storageDevice":{"id":created_storage["id"]}}
)

# Submit the second job
print("# Submitting the second job")
url = "https://" + platform + "/api/v2/jobs/" + created_second_job["id"] + "/submit/"
requests.post(
  url,
  headers={'Authorization': api_token_in_header}
)

# Poll the second job status until it is completed
print("# The second job is running")
while True:
  time.sleep(5)

  raw_reply = requests.get(
    "https://" + platform + "/api/v2/jobs/" + created_second_job["id"] + "/statuses/",
    headers={'Authorization': api_token_in_header}
  )
  second_job_status = json.loads(raw_reply.text)["results"][0]["status"]

  if second_job_status == "Completed":
    break

# Terminate a storage device
print("# Terminating a storage device")
url = "https://" + platform + "/api/v2/storage-devices/" + created_storage["id"] + "/shutdown/"
requests.post(
  url,
  headers={'Authorization': api_token_in_header}
)
