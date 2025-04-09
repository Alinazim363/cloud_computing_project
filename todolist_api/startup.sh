# Create the VM instance named "todolist" in the project "CISC 5550"
gcloud compute instances create todolist \
  --project="CISC 5550" \
  --machine-type=n1-standard-1 \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --tags=http-server \
  --metadata-from-file startup-script=./startup.sh

# Create a firewall rule to allow TCP traffic on port 5001
gcloud compute firewall-rules create rule-allow-tcp-5001 \
  --project="CISC 5550" \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server \
  --allow=tcp:5001
