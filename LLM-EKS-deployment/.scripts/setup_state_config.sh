#!/bin/bash

# target file's path
STATE_FILE="$WORK_DIR/state.config"

BUCKET="${S3_BUCKET}"
REGION="${AWS_REGION}"
STATE_KEY="terraform/eks-llm/remote-state"

# override values
echo "bucket = \"${BUCKET}\"" > "$STATE_FILE"
echo "key    = \"${STATE_KEY}\"" >> "$STATE_FILE"
echo "region = \"${REGION}\"" >> "$STATE_FILE"

echo "Terraform state.config updated:"
cat "$STATE_FILE"