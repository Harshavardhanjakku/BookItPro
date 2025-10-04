# 🧪 BookItPro - Complete Postman Testing Guide

## 📋 **Table of Contents**
1. [Setup & Prerequisites](#setup--prerequisites)
2. [Authentication Flow Testing](#authentication-flow-testing)
3. [User Registration Testing](#user-registration-testing)
4. [Tenant Registration Testing](#tenant-registration-testing)
5. [Login Testing](#login-testing)
6. [Dashboard Testing](#dashboard-testing)
7. [API Endpoints Testing](#api-endpoints-testing)
8. [Password Reset Testing](#password-reset-testing)
9. [Complete Workflow Testing](#complete-workflow-testing)
10. [Troubleshooting](#troubleshooting)

---

## 🛠️ **Setup & Prerequisites**

### **Required Tools:**
- ✅ **Postman** (Download from: https://www.postman.com/downloads/)
- ✅ **Django Server Running** (`python manage.py runserver`)
- ✅ **PostgreSQL Database** (bookitpro database created)

### **Base URL:**
```
http://127.0.0.1:8000
```

### **Important Notes:**
- 🔐 **CSRF Token Required** for POST requests
- 🍪 **Session Cookies** needed for authenticated requests
- 📝 **Password Validation Disabled** for easy testing
- 🔄 **Redirects Expected** for form submissions

---

## 🔐 **Authentication Flow Testing**

### **Step 1: Get CSRF Token**

#### **Functionality:** Get CSRF token for form submissions
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/register/`
#### **Headers:** None required
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `200 OK`
- **Content Type:** `text/html`
- **Response:** HTML registration form
- **Important:** Look for `csrfmiddlewaretoken` in the response HTML

#### **How to Extract CSRF Token:**
1. Send the GET request
2. In the response, find: `<input type="hidden" name="csrfmiddlewaretoken" value="YOUR_TOKEN_HERE">`
3. Copy the value (e.g., `TUQIXuQf5v9tcOMNWT8FTpXjbrESbwmEVIFhaHAQZHwaKyzJctDoTmoG2GBcGxGH`)

---

## 👤 **User Registration Testing**

### **Step 1: Register Individual User**

#### **Functionality:** Create new user with personal tenant and schema
#### **Method:** `POST`
#### **Endpoint:** `http://127.0.0.1:8000/register/`
#### **Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: YOUR_CSRF_TOKEN_HERE
```
#### **Body (form-data):**
```
csrfmiddlewaretoken: YOUR_CSRF_TOKEN_HERE
email: john.doe@example.com
first_name: John
last_name: Doe
password1: admin
password2: admin
phone: +1234567890
role: attendee
```
#### **Expected Response:**
- **Status Code:** `302 Found` (Redirect)
- **Location Header:** `/login/`
- **Response:** Redirect to login page
- **Success Message:** "Account and personal event space created successfully! Your tenant: John Doe's Events"

#### **What Happens:**
- ✅ Creates user account
- ✅ Creates personal tenant: "John Doe's Events"
- ✅ Creates schema: `tenant_john-doe-events`
- ✅ Makes user admin of their personal tenant
- ✅ Creates all necessary tables in schema

---

## 🏢 **Tenant Registration Testing**

### **Step 1: Register Organization**

#### **Functionality:** Create new organization with admin user and schema
#### **Method:** `POST`
#### **Endpoint:** `http://127.0.0.1:8000/register-tenant/`
#### **Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: YOUR_CSRF_TOKEN_HERE
```
#### **Body (form-data):**
```
csrfmiddlewaretoken: YOUR_CSRF_TOKEN_HERE
name: TechCorp Solutions
slug: techcorp-solutions
description: Leading technology event management company
organizer_email: admin@techcorp.com
organizer_first_name: Jane
organizer_last_name: Smith
organizer_password: admin
```
#### **Expected Response:**
- **Status Code:** `302 Found` (Redirect)
- **Location Header:** `/login/`
- **Response:** Redirect to login page
- **Success Message:** "Organization 'TechCorp Solutions' registered successfully! Admin user created. Schema: tenant_techcorp-solutions"

#### **What Happens:**
- ✅ Creates organization/tenant
- ✅ Creates admin user for organization
- ✅ Creates schema: `tenant_techcorp-solutions`
- ✅ Creates all necessary tables in schema

---

## 🔑 **Login Testing**

### **Step 1: Login with User Credentials**

#### **Functionality:** Authenticate user and create session
#### **Method:** `POST`
#### **Endpoint:** `http://127.0.0.1:8000/login/`
#### **Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: YOUR_CSRF_TOKEN_HERE
```
#### **Body (form-data):**
```
csrfmiddlewaretoken: YOUR_CSRF_TOKEN_HERE
email: john.doe@example.com
password: admin
```
#### **Expected Response:**
- **Status Code:** `302 Found` (Redirect)
- **Location Header:** `/dashboard/`
- **Response:** Redirect to dashboard
- **Cookies:** `sessionid` and `csrftoken` will be set

#### **What Happens:**
- ✅ Authenticates user
- ✅ Creates session
- ✅ Sets tenant context
- ✅ Redirects to dashboard

### **Step 2: Login with Organization Admin**

#### **Functionality:** Authenticate organization admin
#### **Method:** `POST`
#### **Endpoint:** `http://127.0.0.1:8000/login/`
#### **Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: YOUR_CSRF_TOKEN_HERE
```
#### **Body (form-data):**
```
csrfmiddlewaretoken: YOUR_CSRF_TOKEN_HERE
email: admin@techcorp.com
password: admin
```
#### **Expected Response:**
- **Status Code:** `302 Found` (Redirect)
- **Location Header:** `/dashboard/`
- **Response:** Redirect to dashboard
- **Cookies:** `sessionid` and `csrftoken` will be set

---

## 📊 **Dashboard Testing**

### **Step 1: Access User Dashboard**

#### **Functionality:** View user dashboard (requires authentication)
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/dashboard/`
#### **Headers:**
```
Cookie: sessionid=YOUR_SESSION_ID; csrftoken=YOUR_CSRF_TOKEN
```
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `200 OK`
- **Content Type:** `text/html`
- **Response:** HTML dashboard page
- **Content:** User information, tenant info, next steps

#### **What You'll See:**
- ✅ Welcome message with user name
- ✅ Tenant information
- ✅ Role-based dashboard (organizer/attendee)
- ✅ Next steps for development
- ✅ No errors (fixed AttributeError)

### **Step 2: Access Dashboard Without Login**

#### **Functionality:** Test authentication requirement
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/dashboard/`
#### **Headers:** None
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `302 Found` (Redirect)
- **Location Header:** `/login/?next=/dashboard/`
- **Response:** Redirect to login page

---

## 🔌 **API Endpoints Testing**

### **Step 1: List All Tenants**

#### **Functionality:** Get all active tenants with schema information
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/api/list-tenants/`
#### **Headers:** None required
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response:**
```json
{
  "success": true,
  "tenants": [
    {
      "id": 1,
      "name": "TechCorp Events",
      "slug": "techcorp-events",
      "description": "Leading technology event organizer",
      "schema_name": "tenant_techcorp-events",
      "created_at": "2025-10-04T00:11:45.670758+00:00"
    },
    {
      "id": 2,
      "name": "John Doe's Events",
      "slug": "john-doe-events",
      "description": "Personal event space for John Doe",
      "schema_name": "tenant_john-doe-events",
      "created_at": "2025-10-04T20:30:00.000000+00:00"
    }
  ],
  "count": 2
}
```

### **Step 2: Create Schema for Existing Tenant**

#### **Functionality:** Manually create schema for existing tenant
#### **Method:** `POST`
#### **Endpoint:** `http://127.0.0.1:8000/api/create-schema/`
#### **Headers:**
```
Content-Type: application/x-www-form-urlencoded
```
#### **Body (form-data):**
```
tenant_slug: techcorp-events
```
#### **Expected Response:**
- **Status Code:** `200 OK`
- **Content Type:** `application/json`
- **Response:**
```json
{
  "success": true,
  "message": "Successfully created schema: tenant_techcorp-events",
  "schema_name": "tenant_techcorp-events",
  "tenant_name": "TechCorp Events"
}
```

### **Step 3: Create Schema for Non-existent Tenant**

#### **Functionality:** Test error handling for non-existent tenant
#### **Method:** `POST`
#### **Endpoint:** `http://127.0.0.1:8000/api/create-schema/`
#### **Headers:**
```
Content-Type: application/x-www-form-urlencoded
```
#### **Body (form-data):**
```
tenant_slug: non-existent-tenant
```
#### **Expected Response:**
- **Status Code:** `404 Not Found`
- **Content Type:** `application/json`
- **Response:**
```json
{
  "success": false,
  "error": "Tenant with slug \"non-existent-tenant\" does not exist"
}
```

---

## 🔄 **Password Reset Testing**

### **Step 1: Request Password Reset**

#### **Functionality:** Request password reset email
#### **Method:** `POST`
#### **Endpoint:** `http://127.0.0.1:8000/password-reset/`
#### **Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: YOUR_CSRF_TOKEN_HERE
```
#### **Body (form-data):**
```
csrfmiddlewaretoken: YOUR_CSRF_TOKEN_HERE
email: john.doe@example.com
```
#### **Expected Response:**
- **Status Code:** `302 Found` (Redirect)
- **Location Header:** `/password-reset/done/`
- **Response:** Redirect to confirmation page

### **Step 2: Password Reset Done Page**

#### **Functionality:** Confirmation page after reset request
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/password-reset/done/`
#### **Headers:** None
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `200 OK`
- **Content Type:** `text/html`
- **Response:** HTML confirmation page

---

## 🏠 **Home Page Testing**

### **Step 1: Access Home Page**

#### **Functionality:** Display available tenants/organizations
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/`
#### **Headers:** None
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `200 OK`
- **Content Type:** `text/html`
- **Response:** HTML page with list of active tenants
- **Content:** Navigation menu, tenant list, registration links

---

## 👤 **Profile Testing**

### **Step 1: Access User Profile**

#### **Functionality:** View user profile (requires authentication)
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/profile/`
#### **Headers:**
```
Cookie: sessionid=YOUR_SESSION_ID; csrftoken=YOUR_CSRF_TOKEN
```
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `200 OK`
- **Content Type:** `text/html`
- **Response:** HTML profile page
- **Content:** User information, edit form

---

## 🚪 **Logout Testing**

### **Step 1: Logout User**

#### **Functionality:** Log out current user and clear session
#### **Method:** `GET`
#### **Endpoint:** `http://127.0.0.1:8000/logout/`
#### **Headers:**
```
Cookie: sessionid=YOUR_SESSION_ID; csrftoken=YOUR_CSRF_TOKEN
```
#### **Body:** None
#### **Expected Response:**
- **Status Code:** `302 Found` (Redirect)
- **Location Header:** `/`
- **Response:** Redirect to home page
- **Cookies:** Session cleared

---

## 🔄 **Complete Workflow Testing**

### **Scenario 1: Individual User Registration Flow**

#### **Step 1: Get CSRF Token**
```
GET http://127.0.0.1:8000/register/
Extract csrfmiddlewaretoken from response
```

#### **Step 2: Register User**
```
POST http://127.0.0.1:8000/register/
Body: email, first_name, last_name, password1, password2, phone, role
Result: User + Personal Tenant + Schema created
```

#### **Step 3: Login**
```
POST http://127.0.0.1:8000/login/
Body: email, password
Result: Session created, redirect to dashboard
```

#### **Step 4: Access Dashboard**
```
GET http://127.0.0.1:8000/dashboard/
Headers: Cookie with sessionid
Result: Dashboard with user info and next steps
```

#### **Step 5: Verify Schema Creation**
```
GET http://127.0.0.1:8000/api/list-tenants/
Result: Should show new tenant with schema_name
```

### **Scenario 2: Organization Registration Flow**

#### **Step 1: Get CSRF Token**
```
GET http://127.0.0.1:8000/register-tenant/
Extract csrfmiddlewaretoken from response
```

#### **Step 2: Register Organization**
```
POST http://127.0.0.1:8000/register-tenant/
Body: name, slug, description, organizer_email, organizer_first_name, organizer_last_name, organizer_password
Result: Organization + Admin User + Schema created
```

#### **Step 3: Login as Admin**
```
POST http://127.0.0.1:8000/login/
Body: organizer_email, organizer_password
Result: Session created, redirect to dashboard
```

#### **Step 4: Access Admin Dashboard**
```
GET http://127.0.0.1:8000/dashboard/
Headers: Cookie with sessionid
Result: Organizer dashboard with organization info
```

---

## 🛠️ **Postman Collection Setup**

### **Environment Variables:**
Create a Postman environment with these variables:
```
base_url: http://127.0.0.1:8000
csrf_token: (will be set dynamically)
session_id: (will be set dynamically)
user_email: john.doe@example.com
user_password: admin
org_email: admin@techcorp.com
org_password: admin
```

### **Pre-request Scripts:**
For requests that need CSRF token, add this pre-request script:
```javascript
// Get CSRF token from cookies or previous response
if (pm.environment.get("csrf_token")) {
    pm.request.headers.add({
        key: 'X-CSRFToken',
        value: pm.environment.get("csrf_token")
    });
}
```

### **Test Scripts:**
Add test scripts to extract and save tokens:
```javascript
// Extract CSRF token from response
if (pm.response.text().includes('csrfmiddlewaretoken')) {
    const csrfMatch = pm.response.text().match(/name="csrfmiddlewaretoken" value="([^"]+)"/);
    if (csrfMatch) {
        pm.environment.set("csrf_token", csrfMatch[1]);
    }
}

// Extract session ID from cookies
const cookies = pm.cookies.all();
const sessionCookie = cookies.find(cookie => cookie.name === 'sessionid');
if (sessionCookie) {
    pm.environment.set("session_id", sessionCookie.value);
}
```

---

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **1. CSRF Token Missing**
- **Error:** `403 Forbidden` or `CSRF token missing`
- **Solution:** Get CSRF token from GET request first
- **Fix:** Add `X-CSRFToken` header with token value

#### **2. Session Expired**
- **Error:** `302 Redirect` to login page
- **Solution:** Login again to get new session
- **Fix:** Update `sessionid` cookie

#### **3. 404 Not Found**
- **Error:** `404 Not Found`
- **Solution:** Check endpoint URL
- **Fix:** Ensure Django server is running on correct port

#### **4. 500 Internal Server Error**
- **Error:** `500 Internal Server Error`
- **Solution:** Check Django server logs
- **Fix:** Ensure database is properly configured

#### **5. Redirect Loops**
- **Error:** Multiple redirects
- **Solution:** Check authentication status
- **Fix:** Clear cookies and login again

### **Debug Tips:**

#### **1. Check Response Headers:**
- Look for `Set-Cookie` headers
- Check `Location` header for redirects
- Verify `Content-Type` header

#### **2. Check Response Body:**
- Look for error messages in HTML
- Check for success messages
- Verify form data is correct

#### **3. Check Server Logs:**
- Run Django server with `python manage.py runserver`
- Watch console for error messages
- Check database connection

#### **4. Verify Database:**
- Check if schemas are created in PostgreSQL
- Verify tenant records exist
- Check user records

---

## 📊 **Expected Results Summary**

### **✅ Successful Responses:**
- **User Registration:** `302` → `/login/` with success message
- **Tenant Registration:** `302` → `/login/` with success message
- **Login:** `302` → `/dashboard/` with session cookies
- **Dashboard:** `200` with user/tenant info
- **API List Tenants:** `200` with JSON tenant list
- **API Create Schema:** `200` with success message

### **❌ Error Responses:**
- **Unauthorized:** `302` → `/login/`
- **CSRF Missing:** `403 Forbidden`
- **Invalid Tenant:** `404 Not Found`
- **Server Error:** `500 Internal Server Error`

---

## 🎯 **Testing Checklist**

### **✅ Authentication Flow:**
- [ ] Get CSRF token from registration page
- [ ] Register individual user successfully
- [ ] Register organization successfully
- [ ] Login with user credentials
- [ ] Login with organization admin credentials
- [ ] Access dashboard with authentication
- [ ] Logout successfully

### **✅ API Endpoints:**
- [ ] List all tenants
- [ ] Create schema for existing tenant
- [ ] Handle non-existent tenant error
- [ ] Verify schema creation in database

### **✅ Error Handling:**
- [ ] Test unauthorized access
- [ ] Test missing CSRF token
- [ ] Test invalid credentials
- [ ] Test non-existent endpoints

### **✅ Complete Workflows:**
- [ ] Individual user registration flow
- [ ] Organization registration flow
- [ ] Password reset flow
- [ ] Profile access flow

---

## 🚀 **Ready for Production Testing!**

This comprehensive guide covers every endpoint and scenario in your BookItPro system. Follow the steps in order, and you'll be able to test the entire multitenant event booking platform using Postman.

**Key Points to Remember:**
- 🔐 Always get CSRF token first for POST requests
- 🍪 Save session cookies for authenticated requests
- 📝 Password validation is disabled for easy testing
- 🔄 Expect redirects for form submissions
- ✅ All registrations create schemas automatically

Happy Testing! 🎉
