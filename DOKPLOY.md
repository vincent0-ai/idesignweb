# Dokploy Deployment Guide: Idesignweb

This guide walks you through deploying the **Idesignweb** website and member portal onto a [Dokploy](https://dokploy.com/) instance using either **Docker Compose** (recommended: Django + MongoDB all-in-one) or **Application + Managed MongoDB**.

---

## Architecture Overview

- **Web Server**: Django 6.1 served by Gunicorn (WSGI) on port `8000`.
- **Static Assets**: Automatically collected and served with gzip compression and caching headers via **WhiteNoise**.
- **Relational Storage**: SQLite side-store for auth, sessions, and Django admin, mounted to a persistent Docker volume (`/app/data/db.sqlite3`).
- **Document Storage**: MongoDB for services, case studies, deliverables, and tickets.
- **Reverse Proxy & SSL**: Handled automatically by Dokploy's built-in Traefik with automated Let's Encrypt SSL certificates.

---

## Method 1: Deploy with Docker Compose (Recommended)

This method spins up the Django web application and a dedicated MongoDB container together with persistent storage.

### Step 1: Push Code to Git
Ensure your latest changes are pushed to your GitHub or GitLab repository:
```bash
git add .
git commit -m "Configure Dokploy production deployment"
git push origin main
```

### Step 2: Create a Compose Service in Dokploy
1. Log into your Dokploy dashboard.
2. Select your Project (or create a new project named `idesignweb`).
3. Click **Create Service** and select **Compose**.
4. Set Name to `idesignweb-stack`.
5. Under **Source**, choose **GitHub** (or Git Provider) and select your repository and branch (`main`).
6. Compose Path should point to `docker-compose.yml` (default).

### Step 3: Configure Environment Variables
In the Dokploy Compose service, navigate to the **Environment** tab and add the following variables:

```ini
SECRET_KEY=replace-with-a-random-50-character-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_PATH=/app/data/db.sqlite3
GUNICORN_WORKERS=3
```
*(Note: `MONGO_URI` is pre-configured in `docker-compose.yml` to point to `mongodb://mongo:27017/`)*

### Step 4: Map Custom Domain & SSL
1. Go to the **Domains** tab in your Dokploy service.
2. Click **Add Domain**.
3. Set:
   - **Service**: `web`
   - **Port**: `8000`
   - **Host**: `yourdomain.com` (and optionally another for `www.yourdomain.com`)
   - **HTTPS**: Toggle **Enabled** (Automatic Let's Encrypt certificate)
4. Ensure your DNS records (`A` or `CNAME`) point to your Dokploy server IP.

### Step 5: Deploy
1. Click **Deploy**.
2. Monitor the build logs. Dokploy will:
   - Build the Docker image from `Dockerfile`.
   - Start MongoDB with health checks.
   - Run database migrations (`manage.py migrate`).
   - Run initial seed data (`manage.py seed_data`).
   - Run static asset collection (`manage.py collectstatic`).
   - Launch Gunicorn on port `8000`.

---

## Method 2: Deploy as Application (with Dokploy Managed Database)

If you prefer using Dokploy's managed database feature instead of Compose:

### Step 1: Create MongoDB Database in Dokploy
1. In Dokploy, click **Create Service** -> **Database** -> **MongoDB**.
2. Name it `idesignweb-mongo`.
3. Click **Deploy**. Once running, copy the internal connection string:
   `mongodb://<username>:<password>@idesignweb-mongo:27017/?authSource=admin`

### Step 2: Create Application Service
1. Click **Create Service** -> **Application**.
2. Connect your Git repository.
3. Under **Build Type**, select **Dockerfile**.
4. In the **Volumes** tab, add a persistent volume mount:
   - **Host Path**: `idesignweb-data`
   - **Mount Path**: `/app/data`

### Step 3: Add Environment Variables
```ini
SECRET_KEY=replace-with-a-random-50-character-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
MONGO_URI=mongodb://<username>:<password>@idesignweb-mongo:27017/?authSource=admin
MONGO_DB_NAME=idesignweb_db
DATABASE_PATH=/app/data/db.sqlite3
GUNICORN_WORKERS=3
```

### Step 4: Set Domain & Deploy
1. In the **Domains** tab, map port `8000` to your custom domain with HTTPS enabled.
2. Click **Deploy**.

---

## Post-Deployment Operations

### 1. Default Login Credentials
Once deployed, the seed script provisions initial accounts:
- **Staff Administrator**:
  - Username: `admin`
  - Password: `AdminPass2026!`
- **Demo Client**:
  - Username: `client_apex`
  - Password: `MemberPass2026!`

### 2. Changing Admin Password
To change the admin password on the production server:
1. In Dokploy, go to your `web` service and open the **Terminal / Console** tab.
2. Run:
   ```bash
   python manage.py changepassword admin
   ```

### 3. Managing Client Accounts & Projects
- Access Django Admin at: `https://yourdomain.com/admin/`
- Access the Client Portal at: `https://yourdomain.com/login/`
- Manage Inquiries at: `https://yourdomain.com/portal/inquiries/`

---

## Troubleshooting Common Issues

### 1. 403 Forbidden (CSRF verification failed)
- **Cause**: Traefik forwards HTTPS requests, but Django didn't recognize the origin.
- **Fix**: Make sure `CSRF_TRUSTED_ORIGINS` in Dokploy environment variables includes `https://` (e.g. `https://yourdomain.com,https://www.yourdomain.com`).

### 2. Static files (CSS / Images) not showing
- **Fix**: WhiteNoise is pre-configured and runs `collectstatic` on every deployment. Verify that the build logs show `140 static files copied`.

### 3. Preserving User Accounts Across Redeploys
- **Fix**: Verify that the `/app/data` volume is mounted. The SQLite database is stored at `/app/data/db.sqlite3`, preventing data loss when new Docker images are built and deployed.
