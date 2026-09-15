# Authentication with OAuth Quickstart

## Overview

The easiest way to authenticate to the Gemini API is by using an API key.

For applications that require stricter access controls, OAuth can be used instead.

This quickstart demonstrates a simplified OAuth authentication approach intended for **testing environments**. For production applications, review Google's authentication and authorization documentation before selecting the appropriate credentials.

---

# Objectives

This quickstart covers:

1. Setting up a Google Cloud project for OAuth.
2. Setting up Application Default Credentials (ADC).
3. Managing OAuth credentials directly in your program instead of using `gcloud auth`.

---

# Prerequisites

You need:

- A Google Cloud project.
- A local installation of the `gcloud` CLI.

---

# Set Up the Cloud Project

## 1. Enable the API

Before using Google APIs, enable the **Google Generative Language API** in your Google Cloud project.

---

## 2. Configure the OAuth Consent Screen

Configure the project's OAuth consent screen and add yourself as a test user.

### Steps

1. Open **Google Cloud Console → Google Auth platform → Overview**.
2. Complete the project configuration form.
3. Set the user type to **External** under the Audience section.
4. Complete the remaining configuration and accept the User Data Policy terms.
5. Click **Create**.
6. For this quickstart, scopes can initially be skipped.
7. Click **Save and Continue**.

### Add Test Users

1. Open the **Audience** page of the Google Auth platform.
2. Under **Test users**, click **Add users**.
3. Add your email address and any other authorized test users.
4. Click **Save**.

> For applications intended for use outside your Google Workspace organization, the required authorization scopes must be added and verified.

---

# 3. Create OAuth Credentials for a Desktop Application

OAuth 2.0 Client IDs identify applications to Google's OAuth servers.

If an application runs on multiple platforms, a separate client ID should be created for each platform.

### Steps

1. Open **Google Cloud Console → Google Auth platform → Clients**.
2. Click **Create Client**.
3. Select **Application type → Desktop app**.
4. Enter a name for the credential.
5. Click **Create**.
6. Google displays the newly created Client ID and Client Secret.
7. Click **OK**.
8. Under **OAuth 2.0 Client IDs**, locate the new credential.
9. Download the JSON credential file.
10. The downloaded file will have a name similar to:

```text
client_secret_<identifier>.json