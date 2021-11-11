#!/bin/bash
for file in $GITHUB_WORKSPACE/jobs/*
do
  docker run --rm --pull always --volume "$file:/app/data/device_auths.json" ghcr.io/jackblk/epicgames-freebies-claimer:latest > epic.log
  python webhook_parser.py
  curl -H "Content-Type: application/json" -d@webhook.json $Discord_Webhook
done