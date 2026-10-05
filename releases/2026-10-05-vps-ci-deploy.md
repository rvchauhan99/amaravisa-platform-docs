# 2026-10-05 — CI deploy targets VPS

## Summary

GitHub Actions no longer deploys the Passage API to Cloud Run. Push to `main` builds and recreates `amaravisa-api` on the AmaraVisa VPS behind `https://api.amaravisa.com`.

## Why

Cloud Run / Artifact Registry CI failed with GCP `BILLING_DISABLED`. Production already runs on the VPS.

## What changed

- Removed `.github/workflows/deploy-cloudrun.yml`
- Added `.github/workflows/deploy-vps.yml` (rsync → `docker build` → recreate container with existing `/root/amaravisa/api.env` → public health check)
- Docs updated for VPS hosting and CI secrets

## Operator notes

- Env and secrets stay on the VPS (`api.env`); CI never overwrites that file
- Manual workflow run: Actions → **Deploy VPS** → Run workflow
- Post-deploy: `curl -sfS https://api.amaravisa.com/api/health`
