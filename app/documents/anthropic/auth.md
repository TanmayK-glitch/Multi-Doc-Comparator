# Claude API Authentication

## Overview

The Claude API supports three authentication methods:

  -----------------------------------------------------------------------
  Authentication method   Credential              Best suited for
  ----------------------- ----------------------- -----------------------
  API key                 Static `sk-ant-api...`  Local development,
                          secret sent as a bearer prototyping, scripts,
                          token in the            and servers where
                          `Authorization` header  secret storage is
                                                  controlled

  Workload Identity       Short-lived bearer      Production workloads on
  Federation (WIF)        token exchanged from an AWS, Google Cloud,
                          identity provider's     Azure, CI/CD, and
                          identity token          Kubernetes when
                                                  eliminating static
                                                  secrets is desired

  App Attest              Short-lived access      iOS and macOS apps
                          token issued to a       distributed to end
                          genuine, attested       users that call the
                          installation of a       Claude API directly
                          registered iOS or macOS without a backend or
                          app                     proxy
  -----------------------------------------------------------------------

### Authentication selection

-   **API keys and Workload Identity Federation provide the same access
    to Claude API endpoints.**
-   Use an **API key** to get started quickly:
    -   Use a **personal key** for your own development.
    -   Use a **service account key** for shared or automated workloads.
-   Prefer **Workload Identity Federation** when the workload already
    has a platform-issued identity that can be federated.
-   Use **App Attest** for iOS and macOS applications distributed to end
    users.

------------------------------------------------------------------------

# API Keys

API keys are static secrets generated in the Claude Console. They are
sent with every API request as a bearer token in the `Authorization`
header.

## API Key Types

When creating an API key, its type determines:

1.  What identity the key acts as.
2.  Where the key works.
3.  When the key stops working.

  ------------------------------------------------------------------------
  Key type          Acts as           Works in          Stops working when
  ----------------- ----------------- ----------------- ------------------
  **Personal key**  The user, with    Either one        The user loses
                    the user's roles  workspace or the  organization
                    and permissions   workspaces where  access or, for a
                                      the user's role   single-workspace
                                      permits API use,  key, loses access
                                      according to the  to that workspace.
                                      scope selected    Personal keys are
                                      during key        archived when the
                                      creation          user is removed
                                                        from the
                                                        organization. If
                                                        re-invited, new
                                                        keys must be
                                                        created; archived
                                                        keys are not
                                                        restored.

  **Service account A service account Either one        The service
  key**                               workspace or any  account is
                                      workspace         archived or, for a
                                      accessible to the single-workspace
                                      service account,  key, is removed
                                      according to the  from that
                                      key's scope.      workspace.
                                      Service accounts  
                                      have access to    
                                      the Default       
                                      Workspace and     
                                      workspaces to     
                                      which they are    
                                      added.            

  **Workspace key   No individual     That workspace    It expires, is
  (legacy)**        identity; it                        disabled or
                    belongs to the                      deleted, or the
                    workspace where                     workspace is
                    it was created                      archived,
                                                        regardless of
                                                        whether the key
                                                        creator leaves the
                                                        organization.
  ------------------------------------------------------------------------

### Identity-backed keys

Personal keys and service account keys are **identity-backed**:

-   A personal key belongs to an existing managed user identity.
-   A service account key belongs to an organization-managed service
    account.
-   Requests made with the key act as that identity.
-   If the identity is removed from the organization, the key stops
    working.
-   This prevents keys from accidentally outliving the people or
    workloads that own them.

**Preferred approach:** use personal keys or service account keys
instead of workspace keys for new integrations.

### Choosing between personal and service account keys

Use a **personal key** for:

-   Your own development.
-   Personal scripts.
-   Tooling that is not intended to represent a shared or unattended
    workload.

Do **not** use one person's personal key as a shared production
credential. A shared personal key acts as that individual and stops
working if the individual leaves the organization.

For shared or automated workloads such as:

-   CI/CD
-   Production services
-   Unattended applications

have an organization administrator create a **service account**, so the
workload has its own identity.

### Workspace keys are legacy

Workspace API keys continue to work, but they should be considered
**legacy**.

Preferred alternatives:

-   Identity-backed personal keys.
-   Identity-backed service account keys.
-   Workload Identity Federation.

Migration guidance is covered in [Replacing workspace API
keys](https://platform.claude.com/docs/en/manage-claude/authentication#replacing-workspace-api-keys).

------------------------------------------------------------------------

# Creating and Using an API Key

## Create a key

Create an API key from **Claude Console → Settings → API keys**:

1.  Click **Create key**.
2.  Name the key.
3.  Choose an expiration.
4.  Set **Linked account**:
    -   Link to yourself for a personal key.
    -   Link to a service account for a key intended to be shared across
        multiple users or used by an automated workload.
5.  Optionally scope the key to a specific workspace.

Scoping a key to a workspace allows future requests to omit the
workspace ID.

## Send the key with HTTP requests

For direct HTTP requests, send the key as a bearer token:

``` http
POST /v1/messages
Authorization: Bearer YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

The legacy header below is also still supported:

``` http
x-api-key: YOUR_API_KEY
```

However, `Authorization: Bearer <key>` is the documented bearer-token
form.

## Use the SDK

The SDK can receive the key explicitly:

``` python
client = Anthropic(api_key="my-anthropic-api-key")
```

Or the SDK can read the `ANTHROPIC_API_KEY` environment variable
automatically:

``` python
client = Anthropic()
```

## API Key Security

API keys are static secrets, so protect them carefully:

-   Store API keys in a **secrets manager**.
-   Rotate keys periodically.
-   Disable or delete a key if it may have leaked.
-   Use key expiration to reduce the lifetime of a leaked credential.

### Disable versus delete

On the Claude Console API keys page:

-   **Disable** is reversible.
    -   The Admin API reports the key's status as `"inactive"`.
    -   Re-enabling returns the status to `"active"`.
-   **Delete** is permanent.
    -   The key is archived.
    -   Archived keys still appear in List API Keys with
        `status: "archived"`.
-   Expired keys can only be deleted.

Expiration reduces the lifetime of a leaked credential, but it **does
not replace proper secret hygiene**.

------------------------------------------------------------------------

# Selecting a Workspace

Workspace behavior depends on whether the API key is scoped to a
workspace.

## Workspace-scoped API key

If an API key was created for a specific workspace:

-   The key only works in that workspace.
-   API requests using the key can omit the workspace ID.

## Multi-workspace or non-workspace-scoped API key

If the API key is **not scoped to a workspace**, every request must
specify the workspace ID using:

``` http
anthropic-workspace-id: WORKSPACE_ID
```

Example using the Python SDK:

``` python
client = Anthropic()  # reads ANTHROPIC_API_KEY

# Required on every request for a multi-workspace key.
# Omit extra_headers for a single-workspace key.
message = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    extra_headers={
        "anthropic-workspace-id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
    },
)
print(message.content)
```

The workspace header can also be configured once for all requests from a
client:

``` python
workspace_client = Anthropic(
    default_headers={
        "anthropic-workspace-id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
    },
)
```

## Finding a workspace ID

A workspace ID can be obtained from:

-   **Claude Console → Settings → Workspaces**, using the **ID** column.
-   The **List Workspaces** endpoint.

The List Workspaces endpoint includes the Default Workspace only when:

``` text
include_default=true
```

The Default Workspace ID is also returned in the
`anthropic-workspace-id` response header for requests that execute in
that workspace.

## Admin API restriction

The Admin API accepts:

-   Personal keys.
-   Service account keys.

But the key must **not be scoped to a specific workspace**.

## Missing workspace header error

If an identity-linked API key is not scoped to a workspace and the
request omits the workspace header, the API returns HTTP **400** with
`invalid_request_error`.

Example:

``` json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "anthropic-workspace-id is required when authenticating with an identity-linked API key; send the id of the workspace this request acts in."
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

## Invalid workspace ID

If the `anthropic-workspace-id` header value is not a valid workspace
ID:

-   HTTP status: **400**
-   Error type: `invalid_request_error`
-   Message:

``` text
anthropic-workspace-id header must be a valid workspace ID.
```

If the workspace does not exist, or the key's user/service account does
not have access to it:

-   HTTP status: **404**
-   Error type: `not_found_error`
-   Message:

``` text
Workspace `<id>` not found.
```

This is the same response used for an unknown workspace.

## Workload Identity Federation workspace selection

Workload Identity Federation selects a workspace during token exchange
rather than through the `anthropic-workspace-id` request header.

------------------------------------------------------------------------

# API Key Expiration

When creating an API key in the Claude Console, an expiration must be
selected from the available options.

## Expiration options

Available choices include:

-   3 hours.
-   1 day.
-   7 days.
-   30 days.
-   Custom duration.
-   **Never**.

`Never` is intended for keys that are stored in a secrets manager and
rotated manually.

### Organization expiration policies

If the organization has a maximum key-expiration policy:

-   The Console limits preset and custom durations to the policy
    maximum.
-   **Never** is unavailable when prohibited by the policy.

Existing keys retain their current behavior.

Important: **expiration is set when the key is created and cannot be
changed afterward.**

The same expiration choice applies when creating an Admin API key from
the Claude Console.

## Expiration warning emails

Anthropic emails the key creator as expiration approaches:

-   **7 days before expiration** for keys with a lifetime of at least 14
    days.
-   **1 day before expiration** for keys with a lifetime of at least 7
    days.
-   Keys with shorter lifetimes expire without a warning email.

## Behavior after expiration

After a key expires:

-   Requests using it return HTTP **401**.
-   The error type is `authentication_error`.
-   The key cannot be reactivated.
-   A new key must be created to restore access.

## Auditing expiration

The Claude Console API keys table displays each key's expiration.

The Admin API exposes the `expires_at` timestamp through:

-   List API Keys.
-   Retrieve API Key.

For keys without an expiration:

``` text
expires_at = null
```

## Expiration is not secret management

Expiration limits how long a leaked credential remains usable, but it is
**not a substitute for secret hygiene**.

Regardless of expiration:

-   Store API keys in a secrets manager.
-   Disable or delete suspected leaked keys.

------------------------------------------------------------------------

# Replacing Workspace API Keys

Workspace API keys should be considered legacy. They can be replaced
with:

-   Workload Identity Federation.
-   Personal API keys.
-   Service account API keys.

These alternatives provide stronger identity handling and observability.

## Recommended migration process

### Step 1: Decide the new key type

Use:

-   **Personal key** for tooling owned and operated by an individual.
-   **Service account key** for shared or unattended workloads.

### Step 2: Create a service account if necessary

For shared workloads, an organization administrator may need to:

1.  Create a service account in **Settings → Service accounts**.
2.  Add the service account to the relevant workspace.

### Step 3: Create the replacement key

Create the new key specifically for the integration's workspace unless
the integration genuinely requires access to multiple workspaces.

### Step 4: Deploy the replacement key

Replace the old workspace key wherever the integration reads it.

Typical locations include:

-   The `ANTHROPIC_API_KEY` environment variable.
-   A secrets manager.

For a multi-workspace key, also configure:

``` http
anthropic-workspace-id: WORKSPACE_ID
```

### Step 5: Verify and delete the old key

After confirming that requests with the replacement key succeed:

1.  Delete the old workspace key.
2.  Verify the integration continues to work.

------------------------------------------------------------------------

# Workload Identity Federation (WIF)

## What WIF is

Workload Identity Federation allows a workload to authenticate using a
**short-lived identity token** issued by an identity provider (IdP) that
the organization already trusts.

Supported identity sources can include:

-   AWS IAM.
-   Google Cloud.
-   Microsoft Azure.
-   GitHub Actions.
-   Kubernetes service accounts.
-   SPIFFE.
-   Microsoft Entra ID.
-   Okta.
-   Other standards-compliant OIDC issuers.

## WIF authentication flow

The high-level flow is:

1.  A workload obtains a JWT from its trusted identity provider.
2.  The workload sends the IdP-issued JWT to Claude's token endpoint:

``` http
POST /v1/oauth/token
```

3.  Claude exchanges the identity token for a **short-lived Claude API
    access token**.
4.  The Claude SDK automatically refreshes the access token before it
    expires.
5.  The workload uses the short-lived Claude access token to access
    Claude API endpoints.

### Key characteristic

With WIF, there is no long-lived:

``` text
sk-ant-api...
```

credential to mint, distribute, or rotate.

## Security advantages

WIF removes long-lived Claude API keys from workload environments.

This can:

-   Reduce the blast radius of a leaked credential.
-   Avoid distributing static Claude secrets.
-   Reuse existing identity-provider controls.
-   Allow access management through the same identity infrastructure
    already used for cloud resources.

## WIF security limitations

WIF does **not automatically guarantee end-to-end security**.

The security of the trust chain depends on:

-   Correct identity-provider configuration.
-   Security of the upstream identity.
-   Security of credentials that can mint identity-provider tokens.

For example, a long-lived static cloud credential that can mint valid
IdP tokens can still undermine the security benefits of federation.

Use WIF together with the identity provider's security controls, such
as:

-   IP allowlists.
-   MFA.
-   Audit logging.
-   Other provider-specific identity and workload controls.

## WIF setup

To configure federation in the Claude Console, create three resources:

1.  A **service account**.
2.  A **federation issuer**.
3.  A **federation rule**.

Then configure the Claude SDK to use the federation rule.

The full setup is covered by the Workload Identity Federation
documentation.

------------------------------------------------------------------------

# App Attest

## What App Attest is

App Attest authenticates **iOS and macOS applications** that call the
Claude API directly from the device.

It is intended for applications distributed to end users where there is:

-   No backend.
-   No proxy between the application and the Claude API.

## App Attest authentication flow

Each application installation proves that it is:

-   A genuine installation.
-   An unmodified build.
-   An installation of an app registered in the Claude Console.

The proof is provided through Apple's **App Attest** service.

Anthropic then issues the device a **short-lived access token**.

## App Attest token properties

App Attest access tokens:

-   Are short-lived.
-   Are scoped to the application's workspace.
-   Expire after **one hour**.
-   Authorize only **Messages API** calls.
-   Bill usage to the application's workspace.

## App Attest registration

To use App Attest:

1.  Register the application in the Claude Console.
2.  Obtain a client ID.
3.  Configure the application to use App Attest.

------------------------------------------------------------------------

# Authentication Decision Guide

  -----------------------------------------------------------------------
  Scenario                            Recommended authentication
  ----------------------------------- -----------------------------------
  Personal development                Personal API key

  Local scripts                       Personal API key

  Prototyping                         Personal API key

  Shared production service           Service account key or WIF

  CI/CD workload                      Workload Identity Federation

  AWS / Google Cloud / Azure workload Workload Identity Federation
  with an existing workload identity  

  Kubernetes workload with a suitable Workload Identity Federation
  identity provider                   

  GitHub Actions workload             Workload Identity Federation

  iOS app calling Claude directly     App Attest

  macOS app calling Claude directly   App Attest

  Legacy workspace API key            Migrate to personal/service-account
  integration                         key or WIF
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Security Principles

## Prefer identity-backed credentials

For new API-key integrations, prefer:

-   Personal keys for individual development.
-   Service account keys for shared or automated workloads.

Avoid using a single person's personal key as a shared production
credential.

## Prefer federation for suitable production workloads

If the workload already has a trusted platform identity, Workload
Identity Federation can eliminate long-lived Claude API keys.

## Treat API keys as secrets

Regardless of expiration:

-   Never expose API keys unnecessarily.
-   Store them in a secrets manager.
-   Rotate them periodically.
-   Disable or delete suspected leaked keys.

## Use expiration as a risk-reduction mechanism

Key expiration limits how long a compromised key can remain useful.

However:

> Key expiration is a risk-reduction control, not a replacement for
> secret management.

## Understand workspace scope

A key's workspace scope affects:

-   Where the key can operate.
-   Whether `anthropic-workspace-id` is required.
-   Whether the key can be used with the Admin API.

For identity-linked keys that are not workspace-scoped, the request must
identify the workspace using:

``` http
anthropic-workspace-id: WORKSPACE_ID
```

------------------------------------------------------------------------

# Important Authentication Errors

  ----------------------------------------------------------------------------
  Condition                              HTTP status Error type / behavior
  --------------------- ---------------------------- -------------------------
  Expired API key                                401 `authentication_error`

  Missing workspace                              400 `invalid_request_error`
  header for an                                      
  identity-linked key                                
  that is not                                        
  workspace-scoped                                   

  Invalid workspace ID                           400 `invalid_request_error`
  format                                             

  Workspace does not                             404 `not_found_error`
  exist or key identity                              
  lacks workspace                                    
  access                                             
  ----------------------------------------------------------------------------

------------------------------------------------------------------------

# Key Terms

## API key

A static secret used to authenticate Claude API requests. It can be
personal, service-account-backed, or legacy workspace-based.

## Personal key

An identity-backed API key that acts as an individual user.

## Service account key

An identity-backed API key that acts as an organization-managed service
account and is intended for shared or automated workloads.

## Workspace key

A legacy API key belonging to a workspace rather than an individual
identity.

## Workload Identity Federation (WIF)

An authentication mechanism that exchanges a trusted identity provider's
short-lived identity token for a short-lived Claude API access token.

## App Attest

An authentication mechanism for registered iOS and macOS applications
that uses Apple's App Attest service to prove that an installation is
genuine and unmodified.

## `ANTHROPIC_API_KEY`

Environment variable used by Claude client SDKs to automatically obtain
the API key.

## `anthropic-workspace-id`

HTTP header used to identify the workspace for an API key that is not
scoped to a single workspace.

## `expires_at`

Admin API field representing an API key's expiration timestamp. It is
`null` when the key has no expiration.

## Identity-backed key

A personal or service account key associated with an
organization-managed identity. Requests using the key act as that
identity, and the key stops working when that identity loses the
relevant organization/workspace access.
