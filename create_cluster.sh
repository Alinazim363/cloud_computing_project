gcloud container clusters create todolist-cluster \
 --project=cisc-5550 \
 --zone=us-central1-a

gcloud container clusters get-credentials todolist-cluster \
 --project=cisc-5550 \
 --zone=us-central1-a