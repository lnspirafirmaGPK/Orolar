let token = localStorage.getItem('token');
const API_URL = ""; // Relative path

// Check auth on load
if (token) {
    showChat();
    updateProfile();
}

async function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, full_name: "User" })
        });
        if(res.ok) {
            document.getElementById('authStatus').innerText = "Register success! Please login.";
        } else {
            const data = await res.json();
            document.getElementById('authStatus').innerText = "Error: " + data.detail;
        }
    } catch (e) { console.error(e); }
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        if (res.ok) {
            token = data.access_token;
            localStorage.setItem('token', token);
            showChat();
            updateProfile();
        } else {
            document.getElementById('authStatus').innerText = "Login failed";
        }
    } catch (e) { console.error(e); }
}

function showChat() {
    document.getElementById('authSection').classList.add('hidden');
    document.getElementById('chatSection').classList.remove('hidden');
}

async function updateProfile() {
    const res = await fetch(`${API_URL}/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
        const user = await res.json();
        document.getElementById('userBalance').innerText = `$${user.balance.toFixed(4)}`;
    }
}

async function sendMessage() {
    const msg = document.getElementById('messageInput').value;
    const model = document.getElementById('modelSelect').value;
    const chatBox = document.getElementById('chatBox');

    if (!msg) return;

    // Add User Message
    chatBox.innerHTML += `<div class="mb-2 text-right"><span class="bg-blue-600 p-2 rounded inline-block">${msg}</span></div>`;
    document.getElementById('messageInput').value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const res = await fetch(`${API_URL}/chat/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ message: msg, model: model })
        });

        const data = await res.json();

        if (res.ok) {
            chatBox.innerHTML += `
                <div class="mb-2 text-left">
                    <span class="bg-slate-700 p-2 rounded inline-block border border-purple-500">
                        ${data.text} <br>
                        <span class="text-xs text-gray-400">Cost: $${data.cost.toFixed(4)}</span>
                    </span>
                </div>`;
            updateProfile(); // Update balance
        } else {
            chatBox.innerHTML += `<div class="text-red-500 text-sm">Error: ${data.detail}</div>`;
        }
    } catch (e) {
        chatBox.innerHTML += `<div class="text-red-500 text-sm">Connection Error</div>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}
