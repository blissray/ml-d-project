SET PROJECT_ID=dl-project-259304
SET ZONE=us-central1-c
SET INSTANCE_NAME=tf-dsme-vm
gcloud compute ssh --project %PROJECT_ID% --zone %ZONE% %INSTANCE_NAME% -- -L 8080:localhost:8080
