function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function removeToken() {
  localStorage.removeItem("access_token");
}

function isAuthenticated() {
  return !!getToken();
}

async function getCurrentUser() {
  const token = getToken();
  if (!token) return null;
  try {
    const res = await fetch("/api/v1/users/me", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
}

async function logout() {
  const token = getToken();
  try {
    if (token) {
      await fetch("/api/v1/auth/logout", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
    }
  } catch (e) {
  } finally {
    removeToken();
    window.location.href = "/login";
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const logoutBtn = document.getElementById("logout-btn");
  const loginLink = document.getElementById("login-link");
  const registerLink = document.getElementById("register-link");
  const userChip = document.getElementById("user-chip");

  if (logoutBtn) logoutBtn.addEventListener("click", logout);

  const user = await getCurrentUser();
  if (user && user.email) {
    if (userChip) {
      userChip.textContent = user.email;
      userChip.style.display = "inline";
    }
    if (logoutBtn) logoutBtn.style.display = "inline-flex";
    if (loginLink) loginLink.style.display = "none";
    if (registerLink) registerLink.style.display = "none";
  } else {
    if (userChip) userChip.style.display = "none";
    if (logoutBtn) logoutBtn.style.display = "none";
    if (loginLink) loginLink.style.display = "inline-flex";
    if (registerLink) registerLink.style.display = "inline-flex";
  }
});

async function apiGet(path) {
  const token = getToken();
  const res = await fetch(path, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) {
    throw new Error("Ошибка запроса: " + res.status);
  }
  return res.json();
}

async function apiPost(path, body) {
  const token = getToken();
  const res = await fetch(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body || {}),
  });
  if (!res.ok) {
    throw new Error("Ошибка запроса: " + res.status);
  }
  return res.json();
}
