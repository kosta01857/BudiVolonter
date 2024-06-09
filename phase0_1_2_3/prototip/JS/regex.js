function check_pass(event){
    let pass = document.getElementById('lozinka').value;
    if(pass === ''){
        document.getElementById('pass error').innerHTML = 'Popunite polje';
        event.preventDefault();
    }
    else if(/^\w{8,12}$/.test(pass) == false){
        document.getElementById('pass error').innerHTML = 'Pogresan format'
        event.preventDefault();
    }
    else{ 
        document.getElementById('pass error').innerHTML = '';
    }
}
function check_phone(event){
    let phone = document.getElementById('telefon').value;
    if(phone === ''){
        document.getElementById('tel error').innerHTML = 'Popunite polje';
        event.preventDefault();
    }
    else if(/^\+[0-9]+$/.test(phone) == false){
        document.getElementById('tel error').innerHTML = 'Pogresan format'
        event.preventDefault();
    }
    else{ 
        document.getElementById('tel error').innerHTML = '';
    }
}
function check_pib(event){
    let pib= document.getElementById('pib').value;
    if(pib === ''){
        document.getElementById('pib error').innerHTML = 'Popunite polje';
        event.preventDefault();
        return;
    }
    let num = pib.substring(0,8);
    num = parseInt(num);
    if(num < 10000001){
    document.getElementById('pib error').innerHTML = 'Pogresan format'
    event.preventDefault();
    }
    else if(/^[0-9]{9}$/.test(pib) == false){
        document.getElementById('pib error').innerHTML = 'Pogresan format'
        event.preventDefault();
    }
    else{ 
        document.getElementById('pib error').innerHTML = '';
    }
}
function check_confirm_pass(event){
    let pass = document.getElementById('lozinka').value;
    let confirm_pass = document.getElementById('potvrdiLozinku').value; 
    if(confirm_pass === ''){
        document.getElementById('confirm pass error').innerHTML = 'Popunite polje';
        event.preventDefault();
    }
    else if(confirm_pass !== pass){
        document.getElementById('confirm pass error').innerHTML = "Lozinke i potvrda lozinke se ne poklapaju. Molimo vas da se uverite da oba polja sadrže istu lozinku.";
        event.preventDefault();
    }
    else{ 
        document.getElementById('confirm pass error').innerHTML = '';
    }
}
function check_email(event){
    let email = document.getElementById('email').value;
    if(email === ''){
        document.getElementById('email error').innerHTML = 'Popunite polje';
        event.preventDefault();
    }
    else if(/^[a-zA-Z]\w*@[a-zA-Z]+\.[a-z]{2,3}$/.test(email) == false){
        document.getElementById('email error').innerHTML = 'Pogresan format';
        event.preventDefault();
    }
    else{ 
        document.getElementById('email error').innerHTML = '';
    }
 
}
function check_name(event){
    let name = document.getElementById('ime').value;
    if(name === ''){
        document.getElementById('name error').innerHTML = 'Popunite polje';
        event.preventDefault();
    }
    else if(/[0-9]/.test(name)){
        document.getElementById('name error').innerHTML = 'Ime ne sme sadrzati brojeve';
        event.preventDefault();
    }
    else{ 
        document.getElementById('name error').innerHTML = '';
    }
}
function check_lastname(event){
    let lastname = document.getElementById('prezime').value;
    if(lastname === ''){
        document.getElementById('lastname error').innerHTML = 'Popunite polje';
        event.preventDefault();
    }
    else if(/[0-9]/.test(lastname)){
        document.getElementById('lastname error').innerHTML = 'Prezime ne sme sadrzati brojeve';
        event.preventDefault();
    }
    else{ 
        document.getElementById('lastname error').innerHTML = '';
    }
}
function check_date(event){
    let date = document.getElementById('datumRodjenja').value;
    if(date === ''){
        document.getElementById('date error').innerHTML = 'Popunite polje';
        event.preventDefault();
    }
    else{ 
        document.getElementById('date error').innerHTML = '';
    }
}
function addListeners (){ 
    let btn = document.getElementById('confirm btn');
    btn.addEventListener('click',check_pass);
    btn.addEventListener('click',check_confirm_pass);
    btn.addEventListener('click',check_email);
    btn.addEventListener('click',check_lastname);
    btn.addEventListener('click',check_name); 
    btn.addEventListener('click',check_date);
    btn.addEventListener('click',check_phone)
    btn.addEventListener('click',check_pib);
}