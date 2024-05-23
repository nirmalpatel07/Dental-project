


const passwordField = document.getElementById('password');
    const togglePasswordButton = document.getElementById('toggle-password');

    togglePasswordButton.addEventListener('click', function() {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        
        const icon = this.querySelector('img');
        icon.src = type === 'password' ? '/static/images/close-eye.png' : '/static/images/eye.png';
	});



	const loginPasswordField = document.getElementById('login-password');
    const toggleLoginPasswordButton = document.getElementById('toggle-login-password');

    toggleLoginPasswordButton.addEventListener('click', function() {
        const type = loginPasswordField.getAttribute('type') === 'password' ? 'text' : 'password';
        loginPasswordField.setAttribute('type', type);
        
        const icon = this.querySelector('img');
        icon.src = type === 'password' ? '/static/images/close-eye.png' : '/static/images/eye.png';
    });