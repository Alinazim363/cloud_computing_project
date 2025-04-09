gcloud compute firewall-rules create rule-allow-tcp-5001 \
  --project=cisc-5550 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server \
  --allow=tcp:5001
