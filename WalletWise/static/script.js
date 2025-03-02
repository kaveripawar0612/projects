// Initialize Socket.IO
const socket = io();

// Loading overlay
const loadingOverlay = document.createElement('div');
loadingOverlay.className = 'loading-overlay';
loadingOverlay.innerHTML = `
    <div class="loading-spinner">
        <i class="fas fa-wallet fa-3x"></i>
    </div>
`;
document.body.appendChild(loadingOverlay);

function showLoading() {
    loadingOverlay.classList.add('show');
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
}

// Local Storage Management
const LOCAL_STORAGE_KEYS = {
    TRANSACTIONS: 'rokda_transactions',
    BUDGET: 'rokda_budget',
    USER_NAMES: 'rokda_user_names',
    CURRENT_USER: 'rokda_current_user',
    USER_AVATARS: 'rokda_user_avatars'
};

// Initialize data from localStorage or set defaults
let currentUserId = parseInt(localStorage.getItem(LOCAL_STORAGE_KEYS.CURRENT_USER) || '1');
let userTransactions = {};
let userBudgets = {};
let userNames = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEYS.USER_NAMES) || '{"1":"User 1","2":"User 2","3":"User 3","4":"User 4","5":"User 5"}');
let userAvatars = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEYS.USER_AVATARS) || '{"1":"ninja","2":"astronaut","3":"graduate","4":"secret","5":"doctor"}');

// Load all user data
for (let i = 1; i <= 5; i++) {
    userTransactions[i] = JSON.parse(localStorage.getItem(`${LOCAL_STORAGE_KEYS.TRANSACTIONS}_${i}`) || '[]');
    userBudgets[i] = parseFloat(localStorage.getItem(`${LOCAL_STORAGE_KEYS.BUDGET}_${i}`) || '0');
}

const AVATARS = [
    'ninja', 'astronaut', 'graduate', 'secret', 'tie', 
    'doctor', 'chef', 'detective', 'crown', 'shield'
];

// Update UI functions
function updateTransactionsList() {
    const transactionList = document.querySelector('.transaction-list');
    if (!transactionList) return;

    const transactions = userTransactions[currentUserId];

    if (!transactions || transactions.length === 0) {
        transactionList.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-receipt fa-3x mb-3"></i>
                <p class="mb-0">No transactions yet</p>
            </div>`;
        return;
    }

    transactionList.innerHTML = transactions.slice().reverse().map(t => `
        <div class="card bg-dark border-secondary mb-3 transaction-card">
            <div class="card-body p-3">
                <div class="d-flex align-items-center gap-3">
                    <div class="payment-icon">
                        <i class="fas ${t.payment_method_icon} fa-lg"></i>
                    </div>
                    <div class="flex-grow-1">
                        <h6 class="mb-1">${t.description}</h6>
                        <small class="text-muted">${t.date}</small>
                    </div>
                    <div class="text-end">
                        <h6 class="mb-1">₹${parseFloat(t.amount).toFixed(2)}</h6>
                        <small class="text-muted">${t.payment_method_name}</small>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function updateBudgetStatus() {
    const budget = userBudgets[currentUserId] || 0;
    const transactions = userTransactions[currentUserId] || [];
    const totalSpent = transactions.reduce((sum, t) => sum + parseFloat(t.amount), 0);
    const remaining = budget - totalSpent;
    const percentage = budget > 0 ? Math.min((totalSpent / budget * 100), 100) : 0;

    // Update progress bar
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = `${percentage}%`;
        progressBar.setAttribute('aria-valuenow', percentage);
    }

    // Update budget stats
    document.querySelector('[data-budget-stat="spent"]').textContent = `₹${totalSpent.toFixed(2)}`;
    document.querySelector('[data-budget-stat="budget"]').textContent = `₹${budget.toFixed(2)}`;
    document.querySelector('[data-budget-stat="remaining"]').textContent = `₹${remaining.toFixed(2)}`;
}

// Socket.IO event handlers
socket.on('transaction_added', function(data) {
    if (!userTransactions[currentUserId]) {
        userTransactions[currentUserId] = [];
    }
    userTransactions[currentUserId].push(data);
    localStorage.setItem(`${LOCAL_STORAGE_KEYS.TRANSACTIONS}_${currentUserId}`, 
        JSON.stringify(userTransactions[currentUserId]));
    updateTransactionsList();
    updateBudgetStatus();
    hideLoading();
});

socket.on('budget_updated', function(data) {
    userBudgets[currentUserId] = data.budget;
    localStorage.setItem(`${LOCAL_STORAGE_KEYS.BUDGET}_${currentUserId}`, data.budget);
    updateBudgetStatus();
    hideLoading();
});

// User management functions
function switchUser(userId) {
    currentUserId = userId;
    localStorage.setItem(LOCAL_STORAGE_KEYS.CURRENT_USER, userId);
    document.getElementById('currentUser').textContent = userNames[userId];
    document.getElementById('currentUserAvatar').className = `fas fa-user-${userAvatars[userId]} fa-fw`;
    updateTransactionsList();
    updateBudgetStatus();
}

function editUserName() {
    const editUserNameModal = new bootstrap.Modal(document.getElementById('editUserNameModal'));
    document.getElementById('newUserName').value = userNames[currentUserId];

    // Update avatar options
    const avatarContainer = document.getElementById('avatarOptions');
    avatarContainer.innerHTML = AVATARS.map(avatar => `
        <div class="avatar-option">
            <input type="radio" name="avatar" value="${avatar}" id="avatar-${avatar}" 
                   class="d-none" ${userAvatars[currentUserId] === avatar ? 'checked' : ''}>
            <label for="avatar-${avatar}" class="avatar-label">
                <i class="fas fa-user-${avatar} fa-2x"></i>
            </label>
        </div>
    `).join('');

    editUserNameModal.show();
}

function saveUserName() {
    const newName = document.getElementById('newUserName').value.trim();
    const selectedAvatar = document.querySelector('input[name="avatar"]:checked')?.value;

    if (newName && selectedAvatar) {
        userNames[currentUserId] = newName;
        userAvatars[currentUserId] = selectedAvatar;
        localStorage.setItem(LOCAL_STORAGE_KEYS.USER_NAMES, JSON.stringify(userNames));
        localStorage.setItem(LOCAL_STORAGE_KEYS.USER_AVATARS, JSON.stringify(userAvatars));

        document.getElementById('currentUser').textContent = newName;
        document.getElementById('currentUserAvatar').className = `fas fa-user-${selectedAvatar} fa-fw`;

        bootstrap.Modal.getInstance(document.getElementById('editUserNameModal')).hide();
    }
}

// Calculator functions
let calcDisplay = '';

function appendToDisplay(value) {
    calcDisplay += value;
    document.getElementById('calcDisplay').value = calcDisplay;
}

function clearDisplay() {
    calcDisplay = '';
    document.getElementById('calcDisplay').value = '';
}

function calculate() {
    try {
        // Using Function instead of eval for better security
        const result = new Function('return ' + calcDisplay)();
        calcDisplay = result.toString();
        document.getElementById('calcDisplay').value = calcDisplay;
    } catch (error) {
        calcDisplay = '';
        document.getElementById('calcDisplay').value = 'Error';
    }
}

// Initialize calculator modal
const calculatorModal = new bootstrap.Modal(document.getElementById('calculatorModal'));
const calculatorBtn = document.getElementById('calculatorBtn');
if (calculatorBtn) {
    calculatorBtn.addEventListener('click', function() {
        calculatorModal.show();
    });
}

// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize UI with stored data
    updateTransactionsList();
    updateBudgetStatus();
    document.getElementById('currentUser').textContent = userNames[currentUserId];
    document.getElementById('currentUserAvatar').className = `fas fa-user-${userAvatars[currentUserId]} fa-fw`;

    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            showLoading();
        });
    });

    // Auto-dismiss flash messages
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(function(message) {
            const alert = new bootstrap.Alert(message);
            alert.close();
        });
    }, 3000);
});

// Handle page load
window.addEventListener('load', function() {
    hideLoading();
});

// Handle page transitions
window.addEventListener('beforeunload', function() {
    showLoading();
});

// Expose PAYMENT_METHODS for use in transaction updates
const PAYMENT_METHODS = {
    'googlepay': {'name': 'Google Pay', 'icon': 'fa-google-pay'},
    'cash': {'name': 'Cash', 'icon': 'fa-money-bill'},
    'card': {'name': 'Card', 'icon': 'fa-credit-card'},
    'bank': {'name': 'Bank Transfer', 'icon': 'fa-university'},
    'other': {'name': 'Other', 'icon': 'fa-circle-dollar'}
};